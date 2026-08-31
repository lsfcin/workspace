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

**Second sighting, 2026-08-31:** an image post (`instagram.com/p/DcMf6TuFIYS/`) returned *no text at
all*, at `--level full` too — same dispatch gap, one step further: not a thin block, an empty one. The
entry was routed on Lucas's own note alone, which is the fallback, not the design.

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

## B9 — a verification run rewrites ISSUES.md, so it is not a verification

**Symptom:** `test_features_wiring` probes every registered hook, and one of them is the entropy
dashboard, which **writes**. Running the suite therefore modifies the working tree.

**Why it matters twice.** A check with a side effect cannot be trusted to report on the thing it
changed — the rule the deleted `Makefile` stated in its own comment. And it is what blocks the
cheapest available speedup: `pytest -n auto` is unsafe while any test writes to a shared file, and
the suite's ~110s is the standing cost of every commit.

**Where to look:** the probe should call the dashboard with a temp output path, or the dashboard
should grow a `--dry-run` that reports without writing.

**Cost measured 2026-08-30:** it blocked a merge twice in one session. Every commit's verify run
dirties `ISSUES.md`, and `git merge` refuses to start with a modified tracked file, so pulling a
parallel session's work meant discarding the rewrite first — a manual step in the middle of the one
operation where losing track of local changes is most expensive. And on 2026-08-28 it did the damage
it threatens: a test run on the second machine rewrote the generated block of `ISSUES.md` with that
machine's partial scan (B19), and the rewrite had to be reverted by hand.

## B12 — `core/run` says it runs anything in `core/`, and it only runs Python

**Symptom:** the launcher's own first line is *"the one command that runs anything in core/"*, but it
`exec`s every target with the venv interpreter. `core/tools/wos/sync-skills` and `sync-global-skills`
are bash, so `core/run tools/wos/sync-skills` dies with `SyntaxError: unmatched ')'`.

**Why it is worse than a wrong doc:** `SETUP.md` § Caveman taught `core/run tools/wos/sync-global-skills
--check` as a **precondition**, so the step could never report itself already done. Found 2026-08-30
while adding the § Skill mirrors step, which nearly copied the same broken spelling.

**Already true:** every *code* call site was already correct — `generators.py` and
`postedit/sync.sh` both spawn `sh <path>` — so the convention exists and only the prose disagreed.
Both `SETUP.md` sites now say `sh core/tools/wos/…`.

**The decision owed:** whether the launcher learns to dispatch on the target (a `.sh`/shebang arm) or
whether two bash tools stay a documented exception. **Lucas's call**, because it is the difference
between one entry point and two, and `test_no_document_teaches_a_tool_call_that_cannot_run` currently
catches neither spelling.

## B13 — the harness mirror list is hand-maintained in a bash array

**Symptom:** `core/tools/wos/sync-skills` declares `MIRRORS=(.opencode .claude .zcode .agents)` in
its own source. Adding a harness means editing that array by hand — done twice in one week, once for
`.agents/` (Antigravity, 2026-08-30) and once when `.zcode/` arrived.

**Why it matters:** which harnesses this workspace publishes to is a **declaration**, and every other
declaration in the workspace lives in a data file that something reads — `core/features.txt`,
`core/profile.txt`, `core/tools/deps.txt`, `core/hooks/limits.env`. This one is code, so nothing can
check it, the `.gitignore` block has to restate the same list in git's format, and a harness added to
one and not the other fails silently in the direction that leaves stale mirrors on disk.

**Root cause:** it predates the registry. Same shape as the defect fixed 2026-08-30 in
`platform_law.py`, which branched on data it never published.

**Third instance, 2026-08-28:** `test_shim_paths.py` guarded opencode, copilot and zcode and never
`.claude/settings.json` — the one shim it existed to guard was the one it did not read, which is how
twenty dead commands survived there (B16). It is added now. The lesson is not the missing file: the
shim table was written by hand and nobody compared it against an `ls` of the configs that exist.

## B11 — every Google OAuth token on this machine is world-readable

**Symptom:** `~/.config/workspace-{drive,drive-write,gmail,docs,forms}/` are `775` and the
`*.token.json` inside them are `664`, so any local user account can read a live refresh token for
Lucas's mail, Drive, Docs and Forms. Found 2026-08-26.

**Why it matters:** a refresh token is the credential, not a cache of one — reading it is having the
account until it is revoked. Nothing in the workspace sets a mode when it writes these files, so
every new provider directory inherits the umask and the exposure grows with the tool surface.

**Root cause:** the token writers create files with default permissions and no check asserts on the
mode. The fix is `700`/`600` plus a writer that sets the mode itself; it was left undone because
tightening could break another local user running the tools, which is Lucas's call to make.

## B20 — two sessions share one checkout and only the branch is guarded

**Symptom:** on 2026-08-31, minutes after six issues (B14-B19) were committed here, another live
session in the same working tree wrote its own older copy of `ISSUES.md` back over them — 93 lines
deleted, nothing inserted. They were recovered from the commit; had the drain not committed first,
they were gone with nothing to notice the loss.

**Why the existing guard misses it:** `core/hooks/git/branch_marker.py` warns when **HEAD** moves
under a session, and it fired correctly today. Nothing watches a **file** read early and written
late, which is the shape a long session has by default — and the workspace's own convention for
parallel work (partition by subtree) is prose, obeyed by whoever remembers it.

**Where to look:** the durable files every session touches at close — `ISSUES.md`, `ROADMAP.md`,
`brain/INBOX.md` — are the whole exposure. A hook that compares a write against the file's mtime
since the session's own last read would catch it; whether that is worth a gate is Lucas's call.

## B14 — a path becomes text and the separator follows the operating system

**Symptom:** on the Windows machine (measured 2026-08-27) the largest single group of test failures
is one pattern: the code emits `C:\Users\lucas\workspace\academy\papers` where the test expects
`academy/papers`. `pathlib` resolved the **filesystem** and never resolved the **vocabulary**.

**Where it bites:** every place a path stops being a handle and becomes data — a routing-table row, a
registry key, a line in `ISSUES.md`, a comparison against `core/features.txt`.

**The fix, and why it is not a concession:** forward slash always, for every path that is *data* —
`.as_posix()` at the boundary, `Path` only to touch disk. Git has done exactly this internally for
twenty years. It makes the routing tables and the entropy dashboard byte-identical between machines,
which is what `test_the_output_is_deterministic` already asks for and cannot get today.

## B15 — the gates run on the second machine and block nothing, and half a fix makes it worse

**Symptom:** the shim was repaired (`core/hooks/run` finds the interpreter and the workspace root),
so the gates now execute there. They still pass everything: `context-gate.py:45` compares paths as
text — `str(target).startswith(str(WORKSPACE) + '/')` — and a Windows target carries `\` against a
`/` prefix, so nothing ever matches and every access returns 0 early. Three sites: `chain.py:53`,
`context-gate.py:45`, `spec-read-gate.py:79`.

**Why it cannot be fixed alone:** the session markers live in a literal `/tmp`, in fifteen files.
Native Python reads `/tmp` as `C:\tmp`, which does not exist; Git Bash reads the MINGW one. So
`pre-read.sh` (shell) reads markers `context-tracker.py` (Python) never wrote. Fix the comparison by
itself and the gate starts blocking with no way to satisfy it — the workspace becomes unusable there.

**Both halves land together, and together they are the de-bash migration.** Silent-pass is the same
failure mode as the Store alias: a check that reports success by never running.

## B16 — the versioned configuration assumes one machine, and says the opposite

**Symptom:** `SETUP.md` states the hooks activate on their own after a clone. They do not.
`.claude/settings.json` and `.zcode/config.json` are versioned with `/mnt/workspace/…` hardcoded in
~20 commands, and the "Workspace path" step only rewrites shebangs under `core/tools`. In any clone
outside that path the whole enforcement layer is dead in silence — the exact failure `deps.txt`
exists to eliminate. Same class: `permissions.allow` is entirely `Bash(git -C * log *)`, so on a
machine whose agent calls a PowerShell tool nothing matches and Lucas is prompted for everything.

**The three per-OS forks are all broken, and that is the argument, not a coincidence:**
`start-session.ps1` prints `WORKSPACE.md`, a file that does not exist — the real one is `AGENTS.md`,
which the `.sh` prints while calling itself a *"neutral session-start entrypoint"*; `.agentrc.json`
points `start_session_windows` at that broken `.ps1`; `caveman/hooks/activate.js` selects
`caveman-statusline.ps1`, which is not in the repo. **The fix is to delete the `.ps1` files**, not to
repair them: one entrypoint that runs on both.

**Still shell-only, so still absent there:** `core/tools/wos/roundup`, which is why one close was done
by hand; and the `bash -n` check globs by extension, which is how `pre-commit`, `post-commit` and
`run` — the three shell files with the widest blast radius, none of them allowed an extension — were
the three nothing checked. That last one now has a test. `caveman` is called vendored by the port
plan and is not in `core/hooks/vendored.txt`: either it is listed, or it stops being called vendored.

## B17 — text is read and written in whatever encoding the operating system prefers

**Symptom:** file reads and writes now declare `encoding='utf-8'` — the port fixed those after six
`UnicodeDecodeError` failures on a Brazilian Windows install (cp1252). `sys.stdout` still inherits the
console's: `permissions --check` printed `permissions: open <?> rendered config matches`.

**Why the default is never the answer:** every `.md` in this workspace is UTF-8, so the OS default is
wrong everywhere — including Linux, where it happens to work by accident of locale.

## B18 — a declared dependency can be installed, importable, and useless, and the probe reads green

**Symptom:** `secretstorage` is declared in `core/tools/deps.txt` with an import probe. On Windows
(2026-08-27) `pip install secretstorage` exits 0 and `import secretstorage` exits 0, so the probe is
**green** — while the Secret Service it talks to is D-Bus and exists only on Linux.

**Why a false green is worse than a false red:** the `breaks` column promises to say when a feature
goes away, and here it stays quiet. Two things are missing: `kind` has no ceiling saying which systems
a dependency applies to, and the probe measures an import where it should measure the function.

**Adjacent and unmigrated:** the four `apt` rows (poppler-utils, ffmpeg, tesseract-ocr, ddgr) still
print `sudo apt-get` on a machine with no apt. The build is on `/ROADMAP.md` § Portability.

## B19 — four instruments report smaller, cleaner, or different, and none of them says so

**Symptom, all found in single sessions on the second machine (2026-08-28):**

- Git Bash rewrites an argument that looks like an absolute POSIX path, so `git grep '/mnt/workspace'`
  returns nothing in a tree holding it in over a hundred places — MSYS turned the pattern into
  `C:/Program Files/Git/mnt/…`. Use `MSYS_NO_PATHCONV=1`, or the Grep tool.
- PowerShell's `Measure-Object -Line` does not count blank lines, underreports by about a fifth, and
  made one session promise a reduction that did not exist. Use `wc -l`.
- **The Grep tool normalises the path separator inside the matched content**, not only in the path
  prefix: it showed `'core\hooks\pre-commit'` in a file that contains `'core/hooks/pre-commit'`, and a
  bug that did not exist was nearly "fixed". **Confirm with Read before acting on a path seen in Grep.**
- The entropy dashboard scans a much smaller tree there — hundreds of files against thousands, with
  most nested repos missing — and reports the partial picture in the same shape as a full one.

**What they have in common:** each answers confidently and none carries its own caveat, so the reader
cannot tell a measurement from a shrug. The dashboard is the one we own: a scan that sees less has to
say it saw less.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans the whole tree. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-08-31 · 2357 tracked files scanned · **46 findings here** (2026-08-25: 33 · +13 over 6 days) · 560 more across 27 nested repos, each in its own ISSUES.md

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
| Size signals | 29 |
| Source files with no interface stub | 2 |
| Directories holding too many files | 10 |
| Prose describing finished work | 0 |
| Unanswered scaffold placeholders | 1 |
| Doubt stores missing their own discipline | 0 |
| Ledgers naming a model where they mean a tier | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 0 |
| Constraints trapped in a CONTEXT.md head | 1 |
| Repos on an unmerged feature branch | 1 |
| Remote branches already merged into their base | 1 |

### Findings per code repo

*Each repo keeps its own `ISSUES.md` and fixes its own findings; this table only says which one to open next.*

| Repo | Findings |
|------|----------|
| [`academy/papers/2026-JBCS-relativistic_raytracer`](academy/papers/2026-JBCS-relativistic_raytracer/ISSUES.md) | 11 |
| [`academy/papers/2026-SIBGRAPI-relativistic_raytracer`](academy/papers/2026-SIBGRAPI-relativistic_raytracer/ISSUES.md) | 4 |
| [`academy/papers/2027-CHI-cria`](academy/papers/2027-CHI-cria/ISSUES.md) | 8 |
| [`academy/papers/2027-ICLR-dobra`](academy/papers/2027-ICLR-dobra/ISSUES.md) | 7 |
| [`academy/papers/ai4good`](academy/papers/ai4good/ISSUES.md) | 5 |
| [`academy/papers/mechanism-search`](academy/papers/mechanism-search/ISSUES.md) | 2 |
| [`academy/papers/mutual-credit-ai`](academy/papers/mutual-credit-ai/ISSUES.md) | 2 |
| [`academy/papers/pls-pix`](academy/papers/pls-pix/ISSUES.md) | 2 |
| [`academy/papers/spacemantics`](academy/papers/spacemantics/ISSUES.md) | 4 |
| [`academy/papers/wos-ablation`](academy/papers/wos-ablation/ISSUES.md) | 4 |
| [`branches/casinhas`](branches/casinhas/ISSUES.md) | 6 |
| [`branches/instituto`](branches/instituto/ISSUES.md) | 14 |
| [`code/aiwbot`](code/aiwbot/ISSUES.md) | 122 |
| [`code/apptime`](code/apptime/ISSUES.md) | 21 |
| [`code/corpora`](code/corpora/ISSUES.md) | 12 |
| [`code/cria`](code/cria/ISSUES.md) | 6 |
| [`code/dobra`](code/dobra/ISSUES.md) | 15 |
| [`code/flows`](code/flows/ISSUES.md) | 90 |
| [`code/freeai`](code/freeai/ISSUES.md) | 8 |
| [`code/gira`](code/gira/ISSUES.md) | 5 |
| [`code/isoroll-content`](code/isoroll-content/ISSUES.md) | 45 |
| [`code/isoroll-module`](code/isoroll-module/ISSUES.md) | 97 |
| [`code/laplata`](code/laplata/ISSUES.md) | 4 |
| [`code/obra`](code/obra/ISSUES.md) | 0 |
| [`code/ppc`](code/ppc/ISSUES.md) | 6 |
| [`code/spacemantics`](code/spacemantics/ISSUES.md) | 58 |
| [`code/voti`](code/voti/ISSUES.md) | 2 |
| **collected** | **606** |

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
- AGENTS.md — 3 line(s) over the 120-column cap (first at line 6)
- ROADMAP.md — 239 lines, over the 200 cap; introduced by feeca22 lsfcin
- SETUP.md — 605 lines, over the 200 cap; introduced by 3e575bb lsfcin
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 48 line(s) over the 120-column cap (first at line 3)
- academy/administration/organograma.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/administration/plantel.md — 4 line(s) over the 120-column cap (first at line 2)
- academy/administration/processos/equivalencias.md — 8 line(s) over the 120-column cap (first at line 2)
- academy/administration/processos/normas.md — 3 line(s) over the 120-column cap (first at line 6)
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 147)
- brain/INBOX.md — 2 line(s) over the 120-column cap (first at line 18)
- brain/USER.md — 1 line(s) over the 120-column cap (first at line 16)
- brain/attachments/instituto-estrategias.md — 4 line(s) over the 120-column cap (first at line 21)
- brain/goals/craft-flows.md — 3 line(s) over the 120-column cap (first at line 121)
- brain/goals/cria.md — 1 line(s) over the 120-column cap (first at line 65)
- brain/goals/home-casinhas.md — 3 line(s) over the 120-column cap (first at line 68)
- brain/goals/spacemantics.md — 2 line(s) over the 120-column cap (first at line 57)
- brain/goals/spec-driven-development.md — 1 line(s) over the 120-column cap (first at line 46)
- brain/goals/workspace-os.md — 3 line(s) over the 120-column cap (first at line 141)
- brain/memory/user_profile.md — 1 line(s) over the 120-column cap (first at line 16)
- core/SCHEMA.md — 223 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/hooks/SPECS.md — 361 lines, over the 200 cap; introduced by 0237832 lsfcin
- core/norms/reduce.md — 1 line(s) over the 120-column cap (first at line 6)
- core/norms/secrets.md — 1 line(s) over the 120-column cap (first at line 6)
- core/refs/REFS-context.md — 1 line(s) over the 120-column cap (first at line 36)
- core/refs/REFS-legibility.md — 1 line(s) over the 120-column cap (first at line 31)
- core/refs/REFS-tooling.md — 2 line(s) over the 120-column cap (first at line 67)
- core/skills/drive.md — 2 line(s) over the 120-column cap (first at line 46)

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
- core/tools/test/workspace — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/wos — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds

### Prose describing finished work

*git is the history — cut it, or rewrite it as present-tense state*

Clean.

### Unanswered scaffold placeholders

*a generator asked a question — answer it at the source, never by cutting the marker*

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

- . — feature/inbox-drain is 2 ahead of main

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 2 merged into main: git -C . push origin --delete feature/opencode-wiring-review feature/os-agnostic-port

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-08-31 · `verify.py full` · **green (627 passed in 46.44s)**
<!-- verify:end -->
