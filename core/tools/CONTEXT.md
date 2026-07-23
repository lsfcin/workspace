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

## Google services auth (Drive / Gmail / Calendar)

Tokens são por `(service, alias)` em `~/.config/workspace-<service>/<alias>.token.json`.
Se um `core/tools/drive|gmail|calendar` falhar com **`RefreshError` / `invalid_grant`
(Token has been expired or revoked)**, o token está morto e o refresh não se recupera
sozinho. Recupere re-consentindo (abre o navegador — precisa de sessão interativa):

```bash
core/tools/drive auth <alias> --reauth            # token de leitura
core/tools/drive auth <alias> --write --reauth    # token de escrita (drive-write)
```

`--reauth` apaga o token stale antes do consentimento. Escrita em Drive (`mkdir`, `put`,
`put --gdoc`) usa o token `drive-write` separado; leitura usa `drive`.

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

| Subdirectory | Description |
|--------------|-------------|
| [`verify/`](verify/CONTEXT.md) | Verification contract + patterns for all code projects: tiers T0-T3, script name |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Slides Pipeline — Specs & Architecture Decisions |
| [`annotate`](annotate) | — | — | persistent paper annotation store keyed by arXiv ID, DOI, or URL; returns JSON |
| [`attachments_util.py`](attachments_util.py) | [`attachments_util.pyi`](attachments_util.pyi) | `safe_name`, `month_dir`, `unique_path` | !/mnt/workspace/.venv/bin/python3 |
| [`calendar`](calendar) | — | — | Google Calendar read-only CLI for workspace OS — commands: auth, upcoming, range, calendars |
| [`calendar_fetch.py`](calendar_fetch.py) | [`calendar_fetch.pyi`](calendar_fetch.pyi) | `get_service`, `list_calendars`, `upcoming_events`, `events_in_range`, `fmt_events` | !/mnt/workspace/.venv/bin/python3 |
| [`code`](code) | — | — | browse and search GitHub repository files; returns JSON or raw text |
| [`code-search`](code-search) | — | — | search code examples and technical documentation via Exa (default) or GitHub code search (--gh); returns JSON |
| [`drive`](drive) | — | — | Google Drive read+write CLI for workspace OS — commands: auth, recent, list, search, download, mkdir, put |
| [`drive_core.py`](drive_core.py) | [`drive_core.pyi`](drive_core.pyi) | `get_service`, `list_files`, `search_files`, `recent_files`, `download_file` | !/mnt/workspace/.venv/bin/python3 |
| [`drive_migrate.py`](drive_migrate.py) | [`drive_migrate.pyi`](drive_migrate.pyi) | `migrate_recursive`, `run` | !/usr/bin/env python3 |
| [`drive_migrate_core.py`](drive_migrate_core.py) | [`drive_migrate_core.pyi`](drive_migrate_core.pyi) | `get_cin_service`, `get_personal_service` | !/usr/bin/env python3 |
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
| [`search`](search) | — | — | unified web search; Exa (keyed) by default, ddgr (no-key) fallback; returns normalized JSON array [{title, url, abstract, score?}] |
| [`slides`](slides) | — | — | Slidev presentation CLI: auth, new, serve, build, port |
| [`slides_fetch.py`](slides_fetch.py) | [`slides_fetch.pyi`](slides_fetch.pyi) | `get_service`, `get_presentation`, `list_presentations` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_port.py`](slides_port.py) | [`slides_port.pyi`](slides_port.pyi) | `convert` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_shapes.py`](slides_shapes.py) | [`slides_shapes.pyi`](slides_shapes.pyi) | `render_element` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_style.py`](slides_style.py) | [`slides_style.pyi`](slides_style.pyi) | `set_theme_colors`, `rotation_deg`, `eff_scale`, `compose_transforms` | !/mnt/workspace/.venv/bin/python3 |
| [`slides_text.py`](slides_text.py) | [`slides_text.pyi`](slides_text.pyi) | `text_html`, `has_content` | !/mnt/workspace/.venv/bin/python3 |
| [`spec-contract-check`](spec-contract-check) | — | — | verify every spec-locked module has a complete SPEC.md contract (Inputs/Outputs/Invariants filled); optionally type-check declared edges. Exit 1 on any gap. See code/SPEC-DRIVE.md. |
| [`spec-scan`](spec-scan) | — | — | ledger of module SPEC.md status (locked|draft|optout|none) |
| [`sync-skills`](sync-skills) | — | — | regenerate skill mirrors from core/skills/*.md |
| [`terms`](terms) | — | — | scan .tex files for terminology inconsistencies defined in terms.yaml |
| [`test/conftest.py`](test/conftest.py) | [`test/conftest.pyi`](test/conftest.pyi) | `pytest_configure` | conftest.py — put core/tools on sys.path and register the network marker for video tests |
| [`test/test_video_core.py`](test/test_video_core.py) | [`test/test_video_core.pyi`](test/test_video_core.pyi) | `FakeProc`, `FakeMedia`, `test_probe_parses_dump`, `test_probe_failure_no_crash`, `test_clean_vtt` | test_video_core.py — T0/T1 unit tests for video_core (no network; fixtures + injected runners) |
| [`test/test_video_relevance.py`](test/test_video_relevance.py) | [`test/test_video_relevance.pyi`](test/test_video_relevance.pyi) | `test_load_goals_parses_header`, `test_load_goals_strips_auto_blocks_and_urls`, `test_load_goals_skips_non_goal_files`, `test_load_goals_missing_dir_is_empty`, `FakeEncoder` | test_video_relevance.py — T1 unit tests for video_relevance (no model download, no network) |
| [`video`](video) | — | — | extract navigable text (metadata/captions/transcript/OCR/VLM caption) from a video or image link; --goals also ranks brain/goals by relevance to what was extracted |
| [`video.SETUP.md`](video.SETUP.md) | — | — | video tool — setup |
| [`video_core.py`](video_core.py) | [`video_core.pyi`](video_core.pyi) | `source_of`, `probe`, `clean_vtt`, `get_captions`, `assemble` | !/mnt/workspace/.venv/bin/python3 |
| [`video_media.py`](video_media.py) | [`video_media.pyi`](video_media.pyi) | `download_audio`, `download_video`, `transcribe`, `ocr_image`, `sample_frames` | !/mnt/workspace/.venv/bin/python3 |
| [`video_relevance.py`](video_relevance.py) | [`video_relevance.pyi`](video_relevance.pyi) | `load_goals`, `default_encoder`, `relevance`, `format_matches` | !/mnt/workspace/.venv/bin/python3 |
<!-- routing:end -->
