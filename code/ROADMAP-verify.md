# VERIFY — Agent Verification & Enforcement Roadmap
> Testing-discipline rollout for `code/` projects: make agents verify their own results (no human
> eye per prompt) and enforce code centralization. Pilot: isoroll-module. Second: apptime.

**Lifecycle: transient initiative doc** (REFACTOR.md species, one level up — lives beside
`code/CONTEXT.md` instead of inside one project) — NOT workspace structure. Linked from root
`SETUP.md` and `code/CONTEXT.md` on purpose (this is where the verify:fast contract those files
enforce is tracked). Endstate: once every `code/` project has a real contract and A1 (apptime)
completes, surviving durable rules stay in `core/tools/verify/CONTEXT.md` (already done at W3)
and this file is deleted (git keeps it).

**Scope note:** the workspace-wide hook infrastructure this plan once carried (context-gate,
bash-gate) is the enforcement layer's own contract now —
[`core/hooks/SPECS.md`](../core/hooks/SPECS.md) — and not tracked here. What this
file scopes is the `code/` testing-pyramid rollout: brain/ and academy/ have no `verify:fast`
concept.

Origin: assessment session 2026-07-02. Diagnosis: workspace over-invests in context transfer
(docs, skills, codegraph, facades), zero in behavior verification. No test suite anywhere.
Fixes verified by human eyes in live sessions; verification evaporates at session end
(B32 puppeteer harness built, used once, thrown away). 200 LOC gate without a duplication
gate manufactures copies (z-order walk found in 5 places). Nondeterministic bugs (zIndex
ties → PIXI insertion order) unresolvable without a mechanical oracle.

---

## Principles

1. **Gate or injection — never induction.** Every rule either hard-blocks (exit 2) or is
   force-fed by the harness. Advisory text does not steer agents.
2. **Oracle over eyes.** Correctness checked by machine. Human checks novel visuals once,
   at feature birth; then golden-locked.
3. **State dump over pixels.** Assert on structured JSON dumps; pixels are the last tier.
4. **Diagnostics call live-path functions, never re-derive.** A debug view with its own
   math is a second implementation that can lie (06-30 debug-label saga).
5. **Every visually-confirmed bug exports its scene as a committed fixture.** Reproducible
   scene beats any description of "sometimes."
6. **Bug status flips only with executable proof.** FIXED requires a regression test.

## Locked Decisions (2026-07-02)

| Topic | Decision |
|-------|----------|
| Context gate style | Force actual Read call; deny message lists unread chain. No content embedding. |
| Compaction | PreCompact wipes seen-markers → chain re-read after compaction |
| Subagents | Inherit seen-state (markers keyed by `session_id`, shared) — no re-read |
| Scope | Whole workspace, all subtrees (code/, brain/, academy/, …) |
| 200 LOC cap | KEEP. Pair with duplication gate + rewritten block message |
| jscpd | Full block, no baseline file. Clones touching staged files block the commit |
| Pilot order | isoroll-module (long road), then apptime |

## Verification Tier Ladder

| Tier | What | Catches | Speed |
|------|------|---------|-------|
| T0 | tsc + eslint (exists) | type/style | s |
| T1 | unit + property tests on pure math (vitest + fast-check) | B32-class (geometry/logic) | s |
| T2 | headless functional: real app, scripted actions, assertions on structured state dumps | B33/B25/B2/B27-class (lifecycle, hooks, timing) | 30–60 s |
| T3 | deterministic screenshots + pixelmatch goldens; diff PNG artifact on failure (agent-readable) | render bugs invisible to state dumps | s/scene |

Contract script names (all code projects): **`verify:fast`** = T0+T1 (runs per commit),
**`verify:full`** = T2+T3 (pre-merge / on demand / roundup).

---

## Phase I4 — isoroll Unit Coverage Expansion 🔲

I1 covers the pure-math core only (iso-tile-depth, iso-tile-geom, coord-map). Expand T1 to
every module that is pure or cheaply fakeable; leave PIXI/DOM/hook-lifecycle behavior to T2
(unit-mocking Foundry there tests the mocks, not the code).

Unit-testable targets (pure / fake-with-TileMeshCoord-style stubs):
- `walls/wall-coords.ts` — anchor↔canvas roundtrips, elevation/imageOffset factoring
- `render/iso-geometry.ts` — footprint + volume-box vertex math (elevation, boundHeight)
- `core/util.ts` — elevToCanvas, screenToCanvas, gridDistance
- `render/fog-state.ts` — VISIBLE/EXPLORED/UNSEEN classification given stubbed point tests
- `preset/preset-upsert.ts` — key derivation, upsert/merge decisions
- `transform/constants.ts` — projection preset invariants (counterFactor = √10/4 etc.)
- `walls/wall-crud.ts` — generateBaseWallDefs geometry (defs only, no documents)
- shadows — `draw/shadow.ts` shadowAlpha/shadowTexture params

T2-only (do NOT unit-mock): UI/HUD injection, gizmo drag handlers, sprite clones,
layer z-order at runtime, occluder fades, linked-wall document sync, undo stacks.

Also: wire `vitest --coverage` into `verify:fast` reporting (not gating) so gaps stay visible.

## Phase A1 — apptime Adoption 🔲 (deferred)

After isoroll road. Contract + T1 first; T2 adapter designed against apptime's actual stack then.

---

## Sequence

`I4 → A1` is what remains; § Status Log holds the dated record of everything before them.
The workspace-wide half of the rollout is the enforcement layer's own contract
([`core/hooks/SPECS.md`](../core/hooks/SPECS.md)), not a phase of this plan.

## Status Log

| Date | Event |
|------|-------|
| 2026-07-02 | Plan written. All phases 🔲. |
| 2026-07-02 | W1 done: context-gate/tracker/bash-gate/precompact-wipe/session-prune hooks live; legacy hooks migrated to shared parser (`hook_input.py`), session_id markers, nested+flat schema; fixed dead `Code`→`code` check in facade-gate/scan. 12/12 piped-JSON tests pass. NOTE: new hooks activate on next session start (hook config snapshots at startup). |
| 2026-07-02 | W2 done: jscpd gate in global pre-commit (`check-duplication.py`, blocks clones involving staged files, 75 tokens/10 lines); pre-edit SIZE GATE message now instructs extract-and-import, warns copies blocked at commit. Legacy scan: isoroll src has ZERO clones at threshold (refactor phases + B32 fix already unified them) — no dedup burst needed. Known legacy clones: copilot-pre/post-tool.py pair (91 lines) — forced clean on next touch. |
| 2026-07-02 | I1 done (isoroll `feature/verify-harness` 7a49bcf): vitest+fast-check, 17 tests — frontier walk, B32 overhang clamp, depthZIndex ordering, tileSortBand no-ties, cut invariants, cell coverage, coord roundtrips, cross-tile zIndex oracle. `verify:fast` (lint+unit) + pre-commit contract gate live (1a). Fixed 3 pre-existing lint errors; split wall-keys/wall-paste out of wall-manager (line gate). tsc --noEmit NOT gated — pre-existing Foundry global type gaps (open item). |
| 2026-07-02 | W3 done: SETUP.md hook rows + agent-coverage table updated (opencode gaps marked with wiring instructions); Copilot shims rewired — copilot_shared.py extraction (dup gate cleared), context-gate/bash-gate/issues-gate/trackers wired, stable `copilot<pid>` session ids, verified via piped events; code/CONTEXT.md enforce list updated; _templates ISSUES.md + SETUP.md verification contract; core/tools/verify/CONTEXT.md pattern doc (code extraction deferred to first second consumer, A1); /dedup skill created + /handoff gained verification gate; pre-edit md rule now accepts YAML frontmatter; skills synced. VERIFY.md endstate: keep until A1 (apptime) completes, then delete per lifecycle note. |
| 2026-07-02 | Field test (Lucas: "fix it without my help"): junction z-order bug root-caused as TWO independent bugs. B34 — flip-blind imageOffset (form toggle + preset stored/applied raw; preset drift corrupted scene calibrations); fixed with shared mirrorImageOffset + preUpdateTile compensation + canonical preset space. B35 — stale slice sync (faces baked at create, needsRebuild blind to position; peer bands lazy) = the debugSlices-fixes-it bug; fixed structurally: sync() is now a reconcile (fresh computeSliceCuts each pass, structural diff decides rebuild, schedulePeerResync per tick). B33 fixed by same pass. Key process lesson: the original b32-junction spec MASKED H1 (moved and moved BACK before asserting) — specs must assert at intermediate states, not just round-trips. isoroll 904e13e: 21 unit + 7 e2e green, 0 xfail. |
| 2026-07-02 | I3 done (isoroll d858033): golden layer — UI-hidden fixed-camera viewport captures, pixelmatch 0.5% budget, junction golden committed (approval = commit), determinism verified across runs. Diff artifacts → test/e2e/output/ (gitignored, agent-readable). Note: e2e slows ~4x when a second GM client is connected. |
| 2026-07-02 | I2 done (isoroll c6e59b9): Playwright headless harness against live Foundry — `dumpZOrderJSON()` live-path oracle on `globalThis.isoroll`; GM force-join (held seats are client-disabled only); fx-* fixture scenes with keeper-scene cleanup; XFAIL runner. Results: **b32-junction PASS (first mechanical verification of the B32 fix)**; b33-unhide XFAIL (confirmed open); b2-rescale PASS on direct scene.update — B2's GridConfig repro still uncovered, stays OPEN. `verify:full` = fast+build+e2e (~40s). bugs-gate.py live (FIXED flip requires test/**/b<N>-* spec). pre-read.py gap fixed: reading the interface unlocks the source for the session (edit-intent deadlock). |

| 2026-08-01 | **VERIFY audit — prompted by Lucas's INBOX note** (*"I'm a bit worried we may have messed up the VERIFY strategy after several commits on the latest sessions"*), after `core/hooks` (50 files) and `core/tools` (37) were split into families and every test file moved. **Verdict: the strategy is intact and is now measured rather than assumed.** Four checks. **(1) The extension-list guard was a hand-list covering 14 of 62 hook files** — it could not have noticed a new checker restating `is_code_file` in `checks/`, `entropy/`, `routing/`, `git/` or `facade/`. NOT caused by the split (it was 6-of-50 before, the same blind spot at a different size), but the split made it measurable. `test_no_checker_carries_its_own_extension_list` now **walks the tree**, with four named exemptions in `NOT_THE_CODE_LAW` — `entropy_corpus.SCANNED` and `entropy_naming.AUTHORED` are genuinely different populations, the two `facade/` files are per-language dispatch — and a companion test fails if an exemption stops naming a real file. **(2) Both shrunken baselines assert strictly more:** `test_entropy_fanout` pairs `live <= BASELINE` with `BASELINE <= live`, so the two together force equality — a stale baseline fails as loudly as a new violation. Same shape in `test_entropy_naming`. **(3) No module shadowing:** `conftest.py` now inserts 30 directories on `sys.path`; 67 importable names, zero basename collisions. Locked by a new `workspace/test_import_paths.py`, because absence of a collision today is not a property. **(4) The pre-commit chain is whole:** every absolute hook path the sourced stages reference resolves, and `gitflow-gate`, `nested-gitlink-gate`, `type-gate` and `check-line-counts` all exit 0 when run from `code/corpora`, `code/spacemantics` and `code/aiwbot` working directories, each of which still declares its `verify:fast` contract. One asymmetry found and fixed: `generators/prepare.sh` invoked `brain_stats.py` by a **cwd-relative** path — harmless only because a `brain/GOALS.md` guard kept it from firing outside the wos repo, which is exactly how it survived the split unnoticed. Suite 105 → 107. |

## Open Items

- Test subagent marker inheritance in practice (same `session_id` assumption).
- Decide permission-deny belt for `cat|head|tail` after field testing.
- tsc --noEmit as T0 gate (G7) — **bigger than scoped, not landed yet.** Root cause of the
  `Tile`/`TileDocument`/`canvas`/`Token`/`Hooks`/`PIXI`/`JQuery`/`game` "cannot find name"
  errors (606 of 645 lines) was `tsconfig.json`'s `typeRoots` pointing at
  `foundry-vtt-types/src` directly instead of letting normal package resolution find its
  `index.d.mts`, combined with `"types": []` disabling auto-inclusion entirely — fixed by
  replacing both with `"types": ["@league-of-foundry-developers/foundry-vtt-types"]`. That
  fix is landed (real, low-risk, worth keeping regardless). But it unmasks **304 genuine
  strict-mode errors** (TS18048 `possibly undefined` on `canvas`/etc., TS2345, TS2353, …) —
  real Foundry-nullability and type-mismatch issues needing per-call-site judgment, not a
  config fix. Adding `tsc --noEmit` to `verify:fast` now would hard-block every isoroll
  commit on 304 pre-existing errors — too large to absorb into this rollout session.
  Needs its own dedicated type-debt pass (triage by file, likely several sessions) before
  the gate can land. `code/_templates` already defaults new projects to a clean
  `tsc --noEmit` from day one, so this debt doesn't recur elsewhere.
- B2 GridConfig-path spec variant (direct-path spec passes; dialog path unreproduced).
- Phase I4 (unit coverage expansion) + merge decision for isoroll `feature/verify-harness`
  (contains B32 fix branch history) — Lucas reviews.
- Human verification pass: Lucas confirms B32 visually in Foundry once, closing the loop
  between oracle and eyes.
- code/SETUP.md + code/SPECS.md: fold verification contract mention (only _templates and
  `core/hooks/SPECS.md` carry it so far).
- 200-LOC file-size hook: scope the .frag/.txt exemption by PATH, not extension — exempt
  design/** prototype/artifact dirs, gate everything under src/ regardless of extension.
  Rationale (2026-07-14 isoroll session, Lucas-raised): rig.frag exemption is correct
  (single-file Artifact constraint, frozen design reference, no product future) but a
  blanket extension exemption is a loophole for dodging the gate in product code.
