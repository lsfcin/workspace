# T1 gdrive home account: a one-account command without --account lands on the workspace's own Drive (the first account), never asks.
import importlib.machinery
import importlib.util
import sys

from conftest import WORKSPACE_ROOT


def load_gdrive():
    path = WORKSPACE_ROOT / "core/tools/files/gdrive"
    loader = importlib.machinery.SourceFileLoader("gdrive_cli", str(path))
    spec = importlib.util.spec_from_loader("gdrive_cli", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def test_home_account_is_the_first_configured_account(monkeypatch) -> None:
    gdrive = load_gdrive()
    monkeypatch.setattr(gdrive.gauth, "primary_aliases", lambda: ["personal", "cin", "ufrpe"])
    assert gdrive.home_account() == "personal"


def test_put_without_account_goes_to_home_and_explicit_account_wins(monkeypatch) -> None:
    gdrive = load_gdrive()
    monkeypatch.setattr(gdrive.gauth, "primary_aliases", lambda: ["personal", "ufrpe"])
    seen = []
    monkeypatch.setattr(gdrive, "cmd_put", lambda account, *rest: seen.append(account))
    monkeypatch.setattr(sys, "argv", ["gdrive", "put", "x.pdf"])
    gdrive.main()
    monkeypatch.setattr(sys, "argv", ["gdrive", "put", "--account", "ufrpe", "x.pdf"])
    gdrive.main()
    assert seen == ["personal", "ufrpe"]
