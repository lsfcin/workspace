#!/usr/bin/env python3
# PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description.
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from file_law import CODE_EXTS, EXAMPLE_COMMENT, is_authored, load_limits
from hook_input import capability, parse_stdin

CONTENT_EXTS = {'.md', '.yaml', '.yml', '.toml'}
# parents[3], not [2]: this file is core/hooks/checks/pre-edit.py, so [2] is core/ and every
# workspace-relative `vendored.txt` pattern silently failed to match — is_vendored() always
# returned False here, and the size gate blocked the vendored files that list exists to waive.
# Latent for as long as the file has been in checks/; caught by reading, not by a failure.
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

_limits = load_limits()
WARN_LINES, BLOCK_LINES = _limits['WARN_LINES'], _limits['BLOCK_LINES']

FIRST_LINE_COMMENT = {
	'.py': r'^\s*#',    '.js':   r'^\s*//', '.ts':   r'^\s*//',
	'.tsx': r'^\s*//', '.dart': r'^\s*//', '.css':  r'^\s*/\*',
	'.scss': r'^\s*/\*', '.html': r'^\s*<!--',
	'.yaml': r'^\s*#', '.yml':  r'^\s*#', '.toml': r'^\s*#',
	'.tex': r'^\s*%',  '.md':   r'^\s*(#|---\s*$)',  # md: title or YAML frontmatter (skills)
}

def block(*lines):
	"""Reject the edit, on stderr, which is the only stream the model is handed.

	Claude Code feeds a PreToolUse exit-2's STDERR back as the blocking reason; stdout is
	dropped. This gate was the only one of six printing to stdout, so every rejection here
	arrived as "No stderr output" — an edit blocked with no reason attached, costing a round
	of investigation each time. It read as intermittent because it is provider-shaped, not
	path-shaped: the opencode and copilot shims concatenate both streams and were fine, and
	running the hook by hand shows stdout in the terminal. Only Claude Code went mute.
	"""
	print(*lines, sep='\n', file=sys.stderr)
	sys.exit(2)


_, tool, data, _, _ = parse_stdin()
# By capability, never by name (b20260901). The two branches below then ask the PAYLOAD which
# shape of write this is: whole content, or a patch. A harness naming its tools differently
# still sends one of those two shapes, and neither branch has ever known the tool's name for
# any reason but its shape.
if capability(tool, data) != 'write':
	sys.exit(0)
file_path = data.get('file_path', '')
basename  = os.path.basename(file_path)

# CONTEXT.md: new files must have a description on line 2 (> short description)
if basename == 'CONTEXT.md' and 'content' in data and not os.path.exists(file_path):
	lines = data.get('content', '').splitlines()
	line2 = lines[1].strip() if len(lines) > 1 else ''
	if not re.match(r'^>\s*\S', line2):
		block(f"⛔ CONTEXT.md DESCRIPTION MISSING — {file_path}",
		      f"   Line 2 must be: > Short description of this directory")

_, ext = os.path.splitext(file_path)
_path      = Path(file_path)
is_code    = is_authored(_path, WORKSPACE_ROOT)
is_content = ext in CONTENT_EXTS and basename != 'CONTEXT.md'

if not is_code and not is_content:
	sys.exit(0)

if 'content' in data:
	content   = data.get('content', '')
	new_lines = len(content.splitlines())
	if not os.path.exists(file_path):
		pattern = FIRST_LINE_COMMENT.get(ext)
		first   = content.splitlines()[0] if content.strip() else ''
		if pattern and not re.match(pattern, first):
			block(f"⛔ FIRST-LINE MISSING — {file_path}",
			      f"   New files must start with a description.",
			      f"   Example: {EXAMPLE_COMMENT.get(ext, '# Description')}")

elif 'new_string' in data:
	if not os.path.exists(file_path):
		sys.exit(0)
	current_lines = len(open(file_path, encoding='utf-8').read().splitlines())
	net       = data.get('new_string', '').count('\n') - data.get('old_string', '').count('\n')
	new_lines = current_lines + net

else:
	sys.exit(0)

if is_code and new_lines >= BLOCK_LINES:
	block(f"⛔ SIZE GATE — {file_path} would reach {new_lines} lines (limit: {BLOCK_LINES}).",
	      f"   Extract shared logic into a new module and import it from existing callers.",
	      f"   Do NOT copy existing functions into a new file — copies are blocked at commit.")

sys.exit(0)
