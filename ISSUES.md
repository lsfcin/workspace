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

**Second report, Lucas 2026-09-05:** the closing cost message is *fixed* on saying the model is
opus-5, and the value printed also looks wrong. Same root cause — the harness's stamp trusted as
fact — now confirmed visible in the user-facing line, not only in the transcript.

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

## b20260905-hooks-and-tools-suspected-of-paying-more-time-than-needed

**Symptom:** Lucas's strong suspicion (2026-09-05, unmeasured) that our hooks and maybe tools
consume far more time than they need — "honestamente, acho difícil acreditar que seja algo normal" —
and the problem seems worse on the Windows clone. Suspected, not proven: no number exists yet, and
this file records what is untrue that we *know*, so the first work is the measurement.

**Why it matters:** every gated tool call pays the hooks' latency, so a per-call overhead multiplies
across a whole session; and if Windows pays more than Linux, the two clones have systematically
different session economics that no check sees.

**Root cause:** unmeasured. Candidate shape: one dispatcher per PreToolUse gate was already the
2026-09-04 fix (bf46b96), but interpreter startup per invocation — `core/run` resolving the
interpreter on every call — is the obvious next suspect.

## b20260905-brain-drafts-carries-two-asymmetries

**Symptom:** found 2026-09-01 by the metodologia-aulas session and left unfixed. (1) `brain/drafts/`
has no `CONTEXT.md`, is absent from `brain/CONTEXT.md`'s routing, and therefore never entered the
`.gitignore` (`brain/*`) exception list — the four class-methodology drafts are outside git, and the
only copy is the disk. (2) Those drafts carry provider names in their filenames (`-sonnet`,
`-gemini`, `-opus`), against the provider-agnostic naming norm; here the provider *is* the data (a
blind three-way experiment), which the norm has no written exception for.

**Why it matters:** (1) is a real data-loss exposure — work existing on one disk only; (2) spreads a
naming pattern before the rule decides whether it is legal, and `SCHEMA.md` owns naming law.

**Root cause:** each is a decision Lucas has not made: drafts becomes a real subtree (CONTEXT.md +
ignore exception) or is declared ephemeral in writing; the norm gains a written exception for
comparative experiments, or the three files become `-a/-b/-c` with the provider named inside.
Decide before the pattern spreads.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans this repo and no other. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-05 · 706 tracked files scanned · **26 findings here** (2026-08-25: 33 · -7 over 11 days)

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
| Size signals | 11 |
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

*A check with no findings is the `0` in that table and nothing more. Only a check with something to show gets a section below.*

### Size signals

*a signal for review, never a cap — do not summarize to fit*

- .zcode/SPECS.md — 1 line(s) over the 120-column cap (first at line 55)
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 274 lines, over the 200 cap; introduced by f05cac9 lsfcin
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 147)
- academy/talks/rva-chico/roteiro.md — 1 line(s) over the 120-column cap (first at line 3)
- brain/INBOX.md — 1 line(s) over the 120-column cap (first at line 26)
- brain/goals/craft-flows.md — 1 line(s) over the 120-column cap (first at line 41)
- core/SCHEMA.md — 222 lines, over the 200 cap; introduced by 5c22650 lsfcin
- core/SPECS.md — 266 lines, over the 200 cap; introduced by 4c3d952 lsfcin
- core/flows/craft/tree.md — 1 line(s) over the 120-column cap (first at line 65)
- core/refs/REFS.md — 2 line(s) over the 120-column cap (first at line 53)
- core/skills/install.md — 1 line(s) over the 120-column cap (first at line 22)

### Directories holding too many files

*splitting costs one hop — pay it only when it removes more table than it adds*

- academy/administration/coordenacao-lc/novo-ppc-bcc/ementas — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/entropy — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/routing — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/hooks — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/scripts — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/law/entropy — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace — 14 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 20 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/wos — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds

### Constraints trapped in a CONTEXT.md head

*the only enforced-read type — move the contract to a sibling SPECS.md*

- core/hooks/entropy/dashboard/CONTEXT.md: head is 425 tok carrying 3 constraint(s).

### Local branches holding unpromoted work

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/codex-and-inbox-wip is 3 ahead of main
- . — feature/pending-decisions is 5 ahead of main

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
