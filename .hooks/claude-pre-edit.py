#!/usr/bin/env python3
import sys, json, os, re

CODE_EXTS = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
LIMIT = 200

FIRST_LINE_COMMENT = {
    '.py':   r'^\s*#',
    '.js':   r'^\s*//', '.ts':  r'^\s*//', '.tsx':  r'^\s*//', '.dart': r'^\s*//',
    '.css':  r'^\s*/\*', '.scss': r'^\s*/\*',
    '.html': r'^\s*<!--',
}

EXAMPLE_COMMENT = {
    '.py': '# Short description of this module',
    '.js': '// Short description of this module',
    '.ts': '// Short description of this module', '.tsx': '// Short description of this module',
    '.dart': '// Short description of this module',
    '.css': '/* Short description of this stylesheet */',
    '.scss': '/* Short description of this stylesheet */',
    '.html': '<!-- Short description of this template -->',
}

data     = json.load(sys.stdin)
tool     = os.environ.get('CLAUDE_TOOL_NAME', '')
file_path = data.get('file_path', '')

_, ext = os.path.splitext(file_path)
if ext not in CODE_EXTS or file_path.endswith('.d.ts'):
    sys.exit(0)

if tool == 'Write':
    content   = data.get('content', '')
    new_lines = content.count('\n') + 1
    # Block new files created without a first-line description comment
    if not os.path.exists(file_path):
        pattern = FIRST_LINE_COMMENT.get(ext)
        first   = content.splitlines()[0] if content.strip() else ''
        if pattern and not re.match(pattern, first):
            print(f"⛔ FIRST-LINE MISSING — {file_path}")
            print(f"   New files must start with a description comment.")
            print(f"   Example: {EXAMPLE_COMMENT.get(ext, '// Description')}")
            sys.exit(2)

elif tool == 'Edit':
    if not os.path.exists(file_path):
        sys.exit(0)
    current_lines = open(file_path).read().count('\n') + 1
    net      = data.get('new_string', '').count('\n') - data.get('old_string', '').count('\n')
    new_lines = current_lines + net

else:
    sys.exit(0)

if new_lines >= LIMIT:
    print(f"⛔ SIZE GATE — {file_path} would reach {new_lines} lines (limit: {LIMIT}).")
    print(f"   Create a new module file and write there instead.")
    sys.exit(2)

sys.exit(0)
