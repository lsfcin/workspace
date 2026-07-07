---
name: loops
description: >
  Run the loop-engineering flow: develop a feature in file-relayed loops with model autorouting
  (clarify → plan → ground → architecture → TDD → code → user test → ship).
  Invoke with /loops [task or feature request].
---

# /loops

Arguments: $ARGUMENTS

---

## Protocol

1. Read `core/flows/loop-engineering.md` in full.
2. Execute it with the task: $ARGUMENTS. This session is the orchestrator.
3. Spawn each loop as a subagent per the flow's Orchestration section — use the pinned agent types `loop-low` / `loop-medium` / `loop-high` so tier→model routing is structural, not discretionary.
4. Tier `max` is never auto-spawned: pause and tell the user (Fable quota is scarce; the user decides).
5. Hold only verdict lines in this session. Never paste loop file contents here.
