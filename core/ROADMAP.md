# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract lives in [SCHEMA.md](SCHEMA.md).

Goal: [[spec-driven-development]] — this is its SPEC-v0 pilot on the `core/` agent library.
Reference implementation = `flows/deepresearch.md` (the validator's oracle; never "fixed").

## Shipped (pilot, 2026-07-18)

- [x] **SCHEMA.md** — per-layer frontmatter contract + flow-type/discipline matrix + the one rule
      (execution metadata on the executor, provider/model names only in generated mirrors).
- [x] **Templates** — added `flows/_template.md` + `agents/_template.md` (only skills had one).
- [x] **Bug: MIGRATION-STATUS leak** — moved `skills/MIGRATION-STATUS.md` → `core/MIGRATION-STATUS.md`
      (it is an ADR, not a skill); routing resynced.
- [x] **Bug: reviewer** — added the `tools:` allowlist its peers had.
- [x] **Bug: lead** — added `tier: high` (orchestrator variant per SCHEMA).
- [x] **Tier unification** — `thinking:`→`tier:` on all 5 `core/agents/*`; zero `thinking:`/`model:`
      left in source. `tier ∈ {low,medium,high,max}`.
- [x] **Pilot flow: compare** — normalized to `type: research-brief`, `confirm: none`, full disciplines
      (required-artifacts + scale-gate + provenance), matching deepresearch.
- [x] **Enforcement** — `sync-skills` now validates skill frontmatter, prunes orphan mirrors/commands
      (the dangling-symlink class that broke opencode), and `--check` reports both. Wired into
      `.hooks/pre-commit` (§10a). Negative-tested: non-skill rejected, orphan flagged+pruned.

## Deferred (the sweep)

- [ ] **2b — loop-agent tier source + generator.** Create `core/agents/loop-{low,medium,high}.md`
      carrying `tier:`; extract loop-engineering's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/loop-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
- [ ] **Flow sweep.** Back-port disciplines per `type` to the remaining flows using deepresearch +
      compare as references: research-brief (lit, review, recipe, audit, replicate, draft),
      utility (watch, autoresearch, summarize). Add `type:`/`confirm:` frontmatter to each; resolve
      the plan-confirmation contradiction by declaring `confirm:` explicitly everywhere.
- [ ] **mechanism-search normalize** (user chose normalize, not exempt): add frontmatter
      (`type: domain`), Tool-Discipline block, artifacts contract; keep its human-in-loop Habermas
      steps and `branches/instituto/` output target.
- [ ] **Flow/agent field validation.** Extend `sync-skills --check` (or a sibling validator) to assert
      flow `type ∈ enum` + `confirm ∈ enum` and agent `tier ∈ enum` + worker-has-tools. Turn on only
      after the sweep so the tree stays green. Consider a ratchet (new files only) like pre-commit §1d.
- [ ] **Skill `flow:` field.** For THIN skills (loops, research), record the dispatched flow slug in
      frontmatter per SCHEMA, so the skill→flow edge is data, not prose.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
