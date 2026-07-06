# Skill Suite Migration Status (AD-07)

## What was done (2026-07-05)

1. Introduced `AD-07` in `core/SPECS.md`: rule for grouping related sub-skills into a suite folder.
2. Moved all `foundry-*.md` subskills into `core/skills/foundry/` suite.
3. Updated `foundry.md` to act as the suite parent/router.
4. Renamed sub-skills to remove the `foundry-` prefix (e.g. `foundry-canvas.md` -> `canvas.md`).
5. Created `foundry/` directory under `.opencode/skills/` and `.claude/skills/` (mirrors the suite parent only).
6. Updated `core/skills/CONTEXT.md` and `.opencode/skills/CONTEXT.md` to remove stale entries.
7. Fixed internal cross-reference in `object-transform.md` (`foundry-canvas.md` -> `canvas.md`).
8. Verified `sync-skills --check` passes cleanly.

## Current state

| Suite / Skill | Type | Path (source) | Path (mirror)ading only) |
|---------------|------|--------------|--------------------------|
| `foundry` | Suite parent | `core/skills/foundry.md` | `.opencode/skills/foundry/SKILL.md` |
| `foundry/*` | Sub-skill (not mirrored) | `core/skills/foundry/*.md` | _(not symlinked — read directly from source)_ |
| `prepare` | Flat skill | `core/skills/prepare.md` | `.opencode/skills/prepare/SKILL.md` |
| `prepare/refs` | References folder | `core/skills/prepare/refs/` | _(not symlinked)_ |

## Convention for future agents

When creating or updating a `refs/` folder for any skill:

1. **Create the folder at the same level as the skill file** (e.g. `core/skills/<name>/refs/`).
2. **Use `.yaml`** for structured references (papers, datasets, configs with schema).
3. **Use `.md`** for reading notes, quick links, and informal summaries.
4. **Use `REFS.md`** for one-line link captures (tier-1), as per the `brain-inbox` protocol.
5. **Never** create `refs/` inside `.opencode/skills/` or `.claude/skills/` — these are mirrors.

## Next steps flagged by user

- `brain/goals/prompt-opt-automation.md`: Goal to automate the prepare/routing logic.
- `core/skills/prepare/refs/research-summary.yaml`: Structured research data on prompt optimization.
