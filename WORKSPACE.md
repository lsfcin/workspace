# Workspace Root
> Canonical workspace entrypoint. Read before any task.

## Core Principles

- The filesystem is the source of truth. Do not rely on memory, prior sessions, or machine-specific state.
- Prefer targeted reads over broad repository traversal.
- Load only the minimal relevant context for the current task.
- Preserve semantic locality: related logic should remain understandable from a small number of nearby files.
- Prefer extraction and modularization over extending large files.

## Context Resolution

- Context concatenates hierarchically by navigating the folder structure downwards.
- Always check for a local `CONTEXT.md` before starting work.
- Load only context relevant to the active subtree.

## Behavioral Rules

- Read the minimal relevant context before modifying code.
- Understand local architecture before introducing changes.
- Do not invent requirements or hidden constraints.
- Prefer simple, explicit, composable solutions.
- Prefer modifying existing abstractions over creating parallel patterns.
- Verify external APIs, package behavior, and current documentation before making factual claims.
- Avoid creating new files unless clearly necessary.
- When in doubt, check the web; if needed, ask.

## Context Conventions

### CONTEXT.md

- Every `CONTEXT.md` must contain:
  - a title heading
  - a one-line description in line 2 (blockquote), immediately below the title
  - relevant local constraints only
  - at the end, a `## Routing` block auto-synced (post-edit | pre-commit hooks) by `context_synchronizer.py`

## Git
- Workspace repo tracks only structural files (`CLAUDE.md`, `CONTEXT.md`, domain-level docs). Commit workspace changes here. Internal projects have internal git repos.

## Infrastructure
- See `SETUP.md` for full replication instructions: hooks, stubgen, tsc, etc.

<!-- ctx-sync:routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`Academy/`](Academy/CONTEXT.md) | Research, teaching, and academic work |
| [`Branches/`](Branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`Code/`](Code/CONTEXT.md) | Software projects developed under this workspace |
| [`Core/`](Core/CONTEXT.md) | Workspace-level shared resources, templates, and cross-domain utilities |
| [`Models/`](Models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
| [`Outputs/`](Outputs/CONTEXT.md) | Generated artifacts; avoid manual edits unless requested |
<!-- ctx-sync:routing:end -->
