# Workspace issues
> What is currently untrue that we know about: hand-written issues first, every measured number
> inside its own generated block.

The scope is the **workspace itself** — the enforcement layer, the tools, the scaffold. A bug in a
project under `code/` belongs to that project's own `ISSUES.md`, and the entropy block below counts
every repo precisely so nothing goes dark while the ownership stays split.

Two rules, both from [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary:
**never hand-edit inside a generated block**, and **never write a measured number outside one** — a
copied count is the drift these checks exist to catch. The FIXED gate governs the hand-written half
only, and it is satisfied the same way here as in every project: a bug flips to FIXED when a
matching regression spec exists and passes.

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
Restored 2026-08-31: a session deleted this section without a fix or a regression spec, which the
FIXED gate forbids — deletion is a status flip like any other.

## b20260831-scattered-ledgers-never-push

**Symptom:** committing in the workspace repo makes the ledger scatter write and **commit** a
regenerated `ISSUES.md` into every nested repo it touched — 25 of them in one go on 2026-08-31 —
and pushes none of them. The commits are correct; they simply stay on this disk.

**Why it matters:** it manufactures exactly what
[`code/SPECS-git.md`](code/SPECS-git.md) § Push policy forbids, at a rate of one commit per repo per
workspace commit, and it does it *behind* the session rather than in front of it — nobody typed the
commit, so nobody thinks to push it. The repo-wide audit that found it had to push 25 repos by hand
after having already declared the tree clean twenty minutes earlier.

**Root cause:** the scatter reuses the commit path and not the push path.
[`core/hooks/post-commit`](core/hooks/post-commit) auto-pushes `feature/*` for the repo the hook
fired in, and nothing carries that to the repos the scatter wrote into. Two candidate fixes, neither
costed yet: push each scattered ledger from the same hook, or stop committing them there and let
each repo's own next commit carry its ledger. The second is smaller and matches "one repo, one
session, one commit"; the first keeps the ledger true the moment it is written.

## b20260901-a-tracked-json-cannot-be-routed-to

**Symptom:** `.agents/hooks.json` is tracked, described, and had a routing row — and the first
sync of `.agents/` in months deleted it. `workspace_scanner.is_scanned` admits a file only if its
suffix is in `workspace_meta.ALL_EXTS`, which has no `.json`, so the row could not be rebuilt.

**Why it matters:** the row was right and the generator cannot produce it, so the directory now
describes itself with a file missing. Every config a harness dictates is a `.json`
(`.agents/hooks.json`, `.zcode/config.json`), which is exactly the class the routing table exists
to name. It also means the deletion looked like this session's regression and had to be proven not
to be — a check that silently drops a row costs that investigation every time.

**Root cause:** unestablished which change dropped `.json` from `ALL_EXTS`, and whether it was
dropped to keep generated `.json` out. The fix is a decision about that set, not about the scanner.

## b20260901-a-second-shell-tool-walks-past-every-read-gate

**Symptom:** on Windows the harness exposes a PowerShell tool alongside Bash. `Get-Content` on a
source file with a current stub is **not blocked**, while `sed` on the same file through Bash is —
`.claude/settings.json` matches `Bash` for the command gate and `Read` for the interface gate, and
this tool is neither. Found 2026-09-01 by using it.

**Why it matters:** the enforcement layer is the workspace's whole premise, and it is weaker on one
operating system than the other — silently, and in the direction where nothing reports it. It is the
same shape as the bare `python3` finding: a gate that reads as installed and never fires.

**Root cause:** the matchers name tools rather than capabilities, and a harness may add a tool. The
fix is a decision — widen the matchers, or state that the gates are Bash-only and say so where a
reader will see it.

## b20260901-a-git-symlink-is-a-text-file-on-windows

**Symptom:** `brain/memory/user_profile.md` is stored as a symlink (mode 120000). Windows git has
`core.symlinks=false`, so the clone materialises a 10-byte file whose whole content is `../USER.md`.
Anything reading it gets that string instead of Lucas's profile, and
[`brain/memory/MEMORY.md`](brain/memory/MEMORY.md) routes to it.

**Why it matters:** it is the ruling [`SETUP.md`](SETUP.md) § Skill mirrors already made on
2026-08-29 — native symlinks under Git Bash need Developer Mode, a privilege out of proportion to
this workspace — applied everywhere except the one file that predates it. The mirrors stopped being
symlinks; this did not follow.

**Root cause:** it was never revisited. Whether the answer is a generated copy, a pointer line, or
folding the file into `USER.md` is Lucas's call.

## b20260901-one-answers-file-is-shared-by-two-operating-systems

**Symptom:** `core/profile.txt` is versioned and its own head says it holds the answers **for THIS
machine**. Two machines pull it. `features --on/--off` on one lands on the other, and the permission
level is one line in the same file.

**Why it matters:** every other per-machine artifact in the workspace is generated and gitignored
(`.claude/settings.local.json`, the mirrors, `.venv`). This one is the answers themselves, tracked,
and the two clones are different operating systems with genuinely different feature sets — `latex`,
`telegram-capture` and the apt-only deps are not the same question here as there.

**Root cause:** it predates the second machine. The per-command escape hatch (`WOS_FEATURES_OFF=`)
exists and the per-machine one does not. **Lucas's call**, because the alternative — a gitignored
answers file — costs the reviewable general/Lucas-specific diff the head says it is for.

## b20260901-a-generator-writes-the-hosts-path-separator

**Symptom:** two generators published a Windows path separator into content meant to be read
anywhere. `core/hooks/routing/workspace_meta.py` § `interface_for` formatted a `Path`, so
regenerating any routing table here wrote `](auth\gauth.pyi)` into a **tracked** `CONTEXT.md` — a
file [`test_pointer_integrity.py`](core/tools/test/workspace/test_pointer_integrity.py) checks. And
`render_command` rebased every command-file link with `os.path.relpath`, so `.claude/commands/`
carried **16 dead links across 5 files**. Both found 2026-09-01, by the tables rewriting themselves
during the skills port. Both fixed there, with `as_posix()`.

**Why it stays open as a class:** a markdown link separator is `/` on every operating system, and
nothing checks that a generator knows it. These two were found by accident — one because an
unrelated edit regenerated a table, the other because a byte-for-byte equivalence diff was being run
for a different reason. `render_command`'s own comment says it exists to fix dead relative links,
and it had been publishing them on this machine since the day it was written, invisibly, because the
machine that authored the fix spells the separator the way markdown wants.

**Root cause:** unestablished how many other generators format a `Path` into text that leaves the
machine. The fix is a check that no generated `.md` contains a backslash inside a `](…)` target —
the one in
[`test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.py`](core/tools/test/workspace/gates/test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.py)
covers `.claude/commands/` only.

## b20260901-a-source-file-is-crlf-in-a-tree-that-declares-lf

**Symptom:** `core/skills/install.md` is CRLF in this working tree. `.gitattributes` declares
`* text=auto eol=lf` and its own comment says *"LF is not 'the Linux ending' here, it is the
workspace's ending"*; the git blob is LF, and `git status` is clean because normalisation hides the
difference on read. The mirrors are byte copies, so the CRLF propagates into all four of them and
into the command file — one skill spelled differently from the other sixteen, on one machine only.

**Why it matters:** it is invisible to every check we have. It surfaced only because the port's
equivalence diff compared bytes. The same shape also means `head -1` disagrees across the two
clones: MSYS strips a trailing CR inside command substitution and GNU bash does not, so a CRLF
source passes the frontmatter check here and would read as having no frontmatter at all on Linux.
The port answers that in `validate._lines` — for the checker. The file itself is still CRLF.

**Root cause:** unestablished how it got that way (an editor, or a checkout before `.gitattributes`
declared the rule). Whether the fix is renormalising the working tree once or a check that catches
the next one is the open question.

## b20260902-nothing-forbids-a-test-from-dirtying-the-real-tree

**Symptom:** two of three full runs were red on this clone on 2026-09-02, on a suite the Windows
clone had seen green three times running. One case seeds drift into `core/skills/compass.md` and
restores it in a `finally`; parallel workers reading inside that window failed — the `sync-skills`
check, and the diagram's determinism, which renders the tree twice and got two different trees.

**Why it matters:** the pre-commit gate runs this whole suite on every commit at the workspace root,
so a race here refuses commits at random, and the operator's evidence is a failure in a file they
did not touch. It is also invisible in the direction that matters: how wide the window opens is a
**core count**, so green on one machine says nothing about the other — the same shape as
`b20260901-one-answers-file-is-shared-by-two-operating-systems`, one layer down.

**Fixed for the one case that was proven:** it wears `@pytest.mark.serial` and `verify.py` runs a
second serial pass. **What stays open is the class.** `core/tools/test/wos/CONTEXT.md` states the
law in as many words — *"Each test builds its own repo and bare origin; nothing touches the real
workspace"* — and nothing checks it. A crude grep for a write beside a `WORKSPACE_ROOT` reference
names ~40 files, almost all of them false (they write into `tmp_path`), so the audit is real work
rather than a scan. The structural fix is a root argument on `mirror-heal.py` and `sync-skills`, so
the one case with no seam gets one.

**Root cause:** the suite went parallel 2026-09-01 and the law it broke was written for a serial
runner, where a mutation restored in a `finally` is invisible to everything.

## b20260902-a-generated-ledger-is-red-on-the-clone-that-did-not-write-it

**Symptom:** `verify.py full` failed here on two `test_entropy_scatter.py` cases —
no collected row, and `academy/papers/2026-JBCS-relativistic_raytracer` missing from the root index
— against an `ISSUES.md` this session had not touched. The block was generated on the Windows clone,
which does not have those nested repos; this one has 27. Regenerating made it green with no source
change.

**Why it matters:** the suite asserts a generated block matches the machine reading it, and the
block is committed. So the same commit is green on the machine that wrote it and red on the other,
and every pull hands the receiving clone a red pre-commit gate for work it did not do — which is
also the shape `mirror-heal.py` was built for, on a different artifact. The first suspicion is
always the local change, so it costs an investigation each time.

**Root cause:** unestablished whether the answer is regenerating on receipt (the `mirror-heal.py`
route), scoping the scatter assertions to repos that exist locally, or accepting that this block is
per-machine and untracking it. **Lucas's call**, because the third costs the reviewable diff the
ledger exists to give.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans the whole tree. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-02 · 2394 tracked files scanned · **23 findings here** (2026-08-25: 33 · -10 over 8 days) · 399 more across 27 nested repos, each in its own ISSUES.md

| Check | Findings |
|-------|----------|
| Off-allowlist `.md` types | 0 |
| CONTEXT.md hand-written inventories | 0 |
| Naming and placement | 0 |
| Routing tables pointing at files git does not carry | 0 |
| Projects not declaring their goal | 0 |
| Wiki-links naming nothing | 0 |
| Retired tokens still alive | 0 |
| Roadmap item numbers cited outside a roadmap | 0 |
| Items claimed by two ledgers | 0 |
| Size signals | 8 |
| Source files with no interface stub | 0 |
| Directories holding too many files | 10 |
| Prose describing finished work | 0 |
| Unanswered scaffold placeholders | 0 |
| Doubt stores missing their own discipline | 0 |
| Ledgers naming a model where they mean a tier | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 0 |
| Constraints trapped in a CONTEXT.md head | 0 |
| Local branches holding unpromoted work | 2 |
| Work that exists on this disk and nowhere else | 1 |
| Local branches already merged into their base | 1 |
| Remote branches already merged into their base | 1 |

### Findings per code repo

*Each repo keeps its own `ISSUES.md` and fixes its own findings; this table only says which one to open next.*

| Repo | Findings |
|------|----------|
| [`academy/papers/2026-JBCS-relativistic_raytracer`](academy/papers/2026-JBCS-relativistic_raytracer/ISSUES.md) | 12 |
| [`academy/papers/2026-SIBGRAPI-relativistic_raytracer`](academy/papers/2026-SIBGRAPI-relativistic_raytracer/ISSUES.md) | 5 |
| [`academy/papers/2027-CHI-cria`](academy/papers/2027-CHI-cria/ISSUES.md) | 9 |
| [`academy/papers/2027-ICLR-dobra`](academy/papers/2027-ICLR-dobra/ISSUES.md) | 8 |
| [`academy/papers/ai4good`](academy/papers/ai4good/ISSUES.md) | 6 |
| [`academy/papers/mechanism-search`](academy/papers/mechanism-search/ISSUES.md) | 3 |
| [`academy/papers/mutual-credit-ai`](academy/papers/mutual-credit-ai/ISSUES.md) | 3 |
| [`academy/papers/pls-pix`](academy/papers/pls-pix/ISSUES.md) | 3 |
| [`academy/papers/spacemantics`](academy/papers/spacemantics/ISSUES.md) | 5 |
| [`academy/papers/wos-ablation`](academy/papers/wos-ablation/ISSUES.md) | 4 |
| [`branches/casinhas`](branches/casinhas/ISSUES.md) | 7 |
| [`branches/instituto`](branches/instituto/ISSUES.md) | 15 |
| [`code/aiwbot`](code/aiwbot/ISSUES.md) | 12 |
| [`code/apptime`](code/apptime/ISSUES.md) | 20 |
| [`code/corpora`](code/corpora/ISSUES.md) | 12 |
| [`code/cria`](code/cria/ISSUES.md) | 6 |
| [`code/dobra`](code/dobra/ISSUES.md) | 14 |
| [`code/flows`](code/flows/ISSUES.md) | 54 |
| [`code/freeai`](code/freeai/ISSUES.md) | 9 |
| [`code/gira`](code/gira/ISSUES.md) | 5 |
| [`code/isoroll-content`](code/isoroll-content/ISSUES.md) | 45 |
| [`code/isoroll-module`](code/isoroll-module/ISSUES.md) | 95 |
| [`code/laplata`](code/laplata/ISSUES.md) | 4 |
| [`code/obra`](code/obra/ISSUES.md) | 1 |
| [`code/ppc`](code/ppc/ISSUES.md) | 3 |
| [`code/spacemantics`](code/spacemantics/ISSUES.md) | 37 |
| [`code/voti`](code/voti/ISSUES.md) | 2 |
| **collected** | **422** |

### Off-allowlist `.md` types

*route via core/SCHEMA.md § four disposal routes*

Clean.

### CONTEXT.md hand-written inventories

*the routing block owns inventory*

Clean.

### Naming and placement

*kebab-case ASCII, types where their scope allows*

Clean.

### Routing tables pointing at files git does not carry

*a clone gets the table and not the file — track the target, or stop routing to it*

Clean.

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

- SETUP.md — 610 lines, over the 200 cap; introduced by 3e575bb lsfcin
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 274 lines, over the 200 cap; introduced by f05cac9 lsfcin
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 147)
- brain/INBOX.md — 4 line(s) over the 120-column cap (first at line 31)
- core/SCHEMA.md — 221 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/hooks/SPECS.md — 367 lines, over the 200 cap; introduced by 0237832 lsfcin
- core/refs/REFS.md — 2 line(s) over the 120-column cap (first at line 53)

### Source files with no interface stub

*the read gate only fires when a stub exists — a missing one turns it off silently*

Clean.

### Directories holding too many files

*splitting costs one hop — pay it only when it removes more table than it adds*

- academy/administration/coordenacao-lc/novo-ppc-bcc/ementas — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/entropy — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/routing — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/hooks — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/scripts — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/law/entropy — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace — 12 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 18 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/wos — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds

### Prose describing finished work

*git is the history — cut it, or rewrite it as present-tense state*

Clean.

### Unanswered scaffold placeholders

*a generator asked a question — answer it at the source, never by cutting the marker*

Clean.

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

Clean.

### Local branches holding unpromoted work

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/codex-and-inbox-wip is 3 ahead of main
- . — feature/roadmap-shape is 2 ahead of main

### Work that exists on this disk and nowhere else

*two machines share this workspace — push it, or give the repo a remote to push to: code/SPECS-git.md § Push policy*

- . — feature/roadmap-shape is 30 ahead of origin/feature/roadmap-shape

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 1 merged into main: git -C . branch -d feature/port-seams

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 2 merged into main: git -C . push origin --delete feature/port-seams feature/read-gate-close

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-02 · `verify.py full` · **green (1 passed, 695 deselected in 3.58s · 695 passed in 65.27s (0:01:05))**
<!-- verify:end -->
