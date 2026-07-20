# Agents
> Agent definitions; load as system prompt to spawn a specialist worker.

Each file is a complete operating context for one agent role. In Claude Code, spawn a worker by passing the file content as the system prompt via the Agent tool.

| Agent | Role |
|-------|------|
| `lead.md` | Orchestrator — receives task, plans, delegates to workers, synthesizes output |
| `researcher.md` | Evidence gathering — web + paper search, source tables, context hygiene |
| `reviewer.md` | Peer review — FATAL / MAJOR / MINOR severity, inline annotations |
| `verifier.md` | Citation verification — anchors claims, checks URLs, removes unsourced content |
| `writer.md` | Synthesis — drafts from evidence only; verifier adds citations afterward |

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`_template.md`](_template.md) | — | — | One line — what evidence or output this worker produces. |
| [`lead.md`](lead.md) | — | — | Orchestrates research workflows; plans tasks, delegates to worker agents, synthesizes results. |
| [`researcher.md`](researcher.md) | — | — | Gather primary evidence across papers, web sources, repos, docs, and local artifacts. |
| [`reviewer.md`](reviewer.md) | — | — | Simulate a tough but constructive AI research peer reviewer with inline annotations. |
| [`verifier.md`](verifier.md) | — | — | Post-process a draft to add inline citations and verify every source URL. |
| [`writer.md`](writer.md) | — | — | Turn research notes into clear, structured briefs and drafts. |
<!-- routing:end -->
