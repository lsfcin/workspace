# Git flow and the branch lock
> Which branches exist, who may write where, and how work reaches develop.
> governs: every repo that has a `develop` branch and an origin owned by the profile's `github-owner`
> enforced-by: core/hooks/git/lock.py, core/hooks/git/lock-gate.py, core/hooks/post-commit

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Releases only; moves by an explicit release, never by a close |
| `develop` | Integration and the sync point between machines; always green |
| `feature/<topic>-<MMDD>` | One session's work, created by the lock, merged back by the close |

**Scope is a fact of the repo, not a list** (ruled 2026-11-19, Lucas): a repo is governed when it has `develop` and its origin's GitHub owner is `github-owner` in `core/profile.txt`. A trunk repo (no `develop`: `brain/`, papers on Overleaf) and a clone of someone else's repo are never gated, merged or pushed.

## The branch is the lock

**The rules bind agents only; people are free** (Lucas, 2026-11-19). Every rule asks for a session id; a git hook run from a person's terminal has none and passes.

**One agent session per repo, one question per action: does it change the repo?** A read never asks. A change passes only for the holder. A governed repo on `develop` or `main` with a clean tree is free, and **a file write is the only way to take one**, all under one `flock`: fetch, fast-forward `develop`, create `feature/<topic>-<MMDD>`, write `core/state/lock_<repo>.txt` naming the session. A git command that changes a repo the session does not hold is refused, free repo included, because a branch made from the shell would have no owner. A repo on `feature/*` that no session holds belongs to nobody, and **`core/run tools/wos/claim <repo> --session <id>`** is the one way to hand a repo over, only on Lucas's explicit word. The holder's own move to another feature is followed. Leaving the feature for a shared branch is the close's job, never the holder's. Uncommitted changes on a free `develop` belong to nobody and stop the take: they are Lucas's to commit or stash.

**Enforced at two layers.** [`lock-gate.py`](lock-gate.py), run by `core/hooks/dispatch.py`, which every harness shim calls for writes and shell commands (`test_every_shim_routes_write_and_shell.py` proves all six). The pre-commit refuses an agent's commit on a shared branch (its session id from the shell environment). The gate fails open only on a crash, never on a refusal.

**No worktrees** (2026-11-19): one checkout per repo, held by one session at a time, is what makes the lock sufficient.

## Close

`core/run tools/wos/roundup` covers the repos this session holds. Dirty → exit 2. `origin/develop` is merged into the feature first, so the suite judges what `develop` will hold. Green → that exact commit is pushed as `develop` (origin refuses it if develop moved meanwhile, and the repo stays held), the feature is deleted. Red, or `--draft` → only the feature is pushed, unmerged. Either way, only after the push is confirmed against origin does the repo switch to `develop` and the lock drop; a failed push keeps it held. An unmerged feature is resumed only on Lucas's word (ruled 2026-11-19): the close's line says so and the handoff carries it. The close commits nothing: generated reports live in `outputs/state/`, never in git.

**Push policy.** Two machines share this workspace, so **unpushed work is invisible work**. Every commit in an owned repo auto-pushes (`core/hooks/post-commit`), except on `develop`/`main` of a governed repo: the close pushes `develop`, a release pushes `main`. A trunk repo such as `brain/` is pushed on every commit. No pull request is required and no branch is protected (2026-08-31): the green suite is the gate. `core/hooks/git/branch_debt.py` counts work no remote has.

**The `--no-verify` bypass leaves no trace** outside the commit message. When used: state the reason in the message and file the debt in the repo's `ISSUES.md`.
