#!/usr/bin/env python3
# PostToolUse: Read — record facade file reads to session state for facade-gate.py.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import parse_stdin

FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool and tool != 'Read':
		return 0
	file_path = str(tool_input.get('file_path', ''))
	if Path(file_path).name not in FACADE_NAMES:
		return 0
	session_file = Path(f'/tmp/claude_facades_{session_id}.txt')
	with session_file.open('a') as f:
		f.write(file_path + '\n')
	return 0


sys.exit(main())
