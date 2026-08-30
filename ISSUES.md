# Workspace issues
> What is currently untrue that we know about: hand-written issues first, every measured number
> inside its own generated block.

The scope is the **workspace itself** — the enforcement layer, the tools, the scaffold. A bug in a
project under `code/` belongs to that project's own `ISSUES.md`, and the entropy block below counts
every repo precisely so nothing goes dark while the ownership stays split.

Two rules, both from [`core/SCHEMA.md`](core/SCHEMA.md) § Boundaries where types nearly touch:
**never hand-edit inside a generated block**, and **never write a measured number outside one** — a
copied count is the drift these checks exist to catch. The FIXED gate governs the hand-written half
only, and it is satisfied the same way here as in every project: a bug flips to FIXED when a
matching regression spec exists and passes.

## B1 — `.opencode/wp-helpers.d.ts` is stale, and it switches the read gate off silently

**Symptom:** `tsc` fails on the stub with `Property 'stdin' does not exist on type '{}'`, so
`core/hooks/postedit/interfaces.sh` never regenerates it and the stub beside the source stays old.

**Why it is worse than a stale file:** `core/hooks/read/pre-read.sh` blocks a source read *only
while the stub beside it is current*. A stub that cannot be regenerated therefore does not merely
go out of date — it turns the interface-first discipline off for that file, and nothing says so.
That is the same failure shape the entropy dashboard's § Source files with no interface stub was
built to count, arriving through a different door.

**Repro:** run the stub generation over `.opencode/wp-helpers.js` and read the `tsc` output.

**Root cause:** unknown. The typed shape of the opencode plugin's helper argument is inferred as
`{}`, so every property access on it is an error; whether the fix is a JSDoc annotation on the
source or a `tsconfig` lib change is unestablished.

## B3 — a mixed carousel is read as a video, so every slide after the first is never opened

**Symptom:** `core/tools/video/video` on an Instagram carousel whose **first slide is a video**
returns only that slide. Found 2026-08-20 draining the INBOX: `instagram.com/p/Db3di5dEpS4/` is an
eight-slide post, and the entry's whole point — MatrAIx / Persona 8B, on slide 3 — was invisible.
Lucas had to screenshot the slide by hand.

**Root cause, confirmed by reading it:** `video_core.assemble` reaches the image path only inside
`if not ok:` — the comment says *"an image post probes as a failure. Retry through gallery-dl before
giving up."* That holds for an all-image carousel, where yt-dlp returns nothing. A **mixed** carousel
succeeds under yt-dlp, so `ok` is true, `video_images.gather` never runs, and the frame sampler reads
the first slide's video alone.

**Repro:** run the URL above at `--level full`. The tell is five near-identical VLM captions of one
frame — the sampler re-describing slide 1 while seven slides sit unread.

**Why it is worse than a thin block:** `/inbox` states that an unextracted link is an unroutable
entry, so this silently converts *routable* entries into ones triaged on a caption alone. Nothing
reports a slide count, so the loss is invisible at the call site.

**Lucas, 2026-08-20:** *"toda a triagem de INBOX deveria automaticamente decifrar imagens e vídeos,
incluindo OCR mas não somente isso, e sempre que possível usando zero-tokens."* The capability is
already there and already zero-token — tesseract plus a local VLM. It is the dispatch that is wrong,
not the extractors.

## B4 — a pre-edit block can exit non-zero with nothing on stderr

**Symptom:** an Edit to `code/isoroll-content/src/pipeline/kit_modules.py` was refused by
`core/hooks/checks/pre-edit.py` reporting **"No stderr output"** — no reason, no named fix. Found
during isoroll CP-3/CP-4.

**Why it matters:** running the same hook by hand with a payload that trips the size gate prints the
right message, so at least one rejection path returns non-zero silently. That breaks the contract in
[`core/hooks/SPECS.md`](core/hooks/SPECS.md) — a hook that blocks names the fix — and costs a round
of investigation per occurrence, which is the same silent-failure shape
[`core/SPECS.md`](core/SPECS.md) § Conventions exists to forbid.

**Root cause:** unknown. Which path exits quietly is unestablished; the size gate is not it.

## B5 — the scatter writes 26 local ledgers and nobody has ever committed one

**Symptom:** every nested repo carries an untracked `ISSUES.md` (and often `ARCHITECTURE.html`).
`git -C code/voti status` shows both as `??`, and the same holds across all 26. Found 2026-08-25
while checking what `make entropy` had dirtied; the files predate this session.

**Why it matters:** the scatter's whole premise is that *each repo keeps its own ledger and fixes its
own findings* — the reason the root header stopped charging itself for 571 findings it cannot act on.
An untracked ledger is not a ledger: it is invisible to that repo's clones, to its own history, and
to anyone who did not run the dashboard locally. So the 571 findings are addressed to readers who
cannot see them, and the design reads as working because the generator rewrites the files each run.

**Repro:** `for r in $(find . -name .git -maxdepth 4); do git -C ${r%/.git} status --short; done`.

**Root cause:** the dashboard writes the local ledgers but nothing stages or commits them, and each
one is a commit this repo may not make. Whether the fix is the scatter committing in each repo, a
`/roundup` step, or one sweep is undecided.

## B6 — half the Google tool families have a skill and half do not, on no stated rule

**Symptom:** `mail/gmail`, `calendar/gcalendar` and `files/gdrive` each have a `core/skills/<n>.md`
wrapping them. `slides/gslides`, `forms/gforms` and now `docs/gdocs` have none — they are reached
only through their `CONTEXT.md`. Found 2026-08-25 while building the docs family, which had to pick
a side with nothing to pick it on.

**Why it matters:** the split is not along capability, cost or how often the tool is used, so
neither answer can be justified when the next family lands — and the question gets re-litigated
every time. It also cuts both ways: if a skill genuinely helps an agent reach a tool, three families
are underserved; if `CONTEXT.md` is sufficient, three skills are lines the workspace re-reads every
session for nothing.

**Root cause:** never decided. The skills predate the routing table being enforced-read, so the
older families kept a wrapper the newer ones never needed. **Lucas's call**, and it should end as
one sentence in `core/tools/SPECS.md` § Adding a tool, so the next family reads the answer instead
of guessing.

## B7 — a bug id is cited across the tree and nothing stops it going stale

**Symptom:** `core/hooks/SPECS-shim.md` cited *"ISSUES.md B6"* for the ZCode trust gate. B6 is now
the Google-skills split — the zcode bug closed and its id was reused, so the pointer resolved to a
file that exists and a bug that is not the one meant. Found 2026-08-27 merging the hooks SPECS.

**Why it matters:** this is exactly the failure `checks/citation-gate.py` exists to stop, and it
only guards `Front <n>`. A `ROADMAP.md` item number is uncitable while an `ISSUES.md` id is cited
freely from prose and code comments — the same shape, half-enforced. **The asymmetry is the bug**,
not this one pointer.

**Root cause:** ids here are positional and completion is deletion, so every close renumbers. Whether
the fix is extending the gate, giving bugs durable slugs, or forbidding the citation is undecided —
Lucas's call, and it belongs in `core/SCHEMA.md` § Boundaries where types nearly touch.

## B8 — 60 generated mirror files are still tracked, and nothing regenerates them on edit

**What is true now:** a mirror is a **copy**, written and checked by content
(`core/tools/wos/skills/mirror.sh`). The symlink half is gone, so the skills stage no longer refuses
a commit and the skill library reads in this clone.

**What is still untrue:** the copies are **in git**. Every skill edit churns 60 tracked files, which
is the maintenance Lucas's ruling exists to delete.

**The ruling (2026-08-29, Lucas), and it is not "make symlinks work":** a native symlink on Windows
needs Developer Mode, a machine-level privilege out of proportion to what WOS is — *"WOS doesn't
tweak the machine's hardware and nothing near that"*. The mirrors become generated copies git does
not track: `.gitignore` covers all four mirror trees, and `/install`, the post-edit hook and the
pre-commit generator materialise them. *"Auto-generated content is totally fine given it is not
versioned; the copies that worry me are the ones we do by hand and have to maintain."*

**The condition attached, still not met:** regeneration must be automatic on install, on edit, on
create and on delete. `post-edit.sh` syncs the routing table and the codegraph and has never synced
skills, so a skill edit reaches the mirrors only at commit time. Untracking before that guarantee
exists would leave the workspace depending on a step that does not run. **Both halves in one pass.**

## B9 — a verification run rewrites ISSUES.md, so it is not a verification

**Symptom:** `test_features_wiring` probes every registered hook, and one of them is the entropy
dashboard, which **writes**. Running the suite therefore modifies the working tree.

**Why it matters twice.** A check with a side effect cannot be trusted to report on the thing it
changed — the rule the deleted `Makefile` stated in its own comment. And it is what blocks the
cheapest available speedup: `pytest -n auto` is unsafe while any test writes to a shared file, and
the suite's ~110s is the standing cost of every commit.

**Where to look:** the probe should call the dashboard with a temp output path, or the dashboard
should grow a `--dry-run` that reports without writing.

## B10 — a stash holds 71 files of already-landed work, and the handoff called it one file

**Symptom:** `stash@{0}` is described in `outputs/handoff.md` as holding only `core/skills/inbox.md`,
awaiting a `git stash pop` once B8 cleared. It actually holds the whole S4 de-bash port as WIP at
`aa17d3a` — `gates.py`, `pre_commit.py`, `stubs.py`, `line_counts.py` and 67 more, all since landed
in different form. **Popping it would have conflicted against every one of them.**

**Already handled:** the one genuinely unlanded line — a pointer to the deleted
`core/hooks/generators/prepare.sh` — was applied by hand to `core/skills/inbox.md`.

**The decision owed:** whether to drop the stash. It is Lucas's call because dropping is not
trivially reversible, and nothing else in it is wanted.

**The lesson worth more than the stash:** a hand-off recorded what a session *believed* was in a
stash rather than what `git stash show --stat` says. A stash is opaque state that outlives the
session that made it, and this one was one command away from being popped blind.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans the whole tree. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-08-29 · 711 tracked files scanned · **42 findings here** (2026-08-25: 33 · +9 over 4 days)

| Check | Findings |
|-------|----------|
| Off-allowlist `.md` types | 0 |
| CONTEXT.md hand-written inventories | 0 |
| Naming and placement | 1 |
| Projects not declaring their goal | 0 |
| Wiki-links naming nothing | 0 |
| Retired tokens still alive | 0 |
| Roadmap item numbers cited outside a roadmap | 0 |
| Items claimed by two ledgers | 0 |
| Size signals | 25 |
| Source files with no interface stub | 2 |
| Directories holding too many files | 9 |
| Prose describing finished work | 0 |
| Unanswered scaffold placeholders | 2 |
| Doubt stores missing their own discipline | 0 |
| Ledgers naming a model where they mean a tier | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 0 |
| Constraints trapped in a CONTEXT.md head | 1 |
| Repos on an unmerged feature branch | 1 |
| Remote branches already merged into their base | 1 |

### Off-allowlist `.md` types

*route via core/SCHEMA.md § four disposal routes*

Clean.

### CONTEXT.md hand-written inventories

*the routing block owns inventory*

Clean.

### Naming and placement

*kebab-case ASCII, types where their scope allows*

- code/_templates/module.SPEC.md: 'module.SPEC.md' is neither a lowercase instance nor a known type.

### Projects not declaring their goal

*line 3 of a code/ CONTEXT.md*

Clean.

### Wiki-links naming nothing

*a [[slug]] is a goal file or an item in one*

Clean.

### Retired tokens still alive

*a rename is unfinished until these are zero*

Clean.

### Roadmap item numbers cited outside a roadmap

*a closed item is deleted — cite the SPECS.md/SCHEMA.md section that owns the rule*

Clean.

### Items claimed by two ledgers

*v1 criterion 2 — an item lives in one place*

Clean.

### Size signals

*a signal for review, never a cap — do not summarize to fit*

- .craft/commands-mirror-cost/0-clarify.md — 2 line(s) over the 120-column cap (first at line 9)
- AGENTS.md — 2 line(s) over the 120-column cap (first at line 6)
- ROADMAP.md — 201 lines, over the 200 cap; introduced by feeca22 lsfcin
- SETUP.md — 566 lines, over the 200 cap; introduced by 3e575bb lsfcin
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 48 line(s) over the 120-column cap (first at line 3)
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 117)
- brain/INBOX.md — 263 lines, over the 200 cap; introduced by 459e3f8 lsfcin
- brain/INBOX.md — 3 line(s) over the 120-column cap (first at line 73)
- brain/USER.md — 1 line(s) over the 120-column cap (first at line 16)
- brain/attachments/instituto-estrategias.md — 4 line(s) over the 120-column cap (first at line 21)
- brain/goals/craft-flows.md — 3 line(s) over the 120-column cap (first at line 121)
- brain/goals/cria.md — 1 line(s) over the 120-column cap (first at line 65)
- brain/goals/home-casinhas.md — 3 line(s) over the 120-column cap (first at line 53)
- brain/goals/spacemantics.md — 2 line(s) over the 120-column cap (first at line 57)
- brain/goals/spec-driven-development.md — 1 line(s) over the 120-column cap (first at line 46)
- brain/goals/workspace-os.md — 3 line(s) over the 120-column cap (first at line 137)
- core/SCHEMA.md — 223 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/hooks/SPECS.md — 341 lines, over the 200 cap; introduced by 0237832 lsfcin
- core/norms/one-action.md — 1 line(s) over the 120-column cap (first at line 6)
- core/norms/storage.md — 1 line(s) over the 120-column cap (first at line 6)
- core/refs/REFS-context.md — 1 line(s) over the 120-column cap (first at line 36)
- core/refs/REFS-legibility.md — 1 line(s) over the 120-column cap (first at line 23)
- core/refs/REFS-tooling.md — 2 line(s) over the 120-column cap (first at line 67)
- core/skills/drive.md — 2 line(s) over the 120-column cap (first at line 42)

### Source files with no interface stub

*the read gate only fires when a stub exists — a missing one turns it off silently*

- code/eslint.shared.js — no .d.ts
- core/tools/test/workspace/harness/test_hook_environment.py — no .pyi

### Directories holding too many files

*splitting costs one hop — pay it only when it removes more table than it adds*

- academy/administration/coordenacao-lc/novo-ppc-bcc/ementas — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/entropy — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/routing — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/hooks — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/scripts — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/law/entropy — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/wos — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds

### Prose describing finished work

*git is the history — cut it, or rewrite it as present-tense state*

Clean.

### Unanswered scaffold placeholders

*a generator asked a question — answer it at the source, never by cutting the marker*

- academy/administration/CONTEXT.md:13: 1 unanswered placeholder(s).
- academy/administration/coordenacao-lc/novo-ppc-bcc/CONTEXT.md:14: 1 unanswered placeholder(s).

### Doubt stores missing their own discipline

*an experiment states its Method, Results, What changed and Limitations; a judged reference carries a source tier*

Clean.

### Ledgers naming a model where they mean a tier

*which model fills a tier is data — core/flows/craft/routing.md*

Clean.

### Header fields naming code that is not there

*a field naming our own tree is a claim, and it is checked before a later session inherits it as fact — core/SCHEMA.md § Every field that names our own code is verified*

Clean.

### Truncated routing descriptions

*the source wrote past the bound — shorten it there, never edit the table*

Clean.

### Constraints trapped in a CONTEXT.md head

*the only enforced-read type — move the contract to a sibling SPECS.md*

- core/tools/verify/CONTEXT.md: head is 607 tok carrying 1 constraint(s).

### Repos on an unmerged feature branch

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/os-agnostic-port is 9 ahead of main

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 6 merged into main: git -C . push origin --delete feature/calendario-tecedu feature/gdocs feature/self-description-grounding feature/wos-lean feature/wos-lean-setup feature/wos-lean-specs

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-08-29 · `verify.py full` · **green (591 passed, 4 skipped in 114.49s (0:01:54))**
<!-- verify:end -->
