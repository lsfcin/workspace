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

## Measurement — does any of this earn its keep

**🟡 the scoreboard is running and owes its first reading**
*What* — the two-week reading, and the cuts it justifies: `core/run tools/wos/features --scoreboard`,
into `core/experiments/hook-scoreboard.md`. **Due 2026-09-28**; the tool prints its own start date,
so check it rather than this line.
*Why* — 82 features are on, so every cut is a guess and kept rules are paid on faith.
*Done when* — the table is read after two weeks of ordinary use and each silent feature is a decision.

**🟡 the public repo his students clone** — *the ablation's precondition, so it comes first*
*What* — the checkout at `code/wos/` and the sync that writes it. The rule deciding what crosses now
exists and reports itself (`core/run tools/wos/publish/repo`); nothing crosses unclaimed, so what
remains is the claims that reading says are missing, then the repo, then the push.
*Why* — students asked for it, and the ablation needs variants of it to turn a feature off in.
*Done when* — a student clones it and gets a working workspace.

**🟡 the ablation — the repo has never been measured against its own absence**
*What* — variants of the public repo, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
It also **runs before the cutting campaign** (Lucas, 2026-09-15), because it is what says which
mechanism earns its keep: public repo → ablation → cuts.
*Done when* — a **per-feature** verdict is readable. Runs outside this workspace (`academy/papers/wos-ablation/`).

## Legibility — can Lucas still read what he owns

**🔴 the health picture is built and does not land — redesign it**
*What* — `ARCHITECTURE.html` redrawn as a list ordered by colour and symbol, where the page now puts
a big mostly-empty table. Next deliverable is the Claude Design prompt for that session, and it has
to resolve one conflict: Lucas wants per-file reads per session on this page, and that is the one
number that breaks its determinism — it is regenerated at every close and must change only when the
workspace does.
*Why* — three drawings answered *what is there*; Lucas read this one 2026-09-15 and ruled it an
inventory with better manners.
*Done when* — he reads it at a glance and the shapes that fail are deleted.

## Portability — would this work on a machine that is not Lucas's

**🟡 the port grew the workspace and the payment is still short** — *after the ablation, not before*
*What* — the cut that funds the port, from the top of `core/run tools/wos/size --weighted` down. The
instrument names the candidate and it is **this file**, so draining the roadmap and paying the debt
are one job.
*Why* — `core/norms/reduce.md`: a session leaves fewer lines than it found. The port was worth every
line; that is a reason to pay, not a reason not to.
The instrument that names candidates arrived early, from the item above: `publish/repo --orphans`
lists every tracked file no feature claims, which is a stronger question than "who reads this" —
`size --weighted` ranks what a session opens, this ranks what nothing can say a purpose for.
*Done when* — the **weighted** total falls: lines SERVED per session, not lines on disk. The disk
number can be paid by deleting a file nobody opens, which nearly took `core/experiments/` — 11% of
the lines, zero reads in 88 sessions, and **the WOS paper's data. The cut never comes from there**
(Lucas, 2026-09-15). Several sessions; re-run the instrument rather than quoting a figure here.

**🟡 the platform boundary's last answer needs one session run from inside Windows**
*What* — manager names for the 3 `apt` rows (`poppler-utils`, `tesseract-ocr`, `ddgr`). The file's
own head only lets a row claim `system` once the name is VERIFIED on the other managers.
*Why* — a row claiming a portability nobody checked is the false green these checks exist to end.
Unblocked 2026-09-15: the machine is dual boot and `/mnt/windows` is that install mounted, so the
block was never "no Windows" but "not booted into it". From **WSL2** on that side the hooks run
unchanged — they are `sh core/run` — and `winget.exe` is reachable by interop. A native port with no
WSL is a different item, blocked on the `sh` in each shim.
*Done when* — each of the three is `system` with a verified name, or stays `apt` with the reason.
One session from Windows does it: WSL2 + Ubuntu, clone, `/install`, read the names out of
`winget.exe search` / `choco search`. `SETUP.md` names no operating system today, so what that
session discovers goes back into it as a step.
The other two answers are in: `is_owner_only()` reads the ACL back rather than trusting `st_mode`,
and `core/tools/deps.txt` carries a `floor` column — a floor, not a ceiling, because the failure is
a distro shipping something too old, never a release from the future.

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
- **An effort table built from `agy --print`** — 2026-09-15: its print mode writes to its own scratch dir and reports success, so every arm would have been a false green.
- **A phone-push channel (ntfy, or the harness's own)** — 2026-09-15 (Lucas): phone addiction is a real cost to him; a channel that fetches him is a loss even when its content is right. Telegram, silent, opened on his schedule.
- **A `Stop` hook for the close offer** — 2026-09-15: fires at the end of every response, so it would have to invent a reason to stay quiet. The crossing already has a once-per-threshold moment.
- **Curing confident wrongness inside this repo** — 2026-09-13 (Lucas): only a parser or solver refuses; research.
- **A research map here, and one review yaml per kept source** — 2026-09-13: a `REFS-<name>.md` does both.
- Eleven killed before 2026-09-11 are in git, not here: `git log -S'## Rejected' -- ROADMAP.md`. A
  tombstone stops earning its line once nobody who might revive the item remembers it, and this is
  the heaviest file in the workspace — one nobody needs is read by everyone.
