---
description: One line — what durable artifact this flow produces.
args: <topic>
type: research-brief
confirm: none
agents: researcher, verifier
---
<!-- Flow template. Fill frontmatter per core/SCHEMA.md; delete disciplines your `type` doesn't require. -->

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `core/tools/` for runtime-specific mappings.

- Search: use `web_search`
- Fetch URLs: use `fetch_content`
- Agent delegation: use `subagent` when available
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

Run this flow for: $@

Derive a short slug from the topic (lowercase, hyphens, no filler words, ≤5 words). Use it for all files.

## Required Artifacts

Every run must leave these on disk:
- `outputs/.plans/<slug>.md`
- `outputs/<slug>.md`
- `outputs/<slug>.provenance.md`   <!-- research-brief/domain only -->

Once work starts, never end with chat-only output. If a capability fails, write a partial artifact with `Verification: BLOCKED`.

## Plan

Write the plan to `outputs/.plans/<slug>.md`.
<!-- confirm: plan → stop and ask "Proceed? Reply yes." | confirm: none → summarize briefly and continue -->

## Scale

Narrow "what is X" → lead-owned direct search, no subagents. Broad/multi-faceted → spawn `researcher` subagents. State the decision in the plan before assigning owners.

## Execute → Deliver

Do the work, write the artifact, then the provenance sidecar. Integrity: read before you summarize; URL or it didn't happen; mark inferred vs verified honestly; no invented sources, numbers, or figures. Verify artifacts exist on disk before the final response.
