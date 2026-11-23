#!/usr/bin/env python3
# PreToolUse write and shell — the branch lock, asked at every write, every shell write its text shows, and every git command that changes a repo. Rules: git/lock.py.
#
# ONE QUESTION PER GIT CALL: does it touch the checkout — HEAD, the index or the files? The lock owns
# the checkout, the one thing two sessions on one clone can clobber. A read, or a call that moves only
# refs or the remote, passes for anyone; one that touches the checkout passes only for the holder
# (lock.change). A verb not listed here touches it. Every `git` in the command is asked, after heredoc
# prose is dropped.
#
# FAILS OPEN on a crash only: a gate that dies must never cost a session its edits (Lucas,
# 2026-11-09). A refusal is never an error.
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from dirt import CD, expand, restores  # noqa: E402
from hook_input import capability, command_only, parse_stdin  # noqa: E402

# `git` as a command word: a path through a `git/` folder (`core/hooks/git/lock.py`) is not a call.
GIT = re.compile(r'(?:^|(?<=[\s;&|(`\'"]))git(?=\s|$)([^;&|\n)`]*)', re.M)
READS = {'archive', 'status', 'log', 'diff', 'show', 'rev-parse', 'rev-list', 'ls-files', 'ls-tree', 'ls-remote',
         'cat-file', 'blame', 'grep', 'describe', 'shortlog', 'for-each-ref', 'show-ref', 'merge-base',
         'reflog', 'name-rev', 'check-ignore', 'show-branch', 'cherry', 'range-diff', 'diff-tree'}
# Verbs that read only in these forms, named by their first argument.
READ_FORMS = {'stash': {'list', 'show'}, 'remote': {'-v', '--verbose', 'show', 'get-url'},
              'config': {'--get', '--get-all', '--get-regexp', '--list', '-l', 'get', 'list'}}
# Verbs that move only refs or the remote, except these forms, which reach HEAD (git refuses the rest
# on the branch in checkout). `push .` is a push into this very clone.
HEREDOC = Path(__file__).resolve().parents[1] / 'checks/heredoc-gate.py'
REFS = {'fetch': {'--update-head-ok', '-u'}, 'push': {'.'}, 'tag': set(), 'branch': {'-m', '-M', '--move'}}


def calls(command: str, cwd: str):
    """(where, verb, args) for every git call: the repo is `-C <dir>`, else the last `cd` before it,
    with the command's own variables filled in."""
    for found in GIT.finditer(command):
        words, where = [w.strip('\'"') for w in found.group(1).split()], None   # sh -c 'git push'
        moved = CD.findall(command[:found.start()])
        last = expand(command, moved[-1]) if moved else '.'
        base, known = Path(cwd or '.') / (last or '.'), bool(last)
        while words and words[0].startswith('-'):
            flag = words.pop(0)
            if flag in ('-C', '-c') and words:
                value = expand(command, words.pop(0)) if flag == '-C' else ''
                known, where = (known and bool(value), base / (value or '.')) if flag == '-C' else (known, where)
        if words and known:   # a folder the command never names is no repo to ask: fail open
            yield where or base, words[0], words[1:]


def changes(verb: str, args: list) -> bool:
    """Does this call touch the checkout? A verb listed nowhere does."""
    if verb in REFS:
        return bool(REFS[verb] & set(args))
    if verb in READ_FORMS:
        return not args or args[0] not in READ_FORMS[verb]
    return verb not in READS


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
        repo = lock.repo_of(path)
        if path not in found and not (repo and lock.git(repo, 'check-ignore', '-q', str(path)).returncode == 0):
            found.append(path)
    return found


def main() -> int:
    raw, tool, data, session, cwd = parse_stdin()
    try:
        import lock
        cap = capability(tool, data)
        refusal = note = ''
        if cap == 'write' and data.get('file_path'):
            refusal, note = lock.verdict(Path(data['file_path']), session)
        elif cap == 'shell':
            command = str(data.get('command', ''))
            for where, verb, args in calls(command_only(command), cwd):
                if changes(verb, args) and not restores(where, session, verb, args) \
                        and (refusal := lock.change(where, session, target(verb, args))):
                    reason = f'git {verb} touches the checkout; a read missing from READS in lock-gate.py is one line there.'
                    break
            else:
                for path in writes(command, cwd):
                    if refusal := lock.verdict(path, session)[0]:
                        reason = f'this command writes {path}, and a shell write meets the lock an Edit does.'
                        break
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
