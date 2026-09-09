#!/usr/bin/env python3
# The map of where every project lives, redrawn at session close into PROJECTS.md.
#
# Only what is the same on every clone. The ROW SET comes from .gitignore, which is tracked, and
# never from the disk: a table describing what happens to be checked out here is a fact about one
# machine, which is what ISSUES.md ruled against on 2026-09-04 after the same commit read green on
# one disk and red on the other. The disk fills CELLS and blanks none — two machines share this
# workspace and neither has every project cloned, so a generator that wrote only what it can see
# would delete the other machine's answer at every close.
import json
from pathlib import Path

import artifacts
from artifacts import git, out

MAP = 'PROJECTS.md'
HEAD = ('| Path | Remote | Drive |', '|------|--------|-------|')


def declared(root: Path) -> set:
    """Project paths as .gitignore declares them — the key column's independent source.

    A project line names a directory with no glob and no trailing slash. The trailing slash
    separates a project from an ignored working directory (`outputs/`, `tmp/`), the glob from a
    subtree rule (`academy/*`).
    """
    lines = (root / '.gitignore').read_text(encoding='utf-8').splitlines()
    return {line.strip() for line in lines
            if '/' in line and not line.startswith(('#', '!', '.', '$'))
            and '*' not in line and not line.rstrip().endswith('/')}


def link(url: str) -> str:
    """A remote as a link named by its host, which is the only thing about it worth reading."""
    clean = url.removesuffix('.git').replace('https://git@', 'https://')
    return f'[{"Overleaf" if "overleaf" in clean else "github"}]({clean})'


def home(folder: Path) -> str:
    """What a folder's drive_sync.json declares, or nothing. Never guessed from a folder name."""
    try:
        found = json.loads((folder / 'drive_sync.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return ''
    return (f'[sync `{found.get("account", "")}`]'
            f'(https://drive.google.com/drive/folders/{found["folder_id"]})'
            if found.get('folder_id') else '')


def known(text: str) -> dict:
    """Path → [remote, drive], read back out of the block already written, so a cell survives.

    PROJECTS.md says an address written from memory is worse than an empty cell, because the
    empty one asks. An address ERASED because one machine lacks the clone is worse than either.
    """
    start, end = artifacts.markers('projects')
    rows = {}
    for line in text.partition(start)[2].partition(end)[0].splitlines():
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if len(cells) == 3 and cells[0].startswith('`'):
            rows[cells[0].strip('`')] = [cells[1], cells[2]]
    return rows


def redraw(root: Path, leave_dirty: bool) -> str:
    """Rewrite the map and settle it. Silent when nothing moved, which is the common case."""
    from platform_law import posix
    from entropy_corpus import nested_repos
    target = root / MAP
    if not target.is_file():   # a repo declaring no map is not a repo that wants one invented
        return ''
    was_clean = git(root, 'diff', '--quiet', MAP).returncode == 0
    seen = known(target.read_text(encoding='utf-8'))
    rows = {name: seen.get(name, ['—', '—']) for name in declared(root)}
    for repo in nested_repos(root):
        name = posix(repo.relative_to(root))
        if name in rows and out(repo, 'remote', 'get-url', 'origin'):
            rows[name][0] = link(out(repo, 'remote', 'get-url', 'origin'))
    for folder in sorted(root.glob('*/*/drive_sync.json')) + sorted(
            root.glob('*/*/*/drive_sync.json')):
        name = posix(folder.parent.relative_to(root))
        if name in rows and home(folder.parent):
            rows[name][1] = home(folder.parent)
    artifacts.write_block(target, 'projects', '\n'.join(
        (*HEAD, *(f'| `{name}` | {cells[0]} | {cells[1]} |' for name, cells in sorted(rows.items())))))
    if git(root, 'diff', '--quiet', MAP).returncode == 0:
        return ''
    return f'{MAP} redrawn' + artifacts.settle(
        root, MAP, was_clean, 'chore(projects): redraw the map at session close', leave_dirty)
