---
name: research
description: >
  Execute a research workflow from the workspace Core research system.
flow: lit, deepresearch, review, draft, compare, audit, replicate, recipe, summarize, autoresearch, watch
---

Execute a research workflow from the workspace Core research system.

Arguments: $ARGUMENTS

Parse the arguments as `<workflow> [query or path]`. If no workflow is given, print the menu below and stop.

## Workflows

| Command | Flow file | Use when |
|---------|-----------|----------|
| `lit` | `core/flows/lit.md` | literature review on a topic |
| `deepresearch` | `core/flows/deepresearch.md` | full multi-source research brief |
| `review` | `core/flows/review.md` | peer-review simulation of a document or claim |
| `draft` | `core/flows/draft.md` | draft a section or document from evidence |
| `compare` | `core/flows/compare.md` | compare two papers or approaches |
| `audit` | `core/flows/audit.md` | source and citation audit |
| `replicate` | `core/flows/replicate.md` | attempt to replicate a method |
| `recipe` | `core/flows/recipe.md` | step-by-step research recipe |
| `summarize` | `core/flows/summarize.md` | summarize a document |
| `autoresearch` | `core/flows/autoresearch.md` | autonomous multi-turn research loop |
| `watch` | `core/flows/watch.md` | monitor a topic for new developments |

## Execution protocol

1. Read the flow file for the requested workflow (`core/flows/<workflow>.md`).
2. Read `core/tools/CONTEXT.md` to know which tools are available and how to call them.
3. Execute the workflow step by step. Use bash to invoke tools:
   - `core/tools/papers "<query>"` — arXiv / Semantic Scholar
   - `core/tools/search "<query>"` — unified web search (Exa if `~/.feynman/web-search.json` keyed, else ddgr zero-key fallback; flags: `--n`, `--type neural|keyword`, `--since`, `--domains`, `--content`, `--backend auto|exa|ddgr`)
   - `core/tools/fetch "<url>"` — fetch a URL
   - `core/tools/parse <file>` — extract text from PDF/DOCX
   - `core/tools/code list|read|search <owner/repo>` — GitHub
   - `core/tools/annotate set|get|list <id> [note]` — annotation store
4. For steps that require specialist agents, spawn workers using:
   - `core/agents/researcher.md` — evidence gathering
   - `core/agents/reviewer.md` — peer review
   - `core/agents/verifier.md` — citation verification
   - `core/agents/writer.md` — synthesis and drafting
5. Deliver the output in the format the flow specifies.
