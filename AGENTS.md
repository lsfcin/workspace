# Workspace Root
> Canonical workspace entrypoint. Read before any task.

- Filesystem = source of truth. No memory, no assumptions.
- Always load the CONTEXT.md of the active subtree before work.
- Uncertain about APIs, library versions, any factual claim — search web first.
- Workspace repo commits only structural files (`AGENTS.md`, `CONTEXT.md`, domain docs). Internal projects use their own git repos.

See [SETUP.md](SETUP.md) for hooks, stubgen, tsc, caveman, and toolchain setup.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`academy/`](academy/CONTEXT.md) | Research, teaching, academic work |
| [`brain/`](brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`branches/`](branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`code/`](code/CONTEXT.md) | Software projects developed under this workspace |
| [`core/`](core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`datasets/`](datasets/CONTEXT.md) | — |
| [`models/`](models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
