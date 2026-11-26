# T1 regression b20261124-worker-outlives-caller: a worker and everything it spawned die with its caller or at its deadline, and no worker starts when the machine has no memory to give it.
#
# 39 `opencode run` processes were found alive 2026-11-24, parent systemd, some for 14 h, swap full:
# each caller had died before its timeout, and `start_new_session` kept its child out of reach.
# Real processes, no vendor CLI: the fake worker is python, and its grandchild escapes with setsid.
# No clock (b20260905): a FIFO is the barrier, a pidfd says a process exited, and every select
# bound only stops a hang.
import os
import pathlib
import select
import signal
import subprocess
import sys
import textwrap

import pytest

_TOOLS = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_TOOLS))
import worker_guard  # noqa: E402
import workers  # noqa: E402

SCOPED = bool(worker_guard.contain(60, 256))
WORKER = textwrap.dedent('''
    import os, sys, time
    mode, pids, escape = sys.argv[1], sys.argv[2], sys.argv[3] == '1'
    if os.fork() == 0:
        if escape:
            os.setsid()   # out of the worker's group: only a cgroup still reaches it
        with open(pids, 'w') as fh:
            fh.write(f'{os.getpid()}\\n')
        time.sleep(120)   # holds the inherited stdout open all along
        os._exit(0)
    with open(pids, 'w') as fh:
        fh.write(f'{os.getpid()}\\n')
    if mode == 'hang':
        time.sleep(120)
    print('answer', flush=True)
    sys.exit(3)
''')


def _pids(reader: int, n: int = 2) -> list:
    """Both processes have started and said who they are."""
    buf = b''
    while buf.count(b'\n') < n:
        assert select.select([reader], [], [], 30)[0], 'the fake worker never started'
        buf += os.read(reader, 256)
    return [int(x) for x in buf.split()]


def _gone(pids: list) -> bool:
    """Every pid has exited: a pidfd turns readable at exit."""
    for pid in pids:
        try:
            fd = os.pidfd_open(pid)
        except ProcessLookupError:
            continue
        try:
            if not select.select([fd], [], [], 30)[0]:
                return False
        finally:
            os.close(fd)
    return True


@pytest.fixture
def fake(tmp_path, monkeypatch):
    """(worker script, FIFO path, reader fd). Read-write open: the FIFO never blocks its writers."""
    script = tmp_path / 'worker.py'
    script.write_text(WORKER, encoding='utf-8', newline='\n')
    fifo = tmp_path / 'pids'
    os.mkfifo(fifo)
    reader = os.open(fifo, os.O_RDWR | os.O_NONBLOCK)
    monkeypatch.setattr(worker_guard, 'SLOTS', tmp_path / 'slots')
    # The host's own free memory is not this test's subject: the floor has its own case below.
    monkeypatch.setattr(worker_guard, 'memory', lambda: 10 ** 6)
    yield script, fifo, reader
    os.close(reader)


def _cmd(script, fifo, mode, escape):
    return [sys.executable, str(script), mode, str(fifo), '1' if escape else '0']


escapes = [False, pytest.param(True, marks=pytest.mark.skipif(
    not SCOPED, reason='no user systemd: a setsid escape is out of reach, and the guard says so'))]


@pytest.mark.parametrize('escape', escapes)
def test_the_deadline_kills_the_worker_and_its_grandchild(fake, escape):
    script, fifo, reader = fake
    code, text = workers.run(_cmd(script, fifo, 'hang', escape), timeout=1)
    assert code == 124 and 'timed out' in text
    assert _gone(_pids(reader))


def test_without_a_cgroup_the_weaker_promise_is_said(fake, monkeypatch):
    script, fifo, reader = fake
    monkeypatch.setattr(worker_guard, 'contain', lambda *a: [])
    code, text = workers.run(_cmd(script, fifo, 'hang', False), timeout=1)
    assert code == 124 and 'setsid can outlive' in text
    assert _gone(_pids(reader))


@pytest.mark.parametrize('escape, scoped', [(e, True) for e in escapes] + [(False, False)])
def test_a_caller_killed_outright_takes_the_whole_tree_with_it(fake, escape, scoped, tmp_path):
    """scoped=False is a machine with no user systemd: the group is all the guard holds."""
    script, fifo, reader = fake
    caller = subprocess.Popen([sys.executable, '-c', textwrap.dedent(f'''
        import pathlib, sys
        sys.path.insert(0, {str(_TOOLS)!r})
        import workers
        workers.worker_guard.SLOTS = pathlib.Path({str(tmp_path / 'slots')!r})
        workers.worker_guard.memory = lambda: 10 ** 6
        if not {scoped!r}:
            workers.worker_guard.contain = lambda *a: []
        workers.run({_cmd(script, fifo, 'hang', escape)!r}, timeout=300)
    ''')], stderr=subprocess.DEVNULL)
    tree = _pids(reader)
    caller.send_signal(signal.SIGKILL)   # uncatchable: no handler, no atexit, no finally runs
    caller.wait()
    assert _gone(tree), 'the worker outlived a caller that died before its deadline'


def test_a_worker_that_exits_leaves_no_helper_holding_its_output(fake):
    """The helper sleeps 120 s on the inherited stdout; were it left alive, the call would wait
    on it past its own bound and come back 124, not the worker's 3."""
    script, fifo, reader = fake
    code, text = workers.run(_cmd(script, fifo, 'exit', False), timeout=20)
    assert (code, text.strip()) == (3, 'answer')
    assert _gone(_pids(reader))


def test_no_worker_starts_below_the_memory_floor(fake, monkeypatch):
    script, fifo, _ = fake
    monkeypatch.setattr(worker_guard, 'memory', lambda: worker_guard.MEM_FLOOR_MB - 1)
    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **k: pytest.fail('spawned below the floor'))
    code, text = workers.run(_cmd(script, fifo, 'exit', False))
    assert code == 75 and 'MB available' in text and workers.classify(code, text) == 'busy'


def test_no_worker_starts_when_every_slot_is_taken(fake, monkeypatch):
    script, fifo, _ = fake
    monkeypatch.setattr(worker_guard, 'MAX_LIVE', 0)
    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **k: pytest.fail('spawned past the cap'))
    code, text = workers.run(_cmd(script, fifo, 'exit', False))
    assert code == 75 and 'live workers' in text


def test_a_slot_whose_caller_died_is_freed(fake, monkeypatch):
    script, fifo, _ = fake
    monkeypatch.setattr(worker_guard, 'MAX_LIVE', 1)
    worker_guard.SLOTS.mkdir(parents=True)
    dead = subprocess.Popen([sys.executable, '-c', 'pass'])
    dead.wait()
    (worker_guard.SLOTS / f'{dead.pid}-stale').write_text('', encoding='utf-8', newline='\n')
    code, _ = workers.run(_cmd(script, fifo, 'exit', False), timeout=20)
    assert code == 3 and not list(worker_guard.SLOTS.iterdir())


def test_describe_spawns_through_the_one_guarded_door(monkeypatch, tmp_path):
    import describe
    seen = []
    monkeypatch.setattr(worker_guard, 'spawn', lambda cmd, **kw: seen.append(cmd) or (0, 'a figure', ''))
    image = tmp_path / 'i.png'
    from PIL import Image
    Image.new('RGB', (4, 4)).save(image)
    assert describe._cli(['agy', '-p'], image, 'Describe.') == 'a figure'
    assert seen and seen[0][:2] == ['agy', '-p']
