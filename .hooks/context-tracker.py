#!/usr/bin/env python3
# PostToolUse: Read — record CONTEXT.md reads into the session seen-marker file,
# consumed by context-gate.py and bash-context-gate.py. See VERIFY.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import load_seen, mark_seen, parse_stdin


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool and tool != 'Read':
		return 0
	raw = str(tool_input.get('file_path', ''))
	if not raw or Path(raw).name != 'CONTEXT.md':
		return 0
	try:
		path = str(Path(raw).resolve())
	except OSError:
		path = raw
	if path not in load_seen(session_id):
		mark_seen(session_id, path)
	return 0


sys.exit(main())
