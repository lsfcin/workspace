# One latest handoff per repository/environment; an older session cannot clear its replacement.
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest
from conftest import WORKSPACE_ROOT

_spec = importlib.util.spec_from_file_location('handoff_names', WORKSPACE_ROOT / 'core/tools/wos/close/handoff.py')
handoff = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(handoff)


def repo(path):
    path.mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(path)], check=True)
    return path


def log(path, rows):
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8', newline='\n')
    return path


def patch(call, name, lines, success=True):
    return [
        {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'name': 'apply_patch',
         'call_id': call, 'input': f'*** Begin Patch\n*** Update File: {name}\n@@\n{lines}\n*** End Patch'}},
        {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output', 'call_id': call,
         'output': 'Success. Updated the following files:' if success else 'patch verification failed'}},
    ]


def test_same_pair_shares_latest_handoff_and_old_session_cannot_clear_it(tmp_path):
    root = repo(tmp_path / 'workspace')
    a = handoff.choose(root, root, 'same-prefix-session-a', 'chatgpt', None)
    b = handoff.choose(root, root, 'same-prefix-session-b', 'chatgpt', None)
    assert a['path'] == b['path'] == str(root / 'outputs/handoff-workspace-chatgpt.md')
    handoff.publish(a, 'first\n')
    handoff.publish(b, 'second\n')
    handoff.publish(a, None)
    assert Path(b['path']).read_text(encoding='utf-8').endswith('second\n')
    handoff.publish(b, None)
    assert not Path(b['path']).exists()


def test_different_environments_and_repositories_have_distinct_paths(tmp_path):
    root = repo(tmp_path / 'workspace')
    nested = repo(root / 'code/project')
    a = handoff.choose(root, root, 's', 'chatgpt', None)
    b = handoff.choose(root, root, 's', 'claude', None)
    c = handoff.choose(root, nested, 's', 'chatgpt', None)
    assert len({a['path'], b['path'], c['path']}) == 3
    assert c['path'] == str(root / 'outputs/handoff-project-chatgpt.md')


def test_ranking_counts_only_successful_session_edits(tmp_path):
    root = repo(tmp_path / 'workspace')
    nested = repo(root / 'code' / 'project')
    (root / 'unrelated-dirty.md').write_text('other session\n' * 1000, encoding='utf-8', newline='\n')
    rows = patch('a', str(root / 'one.md'), '-old\n+new')
    rows += patch('b', str(nested / 'two.md'), '+one\n+two\n+three')
    rows += patch('failed', str(root / 'bad.md'), '+ignored\n' * 100, False)
    rows += patch('output', str(root / 'outputs' / 'old.md'), '+ignored\n' * 100)
    info = handoff.choose(root, root, 's', 'chatgpt', log(tmp_path / 'log.jsonl', rows))
    assert info['repository'] == str(nested)
    assert info['lines'] == {str(root): 2, str(nested): 3}


def test_claude_errors_and_sidechains_are_excluded(tmp_path):
    root = repo(tmp_path / 'workspace')
    def use(identifier, side=False):
        return {'type': 'assistant', 'sessionId': 's', 'isSidechain': side, 'message': {'content': [
            {'type': 'tool_use', 'id': identifier, 'name': 'Edit', 'input': {
             'file_path': str(root / 'one.md'), 'old_string': 'one\ntwo', 'new_string': 'three'}}]}}
    def result(identifier, error=False):
        return {'type': 'user', 'message': {'content': [
            {'type': 'tool_result', 'tool_use_id': identifier, 'is_error': error}]}}
    path = log(tmp_path / 'claude.jsonl', [use('ok'), result('ok'), use('bad'), result('bad', True),
                                         use('child', True), result('child')])
    assert handoff.edits(path, root) == {str(root / 'one.md'): 3}
    assert handoff.transcript('s', 'claude', root, str(path)) == path
    with pytest.raises(ValueError, match='does not identify'):
        handoff.transcript('other', 'claude', root, str(path))


def test_no_recorded_edits_falls_back_without_inspecting_dirty_diff(tmp_path):
    root = repo(tmp_path / 'workspace')
    info = handoff.choose(root, root, 's', 'chatgpt', None)
    assert info['basis'] == 'working repository fallback'
    assert info['lines'] == {}


def test_identity_is_not_guessed_from_latest_session(monkeypatch):
    for key in ('CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_SESSION_ID'):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ValueError, match='No session identity'):
        handoff.identity()
    monkeypatch.setenv('CODEX_THREAD_ID', 'current-session')
    assert handoff.identity() == ('current-session', 'chatgpt')


def test_name_follows_the_selected_repository_without_session_suffix(tmp_path):
    root = repo(tmp_path / 'workspace')
    nested = repo(root / 'code' / 'project')
    first = handoff.choose(root, root, 's', 'chatgpt', None)
    handoff.publish(first, 'resume\n')
    path = log(tmp_path / 'log.jsonl', patch('ok', str(nested / 'one.md'), '+edited'))
    second = handoff.choose(root, root, 's', 'chatgpt', path)
    assert second['path'] != first['path']
    assert second['path'] == str(root / 'outputs/handoff-project-chatgpt.md')


def test_lock_refuses_concurrent_publication_and_clear_preserves_unknown_owner(tmp_path):
    root = repo(tmp_path / 'workspace')
    info = handoff.choose(root, root, 's', 'chatgpt', None)
    path = Path(info['path'])
    path.parent.mkdir()
    path.write_text('foreign handoff\n', encoding='utf-8', newline='\n')
    handoff.publish(info, None)
    assert path.read_text(encoding='utf-8') == 'foreign handoff\n'
    lock = path.with_suffix('.lock')
    lock.touch()
    with pytest.raises(FileExistsError):
        handoff.publish(info, 'replacement\n')
    assert lock.exists()
    lock.unlink()
    handoff.publish(info, 'replacement\n')
    assert path.read_text(encoding='utf-8').endswith('replacement\n')
