#!/usr/bin/env python3
# PostToolUse: Read — record CONTEXT.md/SPEC.md reads (consumed by context-gate.py /
# bash-context-gate.py / spec-read-gate.py) and interface-file reads (consumed by pre-read.sh:
# interface read unlocks its source). ROADMAP-verify.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
from hook_input import load_seen, mark_seen, parse_stdin
from platform_law import session_state  # noqa: E402

IFACE_SUFFIXES = ('.d.ts', '.pyi', '.dart.api', '.texif', '.csvif')


def _iface_marker(session_id: str):
	return session_state(f'claude_iface_seen_{session_id}.txt')


def _iface_seen(session_id: str) -> set:
	marker = _iface_marker(session_id)
	try:
		return set(marker.read_text(encoding='utf-8').splitlines()) if marker.exists() else set()
	except OSError:
		return set()


def _record_iface(session_id: str, path: str) -> None:
	if path not in _iface_seen(session_id):
		with _iface_marker(session_id).open('a', encoding='utf-8', newline='\n') as f:
			f.write(path + '\n')


def was_read(session_id: str, raw: str) -> bool:
	"""Whether `raw` names an interface already read this session, however it is spelled.

	WHY THIS ARM EXISTS, AND WHY THE QUESTION CANNOT BE ASKED IN SHELL. read/pre-read.sh used to
	answer it with `grep -qxF`, comparing three spellings of one file: this module writes
	`C:\\Users\\...` (Path.resolve), the hook payload arrives as `c:\\Users\\...`, and the
	`readlink -f` in between produced `c:/Users/...`. None matched, so the gate blocked every
	source read and reading the interface -- the thing its own message promised would unlock it --
	could never satisfy it. A gate that can only block is the mirror of one that can only pass.

	The CONTEXT.md chain gate never had this defect for one reason: both of its ends are Python and
	call the same normalisation. So the bug is not Windows, it is the shell/Python boundary, and
	the fix is to move the comparison to the side that owns the marker rather than to spell the
	path more carefully on the other. `_normalise` is used by the writer directly below.
	"""
	return _normalise(raw) in _iface_seen(session_id)


def _normalise(raw: str) -> str:
	try:
		return str(Path(raw).resolve())
	except OSError:
		return raw


def main() -> int:
	# `--seen <session-id> <path>` is a QUERY, not a hook run: exit 0 when that interface has been
	# read this session. read/pre-read.sh is the caller, and it asks only on the branch that is
	# about to block -- rare -- so the subprocess this costs is not on the per-Read path.
	if len(sys.argv) == 4 and sys.argv[1] == '--seen':
		return 0 if was_read(sys.argv[2], sys.argv[3]) else 1
	if not feature_law.is_enabled('subtree-read-tracking'):
		return 0  # switched off: nothing is recorded, so the chain gate fires per file again
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool and tool != 'Read':
		return 0
	raw = str(tool_input.get('file_path', ''))
	if not raw:
		return 0
	path = _normalise(raw)
	if Path(raw).name in ('CONTEXT.md', 'SPEC.md'):
		if path not in load_seen(session_id):
			mark_seen(session_id, path)
	elif raw.endswith(IFACE_SUFFIXES):
		_record_iface(session_id, path)
	return 0


sys.exit(main())
