# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work archived in [HISTORY.md](HISTORY.md).

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
No flow is privileged — the exemplar is `flows/_template.md`. (The old "reference implementation /
validator's oracle" status of `deepresearch` was retired 2026-07-23; see [SCHEMA.md](SCHEMA.md).)

## Open

- [ ] **Ad-hoc venv deps have no declared home — three now.** Each was `pip install`ed directly into
      `.venv` to unblock a tool, so a fresh workspace clone silently loses the capability:
      `pypandoc-binary` (`core/tools/parse` on `.docx`, else `FileNotFoundError: pandoc`),
      `secretstorage` (`core/tools/video` reading Brave cookies — without it yt-dlp fails with an
      AES-CBC decrypt error that reads like wrong credentials, cost a session to diagnose), and
      `gallery-dl` (`core/tools/video` image/carousel path). Fix the class, not the instances:
      a declared dep list or a SETUP.md step the whole `core/tools/` surface is checked against.
- [ ] **2b — loop-agent tier source + generator.** Create `core/agents/loop-{low,medium,high}.md`
      carrying `tier:`; extract loop-engineering's tier→model map to `core/tier-map.json`; add a
      generator that emits `.claude/agents/loop-*.md` with `model:` resolved. Removes the last
      provider-name-in-source violation (`model: haiku`). Symmetric with the skills mirror.
      **BLOCKED:** `loop-*` + `loop-engineering.md` are actively owned by a parallel session; resume
      once that work commits and the files go clean. See [[feedback-parallel-sessions]].
- [ ] **Skill `flow:` field — loops.md.** research.md done (`flow:` comma list, router shape).
      loops.md needs `flow: loop-engineering` (or the router slug once the loop tree lands).
      **BLOCKED:** same contention as 2b — `core/skills/loops.md` owned by the parallel session.

- [ ] **Survey outside skills, decide what to import.** Lucas's ask (INBOX 2026-07-23): take skills
      seriously as a category and study whether any are worth importing into `core/skills/`. Two
      concrete leads, both DM-bait posts that name skills without linking them, so both need a real
      search first: [five general Claude Code skills](https://www.instagram.com/reel/DavN_06t105/)
      (tool discovery, plan-before-code, cross-session project memory, frontend design, self-improvement
      — the first three overlap what `AGENTS.md` + `/loops` + CONTEXT.md already do, so the question is
      overlap vs gap) and the NB-oriented pair captured in `code/isoroll-content/refs/REFS.md`.
      Lucas also asked for a general sweep for **game-asset-generation** skills while doing this.
- [ ] **Audit context building — are we overdoing it?** Lucas's ask (INBOX 2026-07-23): measure what
      actually loads at session start (`AGENTS.md` chain + every `CONTEXT.md` on the path + memory)
      and whether it has grown past its worth. Includes: consider trimming `MEMORY.md`, and inspect
      what is being stored unannounced under the `~/.claude/` folders. Pairs with the session-size
      monitor and context-drift items already in `brain/TODO.md`.
      → **Now Frente 3.2 of [/ROADMAP.md](../ROADMAP.md)** (workspace-os robustness). Reframed by the
      2026-07-23 research: keep CONTEXT.md *local/granular* (it is what makes weak models work, per
      [P] 2607.17598), cap *chain depth* not file count. Do the audit there; this line is the pointer.

## craft-flows — the execution item (decided 2026-07-23, not yet built)

All of the below was **decided in discussion with Lucas on 2026-07-23** and needs an execution
session. The reasoning is recorded in [SCHEMA.md](SCHEMA.md) § *Composition and cycles*; read that
first. Nothing here is open for re-litigation — it is build work.

**The decision in one line:** "loop" is retired as the word for connected agents; **flow** is
canonical; flows compose into a DAG; loops live only at execution time, bounded.

- [ ] **1. Retire the `loop-*` vocabulary — rename + fold into `flows/craft/`.**
      `loop-engineering`→**`craft`**, `loop-router`→**`route`**, `loop-architecture`→**`architect`**,
      `LOOP-TREE.md`→**`TREE.md`**. Single-word filenames (Lucas's convention: prefer the full word
      over a truncation — this is why `architect` beat `arch` and `literature` beat `lit`). They move
      into `core/flows/craft/` per the ownership rule. Blast radius is cross-domain: ~14 `brain/`
      files reference `loop-engineering` by path (goals, `GOALS.md`, `.log/done.md`, attachments) plus
      the `loop-*` agents and both mirrors — **do this from a session already editing those goal
      files**, per the parallel-session partition rule. Update the `loop-*` exemptions in
      `SCHEMA.md` § Enforcement and in `sync-skills validate_flows` (they match on the `loop-` prefix).

- [ ] **2. Rename the goal + concept to `craft-flows`.** `brain/goals/loop-engineering.md` →
      `brain/goals/craft-flows.md`, and the concept "loop engineering" → "craft flows" **wherever it
      appears** (Lucas's call: option (c), applied broadly — not just the flow files). Includes
      `brain/GOALS.md`, `brain/goals/CONTEXT.md`, and the goal cross-refs in `spacemantics.md`,
      `spec-driven-development.md`, `workspace-os.md`. The `[[loop-engineering]]` wiki-links must be
      repointed or they dangle.

- [x] **3. `deep` → `sota`, and redefine what it produces.** Not a rename — a **redefinition**, which
      is why it was deliberately *not* done in the 2026-07-23 session (a `sota.md` still holding
      deepresearch content would be worse than leaving it). New contract:
      fill the relevant `refs/REFS.md` **plus per-paper `*.yaml`** files following the existing
      review/tier strategy, and emit a **≤200-line** summary *written to support a decision* — **not**
      a related-work section, not a giant brief. Rationale: the lean human-facing summary and the rich
      machine-facing yaml serve different readers (Lucas reads 200 lines; future flows read the yaml),
      which is the "artifact is the memory" thesis. Note the scope narrows from "deep dive on
      anything" to "map the state of the art of a field" — accepted, it makes a vague flow crisp.
      Name is `sota` (the field-standard acronym) — **not** `soat`, which reads as a typo of it.

- [x] **4. Make `scout` compose `sota` (the first real DAG edge).** `scout` and `sota` share the
      entire gathering half; today `scout.md` only *asks in prose* not to reimplement search. Make it
      a declared edge — `uses: sota` — so `scout = sota + map-to-our-system + write tiered plan into a
      ROADMAP`. Keep **both** entrypoints: `sota` alone when you want the field map and no plan;
      `scout` when you want the plan too. This is the dogfood case for the composition model.

- [x] **5. Consolidate the template; the oracle is already retired.** `SCHEMA.md` no longer anoints a
      reference implementation (retired 2026-07-23 — Lucas: *"sota should not be special… a template
      should be a template"*; the dual role coupled one flow's evolution to the schema). **Remaining
      work:** physically move the canonical discipline wording (tool-discipline, required-artifacts,
      provenance, scale-gate, integrity) out of `flows/research/deep.md` into `flows/_template.md`,
      annotated by which `type` requires each block, then repoint SCHEMA's "copy from there" pointer.
      SCHEMA currently carries an explicit *migration pending* note — delete it when done.

- [x] **6. Build the cycle guard (two mechanisms, do not merge them).**
      (a) **Static DAG check** in `sync-skills validate_flows`: parse `uses:` from flow frontmatter,
      walk the graph, fail with a clear message if any path returns to its start. This is definition
      time, offline, cheap — and `validate_flows` is already recursive, so it is the natural home.
      (b) **Runtime iteration cap** on execution loops (max N retries + an explicit exit condition),
      which is what makes step-level retry edges safe. (a) forbids cycles; (b) *permits* them,
      bounded. Applying (a) to retry edges would wrongly kill the useful loops.

- [ ] **7. Decompose the `craft` monolith by load-frequency.** `loop-engineering.md` is ~52 KB and
      mixes three levels: general rules that apply to *all* flows, the one specific build flow, and
      heavy reference material (field practice, case studies, prior art). Split by **access pattern**,
      not arbitrarily — this is what resolves the tension with our own finding that blind .md
      fragmentation hurts: (i) general flow rules → up to `SCHEMA.md` / `flows/CONTEXT.md`, since they
      were never specific to one flow; (ii) the always-loaded protocol → a lean `flows/craft/craft.md`;
      (iii) field practice / case studies / prior art → on-demand subfiles in `flows/craft/`, loaded
      only when relevant (the `skills/foundry/` pattern). Always-needed stays one file; rarely-needed
      becomes subfiles. Stratification, not fragmentation. Good technique to apply during the split:
      `/caveman-compress` **plus** an Opus pass that compresses *content* (redundancy, prose→table,
      outright cuts), not just wording.

- [ ] **8. Fold multi-mode skills into folders.** `skills/caveman*` (lite/full/ultra/wenyan variants,
      plus `caveman-commit`/`-review`/`-compress`/`-help`/`cavecrew`) → `skills/caveman/` with a
      router on top and one subfile per mode — same `skills/foundry/` pattern, same reasoning as
      item 7. Note these live in `~/.agents/skills/` (global, outside the workspace) and are **not**
      synced by `core/tools/sync-skills` — check that before moving anything.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
