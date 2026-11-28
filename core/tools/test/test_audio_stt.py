# T1 audio STT: sttd Unix socket protocol, idle unload, client fallback, and refine
from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import json
import pathlib
import threading
import urllib.error

from conftest import TOOLS


def _load_sttd():
    path = TOOLS / "audio" / "sttd"
    loader = importlib.machinery.SourceFileLoader("wos_sttd", str(path))
    spec = importlib.util.spec_from_loader("wos_sttd", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


class _FakeSeg:
    def __init__(self, text: str, avg_logprob: float = -0.25) -> None:
        self.text = text
        self.avg_logprob = avg_logprob


class _FakeWhisper:
    def __init__(self, segments) -> None:
        self.segments = segments
        self.calls: list[dict] = []

    def transcribe(self, path, language="pt", initial_prompt=None, vad_filter=True):
        self.calls.append({"path": path, "language": language,
                           "initial_prompt": initial_prompt, "vad_filter": vad_filter})
        return iter(self.segments), None


def test_sttd_socket_transcribe_ping_and_unload(tmp_path, monkeypatch):
    import stt
    sttd = _load_sttd()
    fake = _FakeWhisper([_FakeSeg("claude sonnet"), _FakeSeg(" no roundup")])
    loads = {"n": 0}

    def _loader():
        loads["n"] += 1
        return fake, "fake-cuda"

    engine = sttd.SttEngine(idle_seconds=60.0, loader=_loader)
    sock = tmp_path / "stt.sock"
    stop = threading.Event()
    ready = threading.Event()
    srv = threading.Thread(target=sttd.serve, args=(sock, engine, stop, ready), daemon=True)
    srv.start()
    try:
        assert ready.wait(timeout=5.0)
        assert stt.daemon_alive(sock)
        monkeypatch.setenv("WOS_STT_SOCKET", str(sock))
        monkeypatch.delenv("WOS_STT_LOCAL", raising=False)
        client = stt.model()
        assert isinstance(client, stt.DaemonWhisper)
        out = stt.run(tmp_path / "voice.wav", client, "Bot, roda.", lang="pt")
        assert out == "claude sonnet no roundup"
        assert loads["n"] == 1
        assert fake.calls[0]["initial_prompt"] == "Bot, roda."
        assert engine.status()["loaded"] is True
        assert stt._rpc(sock, {"op": "unload"})["unloaded"] is True
        assert engine.status()["loaded"] is False
    finally:
        stop.set()
        srv.join(timeout=2.0)


def test_sttd_idle_unload_frees_model():
    sttd = _load_sttd()
    now = {"t": 100.0}
    engine = sttd.SttEngine(idle_seconds=30.0, loader=lambda: (_FakeWhisper([]), "fake"),
                            clock=lambda: now["t"])
    engine.transcribe({"path": "/tmp/a.wav"})
    assert engine.status()["loaded"] is True
    now["t"] = 120.0
    assert engine.maybe_unload() is False
    now["t"] = 135.0
    assert engine.maybe_unload() is True
    assert engine.status()["loaded"] is False


def test_stt_model_falls_back_when_daemon_absent(tmp_path, monkeypatch):
    import stt
    missing = tmp_path / "missing.sock"
    monkeypatch.setenv("WOS_STT_SOCKET", str(missing))
    assert stt.daemon_alive(missing) is False


def test_refine_replacements_and_prompt_shape(tmp_path):
    import refine
    manual = tmp_path / "vocab.json"
    manual.write_text(json.dumps({
        "replacements": {"cloud": "claude", "bote": "bot", "claudsonner": "claude sonnet"},
        "carrier": ["Faz o roundup no ptyxis."],
    }), encoding="utf-8", newline="\n")
    learned = tmp_path / "learned.json"
    learned.write_text(json.dumps({
        "replacements": {"cloud": "WRONG_OVERRIDE", "rondape": "roundup"},
        "terms": ["handoff", "ptyxis"],
    }), encoding="utf-8", newline="\n")

    vocab = refine.load_vocab(manual, learned)
    assert vocab["replacements"]["cloud"] == "claude"
    assert vocab["replacements"]["rondape"] == "roundup"

    prompt = refine.build_prompt(vocab["carrier"], ["Bot, roda os testes."], vocab["learned_terms"])
    assert "Faz o roundup no ptyxis." in prompt
    assert "handoff" in prompt
    assert prompt.endswith(".")

    fixed = refine.apply_replacements("Cloud, bote e rondape no cloudsonner? cloud!", vocab["replacements"])
    assert fixed == "Claude, bot e roundup no cloudsonner? claude!"
    assert refine.apply_replacements("claudsonner", vocab["replacements"]) == "claude sonnet"


def test_refine_polish_ollama_and_fail_safe(monkeypatch):
    import refine

    class _FakeResp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(
        refine.urllib.request, "urlopen",
        lambda req, timeout=4.0: _FakeResp(json.dumps({"response": "Claude, roda o roundup."}).encode("utf-8")),
    )
    assert refine.polish_ollama("claude é roda o roundup") == "Claude, roda o roundup."

    def _boom(*a, **kw):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(refine.urllib.request, "urlopen", _boom)
    assert refine.polish_ollama("texto original") == "texto original"
