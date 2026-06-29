# Code — Specs
> Engineering conventions, architecture decisions, and process rules for all code/ projects.

## Hook Enforcement Reference

What hooks block vs what you must self-enforce:

| Hook | Trigger | What it does |
|------|---------|-------------|
| `pre-edit.py` | Any Edit/Write | Hard-blocks: file exceeds 200 LOC; new file missing first-line description |
| `facade-scan.py` | Write (new files only) | Prints existing exports from target module's facade — verify no duplication before proceeding |
| `post-edit.sh` | Any Edit/Write | Regenerates `.d.ts`/`.pyi`/`.dart.api`; syncs `CONTEXT.md` routing block |
| `pre-read.sh` | Any Read | Redirects source reads to interface file (`.d.ts`/`.pyi`) when interface is current |
| `pre-commit` | git commit | LOC check, facade boundary check, first-line comment, stub generation, CONTEXT.md sync |
| `pre-commit` (§10) | git commit | **Hard-blocks** commit if staged `.ts`/`.tsx` under `code/` has ESLint R1-R6 violations |
| `post-edit.sh` (ESLint) | Any Edit/Write to `code/**/*.ts` | Prettier auto-formats in-place; ESLint R1-R6 violations printed as warnings (non-blocking) |

Full wiring details: [`/SETUP.md`](/SETUP.md#claude-code-hooks-claudesettingsjson)

## Engineering Constraints

These are enforced by code review, not hooks. Violation = redo before continuing.

- **One responsibility per file** — if you need to describe a file with "and", split it
- **Never copy-paste** — if the same logic appears twice, extract a function or class first
- **Names must be guessable** — file, class, function, variable names without opening the file
- **Flat over deep** — prefer sub-modules over nested directories beyond 2 levels
- **After each prompt** — is the code cleaner or messier than before? If messier, redo

## Style Rules (R1-R6)

Enforced for TypeScript projects via ESLint (`code/eslint.shared.js` + project `eslint.config.js`). Python/other languages: induced via this doc.

| Rule | Description | ESLint enforcement |
|------|-------------|-------------------|
| **R1** | One statement per line — no semicolon-separated statements | `max-statements-per-line` + `curly` |
| **R2** | One function/method call per statement — no nested calls `foo(bar())`, no method chaining `arr.filter().map()`. Use intermediate variables | `local/one-call-per-statement` |
| **R3** | Single return per function — use if/else to collect result in variable | `local/single-return` |
| **R4** | No untyped casts — no `as any` in TS, no `# type: ignore` in Python without explanation | `@typescript-eslint/no-explicit-any` |
| **R5** | Max 40 lines per function/method (blank lines and comments excluded) | `max-lines-per-function` |
| **R6** | Max 2 property accesses from root — `a.b.c` is the limit; `a.b.c.d` must be split: `const x = a.b.c; x.d` | `local/max-chain-depth` |

**Canonical shared config:** `code/eslint.shared.js` — exports `localPlugin` (3 custom rules) and `sharedRules`. Each TS project imports both.

**Enforcement hooks:**
- `post-edit.sh` — runs Prettier (auto-format) and surfaces ESLint violations after every edit (non-blocking)
- `pre-commit` — hard-blocks commit if any staged TS file under `code/` has ESLint errors

**Why these rules?** Dense compressed lines force agent to rebuild context before proposing fixes. Each nested call or chained method adds AST depth that must be unwound. Single-return and intermediate variables keep every expression flat and independently debuggable. The effect is shorter debugging sessions and fewer context-limit hits.

## File Size Policy

Applies to `.js .ts .tsx .py .dart .html .css .scss`:

| Threshold | Action |
|-----------|--------|
| Under 100 LOC | Target — ideal file size |
| 150 LOC | Warning at commit (hook warns, does not block) |
| 200 LOC | Hard block — commit and AI edits rejected |

Near limits: extract modules, separate orchestration from implementation logic.

## First-Line Description

Every code file must start with a one-line description comment. New files without it are blocked by `pre-edit.py`.

| Language | Format |
|----------|--------|
| Python / YAML / TOML | `# Short description` |
| JS / TS / Dart | `// Short description` |
| CSS / SCSS | `/* Short description */` |
| HTML | `<!-- Short description -->` |
| LaTeX | `% Short description` |
| Markdown | `# Title` (heading is the description) |

One sentence, no period, ≤80 chars. Describe *what*, not *how*.

## Project File Structure

Each project MUST have:
- `CONTEXT.md` — routing + architecture entry point
- `README.md` — human-facing project overview

Each project CAN have:
- `SPECS.md` — architecture decisions and design rationale (WHY, not WHAT)
- `ROADMAP.md` — pending milestones with agent-ready technical context
- `SETUP.md` — dev environment setup from scratch
- `HISTORY.md` — archive of completed milestones (moved from ROADMAP.md)
- `KNOWN-BUGS.md` — tracked bugs with reproduction steps

Skeletons for all files: [`_templates/`](_templates/)

## Facade Pattern

Every folder with source files exposes a **facade** — the single entry point through which all external consumers import. Nothing imports internal files from another module directly.

**Per-language convention:**

| Language | Facade file | Notes |
|----------|-------------|-------|
| TypeScript / JS | `index.ts` / `index.js` | Explicit named re-exports only — no `export *` (breaks tree-shaking) |
| Python | `__init__.py` | Explicit `__all__` required |
| Dart | `index.dart` | `export '...' show ...` pattern |
| SCSS | `_index.scss` | `@forward` only |
| Java / Kotlin | `package-info.java` / package object | Access modifiers are the facade — `public` = API, `package-private` / `internal` = hidden. No extra file needed; the compiler enforces it. |

**Rules:**
- Facade re-exports only the public API — internal helpers stay invisible
- Cross-folder imports that target a non-facade file → **hard block at commit** (`check-facade-imports.py`)
- Intra-folder imports (within the same module) always allowed
- Circular dependencies → fix the architecture, not the import rule

**Exempt from enforcement:** test files, the facade file itself, `generated/` and `vendor/` dirs.

**Reading facades:** `index.ts` / `__init__.py` / `index.dart` are read directly — `pre-read.sh` does not block them. They are already minimal interfaces. Implementation files are redirected to their `.d.ts` / `.pyi` / `.dart.api` interface instead.

See [SETUP.md](SETUP.md) for facade templates per language.

## Git Branching (Git Flow)

All projects under `code/` follow Git Flow:

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready, tagged releases only |
| `develop` | Integration branch — all features merge here |
| `feature/<name>` | New work — branch from `develop`, merge back to `develop` |
| `release/<version>` | Stabilization — branch from `develop`, merge to `main` + `develop` |
| `hotfix/<name>` | Urgent fix — branch from `main`, merge to `main` + `develop` |

**Rules:**
- Never commit directly to `main`
- `develop` must always build and pass tests
- Feature branches: short-lived, one concern each
- Merge via PR — no direct pushes to `develop` or `main`
- Tag `main` on every release: `v<semver>`
