# Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas.
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from platform_law import session_state  # noqa: E402


def _ppid_session() -> str:
	shell_pid = os.getppid()
	try:
		result = subprocess.check_output(
			['ps', '-o', 'ppid=', '-p', str(shell_pid)],
			text=True, stderr=subprocess.DEVNULL, encoding='utf-8'
		).strip()
		return result if result.isdigit() else str(shell_pid)
	except Exception:
		return str(shell_pid)


def parse_stdin() -> tuple[dict[str, Any], str, dict[str, Any], str, str]:
	"""Returns (raw, tool_name, tool_input, session_id, cwd).

	Current Claude Code sends {session_id, cwd, tool_name, tool_input:{...}}.
	Legacy/Copilot shim sends flat tool_input fields at top level with
	CLAUDE_TOOL_NAME / CLAUDE_TOOL_INPUT in the environment.
	"""
	raw_env = os.environ.get('CLAUDE_TOOL_INPUT', '')
	try:
		data = json.loads(raw_env) if raw_env else json.load(sys.stdin)
	except Exception:
		data = {}
	if not isinstance(data, dict):
		data = {}

	tool = data.get('tool_name') or os.environ.get('CLAUDE_TOOL_NAME', '')
	tool_input = data.get('tool_input')
	if not isinstance(tool_input, dict):
		tool_input = data  # flat legacy schema: fields live at top level
	session_id = str(data.get('session_id') or '') or _ppid_session()
	cwd = str(data.get('cwd') or os.getcwd())
	return data, tool, tool_input, session_id, cwd


def is_subagent(raw: dict[str, Any]) -> bool:
	"""True when this hook fired inside a worker rather than the main thread.

	`agent_id` is present only within a subagent — that is the harness's own documented way to tell
	the two apart, and `agent_type` is NOT (it is set for the main thread too in --agent sessions).

	The rule lives here because two gates need it and a second copy is the drift the law modules
	exist to catch. Why the gates use it: CONTEXT.md carries *routing*, and a worker handed one
	explicit path does not need to know where else it could have gone. Correctness constraints live
	in SPECS.md and `spec-read-gate.py` still fires for everyone. Ruled 2026-08-15 (Lucas); measured
	in core/experiments/subagent-context-chain.md.
	"""
	return bool(raw.get('agent_id'))


def seen_file(session_id: str) -> str:
	return str(session_state(f'claude_ctx_seen_{session_id}.txt'))


def load_seen(session_id: str) -> set[str]:
	try:
		with open(seen_file(session_id), encoding='utf-8') as f:
			return {line.strip() for line in f if line.strip()}
	except OSError:
		return set()


def mark_seen(session_id: str, path: str) -> None:
	with open(seen_file(session_id), 'a', encoding='utf-8', newline='\n') as f:
		f.write(path + '\n')
