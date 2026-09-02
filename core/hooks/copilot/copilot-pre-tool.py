# Copilot PreToolUse hook: enforce workspace read/edit/terminal policy via the canonical
# core/hooks scripts. The gates are located relative to THIS file, never from the workspace
# root: pointing at a spelled-out directory is what left this shim calling a dead `.hooks/`
# for a full day after the hooks moved into core/ (2026-07-31).

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from copilot_shared import (
    EDIT_HINTS,
    READ_HINTS,
    TERMINAL_HINTS,
    COMMAND_KEYS,
    build_payload,
    collect_paths,
    first_string,
    forward_block,
    load_input,
    run_script,
    session_id,
)
import json


def emit_allow(message: str = "") -> None:
    output: dict[str, Any] = {"continue": True}
    if message:
        output["systemMessage"] = message
    print(json.dumps(output, ensure_ascii=False))


HOOKS = Path(__file__).resolve().parents[1]


def gate(script: str, payload: dict[str, Any], tool: str, root: Path, messages: list[str]) -> bool:
    result = run_script(HOOKS / script, payload, tool, root)
    if result.stdout.strip():
        messages.append(result.stdout.strip())
    if result.returncode == 2:
        forward_block(result)
        return True
    return False


def main() -> int:
    data = load_input()
    workspace_root = Path(data.get("cwd") or os.getcwd()).resolve()
    tool_name = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    tool_name_lower = tool_name.lower()
    paths = collect_paths(workspace_root, tool_input)
    messages: list[str] = []

    if any(hint in tool_name_lower for hint in TERMINAL_HINTS):
        command = first_string(tool_input, COMMAND_KEYS)
        if command:
            payload = {"command": command, "session_id": session_id()}
            if gate("read/bash-context-gate.py", payload, "Bash", workspace_root, messages):
                return 2
        emit_allow("\n\n".join(messages))
        return 0

    if any(hint in tool_name_lower for hint in READ_HINTS) and paths:
        for file_path in paths:
            payload = {"file_path": file_path, "session_id": session_id()}
            if gate("read/context-gate.py", payload, "Read", workspace_root, messages):
                return 2
            if gate("read/pre-read.py", payload, "Read", workspace_root, messages):
                return 2
        emit_allow("\n\n".join(messages))
        return 0

    if any(hint in tool_name_lower for hint in EDIT_HINTS) and paths:
        write_like = any(hint in tool_name_lower for hint in ("create", "write", "insert"))
        canonical = "Write" if write_like else "Edit"
        for file_path in paths:
            payload = build_payload(file_path, tool_input)
            if gate("read/context-gate.py", payload, canonical, workspace_root, messages):
                return 2
            if gate("checks/pre-edit.py", payload, canonical, workspace_root, messages):
                return 2
            if write_like:
                gate("facade/facade-scan.py", payload, canonical, workspace_root, messages)
            if gate("facade/facade-gate.py", payload, canonical, workspace_root, messages):
                return 2
            if gate("checks/issues-gate.py", payload, canonical, workspace_root, messages):
                return 2
            if gate("read/spec-read-gate.py", payload, canonical, workspace_root, messages):
                return 2
        emit_allow("\n\n".join(messages))
        return 0

    emit_allow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
