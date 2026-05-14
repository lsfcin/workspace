#!/usr/bin/env python3
import sys, json, os

CODE_EXTS = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
LIMIT = 200

data = json.load(sys.stdin)
tool = os.environ.get('CLAUDE_TOOL_NAME', '')
file_path = data.get('file_path', '')

_, ext = os.path.splitext(file_path)
if ext not in CODE_EXTS or file_path.endswith('.d.ts'):
    sys.exit(0)

if tool == 'Write':
    new_lines = data.get('content', '').count('\n') + 1
elif tool == 'Edit':
    if not os.path.exists(file_path):
        sys.exit(0)
    current_lines = open(file_path).read().count('\n') + 1
    net = data.get('new_string', '').count('\n') - data.get('old_string', '').count('\n')
    new_lines = current_lines + net
else:
    sys.exit(0)

if new_lines >= LIMIT:
    print(f"⛔ SIZE GATE — {file_path} would reach {new_lines} lines (limit: {LIMIT}).")
    print(f"   Create a new module file and write there instead.")
    sys.exit(2)

sys.exit(0)
