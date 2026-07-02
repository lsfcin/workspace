# Copilot PostToolUse hook: regenerate interfaces, sync context, record read-trackers.

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from copilot_shared import (
    EDIT_HINTS,
    READ_HINTS,
    build_payload,
    collect_paths,
    load_input,
    run_script,
    session_id,
)


def emit_allow(messages: list[str] | None = None) -> None:
    output: dict[str, Any] = {"continue": True}
    if messages:
        text = "\n\n".join(message for message in messages if message)
        if text:
            output["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": text,
            }
    print(json.dumps(output, ensure_ascii=False))


def main() -> int:
    data = load_input()
    workspace_root = Path(data.get("cwd") or os.getcwd()).resolve()
    tool_name = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    tool_name_lower = tool_name.lower()
    paths = collect_paths(workspace_root, tool_input)

    # Read trackers: facade reads (facade-gate) + CONTEXT.md/interface reads (context-gate, pre-read unlock)
    if any(hint in tool_name_lower for hint in READ_HINTS) and paths:
        for file_path in paths:
            payload = {"file_path": file_path, "session_id": session_id()}
            run_script(workspace_root / ".hooks" / "facade-tracker.py", payload, "Read", workspace_root, via_env=True)
            run_script(workspace_root / ".hooks" / "context-tracker.py", payload, "Read", workspace_root, via_env=True)
        emit_allow()
        return 0

    if not any(hint in tool_name_lower for hint in EDIT_HINTS) or not paths:
        emit_allow()
        return 0

    messages: list[str] = []
    write_like = any(hint in tool_name_lower for hint in ("create", "write", "insert"))
    canonical_tool_name = "Write" if write_like else "Edit"
    for file_path in paths:
        payload = build_payload(file_path, tool_input)
        result = run_script(workspace_root / ".hooks" / "post-edit.sh", payload, canonical_tool_name, workspace_root, via_env=True)
        if result.stdout.strip():
            messages.append(result.stdout.strip())
        if result.stderr.strip():
            messages.append(result.stderr.strip())

    emit_allow(messages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
