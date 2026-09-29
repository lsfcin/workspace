# Google Slides API — facts worth not rediscovering
> What the API actually returns, learned the expensive way — read alongside `CONTEXT.md`.

## Slidev is gone (2026-08-14)

This family used to be a Slidev CLI plus a Google-Slides→Slidev port pipeline (`slides_port`, `slides_shapes`, `slides_style`, `slides_text`). Lucas retired it once remote editing into the live deck was confirmed working: the reason to port decks out was that the source of truth could not be edited from here, and it can. **Resurrecting a local presentation format needs that reason to come back first** — what survived is `slides_geom.py`, the transform algebra below.

## Auth

Two grants: `slides` (`presentations.readonly`) and `slides-write` (`presentations`), the same split as [`../files/`](../files/CONTEXT.md). A read prefers the write token when the alias has one — the edit consent already contains the read consent, so demanding a second browser trip would buy no safety and just create two tokens that can die independently.

**The two grants live in two directories, and the write one is easy to miss.** A read token is `~/.config/workspace-slides/<alias>.token.json`; a write token is `~/.config/workspace-slides-**write**/<alias>.token.json` — the grant name *is* the directory suffix, via `gauth.config_dir(kind)`. Checking the read directory to see whether a write grant landed answers **no** forever, no matter how many times the consent succeeds. That failure ran four times in one session on 2026-08-17, while `gslides auth` printed the real path on its own last line each time. **Read the tool's output, not a directory you inferred the name of.**

## Geometry

- **Slide dimensions: `9144000 × 5143500` EMU** (standard 16:9). `slides_geom.py` reports every position and size as a fraction of these, and the write path takes the same fraction back.
- **A stored `size` is a base size, not the rendered one.** The rendered box is `size × scale` from the transform. An ordinary API-created text box comes back at `scaleY ≈ 0.26`.
- **Rotation lives in the matrix, not in a field**: `atan2(shearY, scaleX)`.
- **`scaleX` of exactly `0.0` is meaningful** — it is what a quarter turn stores. Coalescing it with `or 1.0` reports those elements as 45°, which is the bug the geometry tests now pin.
- **Group members carry transforms relative to their group**, so a member's absolute position is `compose_transforms(group, member)`.

## Ghosts

Slides keeps hidden animation states as **zero-scaled copies** of real elements, and their stored `size` is normal — so a size check cannot find them, only a scale check can. The old port used `eff_scale < 0.4` on either axis. **That threshold was wrong outside ported decks**: real elements routinely sit below it (see above), so it silently ate live content. Anything filtering ghosts needs near-zero on *both* axes, and `read` does not filter at all — hiding a real element is worse than showing a hidden one.

## Colors and fills

- `shapeBackgroundFill.propertyState = "INHERIT"` means "use the theme default", and it means two different things by context: on master elements it is decoration that should stay invisible; on a slide element with no text and no outline it is a visible accent box relying on the theme color.
- Lines with no explicit `solidFill.color` have **no color**, not black. Defaulting them to black renders invisible connector lines as spurious diagonals.
- `CENTERED_TITLE` placeholders do not store paragraph alignment — it is inherited from the theme.

## Rendering

- **`getThumbnail` is an "expensive read"** with a per-minute quota: a 20-slide deck hits 429. `preview` exports one PDF through Drive and renders it locally.
- **Drive refuses exports over ~10 MB** ("too large to be exported"); a link-shared deck still has the public `/export/pdf`, which `preview` falls back to.

## Writing

- **Object ids must be at least 5 characters.** A shorter one fails the whole batch with `Invalid requests[N]: The object ID (x) length should not be less than 5`.
- **`batchUpdate` is atomic and ordered**: requests apply in sequence, and one rejection rolls back the batch. Create-then-modify in a single call is safe.
- **`duplicateObject` takes an `objectIds` map**, so a copy's children get ids you chose instead of generated ones — this is what makes a generated frame sequence addressable.
- **Duplicates are inserted directly after their source**, so duplicating one slide N times leaves the copies in reverse order. `updateSlidesPosition` in the same batch fixes it.
- **Per-frame motion is the two facts above, chained**: `duplicateObject` + `updatePageElementTransform` in one `batchUpdate` authors position/velocity/acceleration sampled into frames, and it survives PDF export (confirmed 2026-08-14).
- **A layout cannot be created, duplicated, or swapped on an existing slide** (`Duplicating a layout is not allowed`; `layoutObjectId` is read-only), but its elements are edited by id and slides inherit position and style live — so a template is a deck you copy, and a new look is an edit to its master/layouts. `isSkipped` is writable (confirmed 2026-09-24). **New layouts and masters therefore come in as a .pptx** (`pptx template` → `gdrive put --slides`): Drive's conversion keeps every master (named), every layout (named), each master's own theme colours, and shape fills and text colours as `themeColor` slots rather than RGB — so one layout set, repeated under one master per section colour, recolours by theme (confirmed 2026-09-26). `normAutofit` arrives as `TEXT_AUTOFIT`, hence the generator writes `noAutofit`.
- **Transitions and animations also come in only as a .pptx**: the API and Apps Script cannot set either, but Drive's conversion keeps `p14:flip`, `p14:prism` (cube), `p14:gallery`, `p:push` (left/right), `p:fade`, dissolve (`fade thruBlk`, where unsupported ones like `p:zoom` land), their `p14:dur`, and object animations (appear/disappear, fade, fly, zoom, spin, "after previous" chains, alpha fills); Morph and PowerPoint Zoom are dropped whole. After import, `duplicateObject` and text rewrites keep a slide's transition and every animation. Transforms never scale text: a shape's scale resizes its box and the text re-wraps (confirmed 2026-09-27; generator in `outputs/.drafts/taste-img/motion_showcase.py`).
- **Restyle a placeholder before shrinking it**: shrinking first makes Slides write a local `fontSize` into every inheriting slide to fit the old text, which cuts inheritance; `updateTextStyle` with the field listed and no value restores it.

## PowerPoint and Canva (tested 2026-09-28; the home is PowerPoint, `core/prompts/slides-padroes.md`)
- **PowerPoint online plays what `pptx` writes**: `p159:morph`, `animScale` (Grow/Shrink), `animMotion` straight and Bézier paths that stay at their end point, and `withEffect` groups on one click. The Transparency emphasis needs BOTH a held `style.opacity` set and `animEffect filter="image" prLst="opacity: x"`: the set alone is ignored and flickers back. Effects sharing a click need equal `dur`, or the move and the scale visibly desync.
- **Online has Atkinson Hyperlegible Next in 400 and 700 only** (Office's PDF, 2026-09-29): ExtraBold, SemiBold and Light fall to Calibri or regular without a word.
- **Also plays online** (spike 2026-09-29, `outputs/.drafts/rodada7/spike.py`): `accel`/`decel` easing, `repeatCount="indefinite"` until the next click (spin a polygon: a flat circle hides it), a trigger on a shape (one-way so far), a native link to a slide, `advTm` auto-advance, text alpha grown in by Morph, and a hole-veil scaled 24× by Morph through `xfrm` alone (hole × zoom past the half-diagonal, 7.6 in, or corners show; its edge rasterises and looks pixelated).
- **Does not**: the "last slide viewed" action (it advances instead; 'back' is a link to the named slide), a generated Slide Zoom (a plain jump that then scrambles navigation), Morph after a link jump (a cut), an in-slide dim followed by Morph (the Morph starts from the static slide: it flashes back to 100%). Wipe's soft edge reads cheap.
- **Morph pairs points only between copies.** Changing position, size, rotation or alpha works on frames built separately; changing the POINTS of a freeform or `custGeom` does not (freeforms fade, arcs shatter into triangles) unless the next frame is a duplicate of the previous with the same point structure. Morph by character failed between two separately built text boxes. Build a frame by copying the one before it and editing, the way a person does in PowerPoint.
- **A deck open in PowerPoint online is locked**: overwriting it answers `423 resourceLocked`, so an agent edit is a new upload or waits for the tab to close.
- **Canva cannot receive motion from an agent.** REST (`@canva/cli`: `canva api …`), the MCP server (edits text and image fills only) and the Apps SDK's Design Editing API set no animation or transition. Its .pptx import keeps layout, notes, alpha and Anton, but maps Atkinson Hyperlegible Next to the original, collapses every transition (push, flip, prism, gallery, Morph) to dissolve, and drops object animations.
