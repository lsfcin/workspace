# Workspace Root

## Domains
- `Code/` — software projects
- `Academy/` — research, teaching, academic management
- `Models/` — local AI models and checkpoints
- `Outputs/` — generated artifacts
- `Core/Skills/` — reusable cognitive skills

## Context
- Always check for a `CONTEXT.md` in the nearest relevant subdirectory before starting work.
- Local `CONTEXT.md` overrides this file. Load only what's relevant to the current subtree.
- Use `SPECS.md` for technical contracts inside coding projects.

## Behavior
- Read before modifying. Understand the local architecture first.
- Don't invent requirements. If scope is unclear, ask.
- Prefer simple over clever. Composition over monoliths. Explicit over implicit.
- Don't create files (docs, READMEs, configs) unless asked or clearly necessary.
- Filesystem is the source of truth — not memory, not assumptions.
