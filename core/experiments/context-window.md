# Context window composition
> What fills a session's context window, split by source, and how much of it the workspace controls.

Asked because a session cannot see its own window, so every claim about what fills it was an
estimate — including the ones steering always-loaded context. The suspicion under
it was specific: that the auto-memory store duplicates what `USER.md`, `goals/` and the CONTEXT chain
already carry, and is therefore worth folding.

## Method

```bash
core/tools/wos/session/context                   # this project
core/tools/wos/session/context --project <name>  # any other
```

Reads `~/.claude/projects/<name>/*.jsonl` and `<name>/<session>/subagents/*.jsonl`. Turn-1 context is
exact (the `usage` fields). Per-source attribution is by character count, converted at a ratio
measured **per turn** rather than an assumed constant. Sources the transcript does not label
(`CLAUDE.md`, `AGENTS.md`, `MEMORY.md`) are measured on disk; what remains after both is the
**residual** — harness system prompt plus tool schemas — reported as its own line.

### Method 2 — ablation, for anything hiding inside the residual

The instrument above cannot decompose the residual, so a source suspected of living there is
measured by **building it and not building it**. Each arm is an empty scratch directory holding
nothing but the `.claude/` folder under test; one headless turn is run in each and turn-1 is read
back with the same definition the table uses (`input + cache_read + cache_creation`):

```bash
cd <arm-dir> && claude -p "Reply with exactly: ok" --output-format json \
  | python3 -c 'import sys,json; u=json.load(sys.stdin)["usage"]; print(
      u.get("input_tokens",0)+u.get("cache_read_input_tokens",0)+u.get("cache_creation_input_tokens",0))'
```

Three runs per arm, median reported. **The arm is what the directory contained, and a delta counts
only against another arm run the same day** — absolute turn-1 moves with the CLI version.

## Results

| Date | turn-1 | residual | skills | memory | CLAUDE | agents | SessionStart | chars/tok | Note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-15 | 27,585 | 15,388 (56%) | 4,454 | 1,874 | 1,337 | 1,314 | 2,261 | 2.43 | **Wrong — see below.** First release. |
| 2026-08-15 | 27,585 | 21,162 (77%) | 2,530 | 1,198 | 855 | 754 | 654 | 2.23 | Corrected: sizes the text, not the JSON envelope. |
| 2026-08-15 | 27,585 | 21,419 (78%) | 2,530 | 1,196 | **599** | 754 | 654 | 2.23 | After the cuts. See the two caveats below. |

**Row 1 was inflated 1.6–3.5x, and it is kept because deleting it would hide the failure mode.**
`session_log.py` sized each injected block with `len(json.dumps(att))` — counting JSON escaping — and
`hook_success` blocks store their payload **twice**, in `content` and in `stdout`. The `SessionStart`
hook was worst hit at 3.5x. Guarded now by `test_a_hook_payload_stored_twice_is_counted_once`.

**Growth after turn 1** (corrected run): assistant output 38%, user prompts 12%, `Read` 8.6%,
`Bash` 7.6%, **CONTEXT.md reads 4.6%**. The chain is 851 reads over 98 sessions, 6 median.

**Subagents, measured for the first time**: 47 workers, 1,457 turns, turn-1 **17,738 tok** median
(p25 10,856 · p75 24,133), peak 71,326 median / 315,142 worst, $79 total. They live in
`<session>/subagents/*.jsonl` and were invisible to every earlier report.

**Two caveats on row 3, and the second is a property of the instrument itself.** The `CLAUDE.md`
chain fell 855 → 599 tok because `~/.claude/RTK.md` moved into `SETUP.md`; that source is measured on
disk, so it moves immediately. **The skill listing still reads 2,530 even though six descriptions
were shortened by 525 chars the same day** — everything the transcript labels is a *median over 98
past sessions*, so a change made today only appears as future sessions accumulate. Read the labelled
rows as "what sessions have been paying", never as "what the next session will pay". The residual
rising to 21,419 is the same artefact, not a regression: it is the arithmetic remainder.

### Results 2 — `.claude/commands/`, the mirror that looked like 52 KB of residual

CLI 2.1.234, opus-5, empty scratch dirs. `.claude/` held only what the arm column names.

| Date | arm — what `.claude/` held | turn-1 | vs A | reads as |
|---|---|---|---|---|
| 2026-08-20 | A — nothing | 23,353 | — | the harness alone |
| 2026-08-20 | D — 14 commands, `description:` = one char (350 B) | 23,450 | +97 | 14 names cost 97 |
| 2026-08-20 | C — 14 commands, bodies = one word (2,883 B) | 24,195 | +842 | descriptions cost 745 |
| 2026-08-20 | B — the 14 commands **verbatim (56,376 B)** | 24,197 | +844 | **the bodies cost 2** |
| 2026-08-20 | E — the 14 skills, no commands | 24,195 | +842 | the listing, same text |
| 2026-08-20 | F — skills + mirror (**the live layout**) | 24,195 | +842 | **the mirror adds 0** |
| 2026-08-20 | G — F, every command renamed `zz<name>` | 25,067 | +1,714 | +872 once names differ |

**Two results, and the second is the one that decides.** B−C = **2 tokens** for 53,493 bytes of
command bodies: what a session loads at turn 1 is the frontmatter, and a body is read when the
command is invoked. Had the bodies been folded in, 56 KB of writing would have cost ~16,000 tokens —
the suspicion was wrong by three orders of magnitude. Then F−E = **0**: in the layout we actually
run, the mirror is not merely small, it is free. `mirror.sh` copies each skill file whole, so the
command inherits the skill's `name:`, and the harness lists that name once. G is the control that
names the mechanism rather than assuming it — the same 14 files, renamed `zz*`, cost **+872**.

The 842 tokens are the listing itself, and they are paid by the skills whether or not the mirror
exists. Only ~97 of that is names; the other ~745 is description writing — the same lever the
2026-08-15 row already pulled for ~138 tokens.

### Results 3 — what the tools RETURN, and which floors are ours to set

*"What our own tools print has never been measured, and it is read by an agent"* (ROADMAP § Cost,
closed here). `core/run tools/wos/session/trace` ranks tool results by bytes returned; a Bash call
running one of our own tools is attributed to that tool rather than to Bash, which is the whole
point — a ranking that says `Bash` and stops answers a question about the harness.

2026-09-15, 96 sessions, **23.1M chars returned over 75 tool names**:

| Tool | Chars | Share | Calls | Avg | The floor, and whose it is |
|---|---:|---:|---:|---:|---|
| `Read` | 12.3M | 53.3% | 4,145 | 2,973 | **Ours, and already being paid down.** The interface-stub gate exists to serve a `.pyi` where a source was asked for; [`read-amplification.md`](read-amplification.md) owns the per-file cut. |
| `Bash` | 8.1M | 35.0% | 7,643 | 1,059 | **Ours.** `core/hooks/compact/` rewrites 56% of calls today; the floor is whatever the rewritten command still prints. |
| `ExitPlanMode` | 831k | 3.6% | 98 | 8,479 | Harness. A plan comes back in full as a tool result — 8.5 KB a time, the highest average on the board. Not ours to set. |
| `Edit` | 464k | 2.0% | 2,900 | 159 | **At its floor.** 159 chars is a confirmation; nothing to cut. |
| `WebSearch` · `AskUserQuestion` | 404k | 1.7% | 242 | — | Harness. |
| `Agent` | 166k | 0.7% | 51 | 3,249 | A worker's final report. Its real cost is its own transcript — [`delegation.md`](delegation.md). |
| `core/tools/notes/notion` | 110k | 0.5% | 25 | 4,410 | **Our loudest tool, by average and by total.** A page read as navigable text; the volume is the page. Keep. |
| `core/tools/wos/roundup` | 63k | 0.3% | 113 | 556 | **At its floor by ruling.** Every line is a state fact the next session needs, and which lines exist is the script's own list. |
| `core/tools/web/fetch` · `slides/gslides` | 122k | 0.5% | 49 | — | The fetched page and the deck ARE the payload. Keep. |
| `core/tools/wos/features` | 43k | 0.2% | 76 | 564 | A row per feature, and the registry is the point. Keep. |

**Two tools are 88% of everything returned, and both are the harness's, not ours.** Every tool this
workspace wrote is **2.8% of returned bytes across 61 names**, and the largest is 0.5%. So the
answer to *"what do our own tools cost an agent to read"* is: about one twentieth of what `Read`
alone costs, with no single cut worth taking inside it. **The item is closed by the measurement
refusing it** — the lever is `Read` and `Bash`, which is where the gates already point.

**The first run of this table said 11.2% across 295 names, and it was wrong the way every other
number in this directory has been wrong at least once.** The attribution searched a Bash command for
one of our paths anywhere in it, so `sed -n 1,200p core/tools/wos/roundup` billed 11,003 chars to
roundup — reading a tool's SOURCE counted as that tool printing, and 234 of the 295 "tool names"
were paths that had merely been grepped. The fix anchors the match at the start of a command
segment; the 8.4 points went back to `Bash`, where they were always spent. Guarded by
`test_reading_a_tool_s_source_is_not_that_tool_printing`. This is the third time an instrument here
printed a startling number that did not survive re-deriving it by hand — see § Three corrections in
[`output-cost.md`](output-cost.md), whose lesson is exactly this one.

## What changed

- **The memory-store question is answered: do not fold it.** At ~1,198 tok it is not where the cost
  is. The always-loaded-context item is updated.
- **The cuts were made and are worth ~394 tok** (~256 from `RTK.md` leaving the always-loaded chain,
  ~138 from six skill descriptions), against a scoped ceiling of ~1,600. The rest of the ceiling is
  caveman, which Lucas kept — see [`caveman-cost.md`](caveman-cost.md).
- **The cascade fear is retired.** The CONTEXT.md chain is 4.6% of growth.
- **Cuts were scoped and found small.** Ceiling ~1,600 tok (5.8%). A session in an empty directory
  with no workspace skills still costs 32k, so the workspace adds 4–9k. Only 36% of the skill listing
  is workspace-owned — three harness plugins outweigh every workspace skill combined.
- **`UserPromptSubmit = 16% of growth` was withdrawn as an artifact**, not acted on.
- **Nothing changed: keep `.claude/commands/` exactly as `mirror.sh` writes it.** Deleting the
  mirror would save 0 tokens and lose every slash command. This is the second time this file has
  recorded that a scoped cut was smaller than feared, and the first time the honest answer was
  *zero* — the row exists so the next session stops re-suspecting it.
- **The one live constraint the check found is a naming one.** The mirror is free *because* the
  command keeps the skill's `name:`. Anything that renames a command away from its skill starts
  charging ~60 tokens per entry, so `mirror.sh` copying the file whole is load-bearing, not lazy.
- **A method was added, not just a number.** Method 2 is the general answer to "is X hiding in the
  residual": build an arm without X. The residual stays opaque, but it is no longer unfalsifiable.
- **One norm line in `AGENTS.md` has a price now: 285 chars ≈ 71 tok, ≈0.026% of a 216-turn
  session** (2026-09-15, opus-5 cache read at `session_cost.py`'s rates). Measured by publishing
  one norm with its switch on and off — `core/hooks/routing/norms.py` makes that a one-command
  diff, which is what a norm being switchable buys. Reusable: this prices EVERY future norm, and
  it is the number that let `notify` be decided on evidence rather than on taste.

## Limitations

- **Shares are of *logged* material.** At 2.23 chars/token against a writing rate of 3.8, ~41% of
  growth is material the transcript never records. It is spread across the reported rows in
  proportion, so any single row is an upper bound.
- **A source riding along with that unlogged material claims tokens it never brought.** The
  `UserPromptSubmit` hook read 10.8% of all growth while being **121 characters**. Such rows are
  flagged `†`; a flagged row is never a finding.
- **The residual is opaque.** 77% of turn 1 is harness system prompt and tool schemas, and Method 1
  cannot decompose it. Method 2 can only rule things *out* of it one arm at a time; it has ruled out
  `.claude/commands/` and says nothing about the rest.
- **Method 2's floor is ~210 tokens, and it is unexplained.** Every arm ran bimodal — a run either
  landed on its median or ~210 below it (A 23,145 · B 23,982 · E 23,984 · G 24,860), the same offset
  regardless of arm, so it does not bias a delta but it does set the resolution. A difference under
  ~210 tokens is not a difference. B−C = 2 and F−E = 0 are far under it: read those as *no measurable
  cost*, not as *provably exactly zero*.
- **Method 2 measured `claude -p`, not an interactive session.** Headless mode does load commands
  (arms C/D/G moved), so the listing is not a TUI-only feature — but nothing here proves the two
  modes compose the system prompt identically. The corroboration is indirect: arm A, a bare
  directory with no commands at all, already costs 23,353, while a real workspace session's entire
  residual measured 21,419 — there is no room in that number for 16,000 tokens of bodies.
  Different CLI versions and five days apart, so it is a bound, not a proof.
- **The arms are scratch directories, not this workspace.** They carry no `CLAUDE.md`, no CONTEXT
  chain, no MCP servers and no repo. That is what makes the deltas clean and it is also why the
  absolute turn-1 figures must never be quoted as a workspace session's cost.
- **Observational only.** No arm, no control; nothing here shows a change *caused* anything. See
  [`subagent-context-chain.md`](subagent-context-chain.md) for the one real ablation.
- **One project short name per run.** The tool prints what it skipped.
