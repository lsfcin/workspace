## Carry
name: commit-hygiene | branch: feature/goals-roadmap | root: /mnt/workspace
provider: anthropic | chain-deleg: none
level-map: anthropic | verified-on: 2026-10-07
test-cmd: `./verify.py fast` (targeted: `core/run --python -m pytest <test files> -q`) | e2e-cmd: none
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=per-feature arch-review-supervised=no
criteria:
 C1 A partial commit (`git commit -- <paths>`; GIT_INDEX_FILE basename not `index` and not `index.lock` — see Plan Review R1) never gains a file the committer did not name: `generators.issues` → ISSUES.md, `brain_stats` → GOALS.md, `gitignore_heal` → .gitignore skip staging any path outside the commit's staged set.
 C2 A full commit (`git commit`, `git commit -a`) behaves as today: regenerated ISSUES.md / GOALS.md / healed .gitignore still staged.
 C3 One shared predicate `is_repo(path)`: True when `path/.git` is a directory holding `HEAD`, or `path/.git` is a FILE; False for an empty `.git` directory or none.
 C4 `is_repo` replaces every bare `(p / '.git').exists()` repo test in core/hooks (entropy_fields:62, entropy_corpus:84 and :120, entropy_size:31, entropy_naming:162, brain_attention:80, gitignore_heal:100). One definition (grep proves it).
 C5 Tests: fixture repo where `git commit -- a.txt` lands without ISSUES.md; full commit (plain and `-a`) carries it; `is_repo` true/false cases incl. empty `tmp_path/.git`. `./verify.py fast` green.
 C6 ISSUES.md gains one hand-written entry: empty `/tmp/.git` (also `/tmp/.codex`, `/tmp/.agents`, root `.codex/`, `.agents/`) — writer not in this repo; coincides with the Codex sandbox (bubblewrap mount points). Hypothesis, not proof.
tasks:
 T1 — `is_repo(path)` in core/hooks/platform_law.py + tests — platform_law.py, test_platform_law.py — medium
 T2 — replace the 7 `.git`-exists sites with `is_repo`; fix fixtures that made an empty `.git` dir — 6 hook files + 3 test files — medium
 T3 — `is_partial()` + `stage(cwd, *paths, named_only=False)` in core/hooks/commit/pre_commit.py; generators._stage delegates; issues() passes named_only=True — pre_commit.py, generators.py — medium
 T4 — brain_stats.py and gitignore_heal.py stage through `stage(..., named_only=True)` — 2 files — medium
 T5 — real-git tests for C1/C2 — new core/tools/test/workspace/test_partial_commit_staging.py — medium
 T6 — ISSUES.md hand entry for C6 — ISSUES.md — low
 T7 — `./verify.py fast` green; caps held — none — low
context: /mnt/workspace/AGENTS.md, core/CONTEXT.md, core/hooks/CONTEXT.md, core/hooks/SPECS.md, code/SPECS-git.md

## Ground
branch-created: feature/goals-roadmap base: feature/pdf-twin
paths: 13/13 ok (11 existing: platform_law.py, entropy_fields.py, entropy_corpus.py, entropy_size.py, entropy_naming.py, brain_attention.py, gitignore_heal.py, pre_commit.py, generators.py, brain_stats.py, ISSUES.md; 2 new with parent dirs: test_platform_law.py, test_partial_commit_staging.py)
test-cmd-runs: yes (1092 passed, 1 skipped in 283.07s)

executor: craft-low model=anthropic/haiku level=low deleg=none
