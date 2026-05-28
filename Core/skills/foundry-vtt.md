Foundry VTT v14 module development reference. Load this context before any isoroll-module work.

Arguments: $ARGUMENTS

If arguments name a topic (e.g. "hud", "tabs", "transform"), jump to that section. Otherwise print the full reference.

---

# Foundry VTT v14 — Module Dev Reference

## Coordinate Systems

- **Canvas coords**: scene pixel space, origin = scene top-left (includes padding). `token.document.x/y`, `tile.document.x/y`.
- **Stage local space** = canvas coords. PIXI stage transform maps canvas → screen.
- **Screen / PIXI global coords**: `stage.worldTransform.apply({x, y})` → where point appears in CSS pixels relative to the PIXI canvas element.
- **`canvas.clientCoordinatesFromCanvas(pt)`**: calls `stage.worldTransform.apply(pt)` — same as above, uses full matrix including rotation.

## Isometric Stage Transform (dimetric 2:1)

```typescript
stage.rotation = rad(-45);
stage.skew.set(rad(18.435), rad(18.435));
// results in worldTransform matrix:
// a = zoom * cos(26.565°) ≈ zoom * 0.8944
// b = zoom * sin(-26.565°) ≈ zoom * -0.4472
// c = zoom * cos(26.565°) ≈ zoom * 0.8944  (note: same as a)
// d = zoom * sin(26.565°) ≈ zoom * 0.4472
// tx = stage.position.x, ty = stage.position.y
```

Counter-transform constants for dimetric 2:1:
- `reverseRotation = +45°`, `reverseSkewX = reverseSkewY = 0` (NOT −18.435° — that doubles distortion)
- `ratio = 2.0`, `counterFactor = √10/4 ≈ 0.7906`

## Background Counter-Transform

```typescript
// canvas.environment.primary.background — the rendered sprite in v14.
// canvas.primary.background exists but transforming it has NO visual effect.
bg.rotation = rad(45);
bg.skew.set(0, 0);
bg.anchor.set(0.5, 0.5);
// Foundry pre-scales the bg sprite — capture at canvasReady and multiply, don't override.
bg.scale.set(origScaleX * counterFactor, origScaleX * ratio * counterFactor);
bg.position.set(scene.width / 2 + paddingX, scene.height / 2 + paddingY);
```

## Per-Object Counter-Transform (tokens / tiles)

Hook: `refreshToken(token, flags?)` and `refreshTile(tile, flags?)`.

**Scale guard** — Foundry resets mesh scale on `refreshMesh | refreshSize | refreshShape | redraw`.
Only apply scale on those flags, never accumulate:

```typescript
const meshReset = !flags || flags["refreshMesh"] || flags["refreshSize"]
  || flags["refreshShape"] || flags["redraw"];
if (meshReset) { /* apply scale */ }
```

**Token (undistorted)**:
```typescript
mesh.rotation = reverseRotation;           // no docRotation — locks against v14 auto-facing
mesh.skew?.set(0, 0);
mesh.anchor?.set(0.5, 0.5);               // required for correct HUD bounds
if (meshReset) {
  mesh.scale.x *= counterFactor;
  mesh.scale.y *= ratio * counterFactor;
}
// TODO: use docRotation for 8-directional sprite selection (not implemented yet)
```

**Tile (undistorted, preserves aspect ratio)**:
```typescript
mesh.rotation = (docRotationDeg * Math.PI / 180) + reverseRotation;
mesh.skew?.set(0, 0);
if (meshReset) {
  const texW = mesh.texture?.width || 1;
  const texH = mesh.texture?.height || 1;
  const uniform = Math.max(docW, docH) / Math.max(texW, texH);  // largest dim wins
  mesh.scale.set(uniform * counterFactor, uniform * ratio * counterFactor);
}
// Do NOT use mesh.scale.x *= / mesh.scale.y *= — use mesh.scale.set() for tiles.
```

## TokenHUD / TileHUD Positioning

`#hud` container CSS: `left = canvas.primary.getGlobalPosition().x`, `top = .y`, `transform = scale(zoom)`.
**No rotation in the HUD container** — it only gets translate+scale.

CSS `left/top` values within `#hud` are in **canvas-unit** space. Foundry's default `_updatePosition` uses raw canvas bounds coords, which works without rotation because the container applies the matching scale+translate.

With isometric rotation, the correct projected coords (zoom cancels):
```typescript
const m = canvas.app.stage.worldTransform;
const zoom = canvas.stage.scale.x;
const L = (m.a * cx + m.c * cy) / zoom;   // = cos(26.565°) * (cx + cy)
const T = (m.b * cx + m.d * cy) / zoom;   // = sin(26.565°) * (cy - cx) (note: b is negative)
$html.css({ left: `${L}px`, top: `${T}px`, transform: "translate(-50%, -50%)" });
```

Hook: `renderTokenHUD(hud, html)`. Use `requestAnimationFrame(() => ...)` so Foundry positions first.

## AppV2 Tab Injection

**Nav selector differs by sheet type:**
- `SceneConfig` → `nav.sheet-tabs:not(.secondary-tabs)`
- `TokenConfig`, `TileConfig` → `nav.tabs:not(.secondary-tabs)`
- Safe combined: `nav.tabs:not(.secondary-tabs), nav.sheet-tabs:not(.secondary-tabs)`

**Content**: `<div class="tab" data-tab="isoroll">` (div, not section; no data-group).
Insert after: `$html.find(".tab[data-tab]").last()` — puts content inside `.sheet-body`, not after the footer.

**AppV2 changeTab rejects unregistered tabs** — "isoroll" is not in static TABS.
Fix: `e.stopPropagation()` on our nav item, activate manually:
```typescript
$html.on("click", `a[data-tab="${TAB}"]`, (e) => {
  e.stopPropagation();
  $nav.find("a[data-tab]").removeClass("active");
  $html.find(".tab[data-tab]").removeClass("active");
  $(e.currentTarget).addClass("active");
  $html.find(`.tab[data-tab="${TAB}"]`).addClass("active");
});
```
Also add delegated handler on nav to deactivate ours when other tabs are clicked.

**html in renderSceneConfig IS the `<form>`** — `$html.find("form")` returns 0. Use `$html` directly.

**Checkbox persistence**: `name="flags.MODULE_ID.key"` — Foundry auto-persists via form submit. No JS needed.

**Submit button**: Foundry's own button persists the form. Do NOT clone/append an extra one.

## Background Sprite Path

```typescript
// v14 — use environment path for visual effect:
canvas.environment?.primary?.background   // ✓ rendered sprite, transforms have visual effect
canvas.primary.background                  // ✗ different object, transforms do nothing visible
```

## Depth Sort

`canvas.primary.children.sort()` corrupts Foundry's internal z-order.
Correct approach: `PrimaryCanvasGroup` API, custom foreground container + `zIndex`. Not implemented in isoroll yet.

## Render Hooks Reference

| Hook | When | Args |
|------|------|------|
| `canvasReady` | Canvas fully loaded | — |
| `updateScene(scene, changes)` | Scene doc updated | changes has `flags.MODULE_ID` if flags changed |
| `refreshToken(token, flags)` | Token refreshed | flags: `refreshMesh`, `refreshSize`, `refreshShape`, `refreshRotation`, `redraw` |
| `refreshTile(tile, flags)` | Tile refreshed | same flags |
| `renderSceneConfig(app, html)` | SceneConfig sheet rendered | html IS the `<form>` |
| `renderTokenConfig(app, html)` | TokenConfig sheet rendered | — |
| `renderTileConfig(app, html)` | TileConfig sheet rendered | — |
| `renderTokenHUD(hud, html)` | Token right-click HUD shown | hud.object = Token |

## Reference

- Fork with working patterns: `github.com/lsfcin/isometric-perspective`
  - `scripts/transform.js` — tile/token counter-transforms
  - `scripts/hud.js` — HUD repositioning
  - `scripts/consts.js` — HudAngle per projection type (dimetric 2:1 → 26.57°)
- Foundry source: `/proc/$(pgrep -f foundry)/cwd/resources/app/public/scripts/foundry.mjs`
  - `BasePlaceableHUD._updatePosition` — how HUD CSS left/top are set
  - `HeadsUpDisplayContainer.align()` — how #hud container is positioned
  - `Canvas.clientCoordinatesFromCanvas` — uses full worldTransform
