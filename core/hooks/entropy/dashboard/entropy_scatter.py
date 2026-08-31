#!/usr/bin/env python3
# Which repo owns a finding, and the local ledger it is written into.
#
# Ruled 2026-08-25 (Lucas): every NESTED REPO keeps its own ISSUES.md, because the reader who can
# fix a finding is the one already inside that repo. The rule was code/-only until then, which left
# the papers and branches/ repos charging the root for findings no reader there could act on — of
# 107 charged here, five were actionable. Having a .git is the declaration now, not sitting under
# code/. core/ and brain/ are parts of WOS itself and neither is a repo, so the workspace repo's own
# ledger covers them (his call, 2026-08-24) — that half of the earlier ruling stands.
#
# The root SUMS, and the sum is recomputed here from the same scan that writes the locals — never
# hand-carried. A collected number that any repo could write into is precisely the copied-count
# drift these checks exist to catch, so one pass by one writer produces both halves or neither.
from pathlib import Path

from blocks import replace_block
from entropy_corpus import nested_repos
from entropy_report import END, START, local_seed, render
from platform_law import rel

def ledger_repos(root: Path) -> list:
    """The repos that get a local ledger, as paths relative to the workspace root."""
    return sorted(rel(repo, root) for repo in nested_repos(root))


def _head(finding: str, root: Path) -> str:
    """The path a finding names, relative to the workspace root.

    Every section leads with the thing it found — a file path, or a repo path for the two git
    checks — so the first whitespace-delimited token is the owner even when a colon or an em dash
    follows it.
    """
    token = finding.splitlines()[0].split()[0] if finding.split() else ''
    return rel(token, root).rstrip(':').lstrip('./')


def owner(finding: str, root: Path, repos: list) -> str:
    """The repo whose ledger a finding belongs in, or '' for the root's own.

    Longest prefix wins, so a repo nested inside another lands in the innermost one.
    """
    head = _head(finding, root)
    matches = [r for r in repos if head == r or head.startswith(f'{r}/')]
    return max(matches, key=len) if matches else ''


def partition(findings: dict, root: Path, repos: list) -> tuple:
    """Split every section's findings into (the root's own, one dict per code repo)."""
    mine = {key: [] for key in findings}
    per_repo = {repo: {key: [] for key in findings} for repo in repos}
    for key, items in findings.items():
        for item in items:
            target = owner(item, root, repos)
            (per_repo[target] if target else mine)[key].append(item)
    return mine, per_repo


def write_local(repo: str, root: Path, findings: dict, scanned: int) -> int:
    """Write one repo's own entropy block into its own ISSUES.md. Returns its finding count."""
    ledger = root / repo / 'ISSUES.md'
    text = ledger.read_text(encoding='utf-8') if ledger.exists() else local_seed(repo)
    block = render(findings, scanned, root / repo, name=repo)
    ledger.write_text(replace_block(text, block, START, END, at_end=True), encoding='utf-8')
    return sum(len(items) for items in findings.values())


def scatter(findings: dict, root: Path, files: list, write: bool = True) -> tuple:
    """Write every local ledger, and hand back (the root's own findings, count per repo).

    Each ledger reports the files scanned in ITS OWN repo. Handing every one of them the
    workspace-wide total would make each local file state something false about itself, which is
    the failure the self-description front exists to name.
    """
    repos = ledger_repos(root)
    mine, per_repo = partition(findings, root, repos)
    scanned = {repo: 0 for repo in repos}
    for path in files:
        if repo := owner(str(path), root, repos):
            scanned[repo] += 1
    if write:
        counts = {repo: write_local(repo, root, per_repo[repo], scanned[repo]) for repo in repos}
    else:
        counts = {repo: sum(len(items) for items in per_repo[repo].values()) for repo in repos}
    return mine, counts

