# Core
> Agent library: skills, agents, prompts, flows, tools. Provider-agnostic.

**Runtime-agnostic** — no provider-specific code. Skills invoke via `/skill-name`. Tools call via bash. Flows
orchestrate agents.

## Research Agent System

Ported from Feynman (https://github.com/companion-inc/feynman), adapted for provider-agnostic use.

1. **Lead agent** (`agents/lead.md`) — receives requests, plans, orchestrates workers, synthesizes results. Read before
   any research task.
2. **Worker agents** (`agents/`) — specialist subagents spawned by lead: `researcher`, `writer`, `verifier`, `reviewer`.
3. **Flows** (`flows/`) — step-by-step orchestration protocols. Each names agents and sequence.
4. **Tools** (`tools/`) — executable CLI scripts; call via bash. Auto-documented in `tools/CONTEXT.md`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`agents/`](agents/CONTEXT.md) | Agent definitions; load as system prompt to spawn a specialist worker. |
| [`experiments/`](experiments/CONTEXT.md) | What we measured about this workspace, when, and what changed because of it. One file per question. |
| [`flows/`](flows/CONTEXT.md) | Workflow protocols; each names the agents and steps to execute. |
| [`hooks/`](hooks/CONTEXT.md) | The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run. |
| [`norms/`](norms/CONTEXT.md) | Rules obeyed rather than enforced. One file each; `AGENTS.md`'s rule block is generated from them. |
| [`prompts/`](prompts/CONTEXT.md) | Prepared session prompts — copy-paste into parallel agent sessions. Each file notes target tier/effort and deliverable. |
| [`refs/`](refs/CONTEXT.md) | Captured references for the agent library / workspace-os scaffold — tier-1 links in [REFS.md](refs/REFS.md). |
| [`skills/`](skills/CONTEXT.md) | Agent skills — provider-agnostic workflows invoked as slash commands or by instruction. |
| [`tools/`](tools/CONTEXT.md) | CLI tools callable via bash, one directory per family; routing block auto-synced on save. |

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Core Library Roadmap |
| [`SCHEMA-layers.md`](SCHEMA-layers.md) | The frontmatter every skill, agent, norm and flow declares, and how they compose. The document law — types, placement, cutting, vocabulary — is the index, [`SCHEMA.md`](SCHEMA.md); this shard is the prompt-loaded half, because a `.md` a session reads and a frontmatter block a runtime parses are two different contracts. |
| [`SCHEMA.md`](SCHEMA.md) | The law about `.md` documents: which types exist, where a file belongs, how one that outgrew the cap is cut, and which words are canonical. The **tables here are load-bearing** — [`schema_law.py`](hooks/schema_law.py) parses them and no checker restates them. Drift is a bug. |
| [`SPECS.md`](SPECS.md) | Architecture decisions and conventions for the Core agent library. |
| [`features.txt`](features.txt) | Every toggleable feature this workspace has, declared: what group it belongs to, how hard it enforces, whether it is general or Lucas-specific, and whether it can actually be switched off. Read by core/hooks/feature_law.py; the answers live in core/profile.txt. |
| [`permissions.txt`](permissions.txt) | Neutral permission tiers: what an agent may do without asking. Tab-separated columns: kind   tier | rule tier   guarded | standard | open key    summary | tradeoff | mode (for kind=tier); allow | ask | deny (for kind=rule) value  prose (for kind=tier); neutral action slug (for kind=rule) |
| [`profile.txt`](profile.txt) | Which features are switched on for THIS machine, and the settings that are not switches. The registry is core/features.txt; this file holds only the answers. Read by core/hooks/feature_law.py, edited through `core/tools/wos/features --on|--off <slug>`. |
| [`run`](run) | The one command that runs anything in core/: find this clone's interpreter, then exec with it. |
<!-- routing:end -->
