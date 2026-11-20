# b20261120-handoff-no-amend regression: a session amends its own handoff section by writing it again, and no other session's section moves.
import importlib.util
import subprocess

from conftest import WORKSPACE_ROOT

_spec = importlib.util.spec_from_file_location('handoff_names', WORKSPACE_ROOT / 'core/tools/wos/close/handoff.py')
handoff = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(handoff)


def test_a_session_rewriting_its_handoff_replaces_only_its_own_section(tmp_path):
    root = tmp_path / 'workspace'
    root.mkdir()
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    path = handoff.path_for(root, 'workspace')
    handoff.write(path, 'claude', 'a', 'draft\n')
    handoff.write(path, 'chatgpt', 'b', 'theirs\n')
    handoff.write(path, 'claude', 'a', 'final\n')
    text = path.read_text(encoding='utf-8')
    assert 'draft' not in text and text.index('theirs') < text.index('final')
