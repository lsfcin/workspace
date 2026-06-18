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
| [`Academy/`](Academy/CONTEXT.md) | Research, teaching, academic work |
| [`Brain/`](Brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`Branches/`](Branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`Code/`](Code/CONTEXT.md) | Software projects developed under this workspace |
| [`Core/`](Core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`Datasets/`](Datasets/CONTEXT.md) | — |
| [`Models/`](Models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
