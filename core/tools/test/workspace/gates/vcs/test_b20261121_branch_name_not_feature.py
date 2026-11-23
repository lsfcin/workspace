# b20261121-branch-name-not-feature regression: a branch is named for its work, by whoever takes the repo.
import re
import sys

import pytest

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402

A, B = 'test-branch-name-session-a', 'test-branch-name-session-b'
QUIET = ('-c', 'core.hooksPath=/dev/null')


@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob('lock_*'):
        if re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve())) in path.name:
            path.unlink(missing_ok=True)


def test_a_first_write_asks_for_a_name(tmp_path):
    repo = governed_repo(tmp_path)
    refusal, _ = lock.verdict(repo / 'core/x.py', A)
    assert f'wos/take {repo}' in refusal and run(repo, 'branch', '--show-current') == 'develop'
    assert not lock.holder(repo)[0]


def test_take_branches_by_the_name_given(tmp_path):
    repo = governed_repo(tmp_path)
    refusal, note = lock.take(repo, A, 'b20261121-branch-name')
    assert not refusal and A in note
    assert lock.holder(repo) == (A, 'feature/b20261121-branch-name')
    assert run(repo, 'branch', '--show-current') == 'feature/b20261121-branch-name'
    assert lock.verdict(repo / 'a', A) == ('', '')


@pytest.mark.parametrize('name', ['', 'a/b', 'Foo', '-x', 'x_y', 'feature/x'])
def test_a_name_outside_the_alphabet_is_refused(tmp_path, name):
    repo = governed_repo(tmp_path)
    assert lock.take(repo, A, name)[0] and run(repo, 'branch', '--show-current') == 'develop'


def test_a_name_already_used_here_or_on_origin_is_refused(tmp_path):
    repo = governed_repo(tmp_path)
    run(repo, 'branch', 'feature/local')
    run(repo, 'switch', '-q', '-c', 'feature/remote')
    run(repo, *QUIET, 'commit', '-q', '--allow-empty', '-m', 'r')
    run(repo, 'push', '-q', 'origin', 'feature/remote')
    run(repo, 'switch', '-q', 'develop')
    run(repo, 'branch', '-D', 'feature/remote')
    for name in ('local', 'remote'):
        refusal, _ = lock.take(repo, A, name)
        assert 'already' in refusal and run(repo, 'branch', '--show-current') == 'develop', name
    assert not lock.holder(repo)[0]


def test_take_is_refused_while_another_session_holds(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, A, 'first')
    assert 'held by session' in lock.take(repo, B, 'second')[0]


def test_claim_switches_to_the_branch_it_resumes(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, A, 'kept')
    run(repo, *QUIET, 'commit', '-q', '--allow-empty', '-m', 'k')
    run(repo, 'push', '-q', 'origin', 'feature/kept')
    run(repo, 'switch', '-q', 'develop')
    run(repo, 'branch', '-D', 'feature/kept')
    lock.release(repo, A)
    refusal, before = lock.claim(repo, B, 'kept')
    assert not refusal and before == ''
    assert run(repo, 'branch', '--show-current') == 'feature/kept' and lock.holder(repo) == (B, 'feature/kept')
    run(repo, 'switch', '-q', 'develop')
    assert lock.claim(repo, A, 'kept')[1] == B and run(repo, 'branch', '--show-current') == 'feature/kept'


def test_claim_refuses_a_dirty_tree_and_a_missing_branch(tmp_path):
    repo = governed_repo(tmp_path)
    assert 'no branch' in lock.claim(repo, A, 'ghost')[0]
    (repo / 'README.md').write_text('dirt\n', encoding='utf-8', newline='\n')
    run(repo, 'branch', 'feature/there')
    assert 'uncommitted' in lock.claim(repo, A, 'there')[0]
    assert run(repo, 'branch', '--show-current') == 'develop' and not lock.holder(repo)[0]
