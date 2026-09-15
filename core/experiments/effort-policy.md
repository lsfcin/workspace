# Effort policy
> Which effort level does which kind of work need, per harness — and what does the headroom cost?

Opened 2026-09-15 to close [/ROADMAP.md](../../ROADMAP.md) § Cost, whose one item said *thinking is
65% of billed output and no instrument here can see it*. The session before it did not attempt the
item and named the risk: effort might not be settable per run from here. It is, in three harnesses,
and one of them reports thinking directly.

This is a different question from [`output-cost.md`](output-cost.md), which asks where our output
tokens are. That file's every row was measured with `effortLevel: medium` in force and none of them
says so — a fact this file exists to stop repeating.

**`core/levels.txt` is the thing under test.** Its `why` column states, per row, what goes wrong
*one level down*. Eight falsifiable claims, none ever tested.

## Method

The knob, per harness, and how a run proves which level it really got:

```bash
claude --effort <low|medium|high|xhigh|max> -p '<frozen prompt>'   # arm reports $CLAUDE_EFFORT
~/.gemini/bin/agy --effort <low|medium|high> --output-format json -p '<frozen prompt>'
```

Cost of a `claude` arm — each arm runs in its own throwaway clone, so it gets its own transcript
project directory and prices alone:

```bash
core/run tools/wos/session/usage --project <arm-project>   # output $, logged/unlogged split
core/run tools/wos/session/trace --project <arm-project>   # turns, clock, loudest tools
```

Cost of an `agy` arm is the `usage` object in its own json: `thinking_tokens` is **reported, not
inferred**. ZCode's knob is `reasoning.variants` in `~/.zcode/v2/config.json`
(`["low","high","max"]`, default `max`, per model); it has no headless run
([`zcode-hook-protocol.md`](zcode-hook-protocol.md)), so its arms are run by Lucas in the UI
against a written rubric and are labelled self-reported.

**Correctness is 0–4, mechanical**: the target test asserts the new law in the right direction ·
`verify.py full` green · the named cure is the mechanism actually implemented · no gate bypassed.

## Results

| Date | Harness | Task | Effort | n | thinking tokens | correct | Verdict |
|---|---|---|---|---|---|---|---|
| 2026-09-15 | agy 3.8-flash | bat-and-ball | low | 3 | 164 / 143 / 95 | 3/3 | Instrument check only — see below |
| 2026-09-15 | agy 3.8-flash | bat-and-ball | medium | 4 | 160 / 139 / 149 / 155 | 4/4 | — |
| 2026-09-15 | agy 3.8-flash | bat-and-ball | high | 4 | 147 / 170 / 170 / 146 | 4/4 | — |

**What the instrument check settled, and it governs every row after it.**

- **The knob reaches the run and is auditable from inside it.** A `claude --effort low` arm printed
  `EFFORT=low` from its own `$CLAUDE_EFFORT`; `agy` refuses a contradicting model id
  (`gemini-3.8-flash-high conflicts with --effort=low`), so its flag and model suffix are two
  spellings of one control, not two knobs.
- **Thinking is task-driven, not knob-driven.** The same `--effort low` that spent 0 thinking
  tokens on *"reply ok"* spent 95–164 on the bat-and-ball. The level sets a propensity, not an
  amount, so a cell measured on a trivial task says nothing about a hard one.
- **Variance at fixed settings is 1.7x** (low: 95 → 164). Adjacent levels overlap completely — low's
  164 beats high's 146. **n=1 per cell measures nothing**, which promotes repetition from a
  nice-to-have to a precondition of the whole design.
- **On a task the bottom level already solves, headroom buys nothing.** 11/11 correct across all
  three levels, for ~18% more thinking from low to high. That is the shape `core/levels.txt`
  asserts for its `search`/`sweep`/`verify` rows, on one toy task and nothing more.

## What changed

- `core/levels.txt` had a false claim deleted: the main thread's level is **not** unreachable by
  configuration. `claude --effort`, `effortLevel` in settings, and `CLAUDE_CODE_EFFORT_LEVEL` all
  reach it, so the 97.5% of spend that file wrote off is addressable after all.
- `core/harnesses.txt` gained an `antigravity` row — a harness Lucas runs, with a CLI (`agy`), a
  matching effort ladder, and better instrumentation for this question than Claude Code has.

## Limitations

- **Every row above is an instrument check on a toy task**, kept because it fixes the method, not
  because it answers the question. A task the bottom level already solves cannot separate levels.
- `thinking_tokens` is direct in `agy` and a **residual** in `claude` — inferred by subtracting
  logged output, so it carries every other untranscribed thing with it
  ([`output-cost.md`](output-cost.md) § Limitations). The two columns are not the same measurement
  and must never be averaged.
- One machine, one version per harness, one model family per harness. Different harnesses run
  different models, so a harness column and a model column cannot be separated here.
- The global `caveman` SessionStart hook fires in every `claude` arm, compressing its prose. It is
  identical across arms so it cancels in a comparison, but it moves the absolute output share.
- ZCode arms are self-reported by a human following a rubric — weaker evidence than an instrumented
  run, and marked as such in any row they reach.
