# Default and local configuration for desktop STT dictation
from __future__ import annotations

import ast
import json
import os
import pathlib
import re
import subprocess
import sys

_HERE = pathlib.Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import refine  # noqa: E402

_DEFAULT_CFG = _HERE / "config.json"
_CUSTOM_ROOT = "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/"
_CUSTOM_LIST_KEY = "org.gnome.settings-daemon.plugins.media-keys"
_CONFLICT_SCHEMAS = (
    "org.gnome.desktop.wm.keybindings",
    "org.gnome.shell.keybindings",
    "org.gnome.settings-daemon.plugins.media-keys",
    "org.gnome.mutter.keybindings",
    "org.gnome.mutter.wayland.keybindings",
)


def default_config_path() -> pathlib.Path:
    return _DEFAULT_CFG


def local_config_path() -> pathlib.Path:
    return refine.state_dir() / "config.json"


def _read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def load_config(default_path: pathlib.Path | None = None,
                local_path: pathlib.Path | None = None) -> dict:
    """Load versioned defaults merged with optional local overrides."""
    base = _read_json(default_path or default_config_path())
    override = _read_json(local_path or local_config_path())
    merged = {**base, **override}
    raw_shortcuts = merged.get("shortcuts")
    shortcuts = [str(s).strip() for s in raw_shortcuts if str(s).strip()] if isinstance(raw_shortcuts, list) else ["<Alt>v"]
    if not shortcuts:
        shortcuts = ["<Alt>v"]
    return {
        "shortcuts": shortcuts,
        "idle_seconds": max(10, int(merged.get("idle_seconds", 300))),
        "max_record_seconds": max(10, int(merged.get("max_record_seconds", 300))),
        "polish": bool(merged.get("polish", False)),
        "no_ibus": bool(merged.get("no_ibus", False)),
    }


def normalize_shortcut(accel: str) -> str:
    """Normalize a GTK/GNOME accelerator string for conflict comparison."""
    mods = sorted(m.lower().replace("primary", "control").replace("ctrl", "control")
                  for m in re.findall(r"<([^>]+)>", accel))
    key = re.sub(r"<[^>]+>", "", accel).strip().lower()
    return "".join(f"<{m}>" for m in mods) + key


def _dump_gnome_bindings() -> str:
    lines: list[str] = []
    for schema in _CONFLICT_SCHEMAS:
        out = subprocess.run(
            ["gsettings", "list-recursively", schema],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=3.0,
        )
        if out.returncode == 0:
            lines.extend(out.stdout.splitlines())
    custom_raw = subprocess.run(
        ["gsettings", "get", _CUSTOM_LIST_KEY, "custom-keybindings"],
        capture_output=True, text=True, encoding="utf-8", check=False, timeout=2.0,
    )
    if custom_raw.returncode == 0:
        for path in _parse_str_list(custom_raw.stdout):
            if "/wos-dictate" in path:
                continue
            b = subprocess.run(
                ["dconf", "read", f"{path}binding"],
                capture_output=True, text=True, encoding="utf-8", check=False, timeout=2.0,
            )
            val = b.stdout.strip()
            if val:
                lines.append(f"custom {path} [{val}]")
    return "\n".join(lines)


def _parse_str_list(raw: str) -> list[str]:
    text = raw.strip()
    if text.startswith("@as "):
        return []
    try:
        parsed = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return []
    return [str(x) for x in parsed] if isinstance(parsed, list) else []


def find_gnome_conflicts(shortcuts: list[str], gsettings_dump: str | None = None) -> dict[str, list[str]]:
    """Return {shortcut: [conflicting schema/key entries]} for GNOME bindings."""
    wanted = {normalize_shortcut(s): s for s in shortcuts if s.strip()}
    conflicts: dict[str, list[str]] = {}
    dump = gsettings_dump if gsettings_dump is not None else _dump_gnome_bindings()
    for line in dump.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        schema, key, raw_val = parts[0], parts[1], parts[2]
        if "[<'" in raw_val or raw_val.startswith("[") or raw_val.startswith("@as"):
            vals = _parse_str_list(raw_val)
        else:
            vals = [raw_val.strip("'\"")]
        for val in vals:
            norm = normalize_shortcut(val)
            if norm in wanted:
                orig = wanted[norm]
                conflicts.setdefault(orig, []).append(f"{schema} {key} ({val})")
    return conflicts


def _dconf_write(key_path: str, value: str) -> None:
    subprocess.run(["dconf", "write", key_path, value], check=True, timeout=2.0)


def apply_gnome_shortcuts(shortcuts: list[str], command: str, force: bool = False,
                          gsettings_dump: str | None = None) -> dict:
    """Check GNOME conflicts and bind wos-dictate custom keybindings."""
    conflicts = find_gnome_conflicts(shortcuts, gsettings_dump=gsettings_dump)
    if conflicts and not force:
        return {"ok": False, "conflicts": conflicts}

    cur_raw = subprocess.check_output(
        ["gsettings", "get", _CUSTOM_LIST_KEY, "custom-keybindings"],
        text=True, encoding="utf-8", timeout=2.0,
    )
    existing = [p for p in _parse_str_list(cur_raw) if "/wos-dictate" not in p]
    created_paths: list[str] = []
    for idx, accel in enumerate(shortcuts):
        suffix = "wos-dictate" if idx == 0 else f"wos-dictate-{idx + 1}"
        path = f"{_CUSTOM_ROOT}{suffix}/"
        created_paths.append(path)
        _dconf_write(f"{path}name", repr(f"WOS Ditado ({accel})"))
        _dconf_write(f"{path}command", repr(command))
        _dconf_write(f"{path}binding", repr(accel))

    # Prune stale wos-dictate-* slots left over from previous multi-shortcut configs.
    for old_path in _parse_str_list(cur_raw):
        if "/wos-dictate" in old_path and old_path not in created_paths:
            subprocess.run(["dconf", "reset", "-f", old_path], check=False, timeout=2.0)

    new_list = existing + created_paths
    subprocess.run(
        ["gsettings", "set", _CUSTOM_LIST_KEY, "custom-keybindings", repr(new_list)],
        check=True, timeout=2.0,
    )
    return {"ok": True, "shortcuts": shortcuts, "paths": created_paths, "conflicts": conflicts}


def sync_systemd_idle(idle_seconds: int, unit_path: pathlib.Path | None = None) -> bool:
    """Update --idle-seconds in wos-stt.service if needed and reload systemd."""
    unit = unit_path or (pathlib.Path.home() / ".config" / "systemd" / "user" / "wos-stt.service")
    if not unit.is_file():
        return False
    text = unit.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"(--idle-seconds\s+)\d+",
        rf"\g<1>{int(idle_seconds)}",
        text,
    )
    if count == 0 or updated == text:
        return False
    tmp = unit.with_suffix(".tmp")
    tmp.write_text(updated, encoding="utf-8", newline="\n")
    os.replace(tmp, unit)
    if unit_path is None:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False, timeout=3.0)
    return True
