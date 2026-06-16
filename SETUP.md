# Workspace Setup

Code quality enforcement + AI-assisted dev infrastructure.
Design principle: **the file system is the source of truth**. No config lives only in machine state or memory — everything versioned here.

## Parity And Enforcement Model

Canonical behavior lives in neutral files under `.hooks/` and `WORKSPACE.md`. Company-specific files act as shims, discovery points, or startup wiring for Claude, Copilot, VS Code.

Hook can block read/edit/commit → **ENFORCED**. File only injects guidance → **INDUCED**. Present only for compatibility, no enforcement effect → **SKIPPED**.

### Modularization / Interface Tasks

| Task | Canonical files | Claude files | Copilot / VS Code files | Behavior |
|------|-----------------|--------------|--------------------------|----------|
| Add workspace parity config and wrapper scripts | `WORKSPACE.md`, `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/start-session.sh`, `.hooks/start-session.ps1` | `CLAUDE.md`, `.claude/settings.json` | `.agentrc.json`, `.hooks/copilot-agent.sh`, `.github/copilot-instructions.md` | **ENFORCED** |
| Wire Copilot wrapper to call pre-read / pre-edit / post-edit hooks | `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/copilot-session-start.py`, `.hooks/copilot-pre-tool.py`, `.hooks/copilot-post-tool.py` | `.claude/settings.json` | `.github/hooks/workspace-policy.json`, `.vscode/settings.json` | **ENFORCED** |
| Integrate `context_synchronizer.py` and interface generation into wrapper | `.hooks/post-edit.sh`, `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/context_synchronizer.py` | `.claude/settings.json` | `.github/hooks/workspace-policy.json` | **ENFORCED** |
| Add VS Code tasks / settings to run session-start checks | `.hooks/start-session.sh`, `.hooks/start-session.ps1`, `.hooks/copilot-session-start.py` | `CLAUDE.md` | `.vscode/tasks.json`, `.vscode/settings.json`, `.github/copilot-instructions.md` | **INDUCED** |
| Test workflow: simulate read / edit / commit and fix issues | `.hooks/pre-read.sh`, `.hooks/pre-edit.py`, `.hooks/post-edit.sh`, `.hooks/copilot-pre-tool.py`, `.hooks/copilot-post-tool.py`, `.hooks/pre-commit` | `.claude/settings.json` | `.vscode/tasks.json` | **INDUCED** |

### Additional Files Not Tied To One Task

| File | Why it exists | Behavior |
|------|---------------|----------|
| `WORKSPACE.md` | Canonical workspace policy + startup anchor for every agent | **INDUCED** |
| `.github/copilot-instructions.md` | One-line Copilot shim pointing to `WORKSPACE.md` | **INDUCED** |
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
| `.hooks/facade-scan.py` | PreToolUse: Write (new files in `Code/`) | **Informs** — prints exports already declared in the target module's facade before a new file is created. Warns if exports list is empty (facade needs updating). Not a block. |
| `.hooks/post-edit.sh` | PostToolUse: Edit, Write | Regenerates `.pyi` / `.d.ts` / `.dart.api`; auto-scaffolds `jsconfig.json`/`tsconfig.json` if missing; reminds about missing first-line comment; runs `context_synchronizer.py` |
| `.hooks/pre-read.sh` | PreToolUse: Read | **Hard-blocks** reading source file when interface is current (timestamp check); warns when interface is stale |
| `.hooks/facade-gate.py` | PreToolUse: Edit, Write (`Code/` files) | **Hard-blocks** edits to any `Code/` module file until the nearest facade has been Read this session |
| `.hooks/facade-tracker.py` | PostToolUse: Read | Records facade reads to `/tmp/claude_facades_<pid>.txt`; consumed by `facade-gate.py` |

For codegraph setup and bash tool reference, see [`Code/SETUP.md`](Code/SETUP.md#codegraph).

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
See [Code/CONTEXT.md](Code/CONTEXT.md) for full file size policy, modularization strategy, and interface conventions Claude follows during coding sessions.

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

### 6. Codeburn
Run `codeburn optimize` periodically to audit token waste.

### 7. Caveman (Claude Code output compression)

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

### 8. Local LaTeX Toolchain (for `Academy/papers/`)

See [Academy/SETUP.md](Academy/SETUP.md).

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

# 5. Hook scripts are executable
ls -la /mnt/workspace/.hooks/post-edit.sh /mnt/workspace/.hooks/pre-read.sh /mnt/workspace/.hooks/pre-commit /mnt/workspace/.hooks/check-line-counts.sh
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
  copilot-session-start.py← Copilot SessionStart shim: injects WORKSPACE.md excerpt as context
  copilot-agent.sh        ← Copilot agent launcher: reads .agentrc.json and runs start-session.sh
  start-session.sh        ← neutral session-start: prints WORKSPACE.md header (Linux/macOS)
  start-session.ps1       ← neutral session-start: prints WORKSPACE.md header (Windows/PowerShell)
.claude/
  settings.json           ← Claude Code hook wiring (calls neutral pre-edit/post-edit/pre-read) + permissions
.github/
  copilot-instructions.md ← Copilot shim: one line pointing to WORKSPACE.md
  hooks/workspace-policy.json ← Copilot hook registration: SessionStart, PreToolUse, PostToolUse
.agentrc.json             ← Copilot agent config: start_session path + declarative capability flags
SETUP.md                  ← this file: replication instructions
CLAUDE.md                 ← workspace behavioral instructions for Claude
WORKSPACE.md              ← canonical workspace entrypoint read by all agents at session start
Code/CONTEXT.md           ← engineering principles: file size, modularization, interface conventions
Core/                     ← provider-agnostic research system (agents, flows, tools)
  Core/agents/            ← agent role definitions (lead, researcher, reviewer, verifier, writer)
  Core/flows/             ← workflow protocols (lit, deepresearch, review, draft, …)
  Core/tools/             ← executable CLI research tools (search, papers, fetch, parse, …)
.claude/commands/         ← Claude Code slash commands (e.g. /research dispatcher)
```

Only steps that can't be versioned: global git config command + external tool installs (stubgen, tsc, nvm). Everything else in file system.

---

## Policy Decisions

### Per-project SETUP.md (pattern)

Projects under `Code/` — and any other workspace subdirectory with non-trivial environment requirements — may include their own `SETUP.md`. This file covers what the workspace-level `SETUP.md` cannot: third-party tool installs, model downloads, platform-specific paths, extension dependencies. The workspace-level file delegates per-project setup to these files; the quick-start table above links to them. When adding a project with environment setup that can't be inferred from the code, create `<project>/SETUP.md` and add a row to the table.

### Line-limit rule (canonicalized)

- Warning threshold: 150 lines (`WARN_LINES` in `.hooks/line-limits.env`)
- Hard block: 200 lines (`BLOCK_LINES` in `.hooks/line-limits.env`)
- Pre-commit hook **incremental only** — checks staged files per commit, not full tree.
- Intent: force graph-like design — small single-responsibility nodes with explicit edges (imports).
- To change thresholds: edit only `.hooks/line-limits.env`. Both `pre-edit.py` and `check-line-counts.sh` read from it; no other file needs updating.
- Project-specific overrides: add note in project's `CONTEXT.md`, document exemption reason. Exempt categories so far: vendored ML model architecture files, generated string-table files, Dart `part of` split fragments.

---

## Per-Project Quick Start

See [Code/SETUP.md](Code/SETUP.md) for Code project quick-start commands and per-project setup.

See [Academy/SETUP.md](Academy/SETUP.md) for LaTeX toolchain and papers compilation.