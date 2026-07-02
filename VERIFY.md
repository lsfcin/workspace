# VERIFY — Agent Verification & Enforcement Roadmap
> Workspace-wide plan: make agents verify their own results (no human eye per prompt) and enforce code centralization. Pilot: isoroll-module. Second: apptime.

**Lifecycle: transient initiative doc** (REFACTOR.md species) — NOT workspace structure; not
linked from AGENTS.md/SETUP.md on purpose. Endstate at W3: surviving rules migrate to SETUP.md
(ENFORCED rows), `code/_templates/`, `core/tools/verify/`; verification contract to SETUP.md;
then this file is deleted (git keeps it). Principles below are hypotheses until the isoroll
pilot validates them — do not copy them into lifetime docs before W3.

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
**`verify:full`** = T2+T3 (pre-merge / on demand / handoff).

---

## Phase W1 — Context Gate + Bypass Hardening ✅ 2026-07-02

Workspace-wide. New hooks in `.hooks/`, registered in `.claude/settings.json` + Copilot shims (SETUP.md parity).

### `context-gate.py` — PreToolUse: `Read|Edit|Write|Grep|NotebookEdit`
- From target path, walk directories up to `/mnt/workspace`; collect every `CONTEXT.md` on the chain.
- Root `AGENTS.md` exempt (auto-loaded via CLAUDE.md).
- Targets named `CONTEXT.md` / `AGENTS.md` exempt from gating (deadlock guard — always freely readable).
- All chain files in seen-markers → exit 0 silent. Any unread → exit 2, message lists ALL
  unread paths: "Read these CONTEXT.md first (one batch), then retry."
- Grep included because content-output mode leaks file bodies; uses its `path` param. Glob harmless (names only).

### `context-tracker.py` — PostToolUse: Read
- Records reads of any `CONTEXT.md` into marker file.
- Marker: `/tmp/claude_ctx_seen_<session_id>.txt`, one absolute path per line.
  `session_id` from hook stdin JSON — NOT `$PPID` (breaks with subagents/multi-window).

### `bash-context-gate.py` — PreToolUse: Bash
- Regex-extract workspace paths from command string; resolve; same chain check; exit 2 with
  "unread CONTEXT.md in chain — use Read tool first: <paths>".
- Known residual hole: dynamically constructed paths (`for f in $(find …)`) escape. Accepted.
- Optional belt (decide during testing): permission deny rules for `cat|head|tail` on workspace paths.

### Lifecycle
- **PreCompact hook:** wipe `/tmp/claude_ctx_seen_<session_id>.txt`.
- **SessionStart:** prune marker files older than 2 days.
- **Migration:** `facade-tracker.py` + codegraph nudge in `pre-read.sh` move from `$PPID` → `session_id`.

### Acceptance
- Fresh session: first Read of `code/isoroll-module/src/render/x.ts` blocks listing 3–4 CONTEXT.mds; after batch-reading them, retry passes; second file in same subtree passes silently.
- Subagent spawned mid-session: no block on same subtree.
- After compaction: block fires again.
- `cat src/render/x.ts` via Bash: blocked with same message.

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

## Phase I3 — isoroll Visual Layer 🔲

- Deterministic render config for fixtures: animations off, fixed viewport + zoom,
  wait-for-render-idle, pixelmatch tolerance threshold.
- Golden screenshots per fixture scene; failure artifact = diff PNG (agent Reads it for diagnosis).
- New-feature flow: harness produces screenshot set → human approves ONCE → golden-locked.
  Human role shifts from per-prompt camera to per-feature approver.

## Phase W3 — Extract + Generalize 🔲

- Generic pieces → `core/tools/verify/`: Playwright launcher helpers, golden runner with
  `approve`/`update` CLI, dump-oracle pattern doc (the contract any project's adapter implements).
- `code/_templates/` update: vitest scaffold, `test/` layout, jscpd config, `verify:fast`/`verify:full`
  stubs, KNOWN-BUGS.md template carrying the regression rule. New projects born compliant.
- SETUP.md: add all new rows as **ENFORCED**; audit existing INDUCED rows — promote or delete.
- `/handoff` skill: runs `verify:full`, result recorded in handoff notes.
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
| 2026-07-02 | I2 done (isoroll c6e59b9): Playwright headless harness against live Foundry — `dumpZOrderJSON()` live-path oracle on `globalThis.isoroll`; GM force-join (held seats are client-disabled only); fx-* fixture scenes with keeper-scene cleanup; XFAIL runner. Results: **b32-junction PASS (first mechanical verification of the B32 fix)**; b33-unhide XFAIL (confirmed open); b2-rescale PASS on direct scene.update — B2's GridConfig repro still uncovered, stays OPEN. `verify:full` = fast+build+e2e (~40s). known-bugs-gate.py live (FIXED flip requires test/**/b<N>-* spec). pre-read.sh gap fixed: reading the interface unlocks the source for the session (edit-intent deadlock). |

## Open Items

- Test subagent marker inheritance in practice (same `session_id` assumption).
- Decide permission-deny belt for `cat|head|tail` after W1 field testing.
- jscpd threshold tuning during the legacy dedup session.
- Verify B32 fix in Foundry (branch `fix/b32-slice-zorder-collision`) — becomes first
  regression spec either way.
