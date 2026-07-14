# VERIFY — Agent Verification & Enforcement Roadmap
> Testing-discipline rollout for `code/` projects: make agents verify their own results (no human eye per prompt) and enforce code centralization. Pilot: isoroll-module. Second: apptime.

**Lifecycle: transient initiative doc** (REFACTOR.md species, one level up — lives beside
`code/CONTEXT.md` instead of inside one project) — NOT workspace structure. Linked from root
`SETUP.md` and `code/CONTEXT.md` on purpose (this is where the verify:fast contract those files
enforce is tracked). Endstate: once every `code/` project has a real contract and A1 (apptime)
completes, surviving durable rules stay in `core/tools/verify/CONTEXT.md` (already done at W3)
and this file is deleted (git keeps it).

**Scope note:** this doc originally tracked workspace-wide hook infra too (context-gate,
bash-gate — see Phase W1 below). That part is done and lives canonically in root `SETUP.md`'s
hook table now; W1 is kept here only as a compressed historical pointer. This doc's live scope
from W2 onward is `code/` testing-pyramid rollout specifically — brain/academy don't have a
`verify:fast` concept.

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

## Phase W1 — Context Gate + Bypass Hardening ✅ 2026-07-02 (workspace-wide, moved out)

Workspace-wide hooks (`context-gate.py`, `context-tracker.py`, `bash-context-gate.py` +
PreCompact/SessionStart lifecycle) — not `code/`-specific, so their canonical documentation
lives in root [`SETUP.md`](../SETUP.md#claude-code-hooks-claudesettingsjson)'s hook table, not
here. Kept as a one-line record: shipped 2026-07-02, forces the CONTEXT.md chain to be Read
before any file access anywhere in the workspace.

---

## Phase W2 — Duplication + LOC Gates ✅ 2026-07-02

### `pre-edit.py` message rewrite
Replace "Create a new module file and write there instead" (line ~86) with:
> "Extract shared logic into a new module and import it from existing callers.
> Do NOT copy existing functions — copies are blocked at commit."
Cap stays 200 (token-economy: single-pass read). Rationale: cap alone leaves two compliant
moves (extract vs copy); agents take the cheap one. Dup gate removes the cheap exit.

### jscpd gate — global pre-commit (`core.hooksPath`, fires in every repo)
- Block any clone involving a staged file. No baseline (locked decision) — editing a file
  with a legacy clone forces extracting it then (boy-scout rule, enforced).
- Config beside `line-limits.env`: min ~10 lines / ~75 tokens; exclude `*.d.ts`, `*.pyi`,
  generated, fixtures, `node_modules`, goldens.
- **Immediately after landing:** one dedicated isoroll dedup session — clear legacy clones
  in hot files as a burst, not a drizzle.

### Layer-2 note (semantic dups)
jscpd catches verbatim/near-verbatim. Agents also *regenerate* similar logic — no static
tool catches that. Periodic `/dedup` audit skill (codegraph: same-signature/same-call-shape
candidates, agent reviews) — deferred to W3+.

---

## Phase I1 — isoroll Unit Foundation ✅ 2026-07-02

- vitest + fast-check into isoroll-module (Vite already in stack).
- Targets: `src/render/iso-tile-depth.ts`, `src/render/iso-tile-geom.ts`, `src/transform/coord-map.ts`.
- Property invariants:
  - No exact zIndex ties across slices of neighboring tiles (any layout).
  - `computeSliceCuts` monotonic; no phantom zero-width slices.
  - `sliceDepthCell` result inside footprint or clamped to edge face.
  - `tileSortBand` total order, stable under permutation, bounded below `TOKEN_BAND`.
- `verify:fast` = tsc + eslint + unit suite.
- **Verify gate lands in global pre-commit here:** project declaring `verify:fast` → red
  blocks commit. Project without contract → warn (promote to block once templates exist).

## Phase I2 — isoroll Headless Harness ✅ 2026-07-02 (core deliverable)

- **Launcher script (committed, `test/`):** start Foundry server
  (`node ~/FoundryVTT/resources/app/main.js --dataPath=~/foundrydata-v14`), health-check,
  Playwright connect to `localhost:30000`, login, activate fixture scene.
- **Fixtures:** committed scene JSONs + minimal assets. Fixture #1 = B32 L/T/X wall-junction
  layout. Standing rule (Principle 5) applies from here on.
- **Formal debug API:** `window.isoroll.debug.dumpZOrder()` → JSON per slice:
  `{tileId, cell:{row,col}, elev, zIndex, band, screenAABB}`. Plus dump endpoints for slice
  visibility state and tile transforms. Must call live-path functions (Principle 4).
- **Assertion pack** (pure logic on the dump — no vision):
  - Z-order oracle: for every pair of screen-overlapping slices, lower `(row − col + elev)`
    has lower zIndex.
  - Zero exact zIndex ties on the iso layer.
  - Slice visibility mirrors `document.hidden` after hide→unhide (B33 oracle).
  - Positions follow grid-rescale like tokens/walls; size stable (B2 oracle).
  - Stability: dump identical after move-tile-and-return and after adversarial reversal of
    PIXI children order.
- **Regression specs:** `test/regressions/b32-junction.spec.ts`, `b33-unhide.spec.ts`,
  `b2-rescale.spec.ts`. One per KNOWN-BUG as they're worked.
- `verify:full` = launcher + all specs + (from I3) goldens.
- **KNOWN-BUGS gate lands here:** pre-edit hook on `KNOWN-BUGS.md` — flipping a bug to
  FIXED blocked unless matching `test/regressions/b<N>-*` exists.

## Phase I3 — isoroll Visual Layer ✅ 2026-07-02

- Deterministic render config for fixtures: animations off, fixed viewport + zoom,
  wait-for-render-idle, pixelmatch tolerance threshold.
- Golden screenshots per fixture scene; failure artifact = diff PNG (agent Reads it for diagnosis).
- New-feature flow: harness produces screenshot set → human approves ONCE → golden-locked.
  Human role shifts from per-prompt camera to per-feature approver.

## Phase W3 — Extract + Generalize ✅ 2026-07-02

- Generic pieces → `core/tools/verify/`: Playwright launcher helpers, golden runner with
  `approve`/`update` CLI, dump-oracle pattern doc (the contract any project's adapter implements).
- `code/_templates/` update: vitest scaffold, `test/` layout, jscpd config, `verify:fast`/`verify:full`
  stubs, KNOWN-BUGS.md template carrying the regression rule. New projects born compliant.
- SETUP.md: add all new rows as **ENFORCED**; audit existing INDUCED rows — promote or delete.
- `/roundup` skill: runs `verify:full`, result recorded in the resume prompt.
- `/dedup` semantic audit skill (see W2 note).

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

```
W1 → W2 (+ legacy dedup session) → I1 → I2 → I3 → W3 → … → A1
```

W1+W2 ≈ one day, whole workspace benefits immediately. I1+I2 = the oracle where the pain is.
W3 makes it portable.

## Status Log

| Date | Event |
|------|-------|
| 2026-07-02 | Plan written. All phases 🔲. |
| 2026-07-02 | W1 done: context-gate/tracker/bash-gate/precompact-wipe/session-prune hooks live; legacy hooks migrated to shared parser (`hook_input.py`), session_id markers, nested+flat schema; fixed dead `Code`→`code` check in facade-gate/scan. 12/12 piped-JSON tests pass. NOTE: new hooks activate on next session start (hook config snapshots at startup). |
| 2026-07-02 | W2 done: jscpd gate in global pre-commit (`check-duplication.py`, blocks clones involving staged files, 75 tokens/10 lines); pre-edit SIZE GATE message now instructs extract-and-import, warns copies blocked at commit. Legacy scan: isoroll src has ZERO clones at threshold (refactor phases + B32 fix already unified them) — no dedup burst needed. Known legacy clones: copilot-pre/post-tool.py pair (91 lines) — forced clean on next touch. |
| 2026-07-02 | I1 done (isoroll `feature/verify-harness` 7a49bcf): vitest+fast-check, 17 tests — frontier walk, B32 overhang clamp, depthZIndex ordering, tileSortBand no-ties, cut invariants, cell coverage, coord roundtrips, cross-tile zIndex oracle. `verify:fast` (lint+unit) + pre-commit contract gate live (1a). Fixed 3 pre-existing lint errors; split wall-keys/wall-paste out of wall-manager (line gate). tsc --noEmit NOT gated — pre-existing Foundry global type gaps (open item). |
| 2026-07-02 | W3 done: SETUP.md hook rows + agent-coverage table updated (opencode gaps marked with wiring instructions); Copilot shims rewired — copilot_shared.py extraction (dup gate cleared), context-gate/bash-gate/known-bugs-gate/trackers wired, stable `copilot<pid>` session ids, verified via piped events; code/CONTEXT.md enforce list updated; _templates KNOWN-BUGS.md + SETUP.md verification contract; core/tools/verify/CONTEXT.md pattern doc (code extraction deferred to first second consumer, A1); /dedup skill created + /handoff gained verification gate; pre-edit md rule now accepts YAML frontmatter; skills synced. VERIFY.md endstate: keep until A1 (apptime) completes, then delete per lifecycle note. |
| 2026-07-02 | Field test (Lucas: "fix it without my help"): junction z-order bug root-caused as TWO independent bugs. B34 — flip-blind imageOffset (form toggle + preset stored/applied raw; preset drift corrupted scene calibrations); fixed with shared mirrorImageOffset + preUpdateTile compensation + canonical preset space. B35 — stale slice sync (faces baked at create, needsRebuild blind to position; peer bands lazy) = the debugSlices-fixes-it bug; fixed structurally: sync() is now a reconcile (fresh computeSliceCuts each pass, structural diff decides rebuild, schedulePeerResync per tick). B33 fixed by same pass. Key process lesson: the original b32-junction spec MASKED H1 (moved and moved BACK before asserting) — specs must assert at intermediate states, not just round-trips. isoroll 904e13e: 21 unit + 7 e2e green, 0 xfail. |
| 2026-07-02 | I3 done (isoroll d858033): golden layer — UI-hidden fixed-camera viewport captures, pixelmatch 0.5% budget, junction golden committed (approval = commit), determinism verified across runs. Diff artifacts → test/e2e/output/ (gitignored, agent-readable). Note: e2e slows ~4x when a second GM client is connected. |
| 2026-07-02 | I2 done (isoroll c6e59b9): Playwright headless harness against live Foundry — `dumpZOrderJSON()` live-path oracle on `globalThis.isoroll`; GM force-join (held seats are client-disabled only); fx-* fixture scenes with keeper-scene cleanup; XFAIL runner. Results: **b32-junction PASS (first mechanical verification of the B32 fix)**; b33-unhide XFAIL (confirmed open); b2-rescale PASS on direct scene.update — B2's GridConfig repro still uncovered, stays OPEN. `verify:full` = fast+build+e2e (~40s). known-bugs-gate.py live (FIXED flip requires test/**/b<N>-* spec). pre-read.sh gap fixed: reading the interface unlocks the source for the session (edit-intent deadlock). |

## Open Items

- Test subagent marker inheritance in practice (same `session_id` assumption).
- Decide permission-deny belt for `cat|head|tail` after field testing.
- ~~opencode shim gaps~~ DONE (G6): context-gate/bash-gate/trackers/known-bugs-gate wired
  into `.opencode/plugins/workspace-policy.js`, verified via synthetic-client smoke test
  (block-then-allow on CONTEXT chain for Read and Bash, known-bugs-gate blocks a FIXED
  flip with no spec). Coverage table in root SETUP.md updated.
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
  root SETUP.md updated so far).
- 200-LOC file-size hook: scope the .frag/.txt exemption by PATH, not extension — exempt
  design/** prototype/artifact dirs, gate everything under src/ regardless of extension.
  Rationale (2026-07-14 isoroll session, Lucas-raised): rig.frag exemption is correct
  (single-file Artifact constraint, frozen design reference, no product future) but a
  blanket extension exemption is a loophole for dodging the gate in product code.
