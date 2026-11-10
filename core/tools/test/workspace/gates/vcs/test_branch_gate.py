# T0 the branch gate (core/hooks/SPECS.md § Branch drift): a session writes on the branch it chose,
# and nothing else it does — switching itself, leaving a finished branch — is ever refused.
#
# The refusals are two and the passes are many, and the passes are what Lucas asked to be sure of:
# a gate that blocks sessions in a way nobody predicted is the bigger headache. Real git repos,
# the real verdict; ROOT points at a throwaway workspace so `code/proj` is inside Git Flow.
import json
import os
import subprocess
import sys

import pytest

from conftest import WORKSPACE_ROOT

sys.path.insert(0, str(WORKSPACE_ROOT / 'core/hooks/git'))
import branch_marker  # noqa: E402

GATE = WORKSPACE_ROOT / 'core/hooks/git/branch-gate.py'
SESSION = 't-gate'


def _git(repo, *args):
    subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def proj(tmp_path, monkeypatch):
    """code/proj on develop, one commit, inside a fake workspace; markers removed afterwards."""
    monkeypatch.setattr(branch_marker, 'ROOT', tmp_path)
    repo = tmp_path / 'code/proj'
    repo.mkdir(parents=True)
    _git(repo, 'init', '-q', '-b', 'main')
    _git(repo, '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-q', '--no-verify', '--allow-empty', '-m', 'one')
    _git(repo, 'branch', 'develop')
    _git(repo, 'switch', '-q', 'develop')
    yield repo
    branch_marker.marker_for(repo, SESSION).unlink(missing_ok=True)


def _verdict(repo):
    return branch_marker.verdict(repo / 'a.txt', SESSION)


def test_a_shared_branch_is_refused_with_the_command_and_the_branches_to_reuse(proj):
    _git(proj, 'branch', 'feature/older')
    refusal, _ = _verdict(proj)
    assert 'switch -c feature/' in refusal and 'feature/older' in refusal, refusal


def test_the_first_write_on_a_feature_passes_and_names_the_branch(proj):
    _git(proj, 'switch', '-q', '-c', 'feature/task')
    refusal, note = _verdict(proj)
    assert not refusal and 'feature/task' in note
    assert _verdict(proj) == ('', ''), 'said once, not on every write'


def test_another_session_switching_an_unfinished_branch_is_refused(proj):
    _git(proj, 'switch', '-q', '-c', 'feature/mine')
    (proj / 'b.txt').write_text('x', encoding='utf-8', newline='\n')
    _git(proj, 'add', 'b.txt')
    _git(proj, '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-q', '--no-verify', '-m', 'unfinished')
    _verdict(proj)
    _git(proj, 'switch', '-q', '-c', 'feature/theirs')
    refusal, _ = _verdict(proj)
    assert "'feature/mine' to 'feature/theirs'" in refusal and 'switch feature/theirs' in refusal


def test_leaving_a_finished_branch_is_not_a_drift(proj):
    """Integrated into develop — the close parks HEAD there, and another session moves on."""
    _git(proj, 'switch', '-q', '-c', 'feature/done')
    _verdict(proj)
    _git(proj, 'switch', '-q', '-c', 'feature/next')
    refusal, note = _verdict(proj)
    assert not refusal and 'feature/next' in note


def test_this_session_s_own_switch_is_followed_not_refused(proj):
    _git(proj, 'switch', '-q', '-c', 'feature/mine')
    (proj / 'b.txt').write_text('x', encoding='utf-8', newline='\n')
    _git(proj, 'add', 'b.txt')
    _git(proj, '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-q', '--no-verify', '-m', 'unfinished')
    _verdict(proj)
    _git(proj, 'switch', '-q', '-c', 'feature/other')
    branch_marker.follow(SESSION)
    assert _verdict(proj) == ('', '')


def test_a_repo_outside_git_flow_and_a_detached_head_pass(proj, tmp_path):
    paper = tmp_path / 'academy/paper'
    paper.mkdir(parents=True)
    _git(paper, 'init', '-q', '-b', 'main')
    assert branch_marker.verdict(paper / 'x.tex', SESSION) == ('', '')
    _git(proj, 'switch', '-q', '--detach')
    assert _verdict(proj) == ('', '')


def _gate(payload, off=False):
    env = dict(os.environ)
    if off:
        env['WOS_FEATURES_OFF'] = 'branch-gate'
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload), env=env,
                          capture_output=True, text=True, encoding='utf-8')


def test_the_real_gate_fails_open_and_can_be_switched_off(tmp_path):
    """A payload it cannot use passes; the switch passes even a write it would have refused."""
    write = {'tool_name': 'Write', 'session_id': SESSION,
             'tool_input': {'file_path': str(WORKSPACE_ROOT / 'nowhere/\0bad'), 'content': 'x'}}
    assert _gate(write).returncode == 0
    assert _gate({'tool_name': 'Write', 'tool_input': {'file_path': 'x'}}, off=True).returncode == 0
