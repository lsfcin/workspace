# Regression test for b20261128-ibus-deadlock: IBusInjector must switch engines asynchronously
from __future__ import annotations

import sys
import types


def test_ibus_async_injection_never_calls_sync_switch(monkeypatch):
    fake_text = lambda s: types.SimpleNamespace(get_text=lambda: s)
    fake_ibus = types.SimpleNamespace(Engine=type("E", (), {}), Text=types.SimpleNamespace(new_from_string=fake_text))
    fake_glib = types.SimpleNamespace(idle_add=lambda fn: fn(), timeout_add=lambda _ms, fn: fn())
    fake_repo = types.SimpleNamespace(IBus=fake_ibus, GLib=fake_glib)
    monkeypatch.setitem(sys.modules, "gi", types.SimpleNamespace(require_version=lambda *_a: None, repository=fake_repo))
    monkeypatch.setitem(sys.modules, "gi.repository", fake_repo)
    monkeypatch.delitem(sys.modules, "ibus_engine", raising=False)
    import ibus_engine

    class _FakeBus:
        calls: list[str] = []
        get_global_engine = staticmethod(lambda: types.SimpleNamespace(get_name=lambda: "xkb:us:intl:eng"))
        set_global_engine = staticmethod(lambda *_a: (_ for _ in ()).throw(AssertionError("sync call forbidden")))
        set_global_engine_async_finish = staticmethod(lambda _res: True)

        def set_global_engine_async(self, name, _t, _c, cb, data):
            self.calls.append(name)
            cb(self, name, data)

    fake_eng = types.SimpleNamespace(enabled=True, committed=[], commit_text=lambda t: fake_eng.committed.append(t.get_text()))
    monkeypatch.setattr(ibus_engine.WosDictateEngine, "active_instance", fake_eng)
    bus = _FakeBus()
    res = ibus_engine.IBusInjector(bus=bus, idle_add=lambda fn: fn(), timeout_add=lambda _ms, fn: fn()).inject("Olá mundo")
    assert res["ok"] is True and fake_eng.committed == ["Olá mundo"] and bus.calls == ["wos-dictate", "xkb:us:intl:eng"]
