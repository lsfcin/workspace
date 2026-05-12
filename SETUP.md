# Workspace Setup

Instructions for reproducing this workspace on a new machine.

## Prerequisites

Install the following before running the setup commands below.

| Tool | Required for | Install |
|------|-------------|---------|
| `git` ≥ 2.9 | global hooks | system package manager |
| `mypy` | Python `.pyi` stub generation | `pip install mypy` |
| `node` + `npm` | TypeScript projects (voti) | [nodejs.org](https://nodejs.org) |
| `flutter` | Mobile projects (apptime) | [flutter.dev](https://flutter.dev) |

## One-Time Setup

Run once after cloning or reinstalling the workspace:

```bash
# Point all local git repos to the central hooks directory
git config --global core.hooksPath /mnt/workspace/.hooks

# Verify
git config --global core.hooksPath
# → /mnt/workspace/.hooks
```

> If the workspace lives at a different path, replace `/mnt/workspace` with the actual path.

## What the Hook Does

The pre-commit hook at `.hooks/pre-commit` runs on every commit across all projects:

- **Line-count warning at 150 lines** — prompts a cohesion check
- **Line-count warning at 300 lines** — flags likely responsibility creep; refactor recommended
- **Python `.pyi` generation** — runs `stubgen` on changed `.py` files and stages the output alongside the source (requires `mypy`)
- **TypeScript notice** — reminds to configure `declarationDir` in `tsconfig.json` if not set

All warnings are non-blocking. The hook never prevents a commit from completing.

## Engineering Conventions

See [Code/CONTEXT.md](Code/CONTEXT.md) for the full engineering policy covering:

- File structure and naming principles
- Interface file strategy per language (`.pyi`, `.d.ts`)
- File size thresholds and what to do when you hit them
- CONTEXT.md File Map convention for navigating project trees

## Per-Project Setup

Each project under `Code/` has its own git repo and may have additional setup steps. See the project's `CONTEXT.md` for specifics.

| Project | Quick start |
|---------|-------------|
| `workflows` | `pip install -r requirements.txt` (if present); `python -B start.py <flow>` |
| `apptime` | `flutter pub get`; open in Android Studio |
| `voti` | `npm install`; `npm run dev` |
