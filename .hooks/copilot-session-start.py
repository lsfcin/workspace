# Copilot SessionStart hook: inject workspace policy context.

from __future__ import annotations

import json
import os
from pathlib import Path
import sys


def load_input() -> dict:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def read_workspace_excerpt(workspace_root: Path, max_lines: int = 120) -> str:
    workspace_file = workspace_root / "WORKSPACE.md"
    if not workspace_file.exists():
        return "WORKSPACE.md was not found in the workspace root."

    lines: list[str] = []
    with workspace_file.open("r", encoding="utf-8") as handle:
        for _ in range(max_lines):
            line = handle.readline()
            if not line:
                break
            lines.append(line.rstrip("\n"))

    return "\n".join(lines)


def main() -> int:
    data = load_input()
    workspace_root = Path(data.get("cwd") or os.getcwd()).resolve()
    excerpt = read_workspace_excerpt(workspace_root)
    output = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "Workspace policy excerpt:\n" + excerpt,
        },
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
