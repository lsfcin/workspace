#!/usr/bin/env python3
# PreToolUse and PostToolUse shell — who dirtied a free repo: what a shell call leaves dirty in a governed repo nobody holds is the session's that ran it.
#
# NO READING OF A COMMAND SEES EVERY WRITE: a script, a build, a test run. lock-gate.py refuses the
# writes the text shows; this catches the rest by comparing `git status` before and after, for the
# repos the command names (its cwd, every `cd`, every `git -C`). The session that left the dirt may
# take the repo with it or `git restore` it; anyone else still meets dirt that belongs to nobody
# (panel argon, Lucas 2026-11-23). Only free repos are snapshotted, so a held repo pays nothing.
# FAILS OPEN on a crash, like lock-gate.py. Contract: core/hooks/git/SPECS.md.
import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
import feature_law  # noqa: E402
import lock  # noqa: E402
from hook_input import capability, command_only, parse_stdin  # noqa: E402
from platform_law import locked, session_state  # noqa: E402

CD = re.compile(r'(?:^|[;&|]\s*)cd\s+([^\s;&|]+)')
GIT_C = re.compile(r'\bgit\s+-C\s+([^\s;&|]+)')
ASSIGN = re.compile(r'(?:^|[\s;&|])([A-Za-z_]\w*)=([^\s;&|]+)')
VAR = re.compile(r'\$\{?([A-Za-z_]\w*)\}?')


def expand(command: str, word: str) -> str:
    """`word` with the variables the command assigns, or the environment holds, filled in; '' when
    one stays unknown. `S=/tmp/x; cd $S` is /tmp/x, never a folder named `$S` under the cwd."""
    names = {**os.environ, **{k: v.strip('\'"') for k, v in ASSIGN.findall(command)}}
    filled = VAR.sub(lambda m: names.get(m.group(1), '\0'), word.strip('\'"'))
    return '' if '\0' in filled else os.path.expanduser(filled)


def owners(repo) -> Path:
    """Who dirtied `repo`: one `session<TAB>path` line per path, relative to the repo's root."""
    return session_state('dirt_' + re.sub(r'[^A-Za-z0-9]', '_', str(Path(repo).resolve())) + '.txt')


def _before(session: str) -> Path:
    return session_state('dirt_before_' + re.sub(r'[^A-Za-z0-9-]', '_', session) + '.json')


def free(repo) -> bool:
    return lock.governed(repo) and not lock.holder(repo)[0] \
        and lock.out(repo, 'branch', '--show-current') in lock.SHARED


def dirty(repo) -> set:
    """Every path `git status` reports, one per file, a rename by its new name."""
    found, skip = set(), False
    for entry in lock.git(repo, 'status', '--porcelain=v1', '-z', '--untracked-files=all').stdout.split('\0'):
        if skip or len(entry) < 4:
            skip = False
            continue
        found.add(entry[3:])
        skip = entry[0] in 'RC'   # -z puts the old name of a rename in the next entry
    return found


def places(command: str, cwd: str) -> list:
    """The free governed repos a command can reach: its cwd, every `cd`, every `git -C`."""
    base, found = Path(cwd or '.'), []
    named = [expand(command, d) for d in CD.findall(command) + GIT_C.findall(command)]
    for folder in (base, *(base / d for d in named if d)):
        repo = lock.repo_of(folder)
        if repo and repo not in found and free(repo):
            found.append(repo)
    return found


def snapshot(session: str, command: str, cwd: str) -> None:
    """Pre-shell: what each reachable free repo already has dirty. A clean one forgets its owners."""
    before = {}
    for repo in places(command, cwd):
        before[str(repo)] = sorted(dirty(repo))
        if not before[str(repo)]:
            owners(repo).unlink(missing_ok=True)
    _before(session).write_text(json.dumps(before), encoding='utf-8', newline='\n')


def attribute(session: str) -> dict:
    """Post-shell: the paths that turned dirty since the snapshot are this session's, by repo."""
    path = _before(session)
    if not path.is_file():
        return {}
    before, touched = json.loads(path.read_text(encoding='utf-8')), {}
    path.unlink()
    for repo, old in before.items():
        if new := dirty(repo) - set(old):
            with locked(owners(repo).with_suffix('.flock')), \
                    owners(repo).open('a', encoding='utf-8', newline='\n') as rows:
                rows.writelines(f'{session}\t{name}\n' for name in sorted(new))
            touched[repo] = sorted(new)
    return touched


def undo(repo, names: list) -> str:
    """The one shell line that hands `names` back: restore the tracked ones, clean the new ones."""
    tracked, q = set(lock.out(repo, 'ls-files', '--', *names).splitlines()), shlex.quote
    parts = [(verb, [n for n in names if (n in tracked) == keep]) for verb, keep in (('restore', True), ('clean -fq', False))]
    return ' && '.join(f'git -C {q(str(repo))} {verb} -- ' + ' '.join(map(q, picked)) for verb, picked in parts if picked)


def mine(repo, session: str) -> set:
    path = owners(repo)
    rows = [line.split('\t', 1) for line in path.read_text(encoding='utf-8').splitlines()] if path.is_file() else []
    return {row[1] for row in rows if len(row) == 2 and row[0] == session}


def owns(repo, session: str) -> bool:
    """Every dirty path in `repo` is this session's, so `take` may carry it onto the new feature."""
    now = dirty(repo)
    return bool(now) and now <= mine(repo, session)


def restores(where, session: str, verb: str, args: list) -> bool:
    """`git restore|clean <paths>` or `git checkout -- <paths>` on paths this session dirtied: its own undo."""
    if verb not in ('restore', 'checkout', 'clean') or not session:
        return False
    names = args[args.index('--') + 1:] if '--' in args else \
        [a for a in args if not a.startswith('-')] if verb != 'checkout' else []
    repo = lock.repo_of(where)
    if not names or not repo:
        return False
    own = mine(repo, session)
    try:
        return all((Path(where) / n).resolve().relative_to(repo).as_posix() in own for n in names)
    except ValueError:
        return False


def main() -> int:
    try:
        raw, tool, data, session, cwd = parse_stdin()
        if not session or capability(tool, data) != 'shell' or not feature_law.is_enabled('branch-lock'):
            return 0
        if str(raw.get('hook_event_name') or raw.get('hookEventName') or 'PreToolUse') != 'PostToolUse':
            snapshot(session, command_only(str(data.get('command', ''))), cwd)
            return 0
        if left := attribute(session):
            lines = ''.join(f'\n   {repo}: carry it with core/run tools/wos/take {shlex.quote(str(repo))} <name>,'
                            f' or undo it with {undo(repo, names)}' for repo, names in left.items())
            print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext':
                f'[Git] this command left dirt in a repo nobody holds. The dirt is yours:{lines}'}}))
    except Exception:   # noqa: BLE001 — fail open, see the head
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
