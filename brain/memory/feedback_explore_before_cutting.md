---
name: feedback-explore-before-cutting
description: "while a design question is still open, keep every variant; delete only after Lucas rules — the exploration-phase exception to delete-weak-features"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 14cb1c14-ed22-4a5f-bc84-222f15facde6
  modified: 2026-08-18T19:16:24.421Z
---

While a design question is still open, **keep every option alive**. Lucas, 2026-08-18, on the `ARCHITECTURE.html` views: *"in my opinion we are still at the level of trying different visualizations to cut it later, so no rush in discarding anything yet."* He also asked for more than one approach to be built and compared at real scale rather than betting on one.

**Why:** this is the exploration-phase exception to [[feedback-delete-weak-features]], not a contradiction of it. That rule governs an already-*ruled* weak signal; this one governs the window before the ruling exists. Cutting early destroys the comparison the ruling needs, and a cut made on suspicion is the mistake the context-inflation episode already taught.

**How to apply:** build the variants with real data at real scale, show them together, let Lucas pick. Delete the losers the moment he picks — then [[feedback-delete-weak-features]] takes over and the cut is total, never a demoted "option". Do not volunteer cuts to *existing* views while new ones are still being tried; collect the cut list and hand it to the sitting that rules on it.

Related: [[feedback-visual-eyeball-gate]] — he is the acceptance test, so variants must reach his eyes fast; an artifact board beats a `file://` path.
