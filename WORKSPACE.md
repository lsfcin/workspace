# Workspace Root
> Canonical workspace entrypoint. Read before any task.

## Core Principles

- The filesystem is the source of truth. Do not rely on memory, prior sessions, or machine-specific state.
- Load only the minimal relevant context for the current task.

## Interaction Side-note
- English is not my (I, Lucas, the user) mother language, and I want to improve my writing. Whenever you can outline my errors and give me writing tips based on my prompts.

## Context Conventions

- `CONTEXT.md` files add context; context chain concatenates hierarchically — navigate the folder structure downward.
- Always check for a local `CONTEXT.md` before starting work; load only context relevant to the active subtree.
- Every `CONTEXT.md` must have a title, a `> one-line description` on line 2, and a `## Routing` block at the end auto-synced by `context_synchronizer.py`.

## Behavioral Rules

- Understand local architecture before introducing changes.
- Do not invent requirements or hidden constraints.
- Prefer modifying existing abstractions over creating parallel patterns.
- Avoid creating new files unless clearly necessary.
- When uncertain about current APIs, library versions, or any factual claim — **search the web first**. Outdated knowledge causes real mistakes; do not assume.

## Git
- Workspace repo tracks only structural files (`CLAUDE.md`, `CONTEXT.md`, domain-level docs). Commit only workspace changes here. For internal projects use internal git repos.

## Core
- `Core/` contains a provider-agnostic agent systems: agent definitions, workflow protocols, and CLI tools.
- See `Core/CONTEXT.md` for the full system map.

## Research
- Use `/research <flow> <query>` to invoke it (e.g. `/research lit "topic"`, `/research review file.tex`).

## Infrastructure
- See `SETUP.md` for full replication instructions: hooks, stubgen, tsc, etc.

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
