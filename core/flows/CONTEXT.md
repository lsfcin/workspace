# Flows
> Workflow protocols; each names the agents and steps to execute.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`research/`](research/CONTEXT.md) | Research-workflow protocols owned by the `research` skill. Invoked as `research  |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`LOOP-TREE.md`](LOOP-TREE.md) | — | — | The Loop Tree |
| [`_template.md`](_template.md) | — | — | One line — what durable artifact this flow produces. |
| [`loop-architecture.md`](loop-architecture.md) | — | — | Architecture-decision subtree of the loop tree — turn a design/technology choice into a recorded decision (problem → options → trade-offs → decision → ADR). Produces a durable decision record, not code. |
| [`loop-engineering.md`](loop-engineering.md) | — | — | Looped engineering flow — development in file-relayed loops with model autorouting; each loop runs in a fresh, cheap session that reads exactly one file. |
| [`loop-router.md`](loop-router.md) | — | — | Loop router — classify a /loops task by TYPE and dispatch to the right subtree flow (padaria · feature/SDD · research · architecture). Thin: it classifies and hands off, it does not do the work. |
| [`mechanism-search.md`](mechanism-search.md) | — | — | Busca sistemática de mecanismos sociais (motivo individual → efeito coletivo) para um ralo quantificado — geração com diversidade forçada, filtro humano deliberativo, saída pronta para piloto test-to-kill. |
<!-- routing:end -->
