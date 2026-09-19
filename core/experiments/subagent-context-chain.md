# The CONTEXT.md chain and who pays for it
> Does forcing an agent to read a folder's CONTEXT.md chain change what it does — and should a subagent be forced at all?

Two runs, one question. The 2026-07-23 ablation asked whether the gate makes an agent *safer*; the 2026-08-15 check asked whether the gate even *fires* for a subagent. The second answer reframes the first: the gate was never protecting workers in the way it was assumed to.

Rescued from `tmp/ablation-bench/`, which is gitignored and slated for cleanup — so this file is the only surviving record. The raw run data (`arms/`, `runners/`, `toy-project/`) is still there and has never been in git.

## Method

**Ablation (2026-07-23).** Two arms on a seeded race-condition bug in a toy project, `with-chain` (gate active) vs `without-chain` (`active: false`), each running the reduced `/craft` flow to a commit. Metrics frozen before the run: `task_completed`, `race_committed`, `context_files_read`, `gate_blocks`, tokens, wall clock, subagents spawned. Operator: opencode + glm-5.2.

**Check (2026-08-15).** Spawn one subagent, have it `Read` a file in a folder whose chain the **parent has already fully read**, and record whether the gate fires:

```bash
cat /tmp/claude_ctx_seen_<session_id>.txt   # before and after the spawn
```

The parent-loaded folder is what makes the test binary: a fresh key means the worker re-pays the chain, an inherited key means it is never gated at all.

## Results

| Date | Arm / question | task done | race committed | CONTEXT files read | gate blocks | tokens |
|---|---|---|---|---|---|---|
| 2026-07-23 | with-chain, n=1 | no | **no** | 2 | 0 | 185,674 |
| 2026-07-23 | without-chain, n=1 | yes | **no** | 2 | 0 | 299,252 |
| 2026-08-15 | subagent, parent-loaded folder | — | — | **0** | **0** | — |

**2026-07-23 — hypothesis not supported.** Both arms read the chain **voluntarily**, reaching the same `context_files_read=2`, because the prompt itself mentioned a "documented contract". The gate had nothing left to force, so its effect was unmeasurable against that prompt. Both arms also fixed the race. The `with-chain` failure to ship is a **methodology artifact** — it ran on a 5-minute budget against the other arm's 10.

**2026-08-15 — the gate does not fire for subagents.** A worker inherits the parent's `session_id`, so it inherits `/tmp/claude_ctx_seen_<id>.txt` and reads gated files with **none** of that chain in its own window. Not a cost problem: a *correctness* one, and arbitrary — the worker is ungated only for folders the parent happened to visit, and pays the full chain everywhere else.

## What changed

- **Subagents are exempt from the context gate by decision** (Lucas, 2026-08-15), replacing an exemption that was accidental and partial. The argument is the type system's own: SCHEMA.md rules that constraints live in `SPECS.md` and `CONTEXT.md` carries **routing**, so a worker told to edit one function does not need to know where else it could have gone. `spec-read-gate.py` keeps firing.
- **The orchestrator owns worker context instead**, injected rather than demanded — induce, never block. [`core/hooks/SPECS.md`](../hooks/SPECS.md).
- **The ablation's follow-up design is preserved** below rather than re-derived.

## Follow-up design, if this is ever re-run

From the 2026-07-23 report, unchanged: a prompt that does **not** mention a "documented contract";
no marker flag in the seeder; **n ≥ 4**; equal wall-clock budget per arm; and a **third arm**
(gate-off *and* prompt-off) to separate the gate's effect from the prompt's. That third arm is the one the pilot lacked, and it is why the pilot could not answer its own question.

## Limitations

- **n=1 per arm.** The 2026-07-23 run planned 6 trials and completed 2; a provider quota stopped it.
  Nothing in that row generalises.
- **The two runs are not comparable.** Different harness, different model, different question. They share a file because they share a subject, not a method.
- **The check is a single observation of a mechanism**, not a rate. It shows the gate *can* be bypassed silently; it does not measure how often that matters.
- **The pilot's source report contains corrupted text** — the operating model emitted stray non-English fragments mid-sentence. Figures were taken from the metrics table, not the writing.
