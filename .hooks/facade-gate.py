#!/usr/bin/env python3
# PreToolUse: Edit|Write — block Code/ module edits until the module's facade has been read.
import json, os, re, subprocess, sys
from pathlib import Path

WORKSPACE    = Path('/mnt/workspace')
FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}
CODE_EXTS    = {'.ts', '.tsx', '.js', '.jsx', '.py', '.dart'}
TEST_RE      = re.compile(r'(?:^|/)(?:test_[^/]+|[^/]+_test|[^/]+\.(?:test|spec))\.[^/]+$')


def get_session_id() -> str:
    shell_pid = os.getppid()
    try:
        result = subprocess.check_output(
            ['ps', '-o', 'ppid=', '-p', str(shell_pid)],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        return result if result.isdigit() else str(shell_pid)
    except Exception:
        return str(shell_pid)


def facades_read() -> set[str]:
    sf = Path(f'/tmp/claude_facades_{get_session_id()}.txt')
    return set(sf.read_text().splitlines()) if sf.exists() else set()


def find_nearest_facade(path: Path) -> Path | None:
    code_idx = next((i for i, p in enumerate(path.parts) if p == 'Code'), None)
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


data      = json.load(sys.stdin)
tool      = os.environ.get('CLAUDE_TOOL_NAME', '')
file_path = Path(data.get('file_path', ''))

if tool not in ('Edit', 'Write'):
    sys.exit(0)
if 'Code' not in file_path.parts:
    sys.exit(0)
if file_path.suffix not in CODE_EXTS:
    sys.exit(0)
if file_path.name in FACADE_NAMES:
    sys.exit(0)
if TEST_RE.search(str(file_path)):
    sys.exit(0)

facade = find_nearest_facade(file_path)
if not facade or str(facade) in facades_read():
    sys.exit(0)

try:
    rel_f = facade.relative_to(WORKSPACE)
    rel_p = file_path.relative_to(WORKSPACE)
except ValueError:
    rel_f, rel_p = facade, file_path

print(f"⛔ READ FACADE FIRST — {rel_p}")
print(f"   Read {rel_f} before editing this module.")
print(f"   Source reads then auto-redirect to .d.ts/.pyi via pre-read.sh.")
sys.exit(2)
