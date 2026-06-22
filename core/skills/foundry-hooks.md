---
name: foundry-hooks
description: >
  Foundry VTT v14 — hooks reference table, key patterns, gridSize detection.
---

Foundry VTT v14 — hooks reference table, key patterns, gridSize detection.

---

## Hook-Registry Convention

All `Hooks.on/once` calls live in **`src/core/hook-registry.ts`** — one central file, grouped by event, with explicit handler execution order. **Never add `Hooks.on` to a subsystem file.** The pre-commit hook enforces this.

`hook-registry.ts` imports through each module's `index.ts` façade, never directly from internal files (e.g. `'../render'` not `'../render/render-gate'`).

To add a new hook: register in `hook-registry.ts`, export the handler from the subsystem's `index.ts`.

---

## Hooks Reference

| Hook | Trigger | Notable args |
|------|---------|-------------|
| `init` | Module init, before canvas | — |
| `canvasInit` | Before canvas first renders (each scene load) | — |
| `canvasReady` | Canvas fully loaded | — |
| `canvasTeardown` | Canvas destroyed (scene switch) | — |
| `changeScene` | Active scene switches | — |
| `ready` | Game fully ready (post-canvas) | — |
| `controlTile(tile, controlled)` | Tile selected/deselected | `controlled`: boolean |
| `controlToken(token, controlled)` | Token selected/deselected | `controlled`: boolean |
| `createScene(scene, data, opts, userId)` | Scene created | — |
| `createTile(doc, data, opts, userId)` | Tile created (persisted) | — |
| `createToken(doc, data, opts, userId)` | Token created (persisted) | — |
| `deleteTile(doc, opts, userId)` | Tile document deleted | `doc.id` for cleanup |
| `deleteToken(doc, opts, userId)` | Token document deleted | `doc.id` for cleanup |
| `deleteWall(doc, opts, userId)` | Wall document deleted | — |
| `destroyTile(tile)` | Tile PIXI object destroyed | guard `isPreviewClone(t)` — preview clone shares id with original |
| `destroyToken(token)` | Token PIXI object destroyed | same guard |
| `drawTile(tile)` | Tile PIXI drawn fresh | — |
| `drawToken(token)` | Token PIXI drawn fresh | — |
| `preCreateTile(doc, data, opts, userId)` | Before tile persisted | Modify via `doc.updateSource({...})`; see blink note below |
| `preUpdateScene(scene, changes)` | Before scene doc update | `scene` = pre-update state; `changes.grid?.size` = new size |
| `preUpdateTile(doc, changes, opts, userId)` | Before tile doc update | — |
| `refreshToken(token, flags)` | Token visual refresh | `flags`: `refreshMesh`, `refreshSize`, `refreshShape`, `refreshRotation`, `redraw` |
| `refreshTile(tile, flags)` | Tile visual refresh | same flags as refreshToken |
| `renderSceneConfig(app, html)` | SceneConfig AppV2 sheet renders | `html` IS the `<form>` element |
| `renderTokenConfig(app, html)` | TokenConfig sheet renders | — |
| `renderTileConfig(app, html)` | TileConfig sheet renders | — |
| `renderTokenHUD(hud, html)` | Token right-click HUD opens | `hud.object` = Token |
| `renderTileHUD(hud, html)` | Tile right-click HUD opens | `hud.object` = Tile |
| `renderGridConfig(app, html)` | Grid Config Tool opens or form re-renders | fires after `#createPreview()` completes; also fires on Reset Changes |
| `resetFogOfWar` | Fog of war reset | — |
| `sightRefresh` | Vision/fog polygon refreshed | — |
| `closeGridConfig(app, html)` | Grid Config Tool closes | fires in `_onClose`; preview container already destroyed |
| `closeSceneConfig(app, html)` | SceneConfig sheet closes | — |
| `closeTokenConfig(app, html)` | TokenConfig sheet closes | — |
| `updateScene(scene, changes)` | After scene doc update | `scene` = updated state; pair with `preUpdateScene` to get old+new |
| `updateTile(doc, changes, opts, userId)` | Tile doc updated | `changes.flags?.MODULE_ID` for isoroll flag changes |
| `updateToken(doc, changes, opts, userId)` | Token doc updated | `changes.flags?.MODULE_ID`; `"elevation" in changes` |
| `updateWall(doc, changes, opts, userId)` | Wall doc updated | — |

Key patterns:
- `Hooks.once("init", ...)` — register settings and hook listeners; fires once per session
- **`preCreateTile` + no-blink pattern**: `doc.updateSource(data)` in `preCreateTile` correctly modifies creation data — `createTile` receives the updated values. BUT calling `doc.update()` again in `createTile` with the same data triggers a full PIXI sprite redraw, causing a visible blink. Skip the `createTile` update when `preCreateTile` already applied the data (use a shared in-memory cache to detect this).
- `Hooks.on("updateScene", (scene, changes) => { if (scene.id !== canvas.scene?.id) return; ... })` — always guard for current scene
- Render hooks for AppV2 sheets fire after DOM built; html already in document
- **`destroyTile`/`destroyToken`**: preview clones share the same `id` as the original — guard with `isPreviewClone(t)` to avoid triggering cleanup on the original when the clone is destroyed

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
