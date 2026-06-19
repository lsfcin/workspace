# Workspace

Personal workspace root. Organizes projects, research, skills, and generated artifacts under a shared context system.

## Structure

| Folder | Purpose |
|--------|---------|
| `code/` | Software projects |
| `academy/` | Research, teaching, and academic management |
| `branches/` | Personal life management (health, finances, home) |
| `models/` | Local AI models and checkpoints |
| `Outputs/` | Generated artifacts |
| `core/` | Reusable skills and cross-domain resources |

## Context System

Each domain may contain a `CONTEXT.md` that specializes behavior for that subtree. Local context overrides the root [`CLAUDE.md`](CLAUDE.md).

## Setup

New machine or reinstall → see [SETUP.md](SETUP.md).

## What's tracked

- `core/` — fully tracked
- `code/`, `academy/`, `models/`, `Outputs/` — first-level `.md` files only
- `.vscode/settings.json` — workspace editor config
