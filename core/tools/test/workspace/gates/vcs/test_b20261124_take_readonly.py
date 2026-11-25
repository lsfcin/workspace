# b20261124-take-readonly regression: a git dir the session cannot write is named as such, by take and by the close, and nobody is made its owner. A Codex sandbox mounted .git read-only and take called it a divergence.
import os
import re
import subprocess
import sys
import tempfile

import pytest

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402

A = 'test-take-readonly-a'
ROUNDUP = WORKSPACE_ROOT / 'core/tools/wos/roundup'


@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob('lock_*'):
        if re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve())) in path.name:
            path.unlink(missing_ok=True)


def readonly(repo):
    """The git dir as a sandbox leaves it: readable, not writable. Restored by the caller."""
    os.chmod(repo / '.git', 0o555)
    if os.access(repo / '.git', os.W_OK):   # root ignores mode bits: no sandbox to imitate
        os.chmod(repo / '.git', 0o755)
        pytest.skip('running as root')


def test_take_names_a_readonly_git_dir_and_takes_nothing(tmp_path):
    repo = governed_repo(tmp_path)
    readonly(repo)
    try:
        refusal, note = lock.take(repo, A, 'work')
    finally:
        os.chmod(repo / '.git', 0o755)
    assert '[readonly]' in refusal and 'diverged' not in refusal and not note
    assert lock.holder(repo) == ('', '') and run(repo, 'branch', '--show-current') == 'develop'
    assert not list((repo / '.git').glob('.wos-write-trial.*'))


@pytest.mark.parametrize(('step', 'code'), [(('switch', '-q', 'develop'), '[git]'),
                                            (('merge', '-q', '--ff-only', 'origin/develop'), '[diverged]'),
                                            (('switch', '-q', '-c', 'feature/work'), '[branch]')])
def test_a_failed_step_keeps_git_words_and_its_own_code(tmp_path, monkeypatch, step, code):
    repo, said, real = governed_repo(tmp_path), 'fatal: what git really said', lock.git
    monkeypatch.setattr(lock, 'git', lambda path, *args: subprocess.CompletedProcess(args, 128, '', said)
                        if args == step else real(path, *args))
    refusal, note = lock.take(repo, A, 'work')
    assert code in refusal and said in refusal and f'git {step[0]}' in refusal and not note
    assert ('Lucas' in refusal) == (code == '[diverged]') and lock.holder(repo) == ('', '')


def test_an_unreachable_origin_takes_offline_and_says_why(tmp_path):
    repo = governed_repo(tmp_path)
    (tmp_path / 'repo.git').rename(tmp_path / 'gone.git')   # the URL still names the owner; nothing answers it
    refusal, note = lock.take(repo, A, 'work')
    assert not refusal and '(offline: not pulled — ' in note and 'repo.git' in note and '\n' not in note
    assert lock.holder(repo) == (A, 'feature/work')


def test_the_close_refuses_a_readonly_git_dir_and_keeps_the_lock(tmp_path):
    repo = governed_repo(tmp_path)
    assert not lock.take(repo, A, 'work')[0]
    readonly(repo)
    try:
        done = subprocess.run([sys.executable, str(ROUNDUP), '--session', A], capture_output=True, text=True,
                              encoding='utf-8', env={**os.environ, 'WOS_STATE_DIR': tempfile.mkdtemp()})
    finally:
        os.chmod(repo / '.git', 0o755)
    assert done.returncode == 1 and '[readonly]' in done.stdout and 'Still held' in done.stdout, done.stdout
    assert lock.holder(repo) == (A, 'feature/work')
