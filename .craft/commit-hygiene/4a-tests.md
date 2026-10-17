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

## Tests
| test file | covers | asserts |
|-----------|--------|---------|
| core/tools/test/workspace/test_partial_commit_staging.py (new) | C1 | real git + real pre-commit hook: `commit -- a.txt` with `stage(..., named_only=True)` leaves HEAD:ISSUES.md 'original'; named ISSUES.md rides; partial commit does not gain healed .gitignore line via `_add_missing_lines` |
| same | C2 | plain `commit` and `commit -a` carry 'regenerated'; control (named_only=False, partial) reaches the bug |
| same | C1 | `is_partial()` on unset / `.git/index` / `index.lock` -> False, `next-index-123.lock` -> True |
| same | C1 | recorders: `generators.issues` and `brain_stats.pre_commit` call `stage(..., named_only=True)` (never touches real GOALS.md) |
| core/tools/test/law/platform/test_platform_law.py (appended) | C3 | `is_repo`: `.git` dir with HEAD / `.git` file True; empty `.git` dir / none False; str and Path |
| same | C4 | zero bare `('.git').exists/is_dir/is_file(` in core/hooks/**/*.py; exactly one `def is_repo` in core/**/*.py |
red-run: 14 failed as expected (12 in staging file, 2 in platform_law; 5 existing pass) | wrong-failures: none. Red causes: NotImplementedError from the 3b placeholders (is_repo, is_partial, stage: hook exits 1 / call raises), the 7 bare `.git` sites still present (C4), generators/brain_stats still call old `_stage`/`git add`, and the .gitignore partial test fails on the old unconditional `git add` (the real bug). No ImportError or syntax failures. C5's `./verify.py fast` green and the T2 fixture fix (empty `.git` dirs in 3 test files) are 4b's.
note: B4 patches `generators.stage` / `brain_stats.stage` with raising=False because 4b creates those names.

executor: craft-medium model=anthropic/sonnet level=medium deleg=none
