# T1 delegate produce: Artifact contracts restrict writes and publish checked changes after retries or escalation.
import hashlib
import pathlib
import subprocess
import sys

import pytest

_TOOLS = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_TOOLS))
sys.path.insert(0, str(_TOOLS / 'delegate'))
import delegation  # noqa: E402
import produce  # noqa: E402
import sandbox  # noqa: E402
import workers  # noqa: E402

CONTRACT = '''---
goal: write an artifact
work: test
role: '-'
write_paths: [artifact.txt]
checks: [test -f artifact.txt]
attempt: 1/2
return: artifact
---
'''
REPLY = 'status: ok\n## Answer\ndone\n## Assumptions\nnone\n## Unverified\nnone\n## Left untouched\nnone\n'


@pytest.fixture(autouse=True)
def _admission_reads_no_machine(monkeypatch, tmp_path):
    """Admission is worker_guard's question, tested in its own file. Here it must not read this
    machine's free memory or its live worker slots: both failed this suite on 2026-11-24 while
    real panel calls ran beside it (2928 MB available, 2 live)."""
    import worker_guard
    monkeypatch.setattr(worker_guard, 'memory', lambda: None)
    monkeypatch.setattr(worker_guard, 'SLOTS', tmp_path / 'slots')


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(produce, 'RUNS', tmp_path / 'delegations.tsv')
    repo = tmp_path / 'repo'
    repo.mkdir()
    subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
    (repo / 'base.txt').write_text('committed\n', encoding='utf-8', newline='\n')
    subprocess.run(['git', 'add', 'base.txt'], cwd=repo, check=True)
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t',
                    '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null',
                    'commit', '-qm', 'base'], cwd=repo, check=True)
    return repo


def _produce(root, caller, contract=CONTRACT):
    return produce.produced(contract, works={'test'}, roles={'-': ''},
                            rows=[{'worker': 'a'}, {'worker': 'b'}], caller=caller, root=root)


def test_outside_accepts_exact_paths_and_directory_prefixes():
    paths = ['artifact.txt', 'dir/x', 'dirx/y', 'artifact.txt.bak']
    assert delegation.outside(paths, ['artifact.txt', 'dir/']) == ['dirx/y', 'artifact.txt.bak']


def test_validate_requires_checks_for_artifacts_and_refuses_writes_for_answers():
    artifact = delegation.parse(CONTRACT)
    with pytest.raises(ValueError, match='artifact needs write_paths and checks'):
        delegation.validate({**artifact, 'checks': []}, {'test'}, {'-'})
    with pytest.raises(ValueError, match='answer is read-only'):
        delegation.validate({**artifact, 'return': 'answer', 'checks': []}, {'test'}, {'-'})
    delegation.validate(artifact, {'test'}, {'-'})


def test_failure_names_the_outside_path_and_exit_code_within_its_limit():
    outside = ['stray.txt']
    command = 'test -f artifact.txt'
    evidence = delegation.failure(outside, [(command, 7, 'missing')], outside, limit=160)
    assert 'stray.txt' in evidence
    assert 'exit 7' in evidence
    assert len(evidence) <= 160
    long_evidence = delegation.failure(outside, [(command, 7, 'x' * 200)], outside, limit=80)
    assert len(long_evidence) <= 80


def test_sandbox_copies_uncommitted_edits_and_lists_modified_created_and_deleted_paths(root):
    (root / 'base.txt').write_text('local edit\n', encoding='utf-8', newline='\n')
    (root / 'deleted.txt').write_text('delete this\n', encoding='utf-8', newline='\n')
    copy = sandbox.make(root)
    try:
        assert (copy / 'base.txt').read_text(encoding='utf-8') == 'local edit\n'
        assert sandbox.changed(copy) == []
        (copy / 'base.txt').write_text('worker edit\n', encoding='utf-8', newline='\n')
        (copy / 'created.txt').write_text('new file\n', encoding='utf-8', newline='\n')
        (copy / 'deleted.txt').unlink()
        assert sandbox.changed(copy) == ['base.txt', 'created.txt', 'deleted.txt']
    finally:
        sandbox.drop(copy)


def test_sandbox_bring_copies_with_a_short_hash_and_applies_deletions(root):
    copy = sandbox.make(root)
    content = b'artifact bytes\n'
    try:
        (copy / 'artifact.txt').write_bytes(content)
        (copy / 'base.txt').unlink()
        brought = dict(sandbox.bring(copy, root, ['artifact.txt', 'base.txt']))
    finally:
        sandbox.drop(copy)
    assert (root / 'artifact.txt').read_bytes() == content
    assert not (root / 'base.txt').exists()
    assert brought == {'artifact.txt': hashlib.sha256(content).hexdigest()[:12], 'base.txt': 'deleted'}


def test_produced_publishes_the_checked_file_and_reports_without_its_contents(root):
    content = 'file contents that should stay on disk\n'

    def caller(worker, prompt, role, *, cwd, write, judge):
        assert (worker, role, write) == ('a', '-', True)
        assert judge(REPLY) == '-'
        (pathlib.Path(cwd) / 'artifact.txt').write_text(content, encoding='utf-8', newline='\n')
        return workers.Result(worker, 'm', 'ok', REPLY, 0.1)

    status, report = _produce(root, caller)
    assert status == 'ok'
    assert (root / 'artifact.txt').read_text(encoding='utf-8') == content
    assert '\nwrote artifact.txt ' in report
    assert '\ncheck passed: test -f artifact.txt\n' in report
    assert content.strip() not in report


def test_produced_retries_with_the_outside_path_and_publishes_only_the_allowed_file(root):
    calls = []

    def caller(worker, prompt, role, *, cwd, write, judge):
        calls.append((worker, prompt))
        stray = pathlib.Path(cwd) / 'stray.txt'
        artifact = pathlib.Path(cwd) / 'artifact.txt'
        if len(calls) == 1:
            stray.write_text('outside the contract\n', encoding='utf-8', newline='\n')
            artifact.write_text('first try\n', encoding='utf-8', newline='\n')
        else:
            assert not (root / 'stray.txt').exists()
            stray.unlink(missing_ok=True)
            artifact.write_text('second try\n', encoding='utf-8', newline='\n')
        return workers.Result(worker, 'm', 'ok', REPLY, 0.1)

    status, report = _produce(root, caller)
    assert status == 'ok'
    assert [worker for worker, _ in calls] == ['a', 'a']
    assert 'stray.txt' in delegation.sections(calls[1][1])['Last Failure']
    assert 'a: ok on try 2' in report
    assert (root / 'artifact.txt').read_text(encoding='utf-8') == 'second try\n'
    assert not (root / 'stray.txt').exists()


def test_produced_escalates_after_quota_and_reports_both_routes(root):
    def caller(worker, prompt, role, *, cwd, write, judge):
        if worker == 'a':
            return workers.Result(worker, 'm', 'quota', 'quota reached', 0.1)
        (pathlib.Path(cwd) / 'artifact.txt').write_text('from b\n', encoding='utf-8', newline='\n')
        return workers.Result(worker, 'm', 'ok', REPLY, 0.1)

    status, report = _produce(root, caller)
    assert status == 'ok'
    assert (root / 'artifact.txt').read_text(encoding='utf-8') == 'from b\n'
    assert '\nroute: a: quota → b: ok on try 1\n' in report


def test_produced_keeps_the_root_unchanged_and_appends_one_row_when_every_check_fails(root):
    previous = '2026-11-26T00:00\ttest\tok\ta: ok on try 1\t0\t1\tprevious run'
    produce.RUNS.write_text(previous + '\n', encoding='utf-8', newline='\n')
    asked = []

    def caller(worker, prompt, role, *, cwd, write, judge):
        asked.append(worker)
        (pathlib.Path(cwd) / 'artifact.txt').write_text('unverified artifact\n', encoding='utf-8', newline='\n')
        return workers.Result(worker, 'm', 'ok', REPLY, 0.1)

    contract = CONTRACT.replace('test -f artifact.txt', 'test -f missing.txt')
    status, report = _produce(root, caller, contract)
    assert status == 'fail'
    assert asked == ['a', 'a', 'b', 'b']
    assert 'check failed (exit 1): test -f missing.txt' in delegation.sections(report)['Last Failure']
    assert subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=root) == b''
    kept, added = produce.RUNS.read_text(encoding='utf-8').splitlines()
    assert kept == previous
    assert added.split('\t')[1:3] == ['test', 'fail']
