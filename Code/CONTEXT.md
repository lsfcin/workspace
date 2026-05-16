# Code
> Software projects developed under this workspace

## Engineering Principles

- **One responsibility per file** — prefer many small files over monoliths; think file-size limits ahead.
- **Explicit naming** — file names must be guessable without opening them.
- **Flat structure** — sub-modules over deep nesting; max 3 directory levels.
- **Low coupling** — small modules with explicit imports; no hidden cross-directory coupling.
- **Interface-first reading** — read `.pyi` / `.d.ts` / `.dart.api` before source files (enforced by hook).

## File Size Policy

Applies to `.js .ts .tsx .py .dart .html .css .scss`:

- Target: under **100 LOC**
- Warning at **150 LOC** (hook warns on commit)
- Hard block at **200 LOC** (commits and AI edits blocked)

When approaching limits: extract modules, separate orchestration from implementation.

## First-Line Description

Every code file must begin with a one-line description comment:

| Language | Format |
|----------|--------|
| Python / YAML / TOML | `# Short description` |
| JS / TS / Dart | `// Short description` |
| CSS / SCSS | `/* Short description */` |
| HTML | `<!-- Short description -->` |
| Markdown | `# Title` (heading IS the description) |
| LaTeX | `% Short description` |

One sentence, no period, ~80 chars. Describe *what*, not *how*. New files without it are blocked.

## CONTEXT.md Convention

Line 2 must be `> Short description` (auto-extracted for parent Routing table).
The `## Routing` block at the end is auto-managed by `context_synchronizer.py` between `<!-- routing:start -->` / `<!-- routing:end -->` — **do not edit manually**. Renames are not tracked; update the description manually.

## Git Structure

Projects inside `Code/` have their own git repos. Commit there: `git -C <project-path> commit`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`apptime/`](apptime/CONTEXT.md) | Android app to reduce phone addiction through awareness, without blocking |
| [`corpora/`](corpora/CONTEXT.md) | Real-time 3D computer vision research pipeline — depth, pose, segmentation from  |
| [`flows/`](flows/CONTEXT.md) | Graph-based workflow execution engine — typed slots, YAML-defined flows, pluggab |
| [`futebots/`](futebots/CONTEXT.md) | Multi-agent football simulation with genetic algorithm agent evolution |
| [`isoroll/`](isoroll/CONTEXT.md) | Foundry VTT isometric-play module and offline asset generation pipeline |
| [`ppc/`](ppc/CONTEXT.md) | Interactive browser tool for experimenting with LC/UFRPE curriculum redesign |
| [`shortvid/`](shortvid/CONTEXT.md) | Desktop video editor for short-form content — chroma-key, timeline, WebM export |
| [`voti/`](voti/CONTEXT.md) | Political alignment tool comparing user answers to real deputy voting records |
<!-- routing:end -->
