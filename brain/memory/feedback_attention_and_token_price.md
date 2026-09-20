---
name: feedback_attention_and_token_price
description: "Never design anything that pulls Lucas's attention; and price a feature in always-loaded tokens before proposing it always-on"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e2cddfd9-42e6-48af-9606-650a0dde2f1e
  modified: 2026-09-15T14:31:27.055Z
---

Two rules that arrived together on 2026-09-15, building the notify channel.

**His attention is not a free resource to spend.** Phone addiction is a real cost to him. He refused a phone-push channel outright — *"não quero receber notificações no celular"* — and took a Telegram message from aiwbot instead, because that is a channel **he** opens on his own schedule.
A notification that *fetches* him is a loss even when its content is right. Design the message to *wait*: silent by default, with a reason required to make anything loud.

**He asks what a feature costs in tokens, and "always on" has to survive the number.** His words:
*"isso está custando tokens? e quanto?"*, with his own framing that the feature was "desejável", not essential. Bring the number before he has to ask. Where the cost actually sits: a hook that prints nothing costs **zero**, a statusline costs **zero** (rendered outside the conversation), a registry row costs **zero**. The only real price is prose in `AGENTS.md`, which every session loads — ~71 tokens per norm line, ≈0.026% of a session. See [[feedback_concise_wos]].

**Why:** both are the same rule about scarce resources that are his, not the workspace's — his attention and the always-loaded prompt. Neither is visible in a diff, so neither gets defended unless a session defends it.

**How to apply:** when a feature would add always-loaded prose, measure it first (publish the norm with its switch on and off), show him the number, and offer default-off as a real option — he took it. Put the rule in its own norm governed by its own feature, never as a clause inside an existing norm, so off removes the lines from every prompt instead of leaving them inert.
Related: [[feedback_question_context]], [[feedback_delete_weak_features]].
