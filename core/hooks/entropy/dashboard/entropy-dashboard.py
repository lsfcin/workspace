#!/usr/bin/env python3
# The entropy dashboard. Runs every Tier 0 check over the whole
# tree and writes ONE generated report, so agents and Lucas read a pre-computed file
# instead of re-scanning the workspace. Zero-token, no LLM.
#
# Division of labour with core/hooks/checks/type-gate.py: the gate is a ratchet and only blocks what
# a commit ADDS, which is why a repo that inherited violations is not blocked on every
# commit. Everything it lets through historically shows up here, once, with a count.
#
# Nothing here blocks. The cap that does live in checks/pre-edit.py; this file reports what the
# tree already carries, including the files a ratchet let through before the cap reached them.
# Crossing a threshold asks for a CUT, never for a summary — forced brevity is the trap, and
# core/SCHEMA.md § A type that outgrows the cap is cut says what a cut may
# not throw away.
import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

# The checks are one level up in entropy/; the law (file_law, schema_law) is two, at the root of
# the enforcement layer; git/ holds the one check that reads git state instead of file content.
_ENTROPY = Path(__file__).resolve().parents[1]
for _dir in (_ENTROPY, _ENTROPY.parent, _ENTROPY.parent / 'git',
             _ENTROPY.parent / 'routing'):
    sys.path.insert(0, str(_dir))

import feature_law  # noqa: E402
from blocks import replace_block  # noqa: E402
from branch_debt import (merged_local_branches, merged_remote_branches,  # noqa: E402
                         unmerged_branches, unpushed_work)
from entropy_context import (check_goal_link,  # noqa: E402
                             check_misplaced_answer, check_truncation)
from entropy_corpus import (enforcement_paths, tracked_files,  # noqa: E402
                            wiki_exempt_paths)
from entropy_fanout import fanout_signals  # noqa: E402
from entropy_fields import field_hits  # noqa: E402
from entropy_ledger import (duplicate_slugs, finished_work_hits,  # noqa: E402
                            goal_vocabulary, retired_hits,
                            unanswered_placeholders, wiki_link_hits)
from entropy_naming import (check_dirs, check_placement,  # noqa: E402
                            check_shape, untracked_routing_targets)
from entropy_size import size_signals, stub_signals  # noqa: E402
from entropy_report import END, SECTIONS, SEED, START, render  # noqa: E402
from entropy_scatter import scatter  # noqa: E402
from entropy_trend import baseline, format_trend  # noqa: E402
from entropy_stores import experiment_hits, ref_tier_hits  # noqa: E402
from entropy_vendor import vendor_directive_hits  # noqa: E402
from file_law import load_limits  # noqa: E402
from platform_law import rel  # noqa: E402
from schema_law import (SCHEMA, WORKSPACE_ROOT, load_law,  # noqa: E402
                        load_retired, load_scopes)

# NAMED, NEVER INHERITED — the law is core/tools/test/workspace/test_encoding_ratchet.py. The status
# line here carries `→`. core/run exports PYTHONIOENCODING for what it spawns, which is every
# production caller and not the suite: this was red under pytest and green through its own hook.
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# The measurements sit under the hand-written issues, in their own block: an entropy finding and a
# known bug answer the same question, and core/SCHEMA.md gives that question one file. This tool
# owns the block, never the file.
REPORT = WORKSPACE_ROOT / 'ISSUES.md'

LEDGERS = {
    # Every shard of the wos ledger is ONE namespace: criterion 2 forbids the same item in two
    # ledgers, and sharding a ledger does not make its own shards rivals.
    'wos-roadmap': [WORKSPACE_ROOT / 'ROADMAP.md',
                    *sorted(WORKSPACE_ROOT.glob('ROADMAP-*.md'))],
    'core-roadmap': [WORKSPACE_ROOT / 'core/ROADMAP.md'],
    'goals': sorted((WORKSPACE_ROOT / 'brain/goals').glob('*.md')),
}


def _gate(name: str):
    """Load a kebab-named gate from checks/ — the dashboard reports what the gates block."""
    spec = spec_from_file_location(
        name.replace('-', '_'), WORKSPACE_ROOT / f'core/hooks/checks/{name}.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rel(path) -> str:
    return rel(path, WORKSPACE_ROOT)


def collect(files: list) -> dict:
    gate = _gate("type-gate")
    allowed, exempt = load_law(SCHEMA)
    scopes = load_scopes(SCHEMA)
    head_warn = load_limits()['CONTEXT_HEAD_WARN']
    findings = {'types': [], 'inventories': [], 'naming': [], 'goals': [],
                'misplaced': [], 'truncated': []}
    for path in files:
        if failure := gate.check_name(path, allowed, exempt):
            findings['types'].append(failure)
        if path.name == 'CONTEXT.md' and (failure := gate.check_inventory(path)):
            findings['inventories'].append(failure)
        if failure := check_misplaced_answer(path, head_warn):
            findings['misplaced'].append(failure)
        if failure := check_goal_link(path):
            findings['goals'].append(failure)
        if failure := check_truncation(path):
            findings['truncated'].append(failure)
        for failure in (check_shape(path, allowed), check_dirs(path, WORKSPACE_ROOT),
                        check_placement(path, scopes, WORKSPACE_ROOT)):
            if failure:
                findings['naming'].append(failure)
    exempt = enforcement_paths(WORKSPACE_ROOT)
    findings['retired'] = retired_hits(files, load_retired(SCHEMA), exempt)
    citations = _gate('citation-gate')
    findings['citations'] = citations.citation_hits(
        files, citations.citation_exempt_paths(WORKSPACE_ROOT))
    findings['wiki'] = wiki_link_hits(
        files, goal_vocabulary(WORKSPACE_ROOT / 'brain/goals'),
        wiki_exempt_paths(WORKSPACE_ROOT))
    findings['duplicates'] = [f'`[{slug}]` claimed by {", ".join(sorted(claims))}'
                              for slug, claims in duplicate_slugs(LEDGERS).items()]
    findings['routing'] = untracked_routing_targets(files, WORKSPACE_ROOT)
    findings['size'] = size_signals(files)
    findings['stubs'] = stub_signals(files)
    findings['fanout'] = fanout_signals(files, WORKSPACE_ROOT)
    findings['branches'] = unmerged_branches(WORKSPACE_ROOT)
    findings['unpushed'] = unpushed_work(WORKSPACE_ROOT)
    findings['locals'] = merged_local_branches(WORKSPACE_ROOT)
    findings['remotes'] = merged_remote_branches(WORKSPACE_ROOT)
    findings['finished'] = finished_work_hits(files, exempt)
    findings['undescribed'] = unanswered_placeholders(files, exempt)
    findings['stores'] = experiment_hits(files) + ref_tier_hits(files)
    findings['vendor'] = vendor_directive_hits(files, exempt)
    findings['fields'] = field_hits(files)
    # One directory-level finding is reported by every file under it; dedupe so a count
    # means "things to fix", not "files touched by a thing to fix".
    findings['naming'] = sorted(set(findings['naming']))
    return findings


def main(argv: list | None = None) -> int:
    if not feature_law.is_enabled('entropy-dashboard'):
        return 0  # switched off: no report is written, so the number stops existing rather than lying
    args = argv if argv is not None else sys.argv[1:]
    dry_run = '--dry-run' in args or bool(os.environ.get('LAW_PROBE')) or bool(os.environ.get('WOS_DRY_RUN'))
    files = tracked_files(WORKSPACE_ROOT, nested=True)
    findings = collect(files)
    # Every code repo's findings go to its own ledger first; what is left is this repo's own, and
    # the counts come back so the root can sum them in the same pass that wrote them.
    mine, counts = scatter(findings, WORKSPACE_ROOT, files, write=not dry_run)
    text = REPORT.read_text(encoding='utf-8') if REPORT.exists() else SEED
    here = sum(len(mine[k]) for k, _, _ in SECTIONS)
    collected = here + sum(counts.values())
    # A bare count is how "flat" got written every session while the real number climbed —
    # re-derive the baseline from git history every run rather than trusting yesterday's memory.
    # Trend on `here`, the number the header prints: baseline() reads that same wording back out of
    # git, so trending `collected` against it subtracts two different scopes and prints nonsense
    # (34 findings with a "+571 over 0 days" beside it, the first run after the header changed).
    trend = format_trend(here, baseline(WORKSPACE_ROOT))
    block = render(mine, len(files), WORKSPACE_ROOT, index=counts, trend=trend)
    if not dry_run:
        REPORT.write_text(replace_block(text, block, START, END), encoding="utf-8", newline='\n')
    status = '[dry-run] ' if dry_run else ''
    print(f'entropy dashboard {status}→ {_rel(REPORT)} ({collected} findings, '
          f'{here} here, {len(counts)} local ledgers)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
