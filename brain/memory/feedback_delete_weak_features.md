---
name: feedback-delete-weak-features
description: "Lucas deletes a feature that only produces weak signal rather than keeping it as a hint — remove it from every file and mention, leaving only a short rejection note"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bf93cf97-3cd4-4e88-9d32-45373e9f7e05
  modified: 2026-07-23T15:54:42.939Z
---

When a built feature turns out to give weak or unreliable signal, Lucas's call is to **delete it completely** — code, tests, flags, docs, dependencies, cached weights, and every mention across files — not to keep it around downgraded to "a hint" or "a tie-breaker".

**Why:** a half-trusted feature is worse than none. It still costs context to explain, still invites the next session to lean on it, and its confident-looking wrong answers compete with the method that actually works. Measured example (2026-07-23): an embedding ranker suggesting goal routes for INBOX links was built, dogfooded over ten real links, and deleted the same day — an agent reading the extracted text routed correctly and was already in the loop, so the ranker only added noise.

**How to apply:** when reporting that something underperforms, propose deletion as the default option, not retention-with-caveats. On deletion, leave exactly one short rejection note in the nearest SETUP/SPECS doc: what failed, what was already tried and rejected, and the one condition that would justify revisiting. That note is the deliverable — it stops a future session rebuilding it. Do not leave the design record, benchmarks, or tuning history behind.

Related: [[feedback-visual-eyeball-gate]] (same instinct — measured verdicts over plausible-looking output), [[project-verify-roadmap]].
