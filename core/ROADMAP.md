# Core Library Roadmap
> Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work archived in [HISTORY.md](HISTORY.md).

Goal: [[spec-driven-development]] — SPEC-v0 pilot on the `core/` agent library.
Reference implementation = `flows/research/deep.md` (the validator's oracle; never "fixed").

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

- [x] **Design symmetry across the skill/flow surface — naming grammar decided (2026-07-23).**
      Decision: a flow **owned by a dispatcher skill** lives in `core/flows/<skill>/` and its
      **filename equals the command tail** (`research <verb>` ⟺ `flows/research/<verb>.md`); flows
      not owned by any dispatcher stay flat. The axis is *invocation independence*, not composition
      (`scout` composes `deep`/`lit` yet stays a sub-flow). Rule written into [SCHEMA.md](SCHEMA.md)
      (flow-layer Location rule). **Done:** the 12 research flows moved to `flows/research/`, the two
      stutterers renamed `deepresearch`→`deep` and `autoresearch`→`auto`, `sync-skills validate_flows`
      made recursive, `research.md`/`loop-router.md`/`LOOP-TREE.md`/`SCHEMA.md` repathed, back-compat
      aliases kept in the dispatcher. **Deferred (own item below):** `flows/loops/` — same treatment
      for the `loop-*` cluster, held because its refs reach ~14 `brain/` files (goals + GOALS.md);
      do it from a session already in those files, per the parallel-session partition rule.

- [ ] **Finish the pool reorg: `flows/loops/`.** Move the `loop-*` cluster (loop-engineering,
      loop-architecture, loop-router) + `LOOP-TREE.md` into `core/flows/loops/` so the pool is fully
      foldered-by-owner (no half-foldered asymmetry). Blast radius is cross-domain (~14 `brain/`
      files reference `loop-engineering` by path) — schedule it when a session is already editing
      those goal files; do not churn `brain/` from a `core/`-only session.

## Notes

- `.claude/` + `.opencode/` are generated mirrors (tracked). Never hand-edit; run `sync-skills`.
- `sync-skills` prunes orphans on every `sync` now — renaming/removing a skill no longer dangles.
