# b20261110-verify-not-merge-result regression: the close's suite judges the feature merged with origin/develop, and that commit is what lands.
import os
import re
import subprocess
import sys

import pytest

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402

ROUNDUP = WORKSPACE_ROOT / 'core/tools/wos/roundup'
SUITE = 'import pathlib, sys\nsys.exit(pathlib.Path("gate.txt").exists())\n'


@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    key = re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve()))
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob(f'lock_*{key}*'):
        path.unlink(missing_ok=True)


def test_develop_moved_on_origin_is_merged_before_the_suite_runs(tmp_path):
    session = f'test-merge-result-{tmp_path.name}'
    repo = governed_repo(tmp_path)
    lock.take(repo, session, 'work')
    (repo / 'verify.py').write_text(SUITE, encoding='utf-8', newline='\n')
    run(repo, 'add', '.')
    run(repo, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'work')
    other = tmp_path / 'other'
    subprocess.run(['git', 'clone', '-q', '-b', 'develop', str(tmp_path / 'repo.git'), str(other)], check=True)
    (other / 'gate.txt').write_text('red once merged\n', encoding='utf-8', newline='\n')
    run(other, 'add', '.')
    run(other, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'moves develop')
    run(other, 'push', '-q', 'origin', 'develop')
    done = subprocess.run([sys.executable, str(ROUNDUP), '--session', session], capture_output=True, text=True,
                          encoding='utf-8', env={**os.environ, 'WOS_STATE_DIR': str(tmp_path)})
    assert done.returncode == 1 and 'verify red' in done.stdout, done.stdout
    assert 'red' in next(tmp_path.glob('verify-*.md')).read_text(encoding='utf-8')
    assert run(repo, 'rev-parse', 'origin/develop') == run(other, 'rev-parse', 'develop')
