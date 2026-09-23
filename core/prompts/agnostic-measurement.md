# Measurement that any harness can do, and the page that shows it

> Session plan, 2026-09-22. Decisions taken with Lucas in conversation; each frente names what will
> exist, why, and the observable that ends it.

## Context

`ROADMAP.md` § Legibility carries one 🔴 item: `ARCHITECTURE.html` is built, and Lucas read it on
2026-09-15 and ruled it *an inventory with better manners*. Redrawing it was the item. Two things
changed that during this session's interview.

**First, the page has a second purpose that was never written down.** Lucas, today: it must make
clear — to him, not only to a stranger — that using the WOS adds to his life. Not marketing. The
page has to show value, not only report contents.

**Second, the number he wants on it cannot be measured on any harness but one.** He wants per-file
reads per session. That number comes from `core/tools/wos/session/*`, and every one of those tools
reads `Path.home()/'.claude'/'projects'` — a transcript only Claude Code writes.

**Root cause of that asymmetry, found 2026-09-22:** `session/*` was built as archaeology — it reads
the artifact a vendor left on disk, so it was bound to one vendor from its first line.
`core/hooks/scoreboard.py` was built as instrumentation — it records the fact at the instant it
happens, inside `feature_law.is_enabled()`, which every harness passes through, and is
vendor-agnostic for free because of where it sits. Same workspace, two answers to "what did this
session do", and only one of them travels. `AGENTS.md` calls symmetry a core value; this is the
asymmetry that value names.

**And the measurement found a live bug while being measured.** 76% of all reads are re-reads — 83%
of every character served. Part of that is the CONTEXT.md chain by design, and part is a defect:
the context gate stores its seen-markers in a directory named by session id (`hook_input.store`),
and a session RESUME issues a new id. The store is born empty, and the gate demands files that are
still whole in the agent's window. Measured in this very session: three CONTEXT.md re-read after
the resume, their markers timestamped minutes after files read the day before. **The gate asks
"did this session read it?" when the question is "is this content in the window?"** — the two agree
only while a session is unbroken.

## Frentes, in dependency order

### 1 🟢 The re-read bug — the marker outlives the id

*What* — the seen-marker store survives a resume, so a chain read once is not demanded again.
*Why* — every resume currently re-reads the whole chain, and the content was never gone.
*Done when* — a resumed session is not asked for a CONTEXT.md it already read, proven by a
regression spec that resumes under a new id and asserts the gate stays quiet.

Critical files: [`core/hooks/hook_input.py`](../../core/hooks/hook_input.py) (`store`, `_mark`,
`_load`), [`core/hooks/read/context-gate.py`](../../core/hooks/read/context-gate.py),
[`core/hooks/session/session-prune.py`](../../core/hooks/session/session-prune.py) — the prune is
what keeps a non-session-scoped store from leaking, so its `MAX_AGE_SECONDS` is the other half of
the design, not an afterthought.

### 2 🟡 Measurement that travels — count at the moment, stop reading transcripts

*What* — file reads recorded where they happen, in
[`core/hooks/read/context-tracker.py`](../../core/hooks/read/context-tracker.py), which already runs
on every `Read` under every harness and already writes one marker per file. It sees everything the
count needs and throws the rest away.
*Why* — the root cause above. This is the same move that made `scoreboard.py` agnostic, applied to
the family that never got it.
*Done when* — the read counts are produced with no transcript read, and a harness with no
`~/.claude` still reports them.

**The price, stated rather than discovered later:** at the moment of the event the hook knows the
file's SIZE IN BYTES, not the tokens the API billed. The transcript knows price; the hook knows
volume. `session/*` keeps its transcript reader for what only a transcript can answer (per-turn
cost, model, cache) and loses the half that was never its job.

### 3 🟡 The matrix — file × day, 365 columns, circular

*What* — one generated TSV: one row per file, 365 columns, one per day of the last year, each cell
a read count. A header names today's column. Lucas's design, with one correction agreed in the
interview: **the columns do not shift.** The pointer moves and wraps, overwriting the column that
falls out of the window. Shifting would rewrite all ~1200 rows daily and commit ~900KB of diff that
means nothing.
*Why* — `AGENTS.md`: cut where a line is READ, not where it sits. The per-session answer dies with
the session, so the question "what cost me most this month" has never been answerable.
*Done when* — `/roundup` updates it with no token spent, and a range (week, month, semester) is one
function summing a span of columns, modulo 365.

Settled in the interview: rows carry the **file name, sorted alphabetically** — a hash saves 2% of
the file and costs its whole legibility, and alphabetical order is what keeps a new row from moving
every row below it. **TSV**, the language `features.txt`, `deps.txt`, `harnesses.txt`,
`scoreboard.tsv` and `described.txt` already speak. A row that zeroes across the whole window is
deleted, which is what holds the file's size still. It is declared in
[`core/hooks/generated.txt`](../../core/hooks/generated.txt) and **read only through a function** —
900KB is ~200k tokens and no agent may open it.

### 4 🔴 ARCHITECTURE.html — one page, two purposes

*What* — the redesign, plus the Claude Design prompt that drives it (Lucas: both in the same
session). One page, decided 2026-09-22 — not two, and not two modes.
*Why* — the 🔴 ROADMAP item, now with the second purpose written down: the page has to answer *is
this well tied, what is loose, what are the flows, the sizes, the sore spots, the imbalances*, AND
make the value of the whole thing legible to the person who owns it.
*Done when* — Lucas reads it and approves it by eye; the shapes that fail are deleted.

Critical files: [`core/tools/wos/diagram/views/diagram_overview.py`](../../core/tools/wos/diagram/views/diagram_overview.py)
(the heat grid — 6 layers × 5 strengths, mostly empty, is the table the item names),
[`diagram_health.py`](../../core/tools/wos/diagram/diagram_health.py) (findings already carry a
`target` column, which is the half that makes a number judgeable and the half to build on).

**The determinism conflict is dissolved, not traded.** It only ever existed while the number entered
raw. With frente 3, the matrix is a workspace file, the page stays a pure function of the
repository, and `--check` survives. Order at close: matrix → diagram → check.

### 5 🟢 One retired token

The 2026-09-14 rename that gave `list` its name survives in exactly one tracked line:
[`entropy_list.py:34`](../../core/hooks/entropy/entropy_list.py#L34), a comment citing that file's
own former name as its example of a retired token hiding inside a compound identifier. The checker
is exempt from itself, so nothing fails. Any other example teaches the same lesson without carrying
the corpse — and this plan tripped the check while describing it, which is the argument in one line.

## How a session on this plan ends

**Lucas, 2026-09-22: frentes 1, 2 and 3 are this session's cut; 4 and 5 wait.** Every session that
takes this plan ends the same way, however far it got:

1. `/roundup`. A parallel session is editing `academy/` — commit its files in whatever state they
   are at `add` time, do not wait for it and do not try to reconcile it.
2. `/handoff`, pointing the next session **at this file by name** and saying which frente it
   resumes at and why the one before it is finished.
3. The handoff repeats this protocol to the session it addresses: if it cannot finish what is left,
   it closes with `/roundup` and a handoff that situates the one after it.

## Deliberately not in this plan

A warning when a session re-reads a file it did not need to. Lucas, 2026-09-22: fix the bug, do not
catalogue it repeating. Revisit as a hook that opens an issue, never as a column in the matrix.

## Verification

Each frente ships its regression spec, and the FIXED gate in `ISSUES.md` is satisfied the same way
it always is: an item flips only when a matching spec exists and passes. Frentes 1–3 are provable by
suite; frente 4 ends at Lucas's eye, which is the gate `feedback_visual_eyeball_gate` names and the
only one a test cannot stand in for.

`core/run tools/test/verify-fast` for the gate work; the full suite at close.
