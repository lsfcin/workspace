#!/mnt/workspace/.venv/bin/python3
# attachments_util.py — shared filename/dir helpers for Core/tools attachment downloaders (gmail, telegram)
import pathlib, re
from datetime import datetime


def safe_name(filename: str) -> str:
    return re.sub(r"[^\w\-.]", "-", filename).lower()


def month_dir(base: pathlib.Path) -> pathlib.Path:
    d = base / datetime.now().strftime("%Y-%m")
    d.mkdir(parents=True, exist_ok=True)
    return d


def unique_path(base: pathlib.Path) -> pathlib.Path:
    if not base.exists():
        return base
    i = 1
    while True:
        candidate = base.parent / f"{base.stem}-{i}{base.suffix}"
        if not candidate.exists():
            return candidate
        i += 1
