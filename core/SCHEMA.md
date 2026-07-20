# Core Library Schema
> The enforced frontmatter contract for skills, flows, and agents. Drift from this is a bug.

Companion to the code-side spec-drive convention (the `> spec:` module gate in `.hooks/pre-commit`,
tracked under the [[spec-driven-development]] goal): that governs `code/` modules, this governs the
`core/` agent library. `deepresearch` is the reference implementation — the validator is calibrated
against it, so it is the one flow you never "fix".

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
| `tier` | ✅ | `low` \| `medium` \| `high` \| `max` — the provider-agnostic effort ladder (same as loop-engineering) |
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

## Layer: flow — `core/flows/<name>.md`

| field | req | value |
|-------|-----|-------|
| `description` | ✅ | one line: what the flow produces |
| `args` | ✅ | arg signature, e.g. `<topic>` |
| `type` | ✅ | `research-brief` \| `utility` \| `domain` |
| `confirm` | ✅ | `plan` (stop for explicit "yes" before work) \| `none` (summarize plan, continue) |
| `agents` | — | comma list of worker agents the flow may spawn |

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

The canonical wording for each discipline is in [`deepresearch.md`](flows/deepresearch.md); copy from
there. Symmetry is required **within a type**, not flattened across all flows — a scheduler
(`utility`) is not forced to emit a provenance sidecar.

Flow-type assignments:
- **research-brief:** deepresearch, lit, review, recipe, compare, audit, replicate, draft
- **utility:** watch, autoresearch, summarize
- **domain:** mechanism-search
- **engineering:** the `loop-*` cluster (loop-engineering + subtree flows + `LOOP-TREE.md` index) is its own protocol (declares tier routing directly); exempt from this table and from flow-layer validation.

## Enforcement

`core/tools/sync-skills --check` parses frontmatter and fails on violations; it is wired into
`.hooks/pre-commit`. All three layers are live:
- **skill:** frontmatter present, `name:` + `description:`, non-skills rejected.
- **flow:** `description:` + `args:` present, `type ∈ {research-brief, utility, domain}`,
  `confirm ∈ {plan, none}`. Exempt: `CONTEXT.md`, `LOOP-TREE.md`, `loop-*` (engineering cluster).
- **agent:** `name:` + `description:` present, `tier ∈ {low, medium, high, max}`, `model:`/`thinking:`
  forbidden in source, workers (everyone but `lead`) must carry `tools:` + `output:`.
