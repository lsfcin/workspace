# git
> Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Which branches exist, who may write where, and how work reaches develop. |
| [`branch_debt.py`](branch_debt.py) | [`branch_debt.pyi`](branch_debt.pyi) | `repos`, `unmerged_branches`, `merged_local_branches`, `unpushed_work`, `merged_remote_branches` | What the entropy dashboard counts about branches: work that lives in only one place, and labels whose commits already landed. |
| [`dirt.py`](dirt.py) | — | `expand`, `owners`, `free`, `dirty`, `places` | PreToolUse and PostToolUse shell — who dirtied a free repo: what a shell call leaves dirty in a governed repo nobody holds is the session's that ran it. |
| [`gitignore_heal.py`](gitignore_heal.py) | [`gitignore_heal.pyi`](gitignore_heal.pyi) | `heal`, `main` | Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md. |
| [`gitlink_gate.py`](gitlink_gate.py) | [`gitlink_gate.pyi`](gitlink_gate.pyi) | `check` | Nested-gitlink gate: block committing an undeclared gitlink (mode 160000) into the workspace repo. |
| [`lock-gate.py`](lock-gate.py) | [`lock-gate.pyi`](lock-gate.pyi) | `calls`, `changes`, `target`, `writes`, `main` | PreToolUse write and shell — the branch lock, asked at every write, every shell write its text shows, and every git command that changes a repo. Rules: git/lock.py. |
| [`lock.py`](lock.py) | [`lock.pyi`](lock.pyi) | `git`, `out`, `repo_of`, `owned`, `governed` | The branch is the lock: one agent session per repo, held by standing on the branch it created. |
<!-- routing:end -->
