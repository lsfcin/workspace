# hook-scoreboard
> Which features ever actually fire, and which of those ever actually block anything?

82 features are declared and switched on, and not one has ever been counted. Every cut is therefore a guess and every kept rule is paid for on faith ([/ROADMAP.md](../../ROADMAP.md) § Measurement). This is the cheap half of the ablation: before asking *what does the workspace cost without X*, ask whether X has ever done anything at all.

## Method

```
core/run tools/wos/features --scoreboard
```

Two counts per feature, recorded where each is knowable and nowhere else.
[`core/hooks/feature_law.py`](../hooks/feature_law.py) `is_enabled()` records **fired** — it is the one function every switched feature of every group passes through.
[`core/hooks/dispatch.py`](../hooks/dispatch.py) records **blocked**, because it is the only place that sees a gate's exit code; the feature it counts against is declared in [`core/hooks/gates.txt`](../hooks/gates.txt) § feature.

The store is `core/scoreboard.tsv`, gitignored and per machine, one row per event, aggregated on read. The suite sets `WOS_SCOREBOARD` at [`conftest.py`](../tools/test/conftest.py) and so stays out of the measurement — one unguarded run wrote 47,000 rows, which would have made a two-week reading a recording of pytest.

**The measurement is the pair, never either column alone.** A feature that fired ten thousand times and blocked nothing is either guarding something nobody violates or guarding nothing, and the registry cannot tell those apart. `-` under blocked means the feature does not block by declaration;
`0` means it does and never has.

**A THIRD READING OF `fired` HIGH / `blocked` 0, found 2026-09-21 and the one this pair cannot see: the gate is aimed at a shape its subject does not have.** `issues-gate` read 937 / 0, which looks like the first case — a rule nobody violates. It was neither. Its matcher wanted `## b<id>` headings and every `ISSUES.md` in the workspace is written in bullets, so it had never had anything to match and could not have blocked whatever anyone wrote. Nothing in the two columns says so; it took opening the regex. **So a `0` is a question for the reading, never an answer** — before a feature is cut for never blocking, check that it can see its subject at all, because a cut made on this evidence would have deleted a gate whose only fault was aim.

## Results

| Date | Window | Features fired | Never fired | Blocks recorded | Notes |
|------|--------|---------------|-------------|-----------------|-------|
| 2026-09-14 | instrument landed | — | — | — | clock starts; the first reading is owed after two weeks of ordinary use |

## What changed

Nothing yet — the instrument is one session old and has no window to report. What it has already changed is [`core/hooks/gates.txt`](../hooks/gates.txt): asking every row to name its feature made three gates answer `-`. `checks/pre-edit.py`, `facade/facade-scan.py` and `facade/facade-tracker.py` consult no switch at all, so an ablation run that turns their feature off leaves them running. That was invisible until the column asked.

## Limitations

- **One machine, and it is Lucas's.** The store is per clone by design, so this measures how *he*
  works, not how the workspace behaves. A feature that never fires here may be load-bearing on the
  other clone.
- **`fired` is a consultation, not an action.** It counts a feature being asked whether it is live.
  A gate that runs and finds nothing to say still fired, which is exactly the population the
  `blocked` column exists to split — but only for gates that block, and only through the dispatcher.
- **A commit-side gate's blocks are not counted.** `pre-commit` refuses by raising `Blocked` in its own pipeline, which this does not reach; only the lifecycle gates in `gates.txt` report blocks.
- **Three gates cannot be attributed at all** — the `-` rows above. Their blocks are recorded nowhere, so this undercounts, and the fix is to wire them rather than to adjust the number.
- **It cannot say whether a rule is worth keeping.** A feature that never fires may be cheap insurance against something rare. This narrows the question; the ablation answers it.
