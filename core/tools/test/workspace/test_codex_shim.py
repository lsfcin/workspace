# Codex shim tests: project config stays relocatable and apply_patch reaches canonical gates.
import json
import subprocess
import sys

from conftest import WORKSPACE_ROOT

sys.path.insert(0, str(WORKSPACE_ROOT / 'core/hooks/codex'))
import codex_policy


def test_project_hook_config_is_relocatable_and_valid_json():
    path = WORKSPACE_ROOT / '.codex/hooks.json'
    config = json.loads(path.read_text())
    commands = [handler['command'] for groups in config['hooks'].values() for group in groups
                for handler in group['hooks']]
    assert commands
    assert all('/mnt/workspace' not in command for command in commands)
    assert all('git rev-parse --show-toplevel' in command for command in commands)


def test_apply_patch_payloads_preserve_paths_content_and_deltas():
    data = {
        'cwd': str(WORKSPACE_ROOT),
        'session_id': 'shim-test',
        'tool_input': {'command': '''*** Begin Patch
*** Add File: tmp/new.py
+# New file
+value = 1
*** Update File: core/features.txt
-old
+new
*** End Patch'''},
    }
    payloads = codex_policy.patches(data)
    assert payloads[0] == ('Write', {'file_path': str(WORKSPACE_ROOT / 'tmp/new.py'),
                                     'session_id': 'shim-test',
                                     'content': '# New file\nvalue = 1'})
    assert payloads[1] == ('Edit', {'file_path': str(WORKSPACE_ROOT / 'core/features.txt'),
                                    'session_id': 'shim-test', 'old_string': 'old',
                                    'new_string': 'new'})


def test_codex_feature_switch_disables_the_adapter():
    result = subprocess.run(
        ['python3', str(WORKSPACE_ROOT / 'core/hooks/codex/codex-policy.py')], input='{}', text=True,
        capture_output=True, cwd=WORKSPACE_ROOT,
        env={'WOS_FEATURES_OFF': 'codex-hooks'}, check=False,
    )
    assert result.returncode == 0
    assert result.stdout == result.stderr == ''
