# b20261127 regression — /tmp is tmpfs here, so a leak in it is RAM: 4 GB of folders nobody deleted starved every worker. What grows with its input lives off it, what a run makes is gone when the run ends, and what a killed run left is swept after a day.
import importlib.util
import os
import socket
import sys
import tempfile

from conftest import HOOKS, WORKSPACE_ROOT

sys.path.insert(0, str(HOOKS))
import platform_law  # noqa: E402

DAY = 24 * 60 * 60
NOW = 2_000_000_000   # a fixed instant: the suite reads no clock


def _hook(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, HOOKS / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _age(path, seconds):
    os.utime(path, (NOW - seconds, NOW - seconds), follow_symlinks=False)


def test_scratch_routes_every_mkdtemp_inside_it_and_leaves_nothing():
    root = platform_law.scratch_root()
    assert str(root).startswith(os.environ['WOS_SESSION_STATE']), 'the suite must hold its own scratch'
    with platform_law.scratch('video-') as folder:
        inner = tempfile.mkdtemp(prefix='frames-')
        assert inner.startswith(str(folder)) and os.environ['TMPDIR'] == str(folder)
    assert not folder.exists() and tempfile.gettempdir() != str(folder)


def test_a_tree_copy_goes_to_native_disk_outside_the_suite(monkeypatch):
    monkeypatch.delenv('WOS_SESSION_STATE')
    tree = platform_law.scratch_root(tree=True)
    assert tree.is_dir() and platform_law.system_temp() not in tree.parents, 'a tree copy is never RAM'


def test_sweep_takes_a_dead_runs_folder_and_spares_a_young_one_and_a_listening_one(tmp_path):
    prune = _hook('session_prune', 'session/session-prune.py')
    dead, young, live = tmp_path / 'mat-debug-1', tmp_path / 'video-2', tmp_path / 'tmux-1000'
    for folder in (dead, young, live):
        folder.mkdir()
    (dead / 'out.png').write_bytes(b'x')
    listener = socket.socket(socket.AF_UNIX)
    listener.bind(str(live / 'default'))
    for path in (dead / 'out.png', dead, live / 'default', live):
        _age(path, 2 * DAY)
    _age(young, 0)
    old_scratch = platform_law.scratch_root() / 'video-old'
    old_scratch.mkdir()
    _age(old_scratch, 2 * DAY)
    try:
        prune.sweep(NOW, tmp_path)
    finally:
        listener.close()
    assert not dead.exists() and not old_scratch.exists()
    assert young.exists() and live.exists()


def test_the_temp_directory_is_warned_about_at_a_lower_bar_than_the_disk(monkeypatch):
    reminders = _hook('reminders', 'session/reminders.py')
    temp, full, empty = tempfile.gettempdir(), (100, 65, 35), (100, 10, 90)
    monkeypatch.setattr(reminders.shutil, 'disk_usage', lambda where: type('U', (), dict(
        zip(('total', 'used', 'free'), full if str(where) == temp else empty))))
    said = reminders.disk()
    assert 'temp directory' in said and 'partition holding ~' not in said


def test_an_agent_cli_alive_past_a_day_is_named_and_the_asker_is_not():
    sys.path.insert(0, str(WORKSPACE_ROOT / 'core/tools'))
    import worker_guard  # noqa: PLC0415
    mine = {pid for pid, _, _ in platform_law.ancestors()}
    assert all(pid not in mine for _, pid, _, _ in worker_guard.strays(0, mine))
    assert worker_guard.strays(10 ** 6, set()) == []


def test_the_suite_root_is_one_per_run_and_holds_each_process():
    root = os.environ['WOS_TEST_ROOT']
    assert os.path.basename(root).startswith('wos-test-')
    assert os.environ['WOS_SESSION_STATE'].startswith(root)
    assert os.environ['WOS_SCOREBOARD'].startswith(root)
