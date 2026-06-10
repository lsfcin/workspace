# Workspace Root
> Canonical workspace entrypoint. Read before any task.

## Core Principles

- Filesystem = source of truth. Don't rely on memory, prior sessions, or machine state.
- Load minimal relevant context for current task.

## Context Conventions

- `CONTEXT.md` files COMPOUND context; chain concatenates hierarchically — navigate folder structure downward.
- ALWAYS check `CONTEXT.md` before work; MUST load the CONTEXT.md of the active subtree.
- Every `CONTEXT.md` must have title, `> one-line description` on line 2, and `## Routing` block at end auto-synced by `context_synchronizer.py`.

## Behavioral Rules

- Understand local architecture, file structure, and ALL patterns before changes.
- Uncertain about APIs, library versions, any factual claim — **search web first**. Avoid mistakes and rework; DO NOT assume.
- **Understand before editing.** Never edit blind.

## Git
- Workspace repo tracks only structural files (`WORKSPACE.md`, `CONTEXT.md`, domain-level docs). Commit only workspace changes here. Internal projects use internal git repos.

## Infrastructure
- See `SETUP.md` for full replication instructions: hooks, stubgen, tsc, caveman, codeburn, etc.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`Academy/`](Academy/CONTEXT.md) | Research, teaching, academic work |
| [`Brain/`](Brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`Branches/`](Branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`Code/`](Code/CONTEXT.md) | Software projects developed under this workspace |
| [`Core/`](Core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`Datasets/`](Datasets/CONTEXT.md) | — |
| [`Models/`](Models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
