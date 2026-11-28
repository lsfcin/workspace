# Persistent IBus engine helper for injecting dictated UTF-8 text on Wayland
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import signal
import socket
import subprocess
import sys
import threading

import gi

gi.require_version("IBus", "1.0")
from gi.repository import GLib, IBus  # noqa: E402

_ENGINE_NAME = "wos-dictate"
_COMP_NAME = "org.freedesktop.IBus.WosDictate"


def default_socket_path() -> pathlib.Path:
    override = os.environ.get("WOS_IBUS_SOCKET")
    if override:
        return pathlib.Path(override)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/tmp/wos-stt-{os.getuid()}"
    return pathlib.Path(runtime) / "wos-ibus.sock"


def _fallback_engine_from_gsettings() -> str:
    try:
        out = subprocess.check_output(
            ["gsettings", "get", "org.gnome.desktop.input-sources", "mru-sources"],
            text=True, encoding="utf-8", timeout=1.0, stderr=subprocess.DEVNULL,
        )
        m = re.search(r"\('xkb',\s*'([^']+)'\)", out)
        if m:
            layout = m.group(1)
            if layout == "us+intl":
                return "xkb:us:intl:eng"
            if layout == "br":
                return "xkb:br::por"
    except Exception:
        pass
    return "xkb:us:intl:eng"


class WosDictateEngine(IBus.Engine):
    """Minimal passthrough IBus engine used strictly for atomic CommitText injection."""

    active_instance: WosDictateEngine | None = None

    def do_enable(self) -> None:
        # Avoid IBus.Engine's read-only C `enabled` field (RuntimeError: unable to set value for field).
        self._is_enabled = True
        WosDictateEngine.active_instance = self

    def do_disable(self) -> None:
        self._is_enabled = False
        if WosDictateEngine.active_instance is self:
            WosDictateEngine.active_instance = None

    def do_focus_in(self) -> None:
        self._is_focused = True
        WosDictateEngine.active_instance = self

    def do_focus_out(self) -> None:
        self._is_focused = False

    def do_process_key_event(self, keyval: int, keycode: int, state: int) -> bool:
        return False


class IBusInjector:
    """Thread-safe bridge between socket requests and the GLib/IBus main loop."""

    def __init__(self, bus=None, idle_add=GLib.idle_add, timeout_add=GLib.timeout_add) -> None:
        self._idle_add, self._timeout_add = idle_add, timeout_add
        if bus is None:
            IBus.init()
            self.bus = IBus.Bus()
            if not self.bus.is_connected():
                raise RuntimeError("ibus-daemon is not connected")
            self.factory = IBus.Factory.new(self.bus.get_connection())
            self.factory.add_engine(_ENGINE_NAME, WosDictateEngine)
            self.bus.request_name(_COMP_NAME, 0)
            comp = IBus.Component.new(_COMP_NAME, "WOS Dictate", "0.1", "MIT", "WOS", "", "", "wos")
            comp.add_engine(IBus.EngineDesc.new(_ENGINE_NAME, "WOS Dictate", "Local STT", "pt", "MIT", "WOS", "", "default"))
            if not self.bus.register_component(comp):
                raise RuntimeError("register_component failed")
        else:
            self.bus, self.factory = bus, None
        self._lock = threading.Lock()

    def _current_engine_name(self) -> str:
        try:
            cur = self.bus.get_global_engine()
            if cur is not None and cur.get_name() and cur.get_name() != _ENGINE_NAME:
                return cur.get_name()
        except Exception:
            pass
        return _fallback_engine_from_gsettings()

    def inject(self, text: str, timeout: float = 1.5) -> dict:
        if not text:
            return {"ok": True, "empty": True}
        with self._lock:
            done = threading.Event()
            result: dict = {"ok": False, "error": "timeout"}
            prev = self._current_engine_name()

            def _restore() -> bool:
                def _on_restore(bus_obj, res, _data) -> None:
                    try:
                        bus_obj.set_global_engine_async_finish(res)
                    except Exception:
                        pass
                    done.set()

                try:
                    self.bus.set_global_engine_async(prev, 1000, None, _on_restore, None)
                except Exception:
                    done.set()
                return False

            def _start() -> bool:
                def _on_switched(bus_obj, res, _data) -> None:
                    try:
                        if not bus_obj.set_global_engine_async_finish(res):
                            result["error"] = "set_global_engine_async returned False"
                            done.set()
                            return
                    except Exception as exc:
                        result["error"] = str(exc)
                        done.set()
                        return
                    checks = {"n": 0}

                    def _wait_and_commit() -> bool:
                        checks["n"] += 1
                        eng = WosDictateEngine.active_instance
                        if eng is not None and getattr(eng, "_is_enabled", False):
                            try:
                                eng.commit_text(IBus.Text.new_from_string(text))
                                result.clear()
                                result["ok"] = True
                            except Exception as exc:
                                result["error"] = str(exc)
                            self._timeout_add(80, _restore)
                            return False
                        if checks["n"] >= 30:
                            result["error"] = "engine did not enable in time"
                            self._timeout_add(10, _restore)
                            return False
                        return True

                    self._timeout_add(15, _wait_and_commit)

                try:
                    # Async switch prevents deadlocking CreateEngine on the same GLib loop (b20261128-ibus-deadlock).
                    self.bus.set_global_engine_async(_ENGINE_NAME, int(timeout * 1000), None, _on_switched, None)
                except Exception as exc:
                    result["error"] = str(exc)
                    done.set()
                return False

            self._idle_add(_start)
            done.wait(timeout + 0.5)
            return result


def _serve_socket(sock_path: pathlib.Path, injector: IBusInjector, stop: threading.Event, tray=None) -> None:
    sock_path.parent.mkdir(parents=True, exist_ok=True)
    sock_path.unlink(missing_ok=True)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as srv:
        srv.bind(str(sock_path))
        os.chmod(sock_path, 0o600)
        srv.listen(8)
        srv.settimeout(0.5)
        try:
            while not stop.is_set():
                try:
                    conn, _ = srv.accept()
                except socket.timeout:
                    continue
                with conn, conn.makefile("r", encoding="utf-8") as reader:
                    line = reader.readline()
                    try:
                        req = json.loads(line) if line else {}
                        op = req.get("op", "")
                        if op == "ping":
                            resp = {"ok": True, "engine": _ENGINE_NAME}
                        elif op == "inject":
                            resp = injector.inject(str(req.get("text", "")))
                        elif op == "state":
                            st = str(req.get("state", "idle"))
                            if tray is not None:
                                GLib.idle_add(lambda s=st: (tray.set_state(s), False)[1])
                            resp = {"ok": True, "state": st}
                        else:
                            resp = {"ok": False, "error": f"unknown op: {op}"}
                    except Exception as exc:
                        resp = {"ok": False, "error": str(exc)}
                    conn.sendall((json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8"))
        finally:
            sock_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WOS IBus CommitText daemon")
    parser.add_argument("--socket", type=pathlib.Path, default=default_socket_path())
    args = parser.parse_args(argv)
    injector = IBusInjector()
    try:
        import tray as tray_mod
        tray = tray_mod.start_tray()
    except Exception:
        tray = None
    loop, stop = GLib.MainLoop(), threading.Event()

    def _shutdown(*_a) -> None:
        stop.set()
        if tray is not None:
            tray.close()
        GLib.idle_add(loop.quit)

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, _shutdown)
    threading.Thread(target=_serve_socket, args=(args.socket, injector, stop, tray), daemon=True).start()
    print(f"wos-ibus: listening on {args.socket}", flush=True)
    try:
        loop.run()
    finally:
        stop.set()
        if tray is not None:
            tray.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
