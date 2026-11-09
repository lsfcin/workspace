# b20261109 regression: a close acts on the repos its session worked in, and settles its own files.
#
# A session that only touched code/apptime was stopped by twenty files at the workspace root, and
# every close pushed and promoted all nested projects with no verify run. Each case builds its own
# throwaway repos; the transcript is a real file under a throwaway HOME.
import json
import os
import subprocess
import sys

from conftest import WORKSPACE_ROOT
from platform_law import interpreter
from test_roundup import _dirty, _git, _run, _workspace


def _project(ws):
    """A nested project with commits main does not have yet."""
    project = ws / 'code/proj'
    project.mkdir(parents=True)
    with (ws / '.git/info/exclude').open('a', encoding='utf-8', newline='\n') as ignored:
        ignored.write('code/\n')   # a nested repo is ignored by the workspace's git, as every real one is
    _git(project, 'init', '-q', '-b', 'main')
    _git(project, 'config', 'user.email', 't@t')
    _git(project, 'config', 'user.name', 't')
    _git(project, 'config', 'core.hooksPath', '/dev/null')
    (project / 'a.txt').write_text('one\n', encoding='utf-8', newline='\n')
    _git(project, 'add', '-A')
    _git(project, 'commit', '-qm', 'first', '--no-verify')
    return project


def _close(ws, home, edited, *args):
    """Run the close as a session whose transcript records one Edit, at `edited`."""
    folder = home / '.claude/projects' / ''.join(c if c.isalnum() else '-' for c in str(ws))
    folder.mkdir(parents=True)
    rows = [{'cwd': str(ws), 'message': {'content': [
                {'type': 'tool_use', 'id': 'a', 'name': 'Edit',
                 'input': {'file_path': str(edited), 'old_string': 'x', 'new_string': 'y'}}]}},
            {'message': {'content': [{'type': 'tool_result', 'tool_use_id': 'a'}]}}]
    (folder / 's1.jsonl').write_text('\n'.join(map(json.dumps, rows)) + '\n', encoding='utf-8',
                                       newline='\n')
    env = {**os.environ, 'HOME': str(home), 'CLAUDE_CODE_SESSION_ID': 's1'}
    return subprocess.run([interpreter(), str(ws / 'core/tools/wos/roundup'), *args], cwd=ws,
                          capture_output=True, text=True, encoding='utf-8', env=env)


def test_only_the_commit_s_own_directory_counts(tmp_path):
    """`git -C other status` earlier in the same command line once put `other` in the session."""
    sys.path[:0] = [str(WORKSPACE_ROOT / d) for d in ('core/tools/wos/close', 'core/hooks/routing')]
    from projects import _commit_dir
    assert _commit_dir('git -C other status; git add x && git commit -m y', tmp_path) == tmp_path
    assert _commit_dir('cd code/a && git commit -m y', tmp_path) == tmp_path / 'code/a'
    assert _commit_dir('git -C code/b commit -m y', tmp_path) == tmp_path / 'code/b'
    assert _commit_dir('git status', tmp_path) is None


def test_a_session_in_a_nested_repo_is_not_stopped_by_dirt_at_the_root(tmp_path):
    ws = _workspace(tmp_path)
    project = _project(ws)
    _dirty(ws)
    before = _git(ws, 'status', '--porcelain').stdout
    r = _close(ws, tmp_path / 'home', project / 'a.txt')
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'left alone' in r.stdout and 'code/proj' in r.stdout
    assert _git(ws, 'status', '--porcelain').stdout == before, 'the root was not this session\'s'


def test_a_repo_the_session_never_touched_gets_no_action(tmp_path):
    ws = _workspace(tmp_path)
    project = _project(ws)
    head = _git(project, 'rev-parse', 'HEAD').stdout
    r = _close(ws, tmp_path / 'home', ws / 'shipped.txt')
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'code/proj' not in r.stdout
    assert _git(project, 'rev-parse', 'HEAD').stdout == head


def test_no_session_identity_means_only_the_current_repo(tmp_path):
    ws = _workspace(tmp_path)
    _project(ws)
    env_free = {k: v for k, v in os.environ.items() if 'SESSION_ID' not in k and 'THREAD_ID' not in k}
    r = subprocess.run([interpreter(), str(ws / 'core/tools/wos/roundup')], cwd=ws, env=env_free,
                       capture_output=True, text=True, encoding='utf-8')
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'code/proj' not in r.stdout


def test_a_generated_file_left_dirty_does_not_stop_the_close_and_gets_committed(tmp_path):
    ws = _workspace(tmp_path)
    page = ws / 'ISSUES.md'
    page.write_text(page.read_text(encoding='utf-8').replace('9 findings', '8 findings'),
                    encoding='utf-8', newline='\n')
    r = _run(ws)
    assert r.returncode == 0, r.stdout
    assert 'ISSUES.md' not in _git(ws, 'status', '--porcelain').stdout


def test_hand_edits_in_issues_still_stop_the_close(tmp_path):
    ws = _workspace(tmp_path)
    page = ws / 'ISSUES.md'
    page.write_text(page.read_text(encoding='utf-8') + '\nA bug someone is writing\n',
                    encoding='utf-8', newline='\n')
    r = _run(ws)
    assert r.returncode == 2 and 'ISSUES.md' in r.stdout


def test_a_regenerated_file_never_carries_foreign_staged_work(tmp_path):
    ws = _workspace(tmp_path)
    _dirty(ws)
    r = _run(ws, '--leave-dirty', 'parallel session on theirs.md')
    assert r.returncode == 0, r.stdout
    assert 'parallel session on theirs.md' in r.stdout
    assert 'theirs.md' not in _git(ws, 'log', '--name-only', '--pretty=format:', 'feature/x').stdout
    assert 'A  theirs.md' in _git(ws, 'status', '--porcelain').stdout


def test_leave_dirty_without_a_reason_is_a_usage_error(tmp_path):
    assert _run(_workspace(tmp_path), '--leave-dirty').returncode == 64


def _inbox(ws, added):
    path = ws / 'brain/INBOX.md'
    path.parent.mkdir()
    path.write_text('# Inbox\n', encoding='utf-8', newline='\n')
    _git(ws, 'add', '-A')
    _git(ws, 'commit', '-qm', 'inbox', '--no-verify')
    path.write_text('# Inbox\n' + added, encoding='utf-8', newline='\n')


def test_a_bot_capture_is_committed_by_the_close(tmp_path):
    ws = _workspace(tmp_path)
    _inbox(ws, '\nhttps://example.com\n— via aiwbot · 2026-11-09\n')
    r = _run(ws)
    assert r.returncode == 0, r.stdout
    assert 'brain/INBOX.md' not in _git(ws, 'status', '--porcelain').stdout


def test_an_unsigned_addition_to_the_inbox_is_not_the_bot_s(tmp_path):
    ws = _workspace(tmp_path)
    _inbox(ws, '\nan entry someone is still drafting\n')
    r = _run(ws)
    assert r.returncode == 2 and 'brain/INBOX.md' in r.stdout
