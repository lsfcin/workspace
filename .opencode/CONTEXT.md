# opencode
> opencode configuration, plugins, and skills for this workspace.

## Workspace policy plugin

`.opencode/plugins/workspace-policy.js` mirrors the workspace behavioral hooks
defined in `.claude/settings.json` so opencode enforces the SAME policies as
Claude Code: first-line comment, line-count limits, CONTEXT.md line-2
description, facade-first reads, interface-first source reads, and interface
regeneration after edits.

The existing `.hooks/*` scripts remain the single source of truth for policy
logic. The plugin only TRANSLATES opencode's `tool.execute.before`/`after`
events into the stdin-JSON + `CLAUDE_TOOL_NAME`/`CLAUDE_TOOL_INPUT` env schema
the scripts already expect, and maps Claude's exit-2 block convention to
opencode's `throw` from `tool.execute.before`.

Design lifted from the parallel `.hooks/copilot-pre-tool.py` and
`.hooks/copilot-post-tool.py`, which already solve the same translation
problem for a non-Claude agent. Field-name lists (`PATH_KEYS`,
`CONTENT_KEYS`, `OLD_KEYS`, `NEW_KEYS`) are reused verbatim.

### Event → script mapping

| opencode event + tool name | Claude matcher | Script | Block via |
|---|---|---|---|
| `tool.execute.before`, `read` | PreToolUse `Read` | `.hooks/pre-read.sh` | exit 2 → throw |
| `tool.execute.before`, `edit`/`write` | PreToolUse `Edit\|Write` | `.hooks/pre-edit.py` | exit 2 → throw |
| `tool.execute.before`, `edit`/`write` | PreToolUse `Edit\|Write` | `.hooks/facade-scan.py` | (warn only; never exits 2) |
| `tool.execute.before`, `edit`/`write`/`apply_patch` | PreToolUse `Edit\|Write` | `.hooks/facade-gate.py` | exit 2 → throw |
| `tool.execute.after`, `read` | PostToolUse `Read` | `.hooks/facade-tracker.py` | n/a (no block) |
| `tool.execute.after`, `edit`/`write`/`apply_patch` | PostToolUse `Edit\|Write` | `.hooks/post-edit.sh` | n/a (no block) |

### Tool-name mapping (opencode → Claude canonical env value)

| opencode tool | `CLAUDE_TOOL_NAME` | matcher group |
|---|---|---|
| `read` | `Read` | read |
| `edit` | `Edit` | edit |
| `write` | `Write` | edit |
| `apply_patch` | `Edit` | edit (paths parsed from `patchText` `*** ... File:` markers) |

Other opencode tools (`bash`, `grep`, `glob`, `webfetch`, etc.) are not in
`TOOL_MAP` and pass through untouched.

### stdin vs env-var schema (per script, verified by reading each)

- `pre-edit.py`, `facade-scan.py`, `facade-gate.py`, `pre-read.sh` → read JSON
  from **stdin**. Plugin spawns with `spawnSync({input: json})`.
- `post-edit.sh`, `facade-tracker.py` → read JSON from the **`CLAUDE_TOOL_INPUT`
  env var** (not stdin). Plugin sets `env.CLAUDE_TOOL_INPUT = json`.
- All scripts also read `CLAUDE_TOOL_NAME` (values `Edit`/`Write`/`Read`); the
  plugin sets it on every spawn.

### Warning surfacing (known limitation)

opencode has no inline-tool-warning API on `tool.execute.before`. Blocking
messages reach the LLM via `throw` (the only inline channel). Non-blocking
warnings (e.g. `⚠️ INTERFACE STALE` from `pre-read.sh`, `💬 FIRST-LINE MISSING`
from `post-edit.sh`) use two channels:

- `client.app.log({ body: { level: "warn", message } })` — server log entry.
- `client.tui.showToast({ body: { variant: "warning", message } })` — TUI toast.

The LLM does NOT see pre-hook warnings; only the user does. Post-hook messages
(`✓ .pyi regenerated`, etc.) are appended to `output.output` on
`tool.execute.after` so the LLM sees them in the tool result (the only inline
channel for after-hooks).

### Load order

Project-level plugin (`.opencode/plugins/`), loaded after global config and
global plugins. Symmetric with `.claude/settings.json` (project-level Claude
Code hooks). No changes to global `~/.config/opencode/` are made.

### Verifying the plugin

Syntax + export check:
`node --input-type=module -e "import('/mnt/workspace/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"`

End-to-end smoke test (synthetic client, no opencode process needed): see the
test harness in the session that created this file — it covers all seven
scenarios: read-block-with-pyi, read-allow-no-pyi, write-block-no-comment,
write-block-oversized, write-allow-small, edit-allow-then-post-regenerates-pyi,
read-facade-allow-then-tracker-silent.

To validate inside a real opencode session, start opencode in `/mnt/workspace`
and run the test plan from the resume prompt: try to read a `.py` with a current
`.pyi` (expect block), write a new `.py` without a first-line comment (expect
block), edit a `.py` past `BLOCK_LINES` (expect block), edit a `.py` (expect
`.pyi` timestamp updates), edit a `CONTEXT.md`-adjacent dir (expect
`context_synchronizer` runs).

### Files

- `plugins/workspace-policy.js` — the plugin (this file's subject).
- `package.json` — `"type": "module"` + `@opencode-ai/plugin` dependency.
- `skills/` — opencode skill mirror (managed by sync-skills; see
  `core/skills/sync-skills`).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`skills/`](skills/CONTEXT.md) | — |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`index.js`](index.js) | — | — | **facade** — opencode config facade — public surface consumed by plugins/workspace-policy.js. |
| [`plugins/workspace-policy.js`](plugins/workspace-policy.js) | — | `WorkspacePolicy`, `blockMsg` | Workspace policy plugin for opencode. |
| [`wp-helpers.js`](wp-helpers.js) | — | `buildPayloads`, `run`, `warn`, `WORKSPACE`, `HOOKS` | Helpers for the workspace-policy opencode plugin. |
<!-- routing:end -->
