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

- **The feature is called `bot` and the directory is called `code/aiwbot/`.** `core/tools/CONTEXT.md`
  says a family directory IS the feature, and this is the one crossing tree where the two spellings
  disagree — the registry dropped the vendor on 2026-09-17 and the directory kept it. What closes it
  is renaming the tree, 281 tracked paths and every pointer into them, which did not fit beside the
  crossing work. The rename is cheap to describe and expensive to do, which is exactly why it is
  written down rather than remembered.

- **`WARN_FILES` is a warning for a directory that already exists and a refusal for a new one.**
  `entropy_crowding.py` reads it as the signal and `BLOCK_FILES` as the cap, exactly as
  `limits.env` describes them — but `test_no_new_directory_exceeds_the_crowding_signal` ratchets on
  the WARN, so a directory crossing 10 fails the suite while `limits.env` says nothing stops until
  15. Both behaviours are defensible and the pair is not written down anywhere, so the number reads
  as one law and acts as two: it misled the agent AND Lucas in the same session, 2026-09-17, on
  `core/hooks/session/` at 11 files. Either the ratchet moves to `BLOCK_FILES`, or `limits.env` says
  that a NEW offender is held to the signal while an existing one is only asked to look.

- **The wiring check's name witness passes on any word the file already uses.**
  `test_features_wiring.py` asks `row['name'] not in path.read_text()` over RAW text, comments
  included — the same weakness that let `symmetry` pass on the word *asymmetry*. The `bot` row is
  the live case: the word is in every other line of `code/aiwbot/frontend/bot.py`, so that arm
  proves nothing for it, and only the behavioural arm beside it still does. Measured 2026-09-17:
  64 of the 68 wired points name themselves inside `require('<name>')` or `is_enabled('<name>')`,
  so demanding the QUOTED name would hold everywhere but the four `.sh` and `.js` points, which
  spell the call differently. The fix is one line plus a shape for those four. **A second live case
  on 2026-09-17**: the regression test forbidding `--no-verify` in `publish/repo` failed on the
  comment explaining the bypass it forbids. That one is fixed by stripping comments first, which is
  the same shape the fix above needs and is now written down in
  `core/tools/test/wos/test_b20260917_the_sync_never_finished_at_the_destination.py`.

- **Three private skills lost their switch, because a registry that crosses whole cannot name a
  file the clone does not have.** `foundry`, `iso-visual` and `prof` are Lucas's and must not reach
  the public repo (2026-09-17). Refusing them in `core/public.txt` is what actually stops the copy —
  but `core/features.txt` crosses verbatim, so a row left behind names a skill the clone lacks and
  the target's own suite refuses the sync commit, correctly. The rows came out instead, and the
  three are now unswitchable: `is_enabled` fails open, so they are permanently on, against
  `core/SPECS.md` § AD-14. **The fix is to filter the registry as it crosses** — drop the rows whose
  `ships` the floor refuses — which needs `_same()` to compare the target against the FILTERED text
  rather than the source, or the whole oscillation returns. `repo` is at 248 of 250 lines and
  `crossing.py` at 248, so it needs a cut first; `rebuild.py` is the natural home for the filter.

- **A file that BECOMES refused is never removed from the target, because the sync hides it from
  itself.** `_present()` asks the target's git what it holds and subtracts what the target's
  `.gitignore` ignores — and that `.gitignore` is written by this same tool from the `absent` list,
  so the moment a path is refused it stops being visible as an ORPHAN and the copy already on disk
  stays forever. Found 2026-09-17 by refusing `core/skills/prof`: twelve files had crossed one run
  earlier and no verdict mentioned them again. **Not a leak** — they are gitignored there, so
  `git add -A` skips them and nothing reaches the remote — but they sit in the working tree and
  would reappear the day the refusal moves. Same family as the `roots`-only exception bug fixed the
  same day: one `.gitignore` answering both *what git carries* and *what the sync owns*. The cure is
  to delete what the generated half of the ignore file names (the `absent` and orphan lines) while
  never touching what `IGNORE_HEAD` names, which is explicitly the list the sync must NOT delete.
  Cleaned by hand this time; `repo` is at 248 of 250 lines, so the fix needs a cut first.

- **`publish/repo --check` cannot see a stale generated block, and says `0 difference(s)` anyway.**
  `_same()` ignores generated blocks on purpose — the correct block genuinely differs between the
  two repos — so the comparison is silent about the one thing that drifted for weeks. The drift
  itself is fixed: `--sync` now runs the target's generators (`publish/rebuild.py`), so a block
  cannot go stale between syncs. What is still untrue is the REPORT: a target whose blocks were
  wrecked by something other than this tool still reads clean, and `/roundup`'s new `public:` line
  inherits that blind spot. The honest check is to regenerate and compare, which writes — so it
  belongs to `--sync`, not to `--check`, and the shape that resolves it is not yet chosen.

- **Prose that crossed still points at 30 files the public repo does not have.** Measured
  2026-09-17 over tracked `.md` in the clone, after the generated blocks were fixed (34 broken
  pointers there went to 5). These are in AUTHORED text, so no generator reaches them, and they
  split three ways: the refused trees a sentence promises anyway (`README.md` → `brain/`,
  `academy/`, `branches/`, `models/`; `SETUP.md` → `academy/SETUP.md`), his plans cited by machinery
  that crossed (`core/flows/craft/tree.md` → `code/ROADMAP-spec-drive.md`, `core/hooks/CONTEXT.md` →
  `code/ROADMAP-verify.md`), and goal files named by a `> goal:` header the routing generator then
  hoists (`core/flows/craft/` → `brain/goals/*`). The `.gitignore` the sync generates keeps the
  POINTER CHECK green by declaring each one deliberately absent, which is right for a checker and
  wrong for a student, who clicks and gets nothing. Each needs a sentence rewritten here or a file
  let across; neither is mechanical, which is why this is a list and not a fix.

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

2026-09-17 · 959 tracked files scanned · **3 findings here** (2026-09-05: 26 · -23 over 12 days)

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

- . — feature/bot-crossing is 6 ahead of main

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 3 merged into main: git -C . branch -d feature/hook-scoreboard feature/legibility-identifiers feature/roadmap-drain

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 3 merged into main: git -C . push origin --delete feature/hook-scoreboard feature/legibility-identifiers feature/roadmap-drain

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-17 · `verify.py full` · **green (25 passed, 936 deselected in 2.37s · 936 passed in 49.39s)**
<!-- verify:end -->
