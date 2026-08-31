# B12 regression — core/run runs what it says it runs.
# The launcher's own first line promises "the one command that runs anything in core/", but it
# exec'd every target with the venv interpreter, so the two bash tools died with
# `SyntaxError: unmatched ')'`. It now dispatches on the shebang (ruled 2026-08-31, Lucas:
# add capabilities, never exceptions). This spec holds both arms: a bash target runs as bash,
# and a python target still reaches the interpreter.
import subprocess

from conftest import WORKSPACE_ROOT


def _run(target, *args):
    return subprocess.run(['bash', str(WORKSPACE_ROOT / 'core/run'), target, *args],
                          cwd=WORKSPACE_ROOT, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=180)


def test_a_bash_target_runs_as_bash():
    out = _run('tools/wos/sync-skills', '--check')
    assert out.returncode == 0, out.stdout + out.stderr
    assert 'SyntaxError' not in out.stderr


def test_a_python_target_still_reaches_the_interpreter():
    out = _run('tools/wos/size')
    assert out.returncode == 0, out.stderr
    assert '.md files' in out.stdout
