---
name: research
description: >
  Execute a research workflow from the workspace Core research system.
---

Execute a research workflow from the workspace Core research system.

Arguments: $ARGUMENTS

Parse the arguments as `<workflow> [query or path]`. If no workflow is given, print the menu below and stop.

## Workflows

| Command | Flow file | Use when |
|---------|-----------|----------|
| `lit` | `Core/flows/lit.md` | literature review on a topic |
| `deepresearch` | `Core/flows/deepresearch.md` | full multi-source research brief |
| `review` | `Core/flows/review.md` | peer-review simulation of a document or claim |
| `draft` | `Core/flows/draft.md` | draft a section or document from evidence |
| `compare` | `Core/flows/compare.md` | compare two papers or approaches |
| `audit` | `Core/flows/audit.md` | source and citation audit |
| `replicate` | `Core/flows/replicate.md` | attempt to replicate a method |
| `recipe` | `Core/flows/recipe.md` | step-by-step research recipe |
| `summarize` | `Core/flows/summarize.md` | summarize a document |
| `autoresearch` | `Core/flows/autoresearch.md` | autonomous multi-turn research loop |
| `watch` | `Core/flows/watch.md` | monitor a topic for new developments |

## Execution protocol

1. Read the flow file for the requested workflow (`Core/flows/<workflow>.md`).
2. Read `Core/tools/CONTEXT.md` to know which tools are available and how to call them.
3. Execute the workflow step by step. Use bash to invoke tools:
   - `Core/tools/papers "<query>"` — arXiv / Semantic Scholar
   - `Core/tools/search "<query>"` — Exa web search
   - `Core/tools/fetch "<url>"` — fetch a URL
   - `Core/tools/parse <file>` — extract text from PDF/DOCX
   - `Core/tools/code list|read|search <owner/repo>` — GitHub
   - `Core/tools/annotate set|get|list <id> [note]` — annotation store
4. For steps that require specialist agents, spawn workers using:
   - `Core/agents/researcher.md` — evidence gathering
   - `Core/agents/reviewer.md` — peer review
   - `Core/agents/verifier.md` — citation verification
   - `Core/agents/writer.md` — synthesis and drafting
5. Deliver the output in the format the flow specifies.
