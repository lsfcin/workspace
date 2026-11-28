# worker_guard.py — the process between a worker and its caller: when the caller dies, or the deadline passes, the worker and everything it spawned die with it.
#
# WHY IT EXISTS (b20261124-worker-outlives-caller). 39 `opencode run` were found alive, parent
# systemd, some for 14 h, swap full. Each caller had died before its timeout — a session ended, a
# background shell was reaped — and `start_new_session` had kept the child out of the dying group.
# A timeout that lives in the caller dies with the caller; this one lives beside the worker.
#
# HOW THE CALLER'S DEATH IS SEEN. The caller keeps the write end of a pipe and never writes. The
# kernel closes it when the caller dies, however it dies, SIGKILL and OOM included, and the guard
# reads end-of-file. No signal handler, no PDEATHSIG (bound to a thread, and lost across the fork
# the panel found), no polling of a pid that may be reused.
#
# WHY A CGROUP WHEN THERE IS ONE. A worker is another vendor's CLI and spawns what it likes, setsid
# included: a process group does not hold that, a cgroup does. With a user systemd each worker runs
# in a scope of its own, capped in time and memory by the kernel, the guard included. Without one
# the group is all there is, and a setsid escapes it — said in one line, never hidden.
# Detected by capability (is there a user manager), not by operating system name.
from __future__ import annotations

import os
import select
import signal
import subprocess
import sys
import time
from pathlib import Path

GRACE_S = 5   # a worker past its deadline gets this long after SIGTERM to flush and go
# Admission, before anything is spawned (Lucas, 2026-11-24: act at the spawn, not after). A worker
# measured 200-430 MB (opencode); the floor keeps the laptop out of swap with three in flight.
MAX_LIVE = 4          # workers alive at once on this machine, every session counted
MEM_FLOOR_MB = 2048   # MemAvailable below this, plus RESERVE_MB per live worker, refuses the spawn
RESERVE_MB = 512
MEM_MAX_MB = 2048     # the cgroup's ceiling for one worker and all it spawns; past it the kernel kills it
SLOTS = Path(__file__).resolve().parents[2] / 'core' / 'state' / 'worker_slots'
BUSY = 75             # EX_TEMPFAIL: no worker was started, try later


def contain(lifetime_s: int, mem_mb: int) -> list:
    """argv prefix that runs a command in a cgroup of its own, capped in time and memory, or []."""
    if not hasattr(os, 'getuid') or not Path(f'/run/user/{os.getuid()}/systemd/private').exists():
        return []
    return ['systemd-run', '--user', '--scope', '--quiet', '--collect',
            f'--unit=wos-worker-{os.getpid()}-{os.urandom(3).hex()}',
            '-p', f'RuntimeMaxSec={lifetime_s}', '-p', f'MemoryMax={mem_mb}M', '-p', 'MemorySwapMax=0']


def memory(field: str = 'MemAvailable') -> int | None:
    """MB of a /proc/meminfo field (by default what the kernel can hand out without swapping), or
    None where it does not say."""
    try:
        for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines():
            if line.startswith(f'{field}:'):
                return int(line.split()[1]) // 1024
    except OSError:
        pass
    return None


AGENTS = ('claude', 'codex', 'opencode', 'gemini', 'agy')   # a CLI's process name, as /proc spells it


def strays(hours: float, spare: set) -> list:
    """(name, pid, days, MB) of this user's agent CLIs alive past `hours`, outside `spare` (the asker's
    own ancestry). The guard ends a delegated worker; a session's own CLI or a tool an agent backgrounded
    is ended by no one: Foundry ran 6 days; two idle sessions were 1 and 3 days old (2026-11-27)."""
    try:
        uptime = float(Path('/proc/uptime').read_text(encoding='utf-8').split()[0])
    except OSError:
        return []
    tick, page, found = os.sysconf('SC_CLK_TCK'), os.sysconf('SC_PAGE_SIZE'), []
    for stat in Path('/proc').glob('[0-9]*/stat'):
        try:
            text, pid = stat.read_text(encoding='utf-8'), int(stat.parent.name)
            name, fields = text[text.index('(') + 1:text.rindex(')')], text[text.rindex(')') + 2:].split()
            age = uptime - int(fields[19]) / tick
            if (name in AGENTS and pid not in spare and age > hours * 3600
                    and stat.parent.stat().st_uid == os.getuid()):
                found.append((name, pid, age / 86400, int(fields[21]) * page // 2 ** 20))
        except (OSError, ValueError, IndexError):
            continue
    return sorted(found, key=lambda row: -row[3])


def _scope_procs() -> Path | None:
    """This process's cgroup member list, when it stands in a worker scope."""
    try:
        cgroup = Path('/proc/self/cgroup').read_text(encoding='utf-8').strip().split('::', 1)[1]
    except (OSError, IndexError):
        return None
    return Path('/sys/fs/cgroup' + cgroup) / 'cgroup.procs' if Path(cgroup).name.startswith('wos-worker-') else None


def kill_tree(pgid: int) -> None:
    """Kill the worker's group, then every other process left in this scope: what left the group
    with setsid is still in the cgroup."""
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    procs = _scope_procs()
    for _ in range(50):   # one forking while we kill shows up on the next read
        others = [int(p) for p in procs.read_text(encoding='utf-8').split() if int(p) != os.getpid()] if procs and procs.exists() else []
        if not others:
            return
        for pid in others:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        time.sleep(0.02)


def guard(fd: int, timeout: int, cmd: list) -> int:
    """Run `cmd`; return its exit code, or 124 at the deadline, or kill everything when `fd` closes."""
    if _scope_procs() is None:
        print('worker_guard: no cgroup here, so a process that leaves the group with setsid can outlive this call',
              file=sys.stderr)
    child = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, start_new_session=True)
    deadline = time.monotonic() + timeout
    while True:
        if child.poll() is not None:
            kill_tree(child.pid)   # a helper still holding stdout would keep the caller waiting
            return child.returncode
        left = deadline - time.monotonic()
        if left <= 0:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(GRACE_S)
            except subprocess.TimeoutExpired:
                pass
            kill_tree(child.pid)
            child.wait()
            print(f'timed out after {timeout} s', file=sys.stderr)
            return 124
        if select.select([fd], [], [], min(left, 0.5))[0] and not os.read(fd, 1):
            kill_tree(child.pid)   # end-of-file: the caller is gone, and nobody will read the answer
            child.wait()
            return 137


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


def _admit() -> tuple:
    """(slot, refusal): a slot named for this caller, taken under one lock so three callers at once
    cannot all read the same free memory. A slot whose caller died is dropped on the way."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'hooks'))
    from platform_law import locked  # noqa: PLC0415
    SLOTS.mkdir(parents=True, exist_ok=True)
    with locked(SLOTS.parent / 'worker_slots.flock'):
        live = []
        for slot in SLOTS.iterdir():
            if _alive(int(slot.name.split('-', 1)[0])):
                live.append(slot)
            else:
                slot.unlink(missing_ok=True)
        need = MEM_FLOOR_MB + RESERVE_MB * len(live)
        if len(live) >= MAX_LIVE:
            return None, f'worker refused: {len(live)} live workers, the cap is {MAX_LIVE}; retry when one ends'
        if (free := memory()) is not None and free < need:
            return None, (f'worker refused: {free} MB available, {need} MB needed '
                          f'({MEM_FLOOR_MB} floor + {RESERVE_MB} for each of {len(live)} live); free memory, then retry')
        slot = SLOTS / f'{os.getpid()}-{os.urandom(4).hex()}'
        slot.touch()
    return slot, ''


def spawn(cmd: list, cwd: str | None = None, timeout: int = 900) -> tuple:
    """(exit code, stdout, stderr) of `cmd` run under the guard, or (BUSY, '', why) when admission
    refuses. The one door every worker goes through."""
    slot, refusal = _admit()
    if refusal:
        print(refusal, file=sys.stderr)
        return BUSY, '', refusal
    read, write = os.pipe()   # the caller's half is not inheritable: only the guard gets `read`
    try:
        argv = contain(timeout + 2 * GRACE_S, MEM_MAX_MB) + [sys.executable, __file__, str(read), str(timeout), '--', *cmd]
        try:
            proc = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
                                    pass_fds=(read,))
        finally:
            os.close(read)
        try:
            out, err = proc.communicate(timeout=timeout + 4 * GRACE_S)   # the guard's own deadline, missed
        except subprocess.TimeoutExpired:
            os.close(write)
            write = -1   # end-of-file: the guard kills its tree on the way out
            proc.kill()
            out, err = proc.communicate()
            return 124, out or '', f'timed out after {timeout} s; the guard missed its deadline'
        return proc.returncode, out or '', err or ''
    finally:
        if write >= 0:
            os.close(write)
        slot.unlink(missing_ok=True)


if __name__ == '__main__':
    sys.exit(guard(int(sys.argv[1]), int(sys.argv[2]), sys.argv[4:]))   # FD TIMEOUT -- CMD...
