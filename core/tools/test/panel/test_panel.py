# T1 panel/ask: a spent quota or a broken call falls to the next model, the first verdict wins, none at all stops with every reason, and a debate never gives two roles to one vendor. Models faked.
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


def _tool():
    path = _TOOLS / 'panel' / 'ask'
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
    codex = tmp_path / 'codex'  # a harness that lists nothing is proven by --help alone
    codex.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8', newline='\n')
    codex.chmod(0o755)
    monkeypatch.setenv('CODEX', str(codex))
    assert workers.live({'harness': 'codex', 'id': 'anything'}) == 'ok'


def test_every_declared_worker_has_a_model_id_and_the_chain_is_ordered():
    ids = workers.models()
    assert all(r['worker'] in ids for r in workers.catalog())
    positions = [int(r['chain']) for r in workers.chain()]
    assert positions == sorted(positions) and len(set(positions)) == len(positions)


def test_a_timeout_kills_the_whole_process_group():
    code, text = workers.run(['sh', '-c', 'sleep 30 & sleep 30'], timeout=1)
    assert code == 124 and 'timed out' in text
