# Core Library History
> Archive of completed work. Open work lives in [ROADMAP.md](ROADMAP.md).

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
