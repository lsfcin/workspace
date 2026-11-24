# T1 the branch lock (core/hooks/git/SPECS.md): one agent session per repo, people never gated.
# Zero-token, no network — every case builds a throwaway repo whose GitHub origin is rewritten to a
# local bare repo, so `governed` sees the profile's owner and every push lands on disk.
import json
import os
import re
import subprocess
import sys
import threading

import pytest

from conftest import WORKSPACE_ROOT, governed_repo, run

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git')]
import lock  # noqa: E402

A, B = 'test-lock-session-a', 'test-lock-session-b'
GATE = WORKSPACE_ROOT / 'core/hooks/git/lock-gate.py'
@pytest.fixture(autouse=True)
def _drop_locks(tmp_path):
    yield
    for path in lock.lock_file(WORKSPACE_ROOT).parent.glob('lock_*'):
        if re.sub(r'[^A-Za-z0-9]', '_', str(tmp_path.resolve())) in path.name:
            path.unlink(missing_ok=True)


def test_take_branches_a_clean_develop(tmp_path):
    repo = governed_repo(tmp_path)
    refusal, note = lock.take(repo, A, 'work')
    assert not refusal and run(repo, 'branch', '--show-current') == 'feature/work' and A in note
    assert lock.holder(repo) == (A, 'feature/work') and repo.resolve() in lock.held_by(A)


def test_another_session_is_refused_until_claim(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, A, 'work')
    refusal, _ = lock.verdict(repo / 'a.md', B)
    # A runnable claim tempted agents to steal a live lock (argon, 2026-11-23): handing over is Lucas's.
    assert '[held]' in refusal and 'Lucas' in refusal and 'wos/claim' not in refusal
    lock.claim(repo, B)
    assert lock.verdict(repo / 'a.md', B) == ('', '') and lock.verdict(repo / 'a.md', A)[0]


def test_two_racing_sessions_get_one_lock(tmp_path):
    repo = governed_repo(tmp_path)
    results = {}
    threads = [threading.Thread(target=lambda s=s: results.update({s: lock.take(repo, s, s)[0]}))
               for s in (A, B)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(bool(r) for r in results.values()) == [False, True]
    assert len(run(repo, 'branch', '--list', 'feature/*').splitlines()) == 1


def test_an_own_switch_is_followed_and_a_shared_branch_is_not(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, A, 'work')
    run(repo, 'branch', '-m', 'feature/renamed')
    assert lock.verdict(repo / 'a', A) == ('', '') and lock.holder(repo)[1] == 'feature/renamed'
    run(repo, 'switch', '-q', 'develop')
    assert 'switch feature/renamed' in lock.verdict(repo / 'a', A)[0]


def test_an_unheld_feature_and_stray_dirt_are_refused(tmp_path):
    repo = governed_repo(tmp_path)
    (repo / 'README.md').write_text('someone else\n', encoding='utf-8', newline='\n')
    assert 'nobody holds' in lock.take(repo, A, 'work')[0]
    run(repo, 'checkout', '-q', '--', '.')
    run(repo, 'switch', '-q', '-c', 'feature/orphan')
    assert 'held by nobody' in lock.verdict(repo / 'a', A)[0]


def test_an_ignored_path_is_written_by_edit_as_by_shell(tmp_path):
    """An Edit on an ignored path of a free repo was refused while the same shell write passed. One
    rule now: a write git never sees passes, judged at the real target, and never a lock file."""
    repo = governed_repo(tmp_path)
    (repo / '.git/info/exclude').write_text('out/\n', encoding='utf-8', newline='\n')
    (repo / 'out').mkdir()
    (repo / 'out/readme-link.md').symlink_to(repo / 'README.md')
    assert lock.verdict(repo / 'out/not/yet/made.md', A) == ('', '')
    assert '[free]' in lock.verdict(repo / 'out/readme-link.md', A)[0]   # the target is tracked
    assert '[free]' in lock.verdict(repo / 'a.md', A)[0]
    assert _shell('echo x > out/report.md', cwd=repo).returncode == 0
    assert not lock.ignored(lock.lock_file(repo))


def test_outside_scope_nothing_is_gated(tmp_path):
    repo = governed_repo(tmp_path)
    run(repo, 'remote', 'set-url', 'origin', 'https://github.com/someone-else/x.git')
    assert lock.verdict(repo / 'a', A) == ('', '')
    trunk = tmp_path / 'trunk'
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(trunk)], check=True)
    assert lock.verdict(trunk / 'a', A) == ('', '')


def _gate(payload):
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload),
                          capture_output=True, text=True, encoding='utf-8')


def _shell(command, session=A, cwd=None):
    return _gate({'tool_name': 'Bash', 'session_id': session, 'cwd': str(cwd or '.'),
                  'tool_input': {'command': command}})


def _judge(argv, cwd, session=A):
    """The git wrapper's verdict on a call, without running it (core/hooks/git/wrapper.py)."""
    import wrapper   # noqa: PLC0415
    return wrapper.judge(argv, str(cwd), session)


def test_a_free_checkout_is_changed_only_after_take(tmp_path):
    """b20261120-shell-branch-unheld: a checkout moved from the shell would be born without an owner.
    Refs and the remote are not the checkout, so a release passes on a free repo (2026-11-23)."""
    repo = governed_repo(tmp_path)
    for argv in (['commit', '-qm', 'x'], ['switch', '-c', 'feature/mine'], ['clean', '-fdq'], ['add', '.'],
                 ['update-ref', 'HEAD', 'HEAD~'], ['branch', '-m', 'renamed'],
                 ['fetch', '-u', 'origin', 'develop:develop'], ['push', '.', 'main:develop'], ['stash'],
                 ['frobnicate'], ['-C', str(repo), 'add', '.']):
        refusal = _judge(argv, repo)
        assert '[free]' in refusal and 'wos/take' in refusal, argv
        assert 'lock-gate.py' not in refusal and 'wrapper.py' not in refusal, argv   # never sends one to edit it
    for argv in (['push', 'origin', 'develop:main'], ['fetch', 'origin', 'main:main'], ['tag', 'v1.0'],
                 ['push', 'origin', 'v1.0'], ['branch', '-d', 'feature/merged'], ['config', '--get', 'user.name']):
        assert _judge(argv, repo) == '', argv
    assert not lock.holder(repo)[0]


def test_the_holder_never_leaves_its_feature_by_itself(tmp_path):
    """b20261120-red-close-strands-session: going back after a close is the same refusal as any free repo."""
    repo = governed_repo(tmp_path)
    lock.take(repo, A, 'work')
    feature = run(repo, 'branch', '--show-current')
    assert 'close\'s job' in _judge(['switch', 'develop'], repo)
    assert _judge(['switch', '-c', 'feature/second'], repo) == ''
    for restore in (['checkout', 'develop', '--', 'README.md'], ['checkout', 'develop', 'README.md']):
        assert _judge(restore, repo) == '', restore   # a file from develop is not a move onto it
    run(repo, 'switch', '-q', 'develop')   # a person, or the close, moved it back
    assert 'switch' in lock.verdict(repo / 'a', A)[0]
    assert _judge(['switch', feature], repo) == ''
    lock.release(repo, A)
    assert 'wos/take' in _judge(['switch', feature], repo)


def test_a_person_commits_on_develop_and_an_agent_cannot(tmp_path):
    repo = governed_repo(tmp_path)
    env = {k: v for k, v in os.environ.items() if k not in lock.SESSION_ENV}
    hooks = ['-c', f'core.hooksPath={WORKSPACE_ROOT / "core/hooks"}']
    (repo / 'b.md').write_text('# B\n', encoding='utf-8', newline='\n')
    run(repo, 'add', 'b.md')
    person = subprocess.run(['git', *hooks, 'commit', '-qm', 'person'], cwd=repo, env=env,
                            capture_output=True, text=True, encoding='utf-8')
    assert person.returncode == 0, person.stdout + person.stderr
    (repo / 'c.md').write_text('# C\n', encoding='utf-8', newline='\n')
    run(repo, 'add', 'c.md')
    agent = subprocess.run(['git', *hooks, 'commit', '-qm', 'agent'], cwd=repo,
                           env={**env, 'CLAUDE_CODE_SESSION_ID': A}, capture_output=True, text=True, encoding='utf-8')
    assert agent.returncode != 0 and 'BRANCH LOCK' in agent.stdout + agent.stderr


def test_the_switch_really_switches_the_lock_off(tmp_path, monkeypatch):
    repo = governed_repo(tmp_path)
    assert _judge(['commit', '-qm', 'x'], repo)
    monkeypatch.setenv('WOS_FEATURES_OFF', 'branch-lock')
    assert _judge(['commit', '-qm', 'x'], repo) == ''
