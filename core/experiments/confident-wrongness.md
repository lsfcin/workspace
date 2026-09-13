# confident-wrongness
> When this workspace has been confidently wrong, what caught it — and how much of that was one of our own checks?

## Method

The reproducible half is a count of **retraction markers**: lines where our own record states that a
belief we held turned out false. The regex is frozen as of 2026-09-12 and must not be edited to fit a
later corpus — a widened pattern would report drift as improvement.

```sh
RE='was wrong (in every claim|by)|was (still )?wrong by|was an artifact|read as confirmation|went unverified for months|first (run|version) .{0,40}was wrong|reported .{0,30}MISSING|stayed green|read green on .{0,30}red|could not see|overruled twice'
git grep -nIE "$RE" | wc -l    # marker lines
git grep -lIE "$RE" | wc -l    # files carrying at least one
```

Whole tracked tree, no extension filter. An earlier draft filtered on `*.md`/`*.py`/`*.txt` and
missed the extensionless entrypoints, `core/tools/wos/roundup` among them — so the scope is now
"every text file git tracks" and nothing narrower.

The judged half is the **incident set**: distinct events behind those markers, deduplicated, each
read in place and each classified by *what caught it*. Several markers describe one incident and some
incidents carry no marker at all, so the marker count is a floor on the incident count, never an
estimate of it. The classification is judgment and is not reproducible by the command above.

Hand-check, as `SPECS.md` requires of a new instrument: three incidents were traced to real commits
with `git log -S` on the identifier each one names, confirming the prose describes code that changed
rather than a story about code.

## Results

| Date | Marker lines | Files | Distinct incidents | Caught by one of our own automated checks | Slowest catch |
|---|---|---|---|---|---|
| 2026-09-12 | 31 | 29 | 18 | 1 | months |

Three of the 29 files sit outside the scaffold, in `code/aiwbot/` and `academy/papers/`.

What caught each of the 18, for the 2026-09-12 run:

| What caught it | Count | The clearest instance |
|---|---|---|
| Reading our own stored artifact later | 4 | a close wrote `green (1 passed, 695 deselected)` into the ledger |
| A second machine or clone disagreed | 3 | probes spelled the POSIX venv path, so every other clone reported the dependency missing |
| Re-measuring with a better lens | 3 | *nothing has ever been delegated* was an artifact of the lens, not a fact |
| A hand audit against raw data | 2 | the output-cost number was wrong by 2x for three weeks while two implementations agreed |
| A dedicated review sitting | 2 | the two rules cited as proof we knew how to doubt had gone unverified for months |
| Real execution contradicted it | 2 | the emitted delete command was one git refused |
| An agent verifying before acting | 1 | the entropy block was true when written and false when read |
| **One of our own automated checks** | **1** | `'ROADMAP.md'.isupper()` is false, and the instrument's own test caught it |

## What changed

`nothing yet` — the mechanism is Lucas's ruling, in the dedicated session the `ROADMAP.md` item
names. What the numbers hand that sitting:

- **One of eighteen** was caught by a check this workspace runs. Seventeen needed a second machine, a
  hand audit, a later read, or a sitting. The `ROADMAP.md` item's claim that *nothing catches it* is
  now a measured floor rather than an impression.
- **The largest category is the slowest.** Reading our own stored artifact later caught four, and
  each of those was published as a fact first. That is `core/SPECS.md` AD-16 band 1 exactly: a rule
  written with nothing checking.
- **Three were caught only because a second clone exists.** Two machines share this workspace for
  reasons that have nothing to do with doubt, and that accident is the second most effective catcher
  on the table. Nothing designs for it, nothing would notice if one clone went away, and no check
  asks whether a claim holds on both.

## Limitations

- **The marker count is a floor and cannot be a trend.** It matches phrasing, and a future incident
  worded differently is invisible to it. A falling count is therefore not evidence of improvement,
  and must never be read as one. The frozen regex protects the comparison, not the coverage.
- **Only documented retractions are visible.** An incident nobody wrote down is absent by
  construction, and the ones most likely to go unwritten are the ones nothing caught — so the true
  denominator is larger and the "caught by our own checks" share is an **upper** bound.
- **The classification is judgment, not measurement.** A second reader could move an incident between
  *re-measuring with a better lens* and *a hand audit against raw data*; the two shade into each
  other. The category that matters to the ruling — caught by an automated check of ours, or not — is
  the one with the least room to argue.
- **Latency is recorded only where the source states it.** "Months" and "three weeks" are quoted from
  the record; most incidents carry no date for when the belief formed, so no mean is computable and
  none is offered.
- **Self-reference is unavoidable.** This file is a claim about how bad we are at claims, assembled by
  the agent whose confidence is the subject. It has no second implementation, and by its own
  finding — two implementations of one misunderstanding are one measurement — a second one would not
  settle it either.
