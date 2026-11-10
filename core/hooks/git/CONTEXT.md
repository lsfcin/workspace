# git
> Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`branch-gate.py`](branch-gate.py) | [`branch-gate.pyi`](branch-gate.pyi) | `main` | PreToolUse write and PostToolUse shell — a session writes only on the branch it chose. |
| [`branch_debt.py`](branch_debt.py) | [`branch_debt.pyi`](branch_debt.pyi) | `repos`, `unmerged_branches`, `merged_local_branches`, `unpushed_work`, `merged_remote_branches` | What the entropy dashboard counts about branches: work that lives in only one place, and labels whose commits already landed. |
| [`branch_marker.py`](branch_marker.py) | [`branch_marker.pyi`](branch_marker.pyi) | `marker_for`, `env_session`, `finished`, `record`, `verdict` | Branch drift: HEAD is shared mutable state between parallel sessions, so each session keeps the branch it chose, per repo, and is stopped before writing on one it did not choose. |
| [`gitflow_gate.py`](gitflow_gate.py) | [`gitflow_gate.pyi`](gitflow_gate.pyi) | `check`, `enforced` | Git Flow branch gate: block direct commits to main/master/develop, require feature|release|hotfix. |
| [`gitignore_heal.py`](gitignore_heal.py) | [`gitignore_heal.pyi`](gitignore_heal.pyi) | `heal`, `main` | Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md. |
| [`gitlink_gate.py`](gitlink_gate.py) | [`gitlink_gate.pyi`](gitlink_gate.pyi) | `check` | Nested-gitlink gate: block committing an undeclared gitlink (mode 160000) into the workspace repo. |
<!-- routing:end -->
