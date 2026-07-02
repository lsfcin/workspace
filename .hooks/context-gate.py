#!/usr/bin/env python3
# PreToolUse: Read|Edit|Write|Grep|NotebookEdit — force-read the CONTEXT.md chain of the
# target's subtree before any other file access. Session-deduped via marker file
# (/tmp/claude_ctx_seen_<session_id>.txt, written by context-tracker.py). See VERIFY.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import load_seen, parse_stdin

WORKSPACE = Path('/mnt/workspace')
GATED_TOOLS = {'Read', 'Edit', 'Write', 'Grep', 'NotebookEdit'}
# Always freely readable — deadlock guard + docs that ARE the context.
EXEMPT_NAMES = {'CONTEXT.md', 'AGENTS.md', 'CLAUDE.md', 'MEMORY.md'}
SKIP_PARTS = {'.git', 'node_modules', 'dist', '.codegraph', '__pycache__', '.vscode'}


def target_path(tool: str, tool_input: dict) -> str:
	if tool == 'NotebookEdit':
		return str(tool_input.get('notebook_path', ''))
	if tool == 'Grep':
		return str(tool_input.get('path', ''))
	return str(tool_input.get('file_path', ''))


def context_chain(target: Path) -> list[Path]:
	"""CONTEXT.md files from the target's directory up to (excluding) workspace root."""
	start = target if target.is_dir() else target.parent
	chain: list[Path] = []
	current = start
	while current != WORKSPACE and current != current.parent:
		ctx = current / 'CONTEXT.md'
		if ctx.is_file():
			chain.append(ctx)
		current = current.parent
	return chain


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool not in GATED_TOOLS:
		return 0
	raw = target_path(tool, tool_input)
	if not raw:
		return 0
	target = Path(raw)
	if not target.is_absolute():
		return 0
	try:
		target = target.resolve()
	except OSError:
		return 0
	if not str(target).startswith(str(WORKSPACE) + '/'):
		return 0
	if target.name in EXEMPT_NAMES:
		return 0
	if SKIP_PARTS.intersection(target.parts):
		return 0

	seen = load_seen(session_id)
	unseen = [c for c in context_chain(target) if str(c) not in seen]
	if not unseen:
		return 0

	print('CONTEXT GATE - subtree context not yet loaded this session.', file=sys.stderr)
	print('Read these CONTEXT.md files first (one parallel batch), then retry:', file=sys.stderr)
	for ctx in unseen:
		print(f'   {ctx}', file=sys.stderr)
	return 2


sys.exit(main())
