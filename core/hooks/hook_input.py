# Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas.
import hashlib
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


def normalise(raw: str) -> str:
	"""One spelling of a path, so a marker written by one hook is legible to another.

	The alternative cost a live gate: the interface gate, while it was still shell, compared three
	spellings of one file with `grep -qxF` — this side's `C:\\Users\\...`, the payload's
	`c:\\Users\\...`, and a `readlink -f` `c:/Users/...`. None matched, so it blocked every source
	read and reading the interface, the thing its own message promised would unlock it, never could.
	Both ends call this now, which is the fix the port made structural.
	"""
	try:
		return str(Path(raw).resolve())
	except OSError:
		return raw


# A SESSION MARKER IS A DIRECTORY, ONE FILE PER ENTRY, and that shape IS the fix for a lost mark.
#
# These were one text file appended to per entry, and a PostToolUse hook is one process per Read, so
# a parallel batch of N reads ran N of them at once. Measured 2026-09-02 on this clone, 16 concurrent
# trackers over 30 rounds: `open(path, 'a')` lost an entry in EVERY round — 22% of writes gone — and
# `os.open(O_APPEND)` + a single `os.write` lost them in 8 rounds of 20. The CRT emulates append as
# seek-to-end-then-write, which is not atomic across processes, so the last writer overwrites what
# landed between its seek and its write. What the agent saw was a gate re-demanding a CONTEXT.md it
# had just read, on the turn it did the right thing.
#
# Creating a DISTINCT file is atomic on both systems: no lock, no retry, and nothing here has to ask
# the seam what an operating system is. The entry's name is a digest of the path so the same mark
# twice is the same file, which is also what makes marking idempotent and lets every caller drop its
# read-before-write guard.
def _store(session_id: str, kind: str) -> Path:
	return session_state(f'claude_{kind}_{session_id}')


def _load(session_id: str, kind: str) -> set[str]:
	try:
		return {entry.read_text(encoding='utf-8').strip()
		        for entry in _store(session_id, kind).iterdir()}
	except OSError:
		return set()


def _mark(session_id: str, kind: str, path: str) -> None:
	store = _store(session_id, kind)
	try:
		store.mkdir(parents=True, exist_ok=True)
		entry = store / hashlib.sha1(path.encode('utf-8')).hexdigest()[:16]
		entry.write_text(path, encoding='utf-8', newline='\n')
	except OSError:
		pass  # a PostToolUse exit status is read by nobody; a marker we cannot write is not fatal


def load_seen(session_id: str) -> set[str]:
	return _load(session_id, 'ctx_seen')


def mark_seen(session_id: str, path: str) -> None:
	_mark(session_id, 'ctx_seen', path)


# The interface marker is the same session-scoped ledger one store over, and it lived privately in
# read/context-tracker.py — which no gate can import, because a hyphen is not an identifier. That is
# the whole reason context-tracker grew a query CLI arm, now deleted with the shell caller that
# needed it. Beside its twin, both readers just call it. The facade pair is the third of the same
# shape, hand-rolled in facade-{gate,tracker}.py until the measurement above showed it had been
# losing marks the whole time too.
def load_iface_seen(session_id: str) -> set[str]:
	return _load(session_id, 'iface_seen')


def mark_iface_seen(session_id: str, path: str) -> None:
	_mark(session_id, 'iface_seen', path)


def load_facades(session_id: str) -> set[str]:
	return _load(session_id, 'facades')


def mark_facade(session_id: str, path: str) -> None:
	_mark(session_id, 'facades', path)


def announced(session_id: str, kind: str, key: str) -> bool:
	"""True when `key` has already been said this session — and records it when it has not.

	Every "say it once" nudge wants this and each used to grep its own text file for a substring,
	which matched a path that merely CONTAINED another. Ask-and-record in one call, because the two
	halves apart are what let a nudge mark itself said on a turn it was never shown.
	"""
	if key in _load(session_id, kind):
		return True
	_mark(session_id, kind, key)
	return False
