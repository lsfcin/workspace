#!/usr/bin/env python3
# PreToolUse: Read|Edit|Write|Grep|NotebookEdit — force-read the CONTEXT.md chain of the
# target's subtree before any other file access. Session-deduped via marker file
# (/tmp/claude_ctx_seen_<session_id>.txt, written by context-tracker.py). See code/ROADMAP-verify.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
from chain import EXEMPT_NAMES, SKIP_PARTS, context_chain
from hook_input import is_subagent, load_seen, parse_stdin
from platform_law import WORKSPACE_ROOT  # noqa: E402

GATED_TOOLS = {'Read', 'Edit', 'Write', 'Grep', 'NotebookEdit'}


def target_path(tool: str, tool_input: dict) -> str:
	if tool == 'NotebookEdit':
		return str(tool_input.get('notebook_path', ''))
	if tool == 'Grep':
		return str(tool_input.get('path', ''))
	return str(tool_input.get('file_path', ''))


def main() -> int:
	# context-chain is TWO files — this one and bash-context-gate.py, which closes the
	# cat/grep bypass. Both consult the law, or switching the feature off would leave half
	# the gate standing and an ablation would measure a cost nobody removed.
	if not feature_law.is_enabled('context-chain'):
		return 0
	raw, tool, tool_input, session_id, _ = parse_stdin()
	if tool not in GATED_TOOLS:
		return 0
	if is_subagent(raw):
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
	if not target.is_relative_to(WORKSPACE_ROOT):
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
