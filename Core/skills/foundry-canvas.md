Foundry VTT v14 — PIXI canvas structure: component hierarchy, depth sort, native handle suppression.

---

## Canvas Component Hierarchy

```
PIXI.Application (canvas.app)
└── PIXI.Stage (canvas.app.stage)          ← we apply rotation/skew here for isometric
    ├── EnvironmentCanvasGroup              (canvas.environment)
    │   └── PrimaryCanvasGroup             (canvas.environment.primary)
    │       └── PrimarySpriteMesh          (canvas.environment.primary.background) ← v14 bg sprite
    ├── PrimaryCanvasGroup                 (canvas.primary)
    │   ├── background                     (canvas.primary.background) ← WRONG — no visual effect
    │   ├── TokenLayer                     (canvas.tokens)
    │   │   └── Token[]                    (canvas.tokens.placeables)
    │   │       └── PrimarySpriteMesh      (token.mesh)
    │   └── TilesLayer                     (canvas.tiles)
    │       └── Tile[]                     (canvas.tiles.placeables)
    │           └── PrimarySpriteMesh      (tile.mesh)
    └── HeadsUpDisplayContainer            → DOM overlay, NOT a PIXI child
        └── #hud div                       (canvas.hud.element)
```

Key rule: **`canvas.environment.primary.background` = rendered bg sprite in v14.**
`canvas.primary.background` exists but transforming it has no visual effect.

## Depth Sort

`canvas.primary.children.sort()` corrupts Foundry internal z-order.
Use `PrimaryCanvasGroup` API, assign `zIndex` on objects or add custom foreground container.

## Native Handle Suppression

Foundry renders interactive handles on selected placeables via `tile.controls` (PIXI Container).
Suppress specific handle (e.g. rotation triangle) in iso mode — place invisible event-absorbing overlay on top:

**Locating the rotation handle** (confirmed v14, ShapeControlsHandle with cursor=grab):
```typescript
type H = { children?: H[]; getGlobalPosition?: () => {x:number;y:number}; getBounds?: () => {x:number;y:number;width:number;height:number} };
const handle = (tile as any).controls?.children?.[1]?.children?.[0] as H | undefined;
```

**Creating a blocker on your overlay layer** (layer is a direct child of canvas.stage):
```typescript
const gp  = handle.getGlobalPosition();       // screen coords
const lp  = layer.toLocal(gp);                // canvas coords (layer has identity transform)
const tw  = tile.document.width ?? 0;
// Rotation handle origin is offset from visual center; correct by tw/2 in canvas space
const corrected = { x: lp.x + tw / 2, y: lp.y };
const bounds = handle.getBounds?.();
const zoom = (canvas.stage as any)?.scale?.x ?? 1;
const r = bounds ? Math.max(bounds.width, bounds.height) * 0.5 * 1.03 / zoom : 20;
const g = new PIXI.Graphics();
g.beginFill(0x000000, 0.001); g.drawCircle(0, 0, r); g.endFill();
g.x = corrected.x; g.y = corrected.y;
g.eventMode = "static"; g.cursor = "default";
layer.addChild(g);
```
Key: **`layer.toLocal(globalPos)`** converts screen → canvas coords; `getBounds()` gives screen-space size → divide by zoom for canvas-space radius.
Blocker must be in layer added AFTER all Foundry layers (use `bringToTop()`) to intercept events.
