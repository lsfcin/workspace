# ARCHITECTURE.html — one page, two purposes

> The measurement this plan needed is in git and in `core/hooks/read/read_matrix.py`. What is left
> is below. Delete this file when frente 4 lands.

## Context

`ROADMAP.md` § Legibility carries one 🔴 item: `ARCHITECTURE.html` is built, and Lucas read it on
2026-09-15 and ruled it *an inventory with better manners*. Two things changed during the 2026-09-22
interview, and the next session needs both.

**The page has a second purpose that was never written down.** Lucas, 2026-09-22: it must make
clear — to him, not only to a stranger — that using the WOS adds to his life. Not marketing, and not
a second audience to design for: he is a consumer of that value too. The page answers *is this well
tied, what is loose, what are the flows, the sizes, the sore spots, the imbalances*, and it has to
make the worth of the whole thing legible while doing it.

**One page**, decided 2026-09-22 — not two, and not two modes.

**The determinism conflict is gone, not traded.** It existed only while a per-session number entered
the page raw. `core/read-matrix.tsv` is now a tracked file folded at every close, so the page stays a
pure function of the repository and `architecture --check` still means what it meant. Order at close
is already wired: matrix → diagram → check.

## What is left

### 4 🔴 The redesign, and the prompt that drives it

*What* — the Claude Design prompt AND its execution in one session (Lucas's call, 2026-09-22).
*Why* — the 🔴 item, now with both purposes written down and the number it wanted available.
*Done when* — Lucas reads it and approves it by eye; the shapes that fail are deleted.

Critical files: [`views/diagram_overview.py`](../tools/wos/diagram/views/diagram_overview.py) — the
heat grid, 6 layers × 5 strengths, mostly empty, is the table the ROADMAP item names;
[`diagram_health.py`](../tools/wos/diagram/diagram_health.py) — its findings already carry a
`target` column, which is what makes a number judgeable and the half to build on.

The read counts are reachable now: `read_matrix.load()` and `read_matrix.span(rows, days)` in
[`core/hooks/read/read_matrix.py`](../hooks/read/read_matrix.py). **Never open
`core/read-matrix.tsv`** — a year of rows is ~200k tokens.

## Deliberately not here

A warning when a session re-reads a file it did not need to. Lucas, 2026-09-22: fix the bug, do not
catalogue it repeating. Revisit as a hook that opens an issue, never as a column in the matrix.

## How a session on this plan ends

However far it got:

1. `/roundup`. A parallel session is editing `academy/` — commit its files in whatever state they
   are at `add` time, do not wait for it and do not try to reconcile it.
2. `/handoff`, pointing the next session **at this file by name**, saying which frente it resumes at
   and why the one before it is finished.
3. The handoff repeats this protocol to the session it addresses: if it cannot finish what is left,
   it closes with `/roundup` and a handoff that situates the one after it.
