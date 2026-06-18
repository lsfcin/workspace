---
name: foundry-object-transform
description: >
  Foundry VTT v14 — per-object (token/tile) mesh counter-transform, refresh flag semantics, PIXI mutation guards.
---

Foundry VTT v14 — per-object (token/tile) mesh counter-transform, refresh flag semantics, PIXI mutation guards.

---

## Per-Object Counter-Transform (tokens / tiles)

Hooks: `refreshToken(token, flags?)`, `refreshTile(tile, flags?)`.

Foundry resets mesh scale on certain flags:
```typescript
const meshReset = !flags || flags["refreshMesh"] || flags["refreshSize"]
  || flags["refreshShape"] || flags["redraw"];
// rotation: apply every refresh (absolute, not cumulative)
```

**v14 CRITICAL — `setFlag` does NOT trigger meshReset flags.**
`tile.document.setFlag(MODULE_ID, "someFlag", value)` fires `refreshTile` with flags
`{refreshPosition: true, refreshPerception: true}` — meshReset = **false**.
Code guarded by `if (meshReset)` skipped for custom-flag updates.

**`mesh.scale.set()` safe on every refresh** — absolute assignment (not `*=`), no accumulation risk. Remove `isMeshReset` guard from `mesh.scale.set()` calls if they need to respond to flag changes. Only guard `mesh.scale *= ...` patterns.

**v14 CRITICAL — token animations fire `refreshMesh` every frame, NOT `refreshPosition`.**
Foundry's hide/show animation (alpha lerp) and other non-movement animations call
`_onAnimationUpdate` each tick: sets `refreshMesh: true`, never `refreshPosition`.
`_refreshMesh()` updates only anchor/alpha/tint — does NOT reset `mesh.x/y`.
If hook overrides `mesh.x/y` and captures "natural base" on `refreshMesh`,
offset bakes in and re-adds every animation frame → image drifts off screen.

**`refreshPosition` flag — what actually sets it:**

Only `x` or `y` in update payload triggers `refreshPosition`:
- ✅ fires: movement (x/y update), movement animation frames (via `_onAnimationUpdate` with positionChanged=true)
- ❌ does NOT fire: `setFlag()`, elevation changes (`update({ elevation })`), other doc property changes

Consequence: **elevation changes update document but do NOT reset `mesh.x/y`**. Offsets only on `refreshPosition` → elevation drags silently break. Apply offsets on ALL refresh frames using cached tokenBase.

**Safe pattern for `mesh.x/y` override with elevation + image offset:**
```typescript
// Capture natural base only when _refreshPosition() ran (Foundry reset mesh.x to center).
// On setFlag / elevation changes (no refreshPosition): mesh.x was NOT reset — reuse cached
// base so we apply updated offset without accumulation.
// On refreshMesh-only (hide/show animation): also reuse base — _refreshMesh() never touches mesh.x/y.
if (!flags || flags["refreshPosition"]) {
  tokenBase.set(token, { x: mesh.x, y: mesh.y });
}
const base = tokenBase.get(token) ?? { x: mesh.x, y: mesh.y };
// Read elevation + offset fresh every frame so any document change is reflected immediately:
const E      = elevation * gridSize / gridDist;
const imgOff = VolumeFlags.getImageOffset(token.document);
mesh.x = base.x + hdx * E + imgOff.x;
mesh.y = base.y + hdy * E + imgOff.y;
```

`token.center` ≈ `{x: doc.x + docW/2, y: doc.y + docH/2}` — canvas center of token footprint.

## PIXI Overlay Drag-Drop Blink Guard

`refreshTile` hooks that redraw PIXI overlays (bounding boxes, gizmos, etc.) keyed by `tile.id` will cause a **1-frame blink** after drag-drop if they don't guard against the preview-clone lifecycle:

**What happens:**
1. During drag, the *clone* (isPreview=true) fires `refreshTile` — doc.x/y track cursor. Overlay draws at cursor. ✓
2. On drop, server confirms → doc.x/y update to new position → Foundry fires `refreshState+refreshVisibility` (no `refreshPosition`) on the *original* tile **while the clone still exists** (`hasPreview=true`). At this point `tile.document.x/y` is still the **old pre-drag position** — overlay redraws there. ← **the blink**
3. Clone is destroyed → original fires full refresh at correct new position. ✓

`hasPreview=true` identifies step 2 (original tile, clone still alive). Fix: skip overlay redraw in that state.

```typescript
private static onRefreshTile(tile: Tile, flags?: Record<string, boolean>): void {
  if (!overlay.has(tile.id)) return;
  // Skip while drag clone exists — server update fires refreshState with old doc pos before clone is cleared
  if ((tile as unknown as { hasPreview?: boolean }).hasPreview) return;
  redraw(tile); // now doc.x/y is correct final position
}
```

Clone's `refreshTile` fires with `isPreview=true` (not `hasPreview`), so it still updates the overlay during drag. Guard only suppresses the premature original-tile refresh.

## PIXI Mutation Guards — Prevent Dirty-Signal Feedback Loops

Setting PIXI props (`mesh.scale`, `mesh.rotation`, `mesh.anchor`) unconditionally on every `refreshToken` generates PIXI dirty signals → additional render-flag processing each frame. Guard before mutating:
```typescript
const EPS = 1e-6;
if (Math.abs(mesh.rotation - reverseRotation) > EPS) mesh.rotation = reverseRotation;
if (mesh.skew && (mesh.skew.x !== 0 || mesh.skew.y !== 0)) mesh.skew.set(0, 0);
if (mesh.anchor && (Math.abs(mesh.anchor.x - 0.5) > EPS || Math.abs(mesh.anchor.y - 0.5) > EPS)) {
  mesh.anchor.set(0.5, 0.5);
}
const targetSX = uniform * counterFactor, targetSY = uniform * ratio * counterFactor;
if (Math.abs(mesh.scale.x - targetSX) > EPS || Math.abs(mesh.scale.y - targetSY) > EPS) {
  mesh.scale.set(targetSX, targetSY);
}
// For flipped tiles (scale.x < 0): compare magnitude when guarding scale.
```
After initial setup, subsequent refresh calls find values correct and skip → no dirty signal.

## token.visible vs document.hidden — transient vs stable

`token.visible` is a transient PIXI property. Foundry sets it to `false` during:
- Token drag (mid-drag, while preview clone exists)
- Canvas layer switches (switching from tokens to tiles layer etc.)
- Any state where Foundry temporarily hides the token's PIXI subtree

**Never use `token.visible` to drive clone visibility** — clone will flicker and disappear during drag.

`document.hidden` is the stable, GM-set game state. Only changes when a GM explicitly hides/shows the token via the HUD. Use this for clone visibility:

```typescript
clone.visible = !token.document.hidden;
clone.alpha   = typeof token.document.alpha === "number" ? token.document.alpha : 1;
```

Same applies to tiles: `tile.visible` is transient, `tile.document.hidden` is stable.

## Clone Sync Pattern — geometry only, alpha from document

When cloning a `PrimarySpriteMesh` to an external layer (see `foundry-canvas.md` — VisibilityFilter escape), split sync into two separate operations:

**`syncSprite(clone, mesh)`** — geometry ONLY, called on every refresh:
```typescript
clone.texture   = mesh.texture ?? PIXI.Texture.EMPTY;
clone.position.set(mesh.x, mesh.y);
if (mesh.anchor) clone.anchor.set(mesh.anchor.x, mesh.anchor.y);
if (mesh.skew)   clone.skew.set(mesh.skew.x, mesh.skew.y);
if (mesh.scale)  clone.scale.set(mesh.scale.x, mesh.scale.y);
clone.rotation  = mesh.rotation ?? 0;
// DO NOT copy mesh.alpha — we set it to 0; copying it kills the clone
// DO NOT copy mesh.visible — transient PIXI state; use document instead
```

**`applyDocState(clone, doc)`** — visibility from document, called after syncSprite:
```typescript
clone.alpha   = typeof doc.alpha === "number" ? doc.alpha : 1;
clone.visible = !doc.hidden;
```

Always call both in sequence on `refreshToken`/`refreshTile`. After geometry sync, set `mesh.alpha = 0` again (Foundry may have reset it to 1 during its own refresh pass).

## Token (Undistorted)

```typescript
mesh.rotation = reverseRotation;       // lock rotation — v14 auto-rotates tokens on move
mesh.skew?.set(0, 0);
mesh.anchor?.set(0.5, 0.5);           // required — HUD bounds derived from this
// scale.set() is absolute/safe every refresh — no meshReset guard needed
const uniform = (token.document.width ?? 1) * gs / (mesh.texture?.width || 1);
mesh.scale.set(uniform * counterFactor, uniform * ratio * counterFactor);
```

## Tile (Undistorted, Preserves Aspect Ratio)

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
