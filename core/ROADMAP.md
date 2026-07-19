# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work archived in [HISTORY.md](HISTORY.md).

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
Reference implementation = `flows/deepresearch.md` (the validator's oracle; never "fixed").

## Open

- [ ] **2b — loop-agent tier source + generator.** Create `core/agents/loop-{low,medium,high}.md`
      carrying `tier:`; extract loop-engineering's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/loop-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
      **BLOCKED:** `loop-*` + `loop-engineering.md` are actively owned by a parallel session; resume
      once that work commits and the files go clean. See [[feedback-parallel-sessions]].
- [ ] **Flow sweep — utility + domain tier.** watch, autoresearch, summarize (`type: utility` +
      tool-discipline/integrity only); mechanism-search (see below). Add `type:`/`confirm:` to each.
- [ ] **mechanism-search normalize** (user chose normalize, not exempt): add frontmatter
      (`type: domain`), Tool-Discipline block, artifacts contract; keep its human-in-loop Habermas
      steps and `branches/instituto/` output target.
- [ ] **Flow/agent field validation.** Extend `sync-skills --check` (or a sibling) to assert flow
      `type ∈ enum` + `confirm ∈ enum` and agent `tier ∈ enum` + worker-has-tools. Turn on only after
      the sweep so the tree stays green. Consider a ratchet (new files only) like pre-commit §1d.
- [ ] **Skill `flow:` field.** For THIN skills (loops, research), record the dispatched flow slug in
      frontmatter per SCHEMA, so the skill→flow edge is data, not prose.
- [ ] **Narrow the `**/*audit.md` gitignore pattern.** It still hides any `*audit.md` anywhere; only
      `core/flows/audit.md` is negated. Scope it to its intended target (likely generated audit
      reports) or convert to per-path, so no other real doc goes silently untracked.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
