#!/usr/bin/env python3
# PreToolUse: Edit|Write on KNOWN-BUGS.md — flipping a bug to FIXED requires a matching
# regression spec (test/**/b<N>-*.*) in the same repo. See workspace VERIFY.md I2.
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import parse_stdin

FIXED_RE = re.compile(r'##\s*B(\d+)\b[^\n]*\bFIXED\b', re.IGNORECASE)


def fixed_ids(text: str) -> set[str]:
	return set(FIXED_RE.findall(text or ''))


def repo_root(path: Path) -> Path | None:
	try:
		out = subprocess.check_output(
			['git', '-C', str(path.parent), 'rev-parse', '--show-toplevel'],
			text=True, stderr=subprocess.DEVNULL).strip()
		return Path(out)
	except Exception:
		return None


def has_spec(root: Path, bug_id: str) -> bool:
	matches = list(root.glob(f'test/**/b{bug_id}-*.*'))
	return len(matches) > 0


def main() -> int:
	_, tool, tool_input, _, _ = parse_stdin()
	if tool not in ('Edit', 'Write'):
		return 0
	file_path = Path(str(tool_input.get('file_path', '')))
	if file_path.name != 'KNOWN-BUGS.md':
		return 0

	if tool == 'Write':
		new_text = str(tool_input.get('content', ''))
	else:
		new_text = str(tool_input.get('new_string', ''))
	old_text = str(tool_input.get('old_string', '')) if tool == 'Edit' else ''
	current = file_path.read_text() if file_path.exists() else ''

	newly_fixed = fixed_ids(new_text) - fixed_ids(old_text) - fixed_ids(current)
	if not newly_fixed:
		return 0

	root = repo_root(file_path)
	if root is None:
		return 0
	missing = sorted(b for b in newly_fixed if not has_spec(root, b))
	if not missing:
		return 0

	print('KNOWN-BUGS GATE - FIXED requires executable proof.', file=sys.stderr)
	for b in missing:
		print(f'   B{b}: no regression spec found (expected test/**/b{b}-*.*).', file=sys.stderr)
	print('   Write the regression spec first, verify it passes, then flip the status.', file=sys.stderr)
	return 2


sys.exit(main())
