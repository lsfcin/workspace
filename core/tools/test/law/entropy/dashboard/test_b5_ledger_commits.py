# B5 regression — the ledger the scatter writes is committed by the scatter.
# 26 nested repos carried untracked ISSUES.md ledgers nobody ever committed: invisible to clones,
# to history, and to anyone who did not run the dashboard locally — so the findings were addressed
# to readers who cannot see them. The writer owns its artifact now: write_local commits the ledger
# with a PATHSPEC commit (whatever else is staged in that repo stays staged), and steps aside for
# a repo mid-operation. The commit carries --no-verify because the ledger is generated content —
# the parent's own generated.txt exempts generated files from authoring rules, and a gate blocking
# a generated report would re-create the uncommitted-ledger state it exists to kill.
import os
import subprocess

from entropy_report import SECTIONS
from entropy_scatter import scatter


def _workspace(tmp_path):
    ws = tmp_path / 'ws'
    (ws / 'code/proj').mkdir(parents=True)
    repo = ws / 'code/proj'
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    (repo / 'file.py').write_text('x = 1\n', encoding='utf-8')
    env = {**os.environ, 'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t',
           'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}
    subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(repo), 'commit', '-qm', 'init', '--no-verify'],
                   check=True, env=env)
    return ws, repo


def _findings():
    findings = {key: [] for key, _, _ in SECTIONS}
    findings['size'] = ['code/proj/file.py — 3 line(s) over the cap']
    return findings


FILES = ['code/proj/file.py']


def _git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)


def test_the_ledger_the_scatter_writes_gets_committed(tmp_path):
    ws, repo = _workspace(tmp_path)
    mine, counts = scatter(_findings(), ws, FILES)
    assert counts['code/proj'] == 1
    assert 'entropy ledger' in _git(repo, 'log', '--oneline', '--', 'ISSUES.md').stdout
    assert _git(repo, 'status', '--porcelain').stdout == '', 'the ledger was left dirty'


def test_an_unchanged_ledger_is_not_committed_again(tmp_path):
    ws, repo = _workspace(tmp_path)
    scatter(_findings(), ws, FILES)
    first = _git(repo, 'rev-list', '--count', 'HEAD').stdout.strip()
    scatter(_findings(), ws, FILES)
    assert _git(repo, 'rev-list', '--count', 'HEAD').stdout.strip() == first


def test_a_repo_mid_operation_is_left_alone(tmp_path):
    ws, repo = _workspace(tmp_path)
    (repo / '.git' / 'MERGE_HEAD').write_text('x', encoding='utf-8')
    scatter(_findings(), ws, FILES)
    assert 'ISSUES.md' in _git(repo, 'status', '--porcelain').stdout, 'the ledger must be written'
    assert _git(repo, 'log', '--oneline', '--', 'ISSUES.md').stdout == '', 'mid-operation repo committed'


def test_staged_work_in_the_repo_stays_staged(tmp_path):
    ws, repo = _workspace(tmp_path)
    (repo / 'wip.py').write_text('y = 2\n', encoding='utf-8')
    _git(repo, 'add', 'wip.py')
    scatter(_findings(), ws, FILES)
    assert 'wip.py' in _git(repo, 'status', '--porcelain').stdout, 'the pathspec commit ate staged work'
    assert 'entropy ledger' in _git(repo, 'log', '--oneline', '--', 'ISSUES.md').stdout
