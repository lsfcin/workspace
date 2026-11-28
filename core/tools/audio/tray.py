# Zero-dependency StatusNotifierItem top-bar indicator for WOS desktop dictation
from __future__ import annotations

import json
import math
import os
import pathlib
import subprocess
import sys
import time

import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib  # noqa: E402

_ROOT = pathlib.Path(__file__).resolve().parents[3]
_SNI_PATH, _MENU_PATH, _WATCHER = "/StatusNotifierItem", "/StatusNotifierMenu", "org.kde.StatusNotifierWatcher"

_SNI_XML = """<node><interface name="org.kde.StatusNotifierItem">
  <method name="ContextMenu"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
  <method name="Activate"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
  <method name="SecondaryActivate"><arg name="x" type="i" direction="in"/><arg name="y" type="i" direction="in"/></method>
  <method name="Scroll"><arg name="delta" type="i" direction="in"/><arg name="orientation" type="s" direction="in"/></method>
  <signal name="NewTitle"/><signal name="NewIcon"/><signal name="NewToolTip"/>
  <signal name="NewStatus"><arg name="status" type="s"/></signal>
  <property name="Category" type="s" access="read"/><property name="Id" type="s" access="read"/>
  <property name="Title" type="s" access="read"/><property name="Status" type="s" access="read"/>
  <property name="WindowId" type="i" access="read"/><property name="IconName" type="s" access="read"/>
  <property name="IconThemePath" type="s" access="read"/><property name="IconPixmap" type="a(iiay)" access="read"/>
  <property name="OverlayIconName" type="s" access="read"/><property name="OverlayIconPixmap" type="a(iiay)" access="read"/>
  <property name="AttentionIconName" type="s" access="read"/><property name="AttentionIconPixmap" type="a(iiay)" access="read"/>
  <property name="AttentionMovieName" type="s" access="read"/><property name="ToolTip" type="(sa(iiay)ss)" access="read"/>
  <property name="Menu" type="o" access="read"/><property name="ItemIsMenu" type="b" access="read"/>
</interface></node>"""

_MENU_XML = """<node><interface name="com.canonical.dbusmenu">
  <method name="GetLayout"><arg name="parentId" type="i" direction="in"/><arg name="recursionDepth" type="i" direction="in"/>
    <arg name="propertyNames" type="as" direction="in"/><arg name="revision" type="u" direction="out"/><arg name="layout" type="(ia{sv}av)" direction="out"/></method>
  <method name="GetGroupProperties"><arg name="ids" type="ai" direction="in"/><arg name="propertyNames" type="as" direction="in"/>
    <arg name="properties" type="a(ia{sv})" direction="out"/></method>
  <method name="GetProperty"><arg name="id" type="i" direction="in"/><arg name="name" type="s" direction="in"/><arg name="value" type="v" direction="out"/></method>
  <method name="Event"><arg name="id" type="i" direction="in"/><arg name="eventId" type="s" direction="in"/><arg name="data" type="v" direction="in"/><arg name="timestamp" type="u" direction="in"/></method>
  <method name="AboutToShow"><arg name="id" type="i" direction="in"/><arg name="needUpdate" type="b" direction="out"/></method>
  <signal name="LayoutUpdated"><arg name="revision" type="u"/><arg name="parent" type="i"/></signal>
  <property name="Version" type="u" access="read"/><property name="TextDirection" type="s" access="read"/>
  <property name="Status" type="s" access="read"/><property name="IconThemePath" type="as" access="read"/>
</interface></node>"""


def _circle_argb(size: int, fill: tuple[int, int, int, int],
                 ring: tuple[int, int, int, int] | None = None, dots: bool = False) -> bytes:
    """Render a square ARGB32 big-endian circle icon without external image dependencies."""
    buf = bytearray(size * size * 4)
    cx = cy = (size - 1) / 2.0
    r_out, r_in = size * 0.40, size * 0.25
    for y in range(size):
        for x in range(size):
            dist = math.hypot(x - cx, y - cy)
            idx = (y * size + x) * 4
            if dots and abs(y - cy) <= 1.6 and any(abs(x - dx) <= 1.6 for dx in (cx - 4.5, cx, cx + 4.5)):
                a, r, g, b = 255, 255, 255, 255
            elif dist <= r_out:
                r, g, b, a = ring if (ring and dist >= r_in) else fill
            else:
                a = r = g = b = 0
            buf[idx:idx + 4] = bytes((a, r, g, b))
    return bytes(buf)


def build_icons(size: int = 24) -> dict[str, list[tuple[int, int, bytes]]]:
    """Pre-render StatusNotifierItem pixmaps for each dictation state."""
    return {
        "recording_on": [(size, size, _circle_argb(size, (229, 57, 53, 255), (255, 205, 210, 255)))],
        "recording_off": [(size, size, _circle_argb(size, (90, 22, 22, 180), (229, 57, 53, 255)))],
        "transcribing": [(size, size, _circle_argb(size, (245, 158, 11, 255), (254, 243, 199, 255), dots=True))],
        "idle": [(size, size, _circle_argb(size, (148, 163, 184, 200)))],
    }


def _recorder_alive() -> bool:
    rt = pathlib.Path(os.environ.get("WOS_DICTATE_RUNTIME") or os.environ.get("XDG_RUNTIME_DIR") or f"/tmp/wos-stt-{os.getuid()}")
    sf = rt / "wos-dictate.json"
    if not sf.is_file():
        return False
    try:
        pid = int(json.loads(sf.read_text(encoding="utf-8")).get("pid") or 0)
        return pid > 0 and os.kill(pid, 0) is None
    except (OSError, ValueError):
        return False


def _spawn_dictate(*args: str) -> None:
    subprocess.Popen([str(_ROOT / "core" / "run"), "tools/audio/dictate", *args], cwd=str(_ROOT),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


class DictateTray:
    """StatusNotifierItem + DBusMenu controller living on the GLib main loop."""

    def __init__(self, bus: Gio.DBusConnection | None = None) -> None:
        self._icons, self._state, self._blink_on, self._revision = build_icons(24), "idle", True, 1
        self._state_since, self._tick_id = time.monotonic(), None
        self._bus = bus or Gio.bus_get_sync(Gio.BusType.SESSION, None)
        sni_iface = Gio.DBusNodeInfo.new_for_xml(_SNI_XML).interfaces[0]
        menu_iface = Gio.DBusNodeInfo.new_for_xml(_MENU_XML).interfaces[0]
        self._sni_id = self._bus.register_object(_SNI_PATH, sni_iface, self._on_sni_call, self._on_sni_get, None)
        self._menu_id = self._bus.register_object(_MENU_PATH, menu_iface, self._on_menu_call, self._on_menu_get, None)
        self._watch_id = Gio.bus_watch_name_on_connection(
            self._bus, _WATCHER, Gio.BusNameWatcherFlags.NONE, self._on_watcher, None
        )

    def _on_watcher(self, conn: Gio.DBusConnection, _name: str, _owner: str) -> None:
        conn.call(_WATCHER, "/StatusNotifierWatcher", _WATCHER, "RegisterStatusNotifierItem",
                  GLib.Variant("(s)", (_SNI_PATH,)), None, Gio.DBusCallFlags.NONE, 2000, None, self._finish_reg)

    def _finish_reg(self, conn: Gio.DBusConnection, res: Gio.AsyncResult) -> None:
        try:
            conn.call_finish(res)
        except Exception as exc:
            print(f"wos-ibus tray register warning: {exc}", file=sys.stderr, flush=True)

    def _status_str(self) -> str:
        return "Passive" if self._state == "idle" else "Active"

    def _emit(self, path: str, iface: str, sig: str, arg: GLib.Variant | None = None) -> None:
        try:
            self._bus.emit_signal(None, path, iface, sig, arg)
        except Exception:
            pass

    def set_state(self, state: str) -> str:
        norm = state if state in ("idle", "recording", "transcribing") else "idle"
        self._state, self._blink_on, self._state_since = norm, True, time.monotonic()
        self._revision += 1
        if self._tick_id is not None:
            GLib.source_remove(self._tick_id)
            self._tick_id = None
        if norm in ("recording", "transcribing"):
            self._tick_id = GLib.timeout_add(500, self._on_tick)
        self._emit(_SNI_PATH, "org.kde.StatusNotifierItem", "NewStatus", GLib.Variant("(s)", (self._status_str(),)))
        self._emit(_SNI_PATH, "org.kde.StatusNotifierItem", "NewIcon")
        self._emit(_SNI_PATH, "org.kde.StatusNotifierItem", "NewToolTip")
        self._emit(_MENU_PATH, "com.canonical.dbusmenu", "LayoutUpdated", GLib.Variant("(ui)", (self._revision, 0)))
        return norm

    def _on_tick(self) -> bool:
        if self._state == "recording":
            if (time.monotonic() - self._state_since) > 1.0 and not _recorder_alive():
                self.set_state("idle")
                return False
            self._blink_on = not self._blink_on
            self._emit(_SNI_PATH, "org.kde.StatusNotifierItem", "NewIcon")
            return True
        if self._state == "transcribing" and (time.monotonic() - self._state_since) <= 90.0:
            return True
        self.set_state("idle")
        return False

    def _on_sni_get(self, _c, _s, _p, _i, prop: str) -> GLib.Variant | None:
        tip = {"recording": "WOS Ditado: gravando (clique para parar)", "transcribing": "WOS Ditado: transcrevendo..."}.get(self._state, "WOS Ditado")
        key = ("recording_on" if self._blink_on else "recording_off") if self._state == "recording" else self._state
        table = {
            "Category": GLib.Variant("s", "ApplicationStatus"), "Id": GLib.Variant("s", "wos-dictate"),
            "Title": GLib.Variant("s", "WOS Ditado"), "Status": GLib.Variant("s", self._status_str()),
            "WindowId": GLib.Variant("i", 0), "IconPixmap": GLib.Variant("a(iiay)", self._icons[key]),
            "ToolTip": GLib.Variant("(sa(iiay)ss)", ("", [], tip, "")),
            "Menu": GLib.Variant("o", _MENU_PATH), "ItemIsMenu": GLib.Variant("b", False),
        }
        if prop in table:
            return table[prop]
        if prop in ("IconName", "IconThemePath", "OverlayIconName", "AttentionIconName", "AttentionMovieName"):
            return GLib.Variant("s", "")
        if prop in ("OverlayIconPixmap", "AttentionIconPixmap"):
            return GLib.Variant("a(iiay)", [])
        return None

    def _on_sni_call(self, _c, _s, _p, _i, method: str, _params, inv) -> None:
        if method == "Activate" and self._state == "recording":
            _spawn_dictate("toggle")
        inv.return_value(None)

    def _menu_items(self) -> list[tuple[int, dict[str, GLib.Variant]]]:
        items = [(1, {"label": GLib.Variant("s", "Parar ditado"), "enabled": GLib.Variant("b", True)})] if self._state == "recording" else []
        items.append((2, {"label": GLib.Variant("s", "Copiar último ditado"), "enabled": GLib.Variant("b", True)}))
        return items

    def _on_menu_get(self, _c, _s, _p, _i, prop: str) -> GLib.Variant | None:
        return {"Version": GLib.Variant("u", 3), "TextDirection": GLib.Variant("s", "ltr"),
                "Status": GLib.Variant("s", "normal"), "IconThemePath": GLib.Variant("as", [])}.get(prop)

    def _on_menu_call(self, _c, _s, _p, _i, method: str, params, inv) -> None:
        if method == "GetLayout":
            children = [GLib.Variant("(ia{sv}av)", (mid, props, [])) for mid, props in self._menu_items()]
            inv.return_value(GLib.Variant("(u(ia{sv}av))", (self._revision, (0, {"children-display": GLib.Variant("s", "submenu")}, children))))
        elif method == "GetGroupProperties":
            wanted = set(params.unpack()[0])
            inv.return_value(GLib.Variant("(a(ia{sv}))", ([(mid, p) for mid, p in self._menu_items() if mid in wanted],)))
        elif method == "GetProperty":
            mid, name = params.unpack()
            inv.return_value(GLib.Variant("(v)", (next((p[name] for i, p in self._menu_items() if i == mid and name in p), GLib.Variant("s", "")),)))
        elif method == "Event":
            mid, ev, _d, _ts = params.unpack()
            if ev == "clicked" and mid in (1, 2):
                _spawn_dictate("toggle" if mid == 1 else "copy-last")
            inv.return_value(None)
        elif method == "AboutToShow":
            inv.return_value(GLib.Variant("(b)", (False,)))
        else:
            inv.return_value(None)

    def close(self) -> None:
        if self._tick_id is not None:
            GLib.source_remove(self._tick_id)
            self._tick_id = None
        if self._watch_id:
            Gio.bus_unwatch_name(self._watch_id)
            self._watch_id = 0
        for reg in (self._sni_id, self._menu_id):
            if reg:
                self._bus.unregister_object(reg)
        self._sni_id = self._menu_id = 0


def start_tray() -> DictateTray | None:
    """Create and register DictateTray on the session bus, failing safe if unavailable."""
    try:
        return DictateTray()
    except Exception as exc:
        print(f"wos-ibus tray disabled: {exc}", file=sys.stderr, flush=True)
        return None
