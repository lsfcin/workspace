# Git flow and the branch lock
> Which branches exist, who may write where, and how work reaches develop.
> governs: every repo that has a `develop` branch and an origin owned by the profile's `github-owner`
> enforced-by: core/hooks/git/lock.py, core/hooks/git/lock-gate.py, core/hooks/post-commit

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Releases only; moves by an explicit release, never by a close |
| `develop` | Integration and the sync point between machines; always green |
| `feature/<name>` | One session's work, named by `wos/take`, merged back by the close |

**Scope is a fact of the repo, not a list** (ruled 2026-11-19, Lucas): a repo is governed when it has `develop` and its origin's GitHub owner is `github-owner` in `core/profile.txt`. A trunk repo (no `develop`: `brain/`, papers on Overleaf) and a clone of someone else's repo are never gated, merged or pushed.

## The branch is the lock

**The rules bind agents only; people are free** (Lucas, 2026-11-19). Every rule asks for a session id; a git hook run from a person's terminal has none and passes.

**One agent session per repo, one question per action: does it touch the checkout** — HEAD, the index or the files, the one thing two sessions on one clone can clobber? A read, or a git call that moves only refs or the remote (`fetch`, `push`, `tag`, `branch`, save the forms that reach HEAD), never asks, so a release needs no lock (2026-11-23). Anything else, a verb the gate does not know included, passes only for the holder. A governed repo on `develop` or `main` with a clean tree is free, and **`core/run tools/wos/take <repo> <name>` is the only way to take one** (2026-11-23: the branch says its work, so a write to a free repo is refused until the session names it), all under one `flock`: fetch, fast-forward `develop`, create `feature/<name>`, write `core/state/lock_<repo>.txt` naming the session. A name is `[a-z0-9-]`, the ROADMAP or ISSUES id when one fits, no date, counter or folder; one already used, here or on origin, is refused. A git command that touches the checkout of a repo the session does not hold is refused, free repo included, because a checkout moved from the shell would have no owner. A repo on `feature/*` that no session holds belongs to nobody, and **`core/run tools/wos/claim <repo> [<name>] --session <id>`** is the one way to hand a repo over, only on Lucas's explicit word; with a name it switches a clean tree to `feature/<name>`, from origin if only origin has it. The holder's own move to another feature is followed. Leaving the feature for a shared branch is the close's job, never the holder's. Uncommitted changes on a free `develop` belong to nobody and stop the take: they are Lucas's to commit or stash.

**A shell write meets the lock an Edit does** (Lucas, 2026-11-23, panel argon). `lock-gate.py` refuses one its text shows — a redirect outside quotes, `tee`, `sed -i`, `python -c`, an interpreted heredoc — into a repo the session does not hold; a git-ignored path dirties no tree and passes, by Edit or shell alike (`lock.ignored`: the symlink's target, the innermost repo, never a `lock_*` file). No text shows every write, so [`dirt.py`](dirt.py) compares `git status` before and after each shell call on the free repos the command names: what turned dirty is that session's, which may `take` the repo carrying it when every dirty path is its own, or `git restore` it. Anyone else still meets dirt that belongs to nobody. A `cd` or `-C` to a variable the command never sets fails open.

**Enforced at two layers.** [`lock-gate.py`](lock-gate.py), run by `core/hooks/dispatch.py`, which every harness shim calls for writes and shell commands (`test_every_shim_routes_write_and_shell.py` proves all six). The pre-commit refuses an agent's commit on a shared branch (its session id from the shell environment). The gate fails open only on a crash, never on a refusal.

**A repo moves through `core/run tools/wos/move FROM TO`** (2026-11-24): the lock is keyed by the path, so the move re-keys the lock and dirt files under both flocks, and `lock-gate.py` refuses a raw `mv` of a governed root with that command.

**No worktrees** (2026-11-19): one checkout per repo, held by one session at a time, is what makes the lock sufficient.

## Close

`core/run tools/wos/roundup` covers the repos this session holds. Dirty → exit 2. `origin/develop` is merged into the feature first, so the suite judges what `develop` will hold. Green → that exact commit is pushed as `develop` (origin refuses it if develop moved meanwhile, and the repo stays held), the feature is deleted. Red, or `--draft` → only the feature is pushed, unmerged. Either way, only after the push is confirmed against origin does the repo switch to `develop` and the lock drop; a failed push keeps it held. An unmerged feature is resumed only on Lucas's word (ruled 2026-11-19): the close's line says so and the handoff carries it. The close commits nothing: generated reports live in `outputs/state/`, never in git.

**Push policy.** Two machines share this workspace, so **unpushed work is invisible work**. Every commit in an owned repo auto-pushes (`core/hooks/post-commit`), except on `develop`/`main` of a governed repo: the close pushes `develop`, a release pushes `main`. A trunk repo such as `brain/` is pushed on every commit. No pull request is required and no branch is protected (2026-08-31): the green suite is the gate. `core/hooks/git/branch_debt.py` counts work no remote has.

**The `--no-verify` bypass leaves no trace** outside the commit message. When used: state the reason in the message and file the debt in the repo's `ISSUES.md`.
