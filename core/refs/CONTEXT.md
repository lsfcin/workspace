# References
> Captured references for the agent library / workspace-os scaffold — tier-1 links in [REFS.md](REFS.md).

## Source tiers — cite the tier, always

Research passes over-collect arXiv because it is the easiest surface to search. arXiv is
**not peer reviewed**: a preprint claim is provisional until a venue accepts it. Every ref
in [REFS.md](REFS.md) carries a tier marker so a later reader knows how much weight it holds.

| Tier | Meaning | Weight |
|------|---------|--------|
| `[A]` | Peer-reviewed, excellence venue — ICSE · TSE · ACL · EMNLP · NAACL · NeurIPS · ICLR · ICML · AAAI · CHI · UIST · CSCW · SOSP · USENIX Security · IEEE S&P · CCS · TMLR · TACL | Citable as established |
| `[B]` | Peer-reviewed, other venue / workshop / journal outside the top tier | Citable, note the venue |
| `[P]` | Preprint — arXiv, OpenReview submission, SSRN. **Not reviewed** | Provisional. Never the sole basis for a workspace policy change |
| `[V]` | Vendor / lab engineering post (Anthropic, Google, OpenAI) | Authoritative about *their* product, not independent evidence |
| `[C]` | Community / practitioner — blog, repo, spec draft | Signal about practice, not evidence |

**Rule for research passes**: a query round that returns only `[P]` is incomplete. Re-run it
against a venue-aware source before concluding. `core/tools/papers --ss` reports `venue` and
`peer_reviewed` per hit; `--reviewed` drops preprints, `--min-cit N` drops noise.
Web search often surfaces the published version (`aclanthology.org`, `dl.acm.org`,
`openreview.net` with a venue) when arXiv only shows the preprint — prefer that URL.

A preprint that later gets accepted keeps its arXiv id — upgrade the tier marker in place
when you notice, do not add a second line.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`REFS.md`](REFS.md) | — | — | References |
<!-- routing:end -->
