# dashboard
> The entropy report: running every check over one repo, and what the findings look like.

Split from [`../`](../CONTEXT.md) 2026-08-18, when an eighth check pushed that directory past the
fanout signal. The seam was already the parent's own one-line description — *the dashboard **and**
the checks it runs* — so the split cost no new idea, only the hop.

**The checks stay next door and this directory owns nobody's rule.** Every module in
[`../`](../CONTEXT.md) answers one question about the tree; these ask all of them and render the
answer. A check that moved in here would become invisible to the commit gate, which imports the
checks directly and never touches the dashboard.

**One repo per run** (ruled 2026-09-04, Lucas). No argument means this repo; `--repo <path>` names
another, which is how a project's own pre-commit writes its own `ISSUES.md`. It used to scan every
nested project from the root and commit a ledger into each — but those are repos the root's git
ignores, so the committed block described a disk rather than the repo, and the clone without them
read the same commit as red. Which projects exist is [`PROJECTS.md`](../../../../PROJECTS.md).

`core/tools/wos/roundup` runs it at every session close; the report is the `entropy:` block inside
that repo's `ISSUES.md`, beside the hand-written issues and the `verify:` block the close writes.
**This directory owns the block, never the file** — it reads what is there, swaps its own markers,
and writes the rest back untouched.

It is a **report, never a gate** — nothing here exits non-zero on a finding, and the ratchet
that keeps the counts falling lives in `core/tools/test/workspace/test_corpus_ratchet.py`.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy-dashboard.py`](entropy-dashboard.py) | [`entropy-dashboard.pyi`](entropy-dashboard.pyi) | `collect`, `main` | The entropy dashboard. Runs every Tier 0 check over ONE repo — this one, or the `--repo` named — and writes one generated report, so agents and Lucas read a pre-computed file instead of re-scanning the tree. Zero-token, no LLM. |
| [`entropy_report.py`](entropy_report.py) | [`entropy_report.pyi`](entropy_report.pyi) | `local_seed`, `render` | The entropy report: what the dashboard's findings look like on the page. |
| [`entropy_trend.py`](entropy_trend.py) | [`entropy_trend.pyi`](entropy_trend.pyi) | `baseline`, `format_trend` | The dashboard's own history, re-derived from git rather than stored. |
<!-- routing:end -->
