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

**🟡 the meter shows two thresholds; the ask is the trend between them**
*What* — context growth visible continuously, most likely a statusline.
*Why* — Lucas cannot watch the window fill and only learns at a crossing.
*Done when* — he reads growth without asking and the hook still costs zero tokens until a crossing.

**🟡 anything the agent needs Lucas to physically do is said where he never sees it**
*What* — one channel reaching him at the *end* of a response, and when a session parks, which
`core/tools/wos/session/trace` can now name: a gap past its declared idle threshold.
*Why* — close offers and auth-consent requests land in agent-facing writing at prompt-submit time, and
a session blocked on an `AskUserQuestion` while he is elsewhere is the same defect's third instance.
A harness that auto-compacted a session and said so only at the end is the fourth (INBOX 2026-09-14),
and an expired Instagram cookie that cost a triage 8 of 26 entries is the fifth — both are things
only Lucas can act on, and neither reached him.
*Done when* — all five reach him without interrupting the thread, with measured token cost.

**🟡 thinking is 65% of billed output and no instrument here can see it**
*What* — a number for what thinking effort costs and whether lowering it breaks the work.
*Why* — it is the largest slice of billed output; every composition figure describes the other 35%.
*Done when* — one task has run at two effort levels with billed output *and* correctness compared.

## Measurement — does any of this earn its keep

**🟡 the scoreboard is running and owes its first reading**
*What* — the two-week reading, and the cuts it justifies. The instrument runs and the clock is
running with it: `core/run tools/wos/features --scoreboard`, into
`core/experiments/hook-scoreboard.md`. **The store's first row is 2026-09-14, so the reading is due
2026-09-28** — checked 2026-09-15 and it is not yet time; the tool prints the start date itself.
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
- **A goal↔roadmap warning, and a goal-format audit** — 2026-09-15: 26 of 39 goal files have never been opened.
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
