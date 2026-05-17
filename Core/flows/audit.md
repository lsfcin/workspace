---
description: Compare a paper's claims against its public codebase and identify mismatches, omissions, and reproducibility risks.
args: <item>
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `Core/tools/` for runtime-specific mappings.

- Search: use `web_search`
- Fetch URLs: use `fetch_content`
- Agent delegation: use `subagent` when available
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

Audit the paper and codebase for: $@

Derive a short slug from the audit target (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

Requirements:
- Before starting, outline the audit plan: which paper, which repo, which claims to check. Write the plan to `outputs/.plans/<slug>.md`. Briefly summarize the plan to the user and continue immediately.
- Use the `researcher` subagent for evidence gathering and the `verifier` subagent to verify sources and add inline citations when the audit is non-trivial.
- Compare claimed methods, defaults, metrics, and data handling against the actual code.
- Call out missing code, mismatches, ambiguous defaults, and reproduction risks.
- Save exactly one audit artifact to `outputs/<slug>-audit.md`.
- End with a `Sources` section containing paper and repository URLs.
