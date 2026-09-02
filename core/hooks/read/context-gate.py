#!/usr/bin/env python3
# PreToolUse: Read|Edit|Write|Grep|NotebookEdit — force-read the CONTEXT.md chain of the
# target's subtree before any other file access. Session-deduped via marker file
# (/tmp/claude_ctx_seen_<session_id>.txt, written by context-tracker.py). See code/ROADMAP-verify.md W1.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
from chain import EXEMPT_NAMES, SKIP_PARTS, prerequisites
from hook_input import is_subagent, load_iface_seen, load_seen, parse_stdin
from platform_law import WORKSPACE_ROOT  # noqa: E402

GATED_TOOLS = {'Read', 'Edit', 'Write', 'Grep', 'NotebookEdit'}


def target_path(tool: str, tool_input: dict) -> str:
	if tool == 'NotebookEdit':
		return str(tool_input.get('notebook_path', ''))
	if tool == 'Grep':
		return str(tool_input.get('path', ''))
	return str(tool_input.get('file_path', ''))


def missing_chain(session_id: str, raw: str) -> int:
	"""`--missing-chain <session> <path>`: print the CONTEXT.md files that path still needs.

	A QUERY, not a hook run, and read/pre-read.sh is the caller — the other gate on the same Read,
	which is shell and cannot import chain.py. It asks only on the branch that is about to block,
	so the subprocess is not on the per-Read path, and what it buys is the round trip the agent
	would otherwise spend discovering this list one gate at a time.
	"""
	try:
		target = Path(raw).resolve()
	except OSError:
		return 0
	if not target.is_relative_to(WORKSPACE_ROOT):
		return 0
	for ctx in prerequisites(target, load_seen(session_id), set(), gate_interface=False):
		print(ctx)
	return 0


def main() -> int:
	if len(sys.argv) == 4 and sys.argv[1] == '--missing-chain':
		return missing_chain(sys.argv[2], sys.argv[3])
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

	# The stub is a prerequisite of a READ and of nothing else: read/pre-read.sh matches Read alone,
	# so demanding one before an Edit would invent a rule no gate enforces. And the law is asked
	# here rather than inside chain.py, so that module stays the definition and never the registry.
	gate_interface = tool == 'Read' and feature_law.is_enabled('interface-first-reads')
	seen = load_seen(session_id)
	needed = prerequisites(target, seen, load_iface_seen(session_id), gate_interface)
	if not needed:
		return 0

	print('CONTEXT GATE - subtree context not yet loaded this session.', file=sys.stderr)
	print('Read these first, in ONE parallel batch, then retry:', file=sys.stderr)
	for path in needed:
		note = '' if path.name in EXEMPT_NAMES else '   <- interface; reading it unlocks the source'
		print(f'   {path}{note}', file=sys.stderr)
	return 2


sys.exit(main())
