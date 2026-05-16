# Interface Policy — Implementation Roadmap
> Universal interface generation and enforcement across all supported languages

## Status
**Complete** ✓

## Phase 1 — Generation (post-edit.sh)
- [x] Python `.py` → `.pyi` via stubgen
- [x] JavaScript `.js` → `.d.ts` via tsc --allowJs
- [x] TypeScript `.ts` → `.d.ts` via tsc
- [x] Dart `.dart` → `.dart.api` via dart-api-extract.py
- [x] Auto-scaffold `jsconfig.json` when first `.js` file written in a dir
- [x] Auto-scaffold `tsconfig.json` when no ancestor config found for `.ts`

## Phase 2 — Enforcement (pre-read.sh)
- [x] Python `.py` → block if `.pyi` is current
- [x] JavaScript `.js` → block if `.d.ts` is current
- [x] TypeScript `.ts` → block if `.d.ts` is current
- [x] TypeScript `.tsx` → block if `.d.ts` is current
- [x] Dart `.dart` → block if `.dart.api` is current

## Phase 3 — Dart extractor (new: dart-api-extract.py)
- [x] Created `.hooks/dart-api-extract.py`
  - Extracts: public class/mixin/abstract/enum/extension names + hierarchy
  - Extracts: public member signatures (indent-based, skips `_`-prefixed)
  - Output: `<stem>.dart.api` compact text (signatures only, not valid Dart)
  - Idempotent; handles syntax edge cases without crashing

## Phase 4 — context_synchronizer.py
- [x] Fixed Dart interface lookup: `.dart` → `.dart.api`
- [x] TypeScript `.ts` → `.d.ts` correct

## Phase 5 — Documentation
- [x] Updated `Code/CONTEXT.md` Interface Files table to ideal state
- [x] Update `SETUP.md` tsc PATH section

## Verification
- [x] JS/TS: ctx-sync correctly links `.d.ts` for all 7 ppc JS files
- [x] Dart: extractor generates clean `.dart.api` (tested on goal_config, main_screen, insights)
- [x] Dart enforcement: timestamp logic correctly hard-blocks when interface is current
- [ ] TS generation: needs a real `.ts` file edit to trigger end-to-end test
