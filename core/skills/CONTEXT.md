# skills
> Agent skills — provider-agnostic workflows invoked as slash commands or by instruction.

New skills: copy [`_template.md`](_template.md), fill `name` + `description` in frontmatter, add symlink under `.claude/commands/` for Claude Code.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`_template.md`](_template.md) | — | — | One-line summary of what this skill does and when to invoke it. Invoke with /skill-name [optional args]. |
| [`brain-compass.md`](brain-compass.md) | — | — | Run a compass review of Brain: surface what has good wind, update diagnostics, write ease-starts for stalled goals. |
| [`brain-finished.md`](brain-finished.md) | — | — | Mark an achievement done, advance to the next selected achievement, write a new ease-start. |
| [`brain-inbox.md`](brain-inbox.md) | — | — | Triage brain/INBOX.md — route each entry to a goal file, TODO list, writing draft, or delete. |
| [`foundry-appv2.md`](foundry-appv2.md) | — | — | Foundry VTT v14 — AppV2 sheet customization: tab injection, stale tabGroups bug, partial re-render nav-wipe bug. |
| [`foundry-canvas.md`](foundry-canvas.md) | — | — | Foundry VTT v14 — PIXI canvas structure: component hierarchy, depth sort, native handle suppression. |
| [`foundry-coords.md`](foundry-coords.md) | — | — | Foundry VTT v14 — coordinate systems: canvas space, screen space, HUD CSS space, canvas.dimensions, tile/token document coords. |
| [`foundry-hooks.md`](foundry-hooks.md) | — | — | Foundry VTT v14 — hooks reference table, key patterns, gridSize detection. |
| [`foundry-hud.md`](foundry-hud.md) | — | — | Foundry VTT v14 — HUD positioning in isometric mode: TokenHUD, TileHUD, Ruler waypoint labels. |
| [`foundry-object-transform.md`](foundry-object-transform.md) | — | — | Foundry VTT v14 — per-object (token/tile) mesh counter-transform, refresh flag semantics, PIXI mutation guards. |
| [`foundry-stage-transform.md`](foundry-stage-transform.md) | — | — | Foundry VTT v14 — isometric stage transform, background counter-transform, GridConfig preview counter-transform. |
| [`foundry-undo.md`](foundry-undo.md) | — | — | Foundry VTT v14 — undo/history system: suppression, manual push, dual-stack ordering. |
| [`foundry.md`](foundry.md) | — | — | Foundry VTT v14 module dev reference — router. Load relevant subfiles before working. |
| [`gmail.md`](gmail.md) | — | — | Triage Gmail across all configured accounts — classify, confirm routes, write to brain/INBOX.md. |
| [`handoff.md`](handoff.md) | — | — | End current session cleanly: archive completed work (moves done ROADMAP items and fixed bugs to HISTORY.md), route session knowledge to durable files, then produce a copy-pasteable resume prompt for the next session. Invoke with /handoff [focus for next session]. |
| [`handoff.original.md`](handoff.original.md) | — | — | End current session cleanly: archive completed work (moves done ROADMAP items and fixed bugs to HISTORY.md), route session knowledge to durable files, then produce a copy-pasteable resume prompt for the next session. Invoke with /handoff [focus for next session]. |
| [`research.md`](research.md) | — | — | Execute a research workflow from the workspace Core research system. |
<!-- routing:end -->
