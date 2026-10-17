## Carry
(copied verbatim from 5-user.md Carry)
name: commit-hygiene | branch: feature/goals-roadmap | root: /mnt/workspace
test-cmd: `./verify.py fast` | criteria C1..C6 as in 4a-tests.md

## Ship

diff-scope: clean — all in-scope files staged, extras identified (brain/INBOX.md pre-existing-dirty, .craft/commit-hygiene/ keep-trail)

BLOCKED: Pre-commit hook requires `/mnt/workspace/run` script (called by `core/hooks/pre-commit` wrapper on line 7, `exec sh "$(dirname "$0")/../run"`), which does not exist in the repository. This is infrastructure debt external to the commit-hygiene feature scope.

Staged files ready for commit:
- ISSUES.md (40 lines added/modified via hook generators)
- core/hooks/ platform_law.py/pyi, commit/pre_commit.py/pyi/generators.py/CONTEXT.md, entropy/*.py, git/gitignore_heal.py, brain/*.py (18 files, 270 insertions, 31 deletions)
- core/tools/test/law/entropy/test_entropy_naming.py, law/platform/test_platform_law.py, workspace/test_gitignore_self_heal.py, workspace/test_partial_commit_staging.py (new)

User test (Loop 5): PASSED — partial & full commits work correctly, platform_law.is_repo() validation correct, ISSUES.md entropy tracking functions as expected.

Status: feature complete, ready to ship on infrastructure repair
Next step: create /mnt/workspace/run script (venv handoff per core/hooks comment), or skip pre-commit hook via user --no-verify permission + TODO log.

executor: craft-low model=anthropic/haiku level=low deleg=none
