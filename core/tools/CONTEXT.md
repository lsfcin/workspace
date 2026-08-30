# Tools
> CLI tools callable via bash, one directory per family; routing block auto-synced on save.

**A family directory is the feature; the tool inside it is the provider.** `mail/gmail`,
`calendar/gcalendar`, `files/gdrive` — swapping a provider changes a leaf, never a family.

Naming rules, the auth-failure protocol, and how to add a tool: [`SPECS.md`](SPECS.md).

Call any tool via bash:
```
core/run tools/web/search "relativistic raytracing GPU"
core/run tools/paper/papers "Schwarzschild geodesics" --cat gr-qc --n 15
core/run tools/mail/gmail sync --since 7
core/run tools/calendar/gcalendar upcoming --days 7
core/run tools/files/gdrive search --account personal "aula"
```

## Subagent tool

The `subagent` feature is runtime-specific and has no CLI wrapper:

| Runtime | How to spawn a worker agent |
|---------|----------------------------|
| Claude Code | Agent tool — pass `core/agents/<name>.md` content as system prompt |
| Feynman / Pi | Native `subagent` tool with JSON task spec |

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`assets/`](assets/CONTEXT.md) | Interface stubs for non-code assets (.imgif / .csvif), one file or a whole paper. |
| [`calendar/`](calendar/CONTEXT.md) | Read what is scheduled. Provider leaf: `gcalendar`. Auth: [`../auth/gauth.py`](calendar/../auth/gauth.py). |
| [`docs/`](docs/CONTEXT.md) | Long-form documents, read and edited in place. Provider leaf: `gdocs` (Google Docs API). |
| [`files/`](files/CONTEXT.md) | Remote file storage: list, search, download, upload. Provider leaf: `gdrive`. |
| [`forms/`](forms/CONTEXT.md) | Surveys and their answers: a form written as a versioned spec, applied in one call. Provider leaf: `gforms`. |
| [`mail/`](mail/CONTEXT.md) | Read a mailbox and triage it. Provider leaf: `gmail`. Auth: [`../auth/gauth.py`](mail/../auth/gauth.py). |
| [`notes/`](notes/CONTEXT.md) | Pages and note databases, read as navigable text. Provider leaf: `notion` (Notion REST API). |
| [`paper/`](paper/CONTEXT.md) | Academic sources and text: search papers, extract text, annotate, check terminology. |
| [`slides/`](slides/CONTEXT.md) | Presentations, read and edited in place. Provider leaf: `gslides` (Google Slides API). |
| [`test/`](test/CONTEXT.md) | The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token, no network. |
| [`verify/`](verify/CONTEXT.md) | Verification contract + patterns for all code projects: tiers T0-T3, script names, dump-oracle rules. Reference |
| [`video/`](video/CONTEXT.md) | Link to navigable text — metadata, captions, transcript, OCR, VLM caption. |
| [`web/`](web/CONTEXT.md) | Reach the open web: search, fetch a page as text, browse and search code hosts. |
| [`wos/`](wos/CONTEXT.md) | Tools that act on the workspace itself: spec ledger, contract check, skill mirrors. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | What must be true of a `core/tools/` feature, and why: how a family is named, what a failure has to hand back, and what work is the agent's rather than Lucas's. |
| [`attachments_util.py`](attachments_util.py) | [`attachments_util.pyi`](attachments_util.pyi) | `safe_name`, `month_dir`, `unique_path` | attachments_util.py — shared filename/dir helpers for Core/tools attachment downloaders (gmail, telegram) |
| [`auth/gauth.py`](auth/gauth.py) | [`auth\gauth.pyi`](auth\gauth.pyi) | `config_dir`, `get_accounts`, `primary_aliases`, `resolve_alias`, `AuthExpired` | gauth.py — Google's leaf of the auth family: shared OAuth2 for every Google-backed tool |
| [`deps.txt`](deps.txt) | — | — | Every external dependency the core/tools surface needs, declared: what installs it, what probes it, and what its absence breaks. Read by core/tools/wos/deps (the probe runner) and by core/tools/test/wos/test_deps.py (the class check). |
| [`gcli.py`](gcli.py) | [`gcli.pyi`](gcli.pyi) | `run`, `fanout`, `auth_command` | gcli.py — the two things every Google-backed CLI does identically: consent, and fan out over accounts |
| [`tool_law.py`](tool_law.py) | [`tool_law.pyi`](tool_law.pyi) | `require` | tool_law.py — the feature switch for core/tools features: the one guard every CLI entrypoint calls |
<!-- routing:end -->
