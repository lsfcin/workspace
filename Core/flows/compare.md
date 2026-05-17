---
description: Compare multiple sources on a topic and produce a source-grounded matrix of agreements, disagreements, and confidence.
args: <topic>
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `Core/tools/` for runtime-specific mappings.

- Search: use `web_search`
- Fetch URLs: use `fetch_content`
- Agent delegation: use `subagent` when available
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

Compare sources for: $@

Derive a short slug from the comparison topic (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

Requirements:
- Before starting, outline the comparison plan: which sources to compare, which dimensions to evaluate, expected output structure. Write the plan to `outputs/.plans/<slug>.md`. Briefly summarize the plan to the user and continue immediately.
- Use the `researcher` subagent to gather source material when the comparison set is broad, and the `verifier` subagent to verify sources and add inline citations to the final matrix.
- Build a comparison matrix covering: source, key claim, evidence type, caveats, confidence.
- Generate charts when the comparison involves quantitative metrics. Use Mermaid for method or architecture comparisons.
- Distinguish agreement, disagreement, and uncertainty clearly.
- Save exactly one comparison to `outputs/<slug>-comparison.md`.
- End with a `Sources` section containing direct URLs for every source used.
