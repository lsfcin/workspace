---
description: Scout a topic across web + repos + academia in refined rounds, then convert the findings into a model-tiered, impact-flagged action plan written into the target project's ROADMAP. For "research X, then tell me what we should do about it in our own system".
args: <topic> [target ROADMAP path]
type: domain
confirm: plan
agents: researcher
---

Scout and plan for: $@

This is an execution request. Do not explain the protocol — run it.

## Tool Discipline (read first)

Tool names are literal; use only tools visible in the current tool set. Gathering tools:
`core/tools/search` (web), `core/tools/code-search` (repos), `core/tools/papers` (academia,
`--ss`/`--reviewed`/`--min-cit` for venue filtering), `core/tools/fetch` (URL). If a tool
returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

## Required Artifacts

Every run must leave two things on disk before the final response:
- reference lines appended to the relevant `refs/REFS.md`, tier-tagged (Step 3);
- the plan written into the target ROADMAP (Step 6).

Never end chat-only after Step 2 begins. If gathering is blocked, write a partial plan marked
`BLOCKED` and say what failed. Read every source before summarizing it; never invent sources,
venues, tiers, or results.

## When to use this vs. a plain research flow

`deepresearch` / `lit` produce a **research brief** — knowledge for its own sake.
`scout` produces an **action plan for our own workspace/project** — it always ends by asking
"so what should *we* change, and how?". Use `scout` when the topic exists to inform a decision
about the system you are working in. If the user just wants to understand a topic, use
`deepresearch` instead.

The gathering half of this flow **reuses** the research machinery; the distinctive part is the
back half (map-to-system → tiered plan). Do not reimplement search here — delegate.

## Step 1 — Frame

Write a one-paragraph frame: what decision this scouting serves, and which project/ROADMAP the
plan will land in. If the target ROADMAP is not given, ask which one (a plan with no home is a
violation of the workspace "plans live in roadmaps" rule).

## Step 2 — Gather, in refined rounds

Run **at least two rounds**. Round 1 is broad; let its findings sharpen Round 2's queries —
never fire all queries at once. Hit three surfaces every round: **web** (`core/tools/search`,
blogs + labs + companies), **repos** (`core/tools/code-search`), **academia**
(`core/tools/papers`). For a large topic, delegate surfaces to `researcher` subagents; for a
narrow one, search directly.

**Source-tier discipline is mandatory** (full rule: [`core/refs/CONTEXT.md`](../refs/CONTEXT.md)).
arXiv is the easiest surface, so an unguarded pass returns almost only preprints, which are
**not peer reviewed**. Every round must also reach published venues (ACL/EMNLP anthology, ACM
DL, IEEE, OpenReview with an accepted venue). `core/tools/papers --ss` reports `venue` +
`peer_reviewed`; `--reviewed` drops preprints, `--min-cit N` drops noise. Prefer the published
URL over the arXiv one when both exist.

## Step 3 — Capture references

Write every kept reference into the relevant `refs/REFS.md` (the target project's, or
`core/refs/REFS.md` for workspace-level work), one line each, **tagged with its tier**
`[A] [B] [P] [V] [C]` and a short "why it matters to us". A round that yielded only `[P]` is
incomplete — say so and re-run before concluding. This capture is not optional: it is what
makes the next scout on a related topic cheap.

## Step 4 — Map to our system

Read the actual state of the target project (its CONTEXT.md, ROADMAP, relevant code/docs).
For each finding, state plainly: does it **confirm** what we do, **contradict** it, or reveal a
**gap**? Cite the source tier for each claim. Contradictions and gaps become plan items;
confirmations become a short "we are already aligned on X" note (equally valuable — it stops us
re-solving solved problems).

## Step 5 — Write the tiered, flagged plan into the ROADMAP

Organize the plan as **frentes** (fronts), each a self-contained line of work with numbered
steps. Every step carries three things:

- **impact flag** — 🔴 `decide-first` (changes shared policy or touches security; needs Lucas's
  sign-off + more evidence before coding — usually with an open question), 🟡 `pilot-first`
  (prove on one subtree, measure, then generalize), 🟢 `safe` (mechanical/additive, low blast
  radius). A frente that changes workspace-wide behavior **opens** with a 🔴 step.
- **model tier** — the *floor* tier that suffices: `haiku` (mechanical), `sonnet` (normal
  engineering/writing), `opus` (design, security, cross-cutting judgment). Bigger always works,
  it just costs more.
- **switch mechanism** — how that tier gets onto that step (see the canonical guide below).

State the **evidence caveat once** for the whole plan: where a step leans on preprint-only
evidence, mark it and keep it 🔴/🟡 — a preprint never becomes a hard gate on its own.

End the plan with a **sequencing** section ordered by (impact × cheapness) ÷ risk, and note
that the 🔴 steps are the discussions to have before any code.

## Canonical model-switching guide (reusable — reference this, do not re-tabulate per plan)

| Mechanism | When to use | Who acts |
|-----------|-------------|----------|
| **Same session, `/model`** | The next whole chunk needs a different tier. Cheapest for a sustained stretch at one tier. | **User** flips it; an agent cannot change its own session model. |
| **`/loops` autorouting** | A codeable feature with mixed-tier steps. The loop plan assigns loop-low(haiku)/medium(sonnet)/high(opus) per step; no manual switch. | The flow spawns the right tier per loop. |
| **Agent tool `model:` override** | One sub-task needs a different tier than the driver — especially eval, where the graded model must be the weak one. | The driving agent spawns a sonnet/haiku subagent inline; no session change. |
| **Handoff (`/handoff`)** | A clean tier boundary + heavy context: finish the design phase at one tier, start a fresh session at another carrying only the resume prompt. | **User** starts the new session at the chosen model. |

**Default mapping:** 🔴 decide-first steps → **Opus, same session** (judgment about shared
behavior). 🟢/🟡 build steps → **Sonnet via `/loops`** (mechanical parts drop to haiku
automatically). Run **haiku deliberately** only where a weak model is the *subject under test*
(e.g. behavioral eval gold tasks), spawned via the Agent-tool override.

## Step 6 — Confirm before writing

Summarize the frentes briefly and ask:

`Write this plan into <ROADMAP path>? Reply "yes", or tell me what to change.`

Only after confirmation: write the plan into the ROADMAP (inline or as a referenced sub-roadmap
file), link it from the project's goal/CONTEXT, and confirm the refs are captured. Keep the
final chat response brief: link the ROADMAP, the refs file, and flag the 🔴 steps that need
discussion.
