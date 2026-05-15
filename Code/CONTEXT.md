# Code
> Software projects developed under this workspace

Software projects developed under this workspace.

## Projects

| Project | Stack | Status |
|---------|-------|--------|
| [flows](flows/CONTEXT.md) | Python | Active — V1 in progress |
| [apptime](apptime/CONTEXT.md) | Flutter + Kotlin | Active — pre-release |
| [voti](voti/CONTEXT.md) | Next.js / TypeScript | Active |
| [corpora](corpora/CONTEXT.md) | Python / PyTorch | Research — 3D CV pipeline |
| [futebots](futebots/CONTEXT.md) | Python | Experiment — multi-agent simulation |
| [isoroll](isoroll/CONTEXT.md) | Python / ComfyUI | Active — asset generation pipeline |
| [shortvid](shortvid/CONTEXT.md) | Python / PySide6 | Active — desktop video editor |
| [ppc](ppc/CONTEXT.md) | Vanilla HTML / Alpine.js | Active — LC/UFRPE curriculum redesign tool |

## Engineering Principles

- **Flat structure**: one responsibility per file; prefer many small files over monoliths.
- **Explicit naming**: file names should make contents guessable without opening them.
- **Horizontal hierarchy**: sub-modules over deep nesting; avoid directory trees beyond 3 levels.
- **Interface-first reading**: read interface files (`.pyi`, `.d.ts`) before implementation files.

## File Size Policy

Enforced by `.hooks/pre-commit` at commit time (300+ lines blocks the commit) and by `claude-pre-edit.py` during every Claude session (200+ lines blocks the edit). Both thresholds apply to code files only (`.js .ts .tsx .py .dart .html .css .scss`).

| Lines | Signal | Action |
|-------|--------|--------|
| ≥ 200 | ⚠ Block (Claude session) | Claude Code hook rejects the edit. Create a new module first. |
| ≥ 300 | 🚨 Block (git commit) | Commit is rejected. Split before continuing. |

**Claude instruction — HARD RULE**: before writing code to any file, check its current line count. If your addition would push it past 200 lines, create a new module file first and write there. Never grow an existing file past 200 lines. If a file is already over 300 lines, refuse to add features and propose a concrete split immediately. This rule is not advisory — do not skip it, do not ask for permission to skip it.

## Modularization Strategy

**Claude instruction — STRATEGIC RULE**: the 200-line gate is a symptom detector, not a design tool. When it fires — or before it fires — reason about module boundaries using these criteria, in order:

1. **One reason to change per file.** A file is correctly scoped if you can name exactly one external event that would cause you to edit it. If two different features, layers, or stakeholders could independently require changes to the same file, that file must become two files. This is the primary criterion. Line count is a proxy; this is the cause.

2. **Separate stable from volatile code first.** Before anything else, identify what almost never changes: constants, lookup tables, pure utility functions, type definitions. Isolate these immediately. A future task touching business logic should never need to open a constants file. Volatile code (business rules, UI state, integration adapters) changes often — keep it small, close to its feature, and easy to find.

3. **Minimize the import surface of every new module.** Count imports before finalizing a split. A module with 2-3 imports is well-bounded. A module with 8+ imports is doing too much or is in the wrong layer. High fan-in (many things import it) is a sign of a well-designed stable abstraction. High fan-out is a coupling smell.

4. **Design for the next task's scope.** Before writing code, ask: "what will the next feature in this area need to touch?" Good boundaries mean a future task reads and edits 1-2 files, not 5. If you can predict that constraint logic, state management, and data loading will be independently touched, isolate them now.

5. **Name modules by responsibility, not by implementation detail.** `grade-validator.js` is a module boundary. `utils.js` is not. The name must tell a future reader exactly what is inside and, equally important, what is not. If you cannot write a one-clause name, the module boundary is not yet clear.

When the gate fires, do not split at an arbitrary line. Stop, apply this reasoning, find the natural seam, and split there.

## Interface Files

Each language has a native interface format — a compact public-API summary readable instead of the full implementation:

| Language | Format | Generation | Enforcement |
|----------|--------|------------|-------------|
| Python | `.pyi` stubs | Auto — `stubgen` on every `.py` save | Hard-block if `.pyi` current; warn if stale |
| JavaScript | `.d.ts` declarations | Auto — `tsc --allowJs --emitDeclarationOnly` on every `.js` save; `jsconfig.json` auto-scaffolded if missing | Hard-block if `.d.ts` current; warn if stale |
| TypeScript | `.d.ts` declarations | Auto — `tsc --emitDeclarationOnly` on every `.ts` save; `tsconfig.json` auto-scaffolded if no ancestor found | Hard-block if `.d.ts` current; warn if stale |
| Dart/Flutter | `.dart.api` stubs | Auto — `dart-api-extract.py` on every `.dart` save; extracts public class/mixin/method signatures | Hard-block if `.dart.api` current; warn if stale |

**Generation is universal — every save of a supported file produces an interface file, unconditionally.**

**Enforcement** (`claude-pre-read.sh`): when a source file has a companion interface that is **current** (interface timestamp ≥ source timestamp), reading the source is **hard-blocked** — you must read the interface first. If the source was modified after the interface was generated (stale), a warning is shown and the read is allowed. This ensures interface-first reading is not advisory but enforced whenever the interface is trustworthy.

**jsconfig.json / tsconfig.json** are auto-scaffolded by the hook for IDE tooling. Generation itself always uses the direct CLI and does not depend on these files.

## First-Line Description Convention

**Every code file must have a one-line description comment as its very first line.** This is the canonical description of the file — it is read by `ctx-sync.py` and written into CONTEXT.md automatically. It travels with the file if it is moved or renamed.

| Language / Format | First-line format |
|-------------------|-------------------|
| Python | `# Short description` |
| JavaScript / TypeScript / Dart | `// Short description` |
| CSS / SCSS | `/* Short description */` |
| HTML | `<!-- Short description -->` |
| Markdown (`.md`) | `# Title of this document` |
| YAML / TOML | `# Short description` |
| LaTeX (`.tex`) | `% Short description` |

Rules: one sentence, no period, fits in ~80 chars. Describe *what* the file is responsible for, not *how* it works. For `.md` files the heading IS the description — `ctx-sync.py` extracts it as such and it appears in the File Map.

Enforcement (three layers, in order of when they fire):
1. **Write (new file) → hard block**: `claude-pre-edit.py` rejects the Write if the content doesn't start with a description comment. The file cannot be created without it.
2. **Edit (existing file) → in-session reminder**: `claude-post-edit.sh` checks line 1 after every edit and prints a reminder if it is missing. Non-blocking — but fires immediately in-session.
3. **git commit → warning**: `pre-commit` warns when a newly staged code file lacks the comment.

## CONTEXT.md Convention

**Every `CONTEXT.md` must have a one-line description as line 2**, directly after the title heading, in blockquote format:
```markdown
# Module Name
> Short description of what this directory contains
```
This description is auto-extracted by `ctx-sync.py` and used as the Sub-modules table entry in the parent CONTEXT.md. Enforcement: `claude-pre-edit.py` hard-blocks Write of a new CONTEXT.md without a line-2 description; `claude-post-edit.sh` reminds on Edit.

Every project and significant sub-module has a `CONTEXT.md`. A `## File Map` section (auto-managed by `ctx-sync.py`) lists all source files with their interface and description:

```
| File           | Interface      | API                    | Description                     |
|----------------|----------------|------------------------|---------------------------------|
| `app.js`       | `app.d.ts`     | `initApp`, `getState`  | Alpine component: core state    |
| `validators.js`| —              | `validateGrade`        | Grade constraint validators     |
```

- **File** links to the source (for editing)
- **Interface** links to the `.pyi`/`.d.ts` (read this first — it is the public API summary)
- **API** lists top-level public functions/classes extracted from the file automatically
- **Description** comes from the file's first-line comment; if missing, shows `← add first-line comment`

`ctx-sync.py` runs on every Claude edit (via `claude-post-edit.sh`) and on every git commit (via `pre-commit`). It tracks all meaningful file types — code (`.js .ts .py .dart .html .css .scss`) and content (`.md .yaml .yml .tex .toml`) — and adds new files, removes entries for deleted files, and warns when a directory exceeds 7 code files. **Renames are not detected automatically** — the old entry disappears and the new file appears with a placeholder; update the description manually. **Do not edit the block between `<!-- ctx-sync:auto:start -->
| File | Interface | API | Description |
|------|-----------|-----|-------------|
<!-- ctx-sync:auto:end -->` manually** — changes will be overwritten on the next run.

**Subdirectory folding** — ctx-sync automatically handles subdirectories using a threshold rule:
- **Fold** (< 7 files, no own CONTEXT.md, no sub-subdirs): files appear in the parent's File Map with relative paths (`subdir/file.js`)
- **Link** (≥ 7 files, OR has own CONTEXT.md, OR has sub-subdirs with code): subdir gets its own CONTEXT.md (auto-created as scaffold if missing); a `## Sub-modules` section appears in the parent, auto-managed between `<!-- ctx-sync:sub:start -->
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
<!-- ctx-sync:sub:end -->` sentinels

The parent's Sub-modules section is also updated when you edit a file in a subdirectory (via parent re-sync in `claude-post-edit.sh`). Do not edit either sentinel block manually.

## Claude Code Hooks

Four scripts in `.hooks/` fire during every Claude coding session:

| Script | Trigger | Effect |
|--------|---------|--------|
| `claude-pre-edit.py` | PreToolUse: Edit, Write | **Hard-blocks** edits that would push code files past 200 lines; **hard-blocks Write of new files missing a first-line description comment** |
| `claude-post-edit.sh` | PostToolUse: Edit, Write | Regenerates `.pyi`/`.d.ts`; reminds about missing first-line comment on existing files; runs `ctx-sync.py` |
| `claude-pre-read.sh` | PreToolUse: Read | Non-blocking hint to read interface file before implementation |
| `ctx-sync.py` | Called by post-edit + pre-commit | Syncs CONTEXT.md File Map: adds new files, removes deleted entries, links interfaces |

**To bypass the size gate**: ask explicitly. Temporarily edit `LIMIT` in `claude-pre-edit.py`, or request user approval.
