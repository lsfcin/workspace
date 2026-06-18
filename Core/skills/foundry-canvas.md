---
name: foundry-canvas
description: >
  Foundry VTT v14 — PIXI canvas structure: component hierarchy, depth sort, native handle suppression.
---

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

## VisibilityFilter on canvas.primary

`canvas.primary` has a `VisibilityFilter` applied. It **hard-clips** the rendered output to the token/tile's grid footprint bounding box — any sprite pixels outside the footprint are discarded. This causes visual issues for isometric sprites taller or wider than their footprint (volume sprites, counter-transformed tiles).

**There is no in-place fix.** VisibilityFilter operates at the GPU shader level on the entire PrimaryCanvasGroup output. The only escape: add a separate `PIXI.Container` directly to `canvas.stage` (outside canvas.primary entirely).

```typescript
// Add container to canvas.stage — inherits stage iso transform, not subject to VisibilityFilter
const layer = new PIXI.Container();
canvas.stage.addChild(layer);           // or insert at specific index
layer.eventMode = "passive";            // no hit detection on the layer itself
```

Clones in this external layer share texture handles with originals in canvas.primary — zero extra VRAM.

## canvas.visibility (global fog compositing)

**Separate** from VisibilityFilter. `canvas.visibility` is a global compositing pass that darkens/hides pixels EVERYWHERE on `canvas.stage` based on the vision polygon — including external layers added to canvas.stage. Two distinct problems:

| System | What it does | Affects |
|--------|-------------|---------|
| `VisibilityFilter` on `canvas.primary` | Hard-clips sprite pixels to footprint bounding box | Only children of canvas.primary |
| `canvas.visibility` | Darkens pixels outside vision polygon (fog of war) | Entire canvas.stage |

Phase 3 (IsoSpriteLayer) solves VisibilityFilter clip. Phase 4 handles canvas.visibility darkening on overflow pixels.

## Depth Sort

`canvas.primary.children.sort()` corrupts Foundry internal z-order.
Use `PrimaryCanvasGroup` API, assign `zIndex` on objects or add custom foreground container.

## mesh.alpha = 0 — hide without losing interactivity

Setting `mesh.alpha = 0` on a `PrimarySpriteMesh` makes it invisible but leaves it fully present in canvas.primary — Foundry continues to use it for hit detection, HUD positioning, and mechanics. Used when moving visual rendering to an external layer while keeping Foundry's interaction system intact.

```typescript
// Hide original — stays interactive, hit-detectable, used by Foundry internals
mesh.alpha = 0;

// Clone at same position in external layer — visible, no events
const clone = new PIXI.Sprite(mesh.texture);  // shared texture handle
clone.eventMode = "passive";
externalLayer.addChild(clone);
```

**Restore on destroy:** `mesh.alpha = docAlpha(doc)` when the clone is removed (e.g. on `destroyToken`).

**Do NOT read `mesh.alpha` back for clone state** — we set it to 0, so copying it kills the clone. Clone alpha must come from `doc.alpha`, not from mesh.

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
