# 0 — Clarify

## Carry
slug: commands-mirror-cost | branch: feature/roundup-md-cap (SHARED — do not switch) | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `core/tools/wos/session/context` (instrument sanity only) | e2e-cmd: none
criticality: low | verdict: padaria
subtree: research-shaped, run as padaria (see Routing note) | supervision: io-signoff=no arch-review=none
arch-review-supervised=no
criteria:
  C1 — a turn-1 token number for `.claude/commands/` produced by a probe someone else can re-run
  C2 — the probe separates "the listing" from "the 52 KB of bodies", or says it cannot
  C3 — `core/experiments/context-window.md` gains Method / Results / What changed / Limitations content
  C4 — no file outside `core/experiments/context-window.md` and `.craft/` is written
tasks: single padaria body (probe → record → ship)
context: core/experiments/SPECS.md, core/tools/wos/session/CONTEXT.md

## Routing note (Step R0)
The craft tree has four subtrees: padaria · feature · research · architecture. This task is
**empirical measurement of our own harness** — it fits none of them cleanly. `research/*` are
source-gathering shapes (sota, literature, compare, audit); `research/explore.md` is an *optimization*
loop needing a benchmark command and an iteration budget, not a two-arm ablation.
So it is routed by the bakery gate instead, which it passes on every clause: 1 file touched, no new
API, no migration, an existing pattern covers it (`core/experiments/SPECS.md` format + the
`*probe` scratch-project precedent in `~/.claude/projects/`), revert fully undoes it,
criticality=low. **verdict: padaria.**

## Clarify
intent: measure whether `.claude/commands/` (14 mirrored skills, 56,376 B) is folded into turn-1
  context, then decide whether to keep the mirror.
motivation: the cost roadmap's slash-command row. It is the last unmeasured thing that could live inside the
  77% residual of `context-window.md`. Suspicion is not evidence — the 1.6–3.5x inflation row in the
  same file is what cutting on suspicion looks like.
refs: core/experiments/context-window.md § Limitations (the "first thing to look at" line),
  core/tools/wos/skills/mirror.sh, core/tools/wos/session/session_log.py:130 (turn-1 definition)
scope-files: core/experiments/context-window.md
expected-result: a dated Results row + a stated verdict (keep / cut), and a Limitations entry saying
  what the probe cannot prove.
ambition: minimal
criticality: low tolerance: a null result is a fine outcome; an unfalsifiable one is not.
innovation: none
keep-trail: yes
verdict: padaria

## Micro-plan (≤5 lines, padaria)
1. Build 3 scratch projects outside the workspace, identical but for `.claude/commands/`:
   **A** = no dir · **B** = the real 14 files verbatim · **C** = same 14 filenames + same frontmatter
   `description:` lines, bodies replaced by one word.
2. Run `claude -p` once in each with the same trivial prompt and the same flags; read turn-1 from
   the transcript as `input + cache_read + cache_creation` (the definition already in the table).
3. B−A = the whole mirror's cost. C−A = the listing alone. B−C = the 52 KB of bodies.
   Repeat each arm twice; if arms disagree by more than the A-arm's own run-to-run spread, say so.
4. Append the Results row + a `What changed` verdict + a `Limitations` line to
   `core/experiments/context-window.md`. Never write a number outside the file's own table.
5. Stage `core/experiments/context-window.md` and `.craft/` explicitly on the CURRENT branch. No
   branch creation (a second session holds this repo — craft.md § Field Practice, "two loops, one
   repo = worktree fight"). No merge.

## Deviation from the flow, recorded before it happens
Loop 2's Git Flow step (`branch MUST be feature/<slug>` off develop) is **not run**: a concurrent
session owns the working tree, and a checkout would collide. Staying on `feature/roundup-md-cap`
with explicit staging is the orchestrator's instruction and overrides Loop 2 here.

executor: orchestrator (inline, Field Practice "Loop 0 inline when context is hot") model=anthropic/claude-opus-5
tier=max deleg=none
