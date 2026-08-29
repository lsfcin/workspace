# dashboard
> The entropy report: running every check over the whole tree, and what the findings look like.

Split from [`../`](../CONTEXT.md) 2026-08-18, when an eighth check pushed that directory past the
fanout signal. The seam was already the parent's own one-line description — *the dashboard **and**
the checks it runs* — so the split cost no new idea, only the hop.

**The checks stay next door and this directory owns nobody's rule.** Every module in
[`../`](../CONTEXT.md) answers one question about the tree; these two ask all of them and render the
answer. A check that moved in here would become invisible to the commit gate, which imports the
checks directly and never touches the dashboard.

`core/tools/wos/roundup` runs it at every session close; the report is the `entropy:` block inside
[`ISSUES.md`](../../../../ISSUES.md) at the workspace root, beside the hand-written issues and the
`verify:` block `core/tools/wos/roundup` writes. **This directory owns the block, never the file** —
it reads what is there, swaps its own markers, and writes the rest back untouched.

It is a **report, never a gate** — nothing here exits non-zero on a finding, and the ratchet
that keeps the counts falling lives in `core/tools/test/workspace/test_corpus_ratchet.py`.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy-dashboard.py`](entropy-dashboard.py) | [`entropy-dashboard.pyi`](entropy-dashboard.pyi) | `collect`, `main` | The entropy dashboard. Runs every Tier 0 check over the whole tree and writes ONE generated report, so agents and Lucas read a pre-computed file instead of re-scanning the workspace. Zero-token, no LLM. |
| [`entropy_report.py`](entropy_report.py) | [`entropy_report.pyi`](entropy_report.pyi) | `local_seed`, `render` | The entropy report: what the dashboard's findings look like on the page. |
| [`entropy_scatter.py`](entropy_scatter.py) | [`entropy_scatter.pyi`](entropy_scatter.pyi) | `ledger_repos`, `owner`, `partition`, `write_local`, `scatter` | Which repo owns a finding, and the local ledger it is written into. |
| [`entropy_trend.py`](entropy_trend.py) | [`entropy_trend.pyi`](entropy_trend.pyi) | `baseline`, `format_trend` | The dashboard's own history, re-derived from git rather than stored. |
<!-- routing:end -->
