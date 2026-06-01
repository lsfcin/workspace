Foundry VTT v14 — coordinate systems: canvas space, screen space, HUD CSS space, canvas.dimensions, tile/token document coords.

---

## Coordinate Systems

- **Canvas coords** — scene pixel space, origin = scene top-left (includes padding). `token.document.x/y` / `tile.document.x/y`.
- **Stage local space** = canvas coords. Stage transform maps canvas → screen.
- **PIXI global / screen coords** — `stage.worldTransform.apply({x,y})` = where canvas point appears in screen pixels.
- **`canvas.clientCoordinatesFromCanvas(pt)`** — calls `stage.worldTransform.apply(pt)`. Includes full matrix (rotation + skew + zoom + pan).
- **`#hud` CSS space** — canvas-unit coords (no rotation). Formula: `L = (m.a*cx + m.c*cy) / zoom`.

## `canvas.dimensions` vs Scene Flags for Scene-Space Positioning

`scene.width/height/padding` are static document values — do NOT update when Scene Offset changes. Use `canvas.dimensions` for dynamic scene content bounds:

| Need | Wrong | Right |
|------|-------|-------|
| Scene content center | `scene.width/2 + scene.width*scene.padding` | `dims.sceneX + dims.sceneWidth/2` |
| Scene content top-left | compute from scene flags | `dims.sceneX`, `dims.sceneY` |
| Scene content size | `scene.width`, `scene.height` | `dims.sceneWidth`, `dims.sceneHeight` |

```typescript
const dims = canvas.dimensions as unknown as { sceneX: number; sceneY: number; sceneWidth: number; sceneHeight: number };
const cx = dims.sceneX + dims.sceneWidth / 2;   // tracks scene offset
const cy = dims.sceneY + dims.sceneHeight / 2;
```

Scene offset (GridConfig "Scene Offset" field) reflected in `dims.sceneX/Y`, never in scene flags.

## v14 CRITICAL: `tile.x/y` ≠ canvas position; `document.x/y` = CENTER

In Foundry v14, `Tile` (and `PlaceableObject` subclasses) park PIXI container at `(0, 0)`. Actual canvas-space position is in **document**: `tile.document.x`, `tile.document.y`. `tile.x`/`tile.y` returns 0 — **wrong**.

`tile.document.x/y` = **CENTER** of tile (not top-left). Top-left:
```typescript
const tw = tile.document.width ?? 0;
const th = tile.document.height ?? 0;
const tx = (tile.document.x ?? 0) - tw / 2;   // top-left x
const ty = (tile.document.y ?? 0) - th / 2;   // top-left y
```
`tile.document.width/height` in canvas pixels (not grid units).

## Token Document Coords — DIFFERENT from Tiles

| Property | Tile | Token |
|----------|------|-------|
| `document.x/y` | CENTER of footprint (canvas px) | TOP-LEFT of footprint (canvas px) |
| `document.width/height` | canvas pixels | **grid units** — multiply by `gridSize` for pixels |

```typescript
// Token canvas footprint:
const gs = canvas.grid?.size ?? 100;
const tw = (token.document.width  ?? 1) * gs;   // canvas pixels
const th = (token.document.height ?? 1) * gs;
const tx = token.document.x ?? 0;               // already top-left
const ty = token.document.y ?? 0;
// token.center ≈ { x: tx + tw/2, y: ty + th/2 }
```
