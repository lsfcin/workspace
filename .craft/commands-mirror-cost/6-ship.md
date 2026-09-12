# 6 — Ship

## Carry
slug: commands-mirror-cost | branch: feature/roundup-md-cap (shared, not created) | root: /mnt/workspace
verdict: padaria | criteria: C1 C2 C3 C4 — all met

## Outcome
question: does `.claude/commands/` (14 files, 56,376 B) cost turn-1 context?
answer: the 53,493 B of bodies cost **2 tokens**; the mirror's marginal cost in the live layout is
  **0**, because each command inherits its skill's `name:` and the harness lists that name once.
decision: **keep the mirror unchanged.** Cutting it saves nothing and loses every slash command.
mechanism control: arm G (same files, renamed `zz*`) costs +872 — so the name-sharing is the reason,
  not an assumption about it.

## Files
- `core/experiments/context-window.md` — Method 2 (the ablation recipe), Results 2 (7 arms),
  a `What changed` verdict, 4 new `Limitations` bullets replacing the now-answered residual bullet.
- nothing else. `ISSUES.md`, `ROADMAP*.md`, `core/hooks/**`, `brain/**` untouched (concurrent session).

## Gates
- `entropy_stores.experiment_hits` → clean (all four required sections present)
- `check-line-counts.sh` → under both thresholds `core/hooks/limits.env` declares
- branch: NOT created. `feature/roundup-md-cap` reused; a checkout would collide with the session
  holding this worktree (craft.md § Field Practice, "two loops, one repo = worktree fight").
- staging: explicit paths only. `extras: pre-existing-dirty` = ISSUES.md, core/hooks/entropy/**,
  core/tools/test/law/entropy/** — another session's work, neither committed nor reverted.

## Not done here
The ROADMAP row is left standing. The orchestrating session deletes it.

executor: orchestrator (padaria, inline) model=anthropic/claude-opus-5 tier=max deleg=none
