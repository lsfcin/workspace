# Every harness in core/harnesses.txt reaches the outside workers, even one installed off PATH.
#
# From the bare environment a shim hands a tool, `delegate/ask` starts, and a worker installed only
# where its vendor's app puts it is still found. 2026-11-20: sessions reported codex missing while it sat off PATH inside the ChatGPT
# app; the fallback that finds it is workers.PLACES, and this is what fails if it goes.
import os
import stat
import subprocess

import pytest
import workers
from conftest import WORKSPACE_ROOT

HARNESSES = [line.split('\t')[0] for line in
             (WORKSPACE_ROOT / 'core/harnesses.txt').read_text(encoding='utf-8').splitlines()
             if line.strip() and not line.startswith('#')]
BARE_PATH = '/usr/bin:/bin'


@pytest.mark.parametrize('harness', HARNESSES)
def test_panel_starts_from_a_shim_environment(harness):
    env = {'PATH': BARE_PATH, 'HOME': os.environ.get('HOME', '/tmp'),
           f'{harness.upper()}_PROJECT_DIR': str(WORKSPACE_ROOT)}
    done = subprocess.run([str(WORKSPACE_ROOT / 'core/run'), 'tools/delegate/ask', '--help'], env=env,
                          cwd=str(WORKSPACE_ROOT), capture_output=True, text=True, encoding='utf-8')
    assert done.returncode == 0, done.stderr
    assert '--only' in done.stdout


@pytest.fixture
def app_install(tmp_path, monkeypatch):
    """Each worker's binary exists ONLY at its app place: not on PATH, no $ENV override."""
    def install(name):
        exe = tmp_path / name
        exe.write_text('#!/bin/sh\n', encoding='utf-8', newline='\n')
        exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
        env, _ = workers.PLACES[name]
        monkeypatch.delenv(env, raising=False)
        (tmp_path / 'empty').mkdir(exist_ok=True)
        monkeypatch.setenv('PATH', str(tmp_path / 'empty'))
        monkeypatch.setitem(workers.PLACES, name, (env, (str(exe),)))
        return str(exe)
    return install


@pytest.mark.parametrize('name', sorted(workers.PLACES))
def test_a_worker_off_path_is_found_at_its_app_place(name, app_install):
    exe = app_install(name)
    assert workers.find(name) == exe


@pytest.mark.parametrize('name', sorted(workers.PLACES))
def test_without_the_app_place_the_same_worker_is_missing(name, app_install, monkeypatch):
    app_install(name)
    monkeypatch.setitem(workers.PLACES, name, (workers.PLACES[name][0], ()))
    assert workers.find(name) is None
