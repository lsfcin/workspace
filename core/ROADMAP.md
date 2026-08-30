# Core Library Roadmap

> What is still unsound about the agent library itself — skills, agents, flows, tools and their
> schema. Workspace scaffold work is the wos ledger's, [/ROADMAP.md](../ROADMAP.md); an item belongs
> to exactly one of the two. **Cap: 200 lines.** Same three fields, same deletion policy, same
> refusal to write HOW: [/ROADMAP.md](../ROADMAP.md) states both once.

Contract: [SCHEMA.md](SCHEMA.md). Goal: [[spec-driven-development]].

## Open

**🟡 our own skills are too big, and nobody has checked whether the bulk earns anything**
*What* — every `core/skills/*.md` read for verbosity, redundancy, ambiguity, and steps costing more
than they save. *Why* — Lucas (2026-08-25): *"skills são úteis mas me parecem meio gigantes quase
sempre."* A skill is read in full at invocation, so its length is paid every time it fires.
*Done when* — no skill is longer than the work it describes, and each one still does its job.

**🟡 every skill is invisible to a session started outside the workspace**
*What* — skills reachable from a terminal opened anywhere, or a loud failure saying they are not.
*Why* — `.claude/commands/` is project-scoped, so a session whose project is `$HOME` loads none of
the fourteen and silently has no `/roundup`. Reproduced 2026-08-18. *Done when* — Lucas gets the
skill or an explicit refusal, never silence. Linking them globally means a workspace skill can fire
in a repo it knows nothing about; that trade is the decision, not the wiring.

**🟢 `parse_owns` reads prose as declared paths, and says so on every commit**
*What* — the `>**owns**` block ending where it actually ends. *Why* — it currently runs to the next
field or heading, so ordinary blockquote prose becomes candidate paths and every commit prints
`⚠ <goal>: owns '<prose>' ... resolves to no repo` for at least three goals. The noise trains the
reader to skip post-commit output, which is where the gates also speak. *Done when* — the warnings
are gone and a goal file with prose after its block is in the brain tests.

**🟢 `/caveman compress` carries two bugs that outlived the rejection of its main use**
*What* — the trailing newline it strips, and the stale model id it defaults to.
*Why* — compressing workspace docs was measured and rejected, but the tool still runs on demand.
*Done when* — a compressed file keeps its final newline and the default model id resolves.

**🟡 `/roundup` ends by asking for something it could have proposed inside the plan**
*What* — one fewer round-trip per session. *Why* — Lucas suggested it and flagged it himself:
*"é só uma ideia, avaliar antes de implantar."* *Done when* — evaluated against AGENTS.md § one
action: a closing message naming the next session's close names a second action, so the honest
version may belong in the plan template rather than in roundup's last line.

**🟢 a `gslides frames` command — the capability question is already answered**
*What* — one command taking an element, start and end positions, a frame count and an easing,
emitting the batch. *Why* — per-object tweens are not in the API, but `duplicateObject` plus
`updatePageElementTransform` in one `batchUpdate` authors a frame sequence, proven live 2026-08-14
and PDF-safe by construction. What is left is ergonomics, not discovery. *Done when* — the command
exists and the two known traps are handled; both are in [`tools/slides/SPECS.md`](tools/slides/SPECS.md).

**🟡 Notion reads are built and blocked on one click; writing is unstarted**
*What* — `[notion-read]` closed, then append/update blocks. *Why* — the CLI answers against the live
API and the secret is minted, but an integration sees nothing until a page is connected to it, so
nothing can be smoke-tested against real content. *Done when* — Lucas connects `WOS` to the class
page (⋯ → Connections), `list` returns content, and the write path takes Notion's own request format
rather than a DSL. Intent and ordering live in
[`brain/goals/teaching-materials.md`](../brain/goals/teaching-materials.md); this line owns the build.

**🟢 nothing we build on Drive can be thrown away by the thing that built it**
*What* — a `trash` command on `gdocs` and `gdrive`. *Why* — both write (`new`, `push`, `mkdir`,
`put`) and neither deletes, so every probe an agent creates is cleanup Lucas does by hand; two are
waiting on him now. *Done when* — a file created by the CLI can be trashed by it, on the write token.

## Blocked — waiting on a trigger

**🟢 the `video/` family name describes less than the family delivers** — it gained a page fallback,
so it offers *link → navigable text* while the directory says one medium.
→ **trigger: the next time something else opens `core/tools/` for a path change.** Two sweeps have
already happened and [`tools/SPECS.md`](tools/SPECS.md) § Naming says a third is not free, so pay it
alongside another reason rather than on its own.

## Deferred — flows and agents, findings kept, nothing spent

Lucas, 2026-08-25: the layer waits until the v1 scaffold is tight. These were found by *running* the
flow on 2026-08-24, so they are evidence rather than review notes and are kept at one line each.
None is worked until the layer reopens.

- **A craft executor reverted an uncommitted orchestrator edit it did not write.** Loop 6 had been
  handed the dirty-tree fence and discarded the file anyway; nothing was lost only because the
  orchestrator still held the text. The fence is prose in a spawn prompt, which names no consequence.
- **The router has no `experiment` subtree**, so a controlled measurement fell back to the padaria
  gate, which measures the write rather than the investigation.
- **Padaria mandates a `feature/<slug>` branch off develop** while the same flow's Field Practice
  names "two loops, one repo" as a known hazard.
- **The flow reads 18 KB of routing and runtimes before the gate that decides it needs them.**
- **Only Loop 1 declares a cap**, and the whole-file check reads it as covering the flow — including
  Loop 4b, which is called *Code Until Green*.
- **`engineering` is exempted by path rather than typed**, so the cluster doing the most work is the
  one not schema-checked.
- **The three `craft-*` agent mirrors are hand-written twice with no source in `core/`**, which is
  the last provider-name-in-source violation and the hand-sync hazard `SCHEMA-layers.md` documents.

## Rejected

- **Surveying outside skills for things to import** (asked 2026-07-23, dropped 2026-08-25) — the two
  leads are DM-bait posts naming skills without linking them, and the named capabilities overlap what
  `AGENTS.md` and CONTEXT.md already do. Reopen from a real repository, never from a reel.

## Notes

- `.claude/`, `.opencode/` and `.zcode/` are generated mirrors. Never hand-edit; run `sync-skills`,
  which prunes orphans and writes every link relative so a clone resolves it.
