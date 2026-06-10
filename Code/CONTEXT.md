# Code
> Software projects developed under this workspace

## Engineering Principles

- **High cohesion** — one CRISTAL CLEAR responsibility per file.
- **Minimize file LOC** — small is better! many small files over monoliths; think limits ahead.
- **Explicit naming** — file names guessable without opening, keep naming patterns.
- **Flat structure** — sub-modules over deep nesting.
- **Low coupling** — small modules, explicit imports; no hidden cross-directory coupling.
- **Facade boundaries** — cross-folder imports go through `index` / `__init__` only (enforced by hook).
- **Interface-first reading** — read `.pyi` / `.d.ts` / `.dart.api` before source files (enforced by hook).

## Facade Pattern

Every folder with more than one source file exposes a **facade** — the single entry point through which all external consumers import. Nothing imports internal files from another module directly.

**Per-language convention:**

| Language | Facade file | Notes |
|----------|-------------|-------|
| TypeScript / JS | `index.ts` / `index.js` | Explicit named re-exports only — no `export *` (breaks tree-shaking) |
| Python | `__init__.py` | Explicit `__all__` required |
| Dart | `index.dart` | `export '...' show ...` pattern |
| SCSS | `_index.scss` | `@forward` only |

**Rules:**
- Facade re-exports only the public API — internal helpers stay invisible
- Cross-folder imports that target a non-facade file → **hard block at commit** (`check-facade-imports.py`)
- Intra-folder imports (within the same module) always allowed
- Circular dependencies → fix the architecture, not the import rule

**Exempt from enforcement:** test files, the facade file itself, `generated/` and `vendor/` dirs.

See [Code/SETUP.md](SETUP.md) for facade templates per language.

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
