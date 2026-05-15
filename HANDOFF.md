# Handoff — Modularization Stress Test

## What this is
A multi-session project applying workspace quality policies to all 8 projects under `Code/`.
The full tracking file is `ROADMAP.md` at this root. Read it for detailed per-file history.

---

## Phase status

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Interface generation (.pyi, .d.ts, .dart.api) | ❌ Pending |
| 2 | Critical splits (>500 lines) | ✅ Done |
| 3 | Moderate splits (200–300 lines, no commit-blocking files remain) | ✅ Done |
| 4 | First-line description comments on every source file | ✅ Done |
| 5 | CONTEXT.md File Maps in every project directory | ✅ Done (41 files) |

Phase 1 is the only incomplete phase. The pre-commit hook auto-generates stubs on commit
(stubgen for .py, tsc for .js/.ts, dart-api-extract for .dart), so it runs itself over time.
A manual batch run is possible — see `SETUP.md`.

---

## Open policy decision (resolve first in next session)

**The line limit rule needs to be redesigned.** Current state:
- Hook warns at 200 lines, blocks commit at 300 lines
- "Exceptions" were granted for: test files, ML architecture files, data/string-table files, `part of` split fragments, legacy UI
- The hook is **incremental only** — it checks staged files per commit, not the full tree. Files already committed at large sizes are invisible to it.

**Owner's direction:** move toward a hard 200-line (or stricter: 100, 80, 50) limit with no
exceptions. The intent is to force graph-like design — small single-responsibility nodes with
explicit edges (imports). Data files and test files are not exempt; they should also be split.

**Key questions for next session:**
1. What is the target limit? (200 / 100 / 80 / 50)
2. Do data files (insight lists, l10n strings) split by semantic category or stay exempt?
   - Current insights split: `insights_data_1` (Sleep/Dopamine/Attention/MentalHealth/Productivity)
     vs `insights_data_2` (Exercise/Social/Neuroscience/Childhood/Wellbeing) — numeric, not semantic.
   - Better split would be by topic cluster, not count. User suggested "problem vs solution" framing.
3. Should the hook gain a `--audit` mode that scans the full tree (not just staged files)?

---

## Current violations (files >200 lines, not yet split)

Run this to get fresh numbers:
```bash
find /mnt/workspace/Code -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.dart" | \
  grep -v "node_modules\|\.d\.ts\|\.pyi\|\.next\|build/" | \
  xargs wc -l 2>/dev/null | awk '$1 >= 200' | sort -rn | grep -v " total"
```

Key offenders at session close:
- **flows/engine/ui/app.js** (938) — legacy React-era UI, superseded by `src/`. Skipped so far.
- **test files** (257–483) — `test_ui_m10.py`, `test_benchmark_m8.py`, etc. Were treated as exempt.
- **corpora ML files** (222–415) — `dinov2.py`, `block.py`, `dpt.py`, `transform.py`. Were treated as exempt.
- **apptime `part of` fragments** (250–289) — `tab_day_charts.dart`, `monitoring_screen_widgets.dart`, etc. These are split output files; the primary file is compact.
- **apptime l10n** (233–236) — `app_localizations_en.dart`, `app_localizations_pt.dart`. String tables.
- **apptime insights data** (213–229) — `insights_data_1.dart`, `insights_data_2.dart`.
- **apptime screens** (231–289) — `storage_service.dart`, `settings_screen.dart`, `monitoring_screen.dart`, `insights_screen.dart`, `onboarding_screen.dart`, `per_app_screen.dart`, `tab_week.dart`
- **voti components** (232–286) — `votingAnalyzer.ts`, `PoliticiansGrid.tsx`, `SimpleQuiz.tsx`, `VotingAnalysisComponent.tsx`, `DeputyPhotoExtractor.tsx`
- **flows/start.py** (230)

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

## Hook location and behavior

```
/mnt/workspace/.hooks/pre-commit
```
- Runs on `git commit` against staged files only (`git diff --cached`)
- WARN_LINES=200, CRITICAL_LINES=300 (currently)
- Also auto-runs: ctx-sync.py, stubgen, tsc, dart-api-extract on commit

To change the thresholds, edit lines 8–9 of the hook file.

---

## Projects and their repos

Each project under `Code/` is its own git repo. To commit inside one:
```bash
git -C /mnt/workspace/Code/<project> add -p
git -C /mnt/workspace/Code/<project> commit -m "..."
```
The workspace repo (`/mnt/workspace`) tracks only structural files (CLAUDE.md, CONTEXT.md, hooks).

---

## Suggested next session opening

> Read HANDOFF.md at /mnt/workspace/HANDOFF.md. Then:
> 1. Decide the new line limit (100? 80?) and whether any categories stay exempt.
> 2. Update the pre-commit hook thresholds.
> 3. Split the remaining violations under the new limit.
> Start by showing me the current violation list grouped by project.
