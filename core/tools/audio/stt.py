# stt.py — speech-to-text boundary: faster-whisper large-v3-turbo, lazy-loaded; fails safe to "" .
# Priming is the CALLER's data — a domain passes its own carrier prose to `run`, because the
# prompt is what buys both vocabulary and punctuation, and no two domains share one.
from __future__ import annotations
import json
import os
import pathlib
import socket

_MODEL_NAME = "large-v3-turbo"
# Whisper hallucinates on near-silent audio, and no decoding setting stops it: on one of Lucas's
# empty voice notes the plain prompt emitted "... ... ...", the jargon-primed one invented
# "e-mail e-mail e-mail", and enabling VAD only shortened that to "e-mail.com". What DOES
# separate them is the model's own confidence. Measured across all 15 of his voice notes, every
# real transcript scored between -0.153 and -0.482 while that garbage scored -1.489, so the
# threshold sits between with room on both sides. (`no_speech_prob` was 0.000 for every file,
# real or not — VAD strips the silence it would have keyed on, so it is not a usable signal.)
_MIN_LOGPROB = -0.9
_cached_model = None


class _Segment:
    """Minimal segment shape matching faster-whisper's (text, avg_logprob)."""

    def __init__(self, text: str, avg_logprob: float) -> None:
        self.text = text
        self.avg_logprob = avg_logprob


def default_socket_path() -> pathlib.Path:
    """Unix socket path shared by sttd, dictate, and aiwbot."""
    override = os.environ.get("WOS_STT_SOCKET")
    if override:
        return pathlib.Path(override)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/tmp/wos-stt-{os.getuid()}"
    return pathlib.Path(runtime) / "wos-stt.sock"


def _rpc(sock_path: pathlib.Path, payload: dict, timeout: float = 30.0) -> dict:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        conn.settimeout(timeout)
        conn.connect(str(sock_path))
        conn.sendall((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
        chunks: list[bytes] = []
        while True:
            data = conn.recv(65536)
            if not data:
                break
            chunks.append(data)
            if b"\n" in data:
                break
    raw = b"".join(chunks).decode("utf-8").strip()
    return json.loads(raw) if raw else {"ok": False, "error": "empty reply"}


def daemon_alive(sock_path: pathlib.Path | None = None, timeout: float = 0.3) -> bool:
    """Return True if the shared sttd daemon answers ping on the Unix socket."""
    path = sock_path or default_socket_path()
    if not path.exists():
        return False
    try:
        return bool(_rpc(path, {"op": "ping"}, timeout=timeout).get("ok"))
    except (OSError, ValueError):
        return False


class DaemonWhisper:
    """Drop-in WhisperModel proxy talking to sttd over Unix domain socket."""

    def __init__(self, sock_path: pathlib.Path, timeout: float = 60.0) -> None:
        self.sock_path = pathlib.Path(sock_path)
        self.timeout = timeout

    def transcribe(self, path: str, language: str = "pt", initial_prompt: str | None = None,
                   vad_filter: bool = True):
        resp = _rpc(self.sock_path, {
            "op": "transcribe",
            "path": str(path),
            "lang": language,
            "prompt": initial_prompt or "",
            "vad_filter": bool(vad_filter),
        }, timeout=self.timeout)
        if not resp.get("ok"):
            raise RuntimeError(resp.get("error", "sttd transcribe failed"))
        segs = [_Segment(s["text"], float(s["avg_logprob"])) for s in resp.get("segments", [])]
        return iter(segs), None


def model():
    """Return a DaemonWhisper client when sttd is alive, else lazy-load local WhisperModel.
    faster_whisper is imported *inside* here, never at module top, so tests import without it."""
    global _cached_model
    sock = default_socket_path()
    if os.environ.get("WOS_STT_LOCAL") != "1" and daemon_alive(sock):
        return DaemonWhisper(sock)
    if _cached_model is None:
        from faster_whisper import WhisperModel
        _cached_model = WhisperModel(_MODEL_NAME, device="cpu", compute_type="int8")
    return _cached_model


def confident(segments: list) -> bool:
    """Did the model believe what it just wrote? Mean avg_logprob over the segments."""
    result = False
    if segments:
        total = sum(s.avg_logprob for s in segments)
        mean = total / len(segments)
        result = mean >= _MIN_LOGPROB
    return result


def run(path: pathlib.Path, whisper, hotwords: str, lang: str = "pt") -> str:
    """Transcribe one file with an injectable model — the test boundary. Any failure (bad audio,
    model error) degrades to "" rather than raising: the fail-safe invariant. A transcript the
    model itself doubts degrades the same way."""
    text = ""
    try:
        segments, _info = whisper.transcribe(str(path), language=lang, initial_prompt=hotwords,
                                             vad_filter=True)
        listed = list(segments)
        joined = "".join(seg.text for seg in listed)
        if confident(listed):
            text = joined
        else:
            print(f"stt.run rejected a low-confidence transcript: {joined[:80]!r}")
    except Exception as e:
        print(f"stt.run failed: {e}")
        text = ""
    return text.strip()
