# T1 delegate/ask: a spent quota or a broken call falls to the next model, the first verdict wins, none at all stops with every reason, and a debate never gives two roles to one vendor. Models faked.
import importlib.machinery
import importlib.util
import pathlib
import sys

import pytest

_TOOLS = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_TOOLS))
import workers  # noqa: E402

CODEX_LIMIT = "ERROR: You've hit your usage limit. Upgrade to Pro or try again at 4:31 PM."
AGY_QUOTA = 'Error: Individual quota reached. Resets in 73h6m3s.\nAGY_ERROR: {"status":"RESOURCE_EXHAUSTED"}'


@pytest.fixture(autouse=True)
def _admission_reads_no_machine(monkeypatch, tmp_path):
    """Admission is worker_guard's question, tested in its own file. Here it must not read this
    machine's free memory or its live worker slots: both failed this suite on 2026-11-24 while
    real panel calls ran beside it (2928 MB available, 2 live)."""
    import worker_guard
    monkeypatch.setattr(worker_guard, 'memory', lambda: None)
    monkeypatch.setattr(worker_guard, 'SLOTS', tmp_path / 'slots')


def _tool():
    path = _TOOLS / 'delegate' / 'ask'
    loader = importlib.machinery.SourceFileLoader('panel_ask', str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader('panel_ask', loader))
    loader.exec_module(module)
    return module


def _rows(*pairs):
    return [{'worker': w, 'vendor': v} for w, v in pairs]


def _caller(answers: dict):
    """A fake workers.call: worker -> (exit code, text), classified by the real classifier."""
    asked = []

    def call(worker, prompt, role='-'):
        asked.append((worker, role))
        code, text = answers[worker]
        return workers.Result(worker, 'm', workers.classify(code, text), text, 0.1)
    call.asked = asked
    return call


def test_a_spent_quota_falls_to_the_next_model_and_names_the_one_that_answered():
    rows = _rows(('codex', 'openai'), ('argon', 'google'), ('deepseek', 'deepseek'))
    caller = _caller({'codex': (1, CODEX_LIMIT), 'argon': (0, AGY_QUOTA), 'deepseek': (0, 'Verdict: 9/10')})
    r, _, misses = _tool().ask('q', rows, caller)
    assert (r.worker, r.text) == ('deepseek', 'Verdict: 9/10')
    assert [m.split(':')[0] for m in misses] == ['codex', 'argon']
    assert all(': quota:' in m for m in misses)


def test_a_broken_call_is_unknown_or_missing_never_quota():
    assert workers.classify(127, 'codex not found') == 'missing'
    assert workers.classify(1, 'Unexpected server error') == 'unknown'
    assert workers.classify(124, 'timed out after 900 s') == 'timeout'


def test_no_model_answering_stops_with_every_reason():
    rows = _rows(('codex', 'openai'), ('flash', 'google'))
    with pytest.raises(SystemExit, match='(?s)codex: quota.*flash: unknown'):
        _tool().ask('q', rows, _caller({'codex': (1, CODEX_LIMIT), 'flash': (0, '')}))


def test_a_debate_gives_each_role_to_a_different_vendor():
    rows = _rows(('argon', 'google'), ('flash', 'google'), ('deepseek', 'deepseek'), ('codex', 'openai'))
    caller = _caller({w: (0, f'{w} says') for w in ('argon', 'flash', 'deepseek', 'codex')})
    who, text = _tool().debate('q', rows, caller)
    assert caller.asked == [('argon', 'advocate'), ('deepseek', 'opponent'), ('codex', 'mediator')]
    assert who == 'debate: google, deepseek, openai' and 'flash' not in text


def test_a_binary_off_path_is_found_where_the_vendor_installs_it(tmp_path, monkeypatch):
    exe = tmp_path / 'codex'
    exe.write_text('#!/bin/sh\n', encoding='utf-8', newline='\n')
    exe.chmod(0o755)
    monkeypatch.delenv('CODEX', raising=False)
    monkeypatch.setattr(workers.shutil, 'which', lambda name: None)
    monkeypatch.setitem(workers.PLACES, 'codex', ('CODEX', (str(exe),)))
    assert workers.find('codex') == str(exe)
    monkeypatch.setitem(workers.PLACES, 'codex', ('CODEX', (str(tmp_path / 'missing'),)))
    assert workers.find('codex') is None


def test_a_worker_whose_id_the_harness_stopped_offering_is_not_live(tmp_path, monkeypatch):
    # glm, 2026-11-23: the binary answered --help while its id had left `opencode models`.
    exe = tmp_path / 'opencode'
    exe.write_text('#!/bin/sh\n[ "$1" = models ] && printf "opencode/kept-free\\nother/x\\n"\nexit 0\n',
                   encoding='utf-8', newline='\n')
    exe.chmod(0o755)
    monkeypatch.setenv('OPENCODE', str(exe))
    row = lambda i: {'harness': 'opencode', 'id': i}  # noqa: E731
    offers = {}
    assert workers.live(row('opencode/kept-free'), offers) == 'ok'
    assert workers.live(row('opencode/gone-free'), offers) == 'opencode/gone-free no longer offered'
    assert offers == {'opencode': {'opencode/kept-free', 'other/x'}}
    codex = tmp_path / 'codex'  # a harness that cannot say what it offers is proven by --help alone
    codex.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8', newline='\n')
    codex.chmod(0o755)
    monkeypatch.setenv('CODEX', str(codex))
    monkeypatch.setenv('CODEX_HOME', str(tmp_path / 'no-home'))
    assert workers.live({'harness': 'codex', 'id': 'anything'}) == 'ok'


def test_codex_offers_the_union_of_its_binary_catalog_and_its_account_cache(tmp_path, monkeypatch):
    # 2026-11-23: `debug models` had gpt-5.5 and not gpt-6.2-sol; the account cache the reverse.
    exe = tmp_path / 'codex'
    exe.write_text('#!/bin/sh\n[ "$1" = debug ] && printf \'{"models":[{"slug":"built-in"}]}\\nWARN noise\\n\'\nexit 0\n',
                   encoding='utf-8', newline='\n')
    exe.chmod(0o755)
    (tmp_path / 'models_cache.json').write_text('{"models":[{"slug":"sent","visibility":"hide"}]}',
                                                encoding='utf-8', newline='\n')
    monkeypatch.setenv('CODEX', str(exe))
    monkeypatch.setenv('CODEX_HOME', str(tmp_path))
    assert workers.offered('codex') == {'built-in', 'sent'}
    assert workers.live({'harness': 'codex', 'id': 'gone'}) == 'gone no longer offered'


def test_every_declared_worker_has_a_model_id_and_the_chain_is_ordered():
    assert all(r['id'] and r['id'] != '-' for r in workers.catalog())
    positions = [int(r['chain']) for r in workers.chain()]
    assert positions == sorted(positions) and len(set(positions)) == len(positions)


def test_a_timeout_kills_the_whole_process_group():
    code, text = workers.run(['sh', '-c', 'sleep 30 & sleep 30'], timeout=1)
    assert code == 124 and 'timed out' in text


def _log(tmp_path, monkeypatch, rows):
    log = tmp_path / 'workers.tsv'
    log.write_text(''.join('\t'.join(r) + '\n' for r in rows), encoding='utf-8', newline='\n')
    monkeypatch.setattr(workers, 'LOG', log)
    return log


def test_a_deadline_is_three_p90s_of_the_ok_calls_bounded_and_the_ceiling_under_five(tmp_path, monkeypatch):
    ok = lambda w, s: ['2026-11-20T10:00', w, 'm', '-', 'ok', str(s), '']  # noqa: E731
    _log(tmp_path, monkeypatch, [ok('fast', 10)] * 9 + [ok('fast', 20)] + [ok('slow', 400)] * 6
         + [ok('few', 5)] * 4 + [['2026-11-20T10:00', 'fast', 'm', '-', 'timeout', '900', 'x', 'timeout']])
    assert workers.deadline('fast') == 120          # 3 × p90 = 3 × ~20 < floor
    assert workers.deadline('slow') == 900          # 3 × 400 > ceiling
    assert workers.deadline('few') == 900           # under 5 ok calls: the ceiling
    assert workers.deadline('never') == 900


def test_the_deadline_reaches_every_adapter(monkeypatch):
    seen = []
    monkeypatch.setattr(workers, 'run', lambda cmd, cwd=None, timeout=0: seen.append(timeout) or (0, 'x' * 500))
    for name, adapter in workers.ADAPTERS.items():
        adapter('/bin/true', 'm', 'q', '/tmp', 7)
    assert seen == [7] * len(workers.ADAPTERS)


def test_a_hung_worker_ends_at_its_deadline(tmp_path, monkeypatch):
    _log(tmp_path, monkeypatch, [])
    monkeypatch.setattr(workers, 'catalog', lambda: [{'worker': 'hung', 'harness': 'fake', 'id': 'm'}])
    monkeypatch.setattr(workers, 'find', lambda h: '/bin/sh')
    monkeypatch.setattr(workers, 'deadline', lambda w: 1)
    monkeypatch.setitem(workers.ADAPTERS, 'fake',
                        lambda exe, model, prompt, cwd, timeout: workers.run([exe, '-c', 'sleep 30'], timeout=timeout))
    r = workers.call('hung', 'q')
    assert r.status == 'timeout' and r.seconds < 10


def test_a_debate_keeps_the_answers_it_got_and_names_the_role_that_was_missing():
    rows = _rows(('argon', 'google'), ('deepseek', 'deepseek'))
    caller = _caller({'argon': (0, 'argon says'), 'deepseek': (124, 'timed out after 900 s')})
    who, text = _tool().debate('q', rows, caller)
    assert 'argon says' in text and 'missing: opponent, mediator' in who
    assert 'deepseek: timeout' in text


def test_every_log_line_carries_a_check_derived_from_its_status_and_old_lines_still_count(tmp_path, monkeypatch):
    log = _log(tmp_path, monkeypatch, [['2026-11-20T10:00', 'a', 'm', '-', 'ok', '3.0', '']])  # a 7-column line
    for status in ('ok', 'timeout', 'quota', 'unknown'):
        workers.record(workers.Result('a', 'm', status, 'x' * 500 if status == 'ok' else 'why', 1.0))
    lines = [l.split('\t') for l in log.read_text(encoding='utf-8').splitlines()]
    assert [l[7] for l in lines[1:]] == ['-', 'timeout', 'infra', 'infra']
    assert workers.tally()['a'][0] == 5
    workers.record(workers.Result('a', 'm', 'ok', '', 1.0))
    workers.record(workers.Result('a', 'm', 'ok', 'free text', 1.0), check='bad-format')
    assert [l.split('\t')[7] for l in log.read_text(encoding='utf-8').splitlines()[-2:]] == ['empty', 'bad-format']
    assert workers.cooling('a', '2026-11-20T10:05') == ''


CONTRACT = '---\ngoal: say whether the plan holds\nwork: review\nrole: critic\nread_paths: [{path}]\nreturn: answer\n---\n## Context\nA plan.\n'
FORMATTED = ('status: ok\n## Answer\n' + 'It holds. ' * 1000 + '\n## Assumptions\n- the tests pass\n'
             '## Unverified\nnone\n## Left untouched\nnone\n')


def _judging(answer):
    """A fake workers.call that, like the real one, runs the judge on an ok answer."""
    seen = []

    def call(worker, prompt, role='-', judge=None):
        seen.append((worker, role, prompt, judge(answer) if judge else ''))
        return workers.Result(worker, 'm', 'ok', answer, 0.1)
    call.seen = seen
    return call


def test_a_contract_goes_to_the_worker_framed_and_comes_back_cut_with_the_full_answer_kept(tmp_path, monkeypatch):
    (tmp_path / 'plan.md').write_text('step one', encoding='utf-8', newline='\n')
    caller, out = _judging(FORMATTED), tmp_path / 'full.md'
    who, text, full = _tool().delegated(CONTRACT.format(path='plan.md'), _rows(('argon', 'google')), str(out), caller, tmp_path)
    worker, role, prompt, check = caller.seen[0]
    assert (worker, role, check) == ('argon', 'critic', '-')
    assert prompt.startswith(_tool().ROLES['critic']) and '### plan.md\nstep one' in prompt
    assert full == out and out.read_text(encoding='utf-8') == FORMATTED + '\n'
    assert 'review needed' in text and '- the tests pass' in text and str(out) in text and len(text) < len(FORMATTED)


def test_a_free_text_answer_to_a_contract_is_logged_bad_format(tmp_path, monkeypatch):
    (tmp_path / 'plan.md').write_text('x', encoding='utf-8', newline='\n')
    caller = _judging('Looks fine to me. ' * 40)
    _, text, _ = _tool().delegated(CONTRACT.format(path='plan.md'), _rows(('argon', 'google')), str(tmp_path / 'o.md'), caller, tmp_path)
    assert caller.seen[0][3] == 'bad-format' and 'check bad-format' in text


def test_context_over_budget_goes_only_to_a_worker_that_reads_files_else_blocked(tmp_path, monkeypatch):
    (tmp_path / 'big.md').write_text('x' * 20000, encoding='utf-8', newline='\n')
    rows = [{'worker': 'ollama', 'vendor': 'meta', 'tools': 'text'}, {'worker': 'codex', 'vendor': 'openai', 'tools': 'tools'}]
    caller = _judging(FORMATTED)
    _tool().delegated(CONTRACT.format(path='big.md'), rows, str(tmp_path / 'o.md'), caller, tmp_path)
    assert [s[0] for s in caller.seen] == ['codex'] and 'big.md' in caller.seen[0][2] and 'x' * 100 not in caller.seen[0][2]
    with pytest.raises(SystemExit, match='status: blocked'):
        _tool().delegated(CONTRACT.format(path='big.md'), rows[:1], str(tmp_path / 'o.md'), caller, tmp_path)
