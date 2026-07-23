# Core Library History
> Archive of completed work. Open work lives in [ROADMAP.md](ROADMAP.md).

## Completed — 2026-07-23

**Design symmetry across the skill/flow surface — naming grammar decided + shipped.**
Trigger was the apparent asymmetry `deepresearch` (flow) vs `/research scout` (sub-flow); it turned
out to be purely lexical (both were already sub-flows of the `research` skill), but it exposed a
missing ownership rule. Decision: a flow **owned by a dispatcher skill** lives in
`core/flows/<skill>/` and its **filename equals the command tail** (`research <verb>` ⟺
`flows/research/<verb>.md`); unowned flows stay flat. The axis is *invocation independence*, not
composition — `scout` composes `deep`/`literature` yet stays a sub-flow. Rule in
[SCHEMA.md](SCHEMA.md) (flow-layer Location rule) + [SPECS.md](SPECS.md) AD-08.

Shipped: the 12 research flows moved into `flows/research/`; renamed `deepresearch`→`deep`,
`autoresearch`→`explore`, `lit`→`literature`; `sync-skills validate_flows` made **recursive** (the
flat glob would have let nested flows escape schema validation silently); `research.md`,
`loop-router.md`, `LOOP-TREE.md`, `SCHEMA.md`, `SETUP.md`, `loops.md` repathed; back-compat aliases
kept in the dispatcher. Verified working on all three runtimes (CLI, VSCode extension, opencode).
Also retired the "reference implementation / validator's oracle" status of `deepresearch` — no flow
is privileged; the exemplar is `flows/_template.md`.
Commits: `9d8687f` (fold + recursive validator), `3a7a630` (craft-flows decision), `bbdff54` (stale-ref sweep).

Open follow-up: the **craft-flows** execution item (8 steps) in [ROADMAP.md](ROADMAP.md) — decided
this session, not yet built.

## Completed — 2026-07-18

Pilot: enforced per-layer frontmatter contract — SPEC-v0 of [[spec-driven-development]], `core/` side.
Commits: `5c22650` (schema + tier + bugs + enforcement), `d49a7ca` (flow sweep + audit.md fix).

- **SCHEMA.md** — per-layer frontmatter contract + flow-type/discipline matrix + the one rule
  (execution metadata on the executor; provider/model names only in generated mirrors).
- **Templates** — added `flows/_template.md` + `agents/_template.md` (only skills had one).
- **Bug: MIGRATION-STATUS leak** — moved `skills/MIGRATION-STATUS.md` → `core/MIGRATION-STATUS.md`
  (an ADR, not a skill); routing resynced.
- **Bug: reviewer** — added the `tools:` allowlist its peers had.
- **Bug: lead** — added `tier: high` (orchestrator variant).
- **Tier unification** — `thinking:`→`tier:` on all 5 `core/agents/*`; zero `thinking:`/`model:` in source.
- **Pilot flow: compare** — normalized to `research-brief` with full disciplines.
- **Enforcement** — `sync-skills` validates skill frontmatter + prunes orphan mirrors/commands (the
  dangling-symlink class that broke opencode startup); wired into `.hooks/pre-commit` §10a; negative-tested.
- **Flow sweep — research-brief tier** — all 8 research-brief flows declare `type:`/`confirm:` and carry
  required-artifacts + provenance + scale-gate + integrity: deepresearch (oracle, frontmatter only),
  compare, lit, review, recipe, audit, replicate (`confirm: plan`), draft. Plan-confirmation contradiction resolved.
- **Bug (latent, pre-existing)** — `.gitignore` rule `**/*audit.md` had kept `core/flows/audit.md`
  untracked (the audit flow was never committed); negated the path and committed the flow.

## Completed — 2026-07-19

Flow sweep closed (utility + domain tiers) and flow/agent validation turned on.

- **Flow sweep — utility tier** — watch (`confirm: none`), autoresearch (`confirm: plan`),
  summarize (`confirm: none`, `agents: researcher`) declare `type: utility`; each carries the
  full tool-discipline block (autoresearch was missing map-or-block) + an explicit integrity
  clause (no invented sources/metrics/claims; failures reported honestly).
- **mechanism-search normalized** — `type: domain`, `confirm: plan`, `agents: researcher, writer`;
  canonical Tool-Discipline block; required-artifacts contract (`outputs/.plans/`, `.drafts/<slug>-gen-N`,
  `<slug>-familias.md`, survivors → `branches/instituto/ROADMAP.md`); queue-rule + corpus check made the
  explicit plan gate; integrity section. Human-in-loop Habermas filter and Portuguese body kept intact.
- **Flow/agent validation live** — `sync-skills --check` now asserts flow `type`/`confirm` enums
  (+ description/args present) and agent `tier` enum + `model:`/`thinking:` ban + worker `tools:`/`output:`.
  `loop-*` cluster + `LOOP-TREE.md` exempt per SCHEMA (engineering protocol). Negative-tested in a fake
  workspace tree: all violation classes caught, exemptions honored. SCHEMA Enforcement section updated.
- **Gitignore `**/*audit.md` removed** — audit reports live under `outputs/` (already ignored), so the
  broad pattern only hid real docs (the class of bug that kept `core/flows/audit.md` untracked).
  Dropped it plus the now-redundant `!core/flows/audit.md` negation; verified nothing newly ignored
  or surfaced.
