# Core
> Agent library: skills, agents, prompts, flows, tools. Provider-agnostic.

**Runtime-agnostic** — no provider-specific code. Skills invoke via `/skill-name`. Tools call via bash. Flows orchestrate agents.

## Research Agent System

Ported from Feynman (https://github.com/companion-inc/feynman), adapted for provider-agnostic use.

1. **Lead agent** (`agents/lead.md`) — receives requests, plans, orchestrates workers, synthesizes results. Read before any research task.
2. **Worker agents** (`agents/`) — specialist subagents spawned by lead: `researcher`, `writer`, `verifier`, `reviewer`.
3. **Flows** (`flows/`) — step-by-step orchestration protocols. Each names agents and sequence.
4. **Tools** (`tools/`) — executable CLI scripts; call via bash. Auto-documented in `tools/CONTEXT.md`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`agents/`](agents/CONTEXT.md) | Agent definitions; load as system prompt to spawn a specialist worker. |
| [`flows/`](flows/CONTEXT.md) | Workflow protocols; each names the agents and steps to execute. |
| [`prompts/`](prompts/CONTEXT.md) | Prepared session prompts — copy-paste into parallel agent sessions. Each file no |
| [`refs/`](refs/CONTEXT.md) | Captured references for the agent library / workspace-os scaffold — tier-1 links |
| [`skills/`](skills/CONTEXT.md) | Agent skills — provider-agnostic workflows invoked as slash commands or by instr |
| [`tools/`](tools/CONTEXT.md) | CLI research tools callable via bash; routing block auto-synced on save. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`HISTORY.md`](HISTORY.md) | — | — | Core Library History |
| [`MIGRATION-STATUS.md`](MIGRATION-STATUS.md) | — | — | Skill Suite Migration Status (AD-07) |
| [`ROADMAP.md`](ROADMAP.md) | — | — | Core Library Roadmap |
| [`SCHEMA.md`](SCHEMA.md) | — | — | Core Library Schema |
| [`SPECS.md`](SPECS.md) | — | — | Core SPECS |
| [`WATCHLIST.md`](WATCHLIST.md) | — | — | Watchlist |
<!-- routing:end -->
