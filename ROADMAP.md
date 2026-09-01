# Workspace roadmap

> Everything still open in the workspace scaffold, in one file. **Cap: 200 lines.** A finished item
> is deleted — git is the history. A killed one gets a line under § Rejected so it cannot come back looking new.
>
> **Three fields per item, no fourth.** *What* will exist · *Why* it is worth building · *Done when*,
> the observable that ends it. **HOW is the job of the session that takes the item** — a roadmap
> carrying its own implementation goes stale the day the code disagrees with it. Rules live in the
> `SPECS.md` that owns them; numbers live in `core/experiments/` and `ISSUES.md`. Re-run an instrument.
>
> 🔴 Lucas decides · 🟡 an agent can rule alone · 🟢 mechanical. Items are named, never numbered: a
> number points at nothing the day the item lands. All four v1 criteria were met by 2026-08-16.

## Shape — does the tree still look like what we say it does

**🟢 the scaffold is still most of a lean workspace away from lean**
*What* — root + `core/` + `brain/` at **≤170 `.md` files and ≤10,000 lines**, read from
`core/run tools/wos/size --scope scaffold`. `core/experiments/` keeps conclusions only; `ISSUES.md`'s
hand-written half fits a screen; each top-level skill reaches ~45 lines; `brain/` sheds attachments and
project-state memories. `core/flows/` and `core/agents/` are **not cut** (out of scope) but still count.
*Why* — the norm that produced this mass now says cut. A `.md` line in this tree is re-read by every session.
*Done when* — both numbers are met with `verify-fast` green. Check code parsers before cutting any `.md`.

**🟢 four law files sit over the 200-line cap and each needs its own sitting**
*What* — `SETUP.md`, `core/hooks/SPECS.md`, `core/SPECS.md`, `core/SCHEMA.md` under the cap, cut not split.
*Why* — they are the largest scaffold files and the cut pays twice, closing size findings and the item above.
*Done when* — § Size signals lists none of them. **Not narration — every line is live law.** `SCHEMA.md`'s
tables are parsed by `schema_law.py` and its transient-doc rows are live exemptions; `SETUP.md` answers to
`test_setup_executable.py`. Cut prose around them, never a row, and read the parser before the file.

**🔴 the cap and the rationale rule point opposite ways, and the four law files are where they meet**
*What* — a ruling: shard each by reader, exempt the type, or send rationale to git. `core/norms/CONTEXT.md`
says rationale belongs in the `SPECS.md` that owns the rule; the cap says cut. Both cannot hold at 361 lines.
*Why* — measured 2026-09-01, not guessed: `SCHEMA.md` gave up 6 lines of true redundancy and stopped at 220
with every remaining line a parsed table or a rule with a checker; `core/hooks/SPECS.md` reads the same at 361,
where reaching 200 means deleting the coverage, shim and lifecycle tables. A sibling needs Lucas's explicit OK.
*Done when* — Lucas has ruled and the 🟢 item above is either doable or dead.

## Cost — what a session costs, and which of it is avoidable

**🟢 cheaper models where the work is mechanical**
*What* — mechanical work routed off the most expensive tier.
*Why* — the measured split is opus-heavy and some of that is typing, not thinking.
*Done when* — the split moves and work still lands. Context size is a 4.2x multiplier routing cannot beat.

**🟡 what our own tools print has never been measured, and it is read by an agent**
*What* — a number for what the tools' output costs per session, then the cuts it justifies.
*Why* — output enters the context whether read or not; `core/hooks/compact/` exists as a threshold question.
*Done when* — the ten loudest tools are ranked by bytes returned and each one's floor is a decision.

**🟡 the meter shows two thresholds; the ask is the trend between them**
*What* — context growth visible continuously, most likely a statusline.
*Why* — Lucas cannot watch the window fill and only learns at a crossing.
*Done when* — he reads growth without asking and the hook still costs zero tokens until a crossing.

**🟡 anything the agent needs Lucas to physically do is said where he never sees it**
*What* — one channel reaching him at the *end* of a response.
*Why* — close offer and auth-consent requests land in agent-facing prose at prompt-submit time.
*Done when* — both reach him without interrupting the thread, with measured token cost.

**🟡 thinking is 65% of billed output and no instrument here can see it**
*What* — a number for what thinking effort costs and whether lowering it breaks the work.
*Why* — it is the largest slice of billed output; every composition figure describes the other 35%.
*Done when* — one task has run at two effort levels with billed output *and* correctness compared.

## Measurement — does any of this earn its keep

**🟡 no hook has ever been measured, so no hook can be cut on evidence**
*What* — a count per feature of how often it fired and how often it blocked something real.
*Why* — 71 features are on and none has a scoreboard, so every cut is a guess and kept rules paid on faith.
*Done when* — after two weeks of ordinary use a feature × fired × blocked table exists.

**🟡 the ablation — the scaffold has never been measured against its own absence**
*What* — variants of the public scaffold, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
*Done when* — a **per-feature** verdict is readable. Runs outside this workspace (`academy/papers/wos-ablation/`).

**🔴 the agent is confidently wrong and nothing catches it**
*What* — define knowledge store criteria, and a mechanism grounding decisions before they harden.
*Why* — a plan agreeing with its own premise is the costliest failure mode; a third store is forbidden scatter.
*Done when* — research has run and Lucas has ruled in a dedicated session. Enforced, not prompt-induced.

## Legibility — can Lucas still read what he owns

**🔴 the legibility sitting: the jargon audit and the one-root test**
*What* — plain-word replacement per surviving term; verdict on legibility/self-description/confident-wrongness.
*Why* — previous sweeps were downstream attempts at an unnamed legibility problem.
*Done when* — survivors defined in `core/SCHEMA.md` and rest replaced. Precise word wins, simpler breaks ties.

**🟡 the health picture: keep what Lucas reads at a glance, cut the rest**
*What* — one page answering *is this well tied, and what is missing* — not an inventory.
*Why* — three drawings answered *what is there*; he needs a glanceable health picture.
*Done when* — he reads it at a glance and failing shapes are deleted.

## Portability — would this work on a machine that is not Lucas's

**🟡 ten tools are over the line-count warn threshold, newly visible**
*What* — `gdocs` 183, `permissions` 170, `video_core.py` 169, `session/context` 169, `notion` 153.
*Why* — they were invisible before shebang stripping. None exceeds the 200 cap; backlog, not block.
*Done when* — warn list is empty or rows are deliberately exempted with reasons.

**🔴 the platform seam owes three answers, and one of them is a secret**
*What* — `secure_dir()` / `secure_file()`; dep ceilings in `core/tools/deps.txt`; manager names for 4 `apt` rows.
*Why* — secret convention needs ACL equivalence; dep probes must verify function, not bare import.
*Done when* — seam writes secrets tight on all systems and no probe falsely greens.

**🟢 absorb `code/aiwbot` into this repo**
*What* — aiwbot versioned here, its standalone repo deleted, `telegram-capture` wired.
*Why* — it is part of WOS and the last feature that cannot be switched off.
*Done when* — `core/tools/wos/features --findings` reads zero.

**🟡 the public scaffold repo his students clone**
*What* — public repo checked out at `code/wos/`, one-way sync, allowlist-driven, shipping research subset.
*Why* — students asked for it; hard precondition for ablation study.
*Done when* — a student clones it and gets a working workspace.

## Brain — the part that serves Lucas rather than the code

**🟡 measure which `UPPERCASE.md` files are read, then decide what to do about goal files**
*What* — per-type rollup of reads and cost; then goal↔roadmap warning and goal-format audit.
*Why* — verify whether goal files are dead weight before redesigning fields.
*Done when* — numbers are in `core/experiments/` and downstream steps decide based on data.

## Deferred — real work, deliberately not now

- **`core/flows/` and `core/agents/`** (Lucas, 2026-08-25) — wait until v1 scaffold is tight.
- **Anything a nested repo owns** — each keeps its own `ISSUES.md` and fixes its own findings.
- **`[gdrive-integration]`, `[offline-resilience]`, serious OCR** — content/infrastructure, not scaffold.

## Rejected

- **Adopting `obra/Superpowers` over our craft flow** — no per-task tier routing; trigger imported instead.
- **Curing confident wrongness with a prompt rule** — induced loses to enforced; corpus is evidence.
- **A preliminary cut of features before the ablation** — declined 2026-08-21: cutting on hunches is a guess.
- **An ensemble router** — spend driven by context size; multiple models over large context multiply cost.
- **A global terseness rule, and `effort` as a *length* lever** — wrong budget degrades accuracy.
- **A second compaction shim for copilot** — no copilot session has ever run here.
- **Raising `BLOCK_LINES` to 300** — moves the queue; files needing room need a seam, not higher ceilings.
- **`core/` and `brain/` getting their own `ISSUES.md`** — both are WOS; neither holds hand-written bugs.
- **A check that only asks whether a `TYPE-<slug>.md` is tracked** — built, then dropped 2026-09-01: it
  finds nothing, and the defect it was aimed at is any routing row naming a file git does not carry.
- **Deleting a dated `*-backup-*.md` beside a tracked type as a corpse** — `academy/lab/CONTEXT.md`
  declares those snapshots captured, not authored; the untracked *law* next to them was the real bug.
