# Workspace roadmap

> Everything still open in the workspace scaffold, in one file. **Cap: 200 lines.** A finished item
> is deleted — git is the history. A killed one gets a line under § Rejected so it cannot come back
> looking new.
>
> **Three fields per item, no fourth.** *What* will exist · *Why* it is worth building · *Done when*,
> the observable that ends it. **HOW is the job of the session that takes the item** — a roadmap
> carrying its own implementation goes stale the day the code disagrees with it. Rules live in the
> `SPECS.md` that owns them; numbers live in `core/experiments/` and `ISSUES.md`. Re-run an
> instrument, never quote it into this file.
>
> 🔴 Lucas decides · 🟡 an agent can rule alone · 🟢 mechanical. Items are named, never numbered: a
> number points at nothing the day the item lands. All four v1 criteria were met by 2026-08-16, so
> an item that cannot state its *why* belongs under § Rejected rather than in the list.

## Shape — does the tree still look like what we say it does

**🟢 the scaffold is still most of a lean workspace away from lean**
*What* — root + `core/` + `brain/` at **≤170 `.md` files and ≤10,000 lines**, from 273 and 17,074.
`core/refs`' six shards fold into `REFS.md` and `core/experiments/` keeps
conclusions only; `ISSUES.md`'s hand-written half fits a screen; each top-level skill reaches ~45
lines; `brain/` sheds 19 MB of bot attachments, its project-state memories and most of its 54 goal
files. `core/flows/` and `core/agents/` **wait** — out of scope, so the number to drive is 237 / 14,141.
Four families are done — `SCHEMA` five files → two, `SPECS` five → one, `core/hooks`' four → one,
`SETUP` six → one.
**A seam has to be a second parser, not a heavy section**: `SCHEMA-layers.md` survives because a
runtime parses it, and nothing parses a `SPECS` file, so all five merged. **A merged index lands over
the cap** — 223, 267, 331 — because what survives such a cut is rulings and tables. Same on `SETUP`.
*Why* — the norm that produced this mass now says cut, and nothing has been cut yet. A `.md` line in
this tree is re-read by every session that touches the subtree.
*Done when* — both numbers are met with `verify-fast` green. **Check before cutting any `.md`
whether code parses it**: `core/SCHEMA.md`, `core/norms/*.md` and `ROADMAP*.md` are data, not prose.

**🟢 the corpus is half Portuguese and the rule is English**
*What* — one language across the durable `.md` corpus, with Lucas's quoted words left as he said them.
*Why* — two languages in one document costs tokens and readers; he ruled English for docs.
*Done when* — no file mixes both outside a quote. Convert whole files, never half of one.

**🟡 the line cap and the column cap contradict each other, and `AGENTS.md` satisfies neither**
*What* — one rule for which cap wins, and an `AGENTS.md` not permanently in violation.
*Why* — wrapping to the column cap pushed a file past the line cap, so the two trade finding for
finding; and `test_norms` reads the rule block line by line, so a wrapped norm loses its continuation.
*Done when* — a file near both caps has one legal way out and `AGENTS.md` carries zero findings.

**🟢 a type's sibling files can be gitignored and nothing notices**
*What* — a Tier 0 check that a file passing `entropy_naming.TYPE_SLUG` is tracked.
*Why* — eight `core/SCHEMA-*.md` / `SPECS-*.md` sat untracked with three checks green, so a clone got
an index pointing at nothing. The allowlist was hand-patched and it happened again 2026-08-27:
`academy/lab/CONTEXT.md` links `CHECKPOINTS.md`, which `academy/lab/*` keeps out of git.
*Done when* — the check fails on an ignored sibling and passes on this tree.

**🟢 the `SPEC.md` → `SPECS.md` retyping**
*What* — the singular spelling gone from `code/_templates/module.SPEC.md` and the repos that copied it.
*Why* — one meaning with two spellings, leaked into five enforcement points.
*Done when* — one reviewed change lands template-first and `SPEC.md` earns its § Retired tokens row.

## Cost — what a session costs, and which of it is avoidable

**🟢 cheaper models where the work is mechanical**
*What* — mechanical work routed off the most expensive tier.
*Why* — the measured split is opus-heavy and some of that is typing, not thinking.
*Done when* — the split moves and the work still lands. Context size is a 4.2x multiplier that
routing cannot beat, so check the ceiling before spending on this.

**🟡 the meter shows two thresholds; the ask is the trend between them**
*What* — context growth visible continuously, most likely a statusline.
*Why* — Lucas cannot watch the window fill and only learns at a crossing.
*Done when* — he reads growth without asking and the hook still costs zero tokens until a crossing.

**🟡 anything the agent needs Lucas to physically do is said where he never sees it**
*What* — one channel reaching him at the *end* of a response.
*Why* — the close offer and every auth-consent request land in agent-facing prose at prompt-submit
time; a consent request once sat unclicked through four exchanges.
*Done when* — both reach him without interrupting the thread, and the channel's token cost was
measured before wiring rather than assumed free.

**🟡 thinking is 65% of billed output and no instrument here can see it**
*What* — a number for what thinking effort costs and whether lowering it breaks the work.
*Why* — it is the largest slice of billed output; every composition figure we hold describes the other 35%.
*Done when* — one task has run at two effort levels with billed output *and* correctness compared.
No behaviour change before the number exists: a wrong budget degrades the answer.

## Measurement — does any of this earn its keep

**🟡 no hook has ever been measured, so no hook can be cut on evidence**
*What* — a count per feature of how often it fired and how often it blocked something real.
*Why* — 71 features are on and none has a scoreboard, so every cut is a guess and every kept rule is
paid on faith. `core/hooks/hook_input.py` is the point they all pass through.
*Done when* — after two weeks of ordinary use a feature × fired × blocked table exists.
**Ruled 2026-08-25: nothing is deleted before it does.**

**🟡 the ablation — the scaffold has never been measured against its own absence**
*What* — variants of the public scaffold, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures and a stronger model may not need the
compensation; a rule that outlives its failure is pure cost.
*Done when* — a **per-feature** verdict is readable, not only an aggregate. Needs the public repo and
a clean per-feature switch. Runs outside this workspace; design belongs to `academy/papers/wos-ablation/`.

**🔴 the agent is confidently wrong and nothing catches it**
*What* — two halves Lucas postponed on purpose: what a knowledge store is and what earns a row in it,
and a mechanism that notices a decision is being taken and grounds both sides before it hardens.
*Why* — a plan built by agreeing with its own premise is the costliest version, because the whole
session sits on it; and a third store would be the scatter this workspace forbids.
*Done when* — research has run and Lucas has ruled, in a session about this and nothing else.
**Not with a prompt rule** — induced doubt is already thick here and prevented neither known failure.

## Legibility — can Lucas still read what he owns

**🔴 the legibility sitting: the jargon audit and the one-root test**
*What* — a plain-word replacement per surviving term, and a verdict on whether legibility,
self-description and confident-wrongness are one problem or three.
*Why* — the feature registry, the group rename and the vocabulary sweep were all downstream attempts
at a legibility problem nobody had named, which is why each only helped for a while.
*Done when* — survivors are defined in `core/SCHEMA.md` and the rest replaced across the
corpus. The most precise word wins, simpler breaks the tie, and the fix is subtraction.

**🟡 the health picture: keep what Lucas reads at a glance, cut the rest**
*What* — one page answering *is this well tied, and what is missing* — not an inventory.
*Why* — three drawings were built and none landed, because all three answered *what is there*.
*Done when* — he reads it at a glance and every shape that failed that test is deleted. The lifecycle
sequence passed and is what the others are judged against.

**🟡 a session must not decide things quietly**
*What* — the hand-off naming what this session decided *without asking*, plus a Context / Decision /
Consequences record for anything with lasting blast radius.
*Why* — *"decisions I didn't recall making"* is the complaint under this whole front, and git holds
what changed but never the option space that was rejected.
*Done when* — a decision that cannot be stated in one line is visibly one that was too big to take alone.

## Portability — would this work on a machine that is not Lucas's

**🟢 drive the two port ceilings to zero**
*What* — 45 versioned files still hardcode the authoring machine's workspace path, and 18 still name
the POSIX-only venv bin directory. The largest remaining cluster is `core/tools/deps.txt`, which
spells that directory once per row in its probe column and whose install hints are raw `apt`/`pip`
strings rather than `platform_law.package_install`.
*Note* — spelled in words here on purpose: the ratchet greps for the literal strings, so a ROADMAP
item naming them becomes one of its own findings.
*Why* — a probe that cannot run on a clone reports the dependency missing, which is the same false
answer the `make verify-fast` gate gave. The registry's own rule is that a dependency has **one**
name; a per-machine spelling per row breaks it.
*Done when* — `MACHINE_PATH_CEILING` and `VENV_POSIX_CEILING` in
`core/tools/test/workspace/test_port_ratchet.py` both read 0, and `core/run tools/wos/deps --check`
is meaningful on this machine.

**🟡 ten tools are over the line-count warn threshold, newly visible**
*What* — `gdocs` 183, `permissions` 170, `video_core.py` 169, `session/context` 169, `notion` 153
and five more now warn at commit.
*Why* — they were invisible to `is_code_file` for as long as it recognised code by shebang, and the
shebang strip is what surfaced them. None is over the 200 cap; this is a backlog, not a block.
*Done when* — the warn list is empty, or a row is deliberately exempted with a reason.

**🟢 absorb `code/aiwbot` into this repo**
*What* — aiwbot versioned here, its standalone repo deleted, `telegram-capture` wired.
*Why* — it is part of WOS and deeply entangled, and it is the last feature that cannot be switched
off: any wiring available today makes this repo's Tier 0 test assert on a nested repo's content.
*Done when* — `core/tools/wos/features --findings` reads zero. **Ruled 2026-08-24: absorb.** A build,
not a decision.

**🟡 `.gitignore` says both things about a nested repo's `CONTEXT.md`**
*What* — one answer on whether those four files are tracked.
*Why* — an earlier block re-allows them, a later wholesale entry wins, so none is tracked and the
first block is inert while reading as if it works — which is how the fifth repo will copy it.
*Done when* — the contradiction is gone. Reordering changes what the Tier 0 corpus holds, so decide.

**🟡 the public scaffold repo his students clone**
*What* — a separate public repo checked out at `code/wos/`, one-way sync, allowlist-driven, shipping
the research-and-paper-writing subset with `brain/` as empty structure.
*Why* — students have asked for it, and it is a hard precondition of the ablation.
*Done when* — a student clones it and gets a working workspace, and the general/Lucas line is a
reviewable diff rather than a trusted script.

## Brain — the part that serves Lucas rather than the code

**🟡 the attention dashboard counts edits to goal files, not work on goals**
*What* — a counter over commits touching each goal's declared paths, in whichever repo owns them.
*Why* — `workspace-os` rendered as one touch in a fortnight when 29 of 29 commits were its work, so
any goal whose work lands in `code/` reads as dead and `/compass` is hand-corrected every cycle.
*Done when* — a bar reflects work done, the instrument ignores its own reviews, and area bars union
rather than sum. Started 2026-08-14 and unfinished; `brain_dashboard.py` shrinks, never grows.

**🟡 measure which `UPPERCASE.md` files are read, then decide what to do about goal files**
*What* — a per-type rollup of reads and read cost over time; then, and only then, the goal↔roadmap
warning and the goal-format audit.
*Why* — Lucas suspects goal files are dead weight and roadmaps are heavily read. If that is true,
redesigning goal fields and strengthening links to them are both the wrong move — so the ordering is
the item, not a caveat.
*Done when* — the numbers are in `core/experiments/`, and each downstream half is built or dropped on
what they say. If the warning is built: warn, never block, or it trains empty goal updates.

## Deferred — real work, deliberately not now

- **`core/flows/` and `core/agents/`** (Lucas, 2026-08-25) — they wait until the v1 scaffold is tight.
  Nothing is spent on them, including the trial that would judge them: flows ran twice, agents remain
  wholly untried, so no ruling on that layer is available yet.
- **Anything a nested repo owns** — each keeps its own `ISSUES.md` and fixes its own findings. The
  fanout hard-block, the `.d.ts` stub gap, the last two `ROADMAP-<slug>` renames and the
  first-line-comment queue all live there now.
- **`[gdrive-integration]`, `[offline-resilience]`, serious OCR** — content and infrastructure, not
  scaffold. OCR belongs where the image-only PDFs are.

## Rejected

- **Adopting `obra/Superpowers` over our craft flow** — no per-task tier routing, no file-relayed
  carry. Its trigger was imported instead.
- **Curing confident wrongness with a prompt rule** — induced loses to enforced, and this corpus is
  the evidence.
- **A preliminary cut of features before the ablation** — declined by Lucas 2026-08-21: cutting on a
  hostile blog post and a hunch is the guess the instrument exists to replace.
- **An ensemble router** — spend is driven by context size, so several models over the same large
  context pay the multiplier several times.
- **A global terseness rule, and `effort` as a *length* lever** — a wrong token budget degrades the
  answer. Effort as a *cost* lever stays open above.
- **A second compaction shim for copilot** — no copilot session has ever run here.
- **Raising `BLOCK_LINES` to 300 for every format** — weighed 2026-08-25 when the merged `SCHEMA.md`
  would not fit 200. Nothing in the tree sits between 201 and 306, and ~30 files are parked at
  190-200: that is a queue at the light, not a distribution. A higher cap moves the queue to 290-300
  and buys +3000 lines of headroom in the work whose whole point is losing 4776. The one file that
  genuinely needed room needed a **seam**, not a taller ceiling.
- **`core/` and `brain/` getting their own `ISSUES.md`** — both are WOS, and between them they hold
  no hand-written bug at all.
