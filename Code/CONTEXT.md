# Code
> Software projects developed under this workspace

**Before editing any file:**
1. Read the target project's CONTEXT.md.
2. Read the facade (`index.ts` / `__init__.py`) of every module you'll touch.
3. Language/pattern rules and file templates: [SPECS.md](SPECS.md).

**Hooks enforce automatically** (no need to re-check):
- File size: warn at 150 LOC, hard block at 200 LOC
- Cross-folder imports only through `index` / `__init__` (facade boundary)
- New files require first-line description comment
- Interface stubs (`.d.ts`, `.pyi`, `.dart.api`) regenerated at commit

**You enforce** (hooks cannot catch these):
- One responsibility per file — never copy-paste, extract a function instead
- After each prompt: code cleaner or messier? If messier, redo before continuing
- Names must be guessable without opening the file

**Git**: projects use own repos — `git -C <project-path> commit`. Git Flow branching.
**New project**: needs `CONTEXT.md` + `README.md`. Templates: [`_templates/`](_templates/).
**CONTEXT.md files**: line 2 = `> description`. Routing block auto-managed — do not edit manually.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`_templates/`](_templates/CONTEXT.md) | [One-line description — REQUIRED on line 2; auto-extracted for parent routing ta |
| [`apptime/`](apptime/CONTEXT.md) | Android app to reduce phone addiction through awareness, without blocking |
| [`corpora/`](corpora/CONTEXT.md) | Real-time 3D computer vision pipeline — depth, pose, segmentation from webcam |
| [`flows/`](flows/CONTEXT.md) | Graph-based workflow engine — typed slots, YAML-defined flows, pluggable agents |
| [`futebots/`](futebots/CONTEXT.md) | Multi-agent football simulation with genetic algorithm agent evolution |
| [`isometric-perspective/`](isometric-perspective/CONTEXT.md) | Legacy Foundry VTT isometric perspective fork — v0.7.7, JS, pre-isoroll-module |
| [`isoroll-content/`](isoroll-content/CONTEXT.md) | Offline asset generation pipeline for the isoroll Foundry VTT module |
| [`isoroll-module/`](isoroll-module/CONTEXT.md) | Foundry VTT v14 isometric projection module — TypeScript + Vite + SCSS. |
| [`ppc/`](ppc/CONTEXT.md) | Interactive browser tool for experimenting with LC/UFRPE curriculum redesign |
| [`prog1/`](prog1/CONTEXT.md) | — |
| [`prog1_novo/`](prog1_novo/CONTEXT.md) | — |
| [`shortvid/`](shortvid/CONTEXT.md) | Desktop video editor for short-form content — chroma-key, timeline, WebM export |
| [`voti/`](voti/CONTEXT.md) | Political alignment tool comparing user answers to real deputy voting records |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SETUP.md`](SETUP.md) | — | — | Code Setup |
| [`SPECS.md`](SPECS.md) | — | — | Code — Specs |
<!-- routing:end -->
