# entropy — scope vs rot
> When the entropy count climbs, is the tree drifting or is the check set growing?

The count went 95 (2026-08-13) to 645 (2026-08-24) and every hand-off called it drift. It is not:
the two are separable from the reports themselves, because each one records its own check table and its own scanned-file count. Nothing here needs old code re-run.

## Method

```
git log --format=%h -- entropy.md ISSUES.md      # every dated report; the count lived in
git show <commit>:entropy.md | head -20          # entropy.md until 2026-08-19, ISSUES.md after
```

Then today's per-check totals over the same population the reports used:

```
python3 -c "import sys;from pathlib import Path;R=Path('/mnt/workspace');\
[sys.path.insert(0,str(R/p)) for p in ('core/hooks','core/hooks/entropy','core/hooks/entropy/dashboard')];\
import importlib.util as u;s=u.spec_from_file_location('d',R/'core/hooks/entropy/dashboard/entropy-dashboard.py');\
d=u.module_from_spec(s);s.loader.exec_module(d);from entropy_corpus import tracked_files;\
print({k:len(v) for k,v in d.collect(tracked_files(R,nested=True)).items()})"
```

**The measurement** is the count restricted to the nine checks that existed on 2026-08-13, compared against that day's 95. Everything outside that set is scope, not drift. `size` is split by sub-check, because its width half was born 2026-08-18 and the line cap was not — the same check name covers two different questions on either side of that date, and a third since 2026-09-14, when that half became a document measure (`BLOCK_CHARS`) and stopped counting per line at all.

## Results

| Date | Total | Checks | Files scanned | On the 08-13 check set | Scope | Rot |
|---|---|---|---|---|---|---|
| 2026-08-13 | 95 | 9 | 2125 | 95 | — | baseline |
| 2026-08-14 | 297 | 10 | 2132 | 94 | +203 | **−1** |
| 2026-08-24 | 604 | 19 | 2364 | 111 | +493 | **+16** |

The one-day step the roadmap called the biggest jump is exact arithmetic, not an estimate:
`95 − 1 + 203 = 297`. The 203 is one new check, *source files with no interface stub*, counting a backlog that already existed and had never been looked at. The −1 is a size signal genuinely fixed.
**That day added no drift at all; it added a mirror.**

Today, of the +509 climb, **493 (97%) is scope and 16 (3%) is rot**. The scope is 207 stub findings, 170 column-cap findings from a check that did not exist, and 116 from six further checks.

**Only one of the original nine actually rotted.** Split out, the old check set moved:
`inventories 4→29 (+25)`, `crowding 32→36 (+4)`, `retired 4→5 (+1)`, `naming 4→3 (−1)`, `types 34→30 (−4)`, `size/line-cap 17→8 (−9)`. Without inventories the tree **improved by 9 findings over 11 days**. CONTEXT.md hand-written inventories is the entire drift story.

## What changed

- `ROADMAP.md` item 2 is deleted — it asked this question and the answer is here.
- Its stated hypothesis was **wrong in its mechanism** and the correction is the reusable part: it said the jump day was "also the day the scan went `nested=True`". Nested scanning was already on — that day's scan covered 2132 files, and `tracked_files(nested=False)` returns 707 today, so a 2125-file scan on 08-13 was already reaching the nested repos. Scanned-file count moved +7 that day. The scope was a new **check**, never a wider **tree**.
- The trend line in the dashboard header is therefore comparing across check sets. It is honest about what it measures — *findings on the day* — but it is not a drift meter and must not be read as one, which is what every "entropy: N findings (flat)" hand-off did.

## Limitations

- **The rows are not one instrument re-run; they are three reports read.** The 08-13 and 08-14 numbers come from those days' code, not today's, so a check whose *definition* silently widened without a rename would be counted as rot here. `size` is the one known case and it is split out;
  another would be invisible.
- `inventories 4→29` is measured, but *why* is not. It could be the check widening rather than 25 new hand-written inventories. Nothing here separates those, and the check's own history was not read.
- Whole-tree numbers throughout, root plus nested repos, to match the pre-scatter reports. Today's ISSUES.md header instead splits "N of them here" from the per-repo table.
- **Two of the nineteen checks are not properties of the tree at all.** `branches` and `remotes` read git state, so committing and pushing moves the total without a file changing: this session saw 603 before its own commit and 604 after, from the auto-push alone. Any single-run total carries that noise, and a day's delta smaller than a few findings is not readable.
