## Carry
(copied verbatim from 4b-code.md Carry; fence: brain/GOALS.md and brain/INBOX.md untouched)
name: commit-hygiene | branch: feature/goals-roadmap | root: /mnt/workspace
test-cmd: `./verify.py fast` | criteria C1..C6 as in 4a-tests.md

## User Test
scenario: As Lucas, in a fresh tmp repo (outside the workspace) whose core.hooksPath is this checkout's core/hooks, I stage a change to ISSUES.md and to a.txt, then `git commit -- a.txt`; later I stage b.txt and run a plain `git commit`. I also drop an empty `.git` dir under a tmp path and ask whether it is a repo.
script: inline shell + python3 in scratchpad `r/` and `e/` (no file kept) run: git init; git config core.hooksPath /mnt/workspace/core/hooks; git commit -- a.txt; git commit; platform_law.is_repo(path)
observed:
- partial: commit 2e12691 holds only a.txt (1 file, +1); ISSUES.md stays modified/uncommitted (status `MM ISSUES.md`), so the dashboard rewrite did not ride along
- full: commit b14bd38 holds b.txt AND ISSUES.md (+50 lines, hook-generated); the aggregate still rides a non-partial commit
- is_repo: empty `.git` dir -> False; `.git/HEAD` written -> True; real repo -> True
- /mnt/workspace: nothing committed, index untouched
matches-expected-result: yes

executor: craft-medium model=anthropic/sonnet level=medium deleg=none
