#!/usr/bin/env python3
"""Brain stats — shared config, git helpers, and block replacement."""

import re
import subprocess
from pathlib import Path

BRAIN      = Path("brain")
GOALS_FILE = BRAIN / "GOALS.md"
DONE_LOG   = BRAIN / ".log" / "done.md"
GOALS_DIR  = BRAIN / "goals"

PERIODS = [
    ("month",     30),
    ("trimester", 90),
    ("semester",  180),
    ("year",      365),
    ("2-year",    730),
    ("4-year",    1460),
]

DONE_KEEP = 3

AREAS = ["health", "career", "finances", "fun", "spiritual"]


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def touch_count(path, days):
    out = git("log", "--oneline", f"--since={days} days ago", "--", str(path))
    return len([l for l in out.splitlines() if l.strip()])


def last_touch_date(path):
    out = git("log", "-1", "--format=%ci", "--", str(path))
    return out[:10] if out else None


def replace_block(content, start, end, new_block):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(content):
        return None
    return pattern.sub(lambda _: new_block, content)
