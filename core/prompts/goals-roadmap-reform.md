# goals-roadmap-reform
> Goals stop holding tasks: every task lives in exactly one ROADMAP that names its goal, and each goal shows its open work as a generated block. Decided by Lucas 2026-10-06. Delete when the migration lands.

Level: high (architecture + migration). Run through `/craft`. Language with Lucas: pt-br. Branch: `feature/goals-roadmap`.
**Put every decision's context INSIDE the AskUserQuestion text** — in the VS Code extension, prose written before a tool call does not reach Lucas (it failed twice on 2026-10-06).

## Decided (do not reopen)
- **One rule, no exception: a task lives in a ROADMAP, never in a goal.** A goal keeps why, fears, timing, analysis and its selected next achievement, which points at a ROADMAP item id.
- **Link is one-way by hand:** a ROADMAP declares its goal in its header (code ROADMAPs already do), e.g. `> goal: [[workspace-os]]`; an item belonging to another goal carries that goal's wikilink. Every item must resolve to an existing goal — the type gate already checks that a wikilink names a goal file or an item in one; extend it, do not write a second checker.
- **The goal's list is GENERATED:** a delimited block "open work" in each goal file, rebuilt from the ROADMAPs that point at it — same mechanism as the GOALS.md attention block and the routing tables.
- **Goals with no project get one ROADMAP per area under `branches/`:** `branches/health/` (exercise, sleep, hair, smartphone…), `branches/fun/` (guitar, dance, pandeiro, surf, travel…), `branches/spiritual/` (vipassana, yoga, voice…), `branches/finances/`. Career and research go to the existing `academy/` ROADMAPs. The area comes from the goal header `[ area | subarea | horizon ]`.
- **Sub-repos per ROADMAP: deferred.** This migration draws those boundaries; decide afterwards.

## Scope (~420 open tasks across 38 goals, 2026-10-06 count)
1. Migration script — deterministic, verbatim text, no rewriting: each goal backlog item → its home ROADMAP with the right goal tag; done items are deleted (git holds them). Dry-run report first, Lucas approves the home of each goal.
2. Generator for the "open work" block; hook check that every ROADMAP item resolves to a goal.
3. Update readers: `/compass` (selected achievement = a ROADMAP item id, almost-there from roadmap state), the GOALS.md generator, `brain/SPECS.md` § Backlog, `compress_done`, `/inbox` (routes a task to a ROADMAP only; reverts the 2026-10-02 "redundancy mandate" paragraph), `brain/_templates/`.
4. Close the ISSUES entry "Boundary friction between goal tasks and project roadmaps".

## Also queued for that session
- **Find the root cause of text not reaching Lucas in the VS Code extension** (text between tool calls, and before AskUserQuestion). Measure, then fix the norm or the habit; `core/norms/interview.md` already states the rule.
- `academy/teaching/REFS.md` is 26k: apply the same two-level split `core/refs` got on 2026-10-06 (one yaml per judged ref).
- Two suite cases fail only under load and pass alone: `test_features_wiring::test_the_wired_gates_actually_consult_the_law` and `test_b20260831_silent_stub_gate::test_an_empty_stub_counts_as_absent`.
- An empty `/tmp/.git` appeared twice on 2026-10-06 (14:49, 15:47), not reproducible from the suite alone, and `entropy_fields._repo_root` takes any `.git` for a repo, so every tmp file went unchecked and `test_a_feature_field_names_the_registry` failed. Find the writer; make `_repo_root` require a real repo (`.git/HEAD` or a `.git` file).
- The pre-commit generator stages ISSUES.md into whatever commit is running, even under `git commit -- <paths>` (it landed the triage's ISSUES edits in the video commit c8820b22).
