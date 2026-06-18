---
name: foundry-stage-transform
description: >
  Foundry VTT v14 — isometric stage transform, background counter-transform, GridConfig preview counter-transform.
---

Foundry VTT v14 — isometric stage transform, background counter-transform, GridConfig preview counter-transform.

---

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

## PIXI worldTransform Cache — Initial Load Gotcha

PIXI only recomputes `stage.worldTransform` during its render loop. After setting `stage.rotation` / `stage.skew.set()` in `canvasReady`, `worldTransform` is still **identity** until the next render frame.

Additionally, Foundry sets `#hud style.left = wt.tx` / `style.top = wt.ty` **only inside `canvasPan`**. On initial load, `canvasPan` never fires, so `#hud` is misaligned after `applyStage()` changes `wt.tx/ty`.

**Fix — call after `applyCurrentState()` in `onCanvasReady`:**

```typescript
private static syncHudAfterStageApply(): void {
  const stage = canvas.app?.stage;
  if (!stage) return;
  // Step 1: flush worldTransform cache (stage is root — call 2-step instead of updateTransform())
  stage.transform.updateLocalTransform();
  stage.worldTransform.copyFrom(stage.localTransform);
  // Step 2: sync #hud CSS to match what canvasPan would have done
  const wt  = stage.worldTransform;
  const hud = document.getElementById("hud");
  if (hud) { hud.style.left = `${wt.tx}px`; hud.style.top = `${wt.ty}px`; }
}
```

> `stage.updateTransform()` crashes when `stage.parent` is null (which it is during `canvasReady`). Use the two-step alternative: `updateLocalTransform()` then `copyFrom(localTransform)`.

## Background Counter-Transform

Foundry pre-scales bg sprite to fill canvas (`PrimarySpriteMesh` scale ≠ 1).
Capture original scale at `canvasReady`, multiply — do NOT hardcode `scale(1, ratio)` (→ ~1/4 size).

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

## GridConfig Preview Tool

`GridConfig` (Scene Config → Basics → grid wrench) adds preview overlay via `#createPreview()` directly on `canvas.stage`. Hook: `renderGridConfig` fires after `_onRender` completes (AppV2 async `_doEvent`). Hook `closeGridConfig` fires in `_onClose`.

**Preview container structure** (find by searching stage children in reverse for last plain `PIXI.Container`):

> **CRITICAL**: search for the preview container BEFORE adding any overlay PIXI.Container layer of your own — your layer would be found first (also a plain `PIXI.Container`). Cache the reference at `renderGridConfig` time; reuse on subsequent calls.
```typescript
// children[0] = black fill (screen-space, always correct)
// children[1] = background Sprite  ← position/scale reset by #refreshPreview on every form change
// children[2] = grid mesh          ← inherits stage transform (keep isometric)
for (let i = stage.children.length - 1; i >= 0; i--) {
  const c = stage.children[i];
  if (c instanceof PIXI.Container && c.constructor === PIXI.Container) { previewContainer = c; break; }
}
```

`#refreshPreview()` resets on every form change: `bg.position.set(sceneX, sceneY)`, `bg.width = sceneWidth` (sets `scale.x = sceneWidth / texture.width`).

### Counter-Transform Pattern (updateTransform Override)

Override bg sprite's `updateTransform` with **save→apply→origUpdate→restore** so `#refreshPreview` per-change resets picked up cleanly each frame, no accumulation. Do NOT transform container — grid mesh must inherit stage isometric transform, camera position stays stable.

```typescript
const origUpdate = bg.updateTransform.bind(bg);
(bg as any).updateTransform = function(this: PIXI.Sprite) {
  const x = this.x, y = this.y, sx = this.scale.x, sy = this.scale.y;
  const rot = this.rotation;
  const ax = this.anchor.x, ay = this.anchor.y;
  const skx = this.skew.x, sky = this.skew.y;
  const tw = this.texture?.width ?? 1, th = this.texture?.height ?? 1;
  // apply counter-transform
  this.anchor.set(0, 0);  // position = texture top-left; center via R·S matrix below
  this.rotation = proj.reverseRotation;
  this.skew.set(proj.reverseSkewX, proj.reverseSkewY);
  this.scale.set(sx * proj.counterFactor, sx * proj.ratio * proj.counterFactor);
  // center image on grid: scene center + R·S·(-tw/2,-th/2) converts texture half-size to canvas space
  // skew=0 for all presets: R·S(vx,vy) = (cos·scX·vx − sin·scY·vy, sin·scX·vx + cos·scY·vy)
  const cosR = Math.cos(proj.reverseRotation), sinR = Math.sin(proj.reverseRotation);
  const scX = sx * proj.counterFactor, scY = sx * proj.ratio * proj.counterFactor;
  this.position.set(
    x + sx * tw * 0.5 + cosR * scX * (-tw * 0.5) - sinR * scY * (-th * 0.5),
    y + sy * th * 0.5 + sinR * scX * (-tw * 0.5) + cosR * scY * (-th * 0.5),
  );
  origUpdate.call(this);
  // restore so next frame starts clean (#refreshPreview resets x/y/scale on every form change)
  this.anchor.set(ax, ay); this.rotation = rot; this.skew.set(skx, sky);
  this.scale.set(sx, sy); this.position.set(x, y);
};
```

> **Centering invariant**: if you apply an extra Y multiplier (e.g. `bgYScale`) to `scale.set()`, you **must** also use the same multiplied `scY` in the position formula. Using `scY` without `bgYScale` in position while `scale.set` uses it will shift the visual center upward as the scale decreases — image anchors to its top edge instead of scaling around center.

### GridConfig Form Fields

Native form elements (accessible via `this.form.elements.<name>` inside GridConfig, or `form.elements.namedItem(n)` from outside):

| Name | Meaning | Units | Dispatch |
|------|---------|-------|---------|
| `scale` | Background scale (`sceneWidth / texture.width`) | unitless, range 0.25–10 | `change` event → `_onChangeForm` → `#previewChanges` → `#refreshPreview` |
| `shiftX` / `shiftY` | Scene offset (bg position shift) | canvas pixels | same |
| `grid.size` | Grid cell size | canvas pixels | same |
| `grid.type` | Grid type enum | — | same |

Trigger preview update from code: `el.value = newVal; el.dispatchEvent(new Event("change", { bubbles: true }))`.

### GridConfig `_processSubmitData` — Non-Native Fields

`_processSubmitData` only calls `super._processSubmitData` (→ `document.update`) if one of the 7 native fields above changed. Module-specific form fields are silently skipped.

**Workaround**: patch the instance at `renderGridConfig` time:
```typescript
if (typeof app._processSubmitData === 'function') {
  const orig = app._processSubmitData.bind(app);
  app._processSubmitData = async (...a: unknown[]) => {
    await orig(...a);
    // save module flag regardless of whether native fields changed
    await canvas.scene?.setFlag(MODULE_ID, "myFlag", currentValue);
  };
}
```
This runs after Foundry's native save (or even if Foundry skipped saving). Safe to do on every re-render because the patch is on the instance, not the prototype.
