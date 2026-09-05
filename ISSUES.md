# Workspace issues
> What is currently untrue that we know about: hand-written issues first, every measured number
> inside its own generated block.

The scope is the **workspace itself** — the enforcement layer, the tools, the scaffold. A bug in a
project under `code/` belongs to that project's own `ISSUES.md`, and **the block below counts this
repo alone** (ruled 2026-09-04): those projects are separate repos this one's git ignores, so a
count of them was a fact about one machine's disk rather than about the workspace, and the same
commit read green on the clone that wrote it and red on the other. Each project counts itself, at
its own commit; where each one lives is [`PROJECTS.md`](PROJECTS.md).

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

## b20260905-every-tool-call-now-pays-for-every-gate

**Symptom:** the `PreToolUse` matchers became `.*` on 2026-09-04, so all nine gates spawn on every
tool call. One spawn costs ~54 ms measured here (three runs of `heredoc-gate.py` through
`core/run`, 0.161 s), which puts a full call at ~0.48 s of hook time. A `Read` paid two gates
before (~0.11 s) and a `Bash` three; `Read` is also the most frequent call a session makes.

**Why it matters:** the widening is right and is not in question — it is what closed
`b20260901-a-second-shell-tool-walks-past-every-read-gate`, where naming tools left the enforcement
layer silently weaker on Windows. What is wrong is paying for it seven times per read. A gate whose
first act is to return 0 still costs a process, an interpreter start and the law files it imports,
and this workspace's own `ROADMAP.md` § Cost is the ledger that says such a price must be visible.

**Root cause:** every gate is registered as its own `command`, so the capability question is asked
nine times per call instead of once. The shape of the fix is one dispatcher that reads stdin,
computes `hook_input.capability` once, and calls the gates that capability selects in-process —
which is also what would let a gate stop paying its own interpreter start. Not costed yet: whether
the dispatcher can keep each gate's exit-2-with-its-own-message contract
([`core/hooks/SPECS.md`](core/hooks/SPECS.md)) is the open question, and that contract is load-bearing.

## b20260905-the-cost-line-prices-every-session-at-opus-rates

**Symptom:** the `cost:` line every `/roundup` prints names the model and the dollars from the
transcript's own stamp. A session run through ZCode on **GLM-5.3-flash** logged all 70 assistant
lines as `"model":"claude-opus-5"` — the harness writes that stamp regardless of what answered —
and `core/tools/wos/session/usage` priced it through `session_cost.py`'s `RATES` ($5/$25 per Mtok).
Found 2026-09-04 by the session that ran it.

**Why it matters:** [`ROADMAP.md`](ROADMAP.md) § Cost is the ledger that says a session must report
what it cost, and the number it reports is fiction whenever the model is not an Anthropic one. Turn
and token counts are probably fine; the attribution and the dollars are not. It is also the shape
this workspace forbids twice over — a measured number nobody can check, and a provider's stamp
trusted as fact in a tree whose norm is provider-agnostic.

**Root cause:** `usage` reads the stamp and never asks whether it can be believed. The fix is a
decision: price an unknown or untrusted stamp at zero and print `unpriced`, or make the workspace
own the model attribution rather than the transcript. **Lucas's call.** Recorded here 2026-09-05
because it had been living only in `outputs/handoff.md`, which is gitignored and overwritten every
close — a bug filed in a scratch file is a bug that dies at the next session.

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

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans this repo and no other. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-05 · 700 tracked files scanned · **27 findings here** (2026-08-25: 33 · -6 over 11 days)

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
| Constraints trapped in a CONTEXT.md head | 1 |
| Local branches holding unpromoted work | 2 |
| Work that exists on this disk and nowhere else | 0 |
| Local branches already merged into their base | 1 |
| Remote branches already merged into their base | 1 |

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
- brain/INBOX.md — 8 line(s) over the 120-column cap (first at line 27)
- brain/goals/craft-flows.md — 1 line(s) over the 120-column cap (first at line 41)
- core/SCHEMA.md — 222 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/flows/craft/tree.md — 1 line(s) over the 120-column cap (first at line 65)
- core/hooks/SPECS.md — 376 lines, over the 200 cap; introduced by 0237832 lsfcin
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
- core/tools/test/workspace — 14 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 19 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
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

- core/hooks/entropy/dashboard/CONTEXT.md: head is 425 tok carrying 3 constraint(s).

### Local branches holding unpromoted work

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/codex-and-inbox-wip is 3 ahead of main
- . — feature/pending-decisions is 1 ahead of main

### Work that exists on this disk and nowhere else

*two machines share this workspace — push it, or give the repo a remote to push to: code/SPECS-git.md § Push policy*

Clean.

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 4 merged into main: git -C . branch -d feature/arvore-tecnologias feature/setup-shards feature/talk-rva-chico feature/zcode-wiring

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 4 merged into main: git -C . push origin --delete feature/arvore-tecnologias feature/setup-shards feature/talk-rva-chico feature/zcode-wiring

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-05 · `verify.py full` · **green (1 passed, 738 deselected in 1.08s · 738 passed in 31.45s)**
<!-- verify:end -->
