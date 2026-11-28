# Regression test for b20261128-ibus-deadlock: async engine switch and safe WosDictateEngine fields
from __future__ import annotations

import sys
import types


def test_ibus_async_injection_never_calls_sync_switch(monkeypatch, tmp_path):
    fake_text = lambda s: types.SimpleNamespace(get_text=lambda: s)
    fake_ibus = types.SimpleNamespace(
        Engine=type("E", (), {"enabled": property(lambda self: False, lambda self, v: (_ for _ in ()).throw(RuntimeError("unable to set value for field")))}),
        Text=types.SimpleNamespace(new_from_string=fake_text),
    )
    fake_glib = types.SimpleNamespace(idle_add=lambda fn: fn(), timeout_add=lambda _ms, fn: fn())
    fake_gio = types.SimpleNamespace(DBusConnection=object, BusType=types.SimpleNamespace(SESSION=0))
    fake_repo = types.SimpleNamespace(IBus=fake_ibus, GLib=fake_glib, Gio=fake_gio)
    monkeypatch.setitem(sys.modules, "gi", types.SimpleNamespace(require_version=lambda *_a: None, repository=fake_repo))
    monkeypatch.setitem(sys.modules, "gi.repository", fake_repo)
    monkeypatch.delitem(sys.modules, "ibus_engine", raising=False)
    monkeypatch.delitem(sys.modules, "tray", raising=False)
    import ibus_engine
    import tray

    class _FakeBus:
        calls: list[str] = []
        get_global_engine = staticmethod(lambda: types.SimpleNamespace(get_name=lambda: "xkb:us:intl:eng"))
        set_global_engine = staticmethod(lambda *_a: (_ for _ in ()).throw(AssertionError("sync call forbidden")))
        set_global_engine_async_finish = staticmethod(lambda _res: True)

        def set_global_engine_async(self, name, _t, _c, cb, data):
            self.calls.append(name)
            cb(self, name, data)

    eng = ibus_engine.WosDictateEngine()
    eng.committed = []
    eng.commit_text = lambda t: eng.committed.append(t.get_text())
    eng.do_enable()
    eng.do_focus_in()
    assert ibus_engine.WosDictateEngine.active_instance is eng and eng._is_enabled is True
    bus = _FakeBus()
    res = ibus_engine.IBusInjector(bus=bus, idle_add=lambda fn: fn(), timeout_add=lambda _ms, fn: fn()).inject("Olá mundo")
    eng.do_focus_out()
    eng.do_disable()
    assert res["ok"] is True and eng.committed == ["Olá mundo"] and bus.calls == ["wos-dictate", "xkb:us:intl:eng"]

    icon_dir = tray.write_svg_icons(tmp_path)
    for name in ("wos-rec-0.svg", "wos-rec-1.svg", "wos-rec-2.svg", "wos-tx-0.svg", "wos-tx-1.svg", "wos-tx-2.svg", "wos-tx-3.svg"):
        assert (icon_dir / name).is_file()
    assert "<rect" not in (icon_dir / "wos-tx-0.svg").read_text(encoding="utf-8")
