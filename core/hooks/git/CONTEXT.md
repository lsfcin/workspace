# git
> Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Which branches exist, who may write where, and how work reaches develop. |
| [`branch_debt.py`](branch_debt.py) | [`branch_debt.pyi`](branch_debt.pyi) | `repos`, `unmerged_branches`, `merged_local_branches`, `unpushed_work`, `merged_remote_branches` | What the entropy dashboard counts about branches: work that lives in only one place, and labels whose commits already landed. |
| [`dirt.py`](dirt.py) | [`dirt.pyi`](dirt.pyi) | `expand`, `owners`, `free`, `dirty`, `places` | PreToolUse and PostToolUse shell — who dirtied a free repo: what a shell call leaves dirty in a governed repo nobody holds is the session's that ran it. |
| [`git`](git) | — | — | git, through the branch lock: an agent's call that would touch a repo's checkout is asked first; a person's never is. |
| [`gitignore_heal.py`](gitignore_heal.py) | [`gitignore_heal.pyi`](gitignore_heal.pyi) | `heal`, `main` | Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md. |
| [`gitlink_gate.py`](gitlink_gate.py) | [`gitlink_gate.pyi`](gitlink_gate.pyi) | `check` | Nested-gitlink gate: block committing an undeclared gitlink (mode 160000) into the workspace repo. |
| [`lock-gate.py`](lock-gate.py) | [`lock-gate.pyi`](lock-gate.pyi) | `wrapped`, `writes`, `moves`, `shell`, `main` | PreToolUse write and shell — the branch lock, asked at every write and every shell write its text shows; git is judged by its own wrapper. Rules: git/lock.py. |
| [`lock.py`](lock.py) | [`lock.pyi`](lock.pyi) | `git`, `out`, `repo_of`, `owned`, `governed` | The branch is the lock: one agent session per repo, held by standing on the branch it created. |
| [`outbox.py`](outbox.py) | [`outbox.pyi`](outbox.pyi) | `path`, `pending`, `add`, `done`, `rekey` | The outbox: a note for a repo's ISSUES.md or ROADMAP.md, left by a session that does not hold it. |
| [`wrapper.py`](wrapper.py) | [`wrapper.pyi`](wrapper.pyi) | `parse`, `changes`, `target`, `register`, `session` | git, through the branch lock: the half of core/hooks/git/git that needs Python — who calls, what the call touches, and whether that session holds the repo. |
<!-- routing:end -->
