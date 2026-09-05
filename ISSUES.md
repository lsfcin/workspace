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

**A second case, proven 2026-09-02:** `test_present_tense_state_is_not_a_corpse` died with
`FileNotFoundError` on `code/_nudgeprobe5b974581` — some test creates a probe directory
**inside the real `code/`** and deletes it, and a parallel worker walking that tree hit the gap. It
is a different shape from the first: that one mutated a tracked file's content, this one creates and
removes a real path, so a check that only watched tracked files would miss it. Two cases, two
shapes, from two of five full runs — the class is not a single offender and the marker cannot close
it.

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

2026-09-04 · 2406 tracked files scanned · **26 findings here** (2026-08-25: 33 · -7 over 10 days) · 399 more across 27 nested repos, each in its own ISSUES.md

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
| Size signals | 12 |
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
| **collected** | **425** |

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

- .zcode/SPECS.md — 1 line(s) over the 120-column cap (first at line 55)
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 274 lines, over the 200 cap; introduced by f05cac9 lsfcin
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 147)
- academy/talks/rva-chico/roteiro.md — 1 line(s) over the 120-column cap (first at line 3)
- brain/INBOX.md — 8 line(s) over the 120-column cap (first at line 13)
- brain/goals/craft-flows.md — 1 line(s) over the 120-column cap (first at line 41)
- core/SCHEMA.md — 221 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/flows/craft/tree.md — 1 line(s) over the 120-column cap (first at line 65)
- core/hooks/SPECS.md — 366 lines, over the 200 cap; introduced by 0237832 lsfcin
- core/refs/REFS.md — 2 line(s) over the 120-column cap (first at line 53)
- core/skills/install.md — 1 line(s) over the 120-column cap (first at line 22)

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
- core/tools/test/workspace — 13 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
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
- . — feature/zcode-wiring is 1 ahead of main

### Work that exists on this disk and nowhere else

*two machines share this workspace — push it, or give the repo a remote to push to: code/SPECS-git.md § Push policy*

Clean.

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 3 merged into main: git -C . branch -d feature/arvore-tecnologias feature/setup-shards feature/talk-rva-chico

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 3 merged into main: git -C . push origin --delete feature/arvore-tecnologias feature/setup-shards feature/talk-rva-chico

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-04 · `verify.py full` · **green (1 passed, 709 deselected in 2.98s · 709 passed in 47.38s)**
<!-- verify:end -->
