Foundry VTT v14 module dev reference — router. Load relevant subfiles before working.

Arguments: $ARGUMENTS

---

# Foundry VTT v14 — Topic Index

Load subfiles relevant to the task. Multiple subfiles fine when task spans topics.

| Topic | File | When to load |
|-------|------|-------------|
| PIXI canvas hierarchy, layers, depth sort, handle suppression | `foundry-canvas.md` | canvas structure, z-order, native control suppression |
| Coordinate systems, canvas.dimensions, tile/token doc coords | `foundry-coords.md` | anything involving positions, sizes, or coordinate space |
| Stage isometric transform, background CT, GridConfig preview | `foundry-stage-transform.md` | stage rotation/skew, background counter-transform, GridConfig preview BG |
| Per-object mesh CT, refresh flags, PIXI mutation guards | `foundry-object-transform.md` | token/tile mesh transforms, refreshToken/refreshTile hooks |
| TokenHUD, TileHUD, Ruler label positioning | `foundry-hud.md` | HUD button position, ruler waypoint labels |
| AppV2 tab injection, stale tabGroups, re-render nav-wipe bug | `foundry-appv2.md` | SceneConfig/TokenConfig/TileConfig custom tab, AppV2 sheet work |
| Hooks reference table, gridSize detection pattern | `foundry-hooks.md` | any hook work, scene update patterns |
| Undo/history system: suppression, manual push, dual-stack ordering | `foundry-undo.md` | Ctrl+Z behavior, undo stack, `{ isUndo: true }`, drag history, custom undo stacks |

## Reference Locations

- Foundry v14 source (while server running):
  `/proc/$(pgrep -f 'foundry.*main')/cwd/resources/app/public/scripts/foundry.mjs`
  - `BasePlaceableHUD._updatePosition` — how HUD CSS left/top are set from token bounds
  - `HeadsUpDisplayContainer.align()` — how `#hud` container is positioned (no rotation)
  - `Canvas.clientCoordinatesFromCanvas` — uses full worldTransform matrix
