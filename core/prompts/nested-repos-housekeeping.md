# nested-repos-housekeeping
> Every nested repo commits its uncommitted work and ends on its own main (develop → main where a develop exists). Second half of the 2026-10-06 housekeeping; delete when every repo below is clean.

Level: medium. Language with Lucas: pt-br. **Put every decision's context INSIDE the AskUserQuestion text** — prose before a tool call does not reach Lucas in the VS Code extension.

## Decided (Lucas, 2026-10-06)
- All of them, ending on each repo's main. `code/*` follow Git Flow (the gate blocks main/develop): `feature/housekeeping-<date>` → develop → main, push. Repos under `academy/` and `branches/` are exempt and commit to main directly.
- Before each commit: read the diff, scan for secrets (CPF/CNPJ/tokens belong in a gitignored `segredos.env`), commit by theme with `git commit -- <paths>`.
- Large ones get a per-theme summary that Lucas approves before committing: `academy/administration` (151), `academy/teaching` (17), `academy/reviews` (11).
- `branches/virada` has no remote: creating one is an outward action, ask first. `.Trash-1000/` holds three repos: ignore.

## Dirty on 2026-10-06 (files)
administration 151 · teaching 17 · reviews 11 · talks 6 · isoroll-content 6 · flows 5 · casinhas 5 · papers/ai4good 4 · lab 2 · papers/2027-CHI-avdspace 2 · instituto 2 (branch `master`) · dobra 2 · freeai 2 · isoroll-module 2 · apptime 1 · papers/pls-pix 1. Re-count before starting; this list is a snapshot.
