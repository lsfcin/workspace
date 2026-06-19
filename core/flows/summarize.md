---
description: Summarize any URL, local file, or PDF using the RLM pattern — source stored on disk, never injected raw into context.
args: <source> [--window-size <chars>] [--overlap <chars>] [--tier1-threshold <chars>] [--tier2-threshold <chars>]
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `core/tools/` for runtime-specific mappings.

- Search: use `web_search`
- Fetch URLs: use `fetch_content` — or fetch to disk via `bash`/`curl` (preferred for RLM, see below)
- Agent delegation: use `subagent` when available
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

Summarize the following source: $@

Derive a short slug from the source filename or URL domain (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

## Why this uses the RLM pattern

Standard summarization injects the full document into context. Above ~15k tokens, early content degrades as the window fills (context rot). This workflow keeps the document on disk as an external variable and reads only bounded windows — so context pressure is proportional to the window size, not the document size.

Tier 1 (below the Tier-1 threshold) is a deliberate exception: direct injection is safe for short inputs.

## Runtime knobs

- `--window-size <chars>` (default: `6000`)
- `--overlap <chars>` (default: `500`)
- `--tier1-threshold <chars>` (default: `8000`)
- `--tier2-threshold <chars>` (default: `60000`)

Validate `window-size > overlap` and `tier1-threshold < tier2-threshold`. Log resolved values once: `[summarize] config window=<w> overlap=<o> tier1=<t1> tier2=<t2>`.

## Step 1 — Fetch, validate, measure

- **GitHub repo URL** (exactly 4 slashes): fetch the raw README instead.
- **Remote URL**: fetch to disk with `curl -sL -o outputs/.notes/<slug>-raw.txt <url>`. Do NOT use `fetch_content` — its return value enters context directly, bypassing the RLM principle.
- **Local file or PDF**: copy or extract to `outputs/.notes/<slug>-raw.txt`. For PDFs, extract text via `pdftotext` or equivalent before measuring.
- **Empty or failed fetch**: stop and surface the error.
- **Existing output**: if `outputs/<slug>-summary.md` already exists, ask the user whether to overwrite.

Measure decoded text characters. Log: `[summarize] source=<source> slug=<slug> chars=<count>`

## Step 2 — Choose tier

| Chars | Tier | Strategy |
|---|---|---|
| < tier1-threshold | 1 | Direct read |
| tier1 – tier2 | 2 | RLM-lite — windowed bash extraction |
| > tier2-threshold | 3 | Full RLM — bash chunking + parallel researcher subagents |

Log: `[summarize] tier=<N> chars=<count>`

## Tier 1 — Direct read

Read `outputs/.notes/<slug>-raw.txt` in full. Summarize directly. Write to `outputs/<slug>-summary.md`.

## Tier 2 — RLM-lite windowed read

Extract `<window-size>`-char windows via bash, using char-offset reads (not line offsets). For each window: extract key claims and evidence, append to `outputs/.notes/<slug>-notes.md`. Synthesize notes into `outputs/<slug>-summary.md`.

## Tier 3 — Full RLM parallel chunks

Chunk the document with overlap, dispatch one `researcher` subagent per chunk (reads only its chunk file, no web search), aggregate summaries, deduplicate boundary claims, write `outputs/<slug>-summary.md`.

Example subagent task per chunk:
```
Read ONLY outputs/.notes/<slug>-chunk-NNN.txt. Extract: (1) key claims, (2) methodology, (3) cited evidence. Do NOT use web search. Mark cross-boundary sentences BOUNDARY PARTIAL. Write to outputs/.notes/<slug>-summary-chunk-NNN.md.
```

## Output format

All tiers produce the same artifact at `outputs/<slug>-summary.md`:

```markdown
# Summary: [document title or source filename]

**Source:** [URL or file path]
**Date:** [YYYY-MM-DD]
**Tier:** [1 / 2 (N windows) / 3 (N chunks)]

## Key Claims
[3-7 most important assertions]

## Methodology
[Approach, dataset, evaluation, baselines — omit for non-research documents]

## Limitations
[What the source explicitly flags as weak or out of scope]

## Verdict
[One paragraph: what this document establishes, its credibility, who should read it]

## Sources
1. [Title or filename] — [URL or file path]

## Coverage gaps *(Tier 3 only)*
[Missing chunk indices]
```

Before you stop, verify on disk that `outputs/<slug>-summary.md` exists.
