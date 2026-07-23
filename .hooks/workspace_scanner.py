# Workspace scanner: directory discovery and CONTEXT.md routing-table assembly.
import re
from pathlib import Path

from workspace_meta import (
    ALL_EXTS, PLACEHOLDER, extract_api, file_description, interface_for,
)

SPLIT_THRESHOLD = 7
_SKIP_DIRS   = {'node_modules', '__pycache__', '.git', 'dist', 'build', '.venv', 'venv'}
FACADE_NAMES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}

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
                  and p.name not in ('CONTEXT.md', 'WORKSPACE.md', 'AGENTS.md')
                  and not p.name.endswith(('.d.ts', '.pyi'))
                  and (p.suffix in ALL_EXTS or _is_exec_script(p)))

def has_code_content(directory: Path) -> bool:
    if code_files(directory): return True
    return any(has_code_content(p) for p in directory.iterdir()
               if p.is_dir() and not p.name.startswith('.') and p.name not in _SKIP_DIRS)

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
