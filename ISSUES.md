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

## b20260901-a-mirror-never-reaches-the-machine-that-pulled-it

**Symptom:** the Windows clone had **no skill mirrors at all** — none of the four harnesses — so no
`/inbox`, `/compass`, `/roundup`, `/craft` or `/install` existed on it. Every source was present and
every check that could run said nothing. Found 2026-09-01 after a session of work on the other
machine.

**Root cause, and it is a premise rather than a bug in any file.** The ruling that let the mirrors
leave git is written in [`core/hooks/postedit/sync.sh`](core/hooks/postedit/sync.sh): *generated
content may be untracked provided regeneration is automatic*. The same comment enumerates where that
happens — install, edit, create, and delete one commit behind. **Every one of those moments belongs
to the machine that AUTHORS.** None belongs to the machine that RECEIVES. Skills are edited on one
machine, arrive on the other as sources by `git pull`, and nothing there regenerates the copies, so
the premise holds on exactly half of a two-machine workspace.

`.claude/settings.local.json` is the same class and has no trigger at all — only the manual
`permissions --set`. It was also out of sync on this clone, for the same reason.

**The fix, decided 2026-09-01 (Lucas): a `SessionStart` hook**, not a git `post-merge`. Both would
run on the receiving machine, so that is not the discriminator; the consumer of a mirror is the
**session**, and a pull that happens while a session is open is a change that arrives after the
harness has already read its skill list. It regenerates the skills in silence and prints one line
only when it changed something; permissions it reports rather than writes, because a permission
level arriving over the network should not apply itself.

**Blocked on** [[b20260901-a-bash-tool-costs-thirty-seconds-a-commit-here]] — the check the hook
would call takes 22 s here, and a SessionStart hook may not.

## b20260901-a-bash-tool-costs-thirty-seconds-a-commit-here

**Symptom, measured 2026-09-01 on the Windows clone:** `sync-skills --check` takes **22 s** with the
mirrors in sync, and 16 s with them absent. `core/hooks/commit/generators.py` § `skills` runs the
tool **twice** — regenerate, then `--check` — so **every commit that touches a skill pays ~30 s**,
and every skill edit pays ~16 s through the post-edit hook. Nobody had measured it, and on Linux
nobody would feel it.

**Root cause: `fork`, not work.** 100 forks of `cmp` under Git Bash cost **4.8 s** here — ~48 ms
each, some 50x the Linux cost — and the tool spends ~300 of them: `basename` per skill per mirror,
`cmp` per copy, `grep` per frontmatter field, and one whole **Python interpreter per command file**
inside `render_command`. One Python process hashing all 17 sources costs 250 ms including startup.

**Why it is the workspace's own thesis:** *"porting bash to Python removes the per-OS axis"*
(`test_port_ratchet.py`). These two are the last bash tools in `core/tools/`, which is the half of
B12 that was left undecided — the launcher learned to dispatch on the shebang, and *why these two
are still bash* never got an answer.

**The fix:** port `sync-skills`, `skills/mirror.sh` and `skills/validate.sh` to Python. It also
deletes the `bash …` exception from [`SETUP.md`](SETUP.md) rather than documenting it. **The risk is
the reason it is written down instead of done in a hurry:** `validate.sh` blocks every commit in
both clones, and its loop-cap and DAG rules are regex-subtle. Land it behind an equivalence check —
run both implementations over the same tree and diff the outputs — before deleting the bash.

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

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans the whole tree. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-01 · 2385 tracked files scanned · **20 findings here** (2026-08-25: 33 · -13 over 7 days) · 399 more across 27 nested repos, each in its own ISSUES.md

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
| Work that exists on this disk and nowhere else | 0 |
| Local branches already merged into their base | 0 |
| Remote branches already merged into their base | 0 |

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
| **collected** | **419** |

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

- SETUP.md — 605 lines, over the 200 cap; introduced by 3e575bb lsfcin
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 274 lines, over the 200 cap; introduced by f05cac9 lsfcin
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 147)
- brain/INBOX.md — 1 line(s) over the 120-column cap (first at line 19)
- core/SCHEMA.md — 220 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/hooks/SPECS.md — 361 lines, over the 200 cap; introduced by 0237832 lsfcin
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
- core/tools/test/workspace — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 13 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
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
- . — feature/roadmap-shape is 8 ahead of main

### Work that exists on this disk and nowhere else

*two machines share this workspace — push it, or give the repo a remote to push to: code/SPECS-git.md § Push policy*

Clean.

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

Clean.

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

Clean.

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-01 · `verify.py full` · **green (662 passed in 66.52s (0:01:06))**
<!-- verify:end -->
