#!/usr/bin/env python3
# The branch is the lock: one agent session per repo, held by standing on the branch it created.
#
# A governed repo (it has `develop`, and its origin is the profile's GitHub owner) is FREE on a
# shared branch with a clean tree. `core/run tools/wos/take <repo> <name>` takes it — fetch, pull
# --ff-only, a new feature/<name> and a lock file naming the session, all under one flock — and the
# close gives it back. A write to a free repo is refused until then: the branch says its work, so the
# session names it (2026-11-23, Lucas). `core/run tools/wos/claim` hands a repo over on Lucas's word.
# The rules bind agents only: no session id, no gate (ruled 2026-11-19, Lucas).
# Contract: core/hooks/git/SPECS.md.
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_HOOKS))
import feature_law  # noqa: E402
from platform_law import locked, rel, session_state  # noqa: E402

SHARED = ('main', 'master', 'develop')
NAME = re.compile(r'[a-z0-9][a-z0-9-]*')   # an id from ROADMAP or ISSUES fits; a folder does not
WORKSPACE = _HOOKS.parents[1]
# The ids an agent's shell exports, so a git hook it spawns knows it is an agent's commit.
SESSION_ENV = ('CLAUDE_CODE_SESSION_ID', 'CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_SESSION_ID')


def git(repo, *args) -> subprocess.CompletedProcess:
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True, encoding='utf-8')


def out(repo, *args) -> str:
    done = git(repo, *args)
    return done.stdout.strip() if done.returncode == 0 else ''


def repo_of(path) -> Path | None:
    folder = Path(path)
    while not folder.is_dir() and folder != folder.parent:
        folder = folder.parent
    top = out(folder, 'rev-parse', '--show-toplevel')
    return Path(top).resolve() if top else None


def owned(repo) -> bool:
    """Origin's GitHub owner is the profile's `github-owner`: a clone of someone else's repo, or a
    paper on Overleaf, is never merged or pushed by a hook or a close."""
    match = re.search(r'github\.com[:/]([^/]+)/', out(repo, 'config', '--get', 'remote.origin.url'))
    owner = feature_law.setting('github-owner')
    return bool(match and owner) and match.group(1).lower() == owner.lower()


def governed(repo) -> bool:
    """Owned and has `develop`: the repos the lock holds. An owned repo without one is a trunk."""
    return bool(out(repo, 'rev-parse', '--verify', '-q', 'refs/heads/develop')) and owned(repo)


def lock_file(repo) -> Path:
    return session_state('lock_' + re.sub(r'[^A-Za-z0-9]', '_', str(Path(repo).resolve())) + '.txt')


def holder(repo) -> tuple:
    """(session, branch) holding `repo`, or ('', '')."""
    path = lock_file(repo)
    parts = path.read_text(encoding='utf-8').rstrip('\n').split('\t') if path.is_file() else []
    return (parts[0], parts[1]) if len(parts) >= 3 else ('', '')


def _hold(repo, session: str, branch: str) -> None:
    lock_file(repo).write_text(f'{session}\t{branch}\t{Path(repo).resolve()}\n',
                               encoding='utf-8', newline='\n')


def held_by(session: str) -> list:
    """Every repo this session holds — what the close covers."""
    found = []
    for path in lock_file(WORKSPACE).parent.glob('lock_*.txt'):
        try:   # a lock another close is dropping right now is simply not held
            row = path.read_text(encoding='utf-8').rstrip('\n').split('\t')
        except OSError:
            continue
        if len(row) >= 3 and row[0] == session:
            found.append(Path(row[2]))
    return found


def release(repo, session: str) -> None:
    with locked(lock_file(repo).with_suffix('.flock')):
        if holder(repo)[0] == session:
            lock_file(repo).unlink(missing_ok=True)


def _dirty(repo) -> str:
    return '' if not out(repo, 'status', '--porcelain') else (
        f'⛔ BRANCH LOCK [dirty] — {_name(repo)} has uncommitted changes nobody holds.\n'
        '   They are not this session\'s. Ask Lucas to commit or stash them, then retry.')


def _exists(repo, branch: str) -> bool:
    return any(out(repo, 'rev-parse', '--verify', '-q', ref) for ref in (f'refs/heads/{branch}',
                                                                          f'refs/remotes/origin/{branch}'))


def claim(repo, session: str, name: str = '') -> tuple:
    """(refusal, previous holder): hand `repo` to `session`, on feature/<name> when named, else on
    the branch it stands on. Switching needs a clean tree; a branch only origin has is checked out."""
    with locked(lock_file(repo).with_suffix('.flock')):
        before, branch = holder(repo)[0], f'feature/{name}'
        if name and out(repo, 'branch', '--show-current') != branch:
            if refusal := _dirty(repo):
                return refusal, before
            git(repo, 'fetch', '-q', 'origin')
            if not _exists(repo, branch):
                return f'⛔ claim — no branch {branch} in {_name(repo)} or its origin.', before
            if git(repo, 'switch', '-q', branch).returncode != 0:
                return f'⛔ claim — could not switch {_name(repo)} to {branch}.', before
        _hold(repo, session, out(repo, 'branch', '--show-current'))
    return '', before


def _name(repo) -> str:
    return 'the workspace' if repo == WORKSPACE else rel(repo, WORKSPACE)


def take(repo, session: str, name: str) -> tuple:
    """(refusal, note): a clean shared branch nobody holds — pull develop, branch feature/<name> off it."""
    branch = f'feature/{name}'
    if not session or not feature_law.is_enabled('branch-lock') or not governed(repo):
        return '', ''
    if not NAME.fullmatch(name or ''):
        return f'⛔ take — "{name}" is not a name: [a-z0-9-], an id from ROADMAP or ISSUES when one fits.', ''
    with locked(lock_file(repo).with_suffix('.flock')):
        owner, held = holder(repo)
        head = out(repo, 'branch', '--show-current')
        if owner == session:
            return f'⛔ take — you already hold {_name(repo)} on {held}; one session, one branch.', ''
        if owner or head not in SHARED:
            return _not_yours(repo, session, owner, held, head), ''
        import dirt   # noqa: PLC0415 — dirt imports this module
        if not dirt.owns(repo, session) and (refusal := _dirty(repo)):
            return refusal, ''   # dirt only this session's shell left travels with its take
        fetched = git(repo, 'fetch', '-q', 'origin').returncode == 0
        if _exists(repo, branch):
            return (f'⛔ take — {branch} already exists in {_name(repo)} or its origin.\n'
                    f'   Pick another name, or resume it on Lucas\'s word: core/run tools/wos/claim {repo} {name}'), ''
        if git(repo, 'switch', '-q', 'develop').returncode != 0 or \
                (fetched and git(repo, 'merge', '-q', '--ff-only', 'origin/develop').returncode != 0):
            return (f'⛔ BRANCH LOCK [diverged] — develop in {_name(repo)} cannot fast-forward to origin.\n'
                    '   It diverged; that is Lucas\'s to settle.'), ''
        if git(repo, 'switch', '-q', '-c', branch).returncode != 0:
            return f'⛔ BRANCH LOCK [branch] — could not create {branch} in {_name(repo)}.', ''
        _hold(repo, session, branch)
        dirt.owners(repo).unlink(missing_ok=True)
    return '', (f'[Git] {_name(repo)} is yours on {branch}' + ('' if fetched else ' (offline: not pulled)')
                + f'. The close merges it into develop. Session: {session}')


def verdict(path, session: str) -> tuple:
    """(refusal, note) for this session acting on the repo holding `path`. Never takes a free repo."""
    repo = repo_of(path)
    if not session or not repo or not feature_law.is_enabled('branch-lock') or not governed(repo):
        return '', ''
    with locked(lock_file(repo).with_suffix('.flock')):
        owner, branch = holder(repo)
        head = out(repo, 'branch', '--show-current')
        if owner == session:
            if head == branch or not head:
                return '', ''
            if head in SHARED:
                return (f'⛔ BRANCH LOCK [off-feature] — you hold {_name(repo)} on {branch}, but it is on {head}.\n'
                        f'   git -C {shlex.quote(str(repo))} switch {shlex.quote(branch)}'), ''
            _hold(repo, session, head)   # nobody else can switch a held repo: this was ours
            return '', ''
        return _not_yours(repo, session, owner, branch, head), ''


def _not_yours(repo, session: str, owner: str, branch: str, head: str) -> str:
    """Why `session` may not change a repo it does not hold. The one place each refusal is worded: a
    stable [code], and a command only when running it is the agent's to do — a runnable claim tempted
    agents to take a live lock (2026-11-23)."""
    if owner:
        return (f'⛔ BRANCH LOCK [held] — {_name(repo)} is held by session {owner} on {branch}.\n'
                '   Work elsewhere, or wait for its close. Handing it over is Lucas\'s call: tell him.')
    if head not in SHARED:
        return (f'⛔ BRANCH LOCK [unheld] — {_name(repo)} is on {head or "a detached HEAD"}, held by nobody.\n'
                '   Resuming work nobody holds is Lucas\'s call: tell him.')
    return (f'⛔ BRANCH LOCK [free] — {_name(repo)} is free: name the work before changing it.\n'
            f'   core/run tools/wos/take {shlex.quote(str(repo))} <name>   ([a-z0-9-]; the ROADMAP or ISSUES id when one fits)')


def change(path, session: str, target: str = '') -> str:
    """Refusal for a git command that changes the repo holding `path` (lock-gate.py classifies it).
    Only the holder may, and the holder never moves itself onto a shared branch: leaving the feature
    is the close's job. `target` is the branch a switch or checkout names."""
    repo = repo_of(path)
    if not session or not repo or not feature_law.is_enabled('branch-lock') or not governed(repo):
        return ''
    with locked(lock_file(repo).with_suffix('.flock')):
        owner, branch = holder(repo)
        if owner == session:
            return '' if target not in (*SHARED, '-') else (
                f'⛔ BRANCH LOCK [leave] — leaving {branch} is the close\'s job: core/run tools/wos/roundup')
        return _not_yours(repo, session, owner, branch, out(repo, 'branch', '--show-current'))


def env_session() -> str:
    return next((os.environ[k] for k in SESSION_ENV if os.environ.get(k)), '')


def check(commit) -> None:
    """Pre-commit: an agent never commits on a shared branch of a governed repo. A person may."""
    from pre_commit import Blocked  # noqa: PLC0415
    branch = out(commit.toplevel, 'branch', '--show-current')
    if not env_session() or branch not in SHARED or not feature_law.is_enabled('branch-lock') \
            or Path(commit.toplevel, out(commit.toplevel, 'rev-parse', '--git-dir'), 'MERGE_HEAD').exists() \
            or not governed(commit.toplevel):
        return
    raise Blocked(f'⛔ BRANCH LOCK [shared] — an agent commits on a feature branch, never on {branch}.\n'
                  f'   core/run tools/wos/take {shlex.quote(str(commit.toplevel))} <name>')
