# Antigravity provider shim: translates Antigravity lifecycle events to canonical WOS gates.

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law
from platform_law import WORKSPACE_ROOT, interpreter

HOOKS = Path(__file__).resolve().parents[1]


def run_gate(script: str, payload: dict[str, Any], tool: str, extra_args: list[str] | None = None) -> tuple[int, str]:
    full_path = HOOKS / script
    cmd = [interpreter(), str(full_path)] if full_path.suffix == ".py" else ["bash", str(full_path)]
    if extra_args:
        cmd.extend(extra_args)
    env = {**os.environ, "CLAUDE_TOOL_NAME": tool}
    data = json.dumps(payload)
    env["CLAUDE_TOOL_INPUT"] = data
    proc = subprocess.run(cmd, input=data, text=True, capture_output=True, cwd=str(WORKSPACE_ROOT), env=env, check=False, encoding='utf-8')
    msg = (proc.stderr or proc.stdout).strip()
    return proc.returncode, msg


def pre_tool(call: dict[str, Any], sid: str) -> dict[str, Any]:
    name = call.get("name", "")
    args = call.get("args") or {}
    gates: list[tuple[str, str, dict[str, Any]]] = []

    if name == "view_file":
        p = {"file_path": args.get("AbsolutePath", ""), "session_id": sid}
        gates = [("read/context-gate.py", "Read", p), ("read/pre-read.sh", "Read", p)]
    elif name == "replace_file_content":
        p = {"file_path": args.get("TargetFile", ""), "old_string": args.get("TargetContent", ""),
             "new_string": args.get("ReplacementContent", ""), "session_id": sid}
        gates = [("read/context-gate.py", "Edit", p), ("checks/pre-edit.py", "Edit", p),
                 ("facade/facade-gate.py", "Edit", p), ("checks/issues-gate.py", "Edit", p),
                 ("read/spec-read-gate.py", "Edit", p)]
    elif name == "write_to_file":
        p = {"file_path": args.get("TargetFile", ""), "content": args.get("CodeContent", ""), "session_id": sid}
        gates = [("read/context-gate.py", "Write", p), ("checks/pre-edit.py", "Write", p),
                 ("facade/facade-scan.py", "Write", p), ("facade/facade-gate.py", "Write", p),
                 ("checks/issues-gate.py", "Write", p), ("read/spec-read-gate.py", "Write", p)]
    elif name == "run_command":
        p = {"command": args.get("CommandLine", ""), "session_id": sid}
        gates = [("read/bash-context-gate.py", "Bash", p), ("checks/heredoc-gate.py", "Bash", p)]
    elif name == "grep_search":
        p = {"path": args.get("SearchPath", ""), "session_id": sid}
        gates = [("read/context-gate.py", "Grep", p)]
    elif name == "invoke_subagent":
        subs = args.get("Subagents", [])
        txt = "\n".join(s.get("Prompt", "") for s in subs if isinstance(s, dict))
        p = {"prompt": txt, "session_id": sid, "prompt_id": sid}
        gates = [("read/agent-context.py", "Agent", p)]

    info_msgs: list[str] = []
    for script, tool, payload in gates:
        rc, msg = run_gate(script, payload, tool)
        if rc == 2:
            return {"decision": "deny", "reason": msg or f"Blocked by {script}"}
        if msg:
            info_msgs.append(msg)

    out: dict[str, Any] = {"decision": "allow"}
    if info_msgs:
        out["reason"] = "\n".join(info_msgs)
    return out


def post_tool(call: dict[str, Any], sid: str) -> dict[str, Any]:
    name = call.get("name", "")
    args = call.get("args") or {}
    if name == "view_file":
        p = {"file_path": args.get("AbsolutePath", ""), "session_id": sid}
        run_gate("facade/facade-tracker.py", p, "Read")
        run_gate("read/context-tracker.py", p, "Read")
    elif name in ("replace_file_content", "write_to_file"):
        path = args.get("TargetFile", "")
        tool = "Write" if name == "write_to_file" else "Edit"
        p = {"file_path": path, "session_id": sid}
        if name == "write_to_file":
            p["content"] = args.get("CodeContent", "")
        else:
            p["old_string"] = args.get("TargetContent", "")
            p["new_string"] = args.get("ReplacementContent", "")
        run_gate("post-edit.sh", p, tool)
    return {}


def pre_invocation(data: dict[str, Any]) -> dict[str, Any]:
    msgs: list[str] = []
    sid = str(data.get("conversationId", ""))
    inv_num = data.get("invocationNum", 0)
    if inv_num == 1:
        run_gate("session/session-prune.sh", {}, "SessionStart")
        run_gate("git/branch_marker.py", {}, "SessionStart", extra_args=["record"])
        for script in ("session/mirror-heal.py", "session/inbox-nudge.py",
                       "session/compass-nudge.py"):
            _, msg = run_gate(script, {}, "SessionStart")
            if msg:
                msgs.append(msg)
    _, meter = run_gate("session/context-meter.py", {"session_id": sid}, "PreInvocation")
    if meter:
        msgs.append(meter)
    combined = "\n\n".join(m for m in msgs if m.strip())
    return {"injectSteps": [{"ephemeralMessage": combined}]} if combined else {}


def main() -> int:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    if not feature_law.is_enabled("antigravity-hooks"):
        empty: dict[str, Any] = {"decision": "allow"} if event == "PreToolUse" else {}
        print(json.dumps(empty))
        return 0

    sid = str(data.get("conversationId") or os.getppid())
    res: dict[str, Any] = {}
    if event == "PreToolUse":
        res = pre_tool(data.get("toolCall") or {}, sid)
    elif event == "PostToolUse":
        res = post_tool(data.get("toolCall") or {}, sid)
    elif event == "PreInvocation":
        res = pre_invocation(data)

    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
