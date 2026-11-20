#!/usr/bin/env python3
# PreToolUse write and shell — the branch lock, asked at every write and every git command that
# changes a repo. A write takes a free repo; a git command never does. Rules: git/lock.py.
#
# ONE QUESTION PER GIT CALL: does it change the repo? A read always passes; a change passes only for
# the holder (lock.change). Every `git` in the command is asked, after heredoc prose is dropped.
#
# FAILS OPEN on a crash only: a gate that dies must never cost a session its edits (Lucas,
# 2026-11-09). A refusal is never an error.
import json
import re
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from hook_input import capability, command_only, parse_stdin  # noqa: E402

GIT = re.compile(r'\bgit\b([^;&|\n)`]*)')
CD = re.compile(r'(?:^|[;&|]\s*)cd\s+([^\s;&|]+)')
CHANGES = {'commit', 'merge', 'rebase', 'reset', 'cherry-pick', 'revert', 'switch', 'checkout',
           'restore', 'push', 'pull', 'stash', 'branch', 'tag', 'am'}
# `git branch` lists unless it is told to create, delete, rename, copy or re-point one.
LISTS = {'--show-current', '--list', '-l', '-a', '--all', '-r', '--remotes', '-v', '-vv', '--verbose',
         '--merged', '--no-merged', '--contains', '--no-contains'}
BRANCH_WRITES = {'-d', '-D', '--delete', '-m', '-M', '--move', '-c', '-C', '--copy', '-f', '--force',
                 '-u', '--set-upstream-to', '--unset-upstream', '--edit-description'}


def calls(command: str, cwd: str):
    """(where, verb, args) for every git call: the repo is `-C <dir>`, else the last `cd` before it."""
    for found in GIT.finditer(command):
        words, where = [w.strip('\'"') for w in found.group(1).split()], None   # sh -c 'git push'
        moved = CD.findall(command[:found.start()])
        base = Path(cwd or '.') / (moved[-1] if moved else '')
        while words and words[0].startswith('-'):
            flag = words.pop(0)
            if flag in ('-C', '-c') and words:
                value = words.pop(0)
                where = base / value if flag == '-C' else where
        if words:
            yield where or base, words[0], words[1:]


def changes(verb: str, args: list) -> bool:
    if verb == 'branch':
        flags = set(args)
        positional = [a for a in args if not a.startswith('-')]
        return bool(flags & BRANCH_WRITES) or (bool(positional) and not flags & LISTS)
    if verb == 'stash':
        return not args or args[0] not in ('list', 'show')
    if verb == 'tag':
        return bool([a for a in args if not a.startswith('-')]) and not {'-l', '--list'} & set(args)
    return verb in CHANGES


def target(verb: str, args: list) -> str:
    """The branch a switch or checkout moves to: its first positional before `--`."""
    if verb not in ('switch', 'checkout'):
        return ''
    for arg in args:
        if arg == '--':
            return ''
        if arg == '-' or not arg.startswith('-'):
            return arg
    return ''


def main() -> int:
    raw, tool, data, session, cwd = parse_stdin()
    try:
        import lock
        cap = capability(tool, data)
        refusal = note = ''
        if cap == 'write' and data.get('file_path'):
            refusal, note = lock.verdict(Path(data['file_path']), session)
        elif cap == 'shell':
            for where, verb, args in calls(command_only(str(data.get('command', ''))), cwd):
                if changes(verb, args) and (refusal := lock.change(where, session, target(verb, args))):
                    break
        else:
            return 0
    except Exception:   # noqa: BLE001 — fail open, see the head
        return 0
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    if note:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'additionalContext': note}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
