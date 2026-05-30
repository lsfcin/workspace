Foundry VTT v14 module development reference. Load this before any Foundry module work.

Arguments: $ARGUMENTS

If arguments name a topic (e.g. "hud", "tabs", "transform", "hierarchy", "hooks"), jump to that section. Otherwise print the full reference.

---

# Foundry VTT v14 — Module Dev Reference

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

Key rule: **`canvas.environment.primary.background` is the rendered bg sprite in v14.**
`canvas.primary.background` exists but transforming it has no visual effect.

## Coordinate Systems

- **Canvas coords** — scene pixel space, origin = scene top-left (includes padding). `token.document.x/y` / `tile.document.x/y`.
- **Stage local space** = canvas coords. Stage transform maps canvas → screen.
- **PIXI global / screen coords** — `stage.worldTransform.apply({x,y})` = where a canvas point appears in screen pixels.
- **`canvas.clientCoordinatesFromCanvas(pt)`** — calls `stage.worldTransform.apply(pt)`. Includes full matrix (rotation + skew + zoom + pan).
- **`#hud` CSS space** — canvas-unit coords (no rotation). Formula: `L = (m.a*cx + m.c*cy) / zoom`.

### v14 CRITICAL: `tile.x/y` ≠ canvas position; `document.x/y` = CENTER

In Foundry v14, `Tile` (and `PlaceableObject` subclasses) park their PIXI container at `(0, 0)`. The actual canvas-space position is in the **document**: `tile.document.x`, `tile.document.y`. Using `tile.x` / `tile.y` returns 0 — **wrong**.

Additionally, `tile.document.x/y` is the **CENTER** of the tile (not top-left corner). To get the top-left:
```typescript
const tw = tile.document.width ?? 0;
const th = tile.document.height ?? 0;
const tx = (tile.document.x ?? 0) - tw / 2;   // top-left x
const ty = (tile.document.y ?? 0) - th / 2;   // top-left y
```
`tile.document.width/height` are in canvas pixels (not grid units).

## Isometric Stage Transform (dimetric 2:1)

```typescript
// Apply to canvas.app.stage:
stage.rotation = rad(-45);
stage.skew.set(rad(18.435), rad(18.435));

// Resulting worldTransform matrix coefficients at zoom z:
//   a = z * cos(26.565°)  ≈  z * 0.8944
//   b = z * sin(-26.565°) ≈  z * -0.4472
//   c = z * cos(26.565°)  ≈  z * 0.8944   (same as a)
//   d = z * sin(26.565°)  ≈  z * 0.4472
//   tx = stage.position.x,  ty = stage.position.y
```

Counter-transform constants (dimetric 2:1):
- `reverseRotation = +45°`
- `reverseSkewX = reverseSkewY = 0`  ← NOT −18.435° — applying inside +18.435° parent doubles distortion
- `ratio = 2.0`
- `counterFactor = √10/4 ≈ 0.7906`  ← from matrix composition: worldScale = localScale × 4/√10

## Background Counter-Transform

Foundry pre-scales the bg sprite to fill the canvas (`PrimarySpriteMesh` scale ≠ 1).
Capture the original scale at `canvasReady` and multiply — do NOT hardcode `scale(1, ratio)` (→ ~1/4 size).

```typescript
// canvasReady: capture original
origScaleX = bg.scale.x;

// apply counter-transform:
bg.rotation = rad(45);
bg.skew.set(0, 0);
bg.anchor.set(0.5, 0.5);
bg.scale.set(origScaleX * counterFactor, origScaleX * ratio * counterFactor);
bg.position.set(scene.width / 2 + paddingX, scene.height / 2 + paddingY);
```

## Per-Object Counter-Transform (tokens / tiles)

Hooks: `refreshToken(token, flags?)`, `refreshTile(tile, flags?)`.

Foundry resets mesh scale on certain flags:
```typescript
const meshReset = !flags || flags["refreshMesh"] || flags["refreshSize"]
  || flags["refreshShape"] || flags["redraw"];
// rotation: apply every refresh (absolute, not cumulative)
```

**v14 CRITICAL — `setFlag` does NOT trigger meshReset flags.**
When `tile.document.setFlag(MODULE_ID, "someFlag", value)` fires `refreshTile`, the flags
are `{refreshPosition: true, refreshPerception: true}` — meshReset will be **false**.
Any code guarded by `if (meshReset)` will be skipped for custom-flag updates.

**`mesh.scale.set()` is safe on every refresh** — it is an absolute assignment (not `*=`),
so there is no accumulation risk. Remove the `isMeshReset` guard from `mesh.scale.set()`
calls if you need them to respond to flag changes. Only guard `mesh.scale *= ...` patterns.

**v14 CRITICAL — token animations fire `refreshMesh` every frame, NOT `refreshPosition`.**
Foundry's hide/show animation (alpha lerp) and other non-movement animations call
`_onAnimationUpdate` each tick, which sets `refreshMesh: true` but never `refreshPosition`.
`_refreshMesh()` only updates anchor/alpha/tint — it does NOT reset `mesh.x/y`.
If your hook overrides `mesh.x/y` and you capture the "natural base" on `refreshMesh`,
you'll bake in your own offset and re-add it every animation frame → image drifts off screen.

**Safe pattern for `mesh.x/y` override (token image offset):**
```typescript
// Only capture mesh.x/y as natural base when _refreshPosition() has run.
// refreshPosition is set on movement, setFlag, and all structural resets (redraw,
// refreshSize, refreshShape) — they all propagate through refreshPosition.
// refreshMesh alone (animation frames) does NOT run _refreshPosition() — skip it.
if (!flags || flags["refreshPosition"]) {
  tokenBase.set(token, { x: mesh.x, y: mesh.y });
}
const base = tokenBase.get(token) ?? { x: mesh.x - imgOff.x, y: mesh.y - imgOff.y };
// ... apply counter-transform ...
mesh.x = base.x + imgOff.x;
mesh.y = base.y + imgOff.y;
```

**What `_refreshMesh()` and `_refreshPosition()` actually do (from v14 source):**
```typescript
// _refreshMesh() — updates appearance only, never touches mesh.x/y:
this._refreshMeshSizeAndScale();           // scale from doc size + texture.scaleX/Y
this.mesh.anchor.set(anchorX, anchorY);   // from doc.texture.anchorX/Y (default 0.5/0.5)
this.mesh.alpha = this.alpha * doc.alpha;
this.mesh.tint = doc.texture.tint;

// _refreshPosition() — sets mesh to current token position:
this.position.set(doc.x, doc.y);          // token PIXI container
this.mesh.position = this.center;          // mesh.x = center.x, mesh.y = center.y
```
`token.center` ≈ `{x: doc.x + docW/2, y: doc.y + docH/2}` — the canvas center of the token footprint.

**Token (undistorted)**:
```typescript
mesh.rotation = reverseRotation;       // lock rotation — v14 auto-rotates tokens on move
mesh.skew?.set(0, 0);
mesh.anchor?.set(0.5, 0.5);           // required — HUD bounds derived from this
if (meshReset) {
  mesh.scale.x *= counterFactor;       // *= pattern: must guard (accumulates)
  mesh.scale.y *= ratio * counterFactor;
}
// TODO: use docRotation here for 8-directional sprite selection
```

**Tile (undistorted, preserves aspect ratio)**:
```typescript
mesh.rotation = (docRotationDeg * Math.PI / 180) + reverseRotation;
mesh.skew?.set(0, 0);
// No meshReset guard needed — scale.set() is absolute, safe every refresh:
{
  const texW = mesh.texture?.width || 1;
  const texH = mesh.texture?.height || 1;
  // Include boundHeight in scale so tall volumes scale the image correctly
  const uniform = Math.max(docW, docH, docBoundH) / Math.max(texW, texH);
  mesh.scale.set(uniform * counterFactor, uniform * ratio * counterFactor);
  // use .set(), not *= — tiles need uniform scale to preserve image aspect ratio
}
// Elevation displacement: move mesh so image follows the 3D box base
const E = elevation * gridSize / gridDistance;
mesh.x = (tile.document.x ?? 0) + hdx * E;
mesh.y = (tile.document.y ?? 0) + hdy * E;
// hdx/hdy from getProjection(scene).heightDir — for dimetric 2:1: {x:1, y:-1}
```

## TokenHUD / TileHUD Positioning

`HeadsUpDisplayContainer.align()` sets `#hud` CSS: `left = canvas.primary.getGlobalPosition().x`, `top = .y`, `transform = scale(zoom)`. **No rotation.**

CSS `left/top` within `#hud` are in canvas-unit space. Foundry default `_updatePosition` uses raw `token.bounds.x/y` — correct without rotation because container applies matching scale+translate.

With isometric rotation — correct formula (tx/ty and zoom cancel out):
```typescript
// Hook: Hooks.on("renderTokenHUD", (hud, html) => { ... })
// Use requestAnimationFrame so Foundry positions first, then override:
const m = canvas.app.stage.worldTransform;
const zoom = canvas.stage.scale.x;
const { x: cx, y: cy } = token.center;
const L = (m.a * cx + m.c * cy) / zoom;   // = cos(26.565°) * (cx + cy)
const T = (m.b * cx + m.d * cy) / zoom;   // b is negative → = sin(26.565°) * (cy - cx)
$html.css({ left: `${L}px`, top: `${T}px`, transform: "translate(-50%, -50%)" });
```

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

Key patterns:
- `Hooks.once("init", ...)` — register settings and hook listeners; fires once per session
- `Hooks.on("updateScene", (scene, changes) => { if (scene.id !== canvas.scene?.id) return; ... })` — always guard for current scene
- Render hooks for AppV2 sheets fire after DOM is built; html is already in document

## AppV2 Tab Injection

Nav selector differs by sheet type — SceneConfig uses `sheet-tabs`, others use `tabs`:
```typescript
const $nav = $html.find("nav.tabs:not(.secondary-tabs), nav.sheet-tabs:not(.secondary-tabs)").first();
```

Content element: `<div class="tab" data-tab="NAME">` (div, no data-group). Insert after last existing tab:
```typescript
$html.find(".tab[data-tab]").last().after($section);
// Falls inside .sheet-body — NOT after the footer.
```

AppV2 `changeTab()` validates against static `TABS` — unregistered tab names throw. Fix:
```typescript
$html.on("click", `a[data-tab="${TAB}"]`, (e) => {
  e.stopPropagation();                             // prevent AppV2 from calling changeTab
  $nav.find("a[data-tab]").removeClass("active");
  $html.find(".tab[data-tab]").removeClass("active");
  $(e.currentTarget).addClass("active");
  $html.find(`.tab[data-tab="${TAB}"]`).addClass("active");
});
// Also deactivate ours when other tabs clicked:
$nav.on("click", `a[data-tab]:not([data-tab="${TAB}"])`, () => {
  $html.find(`.tab[data-tab="${TAB}"], a[data-tab="${TAB}"]`).removeClass("active");
});
```

Other AppV2 gotchas:
- `html` in `renderSceneConfig` **IS the `<form>`** — `$html.find("form")` returns 0
- `[data-tab="basics"]` matches both nav `<a>` and content `<section>` — always add element type
- `name="flags.MODULE_ID.key"` on checkbox → Foundry auto-persists on form submit, no JS needed
- Do NOT clone the submit button — Foundry's own button handles form save

## Native Handle Suppression

Foundry renders interactive handles on selected placeables via `tile.controls` (a PIXI Container).
To suppress a specific handle (e.g. rotation triangle) in iso mode — place an invisible event-absorbing overlay on top:

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
Key: **`layer.toLocal(globalPos)`** converts screen coords to canvas coords; `getBounds()` gives screen-space size → divide by zoom to get canvas-space radius.  
The blocker must be in a layer added AFTER all Foundry layers (use `bringToTop()`) to intercept events.

## Depth Sort

`canvas.primary.children.sort()` corrupts Foundry's internal z-order.
Correct: use `PrimaryCanvasGroup` API, assign `zIndex` on objects or add custom foreground container.

## Reference Locations

- Fork with working patterns: `github.com/lsfcin/isometric-perspective`
  - `scripts/transform.js` — tile/token counter-transforms and uniform scale
  - `scripts/hud.js` — HUD repositioning math
  - `scripts/consts.js` — HudAngle per projection (dimetric 2:1 → 26.57°)
- Foundry v14 source (while server running):
  `/proc/$(pgrep -f 'foundry.*main')/cwd/resources/app/public/scripts/foundry.mjs`
  - `BasePlaceableHUD._updatePosition` — how HUD CSS left/top are set from token bounds
  - `HeadsUpDisplayContainer.align()` — how `#hud` container is positioned (no rotation)
  - `Canvas.clientCoordinatesFromCanvas` — uses full worldTransform matrix
