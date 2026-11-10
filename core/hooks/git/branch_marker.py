#!/usr/bin/env python3
# Branch drift: HEAD is shared mutable state between parallel sessions, so each session keeps the
# branch it chose, per repo, and is stopped before writing on one it did not choose.
#
# `record` stores the branch at SessionStart; `verdict` answers the branch gate at every write;
# `follow` re-reads the branch after this session's own git switch; `check` warns at commit time.
# ONE MARKER PER SESSION AND REPO since 2026-11-09: a marker per repo could not tell this session's
# own switch from a parallel one's, so it could only warn. Keyed by session it can block, and the
# blocks are kept narrow on purpose (Lucas: a gate blocking sessions in a way nobody predicted is
# the bigger headache) — every rule below that can refuse names the one command that unblocks it.
#   A SWITCH THIS SESSION MADE IS NEVER A DRIFT: follow() re-records after its own git commands.
#   LEAVING A FINISHED BRANCH IS NEVER A DRIFT: one already integrated into develop is done.
#   A BROKEN QUESTION PASSES: no repo, detached HEAD, no session, git failing — all silent.
#
# Decided 2026-08-14 (Lucas) over one-worktree-per-session, which fights the branch sweep in
# core/skills/roundup.md Phase 5 -- a checked-out worktree makes `git branch -d` refuse.
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(_HOOKS), str(_HOOKS / 'commit'), str(Path(__file__).resolve().parent)]
from gitflow_gate import SHARED, enforced  # noqa: E402
from platform_law import rel, session_state  # noqa: E402
from pre_commit import git  # noqa: E402

ROOT = _HOOKS.parents[1]
PREFIX = 'claude_branch_'


def _key(text: str) -> str:
    return re.sub(r'[^A-Za-z0-9]', '_', text)


def marker_for(repo, session: str) -> Path:
    """The marker file for one session in one repo. The ONE place this path is spelled.

    Asked of the boundary, never built here: a marker in the temp directory does not survive a
    reboot a session survives (b20260922). Holds two lines: the branch, then the repo it is for,
    so follow() can re-read every repo this session holds without guessing them.
    """
    return session_state(f'{PREFIX}{_key(session)}__{_key(str(Path(repo).resolve()))}.txt')


def env_session() -> str:
    """The session a git hook runs under: inherited from the agent's shell, or ''."""
    for name in ('CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_SESSION_ID'):
        if os.environ.get(name):
            return os.environ[name]
    return ''


def _repo(path) -> Path | None:
    folder = Path(path)
    while not folder.is_dir() and folder != folder.parent:
        folder = folder.parent
    top = git('rev-parse', '--show-toplevel', cwd=folder)
    return Path(top) if top else None


def _branch(repo) -> str:
    """`--show-current`: it names an unborn branch, and prints nothing on a detached HEAD."""
    return git('branch', '--show-current', cwd=repo)


def _started(marker: Path) -> str:
    return marker.read_text(encoding='utf-8', errors='replace').split('\n')[0].strip() \
        if marker.is_file() else ''


def _write(marker: Path, branch: str, repo) -> None:
    marker.write_text(f'{branch}\n{Path(repo).resolve()}\n', encoding='utf-8', newline='\n')


def finished(repo, branch: str) -> bool:
    """Whether `branch` is done: gone, or already inside develop (main where there is none)."""
    if not git('rev-parse', '--verify', '-q', f'refs/heads/{branch}', cwd=repo):
        return True
    base = 'develop' if git('rev-parse', '--verify', '-q', 'refs/heads/develop', cwd=repo) else 'main'
    # A returncode, not stdout: --is-ancestor answers by exit status alone, which git() discards.
    return subprocess.run(['git', 'merge-base', '--is-ancestor', branch, base], cwd=repo,
                          capture_output=True).returncode == 0


def record(repo=None, session: str = '') -> None:
    """Store the branch this session started on."""
    top = _repo(repo or Path.cwd())
    branch = _branch(top) if top else ''
    if top and branch and session:
        _write(marker_for(top, session), branch, top)


def _features(repo) -> str:
    return git('for-each-ref', '--sort=-committerdate', '--count=8',
               '--format=     %(refname:short)  (%(committerdate:short))', 'refs/heads/feature/',
               cwd=repo) or '     (none yet)'


def verdict(path, session: str) -> tuple:
    """(refusal, note) for a write to `path`; both '' when there is nothing to say."""
    repo = _repo(path)
    if not repo or not session or not enforced(repo, ROOT):
        return '', ''
    branch = _branch(repo)
    if not branch:
        return '', ''
    name = rel(repo, ROOT) if repo.resolve() != ROOT.resolve() else 'the workspace'
    if branch in SHARED:
        return (f"⛔ BRANCH GATE — {name} is on '{branch}', which only moves by promotion.\n"
                '   Pick this task\'s branch before the first edit:\n'
                f'     git -C {repo} switch -c feature/<task> develop\n'
                f'   or carry on an unfinished one:  git -C {repo} switch feature/<name>\n'
                f'   Most recent here:\n{_features(repo)}'), ''
    marker = marker_for(repo, session)
    started = _started(marker)
    if started == branch:
        return '', ''
    if started and not finished(repo, started):
        return (f"⛔ BRANCH GATE — {name} moved from '{started}' to '{branch}', and not by this "
                'session.\n   A parallel session switched the shared checkout; this edit would land '
                'on its branch.\n'
                f'   If {branch} is right for this task, say so and retry:  git -C {repo} switch {branch}\n'
                '   Never switch back while the other session works there. Ask Lucas.'), ''
    _write(marker, branch, repo)
    last = git('log', '-1', '--format=%cs: %s', cwd=repo) or 'no commit yet'
    return '', f'[Git] Writing in {name} on {branch} (last commit {last}). Is it this task\'s branch?'


def follow(session: str) -> None:
    """Re-record every repo this session holds: called after its own git switch or checkout."""
    if not session:
        return
    for marker in session_state('x').parent.glob(f'{PREFIX}{_key(session)}__*.txt'):
        lines = marker.read_text(encoding='utf-8', errors='replace').split('\n')
        branch = _branch(lines[1]) if len(lines) > 1 and Path(lines[1]).is_dir() else ''
        if branch:
            _write(marker, branch, lines[1])


def check(commit):
    """Warn when HEAD has moved under this session. Never raises -- warn, never block."""
    session, branch = env_session(), _branch(commit.toplevel)
    marker = marker_for(commit.toplevel, session) if session else None
    started = _started(marker) if marker else ''
    if not branch or not started or started == branch:
        return
    print(f"[Git] ⚠ HEAD moved since this session started: '{started}' → '{branch}'.")
    print('   A parallel session may have switched the shared checkout, and this commit is')
    print('   about to land on their branch. If it should be yours:')
    print(f'   git merge-base --is-ancestor {started} HEAD  &&  git branch -f {started} HEAD')
    print('   Never reset or force-push theirs. See core/hooks/SPECS.md § Branch drift.')
    _write(marker, branch, commit.toplevel)


def _payload_session() -> str:
    """SessionStart sends its id on stdin; a terminal or an empty stdin sends nothing."""
    try:
        data = json.loads(sys.stdin.read() or '{}') if not sys.stdin.isatty() else {}
    except (ValueError, OSError):
        data = {}
    return str(data.get('session_id') or '') if isinstance(data, dict) else ''


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'record':
        record(session=_payload_session() or env_session())
        return 0
    if mode == 'check':
        from pre_commit import collect
        check(collect())
        return 0
    print('usage: branch_marker.py record|check', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
