# Code

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

Enforced by `.hooks/pre-commit` at commit time; mirrored here as a behavioral instruction.

| Lines | Signal | Action |
|-------|--------|--------|
| ≥ 150 | ⚠ Check | Evaluate single responsibility. Assess cohesion and coupling. |
| ≥ 300 | 🚨 Refactor | File likely carries multiple responsibilities. Split before next session. |

**Claude instruction**: when reading any source file over 150 lines, evaluate single responsibility before proceeding. Over 300 lines, propose a concrete refactor plan before implementing new features in that file.

## Interface Files

Each language has a native interface format — a compact public-API summary readable instead of the full implementation:

| Language | Format | How to generate |
|----------|--------|-----------------|
| Python | `.pyi` stubs | `stubgen <file.py> -o <same-dir>/` — auto-staged by pre-commit hook |
| TypeScript | `.d.ts` declarations | Add `"declaration": true, "declarationDir": "types"` to `tsconfig.json`; run `tsc --declaration --emitDeclarationOnly` |
| Dart/Flutter | Abstract classes | No auto-generation — declare interfaces explicitly in `lib/core/interfaces/` |

Read the interface file first. Open the `.py` / `.ts` / `.dart` only when you need to understand *how*, not *what*.

## CONTEXT.md Convention

Every project and significant sub-module has a `CONTEXT.md` containing a **File Map**: one line per source file describing its single responsibility. Start there before opening any source file. When a directory grows beyond ~5 files, give it its own `CONTEXT.md`.
