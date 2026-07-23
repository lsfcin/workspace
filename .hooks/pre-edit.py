#!/usr/bin/env python3
# PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description.
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import parse_stdin

CODE_EXTS    = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss', '.tex'}
CONTENT_EXTS = {'.md', '.yaml', '.yml', '.toml'}


def load_line_limits() -> tuple[int, int]:
	limits_path = Path(__file__).with_name('line-limits.env')
	limits: dict[str, int] = {}
	for raw_line in limits_path.read_text().splitlines():
		line = raw_line.strip()
		if not line or line.startswith('#') or '=' not in line:
			continue
		name, value = line.split('=', 1)
		limits[name] = int(value)
	return limits['WARN_LINES'], limits['BLOCK_LINES']


WARN_LINES, BLOCK_LINES = load_line_limits()

FIRST_LINE_COMMENT = {
	'.py': r'^\s*#',    '.js':   r'^\s*//', '.ts':   r'^\s*//',
	'.tsx': r'^\s*//', '.dart': r'^\s*//', '.css':  r'^\s*/\*',
	'.scss': r'^\s*/\*', '.html': r'^\s*<!--',
	'.yaml': r'^\s*#', '.yml':  r'^\s*#', '.toml': r'^\s*#',
	'.tex': r'^\s*%',  '.md':   r'^\s*(#|---\s*$)',  # md: title or YAML frontmatter (skills)
}

EXAMPLE_COMMENT = {
	'.py': '# Short description',   '.js':   '// Short description',
	'.ts': '// Short description',  '.tsx':  '// Short description',
	'.dart': '// Short description', '.css': '/* Short description */',
	'.scss': '/* Short description */', '.html': '<!-- Short description -->',
	'.yaml': '# Short description', '.yml':  '# Short description',
	'.toml': '# Short description', '.tex': '% Short description of this section',
	'.md': '# Title of this document',
}

_, tool, data, _, _ = parse_stdin()
file_path = data.get('file_path', '')
basename  = os.path.basename(file_path)

# CONTEXT.md: new files must have a description on line 2 (> short description)
if basename == 'CONTEXT.md' and tool == 'Write' and not os.path.exists(file_path):
	lines = data.get('content', '').splitlines()
	line2 = lines[1].strip() if len(lines) > 1 else ''
	if not re.match(r'^>\s*\S', line2):
		print(f"⛔ CONTEXT.md DESCRIPTION MISSING — {file_path}")
		print(f"   Line 2 must be: > Short description of this directory")
		sys.exit(2)

def is_vendored(path: str) -> bool:
	"""Third-party code tracked verbatim, declared by a `.vendor` marker in the file's
	directory or any ancestor. Splitting it would fork it from upstream, so the size
	gate does not apply. Same marker the commit-time checker reads."""
	d = os.path.dirname(os.path.abspath(path))
	while d and d != '/':
		if os.path.isfile(os.path.join(d, '.vendor')):
			return True
		if os.path.isdir(os.path.join(d, '.git')):
			return False
		d = os.path.dirname(d)
	return False

_, ext = os.path.splitext(file_path)
is_code    = ext in CODE_EXTS and not file_path.endswith('.d.ts') and not is_vendored(file_path)
is_content = ext in CONTENT_EXTS and basename != 'CONTEXT.md'

if not is_code and not is_content:
	sys.exit(0)

if tool == 'Write':
	content   = data.get('content', '')
	new_lines = content.count('\n') + 1
	if not os.path.exists(file_path):
		pattern = FIRST_LINE_COMMENT.get(ext)
		first   = content.splitlines()[0] if content.strip() else ''
		if pattern and not re.match(pattern, first):
			print(f"⛔ FIRST-LINE MISSING — {file_path}")
			print(f"   New files must start with a description.")
			print(f"   Example: {EXAMPLE_COMMENT.get(ext, '# Description')}")
			sys.exit(2)

elif tool == 'Edit':
	if not os.path.exists(file_path):
		sys.exit(0)
	current_lines = open(file_path).read().count('\n') + 1
	net       = data.get('new_string', '').count('\n') - data.get('old_string', '').count('\n')
	new_lines = current_lines + net

else:
	sys.exit(0)

if is_code and new_lines >= BLOCK_LINES:
	print(f"⛔ SIZE GATE — {file_path} would reach {new_lines} lines (limit: {BLOCK_LINES}).")
	print(f"   Extract shared logic into a new module and import it from existing callers.")
	print(f"   Do NOT copy existing functions into a new file — copies are blocked at commit.")
	sys.exit(2)

sys.exit(0)
