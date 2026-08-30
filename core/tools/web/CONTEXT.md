# web
> Reach the open web: search, fetch a page as text, browse and search code hosts.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`code`](code) | browse and search GitHub repository files; returns JSON or raw text |
| [`code-search`](code-search) | search code examples and technical documentation via Exa (default) or GitHub code search (--gh); returns JSON |
| [`fetch`](fetch) | fetch a URL and return readable plain text; falls back to raw for non-HTML |
| [`hf`](hf) | query HuggingFace Hub metadata and file contents; returns JSON |
| [`search`](search) | unified web search; Exa (keyed) by default, ddgr (no-key) fallback; returns normalized JSON array [{title, url, abstract, score?}] Backend resolution (--backend auto, the default): 1. Exa   — used when ~/.feynman/web-search.json contains an exaApiKey 2. ddgr  — zero-key fallback; also used when Exa errors out (bad key, quota, network) Exa-only flags (--type, --since, --domains, --content) are silently ignored when the ddgr backend is in use. Set --backend exa|ddgr to force one (errors propagate instead of falling back). See SETUP.md §12. |
<!-- routing:end -->
