# Copilot PreToolUse hook: enforce workspace read and edit policy.

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

READ_HINTS = ("read", "open", "view", "inspect", "search")
EDIT_HINTS = ("edit", "write", "create", "replace", "insert", "delete", "patch", "apply")
PATH_KEYS = (
    "filePath",
    "file_path",
    "path",
    "file",
    "filepath",
    "targetPath",
    "target_path",
)
CONTENT_KEYS = ("content", "text", "newCode", "new_code")
OLD_KEYS = ("oldString", "old_string", "oldText", "old_text")
NEW_KEYS = ("newString", "new_string", "newText", "new_text")


def load_input() -> dict[str, Any]:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def normalize_path(workspace_root: Path, raw: Any) -> str | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = workspace_root / candidate
    return str(candidate.resolve())


def collect_paths(workspace_root: Path, value: Any) -> list[str]:
    paths: list[str] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if key in PATH_KEYS:
                    normalized = normalize_path(workspace_root, child)
                    if normalized:
                        paths.append(normalized)
                elif key == "files" and isinstance(child, list):
                    for item in child:
                        if isinstance(item, str):
                            normalized = normalize_path(workspace_root, item)
                            if normalized:
                                paths.append(normalized)
                        else:
                            visit(item)
                else:
                    visit(child)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(value)
    unique_paths: list[str] = []
    for path in paths:
        if path not in unique_paths:
            unique_paths.append(path)
    return unique_paths


def first_string(value: Any, keys: tuple[str, ...]) -> str:
    if not isinstance(value, dict):
        return ""
    for key in keys:
        candidate = value.get(key)
        if isinstance(candidate, str):
            return candidate
    return ""


def build_payload(file_path: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {"file_path": file_path}
    content = first_string(tool_input, CONTENT_KEYS)
    if content:
        payload["content"] = content
    old_string = first_string(tool_input, OLD_KEYS)
    if old_string:
        payload["old_string"] = old_string
    new_string = first_string(tool_input, NEW_KEYS)
    if new_string:
        payload["new_string"] = new_string
    return payload


def run_script(script: Path, payload: dict[str, Any], tool_name: str, workspace_root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CLAUDE_TOOL_NAME"] = tool_name
    return subprocess.run(
        ["python3", str(script)] if script.suffix == ".py" else ["bash", str(script)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace_root),
        env=env,
        check=False,
    )


def emit_allow(message: str = "") -> None:
    output: dict[str, Any] = {"continue": True}
    if message:
        output["systemMessage"] = message
    print(json.dumps(output, ensure_ascii=False))


def main() -> int:
    data = load_input()
    workspace_root = Path(data.get("cwd") or os.getcwd()).resolve()
    tool_name = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    tool_name_lower = tool_name.lower()
    paths = collect_paths(workspace_root, tool_input)

    if any(hint in tool_name_lower for hint in READ_HINTS) and paths:
        messages: list[str] = []
        for file_path in paths:
            result = run_script(workspace_root / ".hooks" / "pre-read.sh", {"file_path": file_path}, tool_name, workspace_root)
            if result.stdout.strip():
                messages.append(result.stdout.strip())
            if result.returncode == 2:
                if result.stdout:
                    sys.stdout.write(result.stdout)
                if result.stderr:
                    sys.stderr.write(result.stderr)
                return 2
        emit_allow("\n\n".join(messages))
        return 0

    if any(hint in tool_name_lower for hint in EDIT_HINTS) and paths:
        messages = []
        write_like = any(hint in tool_name_lower for hint in ("create", "write", "insert"))
        canonical_tool_name = "Write" if write_like else "Edit"
        for file_path in paths:
            payload = build_payload(file_path, tool_input)
            # size / description enforcement
            result = run_script(workspace_root / ".hooks" / "pre-edit.py", payload, canonical_tool_name, workspace_root)
            if result.stdout.strip():
                messages.append(result.stdout.strip())
            if result.returncode == 2:
                if result.stdout:
                    sys.stdout.write(result.stdout)
                if result.stderr:
                    sys.stderr.write(result.stderr)
                return 2
            # facade-scan: inform about existing facade exports before creating new file
            if write_like:
                result = run_script(workspace_root / ".hooks" / "facade-scan.py", payload, canonical_tool_name, workspace_root)
                if result.stdout.strip():
                    messages.append(result.stdout.strip())
            # facade-gate: block Code/ module edits until facade read this session
            result = run_script(workspace_root / ".hooks" / "facade-gate.py", payload, canonical_tool_name, workspace_root)
            if result.stdout.strip():
                messages.append(result.stdout.strip())
            if result.returncode == 2:
                if result.stdout:
                    sys.stdout.write(result.stdout)
                if result.stderr:
                    sys.stderr.write(result.stderr)
                return 2
        emit_allow("\n\n".join(messages))
        return 0

    emit_allow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
