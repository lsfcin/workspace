# Workspace metadata extraction: file descriptions, public APIs, and interface links.
import re, ast
from pathlib import Path

CODE_EXTS    = {'.js', '.ts', '.tsx', '.py', '.dart', '.html', '.css', '.scss'}
CONTENT_EXTS = {'.md', '.yaml', '.yml', '.tex', '.toml'}
ALL_EXTS     = CODE_EXTS | CONTENT_EXTS
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
    """Read 'description:' from YAML frontmatter (files that start with ---).
    Handles inline values and block scalars (> and |)."""
    try:
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    except OSError:
        return ''
    if not lines or lines[0].strip() != '---':
        return ''
    block_mode = False
    block_lines: list = []
    for line in lines[1:30]:
        if line.strip() in ('---', '...'):
            break
        if block_mode:
            if line.startswith((' ', '\t')):
                block_lines.append(line.strip())
            else:
                break
        else:
            m = re.match(r'^description:\s*(.+?)\s*$', line)
            if m:
                val = m.group(1).strip().strip('"\'')
                if val in ('>', '|', '>-', '|-'):
                    block_mode = True
                else:
                    return val
    if block_lines:
        return ' '.join(block_lines)
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
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        # A shebang is a comment to the regex but not a description — every executable
        # module was advertising its interpreter path in the routing table. Take the
        # real first-line comment, which the pre-edit gate already requires below it.
        if lines and lines[0].startswith('#!'):
            lines = lines[1:]
        first = lines[0]
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
