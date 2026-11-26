# T1 delegate contract: a contract file reads as one frontmatter and its sections, a read-only v0 refuses what it cannot keep, context is inlined under its budget and pointed at above it, and a worker's return is read, flagged and cut without losing its fixed fields.
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'delegate'))
import delegation  # noqa: E402

GOOD = '''---
goal: "Find what breaks: a colon in a command must survive"
work: review
role: critic
read_paths: [a.md]
write_paths: []
checks: []
attempt: 1/2
return: answer
---
## Context
The proposal is in a.md.
'''


def test_a_contract_reads_as_its_frontmatter_and_sections():
    c = delegation.parse(GOOD)
    assert c['goal'].endswith('a colon in a command must survive') and c['attempt'] == (1, 2)
    assert c['sections'] == {'Context': 'The proposal is in a.md.'}


def test_a_file_without_frontmatter_is_not_a_contract():
    assert delegation.is_contract('Review this plan: ...') is False and delegation.is_contract(GOOD) is True


@pytest.mark.parametrize('change, error', [
    (('write_paths: []', 'write_paths: [x.py]'), 'read-only'),
    (('checks: []', 'checks: [pytest -q]'), 'checks'),
    (('return: answer', 'return: patch'), 'answer'),
    (('work: review', 'work: dance'), 'work'),
    (('role: critic', 'role: poet'), 'role'),
    (('attempt: 1/2', 'attempt: 2/2'), 'Last Failure'),
    (('attempt: 1/2', 'attempt: 3/2'), 'attempt'),
])
def test_v0_refuses_what_a_read_only_answer_cannot_keep(change, error):
    with pytest.raises(ValueError, match=error):
        delegation.validate(delegation.parse(GOOD.replace(*change)), works={'review'}, roles={'critic'})


def test_a_retry_carries_its_last_failure():
    c = delegation.parse(GOOD.replace('attempt: 1/2', 'attempt: 2/2') + '## Last Failure\nstatus: fail — no verdict\n')
    delegation.validate(c, works={'review'}, roles={'critic'})
    assert 'no verdict' in delegation.prompt(c, '', [])


def test_context_is_inlined_under_its_budget_and_pointed_at_above_it(tmp_path):
    (tmp_path / 'small.md').write_text('tiny', encoding='utf-8', newline='\n')
    (tmp_path / 'big.md').write_text('x' * 500, encoding='utf-8', newline='\n')
    inline, by_path = delegation.bundle(['small.md', 'big.md'], tmp_path, budget=100)
    assert '### small.md\ntiny' in inline and by_path == ['big.md']
    with pytest.raises(ValueError, match='missing.md'):
        delegation.bundle(['missing.md'], tmp_path, budget=100)


def test_the_stable_prefix_comes_first_and_the_task_last():
    p = delegation.prompt(delegation.parse(GOOD), '### a.md\nbody', ['big.md'])
    assert p.startswith(delegation.RETURN_FORMAT) and p.index(delegation.RETURN_FORMAT[-20:]) < p.index('a colon in a command')
    assert p.index('a colon in a command') < p.index('### a.md') and 'big.md' in p


def test_a_return_is_read_and_a_non_empty_list_asks_for_review():
    r = delegation.read('status: ok\n## Answer\nfine\n## Assumptions\n- the tests pass\n## Unverified\nnone\n## Left untouched\n- none\n')
    assert (r['status'], r['check'], r['review']) == ('ok', '-', True)
    assert delegation.read('status: ok\n## Answer\nfine\n## Assumptions\nnone\n## Unverified\nnone\n## Left untouched\nnone\n')['review'] is False


def test_a_return_without_a_status_or_its_lists_is_bad_format():
    assert delegation.read('Looks good to me.')['check'] == 'bad-format'
    assert delegation.read('status: maybe\n## Answer\nx')['check'] == 'bad-format'
    assert delegation.read('status: blocked\n## Answer\nx\n## Questions\n- which branch?')['check'] == 'bad-format'


def test_the_cut_keeps_every_fixed_field_and_points_at_the_full_answer():
    text = 'status: ok\n## Answer\n' + 'word ' * 4000 + '\n## Assumptions\n- one\n## Unverified\nnone\n## Left untouched\nnone\n'
    out = delegation.cut(text, limit=1500, full='outputs/delegate/x.md')
    assert len(out) <= 1500 * delegation.CHARS_PER_TOKEN
    assert out.startswith('status: ok') and '- one' in out and '## Left untouched' in out and 'outputs/delegate/x.md' in out
    assert delegation.cut('status: ok\nshort', limit=1500, full='f') == 'status: ok\nshort'


def test_a_subheading_inside_the_answer_stays_in_the_answer_and_is_cut_with_it():
    # argon's review of this file, 2026-11-26: any `## ` line used to end the Answer.
    text = 'status: ok\n## Answer\nintro\n## Finding 1\n' + 'word ' * 4000 + '\n## Assumptions\nnone\n## Unverified\nnone\n## Left untouched\nnone\n'
    assert 'Finding 1' in delegation.sections(text)['Answer']
    assert len(delegation.cut(text, limit=1500, full='f')) <= 1500 * delegation.CHARS_PER_TOKEN


def test_a_blocked_return_counts_its_questions_not_its_search_notes():
    lists = '## Assumptions\nnone\n## Unverified\nnone\n## Left untouched\nnone\n'
    ok = 'status: blocked\n## Answer\nx\n## Questions\nSearched core/ and git log.\n- Which branch?\n- Which repo?\n' + lists
    assert delegation.read(ok)['check'] == '-'
    assert delegation.read(ok.replace('- Which branch?\n- Which repo?\n', ''))['check'] == 'bad-format'


def test_a_status_in_bold_or_capitals_and_none_in_its_variants_read_as_meant():
    r = delegation.read('**Status:** OK\n## Answer\nx\n## Assumptions\n- none.\n## Unverified\n* (none)\n## Left untouched\nN/A\n')
    assert (r['status'], r['check'], r['review']) == ('ok', '-', False)
    assert delegation.read('status: ok\n## Answer\n\n## Assumptions\nnone\n## Unverified\nnone\n## Left untouched\nnone\n')['check'] == 'bad-format'
