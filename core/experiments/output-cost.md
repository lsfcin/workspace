# Output cost
> Output tokens are more expensive than input — by how much, and where are ours?

Opened by two captures on 2026-08-15: *"de forma geral output tokens são bem mais caros que input
tokens. estudar formas de reduzirmos"* and the Claude Code usage report. Lucas set the method:
research, brainstorm, then repeat refining — *"isso é crítico e deve ser feito com excelência. Não
vamos ser ingênuos."* The plan built on it lived in a side roadmap until 2026-08-17, when the plan
was drained into [/ROADMAP.md](../../ROADMAP.md) and this file absorbed every
number it carried. **This is now the only home for the measurement**, and the list holds only what
is still intended.

**It took three passes and each one cut the previous headline.** That is the finding, as much as any
number below.

## Method

Two commands. The first is the authority for every row in the first table:

```bash
core/tools/wos/session/usage                       # spend split, self-authored share, multiplier
```

Composition of logged output, which `usage` does not print:

```bash
cd ~/.claude/projects/-mnt-workspace && python3 - <<'EOF'
import json, glob, collections
tool = collections.Counter(); prose = 0
for f in glob.glob('*.jsonl'):
    for ln in open(f, errors='replace').read().splitlines():
        try: d = json.loads(ln)
        except: continue
        if d.get('type') != 'assistant' or d.get('isSidechain'): continue
        for b in ((d.get('message') or {}).get('content') or []):
            if not isinstance(b, dict): continue
            if b.get('type') == 'text': prose += len(b.get('text') or '')
            elif b.get('type') == 'tool_use':
                tool[b.get('name', '?')] += len(json.dumps(b.get('input') or {}))
total = prose + sum(tool.values())
print(f'prose {prose/total:.1%}'); [print(f'{k} {v/total:.1%}') for k, v in tool.most_common(5)]
EOF
```

Composition is counted in characters, not tokens, and per content block — so it is unaffected by
the record-duplication bug below, which is a `usage` fault only.

## Results

| Date | turns | spend | output at sticker | self-authored share | bill traceable to it | multiplier | Verdict |
|---|---|---|---|---|---|---|---|
| 2026-08-15 | 21,672 | $3,672 | 14.9% | 75.7% | 86.9% | 5.8x | **Withdrawn.** Every column inflated — see correction 3. |
| 2026-08-16 | 11,381 | $1,765 | 12.9% | 11.5% | 24.8% | **1.9x** | Output is real and secondary. Cache read is 59.1% of the bill. |

Where the billed output token goes (2026-08-16): **35.0% logged** — text and tool-call arguments,
which land in the thread and are re-read every turn — and **65.0% unlogged**, which is thinking plus
anything else the transcript drops, and is paid exactly once.

Composition of the logged 35% (2026-08-16, 11.59M chars):

| Slice | Share of logged output |
|---|---|
| `Bash` arguments | 26.2% |
| `Write` arguments | 25.3% |
| `Edit` arguments | 23.9% |
| writing to the user | 13.7% |
| everything else (`ExitPlanMode`, `AskUserQuestion`, `TodoWrite`, `Read`, `Agent`) | 10.9% |

**"SHUT UP AND WORK" attacks the 13.7%.** Against billed output that is 13.7% × 35% ≈ **4.8%**, and
against the whole bill under 1%. That also bounds [`caveman-cost.md`](caveman-cost.md): caveman
compresses writing, so that is its ceiling.

## Cost by context size — the staircase

The composition above says where an output token goes; this says what a turn costs, and it is the
larger effect by far. Cost of one turn by the context it carried (2026-08-16, same 141-session
population), and what each band adds over the one below it:

| band | $/turn | vs. band below | | band | $/turn | vs. band below |
|---|---|---|---|---|---|---|
| <50k | 0.077 | — | | 200-250k | 0.167 | +13% |
| 50-100k | 0.085 | +10% | | 250-300k | 0.195 | +17% |
| 100-150k | 0.116 | **+36%** ← bend | | 300-400k | 0.244 | +25% |
| 150-200k | 0.148 | +28% | | >400k | 0.326 | +34% |

Flat below 100k, then a climb that never stops — **4.2x from the cheapest band to the dearest**.
**88% of spend is paid above 100k, 56% above 200k**; **72% above 150k and 41% above 250k.** The
mechanism is that every turn re-reads the whole thread: **2.2 Gtok** of cache reads. Long sessions
cost super-linearly in their own length, and the **top decile of sessions is ~46% of total spend**.

**An earlier reading claimed a plateau at 200-300k** (+5%, +8%) and a threshold was set where the
climb was thought to finish. The plateau was an artifact of correction 3's record duplication: bands
whose turns carry more content blocks were counted more times. The corrected curve has no plateau,
which *strengthens* the existing thresholds rather than moving them.

Two facts that decide where a threshold can usefully sit. **Most sessions cross the bend** — median
peak context **136k**, p75 **248k** — so firing at 100k rather than 150k costs almost no extra noise
(52% of sessions against 48%). And **there is runway to act**: after crossing 100k the median session
still has **~85 turns** ahead, enough for a hand-off to repay its re-grounding cost. Warning early
does not cost precision work; that fear priced a session about to end, and at these thresholds the
session is not about to end. Both halves of the response are live —
[`core/hooks/session/context-meter.py`](../hooks/session/context-meter.py) announces the crossings,
[`core/tools/wos/roundup`](../tools/wos/roundup) closes the session; the split is
[`core/SPECS.md`](../SPECS.md) § AD-09.

## Three claims this audit retired

Each was quoted as steering evidence before it was checked against the transcripts.

| Claim | Verdict |
|---|---|
| "59% of usage from subagent-heavy sessions" | **Unmeasured, and its retirement was wrong too.** The audit searched for `Task`; the tool is named **`Agent`**, and it ran **56 times across 12 sessions**. Subagent turns are also absent from the parent transcript by design — they live in `<session>/subagents/*.jsonl`, 48 files that audit never opened. Re-measure with `session/context` before any claim here. |
| "55% from >150k-context sessions" | **Understated** — it is 72%. |
| "25% from `/roundup`" | **~7% was right; 25% was not.** 24 of 119 sessions invoked it; the tail after invocation is ~10%. |

## Three corrections, in the order they were forced

**1. Bash heredocs: 55% → 3.7%** (2026-08-15). First pass: 55% of Bash output is heredoc payload,
with `core/tools/telegram_daemon.py` written whole eight times. Second pass split them by what they
*do*: writes a file (`cat >`/`tee >`) 128 calls / 354,100 chars / 26% of heredoc volume; stdin to an
interpreter (analysis, writes nothing) 430 calls / 599,203 / 44%. Shell-written files are 3.7% of
logged output, not ~15%. What survived is **governance, not cost**: those 128 writes met no gate at
all — `pre-edit.py` and `issues-gate.py` are `PreToolUse: Edit|Write`, and the only Bash gate was a
*read* gate.

**2. RTK: four wrong stories before the test that held** (2026-08-15). Retracted in order: *"we
deleted RTK.md and lost the instruction"*; *"the hook only tracks"*; *"the hook does not rewrite at
all"* — measured as `rtk gain` delta 0; and *"PreToolUse cannot mutate tool input"*, the hypothesis
that delta implied. What is true: `PreToolUse` **does** apply `updatedInput` without requiring
`permissionDecision: "allow"`, and **rtk parses the first line of a payload and nothing else**. The
delta-0 test was submitted as one multi-line Bash call, so its probe commands sat on lines 2 and 3
and never reached rtk. **A negative result is a claim about the probe before it is a claim about the
system** — vary the probe's shape before believing it. Details:
[`core/hooks/compact/SPECS.md`](../hooks/compact/SPECS.md).

**3. The instrument built to end the guessing was itself wrong** (2026-08-16), in two independent
ways that pushed the same direction:

- **A transcript record is not a turn.** Claude Code writes one record per content block and repeats
  the whole `usage` object on each — 22,354 records against 11,370 responses, **1.97x**, with
  `output_tokens` identical across every record of an id. `session_log.walk()` deduped on `requestId`
  from the start and had a test for it; `usage` ran its own loop and did not.
- **Thinking was counted as thread content.** It is billed inside `output_tokens`, but its text is
  never persisted (`{'type': 'thinking', 'thinking': '', 'signature': …}`) and it never re-enters a
  later turn's context. `self_authored()` added raw `output_tokens` to the cumulative thread, which
  drove the ratio to its 1.0 cap within a few turns and reported 75.7%.

The lesson is correction 2's, one turn further out and more uncomfortable: **the check we built to
replace a bad check was never itself checked.** The instrument printed a startling number, the number
was quoted into a roadmap, a hand-off and a limits file, and nothing checked it against a second
method. Correction 1 came from re-reading raw data; correction 2 from varying a check; correction 3
only from re-deriving the tool's own output by hand. Do that once before quoting a new instrument.

## What changed

- `usage` merges records by `requestId` and accumulates only *logged* output into the thread;
  "what counts as one API response" moved to `session_turns.py` with eight tests
  ([`core/tools/test/wos/test_usage.py`](../tools/test/wos/test_usage.py)).
- The output line now prints its logged/unlogged split, so the half that is paid once is visible.
- `ROADMAP.md` § Cost & model routing and `core/hooks/limits.env` had the withdrawn numbers deleted,
  not softened; the side roadmap built on them was drained into that section and this file.
- The re-emit gate was **demoted from a cost item to a governance item**: at 1.9x it is worth ~1% of
  spend, and the ungated-write hole is the whole of its remaining case.

## Limitations

- **The unlogged 65% is a residual, not a measurement.** Thinking text is never in the transcript,
  so it is inferred by subtraction and carries every other unlogged thing with it. Never report it
  as "thinking" alone.
- **Logged tokens are estimated from characters** at a declared 3.6 chars/token
  (`session_turns.CHARS_PER_TOKEN`). It is declared rather than derived because the obvious
  calibration — responses with no thinking block — measures 1.6 chars/token and so is not clean
  either. Tool-call JSON is denser than 3.6, which makes the logged share a **floor**.
- **The self-authored share caps at 1.0 per turn and ignores compaction**, so it remains an upper
  estimate even after the fix.
- **Absolute spend is list price**, and does not reflect a subscription. Ratios are the trustworthy
  part; the ROADMAP § Cost & model routing caveat about the absolute total still stands.
- **Subagent turns are excluded** — they are billed in their own transcripts under
  `<session>/subagents/`, which this measurement does not open.
- **A row will not re-run to the same counts.** The population is every transcript on this machine
  and it grows with every session, so re-running the Method reproduces the *shares* and drifts the
  totals upward. Compare shares across rows; treat turn counts as of their date.
