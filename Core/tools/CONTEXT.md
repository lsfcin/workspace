# Tools
> CLI research tools callable via bash; routing block auto-synced on save.

Call any tool via bash:
```
Core/tools/search "relativistic raytracing GPU"
Core/tools/papers "Schwarzschild geodesics" --cat gr-qc --n 15
Core/tools/fetch "https://arxiv.org/abs/1601.02063"
Core/tools/parse paper.pdf --pages 1-5
Core/tools/hf dataset allenai/c4
```

## Subagent tool

The `subagent` capability is runtime-specific and has no CLI wrapper:

| Runtime | How to spawn a worker agent |
|---------|----------------------------|
| Claude Code | Agent tool — pass `Core/agents/<name>.md` content as system prompt |
| Feynman / Pi | Native `subagent` tool with JSON task spec |

## Adding a tool

1. Create an executable script in `Core/tools/`.
2. Add `# Usage: Core/tools/<name> <args> — <description>` as the first comment line (after shebang).
3. Save — the routing block below regenerates automatically.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`annotate`](annotate) | — | — | persistent paper annotation store keyed by arXiv ID, DOI, or URL; returns JSON |
| [`code`](code) | — | — | browse and search GitHub repository files; returns JSON or raw text |
| [`code-search`](code-search) | — | — | search code examples and technical documentation via Exa (default) or GitHub code search (--gh); returns JSON |
| [`fetch`](fetch) | — | — | fetch a URL and return readable plain text; falls back to raw for non-HTML |
| [`hf`](hf) | — | — | query HuggingFace Hub metadata and file contents; returns JSON |
| [`papers`](papers) | — | — | search academic papers via arXiv (default) or Semantic Scholar (--ss); returns JSON |
| [`parse`](parse) | — | — | extract readable text from PDF, DOCX, PPTX, or plain text files; returns raw text |
| [`search`](search) | — | — | web search via Exa; returns JSON results array |
<!-- routing:end -->
