# Workspace issues
> What is currently untrue that we know about: hand-written issues first, every measured number
> inside its own generated block.

The scope is the **workspace itself** — the enforcement layer, the tools, the structure. A bug in a
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

**An item ends with its id, and the id is what makes that sentence true** (2026-09-21). The gate
matched `## b<id>` headings and nothing else, which no list here has ever used — 937 runs, 0
blocks, while this head already claimed it governed the file. It reads bullets now, and it holds an
item to proof exactly when the item carries an id, so `b20260921` is what a spec filename has to
name. An entry without one is invisible to it.

## Open

- **`brain/INBOX.md` has many writers and no protocol, and the one that was caught losing captures
  is the one that could not defend itself.** The bot now locks the file, writes under the lock and
  reads the entry back before confirming (`f11a2334`), so a capture it cannot land raises instead of
  being confirmed. That is detection, not prevention: an agent session holding a read from minutes
  ago still rewrites the whole file and still wins, and nothing here asks it not to. The eight
  captures lost on 2026-09-20 were lost to exactly such a write — no commit in the window removed
  them, and the bot's writes were never committed, so which session did it is not recoverable.
  What is missing is the rule for THIS side: re-read before writing the capture file, or take the
  same lock. `b20260921-inbox-writers`

- **`core/tools/video/video` returns nothing for a link it cannot treat as media, and says `ok`.**
  A GitHub repository URL in the triage queue came back `[incomplete: ERROR: Unsupported URL]` and
  then `(no text extracted)` from the `fetch` fallback, which had reached the page and pulled only
  its sign-in chrome. The skill promises `fetch` as the fallback for a link carrying no media, so a
  ref would have been routed on nothing; the content was three seconds away at the raw README. Two
  halves: the fallback does not follow a code host to a readable surface, and a link that yielded no
  text is still counted in the `ok` column, which is the false green these checks exist to end.
  `b20260921-fetch-fallback`

- **The template-naming law is written and nothing enforces it, which is the defect `core/SPECS.md`
  § AD-16 names.** The rule landed in `core/SCHEMA.md` on 2026-09-18, in the section
  *A leading underscore marks a shape, never an instance*, after four separate modules were found
  reading that underscore and none of them stating it. The rule is now induced wearing the costume of enforced: no check fails a template
  directory that skips the marker, and one already does —
  `academy/teaching/structure/templates/`. That tree settled on 2026-09-20 and the rename is now
  unblocked, so what is left is the half that was always the harder one: decide whether the rule
  earns a check at all. **It may not.** The four
  mechanisms already behave correctly on a directory without the marker — they simply treat its
  contents as instances, which is the right answer for every directory except a template one, and
  the count of those in this workspace is three. `b20260918-template-naming`

- **Two sessions share one index and one suite, so either can hold the other's commits hostage for
  as long as it is mid-edit.** The question the 2026-09-18 `--no-verify` bypass exposed, and no rule
  answers. The bypass itself is paid — the suite is green at 950 — and how it was paid is the
  argument: neither failure it named survived contact. One was a CHECK BUG in this repo, not the
  other session's tree (a staged delete leaves `w/` empty and the worktree arm read blank as CRLF,
  so three deleted files were reported as CRLF). The other was two untracked routing targets, and
  **one of the two was this session's own**, mis-attributed to the parallel tree by the handoff
  that read the failure without opening it. A failure blamed on a tree nobody may touch is a
  failure nobody diagnoses; that is what the shared index costs, more than the blocked commit.
  **And the bypass left a trace nobody saw for three days**: `core/refs/REFS.md` crossed
  `BLOCK_CHARS` in that same commit and sat 100-200 over it for three commits, until a session
  happened to edit the file and was refused. The cap is enforced on what a commit STAGES, so a file
  that gets over it once stays over until someone touches it — which is the whole cost of
  `--no-verify`, and the part the protocol does not ask anyone to check afterwards.
  `b20260918-shared-index`

- **The other machine's scoreboard still records three features under names nothing answers to.**
  Renaming a feature renames its key in `core/features.txt`, and the scoreboard is an append-only
  log keyed by that name — so 524 rows written before 2026-09-20 say `inbox-nudge`,
  `compass-nudge`, `publish-nudge`. This machine's copy was migrated with the rename and lost
  nothing; the file is gitignored and per-machine, so the other one was not, and the two-week
  reading due 2026-09-28 will show those three at zero there. The substitution is one line and
  anyone can run it, which is why this is a note and not a tool. **The asymmetry is the finding**:
  a feature's name is versioned and its measurements are not, so every future rename silently
  costs history on every machine that is not the one doing the renaming. `b20260920-scoreboard-keys`

- **A nested repo's entropy report only refreshes when someone commits in that repo, so a quiet one
  ages with nothing saying so.** The close runs the dashboard on this repo alone, by design (one
  repo per run, ruled 2026-09-04), and the only other trigger is that repo's own pre-commit. Found
  2026-09-20: a one-word pointer fix in `academy/papers/ai4good/` regenerated a block dated
  2026-09-04 and it moved 6 findings → 8, none of them caused by that commit. Seventeen days of
  drift were invisible because nothing had been committed there. Same class as the branch-list
  entry below — a report read as current while nothing says how old it is — and here the date IS
  printed, which is the cheap half already done. The missing half is anything that reads it.
  `b20260920-quiet-repo-entropy`

- The entropy block's *"safe to delete, and outward-facing"* branch list is a SNAPSHOT presented as
  a standing instruction, and it goes stale inside the session that reads it. Found 2026-09-14 by
  nearly running it: the block named `feature/legibility-identifiers` among three branches merged
  into `main`, but two commits had since landed on it — the post-commit auto-push had carried them
  to the remote, so the command the report offered would have deleted unmerged work. The report is
  regenerated at close and read at open, which is exactly the window auto-push writes into. Nothing
  in the line says how old it is. Two cures, and they compose: re-check `git merge-base
  --is-ancestor origin/<branch> origin/main` at the moment of deletion rather than trusting the
  block, and have `branch_debt.py` exclude any branch whose tip this session moved. The first is
  what saved it by hand this time. `b20260914-branch-list-snapshot`

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
  it corrects the registry, it does not unblock anything. `b20260915-feature-names-carry-vendors`

- **The feature is called `bot` and the directory is called `code/aiwbot/`.** `core/tools/CONTEXT.md`
  says a family directory IS the feature, and this is the one crossing tree where the two spellings
  disagree — the registry dropped the vendor on 2026-09-17 and the directory kept it. What closes it
  is renaming the tree, 281 tracked paths and every pointer into them, which did not fit beside the
  crossing work. The rename is cheap to describe and expensive to do, which is exactly why it is
  written down rather than remembered. `b20260917-bot-directory-keeps-vendor`

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
  `b20260917-private-skills-unswitchable`

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
  `b20260917-refused-file-never-removed`

- **`publish/repo --check` cannot see a stale generated block, and says `0 difference(s)` anyway.**
  `_same()` ignores generated blocks on purpose — the correct block genuinely differs between the
  two repos — so the comparison is silent about the one thing that drifted for weeks. The drift
  itself is fixed: `--sync` now runs the target's generators (`publish/rebuild.py`), so a block
  cannot go stale between syncs. What is still untrue is the REPORT: a target whose blocks were
  wrecked by something other than this tool still reads clean, and `/roundup`'s new `public:` line
  inherits that blind spot. The honest check is to regenerate and compare, which writes — so it
  belongs to `--sync`, not to `--check`, and the shape that resolves it is not yet chosen.
  `b20260917-check-blind-to-stale-block`

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
  `b20260917-crossed-prose-broken-pointers`

- **The read gate charges a session twice for one enforcement layer.** `code/wos` now holds 81
  `CONTEXT.md` byte-identical to this repo's, and the gate keys on the PATH, so a session that has
  oriented in `core/tools/wos/publish/` here is refused again the moment its working directory is
  the target — it cost eight refusals in the session that built it, each one a re-read of prose
  already in the window. The gate is right that they are different subtrees and wrong that they are
  different CONTENT. Cheapest cure: treat a path under a one-way sync target as already-read when
  its source was, which `core/public.txt` can already answer. Found 2026-09-16.
  `b20260916-read-gate-charges-twice`

- **`opencode-plugin` and `antigravity-hooks` spell harnesses a fourth way.** `core/harnesses.txt`
  names them `opencode`, `claude`, `zcode`, `agents`; `antigravity` appears in neither that file nor
  any directory, where the shim actually lives at `core/hooks/antigravity/`. One of the two names
  the mechanism, the other names a vendor, and `features.txt`'s own header says its job is to
  reconcile existing vocabularies rather than invent another. Found alongside the entry above.
  `b20260916-harness-names-four-ways`

- `core/tools/paper/papers` has no working arm: Semantic Scholar returns HTTP 429 and arXiv times
  out, both re-confirmed 2026-09-13. The tool itself is honest — it prints `{"error": ...}` to
  stderr and exits 1 — and the cause is outside this workspace, so nothing here can fix it. What
  was ours is fixed: `deps` now declares both services with a check that CALLS them, so the miss
  reports red instead of the green it read while a whole research run went around the tool, and the
  `sota` and `scout` flows name the fallback that worked (`core/tools/web/search` aimed at venue
  hosts) rather than only the tool. Still open because the capability is still gone: a run pays for
  it by establishing `venue`, `peer_reviewed` and `citations` one fetched page at a time. Worth
  re-checking before any research run, and worth a second provider if it stays down.
  `b20260913-paper-search-has-no-arm`

- **Three stores hold per-machine counts and each ages by a different law, which is one law too
  many.** `core/scoreboard.tsv` is append-only and never collapses — **5.8 MB on 2026-09-22**, ten
  days after it started, and nothing in its design stops that. `core/read-matrix.tsv` holds the
  same kind of fact in a fixed window that cannot grow, because a column is a day modulo 365. The
  session marker stores under `core/state/` are the third, aged by a two-day prune that became
  load-bearing the moment they stopped living somewhere the operating system emptied. All three
  answer *what did this machine do*, and there is no reason for three answers to how such a fact
  gets old — the matrix's window is the one that was designed rather than inherited, and it is the
  shape the other two should take. **Not before 2026-09-29**: the scoreboard owes its first reading
  on 2026-09-28 (`ROADMAP.md` § Measurement), and changing how it stores rows before it is read
  would spend the measurement to tidy the file it is measured from.
  `b20260922-state-stores`

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans this repo and no other. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-09-22 · 977 tracked files scanned · **3 findings here** (2026-09-11: 2 · +1 over 11 days)

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
| Unanswered placeholders | 0 |
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

- . — feature/agnostic-read-measurement is 3 ahead of main

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 7 merged into main: git -C . branch -d feature/bot-crossing feature/checker-honesty feature/hook-scoreboard feature/inbox-capture-honesty feature/legibility-identifiers feature/roadmap-drain feature/word-retirement

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 7 merged into main: git -C . push origin --delete feature/bot-crossing feature/checker-honesty feature/hook-scoreboard feature/inbox-capture-honesty feature/legibility-identifiers feature/roadmap-drain feature/word-retirement

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-09-21 · `verify.py full` · **green (25 passed, 950 deselected in 2.52s · 950 passed in 54.83s)**
<!-- verify:end -->
