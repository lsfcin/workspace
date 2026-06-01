Foundry VTT v14 — hooks reference table, key patterns, gridSize detection.

---

## Hooks Reference

| Hook | Trigger | Notable args |
|------|---------|-------------|
| `init` | Module init, before canvas | — |
| `canvasReady` | Canvas fully loaded | — |
| `updateScene(scene, changes)` | Scene document updated | `changes.flags?.MODULE_ID` to detect flag changes |
| `refreshToken(token, flags)` | Token visual refresh | `flags`: `refreshMesh`, `refreshSize`, `refreshShape`, `refreshRotation`, `redraw` |
| `refreshTile(tile, flags)` | Tile visual refresh | same flags as refreshToken |
| `renderSceneConfig(app, html)` | SceneConfig AppV2 sheet renders | `html` IS the `<form>` element |
| `renderTokenConfig(app, html)` | TokenConfig sheet renders | — |
| `renderTileConfig(app, html)` | TileConfig sheet renders | — |
| `renderTokenHUD(hud, html)` | Token right-click HUD opens | `hud.object` = Token |
| `renderTileHUD(hud, html)` | Tile right-click HUD opens | `hud.object` = Tile |
| `renderGridConfig(app, html)` | Grid Configuration Tool opens | fires after `#createPreview()` completes |
| `preUpdateScene(scene, changes)` | Before scene document update | `scene` = pre-update state; `changes.grid?.size` = new grid size if changing |
| `updateScene(scene, changes)` | After scene document update | `scene` = updated state; use with `preUpdateScene` to get both old and new values |

Key patterns:
- `Hooks.once("init", ...)` — register settings and hook listeners; fires once per session
- `Hooks.on("updateScene", (scene, changes) => { if (scene.id !== canvas.scene?.id) return; ... })` — always guard for current scene
- Render hooks for AppV2 sheets fire after DOM built; html already in document

## Detecting gridSize Changes

`preUpdateScene` fires before the update — `scene.grid.size` = old value, `changes.grid?.size` = new value. Capture ratio there; apply in `updateScene`. Only GM should write embedded document updates.

```typescript
let pendingRescale: { sceneId: string; ratio: number } | null = null;

Hooks.on("preUpdateScene", (scene, changes) => {
  if (!changes.grid?.size) return;
  const ratio = changes.grid.size / scene.grid.size;
  if (ratio === 1) return;
  pendingRescale = { sceneId: scene.id, ratio };
});

Hooks.on("updateScene", (scene) => {
  const p = pendingRescale;
  pendingRescale = null;
  if (!p || p.sceneId !== scene.id) return;
  if (scene.id !== canvas.scene?.id || !game.user?.isGM) return;
  const tiles = canvas.tiles?.placeables ?? [];
  const updates = tiles
    .filter(t => shouldRescale(t))
    .map(t => ({ _id: t.id, x: t.document.x * p.ratio, y: t.document.y * p.ratio,
                  width: t.document.width * p.ratio, height: t.document.height * p.ratio }));
  if (updates.length) void canvas.scene!.updateEmbeddedDocuments("Tile", updates);
});
```

`boundH` (grid units) and `elevation` (feet) are already scale-invariant — don't touch them.
Tile `x/y/width/height` are canvas px — multiply by ratio to keep grid-unit footprint constant.
