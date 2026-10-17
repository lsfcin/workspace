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

## Plan
branch: feature/goals-roadmap (pinned by orchestrator; Phase 0 of goals-roadmap-reform rides it)
Fence (every row): never stage/commit/revert `brain/GOALS.md`, `brain/INBOX.md`. Never hand-edit a `.pyi` (pre-commit regenerates). No file may pass 250 lines or 18000 chars (`wc -lc`); platform_law.py starts at 204 lines, pre_commit.py 186, generators.py 199 — docstrings ≤3 lines.

| id | task | files | done-when | level | effort |
|----|------|-------|-----------|------|--------|
| T1 | Add `def is_repo(path) -> bool` to platform_law.py: `g = Path(path) / '.git'; return g.is_file() or (g.is_dir() and (g / 'HEAD').is_file())`. Tests: `git init` dir → True; dir with `.git` FILE (`gitdir: x`) → True; empty `.git` dir → False; no `.git` → False. | core/hooks/platform_law.py; core/tools/test/law/platform/test_platform_law.py | 4 new tests pass | medium | medium |
| T2 | Swap `(X / '.git').exists()` → `is_repo(X)` at: entropy/entropy_fields.py:62, entropy/entropy_corpus.py:84 and :120, entropy/entropy_size.py:31, entropy/entropy_naming.py:162 (keep its `not`), brain/brain_attention.py:80, git/gitignore_heal.py:100. Import `from platform_law import is_repo` (entropy_fields: core/hooks is not yet on sys.path — add `sys.path.insert(0, str(_HOOKS))` beside the existing insert). Fixtures making an empty `.git` dir now mean "not a repo": give each a HEAD — `(d / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')` after the mkdir — at test_entropy_naming.py:107, test_gitignore_self_heal.py:27, workspace/generators/test_routing_table.py:204. Add one test in test_entropy_fields.py: file under `tmp_path/sub/` with EMPTY `tmp_path/.git` → `_repo_root` returns `WORKSPACE_ROOT`. | the 7 hook files above; the 3 tests + core/tools/test/law/entropy/test_entropy_fields.py | `grep -rnE "['\"]\.git['\"]\)\.exists\(\)" core/hooks --include=*.py` empty; `grep -rn "def is_repo" core --include=*.py` = 1 line; the 4 test files pass | medium | medium |
| T3 | In pre_commit.py add `is_partial()`: `Path(os.environ.get('GIT_INDEX_FILE', '')).name not in ('', 'index', 'index.lock')`. Add `stage(cwd, *paths, named_only=False)`: if `named_only and is_partial()`, read `named = set(git('diff','--cached','--name-only', cwd=cwd).splitlines())` and `top = Path(git('rev-parse','--show-toplevel', cwd=cwd))`; per path, `full = (Path(cwd) / path).resolve()`; if named-mode and `rel(full, top.resolve())` not in `named`, print `→ <that rel> not staged: partial commit; the next full commit carries it` and skip; else `git('add', str(path), cwd=cwd)`. generators._stage(commit, *paths, named_only=False) becomes a one-line call to `stage(commit.toplevel, *paths, named_only=named_only)`; only `issues()` passes `named_only=True` (derived artifacts — .pyi/.d.ts/.texif/CONTEXT.md/AGENTS.md — keep staging: they follow a named file). | core/hooks/commit/pre_commit.py; core/hooks/commit/generators.py | T5 passes; `grep -n "named_only=True" core/hooks/commit/generators.py` = 1 hit, in issues() | medium | high |
| T4 | brain_stats.py:166 `git("add", *to_stage)` → `stage(Path.cwd(), *to_stage, named_only=True)` (add `str(_HOOKS / 'commit')` to sys.path, `from pre_commit import stage`; spawn() already runs it with cwd = repo, env inherited so GIT_INDEX_FILE reaches it). gitignore_heal.py:107 `git('add', str(ignore), cwd=root)` → `stage(root, ignore, named_only=True)`. Behaviour on full commits unchanged. | core/hooks/brain/brain_stats.py; core/hooks/git/gitignore_heal.py | test_gitignore_self_heal.py passes; `grep -n 'git("add"' core/hooks/brain/brain_stats.py` empty | medium | medium |
| T5 | New test file. Fixture: `git init` in tmp_path, set user.name/email, initial commit of a.txt; write a hook dir with `pre-commit` = `#!/bin/sh\nexec <sys.executable> -c "import sys; sys.path.insert(0, '<checkout>/core/hooks/commit'); from pre_commit import stage; open('ISSUES.md','a').write('x\\n'); stage('.', 'ISSUES.md', named_only=True)"` (chmod +x), `git config core.hooksPath <hookdir>`. Cases: (a) edit a.txt, `git commit -m p -- a.txt` → `git show --name-only HEAD` lists a.txt only; (b) `git add a.txt; git commit -m f` → ISSUES.md in HEAD; (c) `git commit -am f` → ISSUES.md in HEAD; (d) `is_partial()` False with GIT_INDEX_FILE unset (monkeypatch). conftest strips GIT_* — run git via subprocess with `cwd=tmp_path`, never inside the workspace. | core/tools/test/workspace/test_partial_commit_staging.py | 4 cases pass | medium | medium |
| T6 | Under `## Open` in root ISSUES.md add one bullet, bold title + date 2026-10-06, 2–3 lines per C6, tag `b20261006-empty-dotgit-in-tmp`; say `is_repo` now ignores an empty `.git`; mark the Codex link as hypothesis. Do not touch the generated `## Entropy` block. | ISSUES.md | entry present; `git diff ISSUES.md` touches only `## Open` | low | low |
| T7 | Run `./verify.py fast`; `wc -lc` every touched file. | — | exit 0; all ≤250 lines, ≤18000 chars | low | low |

## Plan Review (adversarial, assume small executors)
Pass 1:
- R1 FATAL: "basename != `index`" misreads `git commit -a`. Measured here (scratch repo, 2026-10-07): plain commit → `.git/index`; `-a` → `.git/index.lock`; `-- <paths>` → `.git/next-index-<pid>.lock`. Literal rule would drop ISSUES.md from every `-a` commit, breaking C2 → predicate amended to `not in ('', 'index', 'index.lock')`; C1/C2 rewritten; T5(c) pins it. Orchestrator: this sharpens a "do not reopen" decision with evidence, it does not reverse it.
- R2 FATAL: filtering inside the shared `_stage` for ALL callers would drop `.pyi` etc. for named sources on partial commits (they are never in `staged`) → opt-in `named_only` flag; one filter, three opt-in callers (T3 note).
- R3 FATAL: brain_stats runs as a subprocess with no Commit object → the filter must read the index itself (`git diff --cached` under inherited GIT_INDEX_FILE), not `commit.staged` (T3/T4 spelled out).
- R4 FATAL: 3 fixtures build an empty `.git` dir as "a nested repo" and break once `is_repo` needs HEAD → named with line numbers in T2. (test_shim_paths.py:197 exercises a shell hook, not these modules — leave it.)
- R5: entropy_fields lacks core/hooks on sys.path → import line spelled out in T2.
- R6: path mismatch (absolute vs repo-relative, symlinked tmp) → `.resolve()` both sides, compare via `platform_law.rel` (T3).
- R7: a full-pipeline fixture would trip unrelated gates in a tmp repo → T5 drives `stage` through a minimal real hook under real `git commit`.
Pass 2: zero unresolved FATALs. Residual, outside scope: derived artifacts (CONTEXT.md routing sync, AGENTS.md) can still pull a named-adjacent file's unrelated hand edits into a partial commit. Loop 6 should log it in ISSUES.md; brain/INBOX.md is fenced.
Roadmap: no ROADMAP.md line added. Both roadmaps are near the char cap (14586 and 13623 chars) and this chain is Phase 0 of the goals-roadmap-reform plan, which owns the item. Orchestrator: confirm, or have Loop 6 add it.
verdict: PASS

executor: craft-high model=anthropic/opus level=high deleg=none
