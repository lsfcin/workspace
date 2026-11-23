# T0 the worker catalog: core/models.txt, core/workers.txt, core/agents/SPECS.md, core/tools/wos/levels and core/flows/craft/routing.md say one thing about which model is reached how, and a quota miss leaves the chain only for a while.
import importlib.machinery
import importlib.util
import pathlib
import re
import sys

_TOOLS = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_TOOLS))
import workers  # noqa: E402

ROOT = workers.ROOT
DATE = re.compile(r'^(-|\d{4}-\d{2}(-\d{2})?)$')


def _levels():
    loader = importlib.machinery.SourceFileLoader('wos_levels', str(ROOT / 'core/tools/wos/levels'))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader('wos_levels', loader))
    loader.exec_module(module)
    return module


def unknown_models(worker_rows, model_rows):
    """Workers whose `model` has no row in models.txt."""
    known = {m['model'] for m in model_rows}
    return [w['worker'] for w in worker_rows if w['model'] not in known]


def test_every_row_has_exactly_the_header_columns():
    for path in (workers.CATALOG, workers.MODELS):
        lines = path.read_text(encoding='utf-8').splitlines()
        width = len(next(l for l in reversed(lines) if l.startswith('# ') and '\t' in l).split('\t'))
        bad = [l.split('\t')[0] for l in lines if l.strip() and not l.startswith('#') and len(l.split('\t')) != width]
        assert not bad, f'{path.name}: rows without {width} columns: {bad}'


def test_every_worker_names_a_model_models_txt_declares():
    assert unknown_models(workers.table(workers.CATALOG), workers.table(workers.MODELS)) == []


def test_a_worker_whose_model_row_is_gone_is_named():
    rows = workers.table(workers.MODELS)
    assert unknown_models(workers.table(workers.CATALOG), rows[1:]) == [
        w['worker'] for w in workers.table(workers.CATALOG) if w['model'] == rows[0]['model']]


def test_structured_columns_hold_what_they_claim():
    for m in workers.table(workers.MODELS):
        assert m['tools'] in ('tools', 'text'), m['model']
        assert all(re.fullmatch(r'-|\d+(\.\d+)?', m[k]) for k in ('intel', 'coding', 'agentic')), m['model']
        assert DATE.match(m['bench_date']), m['model']
    for w in workers.table(workers.CATALOG):
        assert w['chain'] == '-' or w['chain'].isdigit(), w['worker']
        assert DATE.match(w['depleted']) and DATE.match(w['date']), w['worker']


def test_a_host_harness_worker_runs_the_id_levels_gives_that_level():
    harnesses = _levels().HARNESSES
    for w in workers.table(workers.CATALOG):
        if w['harness'] in harnesses:
            assert w['id'] == harnesses[w['harness']][0][w['level']], w['worker']


def test_every_harness_has_its_call_in_agents_specs():
    labels = [l.split('|')[1].strip().lower() for l in
              (ROOT / 'core/agents/SPECS.md').read_text(encoding='utf-8').splitlines() if l.startswith('| ')]
    missing = {w['harness'] for w in workers.table(workers.CATALOG)} - {
        h for h in workers.PLACES if any(label.startswith(h) for label in labels)}
    assert not missing, f'core/agents/SPECS.md has no call row for {sorted(missing)}'


def test_craft_routing_points_at_models_txt_and_copies_no_benchmark():
    text = (ROOT / 'core/flows/craft/routing.md').read_text(encoding='utf-8')
    assert 'models.txt' in text and not re.search(r'^\|[^\n]*\bintel\b', text, re.M)


def test_a_quota_miss_leaves_the_chain_until_it_cools_or_an_answer_clears_it(tmp_path, monkeypatch):
    log = tmp_path / 'workers.tsv'
    monkeypatch.setattr(workers, 'LOG', log)
    first = workers.chain()[0]['worker']
    names = lambda now: [r['worker'] for r in workers.chain(now)]  # noqa: E731
    log.write_text(f'2026-01-01T12:00\t{first}\tm\t-\tquota\t1.0\tlimit\n', encoding='utf-8', newline='\n')
    assert first not in names('2026-01-01T12:30')
    assert first in names(f'2026-01-01T{12 + workers.COOLDOWN_H}:01')
    with log.open('a', encoding='utf-8', newline='\n') as fh:
        fh.write(f'2026-01-01T12:10\t{first}\tm\t-\tok\t1.0\t\n')
    assert first in names('2026-01-01T12:30')
