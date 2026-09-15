# Delegation
> How often does this workspace actually spawn a subagent, which agent definitions get used, and
> what does the delegated half cost?

## Method

One command, no network:

```bash
core/run tools/wos/session/trace                 # every session; --session <id> for one
```

It joins each `Agent` spawn to the worker transcript it started through
`tool_result.toolUseResult.agentId`, and prices that worker from its OWN transcript under
`<session>/subagents/` — **not** beside the parent in the flat project directory. Reading the flat
directory alone is what produced the retired "nothing has ever been delegated" claim.

The hand-check this instrument owes ([`SPECS.md`](SPECS.md) § The corollary the cost work paid for
twice): **worker transcripts must equal rows.** On 2026-08-17 it held as 37 = 37. On 2026-09-15 it
did **not** — 55 files against 51 spawns — and the four extra are the finding below.

## Results

| Date | Sessions | Delegated | Workers | Worker turns | Cost | Share of spend |
|------|---------:|----------:|--------:|-------------:|-----:|---------------:|
| 2026-08-17 | 152 | 11 (7.2%) | 37 | — | — | — |
| 2026-09-15 | 96 | 17 (17.7%) | 55 | 1,108 | $50.93 | **2.5%** |

| Type | Workers | Turns | Cost | $/worker | Levels the turns actually ran at |
|------|--------:|------:|-----:|---------:|---|
| `general-purpose` | 28 | 612 | $30.11 | 1.075 | opus 396 · sonnet 176 · unpriced 40 |
| `Explore` | 16 | 246 | $9.60 | 0.600 | **opus 195** · unpriced 51 |
| `craft-medium` | 2 | 129 | $7.20 | 3.599 | sonnet 129 |
| `continued` | 4 | 62 | $3.70 | 0.925 | opus 41 · sonnet 11 · haiku 10 |
| `craft-low` | 4 | 51 | $0.32 | 0.080 | haiku 51 |
| `claude-code-guide` | 1 | 8 | $0.00 | — | unpriced 8 |

Three readings, and the third is the one that decides anything:

- **The four that broke the hand-check are `SendMessage` continuations.** A message to a background
  agent opens a fresh worker transcript that no `Agent` tool_use anywhere can claim. They are real
  spend — $3.70 — so they are counted and named `continued` rather than dropped. Dropping them read
  one session as 2.3% delegated where it was 14.3%, which is the direction of error every
  correction in [`output-cost.md`](output-cost.md) had to undo.
- **Level routing works exactly where it is declared, and nowhere else.** Every `craft-low` turn ran
  at haiku and every `craft-medium` turn at sonnet — the only flow that declares a level per step.
  Every `Explore` turn that carried a rate ran at **opus**: a read-only search at the dearest level,
  16 times, because a subagent with no declaration inherits its parent.
- **Routing subagents cannot be the cost answer.** The delegated half is 2.5% of spend. Even sending
  all of it to the cheapest level saves under 2% of the bill; the other 97.5% is the main thread.
  That is the measured case for why the narrow fix — a default subagent model in one settings file —
  was refused (Lucas, 2026-09-14): it is a real cut aimed at a rounding error.

## What changed

The false "nothing has ever been delegated" claim was cut from the wos list's agents item and
replaced with a pointer here. The item was **not** closed on that number: a feature never given a
deliberate trial is not the same as one tried and refused (Lucas, 2026-08-17).

The 2026-09-15 row closed three ROADMAP items at once and re-aimed a fourth — the work→level map is
now known to be worth writing for the main thread, not for the spawns.

## Limitations

- **Scoped to one project directory** (`-mnt-workspace`). Sessions run from another root are not counted.
- **Usage is not value.** Zero spawns of `core/agents/` measures reach and discovery, not worth. The
  research *tools* those flows wrap are heavily used over the same window — `core/tools/web/search`
  319, `video/` 771, `notes/` 325, `paper/parse` 163, `paper/papers` 160 — so the feature is
  exercised daily while the orchestration around it is not. That gap is the finding; its cause is
  not measured here.
- **A worker with no rate is counted and never priced** (`unpriced`, 99 turns here). Its turns are
  in the tables and its dollars are not, so the cost column is a floor.
- **Says nothing about outcome quality.** Whether a delegated turn produced better work than an
  inline one is not in the transcripts.
- **A row will not re-run to the same counts.** The population grows with every session; compare
  shares across rows and treat totals as of their date.
