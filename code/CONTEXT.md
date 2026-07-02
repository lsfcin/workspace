# Code
> Software projects developed under this workspace

You are a SENIOR software architect, your code WILL be evaluated!

**Before editing any file:**
1. Read it first. Before modifying a function, grep for all callers. Research before you edit.
2. Read the target project's CONTEXT.md.
3. For architecture/flow questions, use `codegraph` (via Bash) before reading raw source — projects with a `.codegraph/` index are indexed; see [SETUP.md](SETUP.md#codegraph).
4. Read the facade (`index.ts` / `__init__.py`) of every module you'll touch — `facade-gate` will block edits until you do.
5. Language/pattern rules and file templates: [SPECS.md](SPECS.md).

**codegraph** — most projects indexed; call via Bash (no MCP). Index auto-syncs after every edit via post-edit hook. Command reference: [SETUP.md](SETUP.md#codegraph).

**Hooks enforce automatically** (no need to re-check):
- CONTEXT.md chain of the target subtree must be Read before any file access (context-gate)
- File size: warn at 150 LOC, hard block at 200 LOC
- Cross-folder imports only through `index` / `__init__` (facade boundary)
- New files require first-line description comment
- Interface stubs (`.d.ts`, `.pyi`, `.dart.api`) regenerated at commit
- Duplicated blocks involving staged files block the commit (jscpd) — extract, never copy
- Projects declaring `verify:fast` must be green to commit; KNOWN-BUGS FIXED flips require a `test/**/b<N>-*` regression spec (see workspace [VERIFY.md](../VERIFY.md))

**You enforce** (hooks cannot catch these):
- REUSE always
- NEVER copy-paste, instead, REFACTOR, extract a function or class
- ONE responsibility per file - SMALL IS BETTER
- Style rules R1-R6 apply to ALL languages — TypeScript has ESLint enforcement, Python/others are induced. See [SPECS.md](SPECS.md#style-rules-r1-r6) for the full table
  - **R1** One statement per line
  - **R2** One function/method call per statement — no `foo(bar())`, no `arr.filter().map()`; use intermediate variables
  - **R3** Single return per function
  - **R4** No untyped casts (`as any`, `# type: ignore`)
  - **R5** Max 40 lines per function
  - **R6** Max 2 property accesses from root (`a.b.c` limit; split `a.b.c.d` into two statements)
- REFACTOR after each coding prompt, report only AFTER refactoring
- Names must be guessable, no need to open the file, read the function or inspect the variable

**Git**: projects use own repos — `git -C <project-path> commit`. Git Flow branching.
**New project**: needs `CONTEXT.md` + `README.md`. Templates: [`_templates/`](_templates/).
**CONTEXT.md files**: line 2 = `> description`. Routing block auto-managed — do not edit manually.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`_templates/`](_templates/CONTEXT.md) | Project scaffolding templates — CONTEXT.md, README.md, SPECS.md, ROADMAP.md skel |
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
| [`programacao1/`](programacao1/CONTEXT.md) | Simulador de sociedade em Python puro. Duas camadas: (1) terminal CRUD de pessoa |
| [`shortvid/`](shortvid/CONTEXT.md) | Desktop video editor for short-form content — chroma-key, timeline, WebM export |
| [`voti/`](voti/CONTEXT.md) | Political alignment tool comparing user answers to real deputy voting records |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SETUP.md`](SETUP.md) | — | — | Code Setup |
| [`SPECS.md`](SPECS.md) | — | — | Code — Specs |
| [`eslint.shared.js`](eslint.shared.js) | — | `localPlugin`, `sharedRules`, `countCallsInSubtree`, `getChainDepth` | Shared ESLint rules for all TypeScript/JavaScript projects under code/ — R1-R6 style enforcement. |
<!-- routing:end -->
