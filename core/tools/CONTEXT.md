# Tools
> CLI research tools callable via bash; routing block auto-synced on save.

Call any tool via bash:
```
core/tools/search "relativistic raytracing GPU"
core/tools/papers "Schwarzschild geodesics" --cat gr-qc --n 15
core/tools/fetch "https://arxiv.org/abs/1601.02063"
core/tools/parse paper.pdf --pages 1-5
core/tools/hf dataset allenai/c4
```

## Subagent tool

The `subagent` capability is runtime-specific and has no CLI wrapper:

| Runtime | How to spawn a worker agent |
|---------|----------------------------|
| Claude Code | Agent tool — pass `core/agents/<name>.md` content as system prompt |
| Feynman / Pi | Native `subagent` tool with JSON task spec |

## Workspace line-limit checker

Not a research tool — lives in `.hooks/` alongside the commit hooks:

```bash
bash .hooks/check-line-counts.sh             # scan all code files in cwd
bash .hooks/check-line-counts.sh file.py     # check one file
find . -name "*.py" | bash .hooks/check-line-counts.sh --from-stdin
```

Thresholds: `.hooks/line-limits.env`. The `pre-commit` hook runs it automatically; `pre-edit.py` enforces per-edit. Both read the same limits file.

## Adding a tool

1. Create an executable script in `core/tools/`.
2. Add `# Usage: core/tools/<name> <args> — <description>` as the first comment line (after shebang).
3. Save — the routing block below regenerates automatically.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`annotate`](annotate) | — | — | persistent paper annotation store keyed by arXiv ID, DOI, or URL; returns JSON |
| [`calendar`](calendar) | — | — | Google Calendar read-only CLI for workspace OS — commands: auth, upcoming, range, calendars |
| [`calendar_fetch.py`](calendar_fetch.py) | [`calendar_fetch.pyi`](calendar_fetch.pyi) | `get_service`, `list_calendars`, `upcoming_events`, `events_in_range`, `fmt_events` | !/mnt/workspace/.venv/bin/python3 |
| [`code`](code) | — | — | browse and search GitHub repository files; returns JSON or raw text |
| [`code-search`](code-search) | — | — | search code examples and technical documentation via Exa (default) or GitHub code search (--gh); returns JSON |
| [`drive`](drive) | — | — | Google Drive read-only CLI for workspace OS — commands: auth, recent, list, search, download |
| [`drive_fetch.py`](drive_fetch.py) | [`drive_fetch.pyi`](drive_fetch.pyi) | `get_service`, `list_files`, `search_files`, `recent_files`, `download_file` | !/mnt/workspace/.venv/bin/python3 |
| [`fetch`](fetch) | — | — | fetch a URL and return readable plain text; falls back to raw for non-HTML |
| [`gmail`](gmail) | — | — | read-only Gmail integration for workspace OS |
| [`gmail_attachments.py`](gmail_attachments.py) | [`gmail_attachments.pyi`](gmail_attachments.pyi) | `download` | !/mnt/workspace/.venv/bin/python3 |
| [`gmail_fetch.py`](gmail_fetch.py) | [`gmail_fetch.pyi`](gmail_fetch.pyi) | `auth`, `get_service`, `fetch`, `fetch_all` | !/mnt/workspace/.venv/bin/python3 |
| [`gmail_triage.py`](gmail_triage.py) | [`gmail_triage.pyi`](gmail_triage.pyi) | `classify` | !/mnt/workspace/.venv/bin/python3 |
| [`google_auth.py`](google_auth.py) | [`google_auth.pyi`](google_auth.pyi) | `config_dir`, `get_accounts`, `primary_aliases`, `resolve_alias`, `auth` | !/mnt/workspace/.venv/bin/python3 |
| [`hf`](hf) | — | — | query HuggingFace Hub metadata and file contents; returns JSON |
| [`inspect`](inspect) | — | — | generate or update .imgif/.csvif interface file |
| [`inspect-batch`](inspect-batch) | — | — | generate .pngif/.csvif stubs for all assets missing interfaces |
| [`papers`](papers) | — | — | search academic papers via arXiv (default) or Semantic Scholar (--ss); returns JSON |
| [`parse`](parse) | — | — | extract readable text from PDF, DOCX, PPTX, or plain text files; returns raw text |
| [`search`](search) | — | — | web search via Exa; returns JSON results array |
| [`slides`](slides) | — | — | Slidev presentation CLI: auth, new, serve, build, port |
| [`slides_fetch.py`](slides_fetch.py) | [`slides_fetch.pyi`](slides_fetch.pyi) | `get_service`, `get_presentation`, `list_presentations` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_port.py`](slides_port.py) | [`slides_port.pyi`](slides_port.pyi) | `convert` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_shapes.py`](slides_shapes.py) | [`slides_shapes.pyi`](slides_shapes.pyi) | `render_element` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_style.py`](slides_style.py) | [`slides_style.pyi`](slides_style.pyi) | `rotation_deg`, `eff_scale`, `compose_transforms` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_text.py`](slides_text.py) | [`slides_text.pyi`](slides_text.pyi) | `text_html`, `has_content` | !/mnt/workspace/.venv/bin/python3 |
| [`terms`](terms) | — | — | scan .tex files for terminology inconsistencies defined in terms.yaml |
<!-- routing:end -->
