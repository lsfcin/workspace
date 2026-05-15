# Workspace Root

## Purpose and Design
- This workspace handles all sorts of projects including self-maintaining and improving strategies.
- It is designed for agents to use, the FILE SYSTEM is its core base, don't rely on memory, don't rely on the current machine setup, rely on the file system.

## Domains
- `Code/` — software projects
- `Academy/` — research, teaching, academic management
- `Branches/` — personal life management (health, finances, home)
- `Models/` — local AI models and checkpoints
- `Outputs/` — generated artifacts
- `Core/Skills/` — reusable cognitive skills

## Context
- Always check for a `CONTEXT.md` in the nearest relevant subdirectory before starting work.
- Local `CONTEXT.md` overrides this file. Load only what's relevant to the current subtree.
- Use `SPECS.md` for technical contracts inside coding projects.

## Git
- Each project under `Code/` has its own git repo — commit project changes there, not in the workspace repo.
- Workspace repo tracks only structural files (`CLAUDE.md`, `CONTEXT.md`, domain-level docs). Commit workspace changes here.
- Use `git -C <project-path>` to commit inside a project without leaving the workspace root.

## Infrastructure
- See `SETUP.md` for full replication instructions: git hooks, stubgen, tsc, Claude Code hooks.
- All enforcement infrastructure (`.hooks/`, `.claude/settings.json`) is versioned in this repo.

## Behavior
- Read before modifying. Understand the local architecture first.
- Don't invent requirements. If scope is unclear, ask.
- Prefer simple over clever. Composition over monoliths. Explicit over implicit.
- Don't create files (docs, READMEs, configs) unless asked or clearly necessary.
- Filesystem is the source of truth — not memory, not assumptions.
