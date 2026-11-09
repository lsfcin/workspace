# T1 the projects map (PROJECTS.md): what a redraw fills in, never erases, and when it may commit.
#
# Two machines share this workspace and neither has every project checked out. Which ROWS exist is
# therefore read from .gitignore, which is tracked, and never from the disk — a table describing
# what happens to be cloned here is a fact about one machine, which ISSUES.md ruled against on
# 2026-09-04 after the same commit read green on one disk and red on the other. The disk fills
# CELLS, and the one law with teeth is the negative one: a cell this clone cannot confirm is kept
# exactly as written, because erasing the other machine's answer is worse than leaving it.
import subprocess
import sys

import pytest

from conftest import WORKSPACE_ROOT

IGNORED = 'code/here\ncode/elsewhere\noutputs/\n'

SEED = """# Projects

<!-- projects:start -->
| Path | Remote | Drive |
|------|--------|-------|
| `code/elsewhere` | [github](https://github.com/lsfcin/elsewhere) | — |
<!-- projects:end -->
"""


@pytest.fixture
def repomap():
    for directory in ('core/tools/wos/close', 'core/hooks', 'core/hooks/entropy'):
        sys.path.insert(0, str(WORKSPACE_ROOT / directory))
    import repomap as module
    return module


def _workspace(tmp_path):
    """A throwaway workspace: one project cloned here, one declared and cloned on the other machine."""
    root, project = tmp_path / 'ws', tmp_path / 'ws/code/here'
    project.mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', 'init', '-q', str(project)], check=True)
    subprocess.run(['git', '-C', str(project), 'remote', 'add', 'origin',
                    'https://github.com/lsfcin/here.git'], check=True)
    (root / '.gitignore').write_text(IGNORED, encoding='utf-8', newline='\n')
    (root / 'PROJECTS.md').write_text(SEED, encoding='utf-8', newline='\n')
    return root


def _table(root) -> str:
    return (root / 'PROJECTS.md').read_text(encoding='utf-8')


def test_a_row_this_clone_cannot_confirm_survives_the_redraw(tmp_path, repomap) -> None:
    root = _workspace(tmp_path)

    repomap.redraw(root)

    assert '`code/elsewhere` | [github](https://github.com/lsfcin/elsewhere)' in _table(root), (
        'the redraw erased a project checked out on the other machine')


def test_a_cloned_project_gets_its_remote_and_its_drive_home(tmp_path, repomap) -> None:
    """Read off the disk, never guessed: the remote from git, the Drive home from its own file."""
    root = _workspace(tmp_path)
    (root / 'code/here/drive_sync.json').write_text(
        '{"folder_id": "FOLDER", "account": "personal"}', encoding='utf-8', newline='\n')

    repomap.redraw(root)
    written = _table(root)

    assert '`code/here` | [github](https://github.com/lsfcin/here)' in written, written
    assert 'sync `personal`](https://drive.google.com/drive/folders/FOLDER)' in written, written


def test_a_remote_s_credential_never_reaches_the_map(tmp_path, repomap) -> None:
    """An Overleaf remote carries its token as user:token@; the map is tracked and pushed."""
    root, userinfo = _workspace(tmp_path), 'git:' + 'olp_FAKE' + '@'   # split so secret_law passes
    subprocess.run(['git', '-C', str(root / 'code/here'), 'remote', 'set-url', 'origin',
                    f'https://{userinfo}git.overleaf.com/abc'], check=True)
    (root / 'PROJECTS.md').write_text(SEED.replace('https://github.com', f'https://{userinfo}github.com'),
                                      encoding='utf-8', newline='\n')

    repomap.redraw(root)

    assert 'olp_' not in _table(root), _table(root)
    assert '[Overleaf](https://git.overleaf.com/abc)' in _table(root), _table(root)


def test_a_folder_the_declaration_does_not_name_gets_no_row(tmp_path, repomap) -> None:
    """The trap this file exists for: a repo on this disk that no clone but this one has."""
    root = _workspace(tmp_path)
    subprocess.run(['git', 'init', '-q', str(root / 'code/undeclared')], check=True)

    repomap.redraw(root)

    assert 'code/undeclared' not in _table(root)


def _tracked(root):
    """The same workspace, with its map and its declaration committed, so `settle` is reached at
    all. Every case above leaves both untracked, where the redraw returns before settling."""
    for key, value in (('user.email', 't@e.com'), ('user.name', 't'), ('core.hooksPath', '/dev/null')):
        subprocess.run(['git', '-C', str(root), 'config', key, value], check=True)
    subprocess.run(['git', '-C', str(root), 'add', '.gitignore', 'PROJECTS.md'], check=True)
    subprocess.run(['git', '-C', str(root), 'commit', '-q', '--no-verify', '-m', 'seed'], check=True)


def _declare(root, text, commit):
    (root / '.gitignore').write_text(text, encoding='utf-8', newline='\n')
    if commit:
        subprocess.run(['git', '-C', str(root), 'add', '.gitignore'], check=True)
        subprocess.run(['git', '-C', str(root), 'commit', '-q', '--no-verify', '-m', 'declare'],
                       check=True)


def test_the_close_that_changes_the_project_set_may_still_draw_the_map(tmp_path, repomap) -> None:
    """b20260912 — the close that CHANGES the project set draws the map over someone else's dirt."""
    root = _workspace(tmp_path)
    _tracked(root)
    _declare(root, IGNORED + 'code/absorbed\n', commit=True)
    (root / 'unrelated.md').write_text('another session is working\n', encoding='utf-8', newline='\n')

    repomap.redraw(root)

    assert 'code/absorbed' in _table(root), 'the redraw lost its own change'


def test_a_second_redraw_changes_nothing(tmp_path, repomap) -> None:
    """A file that moves because a generator ran is a file nobody can read a diff of."""
    root = _workspace(tmp_path)
    repomap.redraw(root)
    once = _table(root)

    repomap.redraw(root)

    assert _table(root) == once
