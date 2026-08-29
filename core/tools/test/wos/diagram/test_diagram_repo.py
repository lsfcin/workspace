# T1 the per-repo picture (ROADMAP.md, ruled 2026-08-20): every code repo draws itself
# from the sources it actually has. Zero-token, no network, no browser.
#
# The interesting assertions are the NEGATIVE ones. Sameness was the starting point and the shared
# shape broke; these pin where it broke, so a later session cannot quietly hand a repo page the four
# workspace-only drawings and call it symmetry.
import sys
from pathlib import Path

import pytest

_DIAGRAM = Path(__file__).resolve().parents[4] / 'tools/wos/diagram'
sys.path.insert(0, str(_DIAGRAM))
sys.path.insert(0, str(_DIAGRAM / 'views'))
sys.path.insert(0, str(_DIAGRAM.parent))

import diagram_data as data  # noqa: E402
import diagram_page as page  # noqa: E402
import diagram_repo as repo  # noqa: E402

ROOT = Path(__file__).resolve().parents[4].parent
REPOS = sorted(p for p in (ROOT / 'code').iterdir() if (p / '.git').exists())
# A clone that has not also cloned the code/ projects has no repo to draw, and the two
# cases below indexed REPOS[0] unconditionally: they died with IndexError and read as the
# per-repo picture being broken, on every workspace but the one that wrote them.
needs_repo = pytest.mark.skipif(not REPOS, reason='no code/ repos cloned here')


def test_every_code_repo_has_a_picture() -> None:
    for root in REPOS:
        assert (root / repo.OUTPUT).exists(), f'{root.name} has no ARCHITECTURE.html'


@needs_repo
def test_a_repo_page_carries_only_the_drawings_it_has_a_source_for() -> None:
    """The named type-break: matrix, summary, lifecycle and fan-in all read core/features.txt."""
    html, _ = repo.build(REPOS[0])
    assert 'id="t-spine"' in html and 'id="t-mass"' in html
    assert 'id="t-matrix"' not in html, 'a repo declares no features — it cannot draw enforcement'


def test_the_page_shell_still_renders_every_tab_when_given_every_panel() -> None:
    """The workspace's own page must not lose a tab to the shell being made tolerant."""
    panels = {key: ('<i>drawing</i>', '<i>prose</i>') for key, _, _ in page.TABS}
    html = page.render(panels, {'parsed': 1, 'total': 1, 'unparsed': []}, data.scope(ROOT))
    for key, _, _ in page.TABS:
        assert f'id="t-{key}"' in html


def test_the_findings_band_reads_the_ledger_rather_than_recounting(tmp_path) -> None:
    (tmp_path / 'ISSUES.md').write_text(
        '# x issues\n<!-- entropy:start -->\n2026-08-20 · 9 tracked files scanned · '
        '**7 findings**\n\n| Check | Findings |\n|-------|----------|\n'
        '| Size signals | 5 |\n| Naming and placement | 2 |\n| Wiki-links naming nothing | 0 |\n'
        '<!-- entropy:end -->\n', encoding='utf-8')
    total, rows = repo.findings(tmp_path)
    assert total == 7
    assert rows == [('Size signals', 5), ('Naming and placement', 2)], 'zero rows are noise'


def test_a_repo_with_no_ledger_says_so_instead_of_guessing(tmp_path) -> None:
    total, rows = repo.findings(tmp_path)
    assert total is None and rows == []


@needs_repo
def test_the_picture_is_deterministic() -> None:
    """No timestamp, no sha — which is the only thing that makes --check mean anything."""
    first, _ = repo.build(REPOS[0])
    second, _ = repo.build(REPOS[0])
    assert first == second
