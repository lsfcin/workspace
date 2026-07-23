# Core Library Schema
> The enforced frontmatter contract for skills, flows, and agents. Drift from this is a bug.

Companion to the code-side spec-drive convention (the `> spec:` module gate in `.hooks/pre-commit`,
tracked under the [[spec-driven-development]] goal): that governs `code/` modules, this governs the
`core/` agent library.

**No flow is privileged.** The exemplar is [`flows/_template.md`](flows/_template.md) — a template,
nothing more. There is no "reference implementation" whose behaviour defines correctness (that dual
role coupled one flow's evolution to the schema; retired 2026-07-23). Realism is guaranteed by
`validate_flows` running over *every* flow, including the template, not by anointing one.

## The one rule

**Execution metadata lives on the executor (agent), never on the skill.**
A skill is a trigger. A flow is a procedure. An agent is the thing that runs, so tier/tools/output
belong to it. Provider and model names (`opus`, `haiku`, `claude-*`) appear **only in generated
runtime mirrors** (`.claude/agents/*`), never in `core/` source — exactly the
`core/skills → .claude/skills` split, now extended to agents.

```
skill  (trigger)   →  flow  (procedure)   →  agent  (executor)   →  subagent
name,description       description,args,       name,description,
[flow]                 type,confirm,[agents]   tier,[tools],[output],[defaultProgress]
```

The graph is a **sparse typed DAG**, one direction. Skills do not point to skills.

## Layer: skill — `core/skills/<name>.md`

| field | req | value |
|-------|-----|-------|
| `name` | ✅ | kebab-case, matches filename |
| `description` | ✅ | actionable; drives the menu. End with "Invoke with /name [args]." |
| `flow` | — | slug of the flow this skill dispatches to (THIN skills only); routers list all dispatchable flows as a comma list, same shape as a flow's `agents:` |

No `model`, `tier`, `tools`, or `subagents` on a skill — those are execution detail, pushed down.
A skill is THIN (dispatches to a flow) or FAT (self-contained protocol); both are valid. Any
`core/skills/*.md` that is not a skill (status doc, ADR) does **not** belong here — the validator
rejects a file with no `name`/`description` frontmatter.

## Layer: agent — `core/agents/<name>.md`

| field | req | value |
|-------|-----|-------|
| `name` | ✅ | matches filename |
| `description` | ✅ | one line: what evidence/output this worker produces |
| `tier` | ✅ | `low` \| `medium` \| `high` \| `max` — the provider-agnostic effort ladder (same as the craft flow) |
| `tools` | ▲ | comma list; required for **worker** agents (locked-down allowlist) |
| `output` | ▲ | default artifact filename; required for workers |
| `defaultProgress` | — | `true` for long workers |

**Agent variants:**
- **worker** (researcher, verifier, writer, reviewer): all six fields; `tier` + `tools` + `output` mandatory.
- **orchestrator** (lead): `name` + `description` + `tier` only. `tools`/`output`/`defaultProgress`
  are N/A — the orchestrator inherits the full toolset and owns no single artifact.

`tier` is the source of truth. The runtime mirror generator resolves `tier → provider/model` via
[`tier-map.json`](tier-map.json) when a runtime needs a concrete model (Claude Code's `.claude/agents/`).
**No `thinking:` and no `model:` in `core/agents/` source** — that was the old two-convention drift.

## Layer: flow — `core/flows/[<skill>/]<name>.md`

**Location rule.** A flow owned by a dispatcher skill lives in `core/flows/<skill>/` and its
**filename equals the command tail** — `core/flows/research/scout.md` ⟺ `research scout`. Flows not
owned by any dispatcher skill stay flat at `core/flows/`. Validation is recursive (`sync-skills`
`validate_flows` walks subfolders); a `<skill>/CONTEXT.md` is exempt like the root one. The
engineering cluster owned by the `loops` skill lives in [`flows/craft/`](flows/craft/) —
`craft` · `route` · `architect` (+ the `TREE.md` map) — and is exempt from the table below.

| field | req | value |
|-------|-----|-------|
| `description` | ✅ | one line: what the flow produces |
| `args` | ✅ | arg signature, e.g. `<topic>` |
| `type` | ✅ | `research-brief` \| `utility` \| `domain` |
| `confirm` | ✅ | `plan` (stop for explicit "yes" before work) \| `none` (summarize plan, continue) |
| `agents` | — | comma list of worker agents the flow may spawn |
| `uses` | — | comma list of other flows this flow invokes; empty/absent = leaf. The `uses:` graph must be a **DAG** (see *Composition and cycles*), enforced by `validate_flows` |

`confirm` exists to kill the old contradiction where some flows blocked for approval and others
didn't, with no way for a caller to know which. Now it is declared and readable.

### Disciplines by flow `type`

Legend: ✅ required · ~ recommended · — not required

| discipline | research-brief | utility | domain |
|------------|:--:|:--:|:--:|
| **tool-discipline** — literal tool names, "use only visible tools", map-or-block on `Tool not found` | ✅ | ✅ | ✅ |
| **required-artifacts** — explicit on-disk file list + "never end chat-only after work starts" | ✅ | ~ | ✅ |
| **provenance** — `<slug>.provenance.md` sidecar (or a declared running log) | ✅ | — | ~ |
| **scale-gate** — explicit direct vs decomposed rule ("narrow explainer → no subagents") | ✅ | ~ | ~ |
| **integrity** — read-before-summarize, honest status, no invented sources/results | ✅ | ✅ | ✅ |

The canonical wording for each discipline lives in [`flows/_template.md`](flows/_template.md), each
block annotated with the types that require it — **copy from there**. Symmetry is required **within
a type**, not flattened across all flows: a scheduler (`utility`) is not forced to emit a provenance
sidecar. Holding the wording is the template's only privilege; it is still just a template, not a
reference implementation.

Flow-type assignments:
- **research-brief:** sota, literature, review, recipe, compare, audit, replicate, draft (in `flows/research/`)
- **utility:** watch, explore, summarize (in `flows/research/`)
- **domain:** mechanism-search
- **engineering:** `craft` · `route` · `architect` (in `flows/craft/`) — its own protocol, declares
  tier routing directly; exempt from this table and from flow-layer validation. **Known asymmetry:**
  `engineering` is not in the `type` enum, so the cluster is exempted by path rather than typed. The
  symmetric fix (add `engineering` to the enum, give the three flows real frontmatter, delete the
  exemption) is a schema change and is queued in [ROADMAP.md](ROADMAP.md), not taken silently here.

## Composition and cycles

> Decided 2026-07-23. Vocabulary: **"flow" is the canonical term.** "Loop" is retired for the
> orchestration/connected-agents sense — a real, tight repeat may still be called a loop, but the
> thing that connects agents is a *flow*. "Flow" is also the more accurate word: a loop runs end→start
> with no branching and one exit; our procedures branch, escape, and compose.

**Flows compose.** A flow may invoke another flow, declared as `uses: <flow>, <flow>`. Composite
versus leaf is **not a type** — it is merely whether a flow happens to invoke others. There is no
separate "orchestrator" layer in the schema.

**Two kinds of cycle. They live in different places, and only one is legal.**

| | Definitional cycle | Execution cycle |
|---|---|---|
| What | flow A is *built from* B, B is *built from* A | one flow runs step 3, decides "not good enough", returns to step 2 |
| Graph | the `uses:` graph (definition time) | the runtime trace (execution time) |
| Verdict | **forbidden** | **allowed** |
| Why | never bottoms out — expanding it is infinite | it is *iteration*: state changes each pass, it makes progress |
| Guard | static check: walk `uses:` links, error if any path returns to its start (the `uses:` graph must be a **DAG** — directed acyclic graph: arrows only point at what a flow is built from, and no path leads back to where it began) | runtime **iteration cap** (max N retries) plus an explicit exit condition |

**Why a runtime trace may revisit a flow without breaking the DAG.** An orchestrator `A` that uses
`B` and `C` produces the trace `A → B → C → A → B → C → …`. That is legal: the `uses:` graph holds
only `A → B` and `A → C`. `B` and `C` never call `A` — the back-arrow in the trace is *`A`'s own
bounded execution loop* deciding to go around again. Composition points **downward** through layers;
only the top layer repeats, and it repeats under a cap. Structure is acyclic; the trace need not be.

This mirrors how effective agent loops (ReAct, Reflexion, Voyager) avoid running forever: an exit
condition, a hard iteration cap as backstop, and **state that changes each pass**. A cycle whose
state does not change is not iteration — it is a hang.

## Enforcement

`core/tools/sync-skills --check` parses frontmatter and fails on violations; it is wired into
`.hooks/pre-commit`. All three layers are live:
- **skill:** frontmatter present, `name:` + `description:`, non-skills rejected.
- **flow:** `description:` + `args:` present, `type ∈ {research-brief, utility, domain}`,
  `confirm ∈ {plan, none}`. Exempt: `CONTEXT.md`, `TREE.md`, `loop-*` (engineering cluster).
  Validation is **recursive** — it walks `flows/<skill>/` subfolders, not just the flat root.
- **composition:** every `uses:` target resolves to a real flow, and the `uses:` graph is a **DAG**
  (three-colour DFS; a path returning to its own start fails the check). The exemption list does
  *not* apply here — every flow file is a node, so an engineering flow cannot smuggle in a cycle.
  The **runtime iteration cap** is the other half of this guard and is *not* statically checkable:
  any flow with an execution loop must declare a numeric cap plus an exit condition in prose
  (wording in [`flows/_template.md`](flows/_template.md) § Execution Loops). Do not try to enforce
  it with the DAG check — that check forbids cycles; the cap is what *permits* them, bounded.
- **agent:** `name:` + `description:` present, `tier ∈ {low, medium, high, max}`, `model:`/`thinking:`
  forbidden in source, workers (everyone but `lead`) must carry `tools:` + `output:`.
