#!/usr/bin/env python3
# PreToolUse write and shell — the branch lock, asked at every write and every shell write its text shows; git is judged by its own wrapper. Rules: git/lock.py.
#
# A git call is never read from the command's text (Lucas, 2026-11-24, panels P1 and P3): the wrapper
# in front of git (core/hooks/git/git, wrapper.py) judges the real argv and cwd, whoever spawns it. This
# gate refuses a shell call from a harness whose PATH does not reach that wrapper, since none of its git
# calls would be judged; then the raw move of a governed repo, then a write its text shows.
#
# FAILS OPEN on a crash only: a gate that dies must never cost a session its edits (Lucas,
# 2026-11-09). A refusal is never an error.
import importlib.util
import json
import re
import shlex
import shutil
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from dirt import CD, expand  # noqa: E402
from hook_input import capability, command_only, parse_stdin  # noqa: E402

HEREDOC = Path(__file__).resolve().parents[1] / 'checks/heredoc-gate.py'
MV = re.compile(r'(?:^|(?<=[\s;&|(]))mv\s+([^;&|\n)]+)', re.M)
WRAPPER = Path(__file__).resolve().parent / 'git'


def wrapped() -> bool:
    """Does `git` on this harness's PATH reach the wrapper? Without it, no git call is judged."""
    found = shutil.which('git')
    return bool(found) and Path(found).resolve() == WRAPPER


def writes(command: str, cwd: str) -> list:
    """Paths the shell's own text writes, read by checks/heredoc-gate.py's arms, relative to the last
    `cd`. An ignored path is dropped: it dirties no tree, so it never strands a repo."""
    import lock   # noqa: PLC0415
    spec = importlib.util.spec_from_file_location('heredoc_gate', HEREDOC)
    heredoc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(heredoc)
    moved = CD.findall(command)
    last = expand(command, moved[-1]) if moved else '.'
    if not last:
        return []   # a folder the command never names: fail open, as calls() does
    base, found = Path(cwd or '.') / last, []
    for name in heredoc.candidates(command, str(base), every_line=True):
        path = Path(name).expanduser()
        path = (path if path.is_absolute() else base / path).resolve()
        if path not in found and not lock.ignored(path):
            found.append(path)
    return found


def moves(command: str, cwd: str) -> list:
    """(from, to) for every `mv` of a governed repo's root: a raw move strands its lock (wos/move)."""
    import lock   # noqa: PLC0415
    found = []
    for hit in MV.finditer(command):
        words = [expand(command, w.strip('\'"')) for w in hit.group(1).split() if not w.startswith('-')]
        moved = CD.findall(command[:hit.start()])
        base = Path(cwd or '.') / (expand(command, moved[-1]) if moved else '.')
        if len(words) < 2 or not all(words):
            continue   # a name the command never fills: fail open, as calls() does
        paths = [(base / Path(w).expanduser()).resolve() for w in words]
        found += [(src, paths[-1]) for src in paths[:-1]
                  if src.is_dir() and lock.repo_of(src) == src and lock.governed(src)]
    return found


def shell(command: str, cwd: str, session: str) -> tuple:
    """(refusal, reason) for a shell command: no wrapper, a raw move of a repo, then a write."""
    import feature_law   # noqa: PLC0415
    import lock   # noqa: PLC0415
    if session and not wrapped() and feature_law.is_enabled('branch-lock') and 'wos/gitwrap' not in command:
        return ('⛔ BRANCH LOCK [unwrapped] — git on this PATH is not the branch-lock wrapper, so no git call'
                ' here would be judged.\n   core/run tools/wos/gitwrap --install'), 'install it, then retry.'
    bare = command_only(command)
    for src, dst in moves(bare, cwd) if session else []:
        return (f'⛔ BRANCH LOCK [move] — {src} is a governed repo, and its lock is keyed by its path.',
                f'a raw mv strands that lock. Run instead:\n     core/run tools/wos/move '
                f'{shlex.quote(str(src))} {shlex.quote(str(dst))}')
    for path in writes(command, cwd):
        if refusal := lock.verdict(path, session)[0]:
            return refusal, f'this command writes {path}, and a shell write meets the lock an Edit does.'
    return '', ''


def main() -> int:
    raw, tool, data, session, cwd = parse_stdin()
    try:
        import lock
        cap = capability(tool, data)
        refusal = note = ''
        if cap == 'write' and data.get('file_path'):
            refusal, note = lock.verdict(Path(data['file_path']), session)
        elif cap == 'shell':
            refusal, reason = shell(str(data.get('command', '')), cwd, session)
        else:
            return 0
    except Exception:   # noqa: BLE001 — fail open, see the head
        return 0
    if refusal:
        print(f'{refusal}\n   Refused: {reason}' if cap == 'shell' else refusal, file=sys.stderr)
        return 2
    if note:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'additionalContext': note}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
