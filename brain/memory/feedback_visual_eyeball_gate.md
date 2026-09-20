---
name: feedback-visual-eyeball-gate
description: "Every image-producing pipeline step needs Lucas's visual review (artifact board) before advancing — loops passing their own tests is not enough for visual work"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2f97493f-7bcb-48c5-8f14-cbf62a6a836a
---

Lucas (2026-07-14, isoroll): "I am almost going back to ask you to put me on par of EVERY step so I can check visually" — after the arm_bc marks shipped wrong (screen-grid symbols instead of geometry-anchored) despite the loop passing all its own acceptance tests, and after two cleanup passes missed stale images he had pointed at.

**Why:** visual intent cannot be fully encoded in test criteria; the eyeball is the QC instrument for style/semantics (already codified in core/skills/iso-visual.md — the gap was skipping it between "artifact staged" and "next step").
Also: he is eager to SEE working results; long code-only chains with zero visible content erode trust even when green.

**How to apply:** any loop/step in [[project-isoroll-scene]] (and visual pipelines generally) that produces an image ends with a visual status board (Artifact page, images embedded) + Lucas's explicit OK before the next step spawns.
Prefer shortest path to visible content over parallel machinery-building. Decision log lives in code/isoroll-content/design/RENDER-RESTYLE-MEMO.md (2026-07-14 addendum).
