# Flows
> Workflow protocols; each names the agents and steps to execute.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`LOOP-TREE.md`](LOOP-TREE.md) | — | — | The Loop Tree |
| [`_template.md`](_template.md) | — | — | One line — what durable artifact this flow produces. |
| [`audit.md`](audit.md) | — | — | Compare a paper's claims against its public codebase and identify mismatches, omissions, and reproducibility risks. |
| [`autoresearch.md`](autoresearch.md) | — | — | Autonomous experiment loop — try ideas, measure results, keep what works, discard what doesn't, repeat. |
| [`compare.md`](compare.md) | — | — | Compare multiple sources on a topic and produce a source-grounded matrix of agreements, disagreements, and confidence. |
| [`deepresearch.md`](deepresearch.md) | — | — | Run a thorough, source-heavy investigation on a topic and produce a durable research brief with inline citations. |
| [`draft.md`](draft.md) | — | — | Turn research findings into a polished paper-style draft with equations, sections, and explicit claims. |
| [`lit.md`](lit.md) | — | — | Run a literature review on a topic using paper search and primary-source synthesis. |
| [`loop-architecture.md`](loop-architecture.md) | — | — | Architecture-decision subtree of the loop tree — turn a design/technology choice into a recorded decision (problem → options → trade-offs → decision → ADR). Produces a durable decision record, not code. |
| [`loop-engineering.md`](loop-engineering.md) | — | — | Looped engineering flow — development in file-relayed loops with model autorouting; each loop runs in a fresh, cheap session that reads exactly one file. |
| [`loop-router.md`](loop-router.md) | — | — | Loop router — classify a /loops task by TYPE and dispatch to the right subtree flow (padaria · feature/SDD · research · architecture). Thin: it classifies and hands off, it does not do the work. |
| [`mechanism-search.md`](mechanism-search.md) | — | — | Busca sistemática de mecanismos sociais (motivo individual → efeito coletivo) para um ralo quantificado — geração com diversidade forçada, filtro humano deliberativo, saída pronta para piloto test-to-kill. |
| [`recipe.md`](recipe.md) | — | — | Find ranked, implementable ML training recipes backed by papers, datasets, docs, and code. |
| [`replicate.md`](replicate.md) | — | — | Plan or execute a replication workflow for a paper, claim, or benchmark. |
| [`review.md`](review.md) | — | — | Simulate an AI research peer review with likely objections, severity, and a concrete revision plan. |
| [`summarize.md`](summarize.md) | — | — | Summarize any URL, local file, or PDF using the RLM pattern — source stored on disk, never injected raw into context. |
| [`watch.md`](watch.md) | — | — | Set up a recurring or deferred research watch on a topic, company, paper area, or product surface. |
<!-- routing:end -->
