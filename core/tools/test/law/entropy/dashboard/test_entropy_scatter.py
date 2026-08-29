# T0 the entropy scatter (ruled 2026-08-25): every nested repo keeps its own ledger and the root
# sums them. Zero-token, runs in verify-fast.
#
# The sum is the thing to get right. A collected number any repo could write into is the
# copied-count drift these checks exist to catch, so the test reads every local ledger BACK OFF
# DISK and re-adds it — proving the root's number was computed, not carried.
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / 'hooks/entropy/dashboard'))

from entropy_scatter import ledger_repos, owner, partition  # noqa: E402

ROOT = Path(__file__).resolve().parents[5].parent
# Every ledger's header states ITS OWN count and nothing else (changed 2026-08-25): a reader can
# only act on the repo in front of them, so charging the root header for the whole tree made the
# figure grow with the number of repos scanned. The collected total survives in one place, the
# index table's last row, and these two patterns are the only readers of either number.
HEADER = re.compile(r'\*\*(?P<here>\d+) findings here\*\*')
COLLECTED = re.compile(r'\| \*\*collected\*\* \| \*\*(?P<collected>\d+)\*\* \|')


def _reported(ledger: Path) -> int:
    """The finding count a ledger states in its own generated block."""
    match = HEADER.search(ledger.read_text(encoding='utf-8'))
    return int(match.group('here')) if match else 0


def test_every_nested_repo_has_its_own_ledger() -> None:
    for repo in ledger_repos(ROOT):
        assert (ROOT / repo / 'ISSUES.md').exists(), f'{repo} has no local ISSUES.md'


def test_the_root_total_equals_the_sum_of_the_local_ledgers() -> None:
    repos = ledger_repos(ROOT)
    if not repos:
        # A clone with no nested repos has nothing to sum, and the dashboard writes no collected
        # row for it. Asserting anyway read as the scatter being broken on every fresh clone.
        pytest.skip('no nested repos in this clone — the scatter has nothing to sum')
    root_text = (ROOT / 'ISSUES.md').read_text(encoding='utf-8')
    here = int(HEADER.search(root_text).group('here'))
    collected = int(COLLECTED.search(root_text).group('collected'))
    scattered = sum(_reported(ROOT / repo / 'ISSUES.md') for repo in repos)
    assert collected == here + scattered


def test_the_index_lists_every_repo_that_has_a_ledger() -> None:
    root_text = (ROOT / 'ISSUES.md').read_text(encoding='utf-8')
    for repo in ledger_repos(ROOT):
        assert f'({repo}/ISSUES.md)' in root_text, f'{repo} is missing from the root index'


def test_a_finding_lands_in_the_repo_that_owns_its_path() -> None:
    repos = ['code/aiwbot', 'code/dobra']
    assert owner('code/aiwbot/bot.py — 3 lines over', ROOT, repos) == 'code/aiwbot'


def test_the_innermost_repo_wins_when_one_nests_inside_another() -> None:
    repos = ['code/outer', 'code/outer/inner']
    assert owner('code/outer/inner/thing.py: finding', ROOT, repos) == 'code/outer/inner'


def test_papers_and_branches_own_their_findings() -> None:
    """Ruled 2026-08-25: having a .git is the declaration, not sitting under code/. Until then these
    charged the root for findings no reader there could act on.

    Declared repos, like both tests above: reading ledger_repos() here made the RULING contingent on
    which repos this clone happens to have. A workspace cloned without them proved nothing and
    reported it as the rule being broken."""
    repos = ['academy/papers/wos-ablation', 'branches/casinhas']
    assert owner('academy/papers/wos-ablation/PLAN.md: finding', ROOT, repos) == 'academy/papers/wos-ablation'
    assert owner('branches/casinhas/PROJETO.md: finding', ROOT, repos) == 'branches/casinhas'


def test_core_and_brain_stay_with_the_workspace_repo() -> None:
    """Ruled 2026-08-24 and unchanged by the generalisation: neither is a repo, so WOS's own ledger
    covers both."""
    repos = ledger_repos(ROOT)
    assert owner('core/SCHEMA.md: finding', ROOT, repos) == ''
    assert owner('brain/GOALS.md: finding', ROOT, repos) == ''


def test_the_header_charges_this_repo_for_its_own_findings_only() -> None:
    """Ruled 2026-08-25. The header read `**603 findings**, 33 of them here` and the 603 was what
    every reader took away — a figure that grew with the number of repos scanned rather than with
    this repo's debt, and that nobody could act on from here. The nested total is context for
    picking the next repo, so it stays in the index and out of the headline."""
    from entropy_report import SECTIONS, render
    findings = {key: [] for key, _, _ in SECTIONS}
    findings['size'] = ['core/a.md: 3 lines over']
    block = render(findings, scanned=10, root=Path('/x'), index={'code/one': 90, 'code/two': 7})
    assert '**1 findings here**' in block
    assert '97 more across 2 nested repos' in block
    assert '**98 findings' not in block
    assert '| **collected** | **98** |' in block


def test_the_trend_is_measured_on_the_number_the_header_prints() -> None:
    """The header and its baseline must be the same scope, or the delta is between two scales.

    First run after the header changed printed `**34 findings here** (2026-08-25: 33 · +571 over 0
    days)`: the trend was still computed on the collected total while the header showed this repo's
    own. baseline() reads the header's own wording back out of git, so the two cannot diverge again
    without this failing.
    """
    from entropy_trend import _COUNT
    from entropy_report import SECTIONS, render
    findings = {key: [] for key, _, _ in SECTIONS}
    findings['size'] = ['core/a.md: over', 'core/b.md: over']
    block = render(findings, scanned=10, root=Path('/x'), index={'code/one': 500})
    assert int(_COUNT.search(block).group(1)) == 2


def test_partition_loses_no_finding() -> None:
    findings = {'size': ['code/aiwbot/a.py x', 'core/b.md y'], 'naming': ['code/dobra/c: z']}
    repos = ['code/aiwbot', 'code/dobra']
    mine, per_repo = partition(findings, ROOT, repos)
    kept = sum(len(v) for v in mine.values())
    kept += sum(len(v) for repo in per_repo.values() for v in repo.values())
    assert kept == sum(len(v) for v in findings.values())
