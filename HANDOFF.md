# Handoff — Modularization Stress Test (Archived)

## What this was
A multi-session project applying workspace quality policies to all 8 projects under `Code/`.
All phases are complete. This file is kept as an archive record.

---

## Phase status (final)

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Interface generation (.pyi, .d.ts, .dart.api) | ❌ Partial — see Per-Project table |
| 2 | Critical splits (>500 lines) | ✅ Done |
| 3 | Moderate splits (warning-band files, no hard-blocking files remain) | ✅ Done |
| 4 | First-line description comments on every source file | ✅ Done |
| 5 | CONTEXT.md Routing blocks in every project directory | ✅ Done (41 files) |

Phase 1 is incomplete for some projects. The pre-commit hook auto-generates stubs on commit,
so it runs itself over time. A manual batch run is possible — see `SETUP.md`.

---

## Per-Project Status (at close)

| Project | Interface | Size | Comments | CONTEXT.md | Status |
|---------|-----------|------|----------|------------|--------|
| ppc | ✅ 100% | ✅ 0 violations | ✅ 100% | ✅ | Complete |
| futebots | ❌ 0% | ✅ 0 violations | ✅ 100% | ✅ | Only interfaces pending |
| isoroll | ❌ 0% | ✅ 0 violations | ✅ 100% | ✅ | Only interfaces pending |
| corpora | ❌ 0% | ✅ 0 violations* | ✅ 100% | ✅ | Only interfaces pending |
| shortvid | ❌ 0% | ✅ 0 violations | ✅ 100% | ✅ | Only interfaces pending |
| voti | ✅ .d.ts | ✅ 0 violations | ✅ 100% | ✅ | Only .pyi pending |
| apptime | ✅ .dart.api | ✅ 0 violations | ✅ 100% | ✅ | Only .pyi pending |
| flows | ✅ .pyi | ✅ 0 violations | ✅ 100% | ✅ | Complete |

*corpora ML architecture files (dinov2.py etc.) exempt — interconnected model layers

---

## Technical patterns used (for consistency)

**Dart splits:** use `part`/`part of` — the fragment shares library scope (including private names).
Main file declares `part 'fragment.dart';`. Fragment declares `part of 'main.dart';`. No imports needed between them.

**Python splits:** re-export from the original module so callers don't break:
```python
# original.py
from ._new_module import SomeClass
__all__ = ["SomeClass", ...]
```

**TypeScript splits:** re-export types with `export type { Foo } from './types'` in the original file.

**Dart extension splits:** private methods of a State class can move to a `part of` file as an
extension — BUT extensions cannot access private members (`_foo`) of the extended class.
Workaround: use `widget.storage` instead of `_s`, or make the shorthand non-private.

---

## Line-limit policy

Thresholds live in `.hooks/line-limits.env`. To change them, edit that file only — both `pre-edit.py`
and `check-line-counts.sh` read from it automatically. See `SETUP.md § Policy Decisions` for the
full rationale and exempt categories.

---

## Infrastructure changes (post-archival)

Applied after the modularization project closed:

- `.hooks/ctx-sync.py` → `.hooks/context_synchronizer.py`; `.hooks/ctx_sync_ext.py` → `.hooks/workspace_scanner.py`
- Routing block sentinels renamed: `<!-- ctx-sync:routing:start/end -->` → `<!-- routing:start/end -->` — all CONTEXT.md files migrated automatically via `migrate_legacy()` on first sync
- `context_synchronizer.py` now always appends the routing block at end of file (idempotent; moves it if found mid-file)
- Added `.hooks/check-line-counts.sh` (standalone audit tool; also called by pre-commit) and `.hooks/line-limits.env` (single source of truth for `WARN_LINES` / `BLOCK_LINES`)
- `Code/CONTEXT.md` trimmed 95 → 59 lines: merged Engineering Principles + Modularization Strategy, removed Interface-First table, compressed CONTEXT.md Convention

---

## Projects and their repos

Each project under `Code/` is its own git repo. To commit inside one:
```bash
git -C /mnt/workspace/Code/<project> add -p
git -C /mnt/workspace/Code/<project> commit -m "..."
```
The workspace repo (`/mnt/workspace`) tracks only structural files (CLAUDE.md, CONTEXT.md, hooks).
