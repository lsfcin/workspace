---
description: Architecture-decision subtree of the loop tree — turn a design/technology choice into a recorded decision (problem → options → trade-offs → decision → ADR). Produces a durable decision record, not code.
args: <the decision to make>
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `core/tools/` for runtime-specific mappings. Agent delegation: use `Agent`/`subagent`/`task` when available.

Decide: $@

This is an execution request. Produce a recorded decision, not a discussion. Reached via [`loop-router.md`](loop-router.md) with `subtree: architecture`; see [`LOOP-TREE.md`](LOOP-TREE.md).

## When this subtree runs

A task that *chooses between designs, patterns, or technologies* — "Redis vs in-memory", "how should module boundaries split", "sync or event-driven". Distinct shape from `feature` (which builds) and `research` (which gathers): its output is a **decision with a rationale, recorded durably** so it is not re-litigated. If the decision then needs building, chain into the `feature` subtree with this ADR as an input constraint.

## File protocol

- Directory: `<project>/.loop/<decision-slug>/`. Files append-only. Carry block copied verbatim between steps (same discipline as the feature subtree).
- The **durable output** is an ADR entry, NOT the `.loop/` trail: by default a new `### <NNNN> <Decision>` subsection under `SPECS.md` § Architecture Decisions (the template already defines that structure); for a large/standalone decision, a `docs/adr/<NNNN>-<slug>.md` file instead. `.loop/<decision-slug>/` is deleted on record unless `keep-trail: yes`.

## Step A0 — Frame  ·  **Output:** `0-frame.md`

Interview until you can state: the decision (one sentence), why now, the **constraints** it must satisfy, the **criteria** it will be judged on (C1..Cn — e.g. latency, cost, operability, fit with existing patterns), criticality, and whether the user wants to approve the final decision (`decision-signoff: yes|no`, default **no** — recommended permissive, mirrors the feature subtree panel). Stop if the decision or its criteria can't be stated — it isn't ready.

## Step A1 — Options  ·  **Output:** `1-options.md`

Enumerate **≥2 real options** (no strawmen — each must be something a competent engineer would actually consider). For each: a one-paragraph description and how it would be realized in *this* project. Include the "do nothing / status quo" option when it is viable.

## Step A2 — Trade-offs  ·  **Output:** `2-tradeoffs.md`

A matrix: criteria C1..Cn (rows) × options (columns), each cell a concrete assessment (not "good/bad" — the actual cost/limit). Below it, per option: what you **give up** by choosing it, and its main risk. Ground claims in evidence where it exists (benchmarks, the project's own constraints, prior ADRs); mark inferences as inferences.

## Step A3 — Decide  ·  **Output:** `3-decision.md`

Pick one option. State the rationale **by reference to the trade-off matrix** (which criteria drove it), and name explicitly what is sacrificed. If `decision-signoff: yes`, present A1+A2+the proposed decision and wait for the user's OK (or redirection) before recording; else proceed.

## Step A4 — Record (ADR)  ·  **Output:** the durable ADR + `4-record.md`

Write the decision record. Default target: append to the project `SPECS.md` § Architecture Decisions:

```markdown
### <NNNN> <Decision title>
- **Date:** <date>  ·  **Status:** proposed | accepted  ·  **Criticality:** <low|normal|critical>
- **Context:** <the problem + constraints, 2-3 lines>
- **Options considered:** <one line each, the rejected ones named>
- **Decision:** <what was chosen>
- **Consequences:** <what this enables and what it costs / forecloses>
- **Provenance:** <.loop/<decision-slug>/ if kept, or "trail dropped">
```

Then: update `ROADMAP.md` if the decision spawns work; delete `.loop/<decision-slug>/` unless `keep-trail: yes`; commit on a `feature/*` branch (the gitflow gate applies). Do not merge — the user's call.

**Chain-out:** if the decision requires implementation, hand the ADR to the `feature` subtree as an input constraint for its Loop 3.5 Contract Layout — the ADR bounds the module contracts.

Never end with chat-only: the ADR must exist on disk.
