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


def _record_iface(session_id: str, path: str) -> None:
	marker = session_state(f'claude_iface_seen_{session_id}.txt')
	try:
		seen = set(marker.read_text(encoding='utf-8').splitlines()) if marker.exists() else set()
	except OSError:
		seen = set()
	if path not in seen:
		with marker.open('a', encoding='utf-8') as f:
			f.write(path + '\n')


def main() -> int:
	if not feature_law.is_enabled('subtree-read-tracking'):
		return 0  # switched off: nothing is recorded, so the chain gate fires per file again
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
	if Path(raw).name in ('CONTEXT.md', 'SPEC.md'):
		if path not in load_seen(session_id):
			mark_seen(session_id, path)
	elif raw.endswith(IFACE_SUFFIXES):
		_record_iface(session_id, path)
	return 0


sys.exit(main())
