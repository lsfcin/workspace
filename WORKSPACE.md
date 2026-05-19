# Workspace Root
> Canonical workspace entrypoint. Read before any task.

## Core Principles

- Filesystem = source of truth. Don't rely on memory, prior sessions, or machine state.
- Load minimal relevant context for current task.

## Context Conventions

- `CONTEXT.md` files add context; chain concatenates hierarchically — navigate folder structure downward.
- Always check local `CONTEXT.md` before starting work; load only context relevant to active subtree.
- Every `CONTEXT.md` must have title, `> one-line description` on line 2, and `## Routing` block at end auto-synced by `context_synchronizer.py`.

## Behavioral Rules

- Understand local architecture before changes.
- Do not invent requirements or hidden constraints.
- Prefer modifying existing abstractions over creating parallel patterns.
- Avoid new files unless clearly necessary.
- Uncertain about APIs, library versions, any factual claim — **search web first**. Outdated knowledge causes real mistakes; do not assume.
- **Read before editing.** Read full file before modifying. Grep all callers before changing function. Never edit blind.

## Git
- Workspace repo tracks only structural files (`CLAUDE.md`, `CONTEXT.md`, domain-level docs). Commit only workspace changes here. Internal projects use internal git repos.

## Core
- `Core/` contains provider-agnostic agent systems: agent definitions, workflow protocols, CLI tools.
- See `Core/CONTEXT.md` for full system map.

## Research
- Use `/research <flow> <query>` to invoke (e.g. `/research lit "topic"`, `/research review file.tex`).

## Infrastructure
- See `SETUP.md` for full replication instructions: hooks, stubgen, tsc, caveman, etc.
- Run `codeburn optimize` periodically to audit token waste.
- Caveman auto-compresses Claude output each session (~65% output token savings). Run `/caveman-compress <file>` on CONTEXT.md files to cut input tokens.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`Academy/`](Academy/CONTEXT.md) | Research, teaching, and academic work |
| [`Branches/`](Branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`Code/`](Code/CONTEXT.md) | Software projects developed under this workspace |
| [`Core/`](Core/CONTEXT.md) | Shared research infrastructure: agents, workflow protocols, and CLI tools. |
| [`Models/`](Models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->