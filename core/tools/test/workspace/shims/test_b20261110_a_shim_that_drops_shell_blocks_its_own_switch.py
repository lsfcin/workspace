# b20261110 regression: a session's own git switch reaches the branch gate through every shim.
#
# Copilot and Antigravity forwarded only file paths after a tool ran, so a session's own
# `git switch` never re-recorded its branch marker and its next write was refused as a parallel
# session's switch. Each case runs the real shim over a scratch workspace whose gate table holds
# only the branch-gate rows: an own switch must pass, a foreign one must still block.
import json
import os
import shutil
import subprocess
import sys

import pytest
from conftest import WORKSPACE_ROOT

ROWS = 'pre\twrite\t15\tgit/branch-gate.py\tblocks\tbranch-gate\n' \
       'post\tshell\t10\tgit/branch-gate.py\tinforms\tbranch-gate\n'


def git(root, *args):
    subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)


@pytest.fixture
def workspace(tmp_path):
    shutil.copytree(WORKSPACE_ROOT / 'core/hooks', tmp_path / 'core/hooks',
                    ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('features.txt', 'profile.txt', 'run'):
        shutil.copyfile(WORKSPACE_ROOT / 'core' / name, tmp_path / 'core' / name)
    (tmp_path / 'gates.txt').write_text(ROWS, encoding='utf-8', newline='\n')
    (tmp_path / '.gitignore').write_text('core/\ngates.txt\n.gitignore\n', encoding='utf-8', newline='\n')
    git(tmp_path, 'init', '-q', '-b', 'develop')
    git(tmp_path, '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-q', '--allow-empty', '-m', 'root')
    for branch in ('feature/a', 'feature/b'):
        git(tmp_path, 'switch', '-q', '-c', branch, 'develop')
        git(tmp_path, '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-q', '--allow-empty', '-m', branch)
    git(tmp_path, 'switch', '-q', 'feature/a')
    return tmp_path


def antigravity(root, event, call):
    payload = {'conversationId': 'ag-test', 'toolCall': call}
    return _run(root, ['core/hooks/antigravity/antigravity_policy.py', event], payload)


def copilot(root, event, tool_input):
    script = 'copilot-pre-tool.py' if event == 'PreToolUse' else 'copilot-post-tool.py'
    payload = {'cwd': str(root), 'tool_name': 'edit', 'tool_input': tool_input}
    return _run(root, [f'core/hooks/copilot/{script}'], payload)


def _run(root, argv, payload):
    env = dict(os.environ, WOS_GATES_TABLE=str(root / 'gates.txt'))
    for name in ('CLAUDE_TOOL_INPUT', 'CLAUDE_TOOL_NAME', 'WOS_FEATURES_OFF'):
        env.pop(name, None)
    return subprocess.run([sys.executable, str(root / argv[0]), *argv[1:]], input=json.dumps(payload),
                          capture_output=True, text=True, cwd=str(root), env=env, encoding='utf-8')


def claude(root, event, tool, tool_input):
    payload = {'session_id': 'cc-test', 'hook_event_name': event, 'tool_name': tool,
               'tool_input': tool_input}
    return _run(root, ['core/hooks/dispatch.py'], payload)


def blocked(done):
    return done.returncode == 2 or '"deny"' in done.stdout


SHIMS = {
    'antigravity': (
        lambda root, path: antigravity(root, 'PreToolUse', {
            'name': 'write_to_file', 'args': {'TargetFile': str(path), 'CodeContent': '# x\n'}}),
        lambda root, cmd: antigravity(root, 'PostToolUse', {
            'name': 'run_command', 'args': {'CommandLine': cmd}})),
    'copilot': (
        lambda root, path: copilot(root, 'PreToolUse', {'filePath': str(path), 'content': '# x\n'}),
        lambda root, cmd: copilot(root, 'PostToolUse', {'command': cmd})),
    # The dispatcher itself, as Claude Code calls it: the gate once died importing pre_commit there.
    'claude': (
        lambda root, path: claude(root, 'PreToolUse', 'Write', {'file_path': str(path), 'content': '# x\n'}),
        lambda root, cmd: claude(root, 'PostToolUse', 'Bash', {'command': cmd})),
}


@pytest.mark.parametrize('shim', sorted(SHIMS))
def test_own_switch_never_blocks_the_next_write(workspace, shim):
    write, after_shell = SHIMS[shim]
    target = workspace / 'notes.md'
    assert not blocked(write(workspace, target))
    git(workspace, 'switch', '-q', 'feature/b')
    after_shell(workspace, 'git switch feature/b')
    done = write(workspace, target)
    assert not blocked(done), done.stdout + done.stderr


@pytest.mark.parametrize('shim', sorted(SHIMS))
def test_foreign_switch_still_blocks(workspace, shim):
    write, _ = SHIMS[shim]
    target = workspace / 'notes.md'
    assert not blocked(write(workspace, target))
    git(workspace, 'switch', '-q', 'feature/b')
    done = write(workspace, target)
    assert blocked(done), done.stdout + done.stderr


def test_first_write_names_pre_existing_changes(workspace):
    """Lucas 2026-11-10: whose-work-is-this is asked at the first write, not only at roundup."""
    (workspace / 'left.md').write_text('# someone else\n', encoding='utf-8', newline='\n')
    write, _ = SHIMS['claude']
    done = write(workspace, workspace / 'notes.md')
    assert not blocked(done)
    assert 'pre-existing' in done.stdout, done.stdout + done.stderr
