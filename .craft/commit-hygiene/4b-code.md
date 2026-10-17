## Carry
(copied verbatim from 4a-tests.md Carry; fence: brain/GOALS.md and brain/INBOX.md untouched)
name: commit-hygiene | branch: feature/goals-roadmap | root: /mnt/workspace
test-cmd: `./verify.py fast` | criteria C1..C6 as in 4a-tests.md

## Code
attempt 1: T1 is_repo, T2 seven sites, T3 is_partial/stage/generators, T4 brain_stats+gitignore_heal, T6 ISSUES entry → 3 red (test_entropy_naming::test_readme_needs_a_repo_root, test_gitignore_self_heal x2): their fixtures made an empty `.git` dir, which is_repo now (correctly) rejects (planned T2 fixture fix)
attempt 2: fixtures now also write `.git/HEAD` (setup only, no assertion edited) → 1 red under load: test_features_wiring::test_the_wired_gates_actually_consult_the_law (rtk-compaction, file untouched; passes alone: flake, not mine)
attempt 3: rerun → green
green: yes run: `1106 passed, 1 skipped in 174.15s (0:02:54)`
caps: pre_commit.py 200 (≤200), platform_law.py 211 (≤250), generators.py 198
C4 grep: no bare `.git` exists/is_dir/is_file in core/hooks; one `def is_repo` (platform_law.py)
touched: core/hooks/platform_law.py, commit/pre_commit.py, commit/generators.py, brain/brain_stats.py, brain/brain_attention.py, git/gitignore_heal.py, entropy/entropy_{fields,corpus,size,naming}.py, core/tools/test/law/entropy/test_entropy_naming.py (fixture), core/tools/test/workspace/test_gitignore_self_heal.py (fixture), ISSUES.md (C6 entry; also hook-regenerated parts pre-existing)
note: stub .pyi files regenerate at commit.

executor: craft-medium model=anthropic/sonnet level=medium deleg=none
