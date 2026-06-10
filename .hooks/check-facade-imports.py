#!/usr/bin/env python3
# Blocks cross-module imports that bypass facade files (index.ts / __init__.py).
import sys, re
from pathlib import Path

# Test files, facade files themselves, and generated dirs are exempt.
EXEMPT_RE = re.compile(
    r'(?:^|/)[^/]*\.(?:test|spec)\.[tj]sx?$'     # TS/JS: *.test.ts, *.spec.ts
    r'|(?:^|/)(?:test_[^/]*|[^/]*_test)\.py$'    # Python: test_*.py, *_test.py
    r'|(?:^|/)(?:__init__\.py|index\.[tj]sx?)$'  # facade files themselves
    r'|(?:^|/)(?:generated|vendor|node_modules)/',
    re.IGNORECASE,
)

# Matches: from '...', export ... from '...', require('...')  — relative paths only.
TS_FROM_RE = re.compile(r'''(?:from|require\s*\()\s*['"](\.[^'"]+)['"]''')
# Matches: from ..pkg.submod import  — relative Python imports descending into a submodule.
PY_REL_RE  = re.compile(r'^from\s+(\.+)(\S+)\s+import', re.MULTILINE)


def _has_facade(folder: Path) -> bool:
    """True if the folder already has a facade file — enforcement only applies then."""
    for name in ('index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py'):
        if (folder / name).exists():
            return True
    return False


def ts_violations(path: Path, src: str) -> list[str]:
    out = []
    for m in TS_FROM_RE.finditer(src):
        imp = m.group(1).rstrip('/')
        target = (path.parent / imp).resolve()
        if target.parent == path.parent.resolve():
            continue  # same folder — intra-module, always OK
        if target.is_dir() or target.stem == 'index':
            continue  # resolves to folder (index.ts) or explicit 'index' — OK
        if not _has_facade(target.parent):
            continue  # target folder has no facade yet — not enforced until one is added
        out.append(f"  {path}: '{imp}' bypasses facade → import from '{target.parent.name}/' instead")
    return out


def py_violations(path: Path, src: str) -> list[str]:
    out = []
    for m in PY_REL_RE.finditer(src):
        dots, mod = m.group(1), m.group(2)
        if '.' in mod:  # from ..pkg.submod import — descends past __init__
            pkg = mod.split('.')[0]
            levels = len(dots)
            target_folder = path.parent
            for _ in range(levels):
                target_folder = target_folder.parent
            target_folder = target_folder / pkg
            if not _has_facade(target_folder):
                continue  # target package has no __init__ with public API yet
            out.append(
                f"  {path}: 'from {dots}{mod}' bypasses facade → use 'from {dots}{pkg}' instead"
            )
    return out


def check(f: str) -> list[str]:
    path = Path(f).resolve()
    if not path.is_file() or EXEMPT_RE.search(f.replace('\\', '/')):
        return []
    try:
        src = path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []
    if path.suffix in {'.ts', '.tsx', '.js', '.jsx'}:
        return ts_violations(path, src)
    if path.suffix == '.py':
        return py_violations(path, src)
    return []


if __name__ == '__main__':
    files = sys.argv[1:] or [ln.strip() for ln in sys.stdin if ln.strip()]
    violations = [v for f in files for v in check(f)]
    if violations:
        print('⛔ Facade boundary violations — cross-module imports must go through index / __init__:\n')
        for v in violations:
            print(v)
        print('\n  Fix: import from the folder, not the file.')
        print('  Exempt: test files, index.ts, __init__.py, generated/ and vendor/ dirs.')
        print('  Override (temporary): git commit --no-verify\n')
        sys.exit(1)
