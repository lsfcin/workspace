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

## Core Principle — Files, Not Conversation

Each loop is executed by a **fresh session** of the cheapest capable model. That session receives only:

1. Its own loop section from this flow file.
2. **One** input file: the previous loop's output (which embeds the Carry block — see below).

It never receives conversation history. It appends its output to its own loop file and returns a **one-line verdict** to the orchestrator. The orchestrator never reads loop file contents — only verdicts. This is how the flow *saves* tokens instead of spending them: N cheap short sessions instead of one long expensive one.

### File protocol

- Directory: `<project>/.loop/<feature-slug>/` inside the target project's own repo.
- Files: `0-clarify.md`, `1-plan.md`, `2-ground.md`, `3-arch.md`, `4a-tests.md`, `4b-code.md`, `5-user.md`, `6-ship.md`.
- **Append-only.** Executors add sections; never rewrite prior content. Corrections are new appended sections.
- **Executor self-report.** Every appended section ends with `executor: <agent-type> model=<model> tier=<tier>` — after a run, `grep executor .loop/<slug>/*.md` audits whether routing actually happened.
- **Small.** Soft cap ~80 lines per file. A loop file that wants to exceed the cap is a smell: the task is too big — raise `FLAG: RETURN loop=1 reason=split-needed`.
- **Carry block.** Every loop file starts with a `## Carry` block **copied verbatim** from the previous file (Loop 0 creates it). It holds: slug, branch, project root, test command, criticality, acceptance-criteria digest, context pointers (project `CONTEXT.md`/`AGENTS.md` paths). This is what makes "read exactly one file" true — no loop ever needs to chase earlier files.
- `.loop/` is committed on the feature branch during the flow (audit trail, survives crashes). Loop 6 folds the durable outcome into the project's `ROADMAP.md` (workspace policy: plans live in roadmaps) and deletes `.loop/<slug>/` in the final commit unless Loop 0 recorded `keep-trail: yes`.

### Carry block template

```markdown
## Carry
slug: <feature-slug> | branch: <branch-name> | root: <project path>
test-cmd: <exact command, e.g. `npm test`> | e2e-cmd: <or "none">
criticality: <low|normal|critical> | verdict: <padaria|standard|critico>
criteria: <one line per acceptance criterion, numbered C1..Cn>
tasks: <filled by Loop 1 — one line per row: Tn — task — files — tier>
context: <paths to project CONTEXT.md / AGENTS.md the executor must read>
```

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

### Tier → model mapping — VOLATILE (checked 2026-07, revise freely)

| Tier | Model |
|---|---|
| low | haiku 4.5 |
| medium | sonnet 5 |
| high | opus 4.8 |
| max | fable 5 |

## Return Flags

Flag line format, appended at the end of the executor's section:

```
FLAG: RETURN loop=<N> reason=<slug> evidence=<one line>
```

- The executor **raises**; the orchestrator **routes**. A return of ≤1 loop backwards is honored automatically.
- Two consecutive returns to the same loop, or any `RETURN loop=0`, stops the flow and goes to the **user** — the intent itself is in question.
- The receiving loop re-runs at **one tier above** its default (the cheap tier already failed to produce a survivable artifact).

## Orchestration

The orchestrator (lead session, any tier) holds only: slug, current loop number, verdicts, flags.

**Routing is structural, not discretionary:** in Claude Code, spawn via the pinned agent types `loop-low`, `loop-medium`, `loop-high` (`.claude/agents/loop-*.md` — model is fixed in the agent definition's frontmatter, so the tier→model mapping cannot drift). Only where pinned agents are unavailable, fall back to a generic subagent passing the model explicitly. Spawn each loop with this prompt — nothing more:

```
Read core/flows/loop-engineering.md, section "Loop <N>" plus "Core Principle",
"Autorouting", "Return Flags". Then read <project>/.loop/<slug>/<input-file>.
Execute Loop <N>. Append your output to <project>/.loop/<slug>/<output-file>
following the embedded template. Reply with ONE line:
OK <verdict> | FLAG <flag line> | BLOCKED <reason>.
```

No runtime `subagent`/`Agent` tool → the user runs each loop as a fresh session with the same prompt; the flow is unchanged.

### Runtime portability

The flow itself is runtime-agnostic — all state lives in `.loop/` files, so any agent that reads files and runs git can execute a loop. Only the **pinned executor definitions** are per-runtime (same body, different frontmatter dialect):

| Runtime | Executor definitions | Model field | Status |
|---|---|---|---|
| Claude Code | `.claude/agents/loop-{low,medium,high}.md` | `model: haiku\|sonnet\|opus` | in place |
| opencode | `.opencode/agents/loop-{low,medium,high}.md` (`mode: subagent`) | `model: anthropic/<model-id>` — VOLATILE, verify ids | in place |
| Copilot CLI | `.github/agents/loop-*.md` **in the target project's repo** (or `~/.copilot/agents/`) | `model: <model-id>` | recipe only — copy the Claude Code bodies, adjust frontmatter |
| anything else | none — manual mode: user opens a fresh session per loop with the spawn prompt and picks the model | — | always works |

Adapting to a new runtime ≈ 30 min: mirror the three executor bodies, translate the frontmatter, dry-run one padaria task.

**rtk note:** the rtk hook rewriting shell commands (`grep` → `rtk grep`, test runners, git) is compatible — verified that `grep executor` output passes through intact, and rtk's compression of test output is *aligned* with this flow's token economy. If any audit output looks over-filtered, bypass with `rtk proxy <cmd>`.

---

## Loop 0 — Clarify

**Tier:** high (max if ambitious/innovative). **Input:** the raw request + user interview. **Output:** `0-clarify.md`. The only interactive loop.

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
```

**Padaria shortcut:** verdict `padaria` → skip Loops 1, 3, 4a, 5. One medium-tier session does: append a ≤5-line micro-plan to `0-clarify.md`, execute Loop 2 (branch), edit, run the **existing** test suite, execute Loop 6. Two files total (`0-clarify.md`, `6-ship.md`). The flow must never cost more than the task.

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

```markdown
## Carry
<copied>

## Architecture
<per file: path — responsibility — key functions/signatures — plan task ids>

## Evaluation
criteria-coverage: C1→<where> ... Cn→<where>
seams: <how each criterion will be tested>
verdict: PASS | FAIL <reason>
```

**Flags:** an acceptance criterion cannot be satisfied by any reasonable design → `RETURN loop=1 reason=criterion-infeasible`; two criteria contradict → `RETURN loop=0 reason=criteria-conflict`.

## Loop 4a — Tests First

**Tier:** medium. **Input:** `3-arch.md`. **Output:** `4a-tests.md`.

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

---

## Cost Gate

- Standard path ≈ 8 short sessions. If the task would take a single medium-tier session <30 min end-to-end, it must be `padaria` — re-check the gate before proceeding.
- Any loop file hitting the ~80-line cap → the task is too big; split via `RETURN loop=1 reason=split-needed`.
- The orchestrator context must stay near-empty: verdict lines only. If you find yourself pasting loop file contents into the orchestrator, the flow is being run wrong.

Never end a loop with planning-only chat. Never claim the flow is complete unless `6-ship.md` exists on disk with a commit hash.

## Orchestrator Field Notes (2026-07-14, isoroll post-freeze run — 4 chains, 3 shipped same-day)

- **Loop 0 inline when context is hot.** If the orchestrator session already holds the user's decisions (approved plan, fresh interview), author `0-clarify.md` directly instead of spawning — the interview is the one thing executors can't do, and delegation would launder context through a lossy retelling.
- **Pin the branch base in the spawn prompt** when repo lineage is non-obvious (e.g., docs/spec live on an unmerged branch, `develop` lacks them). A wrong base costs a full plan re-ground. Correction pattern: append-only `## Plan Correction (orchestrator)` section; instruct the next loop that it overrides.
- **Dirty-tree fence.** Pre-existing uncommitted changes in the target repo: name the contaminated paths in every spawn prompt from 4b on, and make Loop 6 list them under `extras: pre-existing-dirty` instead of flagging. Never let an executor "helpfully" commit or revert them.
- **RETURN into a high-tier loop lands on max = the orchestrator.** Don't spawn; rule inline (append `## Amendment` to the target loop file with the ruling + sharpened seams + re-entry route). Distinguish design-wrong from seam-gap: if the architecture already specifies the missing behavior, don't redesign — sharpen seams so 4a must cover it, re-run 4a→4b at default tiers.
- **Executor death mid-4b (session limit) is cheap to recover**: fresh executor reads 4a + partial 4b, re-runs test-cmd for ground truth, continues append-only. Budget hint: 4b is the expensive loop (~150–260k tokens); near a quota boundary, hand off at the 4a→4b seam rather than starting it.
- **Two loops, one repo = worktree fight.** Same-repo loops run sequentially (branch checkouts collide); cross-repo loops parallelize freely.
