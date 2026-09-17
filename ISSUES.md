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

## Open

- The entropy block's *"safe to delete, and outward-facing"* branch list is a SNAPSHOT presented as
  a standing instruction, and it goes stale inside the session that reads it. Found 2026-09-14 by
  nearly running it: the block named `feature/legibility-identifiers` among three branches merged
  into `main`, but two commits had since landed on it — the post-commit auto-push had carried them
  to the remote, so the command the report offered would have deleted unmerged work. The report is
  regenerated at close and read at open, which is exactly the window auto-push writes into. Nothing
  in the line says how old it is. Two cures, and they compose: re-check `git merge-base
  --is-ancestor origin/<branch> origin/main` at the moment of deletion rather than trusting the
  block, and have `branch_debt.py` exclude any branch whose tip this session moved. The first is
  what saved it by hand this time.

- **`ISSUES.md` is invisible to both size numbers while being one of the most read files in the
  workspace.** `core/hooks/generated.txt` declares every `ISSUES.md` generated, which is right for
  the authoring rules — the blocks inside it really are written by a tool — and it also drops the
  file out of `core/run tools/wos/size` entirely, corpus and weight alike. Found 2026-09-15 when the
  weighted ranking was first read and this file was missing from it at 52.8 lines served per
  session, which would have placed it fifth. The hand-written half is authored prose and is charged
  to nobody. The asymmetry, not the exemption, is the bug: a file can be exempt from a RULE without
  being exempt from a MEASUREMENT, and `size` conflates the two by reading one list for both.

- **Seven feature names disobey the rule their own tools live under.** `core/tools/CONTEXT.md`
  says the family directory is the feature and the file is the provider — function in the
  directory, vendor at the leaf — and the registry then spells the same features `google-auth`,
  `notes-notion`, `link-shortener`, `wazip`, `video-text`, `asset-inspect` and
  `vpn-cin`, while the directories are already `auth/`, `notes/`, `links/`, `chat/`,
  `video/`, `assets/` and none. Found 2026-09-15 by Lucas, from `vpn-cin` carrying an institution
  inside a directive. `forms/gforms` is the row that already obeys, so the fix is to DROP the
  vendor, never to spread it — and a skill takes the FAMILY name too (Lucas, 2026-09-16), which is
  how `core/skills/gmail.md` became `mail.md`. **The eighth was paid that day, and how is the
  pattern for the rest**: `mail-triage` → `mail` collided with the skill row `gmail`, because the
  tool half and the skill half of ONE capability were two rows. They merged into one `tools+skills`
  row, the shape `forms` already had — so the sweep PAYS rows rather than spending them.
  **One of the seven cannot be fixed the obvious way**: `link-shortener`
  → `links` collides with the norm named `links`, which owns the name by the same law
  (`core/norms/links.md`), and the registry key set is flat. That collision is the asymmetry worth
  writing down — two namespaces share one key space, and `group` already distinguishes them
  everywhere else. The other six ripple into `SETUP-accounts.md`'s `> feature:` lines, the
  `install` column, `core/tools/deps.txt` and `core/profile.txt` through the three-way join, and
  each pays a `core/SCHEMA.md` § Retired tokens row. Deferred from the session that found it:
  it corrects the registry, it does not unblock anything.

- **The read gate charges a session twice for one enforcement layer.** `code/wos` now holds 81
  `CONTEXT.md` byte-identical to this repo's, and the gate keys on the PATH, so a session that has
  oriented in `core/tools/wos/publish/` here is refused again the moment its working directory is
  the target — it cost eight refusals in the session that built it, each one a re-read of prose
  already in the window. The gate is right that they are different subtrees and wrong that they are
  different CONTENT. Cheapest cure: treat a path under a one-way sync target as already-read when
  its source was, which `core/public.txt` can already answer. Found 2026-09-16.

- **`opencode-plugin` and `antigravity-hooks` spell harnesses a fourth way.** `core/harnesses.txt`
  names them `opencode`, `claude`, `zcode`, `agents`; `antigravity` appears in neither that file nor
  any directory, where the shim actually lives at `core/hooks/antigravity/`. One of the two names
  the mechanism, the other names a vendor, and `features.txt`'s own header says its job is to
  reconcile existing vocabularies rather than invent another. Found alongside the entry above.

- `core/tools/paper/papers` has no working arm: Semantic Scholar returns HTTP 429 and arXiv times
  out, both re-confirmed 2026-09-13. The tool itself is honest — it prints `{"error": ...}` to
  stderr and exits 1 — and the cause is outside this workspace, so nothing here can fix it. What
  was ours is fixed: `deps` now declares both services with a check that CALLS them, so the miss
  reports red instead of the green it read while a whole research run went around the tool, and the
  `sota` and `scout` flows name the fallback that worked (`core/tools/web/search` aimed at venue
  hosts) rather than only the tool. Still open because the capability is still gone: a run pays for
  it by establishing `venue`, `peer_reviewed` and `citations` one fetched page at a time. Worth
  re-checking before any research run, and worth a second provider if it stays down.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans this repo and no other. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-17 · 941 tracked files scanned · **3 findings here** (2026-09-05: 27 · -24 over 12 days)

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
| Items claimed by two lists | 0 |
| Size signals | 0 |
| Source files with no interface stub | 0 |
| Directories holding too many files | 0 |
| Prose describing finished work | 0 |
| Unanswered scaffold placeholders | 0 |
| Doubt stores missing their own discipline | 0 |
| Lists naming a model where they mean a level | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 0 |
| Constraints trapped in a CONTEXT.md head | 0 |
| Local branches holding unpromoted work | 1 |
| Work that exists on this disk and nowhere else | 0 |
| Local branches already merged into their base | 1 |
| Remote branches already merged into their base | 1 |

*A check with no findings is the `0` in that table and nothing more. Only a check with something to show gets a section below.*

### Local branches holding unpromoted work

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/roadmap-drain is 4 ahead of main

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 2 merged into main: git -C . branch -d feature/hook-scoreboard feature/legibility-identifiers

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 2 merged into main: git -C . push origin --delete feature/hook-scoreboard feature/legibility-identifiers

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-17 · `verify.py full` · **green (25 passed, 925 deselected in 2.74s · 925 passed in 51.87s)**
<!-- verify:end -->
