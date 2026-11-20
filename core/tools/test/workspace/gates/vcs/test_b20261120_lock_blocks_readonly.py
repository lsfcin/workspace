# b20261120-lock-blocks-readonly regression: a git command that only reads passes the branch lock, whoever holds the repo.
import json
import re
import subprocess
import sys

import pytest

from conftest import WORKSPACE_ROOT, governed_repo

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402

A, B = 'test-readonly-session-a', 'test-readonly-session-b'
GATE = WORKSPACE_ROOT / 'core/hooks/git/lock-gate.py'


@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob('lock_*'):
        if re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve())) in path.name:
            path.unlink(missing_ok=True)


def _shell(command):
    return subprocess.run([sys.executable, str(GATE)], capture_output=True, text=True, encoding='utf-8',
                          input=json.dumps({'tool_name': 'Bash', 'session_id': A, 'cwd': '.',
                                            'tool_input': {'command': command}}))


def test_a_read_passes_whoever_holds_the_repo(tmp_path):
    """Listing, a read verb, and prose that quotes git; a body fed to an interpreter is still a command."""
    repo = governed_repo(tmp_path)
    lock.verdict(repo / 'a', B)
    for command in (f'git -C {repo} branch --show-current', f'git -C {repo} merge-base develop develop',
                    f'git -C {repo} status', f'git -C {repo} stash list',
                    f"cat <<'EOF'\ngit -C {repo} commit -m quoted\nEOF"):
        done = _shell(command)
        assert done.returncode == 0, (command, done.stderr)
    assert _shell(f"python3 - <<'EOF'\nimport os; os.system('git -C {repo} commit')\nEOF").returncode == 2
