# T1 roundup tool (core/hooks/git/SPECS.md § Close): every repo this session holds goes back to develop.
# Zero-token, no network — each case builds a throwaway repo with a bare origin, held through the
# real lock, and runs the real script on it.
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from conftest import LOCK_URL, WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402


ROUNDUP = WORKSPACE_ROOT / 'core/tools/wos/roundup'


@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    key = re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve()))
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob(f'lock_*{key}*'):
        path.unlink(missing_ok=True)


def held(tmp_path, suite=''):
    """(repo, branch, session): a governed repo its own session holds, one change committed on it.
    One session per case: parallel cases sharing an id would close each other's repos."""
    session = f'test-roundup-{tmp_path.name}'
    repo = governed_repo(tmp_path)
    lock.take(repo, session, 'work')
    if suite:
        (repo / 'verify.py').write_text(suite, encoding='utf-8', newline='\n')
    (repo / 'work.md').write_text('# Work\n', encoding='utf-8', newline='\n')
    run(repo, 'add', '.')
    run(repo, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'work')
    return repo, run(repo, 'branch', '--show-current'), session


def close(session, *args, state=None):
    """The real script, its reports kept in the case's own folder (b20261120-roundup-test-state-leak)."""
    env = {**os.environ, 'WOS_STATE_DIR': str(state or Path(tempfile.mkdtemp()))}
    return subprocess.run([sys.executable, str(ROUNDUP), '--session', session, *args],
                          capture_output=True, text=True, encoding='utf-8', env=env)


def test_green_merges_into_develop_pushes_and_lets_go(tmp_path):
    repo, branch, session = held(tmp_path)
    before = run(repo, 'rev-list', '--count', '--all')
    done = close(session)
    assert done.returncode == 0, done.stdout + done.stderr
    assert run(repo, 'branch', '--show-current') == 'develop'
    assert run(repo, 'rev-parse', 'develop') == run(repo, 'rev-parse', 'origin/develop')
    assert run(repo, 'log', '-1', '--format=%s') == 'work' and lock.holder(repo) == ('', '')
    assert run(repo, 'rev-list', '--count', '--all') == before   # the close commits nothing
    assert not run(repo, 'branch', '--list', branch)


@pytest.mark.parametrize('args, suite, code', [(['--draft'], '', 0),
                                               ([], 'raise SystemExit(1)\n', 1)])
def test_draft_or_red_pushes_the_feature_only(tmp_path, args, suite, code):
    repo, branch, session = held(tmp_path, suite)
    done = close(session, *args)
    assert done.returncode == code, done.stdout + done.stderr
    assert 'not merged' in done.stdout and run(repo, 'branch', '--show-current') == 'develop'
    assert f'ask Lucas before resuming {branch}' in done.stdout   # the line the handoff carries
    assert run(repo, 'rev-parse', branch) == run(repo, 'rev-parse', f'origin/{branch}')
    assert run(repo, 'rev-parse', 'develop') != run(repo, 'rev-parse', branch)
    assert lock.holder(repo) == ('', '')


def test_a_failed_push_keeps_the_lock(tmp_path):
    repo, branch, session = held(tmp_path)
    run(repo, 'config', '--unset-all', f'url.{tmp_path / "repo.git"}.insteadOf')
    run(repo, 'config', 'url./nonexistent.insteadOf', LOCK_URL)
    done = close(session)
    assert done.returncode == 1 and 'Still held' in done.stdout
    assert lock.holder(repo)[0] == session


def test_a_dirty_tree_stops_before_anything(tmp_path):
    repo, branch, session = held(tmp_path)
    (repo / 'work.md').write_text('# Changed\n', encoding='utf-8', newline='\n')
    done = close(session)
    assert done.returncode == 2 and 'dirty' in done.stdout
    assert run(repo, 'branch', '--show-current') == branch and lock.holder(repo)[0] == session


def test_a_claim_on_develop_closes_the_feature_switched_to_never_develop(tmp_path):
    session = f'test-roundup-{tmp_path.name}'
    repo = governed_repo(tmp_path)
    lock.claim(repo, session)                       # records develop, the branch it found
    assert 'not a feature' in close(session).stdout and run(repo, 'branch', '--list', 'develop')
    run(repo, 'switch', '-q', '-c', 'feature/claimed')
    (repo / 'w.md').write_text('# W\n', encoding='utf-8', newline='\n')
    run(repo, 'add', '.')
    run(repo, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'w')
    done = close(session)
    assert done.returncode == 0 and 'feature/claimed merged into develop' in done.stdout, done.stdout
    assert run(repo, 'rev-parse', 'origin/develop') == run(repo, 'rev-parse', 'develop')


def test_a_named_repo_closes_alone_and_the_rest_stay_held(tmp_path):
    repo, branch, session = held(tmp_path)
    other = governed_repo(tmp_path, 'other')
    lock.take(other, session, 'more', True)
    done = close(session, str(repo))
    assert done.returncode == 0 and 'merged into develop' in done.stdout, done.stdout + done.stderr
    assert lock.holder(repo) == ('', '') and lock.holder(other)[0] == session
    assert close(session, str(tmp_path / 'nowhere')).returncode == 64


def test_waiting_notes_are_listed_and_never_block(tmp_path, monkeypatch):
    monkeypatch.setenv('WOS_SESSION_STATE', str(tmp_path / 'state'))
    import outbox
    repo, branch, session = held(tmp_path)
    note = outbox.add(repo, 'ISSUES.md', 'a drive-by finding', 'someone-else')
    done = close(session)
    assert done.returncode == 0 and f'outbox: {repo}: {note}  ISSUES.md: a drive-by finding' in done.stdout


def test_a_session_holding_nothing_closes_quietly():
    done = close('test-roundup-holds-nothing')
    assert done.returncode == 0 and 'holds no repo' in done.stdout


def test_periodic_runs_only_for_the_trees_held_and_only_speaks_with_news(tmp_path, capsys):
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader('roundup_script', str(ROUNDUP))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    module.ROOT = tmp_path
    for tree, said in (('a', 'news'), ('b', ''), ('c', 'never'), ('d', 'nested')):
        (tmp_path / tree).mkdir()
        (tmp_path / tree / 'job.py').write_text(f'import sys\nprint("{said}", sys.argv[1:]) if "{said}" else None\n',
                                                encoding='utf-8', newline='\n')
    run(tmp_path / 'd', 'init', '-q')
    (tmp_path / 'core').mkdir()
    (tmp_path / 'core/periodicos.txt').write_text(
        '# comment\ntree\tcommand\tdays\n' + ''.join(f'{t}\tjob.py --every {{days}}\t30\n' for t in 'abcd'),
        encoding='utf-8', newline='\n')
    # Holding the root (an ancestor) runs neither a plain folder's job nor a nested repo's.
    module.periodic([tmp_path / 'a', tmp_path / 'b', tmp_path])
    shown = capsys.readouterr().out
    assert "periodic: a\nnews ['--every', '30']" in shown
    assert 'periodic: b' not in shown and 'never' not in shown and 'nested' not in shown
