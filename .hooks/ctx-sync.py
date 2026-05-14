#!/usr/bin/env python3
# Sync the auto File Map block in nearest CONTEXT.md with actual directory contents.
import sys, re, ast
from pathlib import Path

CODE_EXTS = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
SPLIT_THRESHOLD = 7
START       = '<!-- ctx-sync:auto:start -->'
END         = '<!-- ctx-sync:auto:end -->'
PLACEHOLDER = '← add first-line comment'

COMMENT_RE = {
    '.py':   [r'^#\s*(.+)', r'^"""(.+?)"""', r"^'''(.+?)'''"],
    '.js':   [r'^//\s*(.+)'],  '.ts':  [r'^//\s*(.+)'],  '.tsx': [r'^//\s*(.+)'],
    '.css':  [r'^/\*\s*(.+?)\s*\*/'],  '.scss': [r'^/\*\s*(.+?)\s*\*/'],
    '.html': [r'^<!--\s*(.+?)\s*-->'], '.dart': [r'^//\s*(.+)'],
}

# ── Extraction ────────────────────────────────────────────────────────────────

def file_description(path: Path) -> str:
    patterns = COMMENT_RE.get(path.suffix, [])
    try:
        first = path.read_text(encoding='utf-8', errors='ignore').splitlines()[0]
    except (IndexError, OSError):
        return ''
    for pat in patterns:
        m = re.match(pat, first.strip())
        if m:
            return m.group(1).strip()
    return ''

def python_api(path: Path) -> list:
    try:
        tree = ast.parse(path.read_text(encoding='utf-8', errors='ignore'))
    except SyntaxError:
        return []
    return [n.name for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not n.name.startswith('_')][:5]

def js_api(path: Path) -> list:
    text = path.read_text(encoding='utf-8', errors='ignore')
    pats = [r'export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)',
            r'export\s+const\s+(\w+)',
            r'^(?:async\s+)?function\s+(\w+)']
    names, seen = [], set()
    for pat in pats:
        for n in re.findall(pat, text, re.MULTILINE):
            if n not in seen:
                seen.add(n); names.append(n)
    return names[:5]

def extract_api(path: Path) -> str:
    if path.suffix == '.py':
        api = python_api(path)
    elif path.suffix in {'.js', '.ts', '.tsx'}:
        api = js_api(path)
    else:
        return '—'
    return ', '.join(f'`{n}`' for n in api) if api else '—'

# ── CONTEXT.md sync ───────────────────────────────────────────────────────────

def interface_for(src: Path) -> str:
    for iext in ('.pyi', '.d.ts'):
        c = src.with_suffix(iext)
        if c.exists():
            return f'[`{c.name}`]({c.name})'
    return '—'

def code_files(directory: Path) -> list:
    return sorted(p for p in directory.iterdir()
                  if p.is_file()
                  and p.suffix in CODE_EXTS
                  and not p.name.endswith('.d.ts')
                  and not p.name.endswith('.pyi'))

def parse_preserved(inner: str) -> dict:
    rows = {}
    for line in inner.splitlines():
        m = re.match(r'\|\s*\[?`([^`]+)`\]?[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|', line)
        if m:
            fname, desc = m.group(1), m.group(2).strip()
            if desc not in ('Description', '—', '', PLACEHOLDER):
                rows[fname] = desc
    return rows

def build_rows(files: list, preserved: dict) -> str:
    lines = ['| File | Interface | API | Description |',
             '|------|-----------|-----|-------------|']
    for f in files:
        desc  = file_description(f) or preserved.get(f.name, PLACEHOLDER)
        iface = interface_for(f)
        api   = extract_api(f)
        lines.append(f'| [`{f.name}`]({f.name}) | {iface} | {api} | {desc} |')
    return '\n'.join(lines) + '\n'

def sync(target: Path):
    directory = target if target.is_dir() else target.parent
    ctx = directory / 'CONTEXT.md'
    if not ctx.exists():
        return

    text = ctx.read_text(encoding='utf-8')
    si, ei = text.find(START), text.find(END)
    if si == -1:
        text += f'\n## File Map\n{START}\n{END}\n'
        si, ei = text.find(START), text.find(END)

    inner     = text[si + len(START): ei]
    preserved = parse_preserved(inner)
    files     = code_files(directory)
    block     = '\n' + build_rows(files, preserved)

    ctx.write_text(text[:si + len(START)] + block + text[ei:], encoding='utf-8')
    print(f'✓ ctx-sync: {ctx}')

    removed = set(preserved) - {f.name for f in files}
    for r in removed:
        print(f'  removed stale entry: {r}')

    if len(files) > SPLIT_THRESHOLD:
        print(f'⚠  {directory}: {len(files)} files — consider a sub-CONTEXT.md')

if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    sync(target)
