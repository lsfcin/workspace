# b20261121-script-write-free-repo regression: a script write into a free repo is refused when its text shows it, and owned by its session when it does not.
import json
import re
import subprocess
import sys

import pytest

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import dirt  # noqa: E402
import lock  # noqa: E402

A, B = 'test-script-write-session-a', 'test-script-write-session-b'
HOOKS = WORKSPACE_ROOT / 'core/hooks/git'


@pytest.fixture(autouse=True)
def _drop_state(tmp_path):
    yield
    key = re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve()))
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob('*'):
        if key in path.name or any(s in path.name for s in (A, B)):
            path.unlink(missing_ok=True)


def _hook(gate, command, cwd, session=A, event='PreToolUse'):
    payload = {'tool_name': 'Bash', 'session_id': session, 'cwd': str(cwd), 'hook_event_name': event,
               'tool_input': {'command': command}}
    return subprocess.run([sys.executable, str(HOOKS / gate)], input=json.dumps(payload),
                          capture_output=True, text=True, encoding='utf-8')


def test_a_write_the_text_shows_is_refused_on_a_free_repo(tmp_path):
    repo = governed_repo(tmp_path)
    for command in ('echo x > a.md', 'printf x | tee notes.md', "sed -i 's/x/y/' README.md",
                    'python3 -c "open(\'README.md\', \'w\').write(\'y\')"', "cat > b.md <<'EOF'\nb\nEOF"):
        done = _hook('lock-gate.py', command, repo)
        assert done.returncode == 2 and 'wos/take' in done.stderr and 'writes' in done.stderr, command
    assert not run(repo, 'status', '--porcelain')


def test_what_is_not_a_write_into_the_repo_passes(tmp_path):
    repo = governed_repo(tmp_path)
    (repo / '.git/info/exclude').write_text('out/\n', encoding='utf-8', newline='\n')
    for command in (f'echo x > {tmp_path}/outside.md', 'echo "a > b.md"', 'python3 -c "print(1 > 0)"',
                    'echo x > out/report.md', 'echo x > "$S/x.md"', 'ls 2>/dev/null'):
        assert _hook('lock-gate.py', command, repo).returncode == 0, command
    elsewhere = tmp_path / 'scratch'
    elsewhere.mkdir()
    assert _hook('lock-gate.py', f'S={elsewhere}; cd $S && git init -q && echo x > a.md', repo).returncode == 0
    assert _hook('lock-gate.py', f'R={repo}; cd $R && git commit -qm x', tmp_path).returncode == 2
    lock.take(repo, A, 'work')
    assert _hook('lock-gate.py', 'echo x > a.md', repo).returncode == 0
    assert _hook('lock-gate.py', 'echo x > a.md', repo, session=B).returncode == 2


def test_unseen_dirt_belongs_to_the_session_that_left_it(tmp_path):
    repo = governed_repo(tmp_path)
    assert _hook('dirt.py', 'python3 build.py', repo).returncode == 0
    (repo / 'README.md').write_text('built\n', encoding='utf-8', newline='\n')
    (repo / 'new.md').write_text('new\n', encoding='utf-8', newline='\n')
    done = _hook('dirt.py', 'python3 build.py', repo, event='PostToolUse')
    assert 'wos/take' in done.stdout and dirt.mine(repo, A) == {'README.md', 'new.md'}
    assert _hook('lock-gate.py', 'git restore README.md', repo, session=B).returncode == 2
    assert _hook('lock-gate.py', 'git restore README.md', repo).returncode == 0
    assert 'nobody holds' in lock.take(repo, B, 'theirs')[0]
    refusal, _ = lock.take(repo, A, 'carry')
    assert not refusal and run(repo, 'branch', '--show-current') == 'feature/carry'
    assert (repo / 'new.md').is_file() and not dirt.owners(repo).is_file()


def test_dirt_that_was_there_before_stays_nobodys(tmp_path):
    repo = governed_repo(tmp_path)
    (repo / 'README.md').write_text('lucas\n', encoding='utf-8', newline='\n')
    _hook('dirt.py', 'make', repo)
    (repo / 'mine.md').write_text('mine\n', encoding='utf-8', newline='\n')
    _hook('dirt.py', 'make', repo, event='PostToolUse')
    assert dirt.mine(repo, A) == {'mine.md'} and 'nobody holds' in lock.take(repo, A, 'work')[0]
