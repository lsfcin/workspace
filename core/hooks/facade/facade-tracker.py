#!/usr/bin/env python3
# PostToolUse: Read — record facade file reads to session state for facade-gate.py.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from file_law import FACADES  # noqa: E402
from hook_input import parse_stdin
from platform_law import session_state  # noqa: E402


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool and tool != 'Read':
		return 0
	file_path = str(tool_input.get('file_path', ''))
	if Path(file_path).name not in FACADES:
		return 0
	session_file = session_state(f'claude_facades_{session_id}.txt')
	with session_file.open('a', encoding='utf-8', newline='\n') as f:
		f.write(file_path + '\n')
	return 0


sys.exit(main())
