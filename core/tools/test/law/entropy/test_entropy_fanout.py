# T0 directory fanout (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast.
#
# The law is not new: a files-per-directory threshold has always existed and
# context_synchronizer.sync has always warned on it — to stdout, during a sync nobody
# reads, which is why the tail grew to 51 files in one directory. These tests hold the
# same law where it is visible.
#
# The whole-tree test is a RATCHET: live violations must be a subset of a named baseline,
# so a new one fails the build while the inherited ones stay visible. Shrinking the
# baseline is the only edit this test should ever get.
import sys
from pathlib import Path

from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine
# sys.path for the enforcement layer is set once, by conftest.py — a second copy
# here would go stale the next time core/hooks is split.

import entropy_fanout  # noqa: E402
import entropy_ledger  # noqa: E402
from file_law import load_limits  # noqa: E402
from platform_law import rel  # noqa: E402

WARN = load_limits()['WARN_FILES']

# Inherited fanout, each a directory that owes a split. Nothing else may join.
#
# MOST ROWS BELOW READ THE SAME WAY, stated once here rather than per row: the directory's NAME has
# not drifted — every file in it really does the one job the directory claims — so the count is the
# cost of that design working, not a responsibility problem. Each keeps the SEAM it would split on,
# because a row with no named retirement is a threshold that quietly rises. COST THE HOP BEFORE
# TAKING IT: the split rejected for `core/hooks/entropy/` was rejected for removing less table than
# it added, and a new directory is a CONTEXT.md the whole tree pays to read.
BASELINE = {
    'core/skills/caveman/scripts',
    'core/skills/caveman/hooks',
    'academy/administration/coordenacao-lc/novo-ppc-bcc/ementas',
    # The exception — this name HAS drifted. `gates/` is supposed to mirror `core/hooks/gates/`, but
    # it holds tests for hooks from read/, checks/, git/ and compact/ as well, which is the
    # responsibility problem the signal exists to surface rather than a count to wave through.
    # Retired the way `law/entropy/` and `workspace/generators/` already are: one test directory per
    # hook directory it covers.
    'core/tools/test/workspace/gates',
    # Seam: what each tool TOUCHES — the ledgers it reads (`spec-scan`, `spec-contract-check`,
    # `features`, `deps`) against the files it rewrites (`wrap`, `sync-skills`,
    # `sync-global-skills`, `roundup`).
    'core/tools/wos',
    # Seam: what each check READS — the tree's shape (corpus, naming, fanout, size) against its text
    # (context, ledger, stores, vendor). Costed and REJECTED 2026-08-24 (Lucas); the directory holds
    # over the signal on purpose and its own CONTEXT.md carries the reason.
    'core/hooks/entropy',
    # Over the BLOCK cap, not the warn, and the only row whose retirement is still an open question:
    # it is described as a mirror of `core/hooks/entropy/` and is not one — ISSUES.md B5.
    'core/tools/test/law/entropy',
    # Seam: what each module DOES TO A DOCUMENT — reads it (`header`, `hoist`, `workspace_meta`,
    # `workspace_scanner`) against writes into it (`blocks`, `context_synchronizer`, `norms`,
    # `shard_table`). Same verdict as `core/hooks/entropy/` for the same reason, in its CONTEXT.md.
    'core/hooks/routing',
    # The OS-agnostic port put the ninth file here: `platform_law.py` joined the three law modules
    # the root is supposed to hold. Retired by the port finishing rather than by a split — the root
    # also carries `post-edit.sh`, and porting the post-edit stages to Python removes it. If the
    # count has not fallen once the last shell hook is gone, this row becomes a real split.
    'core/hooks',
    # The Antigravity integration put the eighth file here: `test_antigravity_shim.py` joined the
    # seven workspace-invariant tests. Costed against the hop: a split saving one table row does not
    # pay for the CONTEXT.md. Retired when provider shim tests split into a dedicated directory once
    # Codex and other runtimes gain behavioral suites.
    'core/tools/test/workspace',
}


def _live() -> set:
    counts = entropy_fanout.fanout_counts(
        entropy_ledger.tracked_files(WORKSPACE_ROOT), WORKSPACE_ROOT)
    return {rel(d, WORKSPACE_ROOT)
            for d, n in counts.items() if n > WARN}


def test_no_new_directory_exceeds_the_fanout_signal() -> None:
    assert _live() <= BASELINE, (
        f'new over-full directories: {sorted(_live() - BASELINE)} — split by '
        f'responsibility, or add to BASELINE with the item that retires it')


def test_baseline_is_not_stale() -> None:
    assert BASELINE <= _live(), (
        f'these are fixed and must leave BASELINE: {sorted(BASELINE - _live())}')


def test_a_small_directory_is_clean(tmp_path) -> None:
    files = [tmp_path / f'mod_{i}.py' for i in range(WARN)]
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_an_over_full_directory_is_flagged(tmp_path) -> None:
    files = [tmp_path / f'mod_{i}.py' for i in range(WARN + 1)]
    signals = entropy_fanout.fanout_signals(files, tmp_path)
    assert len(signals) == 1
    assert f'{WARN + 1} code files' in signals[0]


def test_warn_and_block_are_reported_differently(tmp_path) -> None:
    """Symmetric with the file pair: a WARN asks for a look, a BLOCK is the cap."""
    block = load_limits()['BLOCK_FILES']
    warned = entropy_fanout.fanout_signals(
        [tmp_path / f'm{i}.py' for i in range(WARN + 1)], tmp_path)
    blocked = entropy_fanout.fanout_signals(
        [tmp_path / f'm{i}.py' for i in range(block + 1)], tmp_path)
    assert 'WARN_FILES signal' in warned[0]
    assert 'BLOCK_FILES cap' in blocked[0]


def test_a_flat_document_collection_is_not_fanout(tmp_path) -> None:
    """brain/goals is 57 goal files and splitting it would be wrong. Only code counts."""
    files = [tmp_path / f'goal-{i}.md' for i in range(40)]
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_interface_stubs_do_not_count_toward_fanout(tmp_path) -> None:
    """A stub rides in its source's Interface column; it is not a second thing to hold."""
    files = []
    for i in range(WARN):
        files += [tmp_path / f'mod_{i}.py', tmp_path / f'mod_{i}.pyi']
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_the_threshold_has_exactly_one_home() -> None:
    """The number is read from limits.env, never restated — a second copy is drift."""
    source = (WORKSPACE_ROOT / 'core/hooks/entropy/entropy_fanout.py').read_text(encoding='utf-8')
    assert 'load_limits' in source
    assert f'= {WARN}' not in source
