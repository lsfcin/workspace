# Workspace Setup

Infrastructure for code quality enforcement and AI-assisted development.
Design principle: **the file system is the source of truth**. No configuration lives only in machine state or memory — everything is versioned here.

---

## What Is Configured

### Git Pre-Commit Hook (`.hooks/pre-commit`)
Applied globally via `core.hooksPath`. Fires on every `git commit` across all repos under this workspace.

- Warns on code files ≥ 200 lines (`.js .ts .tsx .py .dart .html .css .scss` — not data files)
- **Blocks** commits on code files ≥ 300 lines (exit 1)
- Warns when a newly staged code file lacks a first-line description comment
- **Auto-syncs CONTEXT.md File Map** via `ctx-sync.py` for every directory with staged files, and stages the result
- Auto-generates `.pyi` stubs for Python files (via `stubgen`) and stages them
- Auto-generates `.d.ts` declarations for JS/TS files (via `tsc`) and `.dart.api` stubs for Dart files (via `dart-api-extract.py`), and stages them

### Claude Code Hooks (`.claude/settings.json`)
Fires on every `Edit`, `Write`, and `Read` tool call during Claude Code sessions.

| Script | Trigger | Behavior |
|--------|---------|----------|
| `.hooks/claude-pre-edit.py` | PreToolUse: Edit, Write | **Hard-blocks** edits that would push any code file past 200 lines; **hard-blocks Write of new files missing a first-line description comment** |
| `.hooks/claude-post-edit.sh` | PostToolUse: Edit, Write | Regenerates `.pyi` / `.d.ts` / `.dart.api`; auto-scaffolds `jsconfig.json`/`tsconfig.json` if missing; reminds about missing first-line comment; runs `ctx-sync.py` |
| `.hooks/claude-pre-read.sh` | PreToolUse: Read | **Hard-blocks** reading a source file when its interface is current (timestamp check); warns when interface is stale |

### CONTEXT.md Auto-Sync (`.hooks/ctx-sync.py`)
Runs on every Claude edit (via `claude-post-edit.sh` — also re-syncs the parent dir) and on every git commit (via `pre-commit`). Keeps each project's `## File Map` block accurate without manual maintenance:

- **Adds** new code files with description from first-line comment + extracted public API
- **Removes** stale entries for deleted files
- **Links** interface files (`.pyi` / `.d.ts` / `.dart.api`) automatically
- **Folds** small subdirectories (< 7 files, leaf dirs) into the parent File Map with relative paths
- **Links** large subdirectories (≥ 7 files, or has own CONTEXT.md, or has deeper nesting) in a `## Sub-modules` section; auto-creates a scaffold CONTEXT.md for intermediate dirs that have no CONTEXT.md but do have sub-hierarchy
- **Warns** when a directory exceeds 7 direct files

Also run manually: `python3 /mnt/workspace/.hooks/ctx-sync.py <directory>`

### First-Line Description Convention
Every code file must begin with a one-line description comment. `ctx-sync.py` reads this as the canonical description and writes it into CONTEXT.md automatically.

Enforcement model:
- **New file (Write)** → hard block: `claude-pre-edit.py` rejects the Write if the content doesn't start with a description comment
- **Existing file (Edit)** → in-session reminder: `claude-post-edit.sh` checks line 1 after every edit and prints a reminder if missing
- **git commit** → warning: `pre-commit` warns when a newly staged file lacks the comment

### Interface File Generation
Every save of a supported source file unconditionally produces an interface file. Generation is universal — no per-project configuration required.

| Language | Output | Tool | Notes |
|----------|--------|------|-------|
| Python | `.pyi` | `stubgen` | Auto on every Claude edit and on git commit |
| JavaScript | `.d.ts` | `tsc --allowJs --emitDeclarationOnly` | Auto on every Claude edit; `jsconfig.json` auto-scaffolded if missing (IDE use only) |
| TypeScript | `.d.ts` | `tsc --emitDeclarationOnly` | Auto on every Claude edit; `tsconfig.json` auto-scaffolded if no ancestor config found |
| Dart/Flutter | `.dart.api` | `dart-api-extract.py` | Auto on every Claude edit; extracts public class/mixin/method signatures |

**Enforcement**: `claude-pre-read.sh` hard-blocks reading any source file when its interface file is current (interface timestamp ≥ source timestamp). Reading the interface file first is not optional when the interface is trustworthy.

### Engineering Policies
See [Code/CONTEXT.md](Code/CONTEXT.md) for the full file size policy, modularization strategy, and interface conventions that Claude follows during coding sessions.

---

## First-Time Setup (New Machine)

Run these steps once after cloning or moving the workspace.

### 1. Wire the Git Hook
```bash
git config --global core.hooksPath /mnt/workspace/.hooks
```
This applies `.hooks/pre-commit` to every git repo on the machine.
If the workspace is at a different path, replace `/mnt/workspace` with the actual path everywhere in this file.

Verify:
```bash
git config --global core.hooksPath
# Expected: /mnt/workspace/.hooks
```

### 2. Make Hook Scripts Executable
```bash
chmod +x /mnt/workspace/.hooks/claude-post-edit.sh
chmod +x /mnt/workspace/.hooks/claude-pre-read.sh
```
(`claude-pre-edit.py` and `dart-api-extract.py` are invoked via `python3` and do not need execute permission.)

### 3. Python Interface Generation (stubgen)
```bash
pip install mypy
```
Or using the workspace virtual environment:
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
Or if Node is already installed but global install requires sudo:
```bash
npm install -g typescript --prefix ~/.local
```
The hook checks `tsc` on PATH first, then falls back to `~/.local/bin/tsc`.

Verify: `tsc --version` or `~/.local/bin/tsc --version`

### 5. Claude Code Hooks
No action required. `.claude/settings.json` is versioned in this repo and Claude Code reads it automatically when the workspace is opened. The hooks in `.hooks/` activate immediately.

---

## Per-Project: Interface Generation Notes

**JavaScript / TypeScript**: no manual setup required. The hook auto-scaffolds `jsconfig.json` (for JS) or `tsconfig.json` (for TS, walking up to the git root first) on the first file write. These config files are for IDE tooling only — the hook generates declarations via direct CLI regardless.

**Dart**: no setup required. `dart-api-extract.py` runs on every `.dart` save and requires only Python 3 (no Dart SDK).

**Python**: requires `stubgen` (mypy) to be installed. See Step 3 above.

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
ls -la /mnt/workspace/.hooks/claude-post-edit.sh /mnt/workspace/.hooks/claude-pre-read.sh
```

Behavioral verification (inside a Claude Code session):
- Edit a `.py` file → `.pyi` regenerates immediately (visible in shell output)
- Edit a `.js` file → `.d.ts` regenerates; `jsconfig.json` auto-created if missing
- Edit a `.ts` file → `.d.ts` regenerates; `tsconfig.json` auto-created if no ancestor config found
- Edit a `.dart` file → `.dart.api` regenerates immediately
- Read a `.py`/`.js`/`.ts`/`.dart` source file when its interface is current → hard-blocked; must read interface first
- Attempt to grow any code file past 200 lines → Claude Code blocks the edit
- Attempt to create a new file without a first-line description comment → Claude Code blocks the Write
- Edit a file missing a first-line comment → reminder printed immediately after the edit
- Run `git commit` on a 300+ line code file → commit is rejected
- Run `git commit` with any staged code file → CONTEXT.md File Map auto-updated and staged

---

## Versioned Files

All infrastructure lives in the workspace git repo. This is what gets replicated:

```
.hooks/
  pre-commit            ← git hook: size enforcement + stub/declaration generation + ctx-sync
  claude-pre-edit.py   ← Claude Code hook: 200-line size gate (PreToolUse: Edit, Write)
  claude-post-edit.sh  ← Claude Code hook: interface regen + ctx-sync (PostToolUse: Edit, Write)
  claude-pre-read.sh   ← Claude Code hook: hard-blocks source reads when interface is current (PreToolUse: Read)
  ctx-sync.py          ← CONTEXT.md File Map synchronizer: add/remove/link files, extract API
  dart-api-extract.py  ← Dart public API extractor: produces .dart.api stubs from .dart sources
.claude/
  settings.json        ← Claude Code hook wiring + workspace permissions
SETUP.md               ← this file: replication instructions
CLAUDE.md              ← workspace behavioral instructions for Claude
Code/CONTEXT.md        ← engineering principles: file size, modularization, interface conventions
```

The only steps that cannot be versioned are the global git config command and external tool installations (stubgen, tsc, nvm). Everything else is in the file system.

---

## Per-Project Quick Start

Each project under `Code/` has its own git repo and `CONTEXT.md`. See those files for project-specific setup.

| Project | Stack | Quick start |
|---------|-------|-------------|
| `flows` | Python | `pip install -r requirements.txt` |
| `apptime` | Flutter + Kotlin | `flutter pub get` |
| `voti` | Next.js / TypeScript | `npm install && npm run dev` |
| `corpora` | Python / PyTorch | `pip install -r requirements.txt` |
| `futebots` | Python | `pip install -r requirements.txt` |
| `isoroll` | Python / ComfyUI | see project CONTEXT.md |
| `shortvid` | Python / PySide6 | `pip install -r requirements.txt` |
| `ppc` | Vanilla HTML / Alpine.js | open `index.html` via local server |
