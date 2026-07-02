#!/usr/bin/env python3
# PreToolUse: Bash — close the cat/head/grep bypass: extract workspace file paths from the
# command string and apply the same CONTEXT.md chain gate as context-gate.py.
# Known residual hole: dynamically constructed paths escape. See VERIFY.md W1.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import load_seen, parse_stdin

WORKSPACE = Path('/mnt/workspace')
EXEMPT_NAMES = {'CONTEXT.md', 'AGENTS.md', 'CLAUDE.md', 'MEMORY.md'}
SKIP_PARTS = {'.git', 'node_modules', 'dist', '.codegraph', '__pycache__', '.vscode', '.hooks'}
TOKEN_RE = re.compile(r'''[^\s'"`;|&<>()=]+''')


def candidates(command: str, cwd: str) -> set[Path]:
	found: set[Path] = set()
	for token in TOKEN_RE.findall(command):
		if '/' not in token:
			continue
		raw = token.strip('\'",:')
		if raw.startswith('~') or raw.startswith('-'):
			continue
		path = Path(raw) if raw.startswith('/') else Path(cwd) / raw
		try:
			path = path.resolve()
		except OSError:
			continue
		if not path.is_file():
			continue
		if not str(path).startswith(str(WORKSPACE) + '/'):
			continue
		if path.name in EXEMPT_NAMES or SKIP_PARTS.intersection(path.parts):
			continue
		found.add(path)
	return found


def context_chain(target: Path) -> list[Path]:
	chain: list[Path] = []
	current = target.parent
	while current != WORKSPACE and current != current.parent:
		ctx = current / 'CONTEXT.md'
		if ctx.is_file():
			chain.append(ctx)
		current = current.parent
	return chain


def main() -> int:
	_, tool, tool_input, session_id, cwd = parse_stdin()
	if tool and tool != 'Bash':
		return 0
	command = str(tool_input.get('command', ''))
	if not command:
		return 0
	seen = load_seen(session_id)
	unseen: list[str] = []
	for path in candidates(command, cwd):
		for ctx in context_chain(path):
			if str(ctx) not in seen and str(ctx) not in unseen:
				unseen.append(str(ctx))
	if not unseen:
		return 0
	print('CONTEXT GATE (Bash) - command touches files in a subtree whose context', file=sys.stderr)
	print('is not loaded. Read these CONTEXT.md files with the Read tool, then retry:', file=sys.stderr)
	for ctx in sorted(unseen):
		print(f'   {ctx}', file=sys.stderr)
	return 2


sys.exit(main())
