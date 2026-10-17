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

## Architecture
Measured 2026-10-07, git 2.55: `git commit -- a.txt` hands the hook GIT_INDEX_FILE=`<abs>/.git/next-index-<pid>.lock` and `diff --cached` = `a.txt` only; `-a` → `<abs>/.git/index.lock`; plain → `.git/index` (RELATIVE). The basename test holds for all three; unset = not inside a commit. The "named set" is what the temp index CHANGES vs HEAD: a named path with no change is not in it (accepted).
- core/hooks/platform_law.py — T1 — `def is_repo(path) -> bool:` body exactly `dot = Path(path) / '.git'` / `return dot.is_file() or (dot / 'HEAD').is_file()`, appended after `rel()`. Docstring gives the reason it lives in the platform boundary: the Codex sandbox (bubblewrap) leaves EMPTY `.git` mount points — a platform fact; a worktree/submodule `.git` is a FILE.
- entropy_fields.py:62, entropy_corpus.py:84 + :120, entropy_size.py:31, entropy_naming.py:162, brain/brain_attention.py:80, git/gitignore_heal.py:100 — T2 — `(X / '.git').exists()` → `is_repo(X)` (`not is_repo(parent)` at naming:162). Import: extend the existing `from platform_law import ...` line (corpus, size, naming); add `from platform_law import is_repo  # noqa: E402` beside `import feature_law` (fields, brain_attention, gitignore_heal — hooks root already on sys.path). Nothing else changes in these files.
- T2 fixtures — empty `.git` dirs that now mean "not a repo": law/entropy/test_entropy_naming.py:107, workspace/test_gitignore_self_heal.py:27, workspace/generators/test_routing_table.py:204 (reaches entropy_corpus.owning_repo via workspace_scanner.carried). Each: right after the mkdir, `(<same>/'.git'/'HEAD').write_text('ref: refs/heads/main\n', encoding='utf-8', newline='\n')`. NOT shims/test_shim_paths.py:197 (shell walk for core/run, never reads .git).
- core/hooks/commit/pre_commit.py — T3 — two functions after `spawn()`; import becomes `from platform_law import WORKSPACE_ROOT, rel`.
  `def is_partial() -> bool:` → `return Path(os.environ.get('GIT_INDEX_FILE', 'index')).name not in ('index', 'index.lock')`.
  `def stage(cwd, *paths, named_only=False) -> None:` → `named = set(git('diff', '--cached', '--name-only', cwd=cwd).splitlines()) if named_only and is_partial() else None`; per path: `if named is None or rel(Path(cwd, path).resolve(), Path(cwd).resolve()) in named: git('add', str(path), cwd=cwd)`. No --diff-filter (a named deletion is still named). Docstring states the RULE: an aggregate (ISSUES.md, GOALS.md, .gitignore) rides only if named; a companion derived from a named file (stub, CONTEXT.md, AGENTS.md norms) always rides, so those callers keep the default.
  BUDGET: 186 lines now, must end ≤200 (limits.env WARN_LINES); docstrings ≤3 lines each.
- core/hooks/commit/generators.py — T3 — DELETE `_stage` (no wrapper: one name, not two — overrides the plan's "delegates"). Import becomes `from pre_commit import Blocked, spawn, stage` (`git` has no other user here). Each `_stage(commit, X)` → `stage(commit.toplevel, X)` (6 sites); in `issues()` add `named_only=True`.
- core/hooks/brain/brain_stats.py — T4 — add `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'commit'))` + `from pre_commit import stage  # noqa: E402`; `git("add", *to_stage)` → `stage(Path.cwd(), *to_stage, named_only=True)`. It is SPAWNED (cwd = committing toplevel; env inherited, so GIT_INDEX_FILE reaches it). Keep the `git` import (staged_goal_files). Staged goal files pass the filter; GOALS.md only if named.
- core/hooks/git/gitignore_heal.py — T4 — `from pre_commit import Blocked, git, stage`; line 107 `git('add', str(ignore), cwd=root)` → `stage(root, ignore, named_only=True)`. `main()` runs outside a commit (env unset) → still stages.
- core/tools/test/law/platform/test_platform_law.py — T1 — C3 cases (B5) + C4 ceiling: zero matches of regex `['"]\.git['"]\)\.(exists|is_dir|is_file)\(` in core/hooks/**/*.py, exactly one `def is_repo` under core/**/*.py.
- core/tools/test/workspace/test_partial_commit_staging.py (new) — T5 — B1–B4.
- ISSUES.md — T6 — one hand entry (C6) OUTSIDE any generated block. ISSUES.md is already MM in this tree; brain/GOALS.md, brain/INBOX.md are fenced (never stage/revert).

## Evaluation
criteria-coverage: C1→pre_commit.stage+is_partial, named_only=True at generators.issues / brain_stats.pre_commit / gitignore_heal._add_missing_lines · C2→same, is_partial False · C3→platform_law.is_repo · C4→7 sites + ceiling test · C5→test_platform_law + test_partial_commit_staging + verify fast · C6→ISSUES.md
boundaries:
 B1 real git in tmp_path: `git init`, user.name/email set, commit ISSUES.md='original\n' + a.txt with `-c core.hooksPath=<tmp>/nohooks` (empty dir). Then `<tmp>/hooks/pre-commit` = `#!/bin/sh\nexec "<sys.executable>" "<tmp>/hook.py"\n` (newline='\n', chmod 0o755); hook.py puts core/hooks + core/hooks/commit on sys.path, writes ISSUES.md='regenerated\n', calls `stage(Path.cwd(), 'ISSUES.md', named_only=<param>)`. Every test commit: `git -c core.hooksPath=<tmp>/hooks commit -m x ...` — the global hooksPath is the workspace pipeline and must never fire here. Assert `git show HEAD:ISSUES.md`.
 B1a C1: edit a.txt, `commit -- a.txt`, named_only=True → 'original'. B1b control, named_only=False → 'regenerated' (the fixture reaches the bug). B1c C2: `git add a.txt; commit` → 'regenerated'. B1d C2: `commit -a` → 'regenerated'. B1e: write ISSUES.md='user\n', `commit -- a.txt ISSUES.md` → 'regenerated' (named rides).
 B2 is_partial (monkeypatch.setenv/delenv): unset, `.git/index`, `/x/.git/index.lock` → False; `/x/.git/next-index-123.lock` → True.
 B3 gitignore_heal, B1 harness, hook.py calls `gitignore_heal._add_missing_lines(Path.cwd(), Path.cwd() / '.gitignore')` (NOT heal(): with root == toplevel outside the workspace it returns before healing); init commit holds .gitignore `core/*\n` and `core/newdir/CONTEXT.md` added with `git add -f`. Partial `-- a.txt` → HEAD:.gitignore lacks `!core/newdir/`; plain full → has it.
 B4 call-site recorders, no git: generators.issues with feature_law.is_enabled→True, generators._keeps_a_list→True, generators.spawn→obj(returncode=0), generators.stage→recorder ⇒ named_only=True. brain_stats.pre_commit with load_goal_files→{'g': tmp file}, Attention→stub(`.missing=[]`), staged_goal_files→{}, feature_law.is_enabled→False, GOALS_FILE→tmp file, check_compass_reminder→noop, stage→recorder ⇒ named_only=True. NEVER touch the real brain/GOALS.md.
 B5 C3: `.git` dir with HEAD → True; `.git` file → True; empty `.git` dir → False; none → False.
verdict: PASS

## Concept-Symmetry Review
checklist: alike-look-alike=ok (one stage() for all generators, one is_repo for all walks) · naming-coherent=ok (`_stage` dies, no synonym survives) · boundaries-consistent=ok (aggregate-vs-companion staging is now a stated rule in stage's docstring, not an accident) · model-sound=ok, noted: platform_law's charter is "what an OS is"; is_repo belongs there only via the sandbox fact, which its docstring must carry — else its home is file_law.
codegraph: not initialized; `init` would index the whole workspace (growth) — substituted a regex sweep: exactly the 7 C4 sites in core/, none elsewhere outside tests.
dedup (manual): four "walk up to the owning repo" walks remain (entropy_corpus.owning_repo, entropy_fields._repo_root, entropy_size._added_by inline, brain_attention.governing_repo) + two `git()` helpers (pre_commit, brain_common). Out of scope; Loop 6 files it in ISSUES.md (brain/INBOX.md is fenced).
supervised: n/a
verdict: PASS

executor: craft-high model=anthropic/opus level=high deleg=none
