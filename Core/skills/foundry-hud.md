Foundry VTT v14 — HUD positioning in isometric mode: TokenHUD, TileHUD, Ruler waypoint labels.

---

## HUD Coordinate Formula

`HeadsUpDisplayContainer.align()` sets `#hud` CSS: `left = canvas.primary.getGlobalPosition().x`, `top = .y`, `transform = scale(zoom)`. **No rotation.**

CSS `left/top` within `#hud` in canvas-unit space. Foundry default `_updatePosition` uses raw `token.bounds.x/y` — correct without rotation; container applies matching scale+translate.

With isometric rotation — correct formula (tx/ty and zoom cancel out):
```typescript
const m = canvas.app.stage.worldTransform;
const zoom = canvas.stage.scale.x;
const L = (m.a * cx + m.c * cy) / zoom;
const T = (m.b * cx + m.d * cy) / zoom;
```

## TokenHUD

Hook `renderTokenHUD`, use `requestAnimationFrame` so Foundry positions first:
```typescript
$html.css({ left: `${L}px`, top: `${T}px`, transform: "translate(-50%, -50%)" });
```

## TileHUD

**Patch `_updatePosition` instead of hooking `renderTileHUD`.**
Foundry calls `_updatePosition` on every tile document change (e.g. resize, flag update) without re-firing the hook. Patching it handles all cases with zero rAF timing issues.
Access via `CONFIG.Tile.hudClass.prototype`. The `position` object passed in has `left/top/width/height/scale`.

Critical: AppV2 elements use **`transform-origin: top-left`** → `visual_left = CSS_left` (no centering correction). Scale(s) shrinks from top-left corner, not center.

For isometric TileHUD positioned at tile visual footprint:
```typescript
const s = canvas.dimensions.uiScale;
const docW = tile.document.width ?? 0, docH = tile.document.height ?? 0;
const cosA = m.a / zoom, cosC = m.c / zoom;        // ≈ 0.895 for dimetric 2:1
const sinB = Math.abs(m.b / zoom);                  // ≈ 0.447 = cosA/2
const visualCssW = cosA * docW + cosC * docH;       // tile visual screen width in CSS px
// Left/top of tile visual footprint (top-left origin: CSS pos = visual pos)
pos.left  = L - visualCssW / 2;
pos.top   = T - sinB * (docW + docH) / 2;           // = T - visualCssW/4
pos.width = visualCssW / s;                         // CSS width → scale(s) → visualCssW rendered
pos.height = 0;  // 0 → el.style.height = "" (auto) — avoids docH dependency
```

`pos.top = T - sinB*(docW+docH)/2` is swap-stable: `docW+docH` is constant when dimensions swap.

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
