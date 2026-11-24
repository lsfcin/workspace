# T1 the git wrapper (core/hooks/git/SPECS.md § The git wrapper): an agent's git call that touches a repo it does not hold is refused, by whatever process makes it; a person's never is.
# Zero-token, no network: a throwaway governed repo, the real wrapper first on a PATH of the case's own.
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import WORKSPACE_ROOT, governed_repo

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git'), str(WORKSPACE_ROOT / 'core/hooks')]
import lock  # noqa: E402
import platform_law  # noqa: E402
import wrapper  # noqa: E402

FRONT = WORKSPACE_ROOT / 'core/hooks/git/git'
OWNER, OTHER = 'test-wrapper-owner', 'test-wrapper-other'


@pytest.fixture
def held(tmp_path, monkeypatch):
    """(repo, env): a governed repo OWNER holds, and an env whose `git` is the wrapper."""
    monkeypatch.setenv('WOS_SESSION_STATE', str(tmp_path / 'state'))
    repo = governed_repo(tmp_path)
    assert lock.take(repo, OWNER, 'work')[0] == ''
    (tmp_path / 'bin').mkdir()
    (tmp_path / 'bin/git').symlink_to(FRONT)
    env = {k: v for k, v in os.environ.items() if k not in (*lock.SESSION_ENV, 'WOS_GIT_JUDGED')}
    env['PATH'] = f'{tmp_path / "bin"}{os.pathsep}{env["PATH"]}'
    (repo / 'new.md').write_text('# New\n', encoding='utf-8', newline='\n')
    return repo, env


def git(repo, env, *args, session=None):
    env = {**env, 'WOS_SESSION': session} if session else env
    return subprocess.run(['git', *args], cwd=repo, env=env, capture_output=True, text=True, encoding='utf-8')


def staged(repo):
    return subprocess.run([platform_law.real_git(), 'diff', '--cached', '--name-only'], cwd=repo,
                          capture_output=True, text=True, encoding='utf-8').stdout.strip()


def test_the_front_reads_the_session_ids_lock_names_in_its_order():
    names = re.findall(r'\$\{(\w+):-', FRONT.read_text(encoding='utf-8').split('session=', 1)[1].splitlines()[0])
    assert tuple(names) == lock.SESSION_ENV


def test_real_git_is_never_the_wrapper(held, tmp_path, monkeypatch):
    monkeypatch.setenv('PATH', held[1]['PATH'])
    platform_law.real_git.cache_clear()
    try:
        assert not os.path.samefile(platform_law.real_git(), FRONT)
    finally:
        platform_law.real_git.cache_clear()


def test_a_foreign_session_is_refused_by_shell_and_by_script(held):
    repo, env = held
    refused = git(repo, env, 'add', 'new.md', session=OTHER)
    assert refused.returncode == 128 and 'BRANCH LOCK' in refused.stderr and not staged(repo)
    script = "import subprocess; raise SystemExit(subprocess.run(['git', 'add', 'new.md']).returncode)"
    by_script = subprocess.run([sys.executable, '-c', script], cwd=repo, capture_output=True, text=True, encoding='utf-8',
                               env={**env, 'WOS_SESSION': OTHER})
    assert by_script.returncode == 128 and not staged(repo)


def test_the_holder_a_person_and_a_read_pass(held):
    repo, env = held
    assert git(repo, env, 'log', '-1', '--format=%s', session=OTHER).returncode == 0
    assert git(repo, env, '-C', str(repo), 'status', session=OTHER).returncode == 0
    assert git(repo, env, 'add', 'new.md').returncode == 0 and staged(repo) == 'new.md'   # a person
    git(repo, env, 'reset', '-q')
    assert git(repo, env, 'add', 'new.md', session=OWNER).returncode == 0 and staged(repo) == 'new.md'


def test_the_repo_is_the_one_git_resolves_through_its_own_options(held, tmp_path):
    repo, env = held
    (tmp_path / 'elsewhere').mkdir()
    for args in (['-C', str(tmp_path), '-C', 'repo', 'add', 'new.md'],
                 ['--git-dir', str(repo / '.git'), '--work-tree', str(repo), 'add', str(repo / 'new.md')],
                 ['-c', 'core.quotepath=false', 'add', 'new.md']):
        done = git(tmp_path / 'elsewhere' if args[0] != '-c' else repo, env, *args, session=OTHER)
        assert done.returncode == 128 and not staged(repo), args


def test_an_ancestor_a_shim_registered_names_the_session(held, tmp_path):
    repo, env = held
    # A child registers itself as a harness host would, then runs git with no session id in env.
    script = ('import os, subprocess, sys; sys.path[:0] = sys.argv[1:3]; import wrapper; '
              f'wrapper.register({OTHER!r}, os.getpid()); '
              "raise SystemExit(subprocess.run(['git', 'add', 'new.md']).returncode)")
    host = subprocess.run([sys.executable, '-c', script, str(WORKSPACE_ROOT / 'core/hooks/git'),
                           str(WORKSPACE_ROOT / 'core/hooks')], cwd=repo, env=env, capture_output=True, text=True, encoding='utf-8')
    assert host.returncode == 128 and not staged(repo), host.stderr
    # The host is gone: its entry no longer matches a live process, so a later git is a person's.
    assert git(repo, env, 'add', 'new.md').returncode == 0 and staged(repo) == 'new.md'


def test_a_reused_pid_names_nobody(tmp_path, monkeypatch):
    monkeypatch.setenv('WOS_SESSION_STATE', str(tmp_path))
    me = platform_law.ancestors()[0]
    (tmp_path / f'agent_pid_{me[0]}.txt').write_text(f'{OTHER}\t{int(me[1]) - 1}\n', encoding='utf-8', newline='\n')
    assert wrapper.session() in ('', lock.env_session())
    monkeypatch.delenv('CLAUDE_CODE_SESSION_ID', raising=False)
    for name in lock.SESSION_ENV:
        monkeypatch.delenv(name, raising=False)
    assert wrapper.session() == ''
    wrapper.register(OTHER, me[0])
    assert wrapper.session() == OTHER


def test_a_harness_whose_git_is_unwrapped_is_refused_its_shell(held):
    import json   # noqa: PLC0415
    repo, env = held
    bare = os.pathsep.join(d for d in env['PATH'].split(os.pathsep)
                           if not (Path(d) / 'git').is_symlink())   # every wrapper link gone
    payload = json.dumps({'tool_name': 'Bash', 'session_id': OTHER, 'cwd': str(repo),
                          'tool_input': {'command': 'ls'}})
    for command, code in (('ls', 2), ('core/run tools/wos/gitwrap --install', 0)):
        done = subprocess.run([sys.executable, str(WORKSPACE_ROOT / 'core/hooks/git/lock-gate.py')],
                              input=payload.replace('"ls"', json.dumps(command)), capture_output=True,
                              text=True, encoding='utf-8', env={**env, 'PATH': bare})
        assert done.returncode == code and ('[unwrapped]' in done.stderr) == (code == 2), done.stderr


def test_a_crash_lets_the_call_through_and_says_so(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('WOS_SESSION_STATE', str(tmp_path))
    monkeypatch.setattr(wrapper, 'judge', lambda *a: 1 / 0)
    ran = []
    monkeypatch.setattr(os, 'execve', lambda *a: ran.append(a))
    wrapper.main(['add', 'x'])
    assert ran and 'crashed' in capsys.readouterr().err
    assert 'ZeroDivisionError' in (tmp_path / 'git_wrapper.log').read_text(encoding='utf-8')
