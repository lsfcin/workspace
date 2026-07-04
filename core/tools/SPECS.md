# Slides Pipeline — Specs & Architecture Decisions

## Architecture Decisions

### Ghost filter: scale-based, not size-based
`eff_scale(transform)` returns `(sqrt(sx²+shy²), sqrt(sy²+shx²))` — the magnitude of the transform matrix columns. Ghost animation elements in Google Slides API have `scaleX ≈ 0`, `scaleY ≈ 0` (zero-scaled hidden state). Threshold: `esy < 0.4 or esx < 0.4` → skip. This is a SCALE check, not a physical size check. Normal elements have scale=1.0 regardless of physical dimensions.

### INHERIT fill: master vs slide elements
`shapeBackgroundFill.propertyState = "INHERIT"` means "use theme default color". Behavior differs by context:
- **Master elements** (`is_master=True`): keep transparent (`fc = None`). Master decorations with INHERIT fill should stay invisible.
- **Slide elements** with no text and no outline (`not is_master and not has_content(inner) and not sc`): apply ACCENT1 (`rgb(103,78,167)`) as theme fallback. These are shapes like visible accent boxes that rely on theme color.
- **Slide elements with text**: keep transparent — the text is the visible content.

### Line rendering: no default fill
Lines with no explicit `solidFill.color` (empty dict or missing `solidFill`) are skipped. Previously defaulted to black, which rendered invisible connector lines as spurious black diagonals. Fix: `if color is None: return None`.

### Font weight: 400 is the no-op
`weightedFontFamily.weight = 400` (Regular) is not emitted as inline CSS — body text inherits from `style.css` global rule (`font-weight: 300`). Only non-400 weights (300, 700, 900) are emitted as `font-weight:N` spans. This means body text rendered without explicit weight gets Raleway Light (300) from CSS default.

### style.css is regenerated on every port
`_make_style_css()` in `core/tools/slides` rewrites `style.css` on each port. Must include all desired global rules there, not just font imports.

### mouseWheel: true in Slidev frontmatter doesn't work
Slidev 52.16.0 ignores `mouseWheel: true` in frontmatter. Wheel navigation requires a custom `setup/main.ts` with a `wheel` event listener. Current impl uses delta accumulation (`accum += deltaY`; advance at ±100 threshold) so one mechanical tick = one slide, trackpad works too. Import `@slidev/types` fails — `@slidev/types` is nested inside `@slidev/cli/node_modules/` and not resolvable from project root. Use plain TypeScript function signatures instead.

### CENTERED_TITLE placeholder needs default_align="center"
Google Slides doesn't store paragraph alignment explicitly for CENTERED_TITLE — it's inherited from theme. Must pass `default_align="center"` to `text_html()` for CENTERED_TITLE placeholders.

### Table overflow: visible, not hidden
Tables use `overflow:visible` (not `hidden` or `auto`) to prevent last-row clipping from browser `<td>` padding. Combined with `style.css` rule `.slidev-slide td { padding: 0; }`.

## Conventions

- All `<p>` tags get `margin:0` via `para_css = ["margin:0"]` default — overrides browser 16px margin.
- `h1/h2/h3` get `margin: 0` via style.css global rule.
- Slide dimensions: `9144000 × 5143500 EMU` (standard Google Slides 16:9). Position/size uses percentage of slide dimensions.
- Canvas pixel space for SVG lines: `960 × 540 px` (`_PX_W, _PX_H`).
