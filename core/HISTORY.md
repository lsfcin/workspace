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
