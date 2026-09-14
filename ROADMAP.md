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

## Shape — does the tree still look like what we say it does

**🟡 four numeric laws have no home, and `core/hooks/limits.env` is not theirs**
*What* — one home per number, or a written reason why a local one is right. The citation gate
covers the line/file/column law and deliberately stops there; the craft loop file's soft size, a
research output's length and a commit subject's width are each declared in the writing that uses them.
*Why* — the same copy-paste that made eight files name a stale warn, one layer out.
*Done when* — each of the four is either parsed from one file or carries its reason where it sits.

## Cost — what a session costs, and which of it is avoidable

**🟢 cheaper models where the work is mechanical**
*What* — mechanical work routed off the most expensive level.
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
*What* — one channel reaching him at the *end* of a response, and at the moment a session parks.
*Why* — close offers and auth-consent requests land in agent-facing writing at prompt-submit time, and
a session blocked on an `AskUserQuestion` while he is elsewhere is the same defect's third instance.
*Done when* — all three reach him without interrupting the thread, with measured token cost.

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

**🟡 no hook has ever been measured, so no hook can be cut on evidence**
*What* — a count per feature of how often it fired and how often it blocked something real.
*Why* — 71 features are on and none has a scoreboard, so every cut is a guess and kept rules paid on faith.
*Done when* — after two weeks of ordinary use a feature × fired × blocked table exists.

**🟡 the ablation — the repo has never been measured against its own absence**
*What* — variants of the public repo, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
*Done when* — a **per-feature** verdict is readable. Runs outside this workspace (`academy/papers/wos-ablation/`).

## Legibility — can Lucas still read what he owns

**🟢 the audit's words also name code, and the rename is unfinished until identifiers follow**
*What* — `slug` out of identifiers, then its row in § Retired tokens. Five of seven are done. The
sixth, `probe`, is renamed everywhere and owes only its row: `brain/goals/google-migration.md` names
a Drive deck `__probe_delete_me` that no rename of ours can reach, so the row lands the moment
Lucas deletes that deck — which is what the line beside it already asks him to do.
*Why* — the check matches filenames, so a row added while a module still carries the word reds the
suite on our own code. Never sweep a bracketed short name, or a word carrying a second sense
elsewhere in the tree — each costs a revert, and one word had three senses in one tree.
*Done when* — the entropy scan finds zero survivors of every row.

**🟡 the health picture: keep what Lucas reads at a glance, cut the rest**
*What* — one page answering *is this well tied, and what is missing* — not an inventory.
*Why* — three drawings answered *what is there*; he needs a glanceable health picture.
*Done when* — he reads it at a glance and failing shapes are deleted.

## Portability — would this work on a machine that is not Lucas's

**🟡 the port grew the workspace and the payment is still short**
*What* — the cut that funds the port. Every named candidate has been tried; the rest was paid by
raising the cap, which moves the line and not the mass.
*Why* — `core/norms/reduce.md`: a session leaves fewer lines than it found. The port was worth every
line; that is a reason to pay, not a reason not to.
*Done when* — the net since 2026-09-01 is negative under `core/run tools/wos/size --scope repo`.
The debt is this repo's: absorbing a project's own writing neither creates nor pays it.

**🔴 the platform boundary owes three answers, and one of them is a secret**
*What* — `secure_dir()` / `secure_file()`; dep ceilings in `core/tools/deps.txt`; manager names for 4 `apt` rows.
*Why* — secret convention needs ACL equivalence; dep checks must verify function, not bare import.
*Done when* — boundary writes secrets tight on all systems and no check falsely greens.

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

- **Exempting Lucas's own writing from the retired-token check** — 2026-09-14 (Lucas): a sentence where a retired
  spelling means something the rename does not cover gets rewritten. A blind spot is worse than a word.
- **The one-root hypothesis** — 2026-09-14: two of three. Dead words die when structure moves and text does not follow,
  which is self-description; the third left and is `back2dsl`.
- **`gate` → `block`** — 2026-09-14: `block` already names a generated region AND is the gate's verb, so the swap reads
  *"a block blocks"*.
- **Flattening the eight personification verbs** — 2026-09-14 (Lucas): 478 uses, and they read. A consistent voice is
  not jargon.
- **Excluding `code/aiwbot` from the entropy scan** — 2026-09-12: a tree our own checks skip is an invisible asymmetry;
  it cost four findings.
- **A repo target of ≤170 `.md` files** — 2026-09-11 (Lucas): "não tem base real." `core/norms/reduce.md` governs; read
  cost picks the cut.
- **Regenerating the entropy block on receipt** — 2026-09-04: a full tree scan before the first prompt, and a tree dirty
  at session open.
- **Adopting `obra/Superpowers` over our craft flow** — no per-task level routing; trigger imported instead.
- **Curing confident wrongness inside this repo** — 2026-09-13 (Lucas): prompt, judge and self-report died on evidence;
  only a parser or solver refuses, so it is research — `academy/papers/back2dsl`.
- **A research map as a plan block here, and one review yaml per kept source** — 2026-09-13: the first grows our most
  re-read file; the second breaches the `core/refs/` crowding block. A `REFS-<slug>.md` does both.
- **A preliminary cut of features before the ablation** — 2026-08-21: cutting on hunches is a guess.
- **An ensemble router** — spend driven by context size; multiple models over large context multiply cost.
- **A global terseness rule, and `effort` as a *length* lever** — wrong budget degrades accuracy.
- **A second compaction shim for copilot** — no copilot session has ever run here.
- **Raising the line block by half** — moves the queue; a file needing room needs a boundary. **Partly reversed
  2026-09-06 (Lucas)** for law files; over the cap a file is still CUT, not split.
- **`core/` and `brain/` getting their own `ISSUES.md`** — both are WOS; neither holds hand-written bugs.
- **Narrowing the pre-commit to the touched tests** — 2026-09-01: the only speed-up that weakens the gate holding both
  clones, and parallelising paid four-fold without it.
- **A check asking only whether a `TYPE-<slug>.md` is tracked** — 2026-09-01: the real defect is any routing row naming
  a file git does not carry.
- **Paying the cap by deleting SETUP steps** — 2026-09-02: every step is a feature a stranger's clone cannot install,
  and strangers are who the file is for.
- **Deleting a dated `*-backup-*.md` as a dead item** — `academy/lab/CONTEXT.md` declares those captured, not authored;
  the untracked *law* beside them was the bug.
