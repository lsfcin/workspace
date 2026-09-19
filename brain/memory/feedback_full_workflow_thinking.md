---
name: feedback-full-workflow-thinking
description: "plan isoroll (and similar) work from the full user workflow, not from artifacts — loose ends are the recurring failure"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37054bbf-5abf-46be-b41b-daf4e99d7f67
  modified: 2026-07-30T03:04:31.191Z
---

Lucas, 2026-07-30, on isoroll: "more often than not in this project we've hit dead walls — progress is made but with loose ends, without connections." He asks for planning that keeps the FULL WORKFLOW in mind: how each result connects to the next step, which part the user plays (he wants it minimal), and what the end-user experience feels like.

**Why:** the failure mode isn't slow progress, it's disconnected progress — an agent ships an artifact (an interface, a mask format, a sheet) that nothing downstream consumes, then the next session inherits a dead end. Compounding it:
Claude is not a Foundry expert by nature and has a weak visual eye, so it silently guesses at exactly the two things this project is made of (Foundry runtime behavior, visual quality) instead of verifying them. The iso-painter needed 19 design rounds of Lucas's own eyeballing to reach minimally good UX; he wants that feeling reached with far less of his effort next time.

**How to apply:** define milestones as **user actions**, never artifacts ("Lucas paints a room and walks a token", not "the renderer interface exists") — an interface is frozen by being used end to end, so fold artifact-shaped milestones into the milestone that consumes them. Enumerate and budget the user's touchpoints, and never route a judgement to him that a test could make. Every time he catches something by eye, convert it into a code invariant so that bug class can never come back to him (precedent: the render-union-mask invariant). Prototype interactions in a throwaway rig before coding them in the module, and reuse already-frozen grammar rather than re-deriving it. Never assert Foundry behavior —
verify against the live instance (`verify:full` e2e + `isoroll.dumpZOrderJSON()`); never assert geometry from looking at an image. All of this is written into `code/isoroll-content/ROADMAP.md` § "How this gets used — the workflow is the spec". Related: [[project_isoroll_scene]] [[feedback_visual_eyeball_gate]] [[feedback_delete_weak_features]]
