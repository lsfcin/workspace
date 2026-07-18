# Workspace Root
> Canonical workspace entrypoint. Read before any task.

- FILESYSTEM = source of truth. No memory, no assumptions.
- IMPROVE WORKSPACE at any opportunity. Findings can be 'existing bad' or 'new good' flows, instructions, skills, etc. Fix it or at least WRITE IT DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- Before declaring a capability is missing or impossible, read [`core/tools/CONTEXT.md`](core/tools/CONTEXT.md) and [`core/flows/CONTEXT.md`](core/flows/CONTEXT.md) — a CLI tool or flow already exists for most research/web/file/Google/PDF/GitHub needs. Same for any task that "would be easier with a tool": check the catalog first, then act.
- If uncertain SEARCH web first via `core/tools/search "<query>"` (bash, any agent, no MCP, no per-agent wiring). Backend resolution is internal: Exa when `~/.feynman/web-search.json` carries an `exaApiKey`, otherwise `ddgr` (DuckDuckGo, no key). Exa-only flags: `--type neural|keyword`, `--since YYYY-MM-DD`, `--domains d1,d2`, `--content` (full page text). Force a backend with `--backend exa|ddgr`. See [SETUP.md §12](SETUP.md#12-unified-web-search-cli-all-agents).
- Workspace repo commits structural files (`AGENTS.md`, `CONTEXT.md`, domain docs). Internal projects use their own git repos.
- PLANS LIVE IN ROADMAPS: any plan (plan mode or otherwise) must be persisted in the target project's `ROADMAP.md` — either inline or as a sub-roadmap file referenced from it. `~/.claude/plans/*` is a scratch copy, never the canonical home.

See [SETUP.md](SETUP.md) for hooks, stubgen, tsc, caveman, and toolchain setup.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`academy/`](academy/CONTEXT.md) | Research, teaching, academic work |
| [`brain/`](brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`branches/`](branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`code/`](code/CONTEXT.md) | Software projects developed under this workspace |
| [`core/`](core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`models/`](models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
