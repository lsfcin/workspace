#!/usr/bin/env python3
# Sync the Routing block in CONTEXT.md (or AGENTS.md at workspace root).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from workspace_meta import CODE_EXTS
from workspace_scanner import (
    SPLIT_THRESHOLD,
    code_files, has_code_content, subdir_scan,
    parse_preserved_files, parse_preserved_subs,
    build_sub_rows, build_file_rows, build_routing_block,
)

RS  = '<!-- routing:start -->'
RE  = '<!-- routing:end -->'

# Legacy sentinel names — detected and converted automatically on first sync.
_OLD_AS = '<!-- ctx-sync:auto:start -->'
_OLD_AE = '<!-- ctx-sync:auto:end -->'
_OLD_SS = '<!-- ctx-sync:sub:start -->'
_OLD_SE = '<!-- ctx-sync:sub:end -->'
_OLD_RS = '<!-- ctx-sync:routing:start -->'
_OLD_RE = '<!-- ctx-sync:routing:end -->'


def _line_pos(text: str, sentinel: str) -> int:
    """Return position of sentinel only when it appears on its own line, else -1."""
    # Match at start of file or after a newline, followed by newline or end.
    for prefix in ('\n', ''):
        idx = text.find(prefix + sentinel)
        if idx == -1:
            continue
        pos = idx + len(prefix)
        after = pos + len(sentinel)
        if after >= len(text) or text[after] in ('\n', '\r'):
            return pos
    return -1


def _extract_between_lines(text: str, start: str, end: str) -> str:
    si = _line_pos(text, start)
    if si == -1:
        return ''
    content_start = si + len(start)
    ei = text.find(end, content_start)
    return text[content_start:ei].strip() if ei != -1 else ''


def migrate_legacy(text: str) -> tuple[str, bool]:
    """Convert old sentinel formats to current routing block (line-anchored only)."""
    # Migration: ctx-sync:routing:* → routing:*
    if _line_pos(text, _OLD_RS) != -1:
        text = text.replace(_OLD_RS, RS).replace(_OLD_RE, RE)
        return text, True

    has_auto = _line_pos(text, _OLD_AS) != -1
    has_sub  = _line_pos(text, _OLD_SS) != -1
    if not has_auto and not has_sub:
        return text, False

    sub_inner  = _extract_between_lines(text, _OLD_SS, _OLD_SE)
    auto_inner = _extract_between_lines(text, _OLD_AS, _OLD_AE)

    # Locate the full extent: from earliest sentinel to end of last sentinel.
    candidates = [p for p in (_line_pos(text, _OLD_AS), _line_pos(text, _OLD_SS)) if p != -1]
    end_sentinels = [s for s in (_OLD_AE, _OLD_SE) if _line_pos(text, s) != -1]
    ends = [_line_pos(text, s) + len(s) for s in end_sentinels]
    first, last_end = min(candidates), max(ends)

    # Walk back to absorb any preceding section heading.
    prefix = text[:first]
    section_start = first
    for h in ('## File Map', '## Sub-modules', '## Routing'):
        idx = prefix.rfind(h)
        if idx != -1 and prefix[idx:].count('\n') <= 5:
            section_start = min(section_start, idx)

    end = last_end
    while end < len(text) and text[end] == '\n':
        end += 1

    new_block = build_routing_block(sub_inner, auto_inner, RS, RE)
    return text[:section_start] + new_block + '\n' + text[end:], True


def sync(target: Path):
    directory = target if target.is_dir() else target.parent

    ctx = directory / 'CONTEXT.md'
    workspace_mode = False
    if not ctx.exists():
        w = directory / 'AGENTS.md'
        if w.exists():
            ctx = w
            workspace_mode = True
        else:
            return

    text = ctx.read_text(encoding='utf-8')

    # Self-heal: migrate legacy sentinel format if present.
    text, migrated = migrate_legacy(text)
    if migrated:
        ctx.write_text(text, encoding='utf-8')
        print(f'  migrated legacy format: {ctx}')

    # Extract preserved descriptions first (workspace_mode uses them for link_list).
    si = _line_pos(text, RS)
    ei = _line_pos(text, RE)
    inner           = text[si + len(RS): ei] if si != -1 and ei != -1 else ''
    preserved_files = parse_preserved_files(inner)
    preserved_subs  = parse_preserved_subs(inner)

    # Scan directory.
    if workspace_mode:
        # Workspace root: include only subdirs with CONTEXT.md or preserved descriptions.
        # This excludes OS system dirs ($RECYCLE.BIN etc.) not in the curated list.
        all_files = []
        all_subdirs = sorted(p for p in directory.iterdir()
                             if p.is_dir() and not p.name.startswith('.'))
        link_list = [s for s in all_subdirs
                     if (s / 'CONTEXT.md').exists() or s.name in preserved_subs]
    else:
        direct_files = [(f, f.name) for f in code_files(directory)]
        fold_list, link_list = subdir_scan(directory, RS, RE)
        all_files = direct_files + fold_list

    # Build new block.
    sub_content  = build_sub_rows(link_list, preserved_subs)  if link_list  else ''
    file_content = build_file_rows(all_files, preserved_files, directory) if all_files else ''
    new_block    = build_routing_block(sub_content, file_content, RS, RE)

    if si != -1 and ei != -1:
        # Remove block from current position; re-append at end (standardized position).
        before = text[:si].rstrip('\n')
        after  = text[ei + len(RE):].lstrip('\n')
        parts  = [p for p in (before, after) if p]
        text   = '\n\n'.join(parts)
    text = text.rstrip('\n') + '\n\n' + new_block

    ctx.write_text(text, encoding='utf-8')
    print(f'✓ routing-sync: {ctx}')

    removed = set(preserved_files) - {rel for _, rel in all_files}
    for r in removed:
        print(f'  removed stale entry: {r}')

    if not workspace_mode:
        code_count = sum(1 for f, _ in direct_files if f.suffix in CODE_EXTS)
        if code_count > SPLIT_THRESHOLD:
            print(f'⚠  {directory}: {code_count} code files — consider splitting')


if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    sync(target)
