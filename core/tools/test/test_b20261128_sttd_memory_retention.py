# Regression test for b20261128-sttd-memory-retention: sttd kills worker subprocess on idle/unload
from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import sys

from conftest import TOOLS


def _load_sttd():
    path = TOOLS / "audio" / "sttd"
    loader = importlib.machinery.SourceFileLoader("wos_sttd_reg", str(path))
    spec = importlib.util.spec_from_loader("wos_sttd_reg", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def test_sttd_subprocess_worker_spawn_and_idle_kill(tmp_path):
    sttd = _load_sttd()
    pid_file = tmp_path / "worker.pid"
    worker_py = tmp_path / "fake_worker.py"
    worker_py.write_text(
        f"import json, os, pathlib, sys\npathlib.Path({str(pid_file)!r}).write_text(str(os.getpid()))\n"
        "for line in sys.stdin:\n"
        "    if line.strip(): print(json.dumps({'ok':True,'segments':[{'text':'ok','avg_logprob':-0.2}],'device':'fake-gpu'}), flush=True)\n",
        encoding="utf-8", newline="\n",
    )
    now = {"t": 100.0}
    eng = sttd.SttEngine(idle_seconds=30.0, loader=None, clock=lambda: now["t"], worker_cmd=[sys.executable, str(worker_py)])
    resp = eng.transcribe({"path": "/tmp/a.wav"})
    assert resp["ok"] is True and resp["device"] == "fake-gpu" and eng.status()["loaded"] is True
    worker_pid = int(pid_file.read_text(encoding="utf-8"))
    now["t"] = 140.0
    assert eng.maybe_unload() is True and eng.status()["loaded"] is False
    try:
        os.kill(worker_pid, 0)
        alive = True
    except OSError:
        alive = False
    assert alive is False
