# Session clock
> How long does a session take, and how much of that was the machine working rather than waiting?

Asked because the three instruments in `core/tools/wos/session/` all measure what a session **costs** and none how long it **took**, so "it ran ten hours" has never been separable from "Lucas was away for eight". A session's span is also the only number in this directory that is not a function of the bill: two sessions of identical cost can differ tenfold in wall-clock, and only one of them is a workflow problem.

## Method

```bash
core/run tools/wos/session/trace                 # every session; --session <id> for one
```

Every `timestamp` in a transcript, sorted; a gap wider than `session_trace.IDLE_SECONDS` is waiting and everything else is working.

**The threshold is DECLARED, not derived**, and that is the honest limit of the measurement rather than a shortcut. A transcript records when a record was *written*, never how long the machine worked on it, so "waiting" can only ever mean a gap over some chosen width. At 120 s a long tool call counts as work and a coffee counts as waiting. Moving the threshold moves both halves together; what it can never do is invent time the span does not contain.

## Results

2026-09-15, 92 sessions with a span over a minute:

| | median | p25 | p75 | max |
|---|---:|---:|---:|---:|
| span | 1.69h | 0.82h | 4.66h | 476.42h |
| working | 0.56h | 0.41h | 0.78h | 2.30h |

**Waiting is 67% of the median session, and 94% of the corpus.** Across all 92, the spans sum to 1,012h and the working halves to 56h.

Three readings:

- **The working half barely varies and the span varies enormously.** Working sits between 0.41h and 0.78h across the middle half of sessions while the span spreads 0.82h to 4.66h — a 6x range against a 2x one. So a session that "took all day" is almost never a session that worked all day;
  it is the same ~30 minutes of machine time with the gaps stretched.
- **The maximum span is 476 hours and it is not an error.** A session resumed three weeks later is one transcript, and its span includes every hour in between. The median is the number to read;
  the mean of spans is meaningless here and is deliberately not reported.
- **This bounds what a faster model could buy.** Machine time is ~6% of the clock on the corpus and a third of the median session. Halving it moves the median session by ~17 minutes and the corpus by ~3%. Latency is not where a session's hours go, which is worth knowing before anything is traded away for speed.

## What changed

The instrument closed ROADMAP § Cost's *"a session's wall-clock has never been split into working and waiting"*, and with it the item that was waiting on it — anything the agent needs Lucas to physically do has to know when a session parked, and a gap over the threshold is that moment.

## Limitations

- **The threshold is a choice, not a measurement.** See Method. Every number here moves with it.
- **A gap is not attributed.** The instrument says a session waited 40 minutes, never whether it waited on Lucas, on a build, or on nothing — the transcript records no reason for a silence.
- **Working time counts a long tool call as work**, which it is, and a model thinking for four minutes as work, which it also is. Neither is separable from the other here.
- **Scoped to one project directory** (`-mnt-workspace`), like every file in this directory.
- **Sessions under a minute are excluded** — a transcript with one event has no span to split.
