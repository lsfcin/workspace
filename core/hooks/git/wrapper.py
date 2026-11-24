#!/usr/bin/env python3
# git, through the branch lock: the half of core/hooks/git/git that needs Python — who calls, what the call touches, and whether that session holds the repo.
#
# ONE QUESTION PER CALL: does it touch the checkout — HEAD, the index or the files? The lock owns the
# checkout, the one thing two sessions on one clone can clobber. A read, or a call that moves only refs
# or the remote, passes for anyone; one that touches the checkout passes only for the repo's holder
# (lock.change). A verb not listed here touches it. The call is judged from its real argv and cwd, so a
# script, a subprocess or an alias meets the lock the shell does (decided 2026-11-24, panels P1 and P3).
#
# WHO CALLS: the session id the shell carries (lock.SESSION_ENV), else the nearest ancestor process a
# harness shim registered (register), matched by pid AND start time. Neither: a person, never gated.
#
# FAILS OPEN on a crash, loudly: one line on stderr and one in core/state/git_wrapper.log (Lucas, 2026-11-24).
import os
import sys
import time
import traceback
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from platform_law import ancestors, real_git, session_state  # noqa: E402

READS = {'archive', 'status', 'log', 'diff', 'show', 'rev-parse', 'rev-list', 'ls-files', 'ls-tree', 'ls-remote',
         'cat-file', 'blame', 'grep', 'describe', 'shortlog', 'for-each-ref', 'show-ref', 'merge-base',
         'reflog', 'name-rev', 'check-ignore', 'show-branch', 'cherry', 'range-diff', 'diff-tree', 'version',
         'help', 'var', 'check-ref-format', 'hash-object'}
# Verbs that read only in these forms, named by their first argument.
READ_FORMS = {'stash': {'list', 'show'}, 'remote': {'-v', '--verbose', 'show', 'get-url'},
              'config': {'--get', '--get-all', '--get-regexp', '--list', '-l', 'get', 'list'}}
# Verbs that move only refs or the remote, except these forms, which reach HEAD (git refuses the rest
# on the branch in checkout). `push .` is a push into this very clone.
REFS = {'fetch': {'--update-head-ok', '-u'}, 'push': {'.'}, 'tag': set(), 'branch': {'-m', '-M', '--move'}}
# git's own options that take the next word as their value (`--git-dir=x` carries it inside).
VALUED = {'-C', '-c', '--git-dir', '--work-tree', '--namespace', '--config-env', '--attr-source'}
# Processes that host more than one session, or a person's terminal beside an agent: registering one
# would hand a person's git to an agent (panel P3: the editor's root and its pty host).
SHARED_HOSTS = {'code', 'electron', 'ptyHost', 'systemd', 'init', 'tmux: server', 'screen', 'sshd', 'login'}
# A harness may run its hook through a shell (agy: `sh -c "cd … && sh core/run …"`); that shell dies
# with the hook, so the host is the first ancestor that is not one (2026-11-24, the agy e2e).
SHELLS = {'sh', 'bash', 'dash', 'zsh'}


def parse(argv: list) -> tuple:
    """(options, verb, args): git's own options before the verb, the verb, and what follows it."""
    i = 0
    while i < len(argv) and argv[i].startswith('-'):
        i += 2 if argv[i] in VALUED else 1
    return argv[:i], (argv[i] if i < len(argv) else ''), argv[i + 1:]


def changes(verb: str, args: list) -> bool:
    """Does this call touch the checkout? A verb listed nowhere does."""
    if verb in REFS:
        return bool(REFS[verb] & set(args))
    if verb in READ_FORMS:
        return not args or args[0] not in READ_FORMS[verb]
    return bool(verb) and verb not in READS


def target(verb: str, args: list) -> str:
    """The branch a switch or checkout moves to: its one positional. A checkout naming paths too
    (`checkout develop -- f.py`, `checkout develop f.py`) restores files and moves nothing."""
    if verb not in ('switch', 'checkout'):
        return ''
    named = [a for a in args if a == '-' or not a.startswith('-')]
    if verb == 'checkout' and ('--' in args or len(named) > 1):
        return ''
    return named[0] if named else ''


def _entry(pid) -> Path:
    return session_state(f'agent_pid_{pid}.txt')


def register(session: str, pid: int) -> None:
    """A harness whose shell carries no session id names its host process `pid` here, at every tool
    call; git then finds it among its ancestors. Dead and reused pids are pruned on the way."""
    chain = ancestors(pid)
    while chain and chain[0][2] in SHELLS:
        chain = chain[1:]
    if not session or not chain or chain[0][2] in SHARED_HOSTS:
        return
    pid = chain[0][0]
    for old in _entry('x').parent.glob('agent_pid_*.txt'):
        held = old.read_text(encoding='utf-8').split('\t')
        alive = ancestors(int(old.stem[10:]))
        if len(held) < 2 or not alive or alive[0][1] != held[1].strip():
            old.unlink(missing_ok=True)
    row = f'{session}\t{chain[0][1]}\n'
    if not _entry(pid).is_file() or _entry(pid).read_text(encoding='utf-8') != row:
        _entry(pid).write_text(row, encoding='utf-8', newline='\n')


def session() -> str:
    """The calling agent session, or '' for a person."""
    import lock   # noqa: PLC0415
    if named := next((os.environ[k] for k in lock.SESSION_ENV if os.environ.get(k)), ''):
        return named
    for pid, start, _ in ancestors():
        if _entry(pid).is_file():
            held = _entry(pid).read_text(encoding='utf-8').split('\t')
            if len(held) >= 2 and held[1].strip() == start:
                return held[0]
    return ''


def judge(argv: list, cwd: str, caller: str) -> str:
    """The refusal for this call, or ''."""
    import subprocess   # noqa: PLC0415
    import lock   # noqa: PLC0415
    from dirt import restores   # noqa: PLC0415
    options, verb, args = parse(argv)
    if not caller or not changes(verb, args):
        return ''
    # The repo as git itself resolves it, through the same -C, --git-dir and --work-tree.
    top = subprocess.run([real_git(), *options, 'rev-parse', '--show-toplevel'], cwd=cwd,
                         capture_output=True, text=True, encoding='utf-8').stdout.strip()
    where = Path(cwd)
    for flag, value in zip(options, options[1:]):
        where = where / value if flag == '-C' else where   # each -C is relative to the one before
    if not top or restores(where, caller, verb, args):
        return ''
    refusal = lock.change(top, caller, target(verb, args))
    return f'{refusal}\n   Refused: git {verb} touches the checkout.' if refusal else ''


def main(argv: list) -> int:
    real = real_git()
    try:
        refusal = judge(argv, os.getcwd(), session())
    except Exception:   # noqa: BLE001 — fail open, see the head
        refusal = ''
        with session_state('git_wrapper.log').open('a', encoding='utf-8', newline='\n') as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} git {" ".join(argv)}\n{traceback.format_exc()}\n')
        print('git (branch lock): the wrapper crashed and let this call through — core/state/git_wrapper.log',
              file=sys.stderr)
    if refusal:
        print(refusal, file=sys.stderr)
        return 128
    # What git spawns (hooks, a rebase's exec) runs inside a call already judged.
    os.execve(real, [real, *argv], {**os.environ, 'WOS_GIT_JUDGED': '1'})
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
