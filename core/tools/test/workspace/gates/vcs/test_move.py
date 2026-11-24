# T1 wos/move: a governed repo moves with its lock and its dirt, and a raw `mv` of one is refused.
import json
import subprocess
import sys

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import dirt  # noqa: E402
import lock  # noqa: E402

A, B = 'test-move-session-a', 'test-move-session-b'
MOVE = WORKSPACE_ROOT / 'core/tools/wos/move'
GATE = WORKSPACE_ROOT / 'core/hooks/git/lock-gate.py'


def _move(src, dst, session=A):
    return subprocess.run([sys.executable, str(MOVE), str(src), str(dst), '--session', session],
                          capture_output=True, text=True, encoding='utf-8')


def _shell(command, cwd, session=A):
    payload = {'tool_name': 'Bash', 'session_id': session, 'cwd': str(cwd), 'tool_input': {'command': command}}
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload),
                          capture_output=True, text=True, encoding='utf-8')


def test_a_held_repo_moves_with_its_lock_and_its_dirt(tmp_path):
    src, dst = governed_repo(tmp_path), tmp_path / 'moved'
    lock.take(src, A, 'work')
    dirt.owners(src).write_text(f'{A}\tx.md\n', encoding='utf-8', newline='\n')
    done = _move(src, dst)
    assert done.returncode == 0, done.stderr
    assert not src.exists() and run(dst, 'branch', '--show-current') == 'feature/work'
    assert lock.holder(dst) == (A, 'feature/work') and lock.holder(src) == ('', '')
    assert dirt.mine(dst, A) == {'x.md'} and not dirt.owners(src).exists()


def test_another_sessions_repo_does_not_move(tmp_path):
    src = governed_repo(tmp_path)
    lock.take(src, B, 'theirs')
    done = _move(src, tmp_path / 'moved')
    assert done.returncode == 1 and '[held]' in done.stderr and src.is_dir()
    assert not (tmp_path / 'moved').exists()


def test_what_is_not_a_repo_root_does_not_move(tmp_path):
    src = governed_repo(tmp_path)
    (tmp_path / 'taken').mkdir()
    assert _move(src / '.git', tmp_path / 'x').returncode == 64
    assert _move(src, tmp_path / 'taken').returncode == 64 and src.is_dir()


def test_a_raw_mv_of_a_governed_root_is_refused_with_the_command(tmp_path):
    src = governed_repo(tmp_path)
    (tmp_path / 'plain').mkdir()
    done = _shell(f'mv {src} {tmp_path / "moved"}', tmp_path)
    assert done.returncode == 2 and f'wos/move {src} {tmp_path / "moved"}' in done.stderr
    assert _shell('mv repo/../plain plain2', tmp_path).returncode == 0
    assert _shell('cd repo && mv -v ../repo ../elsewhere', tmp_path).returncode == 2
