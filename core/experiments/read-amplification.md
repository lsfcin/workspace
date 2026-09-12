# Read amplification
> Do our own gates make a session read the same file more than once — and what does that cost?

Asked by Lucas (2026-08-15): *"does a session, due to our hooks/gates, re-read the same context file
more than once?"* It is the sharpest question anyone has put to the enforcement layer, because it
points at a cost this workspace **imposes** rather than one it inherits. `context-gate.py` demands a
whole `CONTEXT.md` chain before any file access in a subtree and `pre-read.py` redirects a source
read to its stub; both exist to *save* context and neither had ever been measured doing it.

## Method

```bash
core/tools/wos/session/reads                      # this project, all transcripts
core/tools/wos/session/reads --session <id>       # one session
```

A read's size is the `tool_result` that answers it, never the arguments that requested it — an
offset/limit read of a 2,000-line file costs what it was served, and the interface-first gate exists
precisely so the two differ. Subagent turns are excluded: they carry their own transcripts, and a
worker re-reading a chain its parent already read is a different question.

## Results

| Date | sessions | reads | distinct files | served | re-reads | re-read chars |
|---|---|---|---|---|---|---|
| 2026-08-17 | 80 | 3,234 | 863 | 9,389k chars | 2,371 (73%) | 7,520k (80%) |
| 2026-08-19 | 86 | 3,510 | 873 | 9,943k chars | 2,637 (75%) | 8,033k (81%) |
| 2026-09-11 | 97 | 4,254 | 900 | 12,495k chars | 3,354 (79%) | 10,620k (85%) |

By what was served (2026-08-17):

| What | files | reads | chars | reads per file |
|---|---|---|---|---|
| `CONTEXT.md` chain | 159 | 1,077 | 3,134k | 6.8x |
| other `UPPERCASE.md` (the ledgers) | 85 | 586 | 2,708k | 6.9x |
| source | 374 | 996 | 2,297k | 2.7x |
| prose (lowercase `.md`) | 79 | 236 | 1,091k | 3.0x |
| interface stub | 166 | 339 | 159k | 2.0x |

**The chain is not the amplifier, and that is the answer to the question as asked.** Its 6.8x is
across 80 sessions — **per session it is 1.0-1.2x** for every chain file in the top of the list
(`core/tools/CONTEXT.md` 1.1, `core/skills/CONTEXT.md` 1.0, `core/hooks/CONTEXT.md` 1.0,
`brain/CONTEXT.md` 1.1). That is the gate working exactly as designed: one orientation per subtree
per session, not one per file touched.

**The amplifier is the ledger.** `ROADMAP.md` is the single most expensive read in the workspace —
**101 reads, 877k chars, 3.0 times per session**, more than twice the chars of any other file and
three times the per-session repeat rate of the chain it is usually blamed alongside. Next is
`code/aiwbot/ROADMAP.md` at 3.2/session and `brain/goals/workspace-os.md` at 2.3.

**Stubs are cheap and are being served.** 339 stub reads for 159k chars — 470 chars each against
2,300 for a source read — so the redirect is both live and paying.

## Did sharding the ledger lower its read cost? — unanswerable, and it stays that way

Lucas, watching a session open all seven shards: *"we splited those to avoid reading too much,
clearly the split wasn't enough."* Settling it needed ~2 weeks of ordinary sessions and a comparison
of chars served for the whole `ROADMAP*` family, not the root alone. **Those two weeks are not
available.** The shards lived seven days and the family is one file again (`cfe8833`, nine roadmaps
become one), so the arm the comparison needs does not exist and cannot be had without re-splitting a
file that is under its cap.

What the corpus does hold, read on 2026-09-11 over 97 sessions: the whole family cost **1,743k
chars**, `ROADMAP.md` 1,127k of it, and every shard shows 1.0–2.2 reads per session in its one week
alive. A session really did open several of them, which is what Lucas saw. Sharding moves cost
between family members, and nothing here shows it lowered the total.

## What changed

- **This is the measurement behind cutting the ledger.** A line removed from `ROADMAP.md` is not
  removed once; at 2.5 reads per session it is removed 2.5 times per session, forever. The drain
  on 2026-08-17 took the file 971 → 828 lines in one sitting.
- **It is also the instrument that replaced the scaffold size target** (2026-09-11). The target
  counted files and lines; this counts what a session is served, and the two disagree — a skill body
  is ~2 tokens at turn 1 while the gate-mandated `CONTEXT.md` chain is 43% of every char served.
  What gets cut is now read off the top of this list.
- The `CONTEXT.md`-chain-is-expensive suspicion is retired for the second time, now from the read
  side rather than the growth side (`context-window.md` measured it at 4.6% of growth).

## Limitations

- **Chars, not tokens.** No per-turn ratio is available for a single `tool_result`, and prose and
  source do not convert at the same rate. Compare shares, not totals.
- **Population is every transcript on this machine**, so it grows with every session: shares are
  comparable across rows, totals are not.
- **A re-read is not automatically waste.** The same file at turn 3 and turn 300 may be an honest
  re-grounding after compaction; this measurement cannot see compaction boundaries.
- **Subagent reads are excluded**, so a workflow that fans out looks cheaper here than it is.
- **`Read` only.** A file pulled in by `grep`, `cat` through Bash, or a hook payload is invisible to
  this lens even though it lands in the same context window.
- **The first run of this instrument was wrong, and its own test caught it** — `'ROADMAP.md'.isupper()`
  is `False`, so every ledger read was filed under `prose` and the most expensive file in the
  workspace hid inside the largest bucket. The numbers above are the corrected run; the discipline
  that produced the check is [`SPECS.md`](SPECS.md) § The corollary the cost work paid for twice.
