---
name: feedback-question-context
description: "every choice put to Lucas carries the context, the problem and the tradeoffs in the question itself and in each option"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f8f7f3b9-9269-4185-8aea-130fb0062c3e
  modified: 2026-08-24T18:22:22.181Z
---

When I put choices to Lucas (AskUserQuestion, plans, verdicts), **the question and every option have
to explain the context, the problem and the tradeoffs in full, without leaning on anything said
earlier in the conversation**. Pointing him at the plan or the thread to go deeper is fine and
encouraged — but the essential part has to be right there.

**Why:** captured by him in `brain/INBOX.md` on 2026-08-24. The moment of the question is one of the
few where his attention is pulled to the conversation; the rest — intermediate progress, huge plans
— he cannot follow in full. His words: *"tem muitas vezes que aparecem coisas nas respostas que eu
simplesmente 'passo direto', não sei do que se trata."* An option that only makes sense to someone
who read the previous 40 turns is a decision made in the dark.

**How to apply:** in the question text, say what the decision is and why it exists now. In each
option, say what happens if it is chosen and what is lost — never just a label. Mark the recommended
one and say why. If an option depends on something decided earlier, restate that thing in one line
rather than referencing it. Holds for any harness, not just Claude Code.
Related: [[feedback-plain-language]], [[feedback-explore-before-cutting]].
