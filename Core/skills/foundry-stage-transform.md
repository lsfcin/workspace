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

`GridConfig` (Scene Config → Basics → grid wrench) adds preview overlay via `#createPreview()` directly on `canvas.stage`. Hook: `renderGridConfig` fires after `_onRender` completes (AppV2 async `_doEvent`).

**Preview container structure** (find by searching stage children in reverse for last plain `PIXI.Container`):
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
