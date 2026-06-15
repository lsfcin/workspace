#!/usr/bin/env python3
# PostToolUse: Read — record facade file reads to session state for facade-gate.py.
import json, os, subprocess, sys
from pathlib import Path

FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}


def get_session_id() -> str:
    shell_pid = os.getppid()
    try:
        result = subprocess.check_output(
            ['ps', '-o', 'ppid=', '-p', str(shell_pid)],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        return result if result.isdigit() else str(shell_pid)
    except Exception:
        return str(shell_pid)


# PostToolUse: input is in CLAUDE_TOOL_INPUT env var (stdin carries tool result).
raw = os.environ.get('CLAUDE_TOOL_INPUT', '')
try:
    data = json.loads(raw) if raw else json.load(sys.stdin)
except Exception:
    sys.exit(0)

file_path = data.get('file_path', '')
if Path(file_path).name not in FACADE_NAMES:
    sys.exit(0)

session_file = Path(f'/tmp/claude_facades_{get_session_id()}.txt')
with session_file.open('a') as f:
    f.write(file_path + '\n')

sys.exit(0)
