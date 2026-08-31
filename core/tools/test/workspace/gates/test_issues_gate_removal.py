# Regression — the issues gate reads removals, not only FIXED flips.
# A session deleted four fixed bug sections and one OPEN one from the workspace ISSUES.md; the
# gate only fired on the literal word FIXED, so an open bug (B4) left the ledger without a fix or
# a spec. Since 2026-08-31 a section may not leave ISSUES.md — by deletion or by a FIXED flip —
# without a matching regression spec, and a spec for B19 does not pay B1's debt: the id ends at
# the name boundary.
import json
import subprocess
import sys

from conftest import WORKSPACE_ROOT

GATE = WORKSPACE_ROOT / 'core/hooks/checks/issues-gate.py'
SECTION = '## B7 — a bug\n\n**Symptom:** x.\n'
B1_SECTION = '## B1 — another bug\n\n**Symptom:** y.\n'


def _repo(tmp_path, body):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    issues = tmp_path / 'ISSUES.md'
    issues.write_text(f'# Workspace issues\n\n{body}', encoding='utf-8')
    return issues


def _edit(tmp_path, issues, old, new):
    payload = {'session_id': 'test-issues-gate', 'cwd': str(WORKSPACE_ROOT), 'tool_name': 'Edit',
               'tool_input': {'file_path': str(issues), 'old_string': old, 'new_string': new}}
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180)


def test_deleting_an_open_bug_without_a_spec_blocks(tmp_path):
    issues = _repo(tmp_path, SECTION)
    out = _edit(tmp_path, issues, old=SECTION, new='')
    assert out.returncode == 2, out.stdout + out.stderr
    assert 'B7' in out.stderr


def test_deleting_with_a_spec_passes(tmp_path):
    issues = _repo(tmp_path, SECTION)
    testdir = tmp_path / 'test'
    testdir.mkdir()
    (testdir / 'b7-the-bug-is-gone.py').write_text('def test_it():\n    assert True\n', encoding='utf-8')
    out = _edit(tmp_path, issues, old=SECTION, new='')
    assert out.returncode == 0, out.stderr


def test_a_b19_spec_does_not_pay_b1s_debt(tmp_path):
    issues = _repo(tmp_path, B1_SECTION)
    testdir = tmp_path / 'test'
    testdir.mkdir()
    (testdir / 'b19-some-other-bug.py').write_text('def test_it():\n    assert True\n', encoding='utf-8')
    out = _edit(tmp_path, issues, old=B1_SECTION, new='')
    assert out.returncode == 2, out.stdout + out.stderr
    assert 'B1' in out.stderr
