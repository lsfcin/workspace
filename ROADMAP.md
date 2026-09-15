# Workspace roadmap

> Everything still open in the workspace repo, in one file. A finished item is deleted; a killed
> one gets **one line** under § Rejected so it cannot come back looking new.
>
> **Three fields per item, no fourth.** *What* will exist · *Why* it is worth building · *Done when*,
> the observable that ends it. **HOW is the job of the session that takes the item** — a roadmap
> carrying its own implementation goes stale the day the code disagrees with it. Rules live in the
> `SPECS.md` that owns them; numbers live in `core/experiments/` and `ISSUES.md`. Re-run an instrument.
>
> 🔴 Lucas decides · 🟡 an agent can rule alone · 🟢 mechanical. Items are named, never numbered.

## Cost — what a session costs, and which of it is avoidable

**🔴 cheaper models where the work is mechanical, and the map of which case gets which**
*What* — a written mapping from KIND OF WORK to level, and a way to apply it that survives the
harness changing. Re-graded from 🟢 on 2026-09-14: the one-line fix — a default subagent model in
`.claude/settings.json` — was refused as too narrow. *"quero fazer isso decentemente, e não só pro
claude code … quais casos usar qual e como fazer isso de forma segura e precisa"* (Lucas).
*Why* — the split is 99.4% opus over 94 sessions and $2,002, and some of that is typing. The only
live routing is inside `/craft`, whose executors declare haiku/sonnet/opus by level; every other
subagent inherits the parent, so a read-only search runs at the dearest level.
*Done when* — the split moves, the work still lands, and the mapping reaches every harness rather
than one settings file. Context size is a 4.2x multiplier routing cannot beat.

**🟡 the close cannot say which models and agents a session actually spent**
*What* — what the close's report should carry, ruled, then built. *"quantos subagentes foram
spawnados … os custos de cada"* (Lucas, 2026-09-14). Today it prints `session/usage --session` plus
`size`, and says nothing about subagents; `core/experiments/delegation.md` asks the spawn-rate half
and no tool answers the cost half. Nothing needs new instrumenting — `subagent_type`, the spawn
prompt, each worker's own `usage` and every record's `timestamp` are already on disk.
Four candidates, and the ruling is which of them the report carries (Lucas defers to a later
session, 2026-09-14): one line per spawn (type, model, cost, turns, task); the main-thread against
subagent split, which is the number that says whether delegating pays; wall-clock working against
waiting; and the ten loudest tools by bytes returned. The report is a last response and not carried
into the handoff, so its length is not paid by later sessions — that is not an argument against any
of the four.
*Why* — the item above is a routing decision that cannot be made, or checked afterwards, without it.
The third candidate is the § Cost wall-clock instrument, which the channel item waits on, so three
roadmap items meet here and share one `timestamp` read.
*Done when* — the ruling is written, a close prints what it chose, and the numbers reconcile with
`session/usage`.

**🟡 what our own tools print has never been measured, and it is read by an agent**
*What* — a number for what the tools' output costs per session, then the cuts it justifies.
*Why* — output enters the context whether read or not; `core/hooks/compact/` exists as a threshold question.
*Done when* — the ten loudest tools are ranked by bytes returned and each one's floor is a decision.

**🟡 the meter shows two thresholds; the ask is the trend between them**
*What* — context growth visible continuously, most likely a statusline.
*Why* — Lucas cannot watch the window fill and only learns at a crossing.
*Done when* — he reads growth without asking and the hook still costs zero tokens until a crossing.

**🟡 anything the agent needs Lucas to physically do is said where he never sees it**
*What* — one channel reaching him at the *end* of a response, and at the moment a session parks.
*Why* — close offers and auth-consent requests land in agent-facing writing at prompt-submit time, and
a session blocked on an `AskUserQuestion` while he is elsewhere is the same defect's third instance.
A harness that auto-compacted a session and said so only at the end is the fourth (INBOX 2026-09-14),
and an expired Instagram cookie that cost a triage 8 of 26 entries is the fifth — both are things
only Lucas can act on, and neither reached him.
*Done when* — all five reach him without interrupting the thread, with measured token cost.

**🟡 a session's wall-clock has never been split into working and waiting**
*What* — a fourth `core/tools/wos/session/` instrument: how much of a span the machine was busy and
what the idle gaps were parked on, plus the `core/experiments/` file that makes it a trend.
*Why* — the three tools there measure what a session *costs*, none how long it *took*, so "ran ten
hours" has never been separable from "Lucas was away for eight". The item above waits on this.
*Done when* — the instrument runs from a transcript and `core/experiments/` carries its first rows.

**🟡 thinking is 65% of billed output and no instrument here can see it**
*What* — a number for what thinking effort costs and whether lowering it breaks the work.
*Why* — it is the largest slice of billed output; every composition figure describes the other 35%.
*Done when* — one task has run at two effort levels with billed output *and* correctness compared.

## Measurement — does any of this earn its keep

**🟡 the scoreboard is running and owes its first reading**
*What* — the two-week reading, and the cuts it justifies. The instrument runs and the clock is
running with it: `core/run tools/wos/features --scoreboard`, into
`core/experiments/hook-scoreboard.md`.
*Why* — 82 features are on, so every cut is a guess and kept rules are paid on faith.
*Done when* — the table is read after two weeks of ordinary use and each silent feature is a decision.

**🟡 the ablation — the repo has never been measured against its own absence**
*What* — variants of the public repo, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
*Done when* — a **per-feature** verdict is readable. Runs outside this workspace (`academy/papers/wos-ablation/`).

## Legibility — can Lucas still read what he owns

**🟡 the health picture: keep what Lucas reads at a glance, cut the rest**
*What* — one page answering *is this well tied, and what is missing* — not an inventory.
*Why* — three drawings answered *what is there*; he needs a glanceable health picture.
*Done when* — he reads it at a glance and failing shapes are deleted.

## Portability — would this work on a machine that is not Lucas's

**🟡 the port grew the workspace and the payment is still short**
*What* — the cut that funds the port, taken from the top of `core/run tools/wos/session/reads` down.
This line used to say no named candidate was left; the instrument names one, and it is **this file**.
So draining the roadmap and paying the debt are one job. The ranking and what it costs:
`core/experiments/read-amplification.md`.
*Why* — `core/norms/reduce.md`: a session leaves fewer lines than it found. The port was worth every
line; that is a reason to pay, not a reason not to.
*Done when* — the net since 2026-09-01 is negative under `core/run tools/wos/size --scope repo`.
Several sessions of cutting rather than one; re-run it rather than quoting a figure from here.
The debt is this repo's: absorbing a project's own writing neither creates nor pays it.

**🔴 the platform boundary's last answer needs a Windows machine, and there is none**
*What* — manager names for the 3 `apt` rows (`poppler-utils`, `tesseract-ocr`, `ddgr`). The file's
own head only lets a row claim `system` once the name is VERIFIED on the other managers.
*Why* — a row claiming a portability nobody checked is the false green these checks exist to end.
*Done when* — each of the three is `system` with a verified name, or stays `apt` with the reason.
*Blocked* — Lucas has no Windows access, for an unknown stretch (2026-09-14). Nothing else unblocks it.
The other two answers are in: `is_owner_only()` reads the ACL back rather than trusting `st_mode`,
and `core/tools/deps.txt` now carries a `floor` column — a floor, not the ceiling this line asked
for, because the failure is a distro shipping something too old, never a release from the future.

**🟡 the public repo his students clone**
*What* — public repo checked out at `code/wos/`, one-way sync, allowlist-driven, shipping research subset.
*Why* — students asked for it; hard precondition for ablation study.
*Done when* — a student clones it and gets a working workspace.

## Brain — the part that serves Lucas rather than the code

**🟡 measure which `UPPERCASE.md` files are read, then decide what to do about goal files**
*What* — per-type summary of reads and cost; then goal↔roadmap warning and goal-format audit.
*Why* — verify whether goal files are dead weight before redesigning fields.
*Done when* — numbers are in `core/experiments/` and downstream steps decide based on data.

## Deferred — real work, deliberately not now

- **`core/flows/` and `core/agents/`** (Lucas, 2026-08-25) — wait until v1 repo is tight.
- **Anything a nested repo owns** — each keeps its own `ISSUES.md` and fixes its own findings.
- **`[gdrive-integration]`, `[offline-resilience]`, serious OCR** — content/infrastructure, not repo.

## Rejected

- **Tokens as the size unit** — 2026-09-14: 216 ms of vocabulary against a 273 ms write, and no Anthropic tokenizer offline.
- **Measuring one line's width** — 2026-09-14 (Lucas): four exemptions, because it asked about syntax, not size.
- **Exempting Lucas's own writing from the rename check** — 2026-09-14 (Lucas): a blind spot is worse than a word.
- **The one-root hypothesis** — 2026-09-14: two of three; words die when structure moves and text does not follow.
- **`gate` → `block`** — 2026-09-14: `block` already names a generated region AND is the verb: *"a block blocks"*.
- **Flattening the eight personification verbs** — 2026-09-14 (Lucas): 478 uses and they read; a voice is not jargon.
- **Excluding `code/aiwbot` from the entropy scan** — 2026-09-12: a tree our checks skip is an invisible asymmetry.
- **A repo target of ≤170 `.md` files** — 2026-09-11 (Lucas): "não tem base real." Read cost picks the cut.
- **Regenerating the entropy block on receipt** — 2026-09-04: a full tree scan before the first prompt; tree dirty.
- **Adopting `obra/Superpowers` over our craft flow** — no per-task level routing; trigger imported instead.
- **Curing confident wrongness inside this repo** — 2026-09-13 (Lucas): only a parser or solver refuses; research.
- **A research map here, and one review yaml per kept source** — 2026-09-13: a `REFS-<name>.md` does both.
- **A preliminary cut of features before the ablation** — 2026-08-21: cutting on hunches is a guess.
- **An ensemble router** — spend driven by context size; multiple models over large context multiply cost.
- **A global terseness rule, and `effort` as a *length* lever** — wrong budget degrades accuracy.
- **A second compaction shim for copilot** — no copilot session has ever run here.
- **Raising the line block by half** — moves the queue. **Partly reversed 2026-09-06 (Lucas)** for law files.
- **`core/` and `brain/` getting their own `ISSUES.md`** — both are WOS; neither holds hand-written bugs.
- **Narrowing the pre-commit to the touched tests** — 2026-09-01: parallelising paid four-fold without weakening it.
- **A check asking only whether a `TYPE-<name>.md` is tracked** — 2026-09-01: any row naming an untracked file is.
- **Paying the cap by deleting SETUP steps** — 2026-09-02: every step is a feature a stranger's clone cannot install.
- **Deleting a dated `*-backup-*.md` as a dead item** — `academy/lab/` declares those captured, not authored.
