#!/usr/bin/env python3
# PostToolUse: Read — record CONTEXT.md reads (consumed by context-gate.py / bash-context-gate.py)
# and interface-file reads (consumed by pre-read.sh: interface read unlocks its source). VERIFY.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import load_seen, mark_seen, parse_stdin

IFACE_SUFFIXES = ('.d.ts', '.pyi', '.dart.api', '.texif', '.csvif')


def _record_iface(session_id: str, path: str) -> None:
	marker = Path(f'/tmp/claude_iface_seen_{session_id}.txt')
	try:
		seen = set(marker.read_text().splitlines()) if marker.exists() else set()
	except OSError:
		seen = set()
	if path not in seen:
		with marker.open('a') as f:
			f.write(path + '\n')


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool and tool != 'Read':
		return 0
	raw = str(tool_input.get('file_path', ''))
	if not raw:
		return 0
	try:
		path = str(Path(raw).resolve())
	except OSError:
		path = raw
	if Path(raw).name == 'CONTEXT.md':
		if path not in load_seen(session_id):
			mark_seen(session_id, path)
	elif raw.endswith(IFACE_SUFFIXES):
		_record_iface(session_id, path)
	return 0


sys.exit(main())
