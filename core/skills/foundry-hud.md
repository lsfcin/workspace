---
name: foundry-hud
description: >
  Foundry VTT v14 — HUD positioning in isometric mode: TokenHUD, TileHUD, Ruler waypoint labels.
---

Foundry VTT v14 — HUD positioning in isometric mode: TokenHUD, TileHUD, Ruler waypoint labels.

---

## #hud Coordinate System

Foundry positions `#hud` by setting its CSS `style.left = wt.tx + "px"` and `style.top = wt.ty + "px"` **inside the `canvasPan` handler only**. The `#hud` CSS transform is always `scale(1)` — no rotation, no translation in the transform property. Pan offset lives in `style.left/top` directly.

Within `#hud`, the formula for a world point `(cx, cy)` in CSS px:

```typescript
const wt   = canvas.app.stage.worldTransform;
const zoom = canvas.stage.scale.x;
const L = (wt.a * cx + wt.c * cy) / zoom;  // zoom cancels: wt.a includes zoom
const T = (wt.b * cx + wt.d * cy) / zoom;
// wt.tx/ty intentionally omitted — absorbed by #hud style.left/top
```

**Zoom cancels**: `wt.a = zoom * cos_component`, so `wt.a / zoom = cos_component`. The formula is zoom-independent. Works at any zoom level.

## PIXI worldTransform Cache — Critical Gotcha

PIXI only recomputes `worldTransform` during the render loop. After setting `stage.rotation` / `stage.skew`, `worldTransform` remains stale (identity) until the next frame.

**Symptom**: HUD positions correctly after first pan/zoom but wrong on initial load (before any interaction).

**Why**: `canvasPan` never fires on initial load. `#hud style.left/top` are at their default (not matching new `wt.tx/ty`). The formula is correct, but `#hud` is mispositioned.

**Fix** — call after `applyCurrentState()` in `canvasReady`:

```typescript
// 1. Flush worldTransform cache (stage is root — no parent for updateTransform())
stage.transform.updateLocalTransform();
stage.worldTransform.copyFrom(stage.localTransform);
// 2. Sync #hud CSS to match what canvasPan would have set
const hud = document.getElementById("hud");
if (hud) { hud.style.left = `${wt.tx}px`; hud.style.top = `${wt.ty}px`; }
```

## Correct Pattern: _updatePosition Prototype Patch

**Use `_updatePosition` prototype patch for both TileHUD and TokenHUD.** Do NOT use `renderTileHUD` / `renderTokenHUD` hooks:
- Hooks fire only on initial render; `_updatePosition` fires on every tile/token document update too
- Hooks + RAF have timing issues and can accidentally stomp Foundry's native `transform: scale(uiScale)`
- Prototype patch preserves `pos.scale` (uiScale) automatically — only set `left/top/width`

Access via `CONFIG.Tile.hudClass.prototype` and `CONFIG.Token.hudClass.prototype`. Patch at `init`.

```typescript
type HudPosition = { left?: number; top?: number; width?: number; height?: number; scale?: number };
const orig = proto._updatePosition;
proto._updatePosition = function(pos) {
  orig.call(this, pos);           // native runs first; provides centering offset
  const obj = this.object;        // Tile or Token
  if (!isIsoScene()) return pos;
  // ... override pos.left / pos.top / pos.width — never touch pos.scale
  return pos;
};
```

## TileHUD — Visual Footprint Layout

Tile origin is `(tile.document.x, tile.document.y)` — the **top-left corner** (not center).

```typescript
const c = isoHudCenter(cx, cy);      // projected corner (see isoHudCenter below)
const visualCssW = isoVisualCssWidth(docW, docH);   // see below
const s = canvas.dimensions.uiScale;
// AppV2 transform-origin: top-left → CSS left = visual left edge
pos.left   = c.left - visualCssW / 2;
pos.top    = c.top  - visualCssW / 4;   // = T - sinB*(W+H)/2, swap-stable
pos.width  = visualCssW / s;
pos.height = 0;   // auto — avoids docH dependency
```

`pos.top = T - visualCssW/4` is swap-stable: `visualCssW ∝ (W+H)`, constant when W↔H swap.

## TokenHUD — Centered Layout with Expanded Width

Token `center` is the **visual center** in world space. TokenHUD should be centered horizontally on the iso footprint and use native vertical centering.

```typescript
const raw = token.center ?? { x: token.x, y: token.y };
const c   = isoHudCenter(raw.x, raw.y);

// Native vertical centering offset (zoom-independent: zoom cancels in isoHudCenter)
const centeringOffsetY = (pos.top ?? 0) - raw.y;

// Token pixel dimensions: token.w/h = document.width/height * gridSize
const gs  = canvas.grid?.size ?? 100;
const tw  = token.w ?? token.document.width  * gs;
const th  = token.h ?? token.document.height * gs;
const visualCssW = isoVisualCssWidth(tw, th);
const s   = canvas.dimensions.uiScale;

pos.left  = c.left - visualCssW / 2;    // center horizontally on footprint
pos.top   = c.top  + centeringOffsetY;  // preserve native vertical centering
pos.width = visualCssW / s;
```

**Centering offset derivation**: in non-iso, `isoHudCenter(x,y).left = x` (zoom cancels). Native `_updatePosition` gives `pos.left = x + centering_offset`. So `centering_offset = pos.left - x = pos.left - raw.x`, zoom-independent.

## Shared Utilities

```typescript
// isoHudCenter — world point → {left, top} in #hud CSS px (no tx/ty)
export function isoHudCenter(x: number, y: number): { left: number; top: number } | null {
  const wt = canvas.app?.stage?.worldTransform;
  const zoom = canvasZoom();
  if (!wt) return null;
  return { left: (wt.a * x + wt.c * y) / zoom, top: (wt.b * x + wt.d * y) / zoom };
}

// isoVisualCssWidth — iso-projected CSS width of a w×h canvas rectangle
export function isoVisualCssWidth(w: number, h: number): number {
  const wt = canvas.app?.stage?.worldTransform;
  const zoom = canvasZoom();
  if (!wt) return 0;
  return (wt.a / zoom) * w + (wt.c / zoom) * h;
  // For dimetric 2:1 square (w=h): visualCssW ≈ 1.84 * w (≈ √(2²+1²)/√(1²+0.5²) * w)
}
```

## Ruler Waypoint Labels

Both `Ruler` and `TokenRuler` compute `context.position = {x: canvasX, y: canvasY}` in `_getWaypointLabelContext`, then write to `#hud #measurement` as CSS `--position-x`/`--position-y`. Patch both prototypes at `init`:

```typescript
// TokenRuler is NOT a global — access via CONFIG.Token.rulerClass
// Ruler: use v14 namespaced path; fall back to deprecated global for older hosts
const rulerProto      = (globalThis as any).foundry?.canvas?.interaction?.Ruler?.prototype
                     ?? (globalThis as any).Ruler?.prototype;
const tokenRulerProto = (CONFIG as any).Token?.rulerClass?.prototype;

function patch(proto) {
  const orig = proto._getWaypointLabelContext;
  proto._getWaypointLabelContext = function(...args) {
    const ctx = orig.apply(this, args);
    if (!ctx || !isIsoScene()) return ctx;
    const { x, y } = ctx.position;
    const m = canvas.app.stage.worldTransform;
    const zoom = canvas.stage.scale?.x ?? 1;
    ctx.position = { x: (m.a*x + m.c*y)/zoom, y: (m.b*x + m.d*y)/zoom };
    return ctx;
  };
}
patch(rulerProto); patch(tokenRulerProto);
```
