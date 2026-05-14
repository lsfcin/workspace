#!/usr/bin/env python3
# Sync the auto File Map block in nearest CONTEXT.md with actual directory contents.
import sys, re, ast
from pathlib import Path

CODE_EXTS    = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
CONTENT_EXTS = {'.md', '.yaml', '.yml', '.tex', '.toml'}
ALL_EXTS     = CODE_EXTS | CONTENT_EXTS
SPLIT_THRESHOLD = 7
START     = '<!-- ctx-sync:auto:start -->'
END       = '<!-- ctx-sync:auto:end -->'
SUB_START = '<!-- ctx-sync:sub:start -->'
SUB_END   = '<!-- ctx-sync:sub:end -->'
PLACEHOLDER = '← add first-line comment'

COMMENT_RE = {
    '.py':   [r'^#\s*(.+)', r'^"""(.+?)"""', r"^'''(.+?)'''"],
    '.js':   [r'^//\s*(.+)'],  '.ts':  [r'^//\s*(.+)'],  '.tsx': [r'^//\s*(.+)'],
    '.css':  [r'^/\*\s*(.+?)\s*\*/'],  '.scss': [r'^/\*\s*(.+?)\s*\*/'],
    '.html': [r'^<!--\s*(.+?)\s*-->'], '.dart': [r'^//\s*(.+)'],
    '.md':   [r'^#\s*(.+)'],   '.yaml': [r'^#\s*(.+)'], '.yml':  [r'^#\s*(.+)'],
    '.tex':  [r'^%\s*(.+)'],   '.toml': [r'^#\s*(.+)'],
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

# ── Directory scanning ────────────────────────────────────────────────────────

def interface_for(src: Path, ctx_dir: Path) -> str:
    if src.suffix == '.py':            c = src.with_suffix('.pyi')
    elif src.suffix in {'.js', '.ts', '.tsx'}: c = src.with_suffix('.d.ts')
    elif src.suffix == '.dart':        c = src.parent / (src.stem + '.dart.api')
    else: return '—'
    return f'[`{c.relative_to(ctx_dir)}`]({c.relative_to(ctx_dir)})' if c.exists() else '—'

def code_files(directory: Path) -> list:
    return sorted(p for p in directory.iterdir()
                  if p.is_file() and p.suffix in ALL_EXTS
                  and p.name != 'CONTEXT.md'
                  and not p.name.endswith(('.d.ts', '.pyi')))

def has_code_content(directory: Path) -> bool:
    if code_files(directory):
        return True
    return any(has_code_content(p) for p in directory.iterdir()
               if p.is_dir() and not p.name.startswith('.'))

def subdir_scan(directory: Path) -> tuple:
    fold_list, link_list = [], []
    for sub in sorted(p for p in directory.iterdir()
                      if p.is_dir() and not p.name.startswith('.')):
        has_ctx = (sub / 'CONTEXT.md').exists()
        if not has_code_content(sub) and not has_ctx:
            continue
        files = code_files(sub)
        is_branch = any(has_code_content(p) for p in sub.iterdir()
                        if p.is_dir() and not p.name.startswith('.'))
        if has_ctx or len(files) >= SPLIT_THRESHOLD or is_branch:
            if not has_ctx:
                scaffold = sub / 'CONTEXT.md'
                scaffold.write_text(
                    f'# {sub.name}\n> ← add description\n\n## File Map\n{START}\n{END}\n',
                    encoding='utf-8')
                print(f'  created scaffold: {scaffold}')
            link_list.append(sub)
        else:
            for f in files:
                fold_list.append((f, f'{sub.name}/{f.name}'))
    return fold_list, link_list

# ── CONTEXT.md sync ───────────────────────────────────────────────────────────

def parse_preserved(inner: str) -> dict:
    rows = {}
    for line in inner.splitlines():
        m = re.match(r'\|\s*\[?`([^`]+)`\]?[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|', line)
        if m:
            fname, desc = m.group(1), m.group(2).strip()
            if desc not in ('Description', '—', '', PLACEHOLDER):
                rows[fname] = desc
    return rows

def build_rows(files_with_rel: list, preserved: dict, ctx_dir: Path) -> str:
    lines = ['| File | Interface | API | Description |',
             '|------|-----------|-----|-------------|']
    for f, rel in files_with_rel:
        desc  = file_description(f) or preserved.get(rel, preserved.get(f.name, PLACEHOLDER))
        iface = interface_for(f, ctx_dir)
        api   = extract_api(f)
        lines.append(f'| [`{rel}`]({rel}) | {iface} | {api} | {desc} |')
    return '\n'.join(lines) + '\n'

def sync_submodules(ctx: Path, link_list: list):
    text = ctx.read_text(encoding='utf-8')
    block_lines = ['| Subdirectory | Description |', '|--------------|-------------|']
    for sub in link_list:
        ctx_sub = sub / 'CONTEXT.md'
        desc = '—'
        if ctx_sub.exists():
            lines = ctx_sub.read_text().splitlines()
            if len(lines) > 1:
                m = re.match(r'^>\s*(.+)', lines[1].strip())
                if m:
                    desc = m.group(1).strip()[:80]
        block_lines.append(f'| [`{sub.name}/`]({sub.name}/CONTEXT.md) | {desc} |')
    new_block = '\n' + '\n'.join(block_lines) + '\n'
    if SUB_START in text:
        si, ei = text.find(SUB_START), text.find(SUB_END)
        text = text[:si + len(SUB_START)] + new_block + text[ei:]
    else:
        text += f'\n## Sub-modules\n{SUB_START}\n{new_block}{SUB_END}\n'
    ctx.write_text(text, encoding='utf-8')

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

    direct_files = [(f, f.name) for f in code_files(directory)]
    fold_list, link_list = subdir_scan(directory)
    all_files = direct_files + fold_list
    block = '\n' + build_rows(all_files, preserved, directory)

    ctx.write_text(text[:si + len(START)] + block + text[ei:], encoding='utf-8')
    print(f'✓ ctx-sync: {ctx}')

    if link_list:
        sync_submodules(ctx, link_list)
        for sub in link_list:
            print(f'  linked: {sub.name}/')

    removed = set(preserved) - {rel for _, rel in all_files}
    for r in removed:
        print(f'  removed stale entry: {r}')

    code_count = sum(1 for f, _ in direct_files if f.suffix in CODE_EXTS)
    if code_count > SPLIT_THRESHOLD:
        print(f'⚠  {directory}: {code_count} code files — consider splitting')

if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    sync(target)
