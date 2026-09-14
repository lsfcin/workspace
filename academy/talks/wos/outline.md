# Talk — workspace-os (WOS) @ SENAI

> Invited by Rafael. Minimum repo — build out when prep starts. WOS = workspace-os
> (Lucas's file-as-source-of-truth personal operating system for driving AI coding agents).

## Status
Seed only (INBOX 2026-07-24). Date, audience level, and duration TBD — confirm with Rafael.

## Opener candidate — the LLM lock-in risk
From [Goju Gottschlich reel](https://www.instagram.com/reel/DbLIZ39D7sT/) (INBOX 2026-07-24):
you build your infrastructure on hosted LLMs, then the provider cuts you off, or changes the
model / pricing / policy internally, with no mechanism to reinstate the working system you had.
Everything you built can disappear overnight. Local SLMs (small language models) are the secure
alternative. → Strong hook into WOS's provider-agnostic, filesystem-is-truth stance and the
local-ai direction (`brain/goals/local-ai.md`, `code/dobra`).

## Arc (draft — to expand)
1. The lock-in / disappearing-infrastructure risk (opener above).
2. Filesystem as source of truth; provider as data, not code.
3. WOS in practice — CONTEXT chain, skills, flows, hooks, the away-from-PC front door.
4. Toward local: SLMs + context folding (dobra) as the escape hatch.

## Prep TODO
- [ ] confirm date / audience / length with Rafael
- [ ] pull reusable material from `brain/goals/workspace-os.md` and `academy/talks/` (Drive import)
- [ ] slides via `core/tools/slides/gslides` (Google Slides, edited in place) once arc is firm
