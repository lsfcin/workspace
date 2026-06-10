# Workspace scanner: extracts file metadata and builds routing tables from directory contents.
import re, ast
from pathlib import Path

CODE_EXTS    = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
CONTENT_EXTS = {'.md', '.yaml', '.yml', '.tex', '.toml'}
ALL_EXTS     = CODE_EXTS | CONTENT_EXTS
SPLIT_THRESHOLD = 7
PLACEHOLDER  = '← add first-line comment'

COMMENT_RE = {
    '.py':  [r'^#\s*(.+)', r'^"""(.+?)"""', r"^'''(.+?)'''"],
    '.js':  [r'^//\s*(.+)'], '.ts':   [r'^//\s*(.+)'], '.tsx':  [r'^//\s*(.+)'],
    '.css': [r'^/\*\s*(.+?)\s*\*/'],  '.scss': [r'^/\*\s*(.+?)\s*\*/'],
    '.html':[r'^<!--\s*(.+?)\s*-->'], '.dart': [r'^//\s*(.+)'],
    '.md':  [r'^#\s*(.+)'], '.yaml': [r'^#\s*(.+)'], '.yml':  [r'^#\s*(.+)'],
    '.tex': [r'^%\s*(.+)'], '.toml': [r'^#\s*(.+)'],
}

def _exec_description(path: Path) -> str:
    """Extract description from an extensionless executable (shebang file).
    Skips the shebang, finds the first # comment line, returns the part after ' — '."""
    try:
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    except OSError:
        return ''
    for line in lines[:6]:
        if line.startswith('#!'):
            continue
        m = re.match(r'^#\s*(.+)', line)
        if m:
            text = m.group(1).strip()
            if ' — ' in text:
                return text.split(' — ', 1)[1].strip()
            return text
    return ''

def _frontmatter_description(path: Path) -> str:
    """Read 'description:' from YAML frontmatter (files that start with ---)."""
    try:
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    except OSError:
        return ''
    if not lines or lines[0].strip() != '---':
        return ''
    for line in lines[1:20]:
        if line.strip() in ('---', '...'):
            break
        m = re.match(r'^description:\s*["\']?(.+?)["\']?\s*$', line)
        if m:
            return m.group(1).strip()
    return ''

def file_description(path: Path) -> str:
    if not path.suffix:
        return _exec_description(path)
    if path.suffix == '.md':
        fm = _frontmatter_description(path)
        if fm:
            return fm
    patterns = COMMENT_RE.get(path.suffix, [])
    try:
        first = path.read_text(encoding='utf-8', errors='ignore').splitlines()[0]
    except (IndexError, OSError):
        return ''
    for pat in patterns:
        m = re.match(pat, first.strip())
        if m: return m.group(1).strip()
    return ''

def python_api(path: Path) -> list:
    try: tree = ast.parse(path.read_text(encoding='utf-8', errors='ignore'))
    except SyntaxError: return []
    return [n.name for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not n.name.startswith('_')][:5]

def js_api(path: Path) -> list:
    text = path.read_text(encoding='utf-8', errors='ignore')
    pats = [r'export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)',
            r'export\s+const\s+(\w+)', r'^(?:async\s+)?function\s+(\w+)']
    names, seen = [], set()
    for pat in pats:
        for n in re.findall(pat, text, re.MULTILINE):
            if n not in seen: seen.add(n); names.append(n)
    return names[:5]

def extract_api(path: Path) -> str:
    if path.suffix == '.py': api = python_api(path)
    elif path.suffix in {'.js', '.ts', '.tsx'}: api = js_api(path)
    else: return '—'
    return ', '.join(f'`{n}`' for n in api) if api else '—'

def interface_for(src: Path, ctx_dir: Path) -> str:
    if src.suffix == '.py':                     c = src.with_suffix('.pyi')
    elif src.suffix in {'.js', '.ts', '.tsx'}:  c = src.with_suffix('.d.ts')
    elif src.suffix == '.dart':                  c = src.parent / (src.stem + '.dart.api')
    elif src.suffix == '.tex':                   c = src.with_suffix('.texif')
    else: return '—'
    return f'[`{c.relative_to(ctx_dir)}`]({c.relative_to(ctx_dir)})' if c.exists() else '—'

def _is_exec_script(path: Path) -> bool:
    """True for extensionless files that start with a shebang."""
    if path.suffix or not path.is_file():
        return False
    try:
        return path.open('rb').read(2) == b'#!'
    except OSError:
        return False

def code_files(directory: Path) -> list:
    return sorted(p for p in directory.iterdir()
                  if p.is_file()
                  and p.name not in ('CONTEXT.md', 'WORKSPACE.md')
                  and not p.name.endswith(('.d.ts', '.pyi'))
                  and (p.suffix in ALL_EXTS or _is_exec_script(p)))

def has_code_content(directory: Path) -> bool:
    if code_files(directory): return True
    return any(has_code_content(p) for p in directory.iterdir()
               if p.is_dir() and not p.name.startswith('.') and p.name not in _SKIP_DIRS)

_SKIP_DIRS   = {'node_modules', '__pycache__', '.git', 'dist', 'build', '.venv', 'venv'}
FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}

def subdir_scan(directory: Path, rs: str, re_end: str) -> tuple:
    fold_list, link_list = [], []
    for sub in sorted(p for p in directory.iterdir()
                      if p.is_dir() and not p.name.startswith('.')
                      and p.name not in _SKIP_DIRS):
        has_ctx = (sub / 'CONTEXT.md').exists()
        if not has_code_content(sub) and not has_ctx: continue
        files = code_files(sub)
        is_branch = any(has_code_content(p) for p in sub.iterdir()
                        if p.is_dir() and not p.name.startswith('.'))
        if has_ctx or len(files) >= SPLIT_THRESHOLD or is_branch:
            if not has_ctx:
                scaffold = sub / 'CONTEXT.md'
                scaffold.write_text(
                    f'# {sub.name}\n> ← add description\n\n{rs}\n## Routing\n\n{re_end}\n',
                    encoding='utf-8')
                print(f'  created scaffold: {scaffold}')
            link_list.append(sub)
        else:
            for f in files: fold_list.append((f, f'{sub.name}/{f.name}'))
    return fold_list, link_list

def parse_preserved_files(inner: str) -> dict:
    rows = {}
    for line in inner.splitlines():
        m = re.match(r'\|\s*\[?`([^`]+)`\]?[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|', line)
        if m:
            fname, desc = m.group(1), m.group(2).strip()
            if desc not in ('Description', '—', '', PLACEHOLDER): rows[fname] = desc
    return rows

def parse_preserved_subs(inner: str) -> dict:
    rows = {}
    for line in inner.splitlines():
        m = re.match(r'\|\s*\[`([^/`]+)/`\][^|]*\|\s*([^|]+?)\s*\|', line)
        if m:
            name, desc = m.group(1), m.group(2).strip()
            if desc not in ('Description', '—', '', '← add description'): rows[name] = desc
    return rows

def build_sub_rows(link_list: list, preserved_subs: dict) -> str:
    rows = ['| Subdirectory | Description |', '|--------------|-------------|']
    for sub in link_list:
        ctx_sub = sub / 'CONTEXT.md'
        desc = preserved_subs.get(sub.name, '—')
        if ctx_sub.exists():
            lines = ctx_sub.read_text().splitlines()
            if len(lines) > 1:
                m = re.match(r'^>\s*(.+)', lines[1].strip())
                if m:
                    candidate = m.group(1).strip()[:80]
                    if candidate != '← add description':
                        desc = candidate
        link = f'{sub.name}/CONTEXT.md' if ctx_sub.exists() else f'{sub.name}/'
        rows.append(f'| [`{sub.name}/`]({link}) | {desc} |')
    return '\n'.join(rows)

def build_file_rows(files_with_rel: list, preserved: dict, ctx_dir: Path) -> str:
    lines = ['| File | Interface | API | Description |', '|------|-----------|-----|-------------|']
    for f, rel in sorted(files_with_rel, key=lambda x: (x[0].name not in FACADE_NAMES, x[1])):
        pre  = '**facade** — ' if f.name in FACADE_NAMES else ''
        desc = pre + (file_description(f) or preserved.get(rel, preserved.get(f.name, PLACEHOLDER)))
        lines.append(f'| [`{rel}`]({rel}) | {interface_for(f, ctx_dir)} | {extract_api(f)} | {desc} |')
    return '\n'.join(lines)

def build_routing_block(sub_content: str, file_content: str, rs: str, re_end: str) -> str:
    parts = [rs, '## Routing', '']
    if sub_content:
        parts.append(sub_content)
        if file_content: parts.append('')
    if file_content: parts.append(file_content)
    parts.append(re_end)
    return '\n'.join(parts) + '\n'
