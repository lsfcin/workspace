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

**🟡 the ablation — the repo has never been measured against its own absence**
*What* — variants of the public repo, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
It also **runs before the cutting campaign** (Lucas, 2026-09-15), because it is what says which
mechanism earns its keep. Unblocked 2026-09-16: the repo it varies is `lsfcin/wos`, public, synced
one way by `core/run tools/wos/publish/repo` and green on its own suite.
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
The instrument that names candidates is `publish/repo --orphans`: every tracked file no feature
claims, a stronger question than "who reads this" — `size --weighted` ranks what a session opens,
this ranks what nothing can say a purpose for. It read 659 on 2026-09-15 and **10** on 2026-09-16,
because most of those were claims the registry had not written; what is left is the real list.
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

Twenty-six killed items are in git, not here: `git log -S'## Rejected' -- ROADMAP.md`. A tombstone
stops earning its line once nobody who might revive the item remembers it, and this is the heaviest
file in the workspace — one nobody needs is read by everyone. The six of 2026-09-14 and the four of
2026-09-15 joined them on 2026-09-17 (Lucas): the git log IS the other place, and this section keeps
the pointer rather than the list.
