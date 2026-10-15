# nested-repos-housekeeping
> Every nested repo commits its uncommitted work and ends on its own main (develop → main where a develop exists). Second half of the 2026-10-06 housekeeping; delete when every repo below is clean.

Level: medium. Language with Lucas: pt-br. **Put every decision's context INSIDE the AskUserQuestion text** — prose before a tool call does not reach Lucas in the VS Code extension.

## Decided (Lucas, 2026-10-06)
- All of them, ending on each repo's main. `code/*` follow Git Flow (the gate blocks main/develop): `feature/housekeeping-<date>` → develop → main, push. Repos under `academy/` and `branches/` are exempt and commit to main directly.
- Before each commit: read the diff, scan for secrets (CPF/CNPJ/tokens belong in a gitignored `segredos.env`), commit by theme with `git commit -- <paths>`.
- Large ones get a per-theme summary that Lucas approves before committing: `academy/administration` (151), `academy/teaching` (17), `academy/reviews` (11).
- `branches/virada` has no remote: creating one is an outward action, ask first. `.Trash-1000/` holds three repos: ignore.

## Also: /publish was refused by the target
2026-10-06 `--sync` settled at 0 differences, then `--push` was refused by the target's own suite (12 failed, 1068 passed); nothing was pushed and the local branch `feature/sync-20261006-1622` is left in `code/wos`. Fix HERE, never on the far side, then re-run `/publish`. Failing in the target: `test_entropy_fields::test_a_feature_field_names_the_registry` · `test_entropy_context::test_every_project_declares_its_goal` · `test_b20260922_a_marker_store_does_not_survive_a_reboot::test_per_machine_state_never_reaches_git` · `test_entropy_retired::test_a_vendored_file_is_not_policed` · `test_corpus_ceiling::test_routing_tables_pointing_at_untracked_files_do_not_grow` · `test_links::test_a_page_with_habilidades_block_runs_arvore_generator` · `test_b20260905_brain_drafts_carries_two_asymmetries` (2 cases) · `test_shim_paths` codex cases (2 — `.codex/hooks.json` likely does not cross) · `test_file_law::test_the_vendored_waiver_reaches_the_edit_gate` · `test_features_wiring::test_the_wired_gates_actually_consult_the_law`. Also 161 orphans: the `/slides` tree (`core/skills/slides/**`) and `core/tools/wos/handoff` cross with no feature claiming them — a `ships` entry or a refusal, Lucas decides whether /slides is public.

## Dirty on 2026-10-06 (files)
administration 151 · teaching 17 · reviews 11 · talks 6 · isoroll-content 6 · flows 5 · casinhas 5 · papers/ai4good 4 · lab 2 · papers/2027-CHI-avdspace 2 · instituto 2 (branch `master`) · dobra 2 · freeai 2 · isoroll-module 2 · apptime 1 · papers/pls-pix 1. Re-count before starting; this list is a snapshot.
