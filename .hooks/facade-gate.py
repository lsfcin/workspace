#!/usr/bin/env python3
# PreToolUse: Edit|Write — block code/ module edits until the module's facade has been read.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hook_input import parse_stdin

WORKSPACE    = Path('/mnt/workspace')
FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}
CODE_EXTS    = {'.ts', '.tsx', '.js', '.jsx', '.py', '.dart'}
TEST_RE      = re.compile(r'(?:^|/)(?:test_[^/]+|[^/]+_test|[^/]+\.(?:test|spec))\.[^/]+$')


def facades_read(session_id: str) -> set[str]:
	sf = Path(f'/tmp/claude_facades_{session_id}.txt')
	return set(sf.read_text().splitlines()) if sf.exists() else set()


def find_nearest_facade(path: Path) -> Path | None:
	code_idx = next((i for i, p in enumerate(path.parts) if p == 'code'), None)
	if code_idx is None:
		return None
	project_root = Path(*path.parts[:code_idx + 2])
	current = path.parent
	while True:
		for name in FACADE_NAMES:
			candidate = current / name
			if candidate.exists():
				return candidate
		if current == project_root or current == current.parent:
			break
		current = current.parent
	return None


def main() -> int:
	_, tool, tool_input, session_id, _ = parse_stdin()
	if tool not in ('Edit', 'Write'):
		return 0
	file_path = Path(str(tool_input.get('file_path', '')))
	if 'code' not in file_path.parts:
		return 0
	if file_path.suffix not in CODE_EXTS:
		return 0
	if file_path.name in FACADE_NAMES:
		return 0
	if TEST_RE.search(str(file_path)):
		return 0

	facade = find_nearest_facade(file_path)
	if not facade or str(facade) in facades_read(session_id):
		return 0

	try:
		rel_f = facade.relative_to(WORKSPACE)
		rel_p = file_path.relative_to(WORKSPACE)
	except ValueError:
		rel_f, rel_p = facade, file_path
	print(f"⛔ READ FACADE FIRST — {rel_p}", file=sys.stderr)
	print(f"   Read {rel_f} before editing this module.", file=sys.stderr)
	print(f"   Source reads then auto-redirect to .d.ts/.pyi via pre-read.sh.", file=sys.stderr)
	return 2


sys.exit(main())
