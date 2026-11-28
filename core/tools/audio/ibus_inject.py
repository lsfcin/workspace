# Inject dictated UTF-8 text via IBus daemon with wl-copy clipboard fallback
from __future__ import annotations

import json
import os
import pathlib
import shutil
import socket
import subprocess


def default_socket_path() -> pathlib.Path:
    override = os.environ.get("WOS_IBUS_SOCKET")
    if override:
        return pathlib.Path(override)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/tmp/wos-stt-{os.getuid()}"
    return pathlib.Path(runtime) / "wos-ibus.sock"


def notify(title: str, body: str = "", timeout_ms: int = 1800) -> None:
    """Best-effort desktop notification via notify-send."""
    if not shutil.which("notify-send"):
        return
    cmd = ["notify-send", "-a", "WOS Ditado", "-t", str(timeout_ms), title]
    if body:
        cmd.append(body)
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _rpc(sock_path: pathlib.Path, payload: dict, timeout: float = 2.0) -> dict:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        conn.settimeout(timeout)
        conn.connect(str(sock_path))
        conn.sendall((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))
        data = conn.recv(65536).decode("utf-8").strip()
        return json.loads(data) if data else {"ok": False, "error": "empty reply"}


def ibus_alive(sock_path: pathlib.Path | None = None) -> bool:
    path = sock_path or default_socket_path()
    if not path.exists():
        return False
    try:
        return bool(_rpc(path, {"op": "ping"}, timeout=0.3).get("ok"))
    except (OSError, ValueError):
        return False


def inject(text: str, use_ibus: bool = True, sock_path: pathlib.Path | None = None) -> str:
    """Inject text at cursor via IBus, falling back to wl-copy + notification."""
    if not text:
        return "empty"
    path = sock_path or default_socket_path()
    if use_ibus and path.exists():
        try:
            resp = _rpc(path, {"op": "inject", "text": text}, timeout=2.0)
            if resp.get("ok"):
                return "ibus"
        except (OSError, ValueError):
            pass
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy"], input=text, text=True, encoding="utf-8", check=False)
        preview = text[:90] + ("..." if len(text) > 90 else "")
        notify("Ditado copiado (Ctrl+Shift+V)", preview, timeout_ms=2500)
        return "clipboard"
    notify("Ditado concluído (sem injetor)", text[:90], timeout_ms=2500)
    return "none"
