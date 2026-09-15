---
name: feedback_measure_before_cutting
description: A file's cost is lines SERVED per session, never lines on disk — and the ablation runs before the cutting campaign, not after
metadata:
  type: feedback
---

Lucas ruled on 2026-09-15, after a session opened intending to pay a 1,134-line size debt: **weigh a
file by what it is served, not by what it holds.** `core/experiments/` is 11% of the repo's lines and
had zero reads in 88 sessions — deleting it would have moved the number and saved nobody any
attention, and it is the WOS paper's data. The order is now **public repo → ablation → cuts**: the
ablation is the instrument that says which mechanism earns its keep, so cutting before it is guessing.

**Why:** a metric that can be satisfied by deleting what nobody opens rewards exactly the wrong
deletion. `core/run tools/wos/size --weighted` prices the corpus in lines served per session; the
disk number stays, as a second reading rather than the verdict.

**How to apply:** before proposing any cut, run `size --weighted` and cut from the top of that
ranking down. A weight of 0 means no session opened the file — a fact about reading, never a licence
to delete. Complements [[feedback_concise_wos]] (which says a session must shrink the workspace) by
answering *shrink WHERE*, and [[feedback_explore_before_cutting]] (which says *shrink WHEN*).
