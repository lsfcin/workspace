# Core
> Shared research infrastructure: agents, workflow protocols, and CLI tools.

This directory is **runtime-agnostic** — no provider-specific code. Invoke via `/research <flow> <query>` or call `Core/tools/` scripts directly.

## Research Agent System

Ported from Feynman (https://github.com/companion-inc/feynman), adapted for provider-agnostic use.

1. **Lead agent** (`agents/lead.md`) — receives requests, plans, orchestrates workers, synthesizes results. Read it as operating context before any research task.
2. **Worker agents** (`agents/`) — specialized subagents spawned by the lead: `researcher`, `writer`, `verifier`, `reviewer`.
3. **Flows** (`flows/`) — step-by-step orchestration protocols. Each names which agents to use and in what sequence.
4. **Tools** (`tools/`) — executable CLI scripts; call via bash. Auto-documented in `tools/CONTEXT.md`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`agents/`](agents/CONTEXT.md) | Agent definitions; load as system prompt to spawn a specialist worker. |
| [`flows/`](flows/CONTEXT.md) | Workflow protocols; each names the agents and steps to execute. |
| [`tools/`](tools/CONTEXT.md) | CLI research tools callable via bash; routing block auto-synced on save. |
<!-- routing:end -->
