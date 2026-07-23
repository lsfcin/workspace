---
description: Looped engineering flow — development in file-relayed loops with model autorouting; each loop runs in a fresh, cheap session that reads exactly one file.
args: <task or feature request>
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `core/tools/` for runtime-specific mappings.

- Agent delegation: use `subagent` / `Agent` when available; otherwise the user opens a fresh session per loop.
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

Engineer this task in loops: $@

This is an execution request, not a request to explain the workflow. Derive a feature slug (lowercase, hyphens, ≤5 words). Do not ask for confirmation beyond the Loop 0 interview.

> **This is the `feature` subtree of the craft tree** ([`route.md`](route.md), [`TREE.md`](TREE.md)). Reach it via the router, which pins `subtree: feature`. It is **contract-first**: Loop 0 sets a supervision panel, Loop 3.5 lays out every module/step I/O contract before any code, Loop 3 runs a recurrent concept-symmetry review. Research and architecture-decision tasks belong to other subtrees.

## Core Principle — Files, Not Conversation

Each loop is executed by a **fresh session** of the cheapest capable model. That session receives only:

1. Its own loop section from this flow file.
2. **One** input file: the previous loop's output (which embeds the Carry block — see below).

It never receives conversation history. It appends its output to its own loop file and returns a **one-line verdict** to the orchestrator. The orchestrator never reads loop file contents — only verdicts. This is how the flow *saves* tokens instead of spending them: N cheap short sessions instead of one long expensive one.

### File protocol

- Directory: `<project>/.loop/<feature-slug>/` inside the target project's own repo.
- Files: `0-clarify.md`, `1-plan.md`, `2-ground.md`, `3-arch.md`, `3b-contracts.md` (feature subtree), `4a-tests.md`, `4b-code.md`, `5-user.md`, `6-ship.md`.
- **Append-only.** Executors add sections; never rewrite prior content. Corrections are new appended sections.
- **Executor self-report.** Every appended section ends with `executor: <agent-type> model=<provider/model-id> tier=<tier> deleg=<none|from→to>` — after a run, `grep executor .loop/<slug>/*.md` audits whether routing actually happened *and* which provider paid for each loop. The `model=` field MUST include the provider prefix (e.g. `model=nvidia/z-ai/glm-5.2`, not bare `model=glm-5.2`) so the per-provider cost split is recoverable from the chain alone, without the session log.
- **Small.** Soft cap ~80 lines per file. A loop file that wants to exceed the cap is a smell: the task is too big — raise `FLAG: RETURN loop=1 reason=split-needed`.
- **Carry block.** Every loop file starts with a `## Carry` block **copied verbatim** from the previous file (Loop 0 creates it). It holds: slug, branch, project root, test command, criticality, acceptance-criteria digest, context pointers (project `CONTEXT.md`/`AGENTS.md` paths). This is what makes "read exactly one file" true — no loop ever needs to chase earlier files.
- `.loop/` is committed on the feature branch during the flow (audit trail, survives crashes). Loop 6 folds the durable outcome into the project's `ROADMAP.md` (workspace policy: plans live in roadmaps) and deletes `.loop/<slug>/` in the final commit unless Loop 0 recorded `keep-trail: yes`.

### Carry block template

```markdown
## Carry
slug: <feature-slug> | branch: <branch-name> | root: <project path>
provider: <orchestrator provider, e.g. nvidia | openrouter | opencode | anthropic | copilot> | chain-deleg: <none | deleg=<from>→<to>>
tier-map: <one of: nvidia | openrouter | opencode | anthropic | copilot> | verified-on: <date>
test-cmd: <exact command, e.g. `npm test`> | e2e-cmd: <or "none">
criticality: <low|normal|critical> | verdict: <padaria|standard|critico>
subtree: <padaria|feature|research|architecture> | supervision: io-signoff=<yes|no> arch-review=<none|per-feature|periodic> arch-review-supervised=<yes|no>
criteria: <one line per acceptance criterion, numbered C1..Cn>
tasks: <filled by Loop 1 — one line per row: Tn — task — files — tier>
context: <paths to project CONTEXT.md / AGENTS.md the executor must read>
```

`provider:` is the orchestrator's chosen provider for the chain. `tier-map:` names which per-provider table row (the per-provider table in [`routing.md`](routing.md)) fills the chain's tiers — usually equals `provider`, but for downward delegation it may differ (e.g. `provider: openrouter` + `tier-map: nvidia` means the openrouter orchestrator runs every loop on nvidia subagents to save credits — see [`routing.md`](routing.md) § Provider delegation). `chain-deleg:` records the delegation edge if one was applied. ALL THREE fields must be filled — a chain without an explicit provider+map is undefined and Loop 0 must escalate to the user. The orchestrator runs the `opencode models | awk -F/` probe **before** filling these so the row actually exists in this runtime.

Loops 0–1 may fill TBD Carry fields (branch, test-cmd, tasks); from Loop 2 on the block is frozen and copied verbatim.

## Autorouting

Tiers are provider-agnostic. Loop 1 assigns a tier + effort **per task row** in the plan; loops without a plan row use the defaults below.

| Task type | Tier | Effort | Escalate to next tier when |
|---|---|---|---|
| Loop 0 — clarify interview, criticality gate | high | high | ambition high, or innovation/creativity demanded → max |
| Loop 1 — plan + adversarial plan review | high | high | review leaves ≥1 unresolved FATAL → max |
| Loop 2 — branch + grounding checks | low | low | never (mismatch raises a flag instead) |
| Loop 3 — architecture + evaluation | high | medium | criticality=critical or novel design → max |
| Loop 4a — write failing tests | medium | medium | criterion needs deep domain insight to encode → high |
| Loop 4b — code until green | medium (low for padaria) | medium | 3 consecutive red runs on the same test → high |
| Loop 5 — automated user test | medium | medium | 2 environment/flake failures → high |
| Loop 6 — commit, push, ship notes | low | low | never |

**Escalation rules (general):** escalate exactly one tier at a time; append `ESCALATED from=<tier> to=<tier> reason=<evidence>` to the current loop file; the escalated session reads the same single input file. If the **max** tier still fails, do not retry — raise a RETURN flag. Never de-escalate mid-loop.

**Max tier is never auto-spawned.** Escalation to `max` pauses the flow and surfaces to the user with the evidence line — max-tier quota is scarce and spending it is the user's call. The user either runs that loop in a max-tier session or overrides the escalation.

**Which concrete model fills a tier** is in [`routing.md`](routing.md) — the availability probe, the per-provider tier maps, the benchmarks, and the downward-only delegation rule. The **orchestrator** reads it once, before Loop 0, to fill the Carry `provider:` / `tier-map:` fields. Executors do not: they are handed a resolved `model=` in the spawn prompt.

## Return Flags

Flag line format, appended at the end of the executor's section:

```
FLAG: RETURN loop=<N> reason=<slug> evidence=<one line>
```

- The executor **raises**; the orchestrator **routes**. A return of ≤1 loop backwards is honored automatically.
- Two consecutive returns to the same loop, or any `RETURN loop=0`, stops the flow and goes to the **user** — the intent itself is in question.
- The receiving loop re-runs at **one tier above** its default (the cheap tier already failed to produce a survivable artifact).

## Orchestration

The orchestrator (lead session) holds only: slug, current loop number, verdicts, flags, and **the provider + tier-map resolved in Loop 0**.

**Routing is structural, not discretionary:** spawn via the pinned executor agent types `craft-low` / `craft-medium` / `craft-high` (Claude Code: `.claude/agents/craft-*.md`; opencode: `.opencode/agents/craft-*.md`). The pinned executors pin **one model per runtime**, set in frontmatter (so routing cannot drift inside that runtime). For runtimes that support per-spawn model override (opencode's `task`/`subagent` literal-a-models), the orchestrator passes the tier's model **from the active provider's row** of [`routing.md`](routing.md), NOT the frontmatter default — the frontmatter default is just the fallback when the orchestrator doesn't resolve a provider. Spawn each loop with this prompt — nothing more:

```
Read core/flows/craft/craft.md, section "Loop <N>" plus "Core Principle",
"Autorouting", "Return Flags". Then read
<project>/.loop/<slug>/<input-file>. Execute Loop <N>. Append your output to
<project>/.loop/<slug>/<output-file> following the embedded template. End your
section with `executor: craft-<tier> model=<provider/model-id> tier=<tier>
deleg=<none|from→to>`. Reply with ONE line:
OK <verdict> | FLAG <flag line> | BLOCKED <reason>.
```

The executor is told its `model=` — it must **not** load `routing.md` to look one up. That is what keeps a loop session cheap.

**Spawn mechanics are per-runtime and live in [`runtimes.md`](runtimes.md)** — `opencode run` subprocess recipe, Claude Code `Agent` tool, Copilot CLI, and the portability table. Read only the section for the runtime you are in, once, at the first spawn.

No runtime `subagent`/`Agent`/`task` tool → the user opens a fresh session per loop with the same prompt and picks the model per the active tier-map; the flow is unchanged.

---

## Loop 0 — Clarify

**Tier:** high (max if ambitious/innovative). **Input:** the raw request + user interview. **Output:** `0-clarify.md`. The only interactive loop.

**Spec precedes code (SDD).** If any target module under `code/` is spec-locked — its `CONTEXT.md` carries `> spec: <path>` and that `SPEC.md` is `status: locked` — **read the SPEC.md first** (the `spec-read-gate` will block edits otherwise) and treat its `## Invariants` as pre-set acceptance criteria: fold them into `criteria:` below so the flow verifies them. The module spec is the contract; this run must not violate it. See `code/SPEC-DRIVE.md`.

Interview the user (don't assume — workspace rule) until you can fill every field. Then apply the **bakery gate**: verdict `padaria` iff ALL hold — ≤2 files touched, no new public API, no schema/data migration, an existing pattern in the repo covers it, revert fully undoes it, criticality=low|normal. Otherwise `standard` (or `critico` if criticality=critical).

```markdown
## Carry
<fill per template above; branch/test-cmd may be TBD until Loop 1/2>

## Clarify
intent: <what, one sentence>
motivation: <why now>
refs: <links, files, prior art>
scope-files: <known files/folders touched>
expected-result: <observable end state>
ambition: <minimal|solid|showcase>
criticality: <low|normal|critical> tolerance: <what failure is acceptable>
criteria: C1..Cn <objective, testable>
innovation: <none|some|core — is creativity the point?>
verdict: <padaria|standard|critico>
keep-trail: <yes|no>

## Permission Panel (supervision profile — copy into Carry `supervision:`)
io-signoff: <yes|no>                       # human OKs each module/step I/O boundary before code — default NO (agent proceeds)
arch-review: <none|per-feature|periodic>   # recurrent concept-symmetry review cadence — default NONE
arch-review-supervised: <yes|no>           # human checks the arch review — default NO
```

**Permission-panel interview (feature subtree).** After the criteria are settled, ask the user three short questions and record the answers above; the **recommended defaults are permissive** so the agent runs unattended and cheap. The contract itself is never optional — only *human sign-off on it* is. Ask: (1) "Do you want to acknowledge each module/step I/O boundary before I implement? (default no)"; (2) "Should I run the concept-symmetry architecture review — never, once per feature, or as a periodic sweep? (default never)"; (3) if arch-review ≠ none, "Do you want to check that review yourself, or let me? (default me)".

**Padaria shortcut:** verdict `padaria` → skip Loops 1, 3, 3.5, 4a, 5. One medium-tier session does: append a ≤5-line micro-plan to `0-clarify.md`, execute Loop 2 (branch), edit, run the **existing** test suite, execute Loop 6. Two files total (`0-clarify.md`, `6-ship.md`). The flow must never cost more than the task.

**Flags:** none (nothing before it). If the user can't state criteria, the task isn't ready — stop, don't start the flow.

## Loop 1 — Plan

**Tier:** high. **Input:** `0-clarify.md`. **Output:** `1-plan.md`.

Plan, then **adversarially review your own plan assuming smaller models will execute it**: every task row must be executable by its assigned tier from the row text + Carry block alone — no implied context, no "as discussed". Ambiguity that a medium-tier model would trip on is a FATAL. Fix or escalate row tiers until the review passes. Copy the final task rows into the Carry `tasks:` digest (later loops read only one file — this is how they see the plan). Add a line referencing this plan to the project's `ROADMAP.md` (workspace policy).

```markdown
## Carry
<copied + branch name and test-cmd now filled>

## Plan
branch: <name>
| id | task | files | done-when | tier | effort |
|----|------|-------|-----------|------|--------|
| T1 | ...  | ...   | <objective check> | medium | medium |

## Plan Review (adversarial, assume small executors)
- <risk found> → <fix applied | tier raised on Tn>
verdict: PASS | FAIL
```

**Flags:** review exposes a gap in intent that planning can't fix → `RETURN loop=0 reason=intent-gap`. Plan exceeds ~10 rows → `RETURN loop=0 reason=split-needed` (feature too big for one flow run).

## Loop 2 — Ground

**Tier:** low. **Input:** `1-plan.md`. **Output:** `2-ground.md`.

Mechanical grounding: create the branch from the correct base; verify every path in the plan's `files` column exists (or its parent dir does, for new files); verify `test-cmd` actually runs (may be red, must not error out).

**Git Flow (enforced).** The branch MUST be `feature/<slug>` off `develop` (or `hotfix/<slug>` off `main`) — `.hooks/gitflow-gate.sh` blocks commits on `main`/`master`/`develop` or any non-flow branch name in `code/` repos, so a wrong branch here fails at Loop 6 ship. If the project has no `develop` yet, create it from `main` first.

```markdown
## Carry
<copied>

## Ground
branch-created: <name> base: <ref>
paths: <n>/<n> ok | missing: <list or none>
test-cmd-runs: yes|no <output tail if no>
```

**Flags:** >20% of paths missing/renamed, or test-cmd errors → `RETURN loop=1 reason=stale-plan evidence=<list>`.

## Loop 3 — Architecture

**Tier:** high (max if critico). **Input:** `2-ground.md`. **Output:** `3-arch.md`.

Design the high-level shape: folders, files, classes, responsibilities, key function signatures. Then a same-session adversarial evaluation pass: does every criterion C1..Cn have a home and a **testable seam**? Would a medium-tier model implementing file-by-file make a wrong guess anywhere? Fix before writing the verdict.

**Concept-Symmetry Review (recurrent · runs per Carry `supervision: arch-review`).** When `arch-review=per-feature`, run it here; when `periodic`, skip inline and run it as a standalone sweep on cadence; when `none`, skip. It guards conceptual integrity — the semantic soundness of the *whole* project, not just this feature. Two layers:
- **Checklist (judgment):** do alike things look alike (parallel structures named/shaped alike)? Is naming coherent across modules (one concept = one name, no synonyms)? Are module boundaries consistent (same kind of thing split the same way)? Does this design keep the project's mental model sound, or bolt on an asymmetry?
- **Automation:** run `codegraph` (via bash) over the touched project for structural outliers/asymmetry, and the `/dedup` skill for regenerated near-duplicate logic the jscpd gate misses. Feed both into the checklist.
If `arch-review-supervised=yes`, present the findings and wait for the user's call before the verdict; else the reviewer (fresh session, not the author) rules.

```markdown
## Carry
<copied>

## Architecture
<per file: path — responsibility — key functions/signatures — plan task ids>

## Evaluation
criteria-coverage: C1→<where> ... Cn→<where>
seams: <how each criterion will be tested>
verdict: PASS | FAIL <reason>

## Concept-Symmetry Review (omit if arch-review=none)
checklist: alike-look-alike=<ok|issue> · naming-coherent=<ok|issue> · boundaries-consistent=<ok|issue> · model-sound=<ok|issue>
codegraph: <structural outliers/asymmetries, or none>
dedup: <near-duplicate logic found, or none>
supervised: <n/a | findings shown → user verdict: OK|CHANGES> 
verdict: PASS | FAIL <reason>
```

**Flags:** an acceptance criterion cannot be satisfied by any reasonable design → `RETURN loop=1 reason=criterion-infeasible`; two criteria contradict → `RETURN loop=0 reason=criteria-conflict`.

## Loop 3.5 — Contract Layout (feature subtree · mandatory · contract-first)

**Tier:** high. **Input:** `3-arch.md`. **Output:** `3b-contracts.md`.

This is the heart of the feature subtree: **lay out every module/step I/O contract before any implementation**, so the connection graph is defined in advance and the code merely fills the placeholders. The contract is mandatory regardless of the supervision panel; only the *human sign-off* on it is optional.

1. For every `code/` module the architecture touches, create/update its `SPEC.md` from `code/_templates/module.SPEC.md` — fill `Inputs`, `Outputs`, `Invariants` from the architecture's signatures + the Carry criteria; set `> spec: SPEC.md` in the module `CONTEXT.md`. (This is also what satisfies the standing spec gates — see `code/SPEC-DRIVE.md`.)
2. Generate the interface skeleton (the `.pyi`/`.d.ts`/`.dart.api` stubs the post-edit hook already emits) so the boundaries exist as types before bodies.
3. Wire the **connection graph**: for each planned edge `A → B`, assert `A.outputs` type matches `B.inputs` type. Run `core/tools/spec-contract-check <project>` — it fails if any planned module lacks a contract or any edge's types mismatch.
4. **Human gate:** if Carry `supervision: io-signoff=yes`, present the I/O map (modules, their in/out, the edges) and wait for an explicit OK before Loop 4a; otherwise proceed.

```markdown
## Carry
<copied>

## Contracts
modules: <module — SPEC.md path — status: draft|locked>
edges: <A.output:type → B.input:type — MATCH|MISMATCH>
contract-check: <core/tools/spec-contract-check output last line>
io-signoff: <n/a | requested → APPROVED by user | pending>
```

**Flags:** an edge cannot be made to type-match without a design change → `RETURN loop=3 reason=contract-gap`; a criterion has no home in any module contract → `RETURN loop=1 reason=criterion-uncontracted`.

## Loop 4a — Tests First

**Tier:** medium. **Input:** `3b-contracts.md`. **Output:** `4a-tests.md`.

TDD: write functional/unit tests **before** implementation code, one or more per criterion, placed at the seams named in the architecture. Run them; confirm they fail for the right reason (missing behavior, not syntax/import errors).

```markdown
## Carry
<copied>

## Tests
| test file | covers | asserts |
|-----------|--------|---------|
red-run: <n> failed as expected | wrong-failures: <none or list>
```

**Flags:** a criterion is untestable at the designed seams → `RETURN loop=3 reason=no-seam`; untestable as *written* regardless of design → `RETURN loop=1 reason=criterion-untestable`.

## Loop 4b — Code Until Green

**Tier:** medium (per plan-row tiers). **Input:** `4a-tests.md`. **Output:** `4b-code.md`.

Implement plan tasks until `test-cmd` is fully green. Append one `attempt` line per red run — this log is the escalation evidence. **Never edit a test to make it pass**; a wrong test is a flag, not a patch.

```markdown
## Carry
<copied>

## Code
attempt 1: <tasks done> → <n red> <failing test names>
attempt 2: ...
ESCALATED ... (if any)
green: yes run: <test-cmd output last line>
touched: <files>
```

**Flags:** 3 red attempts at default tier + 3 more at escalated tier → decide by evidence: failing test contradicts a Carry criterion → `RETURN loop=4a reason=test-wrong`; test is right but the design fights it → `RETURN loop=3 reason=design-fights-tests`.

## Loop 5 — User Test

**Tier:** medium. **Input:** `4b-code.md`. **Output:** `5-user.md`.

Author and run one automated **complex user scenario** end-to-end (e2e-cmd from Carry, or script the real entrypoint: CLI invocation, HTTP flow, UI driver — whatever the project's `run`/verify skill uses). It must chain multiple criteria in one realistic path, not re-run unit tests. Evaluate the observed output against `expected-result` from Loop 0.

```markdown
## Carry
<copied>

## User Test
scenario: <one paragraph, user's voice>
script: <path> run: <command>
observed: <key output lines>
matches-expected-result: yes|no <diff if no>
```

**Flags:** e2e fails while units are green → `RETURN loop=3 reason=integration-gap`; output is correct per tests but wrong per intent → `RETURN loop=0 reason=intent-mismatch` (user decides).

## Loop 6 — Ship

**Tier:** low. **Input:** `5-user.md` (or `0-clarify.md` on the padaria path). **Output:** `6-ship.md`.

Verify the working tree contains only in-scope changes (diff vs plan `files` + `.loop/`); update the project `ROADMAP.md` line to done with a one-line outcome; delete `.loop/<slug>/` unless `keep-trail: yes`; commit (normal prose, project's commit conventions) and push the feature branch. Do not merge — that is the user's call.

**Spec promotion (SDD).** Before deleting `.loop/<slug>/`, if the chain touched a `code/` module, distill its durable contract into the module's `SPEC.md` (create from `code/_templates/module.SPEC.md` if absent): fold the Carry `criteria` C1..Cn and Loop 3's `seams` into the spec's `## Invariants`/`## Examples`, point `## Examples` at the new tests (`4a-tests.md`), and set the `CONTEXT.md` `> spec: SPEC.md` line + `status: locked`. This converts the ephemeral per-feature journal into a durable per-module contract — a new module born this way satisfies the `1d` new-module gate on the same commit. See `code/SPEC-DRIVE.md`.

```markdown
## Carry
<copied>

## Ship
diff-scope: clean | extras: <list>
roadmap: updated <path>
commit: <hash> pushed: yes|no
leftovers: <follow-ups routed to ROADMAP/INBOX, or none>
```

**Flags:** out-of-scope files or secrets in diff → `RETURN loop=4b reason=dirty-tree`; push rejected → report BLOCKED, never force-push.

**Status (mandatory):** Loop 6 mutates the chain's status field — `<project>/.loop/<slug>/STATUS.md`, single line: `status: active | blocked-flag-pending-user | abandoned | shipped \| commit: <hash or none> \| last-loop: <N> \| last-updated: <date>`. Loop 0 creates the file with `status: active, last-loop: 0`. Any loop that raises a RETURN the orchestrator cannot auto-route (per `Return Flags`, e.g. two consecutive returns or any `RETURN loop=0`) sets `status: blocked-flag-pending-user, last-loop: <N>` and stops. The chain's status is therefore always inspectable: a workspace-wide `/loops --status` summarizer is `cat code/*/.loop/*/STATUS.md` — surfaces in-flight and abandoned chains (e.g. `isoroll-module/.loop/floor-fog-spike` and `.loop/painter-mvp-1`, both stopped pre-ship without status, motivate this mechanism).

**STATUS.md ALSO carries a provider-routing header line** that Loop 0 writes when the chain starts and Loop 6 mirrors on ship:

```
provider: <nvidia|openrouter|opencode|anthropic|copilot> | tier-map: <row-id> | chain-deleg: <none|deleg=<from>→<to>>
```

The `/loops --status` summarizer therefore also surfaces provider + delegation per in-flight chain (`cat code/*/.loop/*/STATUS.md` shows which chains are running on free nvidia vs spending openrouter credits). Empty `tier-map:` on a non-blocked chain ⇒ the orchestrator never resolved routing — file a bug.

### Second-opinion verifier (Voyager-style, closes the self-review gap)

Loops 1 and 3 currently do *same-session* adversarial review — the same high-tier session that wrote the plan/architecture grades it. Voyager (Wang 2023) separates "self-verification" as a distinct prompt; Anthropic's best-practices doc is explicit that *a reviewer running in a fresh subagent context evaluates the result on its own terms, not the reasoning that produced it*. From 2026-07, /loops adds:

- **Loop 3 — architecture second-opinion.** Before Loop 3's own `verdict: PASS`, the orchestrator spawns a **fresh low-tier session** (haiku-level — verifier, not author) reading only `2-ground.md` + the proposed `3-arch.md` + Carry. It returns ONE line: `OK crit-covered:` (criteria homes confirmed) | `GAP <criterion-id> <one-line defect>`. Any non-OK line escalates Loop 3 to high; if high also fails to close the gap, escalate per the existing RETURN protocol (→ Loop 1 or max-tier orchestrator ruling).
- **Loop 6 — ship second-opinion.** Same pattern: fresh low-tier session reads `5-user.md` + the project context + Carry, returns `OK diff matches plan: clean` | `EXTRA <file>` | `MISSING-CRIT <criterion-id>`. Out-of-scope files or unmet criteria fold into the existing `extras:` / `RETURN loop=4b reason=dirty-tree` paths. The verifier never edits — pure audit.

The verifier is **fresh** (own context, not the executor's), **cheap** (haiku), and **silent unless wrong**. This matches Voyager's separate-self-verification primitive directly. Same-executor self-review remains the first line of defense in Loops 1 and 3; the verifier is the gate that closes the loop on biases the executor cannot see in its own work.

---

## Cost Gate

- Standard path ≈ 8 short sessions. If the task would take a single medium-tier session <30 min end-to-end, it must be `padaria` — re-check the gate before proceeding.
- Any loop file hitting the ~80-line cap → the task is too big; split via `RETURN loop=1 reason=split-needed`.
- The orchestrator context must stay near-empty: verdict lines only. If you find yourself pasting loop file contents into the orchestrator, the flow is being run wrong.

Never end a loop with planning-only chat. Never claim the flow is complete unless `6-ship.md` exists on disk with a commit hash.

## Field Practice (overrides of the Autorouting table)

The bullets below were observed in the `isoroll` post-freeze run (2026-07-14 — 4 chains, 3 shipped same-day) and are **load-bearing spec, not optional notes**. Each names which Autorouting table row it overrides; conflict between a bullet and the table → the bullet wins. That is why they stay here and not in [`prior-art.md`](prior-art.md): field *notes* are history, field *practice* is spec.

| Bullet (below) | Overrides Autorouting row | Effect |
|---|---|---|
| Loop 0 inline when hot | Loop 0 — clarify (high) | Orchestrator can author `0-clarify.md` directly at `max` instead of spawning a craft-high session for the interview |
| Pin branch base in spawn prompt | Loop 2 — branch (implicit, low) | Orchestrator names `base:` non-discretionally when lineage is non-obvious; saves a full plan re-ground |
| Dirty-tree fence | Loop 6 — diff scope | Pre-existing dirty paths listed under `extras: pre-existing-dirty`, not flagged as `RETURN loop=4b reason=dirty-tree` |
| RETURN into high-tier → orchestrator-max inline | Escalation rules + max-gate | RETURN to a high-eligible loop → orchestrator amends target file at `max` inline instead of spawning a max executor; only sanctioned structural relaxation |
| Executor death mid-4b → fresh executor continues | Loop 4b escalation clock | Recovery primitive at 4a→4b seam; red-run clock resets from new ground truth after recovery |

- **Loop 0 inline when context is hot.** If the orchestrator session already holds the user's decisions (approved plan, fresh interview), author `0-clarify.md` directly instead of spawning — the interview is the one thing executors can't do, and delegation would launder context through a lossy retelling.
- **Pin the branch base in the spawn prompt** when repo lineage is non-obvious (e.g., docs/spec live on an unmerged branch, `develop` lacks them). A wrong base costs a full plan re-ground. Correction pattern: append-only `## Plan Correction (orchestrator)` section; instruct the next loop that it overrides.
- **Dirty-tree fence.** Pre-existing uncommitted changes in the target repo: name the contaminated paths in every spawn prompt from 4b on, and make Loop 6 list them under `extras: pre-existing-dirty` instead of flagging. Never let an executor "helpfully" commit or revert them.
- **RETURN into a high-tier loop lands on max = the orchestrator.** Don't spawn; rule inline (append `## Amendment` to the target loop file with the ruling + sharpened seams + re-entry route). Distinguish design-wrong from seam-gap: if the architecture already specifies the missing behavior, don't redesign — sharpen seams so 4a must cover it, re-run 4a→4b at default tiers.
- **Executor death mid-4b (session limit) is cheap to recover**: fresh executor reads 4a + partial 4b, re-runs test-cmd for ground truth, continues append-only. Budget hint: 4b is the expensive loop (~150–260k tokens); near a quota boundary, hand off at the 4a→4b seam rather than starting it.
- **Two loops, one repo = worktree fight.** Same-repo loops run sequentially (branch checkouts collide); cross-repo loops parallelize freely.

## Loop 6.5 — Skill Extraction (Voyager-style skill library)

After Loop 6 ship (and before deleting `.loop/<slug>/` unless `keep-trail: yes`), one low-tier executor reads the chain's `3-arch.md` (Adversarial pins / medium-executor traps section) + `4b-code.md` attempt log + `5-user.md` flag-and-fix, extracts any *reusable design pattern*, and appends it (frontmatter: domain tags + provenance link to the kept `.loop/` or commit hash) to `core/flows/.loop-skills/<domain>.md`. New `domain` files are created as needed; sub-domains reuse an existing file. Loop 1 plan-review is then instructed to grep `core/flows/.loop-skills/` for relevant prior patterns **before** authoring a new plan — Voyager's "skill library" primitive, made durable across runs.

The skill registry is small by construction: only patterns that would otherwise die with the chain. If nothing reusable exists (the common case for `padaria` and small `standard` chains), Loop 6.5 writes nothing and the registry doesn't grow — Voyager's library accrues skills; /loops accrues *patterns* and only when they're worth saving.

Extract is one low-tier session, ~30 lines, optional `keep-trail: yes` chains only.
