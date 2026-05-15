# Workspace Root
> Canonical startup file for the workspace; read this before anything else

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
- See `SETUP.md` for full replication instructions: hooks, stubgen, tsc, etc.

## Behavior
- Read before modifying. Understand the local architecture first.
- Don't invent requirements. If scope is unclear, ask.
- Prefer simple over clever. Composition over monoliths. Explicit over implicit.
- When a claim depends on external documentation, current APIs, package behavior, or other facts not established by the workspace, state the uncertainty explicitly and verify it against authoritative web sources before answering.
- If web verification is needed but unavailable in the current turn, ask the user to allow a web search instead of guessing.
- Don't create files (docs, READMEs, configs) unless asked or clearly necessary.
- Filesystem is the source of truth — not memory, not assumptions.

## Context & Modularization Guidance
- Always check for a `CONTEXT.md` in the nearest relevant subdirectory before starting work. Local `CONTEXT.md` overrides the root file when working inside a subtree.

### CONTEXT.md Convention

- Each `CONTEXT.md` must include a one-line description in line 2 (blockquote) after the title heading.
- `ctx-sync.py` keeps file maps in sync and is invoked by post-edit and pre-commit hooks.

### First-Line Description Convention

- Every new code file must start with a one-line description comment as line 1.
- Hooks will block creation of files missing this comment and remind on edits.

### Interface Files and Interface-First Policy

- Interface files (`.pyi`, `.d.ts`, `.dart.api`) are generated and preferred for initial reads.
- If an interface exists and is current, read it before the source. Hooks enforce this when applicable.

### Modularization Strategy

- One reason to change per file. Split files when multiple independent features would cause edits.
- Separate stable from volatile code first.
- Minimize import fan-out when creating new modules.
- Design boundaries for the next likely task.

### File Size Policy

Enforced by hooks: code files should avoid growing beyond the line-count limits.

| Lines | Signal | Action |
|-------|--------|--------|
| ≥ 200 | ⚠ Block (agent pre-edit) | Create a new module before editing larger files |
| ≥ 300 | 🚨 Block (git commit) | Commit rejected; split the file |