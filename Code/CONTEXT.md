# Code
> Software projects developed under this workspace

## Engineering Principles

- **High cohesion** — one CRISTAL CLEAR responsibility per file.
- **Minimize file LOC** — small is better! many small files over monoliths; think limits ahead.
- **Explicit naming** — file names guessable without opening, keep naming patterns.
- **Flat structure** — sub-modules over deep nesting.
- **Low coupling** — small modules, explicit imports; no hidden cross-directory coupling.
- **Facade boundaries** — cross-folder imports go through `index` / `__init__` only (enforced by hook).
- **Interface-first reading** — read `.pyi` / `.d.ts` / `.dart.api` before source files (enforced by hook). Facade files (`index.ts`, `__init__.py`, `index.dart`) are exempt — read directly.

## Facade Pattern

Every folder with source files exposes a facade (`index.ts`, `__init__.py`, etc.) as sole public entry point. Cross-folder imports that bypass the facade are hard-blocked at commit.

Full per-language convention, rules, and enforcement details: [SPECS.md](SPECS.md).

## File Size Policy

Applies to `.js .ts .tsx .py .dart .html .css .scss`:

- Target: under **100 LOC**
- Warning at **150 LOC** (hook warns on commit)
- Hard block at **200 LOC** (commits and AI edits blocked)

Near limits: extract modules, separate orchestration from implementation.

## First-Line Description

Every code file must begin with one-line description comment:

| Language | Format |
|----------|--------|
| Python / YAML / TOML | `# Short description` |
| JS / TS / Dart | `// Short description` |
| CSS / SCSS | `/* Short description */` |
| HTML | `<!-- Short description -->` |
| Markdown | `# Title` (heading IS the description) |

One sentence, no period, ~80 chars. Describe *what*, not *how*. New files without it blocked.

## CONTEXT.md Convention

Line 2 must be `> Short description` (auto-extracted for parent Routing table).
`## Routing` block auto-managed by `context_synchronizer.py` between `<!-- routing:start -->` / `<!-- routing:end -->` — **do not edit manually**. Renames not tracked; update description manually.

## Setup

Dev environment, per-project quick-start, facade templates: [SETUP.md](SETUP.md)

## Core Files
Each project MUST have a CONTEXT.md root file and a README.md file.
In addition, it CAN have:
- SPECS.md — architecture decisions and design rationale (WHY, not WHAT)
- ROADMAP.md — pending milestones with agent-ready technical context
- SETUP.md — dev environment setup from scratch
- HISTORY.md — archive of completed milestones (moved from ROADMAP.md)

Skeletons for all five files: [`_templates/`](_templates/)

## Git Structure

Projects inside `Code/` have own git repos. Commit: `git -C <project-path> commit`.

All projects follow Git Flow (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`). Branching rules: [SPECS.md](SPECS.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`apptime/`](apptime/CONTEXT.md) | Android app to reduce phone addiction through awareness, without blocking |
| [`corpora/`](corpora/CONTEXT.md) | Real-time 3D computer vision research pipeline — depth, pose, segmentation from  |
| [`flows/`](flows/CONTEXT.md) | Graph-based workflow execution engine — typed slots, YAML-defined flows, pluggab |
| [`futebots/`](futebots/CONTEXT.md) | Multi-agent football simulation with genetic algorithm agent evolution |
| [`isometric-perspective/`](isometric-perspective/CONTEXT.md) | — |
| [`isoroll-content/`](isoroll-content/CONTEXT.md) | Offline asset generation pipeline for the isoroll Foundry VTT module |
| [`isoroll-module/`](isoroll-module/CONTEXT.md) | Foundry VTT v14 isometric projection module — TypeScript + Vite + SCSS. |
| [`ppc/`](ppc/CONTEXT.md) | Interactive browser tool for experimenting with LC/UFRPE curriculum redesign |
| [`shortvid/`](shortvid/CONTEXT.md) | Desktop video editor for short-form content — chroma-key, timeline, WebM export |
| [`voti/`](voti/CONTEXT.md) | Political alignment tool comparing user answers to real deputy voting records |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`prog1/main.py`](prog1/main.py) | — | — | ← add first-line comment |
<!-- routing:end -->
