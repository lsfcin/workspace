#!/usr/bin/env python3
# Codex adapter: translate apply_patch and Bash hook payloads onto canonical workspace gates.
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HOOKS = ROOT / "core" / "hooks"
sys.path.insert(0, str(HOOKS))
import feature_law  # noqa: E402

MARKER = re.compile(r"^\*\*\* (Add File|Update File|Delete File|Move to): (.+)$")


def input_data() -> dict[str, Any]:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def patches(data: dict[str, Any]) -> list[tuple[str, dict[str, str]]]:
    """Return canonical tool + payload for every apply_patch file section."""
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return []
    command = str(tool_input.get("command", ""))
    parts: list[tuple[str, str, list[str]]] = []
    current: tuple[str, str, list[str]] | None = None
    for line in command.splitlines():
        match = MARKER.match(line)
        if match:
            if current:
                parts.append(current)
            current = (match.group(1), match.group(2).strip(), [])
        elif current:
            current[2].append(line)
    if current:
        parts.append(current)

    cwd = Path(str(data.get("cwd") or ROOT))
    session_id = str(data.get("session_id") or "")
    out: list[tuple[str, dict[str, str]]] = []
    for operation, raw_path, body in parts:
        path = Path(raw_path)
        path = (path if path.is_absolute() else cwd / path).resolve()
        if operation == "Delete File":
            continue
        added = [line[1:] for line in body if line.startswith("+") and not line.startswith("+++")]
        removed = [line[1:] for line in body if line.startswith("-") and not line.startswith("---")]
        canonical = "Write" if operation == "Add File" else "Edit"
        payload = {"file_path": str(path), "session_id": session_id}
        if canonical == "Write":
            payload["content"] = "\n".join(added)
        else:
            payload["old_string"] = "\n".join(removed)
            payload["new_string"] = "\n".join(added)
        out.append((canonical, payload))
    return out


def call(script: str, payload: dict[str, str], tool: str, post: bool = False) -> subprocess.CompletedProcess[str]:
    path = HOOKS / script
    env = {**os.environ, "CLAUDE_TOOL_NAME": tool}
    text = json.dumps({"session_id": payload.get("session_id", ""), "cwd": str(ROOT),
                       "tool_name": tool, "tool_input": payload})
    if post:
        env["CLAUDE_TOOL_INPUT"] = text
        return subprocess.run(["bash" if path.suffix == ".sh" else "python3", str(path)],
                              capture_output=True, text=True, cwd=ROOT, env=env, check=False)
    return subprocess.run(["bash" if path.suffix == ".sh" else "python3", str(path)], input=text,
                          capture_output=True, text=True, cwd=ROOT, env=env, check=False)


def context_from(result: subprocess.CompletedProcess[str]) -> list[str]:
    try:
        data = json.loads(result.stdout)
        value = data.get("hookSpecificOutput", {}).get("additionalContext", "")
        return [value] if isinstance(value, str) and value else []
    except json.JSONDecodeError:
        return [result.stdout.strip()] if result.stdout.strip() else []


def deny(result: subprocess.CompletedProcess[str]) -> int:
    message = (result.stderr or result.stdout).strip() or "Workspace policy blocked this operation."
    print(message, file=sys.stderr)
    return 2


def first_delivery(data: dict[str, Any]) -> bool:
    """Codex matcher aliases can deliver one apply_patch to two matching groups."""
    session = str(data.get("session_id") or "")
    tool_use = str(data.get("tool_use_id") or "")
    event = str(data.get("hook_event_name") or "")
    if not session or not tool_use or not event:
        return True
    marker = Path(f"/tmp/wos_codex_hook_{session}_{tool_use}_{event}")
    try:
        marker.touch(exist_ok=False)
        return True
    except FileExistsError:
        return False


def pre(data: dict[str, Any]) -> int:
    tool = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    if tool == "Bash":
        payload = {"command": str(tool_input.get("command", "")),
                   "session_id": str(data.get("session_id") or "")}
        for script in ("read/bash-context-gate.py", "checks/heredoc-gate.py"):
            result = call(script, payload, "Bash")
            if result.returncode == 2:
                return deny(result)
            for message in context_from(result):
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                           "additionalContext": message}}))
        return 0
    if tool != "apply_patch":
        if tool == "Read":
            raw = tool_input.get("file_path") or tool_input.get("path")
            if isinstance(raw, str) and raw:
                payload = {"file_path": raw, "session_id": str(data.get("session_id") or "")}
                for script in ("read/context-gate.py", "read/pre-read.sh"):
                    result = call(script, payload, "Read")
                    if result.returncode == 2:
                        return deny(result)
        return 0
    messages: list[str] = []
    for canonical, payload in patches(data):
        scripts = ["read/context-gate.py", "checks/pre-edit.py"]
        if canonical == "Write":
            scripts.append("facade/facade-scan.py")
        scripts += ["facade/facade-gate.py", "checks/issues-gate.py", "read/spec-read-gate.py"]
        for script in scripts:
            result = call(script, payload, canonical)
            if result.returncode == 2:
                return deny(result)
            messages += context_from(result)
    if messages:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                   "additionalContext": "\n\n".join(messages)}}))
    return 0


def post(data: dict[str, Any]) -> int:
    if str(data.get("tool_name") or "") != "apply_patch":
        return 0
    messages: list[str] = []
    for canonical, payload in patches(data):
        result = call("post-edit.sh", payload, canonical, post=True)
        messages += [text for text in (result.stdout.strip(), result.stderr.strip()) if text]
    if messages:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                   "additionalContext": "\n\n".join(messages)}}))
    return 0


def main() -> int:
    if not feature_law.is_enabled("codex-hooks"):
        return 0
    data = input_data()
    if not first_delivery(data):
        return 0
    if data.get("hook_event_name") == "PostToolUse":
        return post(data)
    return pre(data)


if __name__ == "__main__":
    raise SystemExit(main())
