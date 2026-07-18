# Workspace Setup

Code quality enforcement + AI-assisted dev infrastructure.
Design principle: **the file system is the source of truth**. No config lives only in machine state or memory — everything versioned here.

## Parity And Enforcement Model

Canonical behavior lives in neutral files under `.hooks/` and `AGENTS.md`. Company-specific files act as shims, discovery points, or startup wiring for Claude, Copilot, VS Code.

Hook can block read/edit/commit → **ENFORCED**. File only injects guidance → **INDUCED**. Present only for compatibility, no enforcement effect → **SKIPPED**.

### Modularization / Interface Tasks

| Task | Canonical files | Claude files | Copilot / VS Code files | Behavior |
|------|-----------------|--------------|--------------------------|----------|
| Add workspace parity config and wrapper scripts | `AGENTS.md`, `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/start-session.sh`, `.hooks/start-session.ps1` | `CLAUDE.md`, `.claude/settings.json` | `.agentrc.json`, `.hooks/copilot-agent.sh`, `.github/copilot-instructions.md` | **ENFORCED** |
| Wire Copilot wrapper to call pre-read / pre-edit / post-edit hooks | `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/copilot-session-start.py`, `.hooks/copilot-pre-tool.py`, `.hooks/copilot-post-tool.py` | `.claude/settings.json` | `.github/hooks/workspace-policy.json`, `.vscode/settings.json` | **ENFORCED** |
| Integrate `context_synchronizer.py` and interface generation into wrapper | `.hooks/post-edit.sh`, `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/context_synchronizer.py` | `.claude/settings.json` | `.github/hooks/workspace-policy.json` | **ENFORCED** |
| Add VS Code tasks / settings to run session-start checks | `.hooks/start-session.sh`, `.hooks/start-session.ps1`, `.hooks/copilot-session-start.py` | `CLAUDE.md` | `.vscode/tasks.json`, `.vscode/settings.json`, `.github/copilot-instructions.md` | **INDUCED** |
| Test workflow: simulate read / edit / commit and fix issues | `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/copilot-pre-tool.py`, `.hooks/copilot-post-tool.py`, `.hooks/pre-commit` | `.claude/settings.json` | `.vscode/tasks.json` | **INDUCED** |

### Additional Files Not Tied To One Task

| File | Why it exists | Behavior |
|------|---------------|----------|
| `AGENTS.md` | Canonical workspace policy + startup anchor for every agent | **INDUCED** |
| `.github/copilot-instructions.md` | One-line Copilot shim pointing to `AGENTS.md` | **INDUCED** |
| `.github/hooks/workspace-policy.json` | VS Code hook registration for Copilot lifecycle events | **ENFORCED** |
| `.vscode/settings.json` | Limits hook-file discovery so Copilot loads workspace hook path, not user-level `.claude` hooks | **INDUCED** |

---

## What Is Configured

### Git Pre-Commit Hook (`.hooks/pre-commit`)
Applied globally via `core.hooksPath`. Fires on every `git commit` across all repos under this workspace.
- Warns on code files ≥ 150 lines; blocks commits on code files ≥ 200 lines (`.js .ts .tsx .py .dart .html .css .scss .tex` — not data files). Shared thresholds in [`.hooks/line-limits.env`](.hooks/line-limits.env)
- Warns when newly staged code file lacks first-line description comment
- **Hard-blocks cross-module imports bypassing facade** (`index` / `__init__`) via `check-facade-imports.py`
- **Auto-syncs CONTEXT.md Routing block** via `context_synchronizer.py` for every dir with staged files, stages result
- Auto-generates `.pyi` stubs for Python files (via `stubgen`), stages them
- Auto-generates `.d.ts` declarations for JS/TS files (via `tsc`) and `.dart.api` stubs for Dart files (via `dart-api-extract.py`), stages them
- Shares staged-file line-count enforcement with `.hooks/check-line-counts.sh`, which can also run manually for workspace-wide audit

### Claude Code Hooks (`.claude/settings.json`)
Fires on every `Edit`, `Write`, `Read` tool call during Claude Code sessions.

| Script | Trigger | Behavior |
|--------|---------|----------|
| `.hooks/pre-edit.py` | PreToolUse: Edit, Write | **Hard-blocks** edits pushing code file past 200 lines; **hard-blocks Write of new files missing first-line description comment** |
| `.hooks/facade-scan.py` | PreToolUse: Write (new files in `code/`) | **Informs** — prints exports already declared in the target module's facade before a new file is created. Warns if exports list is empty (facade needs updating). Not a block. |
| `.hooks/post-edit.sh` | PostToolUse: Edit, Write | Regenerates `.pyi` / `.d.ts` / `.dart.api`; auto-scaffolds `jsconfig.json`/`tsconfig.json` if missing; reminds about missing first-line comment; runs `context_synchronizer.py` |
| `.hooks/pre-read.sh` | PreToolUse: Read | **Hard-blocks** reading source file when interface is current (timestamp check); warns when interface is stale. Reading the interface unlocks the source for the session |
| `.hooks/facade-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Hard-blocks** edits to any `code/` module file until the nearest facade has been Read this session |
| `.hooks/facade-tracker.py` | PostToolUse: Read | Records facade reads to `/tmp/claude_facades_<session_id>.txt`; consumed by `facade-gate.py` |
| `.hooks/context-gate.py` | PreToolUse: Read, Edit, Write, Grep, NotebookEdit | **Hard-blocks** file access until the target subtree's CONTEXT.md chain was Read this session (whole workspace; session-deduped; CONTEXT.md/AGENTS.md targets exempt) |
| `.hooks/bash-context-gate.py` | PreToolUse: Bash | **Hard-blocks** Bash commands naming workspace files in subtrees whose CONTEXT.md chain is unread (closes the cat/grep bypass) |
| `.hooks/context-tracker.py` | PostToolUse: Read | Records CONTEXT.md reads (context-gate state) and interface reads (pre-read source unlock) |
| `.hooks/known-bugs-gate.py` | PreToolUse: Edit, Write (`KNOWN-BUGS.md`) | **Hard-blocks** flipping a bug to FIXED unless a matching `test/**/b<N>-*` regression spec exists |
| `.hooks/spec-read-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Hard-blocks** editing a spec-locked module's files (CONTEXT.md `> spec:` + SPEC.md `status: locked`) until its `SPEC.md` was Read this session; nudges on new files in spec-less `code/` modules (SDD — [code/SPEC-DRIVE.md](code/SPEC-DRIVE.md)) |
| `.hooks/precompact-wipe.sh` | PreCompact | Wipes context seen-markers — CONTEXT chain is re-read after compaction |
| `.hooks/session-prune.sh` | SessionStart | Prunes stale session marker files (>2 days) |

### Git Pre-Commit additions (see [code/VERIFY.md](code/VERIFY.md))

| Gate | Behavior |
|------|----------|
| `verify:fast` contract (1a) | Projects whose package.json declares `verify:fast` must be green — **hard-blocks** commit |
| `.hooks/check-duplication.py` (1b) | jscpd over the committing repo — **hard-blocks** clones involving staged files (75 tokens / 10 lines) |
| Spec-driven module gate (1d) | New module `CONTEXT.md` under `code/` must declare `> spec: <file>` (existing) or `> spec: none` — **hard-blocks** commit otherwise (ratchet; existing modules grandfathered) |

For codegraph setup and bash tool reference, see [`code/SETUP.md`](code/SETUP.md#codegraph).

### Agent Hook Coverage

All canonical enforcement lives in `.hooks/`. Each agent needs a shim that calls them.

| Hook | Git | Claude Code | Copilot | opencode |
|------|-----|-------------|---------|----------|
| Pre-read (interface redirect) | — | `.claude/settings.json` | `copilot-pre-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Pre-edit (size / description) | — | `.claude/settings.json` | `copilot-pre-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Pre-edit facade-scan (new files) | — | `.claude/settings.json` | `copilot-pre-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Pre-edit facade-gate (code/ edits) | — | `.claude/settings.json` | `copilot-pre-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Post-edit (stubs / context sync / codegraph) | — | `.claude/settings.json` | `copilot-post-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Post-read facade-tracker | — | `.claude/settings.json` | `copilot-post-tool.py` ✅ | `.opencode/plugins/workspace-policy.js` ✅ |
| Size / facade import / stub gen / context sync | `pre-commit` ✅ | — | — | automatic (git) |
| ESLint R1-R6 (TS projects under `code/`) | `pre-commit` ✅ hard-block | `post-edit.sh` ✅ warn | ❌ gap | ❌ gap |
| Prettier auto-format (TS projects under `code/`) | — | `post-edit.sh` ✅ | ❌ gap | ❌ gap |
| Context-gate (CONTEXT.md chain) | — | `.claude/settings.json` ✅ | `copilot-pre-tool.py` ✅ | `workspace-policy.js` ✅ |
| Bash context-gate (cat/grep bypass) | — | `.claude/settings.json` ✅ | `copilot-pre-tool.py` ✅ (terminal hints) | `workspace-policy.js` ✅ (bash tool) |
| Context/interface read tracker | — | `.claude/settings.json` ✅ | `copilot-post-tool.py` ✅ | `workspace-policy.js` ✅ |
| KNOWN-BUGS gate (FIXED needs spec) | — | `.claude/settings.json` ✅ | `copilot-pre-tool.py` ✅ | `workspace-policy.js` ✅ |
| Spec-read-gate (spec-locked module edits) | — | `.claude/settings.json` ✅ | `copilot-pre-tool.py` ✅ | `workspace-policy.js` ✅ |
| Spec-driven new-module gate (1d) | `pre-commit` ✅ hard-block | — | — | automatic (git) |
| Duplication gate (jscpd) | `pre-commit` ✅ hard-block | — | — | automatic (git) |
| verify:fast contract gate | `pre-commit` ✅ hard-block | — | — | automatic (git) |

**Session id note:** Claude Code hooks get `session_id` from stdin JSON; the Copilot shims derive a stable `copilot<host-pid>` id. Any new shim must pass a session-stable id in the payload or markers will never dedupe.

**Existing shims:**
- **Claude Code** — `.claude/settings.json` (PreToolUse/PostToolUse matchers).
- **Copilot** — `.hooks/copilot-pre-tool.py` + `.hooks/copilot-post-tool.py` (translate Copilot's tool events to the Claude stdin-JSON + `CLAUDE_TOOL_NAME` env schema).
- **opencode** — `.opencode/plugins/workspace-policy.js` (translates opencode's `tool.execute.before`/`after` events to the same schema; maps Claude exit-2 → opencode `throw`). Helpers in `.opencode/wp-helpers.js`, re-exported through `.opencode/index.js` facade. See [`.opencode/CONTEXT.md`](.opencode/CONTEXT.md) for the full event → script mapping.

**Wiring a new agent — three hook points:**

```
PreTool (Read)  → bash /mnt/workspace/.hooks/pre-read.sh
PreTool (Edit)  → python3 /mnt/workspace/.hooks/pre-edit.py
                  python3 /mnt/workspace/.hooks/facade-scan.py  (write/create only)
                  python3 /mnt/workspace/.hooks/facade-gate.py
PostTool (Edit) → bash /mnt/workspace/.hooks/post-edit.sh
PostTool (Read) → python3 /mnt/workspace/.hooks/facade-tracker.py
```

Each canonical hook expects:
- `file_path` — absolute path to the file being read/edited
- `CLAUDE_TOOL_NAME` env var — `"Read"`, `"Edit"`, or `"Write"`
- Pre-hooks: JSON payload on **stdin**
- Post-hooks: JSON payload in **`CLAUDE_TOOL_INPUT`** env var

Return code `2` = hard block; stdout = message shown to agent. See `copilot-pre-tool.py` and `copilot-post-tool.py` for a complete Python shim implementation, or `.opencode/plugins/workspace-policy.js` for a JS/opencode-plugin shim that maps exit-2 to opencode's `throw`-from-`tool.execute.before` block convention.

**Session isolation caveat**: `facade-gate` and `facade-tracker` use Claude Code's process PID to isolate parallel sessions. Other agents must adapt `get_session_id()` in those scripts to use their own session identifier.

### CONTEXT.md Auto-Sync (`.hooks/context_synchronizer.py`)
Runs on every Claude edit (via `post-edit.sh` — also re-syncs parent dir) and every git commit (via `pre-commit`). Keeps each project's `## Routing` block accurate without manual maintenance:

- **Adds** new files with description from: first-line comment (code files), `description:` YAML frontmatter (`.md` files), usage comment after ` — ` (extensionless executable scripts)
- **Removes** stale entries for deleted files
- **Links** interface files (`.pyi` / `.d.ts` / `.dart.api`) automatically
- **Folds** small subdirs (< 7 files, leaf dirs) into parent Routing block with relative paths
- **Links** large subdirs (≥ 7 files, or has own CONTEXT.md, or has deeper nesting) in Routing block; auto-creates scaffold CONTEXT.md for intermediate dirs with no CONTEXT.md but with sub-hierarchy
- **Warns** when dir exceeds 7 direct files

**Do not edit the sentinel block manually** (`<!-- routing:start/end -->`). Changes overwritten on next sync run.

**Renames not tracked automatically.** Old entry disappears, new file appears with placeholder description. Update description in CONTEXT.md manually after rename.

Manual run: `python3 /mnt/workspace/.hooks/context_synchronizer.py <directory>`

### First-Line Description Convention
Every code file must begin with one-line description comment. `context_synchronizer.py` reads this as canonical description and writes it into CONTEXT.md automatically.

Enforcement model:
- **New file (Write)** → hard block: `pre-edit.py` rejects Write if content doesn't start with description comment
- **Existing file (Edit)** → in-session reminder: `post-edit.sh` checks line 1 after every edit, prints reminder if missing
- **git commit** → warning: `pre-commit` warns when newly staged file lacks comment

### Interface File Generation
Every save of supported source file unconditionally produces interface file. Generation universal — no per-project config required.

| Language | Output | Tool | Notes |
|----------|--------|------|-------|
| Python | `.pyi` | `stubgen` | Auto on every Claude edit and git commit |
| JavaScript | `.d.ts` | `tsc --allowJs --emitDeclarationOnly` | Auto on every Claude edit; `jsconfig.json` auto-scaffolded if missing (IDE use only) |
| TypeScript | `.d.ts` | `tsc --emitDeclarationOnly` | Auto on every Claude edit; `tsconfig.json` auto-scaffolded if no ancestor config found |
| Dart/Flutter | `.dart.api` | `dart-api-extract.py` | Auto on every Claude edit; extracts public class/mixin/method signatures |
| LaTeX | `.texif` | `tex-interface-gen.py` + `tex_interface_parser.py` | Auto on every Claude edit; extracts structure, equations (full), figures/tables/listings, citations, TODO comments, section/subsection opening sentences. Also regenerates `LABELS.md` (cross-file label registry + dangling ref check) in paper root. `.bib` edits warn about missing `reviews/<key>.yaml` files. |

**Enforcement**: `pre-read.sh` hard-blocks reading source file when interface file is current (interface timestamp ≥ source timestamp). Reading interface first is not optional when interface is trustworthy.

**To bypass size gate temporarily**: edit `BLOCK_LINES` in `.hooks/line-limits.env`, perform operation, revert. Both `pre-edit.py` and `check-line-counts.sh` pick up new value immediately.

### Engineering Policies
See [code/CONTEXT.md](code/CONTEXT.md) for full file size policy, modularization strategy, and interface conventions Claude follows during coding sessions.

---

## First-Time Setup (New Machine)

Run once after cloning or moving workspace.

### 1. Wire the Git Hook
```bash
git config --global core.hooksPath /mnt/workspace/.hooks
```
Applies `.hooks/pre-commit` to every git repo on machine.
If workspace is at different path, replace `/mnt/workspace` with actual path everywhere in this file.

Verify:
```bash
git config --global core.hooksPath
# Expected: /mnt/workspace/.hooks
```

### 2. Make Hook Scripts Executable
```bash
chmod +x /mnt/workspace/.hooks/post-edit.sh
chmod +x /mnt/workspace/.hooks/pre-read.sh
chmod +x /mnt/workspace/.hooks/pre-commit
chmod +x /mnt/workspace/.hooks/check-line-counts.sh
chmod +x /mnt/workspace/.hooks/copilot-agent.sh
chmod +x /mnt/workspace/.hooks/start-session.sh
```
(`pre-edit.py`, `copilot-pre-tool.py`, `copilot-post-tool.py`, `copilot-session-start.py`, `dart-api-extract.py` invoked via `python3` — no execute permission needed.)

### 3. Python Interface Generation (stubgen)
```bash
pip install mypy
```
Or using workspace venv:
```bash
/mnt/workspace/.venv/bin/pip install mypy
```
Verify: `stubgen --version` or `/mnt/workspace/.venv/bin/stubgen --version`

### 4. JavaScript/TypeScript Interface Generation (tsc)
```bash
# Via nvm (recommended):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install -g typescript
```
Or if Node installed but global install requires sudo:
```bash
npm install -g typescript --prefix ~/.local
```
Hook checks `tsc` on PATH first, then falls back to `~/.local/bin/tsc`.

Verify: `tsc --version` or `~/.local/bin/tsc --version`

### 5. Claude Code Hooks
No action needed. `.claude/settings.json` versioned in this repo; Claude Code reads it automatically when workspace opened. Hooks in `.hooks/` activate immediately.

### 6. opencode Workspace Policy Plugin
No action needed. `.opencode/plugins/workspace-policy.js` is a project-level plugin; opencode auto-loads it on startup when run from `/mnt/workspace`. It mirrors the Claude Code hooks in `.claude/settings.json` — same `.hooks/*` scripts, same policies (first-line comment, line-count limits, facade-first reads, interface-first source reads, interface regeneration). Translation helpers in `.opencode/wp-helpers.js` (outside `plugins/` so opencode does not auto-load them as a plugin), re-exported through `.opencode/index.js` facade. See [`.opencode/CONTEXT.md`](.opencode/CONTEXT.md) for the event → script mapping and the warning-surfacing limitation (opencode has no inline-tool-warning API on `tool.execute.before`; pre-hook warnings go to `client.app.log` + `client.tui.showToast`, post-hook output is appended to `output.output`).

Verify: `node --input-type=module -e "import('/mnt/workspace/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"` → `function`.

### 7. Codeburn
Run `codeburn optimize` periodically to audit token waste.

### 8. Caveman (Claude Code output compression)

Installs caveman as Claude Code skill (~65% output token savings). Requires Node ≥18. Safe to re-run.

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
```

**Windows (PowerShell — run as normal user, not admin):**
```powershell
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/src/hooks/install.ps1 | iex
```
If execution policy blocks: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first.

**Set default mode** via caveman's config:

Linux / macOS:
```bash
mkdir -p ~/.config/caveman && echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\caveman" | Out-Null
'{"defaultMode": "full"}' | Set-Content "$env:USERPROFILE\.config\caveman\config.json"
```

Change `"full"` to `"lite"`, `"ultra"`, or `"off"` to adjust. `"full"` is caveman's built-in default — config file optional but makes setting explicit and reproducible.

**Add the `caveman-compress` shell function:**

Linux / macOS — append to `~/.bashrc` (or `~/.zshrc`):
```bash
cat >> ~/.bashrc << 'EOF'

# caveman-compress shortcut
caveman-compress() {
  local CLAUDE_BIN
  CLAUDE_BIN="$(dirname "$CLAUDE_CODE_EXECPATH")"
  (cd ~/.claude/skills/caveman-compress && PATH="$CLAUDE_BIN:$PATH" python3 -m scripts "$1")
}
EOF
source ~/.bashrc
```

Windows — append to PowerShell profile (`$PROFILE`):
```powershell
Add-Content $PROFILE @'

# caveman-compress shortcut
function caveman-compress {
    param([string]$File)
    $claudeBin = Split-Path $env:CLAUDE_CODE_EXECPATH
    Push-Location "$env:USERPROFILE\.claude\skills\caveman-compress"
    $env:PATH = "$claudeBin;$env:PATH"
    python3 -m scripts $File
    Pop-Location
}
'@
```

Run `/caveman-compress <file>` on CONTEXT.md files periodically to cut input tokens.

**Verify:** open Claude Code session — `[CAVEMAN] ⛏` badge should appear in statusline.

**Agent integration pattern — installed vs induced:**
Every agent in this workspace should activate caveman via one of two mechanisms:

| Mechanism | Agent | How |
|-----------|-------|-----|
| **Installed** | Claude Code | `SessionStart` + `UserPromptSubmit` hooks in `~/.claude/settings.json` call `caveman-activate.js`. Auto-activates every session. |
| **Induced** | Copilot | `copilot-session-start.py` reads `~/.config/caveman/config.json` and injects rules as `additionalContext` at session start. |

When adding new agent: if it supports session-start hooks or context injection, add caveman injection there following induced pattern in `.hooks/copilot-session-start.py`. Both mechanisms read same config file — one toggle controls all agents.

> **New agent checklist:** consult [caveman INSTALL.md](https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md) for target agent (e.g. OpenCode → `npx -y github:JuliusBrussee/caveman -- --only opencode --with-init` generates `.opencode/AGENTS.md` and `AGENTS.md`). Cross-check against induced pattern here to avoid duplicating rule injection.

Run `caveman-compress <file>` on CONTEXT.md files periodically to cut input tokens.
Responses use caveman compression by default. Deactivate for a session: say "stop caveman" or "normal mode". To change the default, see `SETUP.md §6`.

### 10. ESLint + Prettier for TypeScript Projects under `code/`

Install project-local ESLint and Prettier in every TS project that has an `eslint.config.js`:

```bash
cd /mnt/workspace/code/isoroll-module && npm install
cd /mnt/workspace/code/voti && npm install
```

Each project imports rules from the shared config at `code/eslint.shared.js`. ESLint is run from the project root using `node_modules/.bin/eslint` — no global install needed.

Verify:
```bash
# Confirm ESLint binary present
ls /mnt/workspace/code/isoroll-module/node_modules/.bin/eslint
ls /mnt/workspace/code/voti/node_modules/.bin/eslint

# Run lint manually
cd /mnt/workspace/code/isoroll-module && npm run lint
```

### 9. Local LaTeX Toolchain (for `academy/papers/`)

See [academy/SETUP.md](academy/SETUP.md).

### 11. RTK (token-optimized CLI proxy, all agents)

[rtk-ai/rtk](https://github.com/rtk-ai/rtk) — Rust CLI proxy that filters/compresses dev-command output (git, test runners, docker, etc.) before it reaches an agent's context: 60-90% token savings, complementary to caveman (which compresses the agent's own output, not tool output). Apache 2.0, single static binary, no deps.
**Install the binary** (per machine, not versioned):
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
```
Installs to `~/.local/bin/rtk`. Verify: `rtk --version`.

**Claude Code** — dual-wired:
- Project-scoped hook already versioned in `/mnt/workspace/.claude/settings.json` (`"Bash"` matcher runs `rtk hook claude` alongside `bash-context-gate.py`) — works immediately after clone, no action needed.
- Global patch, for Claude Code sessions outside this workspace:
  ```bash
  rtk init --global --auto-patch
  ```
  Additive — only inserts a `PreToolUse`/`Bash` block into `~/.claude/settings.json`; does not touch existing `SessionStart`/`UserPromptSubmit`/`statusLine` keys (e.g. caveman hooks). Takes an automatic `.bak` backup. Verify: `rtk init --show`.

**OpenCode** (global plugin — no project-scoped variant exists for rtk):
```bash
rtk init --global --opencode
```
Writes `~/.config/opencode/plugins/rtk.ts` (`tool.execute.before` hook). Coexists with this workspace's own project-local `.opencode/plugins/workspace-policy.js` — separate files, both auto-load.

**Pi** (global extension) — **requires a manual peer-dependency fix**, rtk's generated extension doesn't work out of the box:
```bash
rtk init --agent pi --global
mkdir -p ~/.pi/agent/extensions   # if rtk didn't already create it
cd ~/.pi/agent/extensions
echo '{"name":"pi-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
Why: the generated `~/.pi/agent/extensions/rtk.ts` does `import type { ExtensionAPI } from "@earendil-works/pi-coding-agent"`, but Pi's extension loader resolves it as a real `require()` (type-erasure doesn't happen), and Node resolves `node_modules` relative to the extension file's own directory — not from wherever `pi` itself is installed. Without the local `node_modules`, loading fails with `Cannot find module '@earendil-works/pi-coding-agent'`, even if that package is installed globally. Verify: `pi -e ~/.pi/agent/extensions/rtk.ts --no-session` — no output/exit 0 = loaded; an `Error: Failed to load extension` line means the peer-dep step above is missing.

**Feynman** (research agent, [feynman.is](https://www.feynman.is/) / [companion-inc/feynman](https://github.com/companion-inc/feynman)) — not in rtk's official supported-agent list, but Feynman is built directly on Pi (same `ExtensionAPI`/`tool_call` event model, ships its own `PI_CODING_AGENT_DIR` env override pointing Pi's loader at `~/.feynman/agent` instead of `~/.pi/agent`). Wired by parity, same peer-dep gotcha applies:
```bash
mkdir -p ~/.feynman/agent/extensions
cp ~/.pi/agent/extensions/rtk.ts ~/.feynman/agent/extensions/rtk.ts
cd ~/.feynman/agent/extensions
echo '{"name":"feynman-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
```
**Unverified**: Feynman has no `-e`/dry-run flag to confirm extension load non-interactively (unlike raw `pi`). First real Feynman session should be checked for a `[rtk] rtk binary not found` or `Failed to load extension` warning on startup; absence of either is the confirmation signal.

**GitHub Copilot** — already versioned, dormant until Copilot itself is installed on a machine:
- `.github/hooks/rtk-rewrite.json` (hook config, `rtk hook copilot`)
- `<!-- rtk-instructions -->` block appended to `.github/copilot-instructions.md`

No action needed after clone; both are inert config files until Copilot (VS Code extension or CLI) is present. Not independently verified end-to-end on this machine — Copilot isn't installed here.

**Uninstall** (any target): `rtk init --uninstall [--global] [--copilot|--opencode|--agent pi]`.

---

### 12. ddgr web-search CLI (all agents)

`ddgr` (DuckDuckGo from the terminal) — zero-API-key web search callable from any agent's bash. Wrapped by [`core/tools/web`](core/tools/web) as the default search fallback. When an Exa key is configured at `~/.feynman/web-search.json`, [`core/tools/search`](core/tools/search) is the upgrade (semantic/neural ranking, domain filtering, date filters, full-content mode).

**Why both:** `web` always works (no key, no quota). `search` gives better ranking when configured. Canonical guidance in [`AGENTS.md`](AGENTS.md) — every agent reads it at session start, no per-agent wiring.

**Install** (per machine, not versioned — it's a system package):
```bash
sudo apt install -y ddgr
```
(Optionally `pipx` for non-Debian: `sudo apt install -y pipx && pipx install ddgr`.)

**Verify:**
```bash
ddgr --version                          # expected: 2.2 or later
core/tools/web "test query" --n 3       # expected: JSON array of results
```

**Usage from any agent (bash):**
```bash
core/tools/web "<query>"                       # JSON, 10 results, region us-en
core/tools/web "<query>" --n 5                 # fewer results
core/tools/web "<query>" --region de-de        # other region (DDG region codes: duckduckgo.com/params)
core/tools/web "<query>" --text                # text mode (intermittent HTTP 202 from DDG in piped use — JSON is the reliable default)
WEB_RETRIES=8 WEB_REGION=uk-en core/tools/web "<query>"   # tuning via env
```

**Quirk — DDG HTTP 202:** DuckDuckGo intermittently returns HTTP 202 (Accepted, empty body) for non-interactive / piped requests, especially after a burst of calls from the same IP. `core/tools/web` retries with exponential backoff (`WEB_RETRIES`, default 5) and emits `[]` on final failure so callers can branch. If `web` consistently returns `[]`, wait 30–60s and retry, or fall back to `core/tools/fetch <url>` with a specific URL.

**Per-agent wiring:** none. Every agent's existing bash hook (Claude Code, opencode, Copilot, Feynman) already passes bash commands through to the system shell — `core/tools/web` works the moment `ddgr` is installed. Add a one-line note in any new agent's system prompt pointing at [`AGENTS.md`](AGENTS.md) so the search guidance is discoverable.

---

## Per-Project: Interface Generation Notes

**JavaScript / TypeScript**: no manual setup. Hook auto-scaffolds `jsconfig.json` (JS) or `tsconfig.json` (TS, walks up to git root first) on first file write. Config files for IDE tooling only — hook generates declarations via direct CLI regardless.

**Dart**: no setup. `dart-api-extract.py` runs on every `.dart` save, requires only Python 3 (no Dart SDK).

**Python**: requires `stubgen` (mypy). See Step 3.

---

## Verification

```bash
# 1. Git hook is wired
git config --global core.hooksPath
# Expected: /mnt/workspace/.hooks

# 2. stubgen is available
stubgen --version || /mnt/workspace/.venv/bin/stubgen --version

# 3. tsc is available
tsc --version

# 4. Claude Code hooks are configured
grep -c "hooks" /mnt/workspace/.claude/settings.json
# Expected: > 0

# 4b. opencode workspace-policy plugin parses
node --input-type=module -e "import('/mnt/workspace/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"
# Expected: function

# 5. Hook scripts are executable
ls -la /mnt/workspace/.hooks/post-edit.sh /mnt/workspace/.hooks/pre-read.sh /mnt/workspace/.hooks/pre-commit /mnt/workspace/.hooks/check-line-counts.sh
```

ESLint / Prettier verification:
```bash
# ESLint binary present
ls /mnt/workspace/code/isoroll-module/node_modules/.bin/eslint

# Full lint pass on isoroll-module
cd /mnt/workspace/code/isoroll-module && npm run lint

# Write a bad TS file and confirm violation detected
echo '// test\nconst x = foo(bar());' > /tmp/test-lint.ts
cd /mnt/workspace/code/isoroll-module && node_modules/.bin/eslint /tmp/test-lint.ts
# Expected: "2 calls in one statement" error

# Attempt commit with violation — should be blocked by pre-commit §10
```

Behavioral verification (inside Claude Code session):
- Edit `.py` file → `.pyi` regenerates immediately (visible in shell output)
- Edit `.js` file → `.d.ts` regenerates; `jsconfig.json` auto-created if missing
- Edit `.ts` file → `.d.ts` regenerates; `tsconfig.json` auto-created if no ancestor config found
- Edit `.dart` file → `.dart.api` regenerates immediately
- Read `.py`/`.js`/`.ts`/`.dart`/`.tex` source when interface (`.pyi`/`.d.ts`/`.dart.api`/`.texif`) is current → hard-blocked; must read interface first
- Edit `.tex` file → `.texif` regenerated + `LABELS.md` regenerated immediately
- Edit `.bib` file → warning printed for bib keys missing `reviews/<key>.yaml`
- Attempt to grow code file past 200 lines (`.js .ts .tsx .py .dart .html .css .scss .tex`) → Claude Code blocks edit
- Attempt to create new file without first-line description comment → Claude Code blocks Write
- Edit file missing first-line comment → reminder printed immediately after edit
- Run `git commit` on 200+ line code file → commit rejected
- Run `git commit` with staged code file → CONTEXT.md Routing block auto-updated and staged

---

## Versioned Files

All infrastructure lives in workspace git repo:

```
.hooks/
  pre-commit              ← git hook: size enforcement + stub/declaration generation + routing-sync
  pre-edit.py             ← canonical pre-edit policy: 200-line size gate + first-line check
  post-edit.sh            ← canonical post-edit: interface regen + routing-sync + first-line reminder
  pre-read.sh             ← canonical pre-read: hard-blocks source reads when interface is current
  check-line-counts.sh    ← standalone audit tool (also called by pre-commit); reads line-limits.env
  line-limits.env         ← single source of truth for WARN_LINES and BLOCK_LINES thresholds
  context_synchronizer.py             ← CONTEXT.md Routing block synchronizer: add/remove/link files, extract API
  check-facade-imports.py ← Facade boundary enforcer: blocks cross-module imports bypassing index/__init__
  dart-api-extract.py     ← Dart public API extractor: produces .dart.api stubs from .dart sources
  tex-interface-gen.py    ← LaTeX interface extractor: produces .texif (structure/equations/floats/citations) + LABELS.md; bib-check mode warns about missing reviews/*.yaml
  tex_interface_parser.py ← LaTeX parser module imported by tex-interface-gen.py (parse_tex, find_paper_root, helpers)
  paper-scaffold.py       ← paper directory initializer: `new <name>` creates full layout; `adapt <path>` fills missing files
  copilot-pre-tool.py     ← Copilot PreToolUse shim: dispatches to pre-read.sh / pre-edit.py
  copilot-post-tool.py    ← Copilot PostToolUse shim: dispatches to post-edit.sh
  copilot-session-start.py← Copilot SessionStart shim: injects AGENTS.md excerpt as context
  copilot-agent.sh        ← Copilot agent launcher: reads .agentrc.json and runs start-session.sh
  start-session.sh        ← neutral session-start: prints AGENTS.md header (Linux/macOS)
  start-session.ps1       ← neutral session-start: prints AGENTS.md header (Windows/PowerShell)
.claude/
  settings.json           ← Claude Code hook wiring (calls neutral pre-edit/post-edit/pre-read) + permissions; Bash matcher also runs `rtk hook claude` (see SETUP.md §11)
.opencode/
  CONTEXT.md              ← opencode config docs: event → script mapping, stdin-vs-env schema, warning surfacing
  index.js                ← opencode config facade — re-exports wp-helpers.js (consumed by plugins/workspace-policy.js)
  wp-helpers.js           ← opencode workspace-policy translation layer: spawn, schema mapping, warning surfacing
  plugins/
    workspace-policy.js   ← opencode workspace policy plugin: tool.execute.before/after → .hooks/* scripts
  package.json            ← "type": "module" + @opencode-ai/plugin dependency (gitignored — opencode Bun-managed)
.github/
  copilot-instructions.md ← Copilot shim: one line pointing to AGENTS.md + rtk usage block (SETUP.md §11)
  hooks/workspace-policy.json ← Copilot hook registration: SessionStart, PreToolUse, PostToolUse
  hooks/rtk-rewrite.json ← rtk Copilot hook registration: PreToolUse → `rtk hook copilot` (SETUP.md §11)
.agentrc.json             ← Copilot agent config: start_session path + declarative capability flags
SETUP.md                  ← this file: replication instructions
CLAUDE.md                 ← workspace behavioral instructions for Claude
AGENTS.md                 ← canonical workspace entrypoint read by all agents at session start
code/CONTEXT.md           ← engineering principles: file size, modularization, interface conventions
code/SPECS.md             ← style rules R1-R6, hook enforcement reference, file size policy
code/eslint.shared.js     ← shared ESLint config: 3 custom rules (single-return, one-call-per-statement, max-chain-depth) + built-in R1-R6 rules; imported by all TS projects
core/                     ← provider-agnostic research system (agents, flows, tools)
  core/agents/            ← agent role definitions (lead, researcher, reviewer, verifier, writer)
  core/flows/             ← workflow protocols (lit, deepresearch, review, draft, …)
  core/tools/             ← executable CLI research tools (search, papers, fetch, parse, …)
.claude/commands/         ← Claude Code slash commands (e.g. /research dispatcher)
```

Only steps that can't be versioned: global git config command + external tool installs (stubgen, tsc, nvm). Everything else in file system.

---

## Policy Decisions

### Per-project SETUP.md (pattern)

Projects under `code/` — and any other workspace subdirectory with non-trivial environment requirements — may include their own `SETUP.md`. This file covers what the workspace-level `SETUP.md` cannot: third-party tool installs, model downloads, platform-specific paths, extension dependencies. The workspace-level file delegates per-project setup to these files; the quick-start table above links to them. When adding a project with environment setup that can't be inferred from the code, create `<project>/SETUP.md` and add a row to the table.

### Line-limit rule (canonicalized)

- Warning threshold: 150 lines (`WARN_LINES` in `.hooks/line-limits.env`)
- Hard block: 200 lines (`BLOCK_LINES` in `.hooks/line-limits.env`)
- Pre-commit hook **incremental only** — checks staged files per commit, not full tree.
- Intent: force graph-like design — small single-responsibility nodes with explicit edges (imports).
- To change thresholds: edit only `.hooks/line-limits.env`. Both `pre-edit.py` and `check-line-counts.sh` read from it; no other file needs updating.
- Project-specific overrides: add note in project's `CONTEXT.md`, document exemption reason. Exempt categories so far: vendored ML model architecture files, generated string-table files, Dart `part of` split fragments.

---

## Per-Project Quick Start

See [code/SETUP.md](code/SETUP.md) for Code project quick-start commands and per-project setup.

See [academy/SETUP.md](academy/SETUP.md) for LaTeX toolchain and papers compilation.