# Code — Specs
> Engineering conventions, architecture decisions, and process rules for all Code/ projects.

## Facade Pattern

Every folder with more than one source file exposes a **facade** — the single entry point through which all external consumers import. Nothing imports internal files from another module directly.

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

See [SETUP.md](SETUP.md) for facade templates per language.

## Git Branching (Git Flow)

All projects under `Code/` follow Git Flow:

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
