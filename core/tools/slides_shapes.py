#!/mnt/workspace/.venv/bin/python3
# slides_shapes.py — Element rendering (shapes, lines, tables, images, groups) for slides_port

import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slides_text import text_html, has_content
from slides_style import (_fill_color, _gradient_css, rotation_deg,
                          eff_scale, compose_transforms, _bounds, _download)

# SVG path shapes (100×100 viewBox, OOXML paths normalized to %)
_SVG_PATHS = {
    "LIGHTNING_BOLT": "M 34.6,0 L 12.3,56 31.7,56 0,100 69.3,44 49.9,44 80.3,0 Z",
    "RIGHT_TRIANGLE": "M 0,100 L 0,0 100,100 Z",
}


def _rot_css(el: dict) -> str:
    rot = rotation_deg(el.get("transform", {}))
    return f";transform-origin:0 0;transform:rotate({rot:.2f}deg)" if abs(rot) > 0.1 else ""


def _render_shape(el: dict, l: float, t: float, w: float, h: float,
                  ph_sizes: dict[str, int] = {}, is_master: bool = False,
                  ph_valign: dict[str, str] = {},
                  ph_weight: dict[str, int] = {},
                  ph_color: dict[str, str] = {},
                  ph_family: dict[str, str] = {}) -> str | None:
    shape = el["shape"]
    sp    = shape.get("shapeProperties", {})

    bg  = sp.get("shapeBackgroundFill", {})
    bps = bg.get("propertyState", "")
    if bps == "NOT_RENDERED":
        if not is_master:
            esx, esy = eff_scale(el.get("transform", {}))
            if esy < 0.4 or esx < 0.4:
                return None
        fc = None
    elif bps == "INHERIT":
        fc = None
    else:
        solid = bg.get("solidFill"); grad = bg.get("gradientFill")
        fc = _fill_color(solid) if solid else (_gradient_css(grad) if grad else None)

    sc, sw = None, 0.0
    outline = sp.get("outline", {})
    if outline.get("propertyState") != "NOT_RENDERED":
        _sc = _fill_color(outline.get("outlineFill", {}).get("solidFill", {}))
        _sw = outline.get("weight", {}).get("magnitude", 0)
        if _sc and _sw:
            sc, sw = _sc, round(_sw / 12700, 1)

    ph      = shape.get("placeholder", {}).get("type", "")
    inner   = text_html(shape.get("text", {}), is_title=ph in {"TITLE", "CENTERED_TITLE"},
                        default_font_size=ph_sizes.get(ph),
                        default_font_weight=ph_weight.get(ph),
                        default_font_color=ph_color.get(ph),
                        default_font_family=ph_family.get(ph))
    stype   = shape.get("shapeType", "")
    # Slide-level INHERIT-fill shapes with no other visible content → render as ACCENT1 (theme default)
    # Exclude master elements: their INHERIT-fill decorations should remain transparent
    if bps == "INHERIT" and not is_master and not has_content(inner) and not sc:
        fc = _fill_color({"color": {"themeColor": "ACCENT1"}})
    rcs     = _rot_css(el)
    base    = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%{rcs}"

    if stype in _SVG_PATHS:
        sf  = f'fill="{fc or "none"}"' + (f' stroke="{sc}" stroke-width="{sw}"' if sc else "")
        svg = f'<svg class="absolute" style="{base}" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{_SVG_PATHS[stype]}" {sf}/></svg>'
        return svg + (f'\n<div class="absolute overflow-hidden" style="{base}">{inner}</div>' if has_content(inner) else "")

    css: list[str] = []
    if fc:  css.append(f"background:{fc}")
    if sc:  css.append(f"border:{sw}pt solid {sc}")
    if stype == "ELLIPSE":            css.append("border-radius:50%")
    elif "ROUND" in stype:            css.append("border-radius:6px")
    elif stype == "FLOW_CHART_DELAY": css.append("border-radius:0 50% 50% 0 / 0 50% 50% 0")
    ca = sp.get("contentAlignment") or ph_valign.get(ph, "")
    if ca == "MIDDLE":
        css.append("display:flex;flex-direction:column;justify-content:center")
    elif ca == "BOTTOM":
        css.append("display:flex;flex-direction:column;justify-content:flex-end")
    if not has_content(inner) and not css:
        return None
    style = base + (";" + ";".join(css) if css else "")
    return f'<div class="absolute overflow-hidden" style="{style}">{inner if has_content(inner) else ""}</div>'


_PX_W, _PX_H = 960, 540  # canonical slide px (Google Slides EMU at 96 dpi)


def _render_line(el: dict, slide_w: float, slide_h: float) -> str | None:
    lp  = el.get("line", {}).get("lineProperties", {})
    lf  = lp.get("lineFill", {})
    if lf.get("propertyState") == "NOT_RENDERED":
        return None
    color = _fill_color(lf.get("solidFill", {}))
    if color is None:
        return None  # no explicit fill → inherited/transparent connector, skip
    wt_px = round(lp.get("weight", {}).get("magnitude", 9525) / 12700 * 1.333, 1)
    ea  = lp.get("endArrow", "NONE"); sa = lp.get("startArrow", "NONE")
    tf  = el.get("transform", {}); sz = el.get("size", {})
    sw_e = sz.get("width",  {}).get("magnitude", 0)
    sh_e = sz.get("height", {}).get("magnitude", 0)
    sx  = tf.get("scaleX")  or 0.0; sy  = tf.get("scaleY")  or 0.0
    shx = tf.get("shearX")  or 0.0; shy = tf.get("shearY")  or 0.0
    tx  = tf.get("translateX", 0) or 0; ty = tf.get("translateY", 0) or 0
    x1 = tx/slide_w*_PX_W; y1 = ty/slide_h*_PX_H
    x2 = (tx + sx*sw_e + shx*sh_e)/slide_w*_PX_W
    y2 = (ty + shy*sw_e + sy*sh_e)/slide_h*_PX_H
    if abs(x2-x1) < 0.5 and abs(y2-y1) < 0.5: return None
    ms_px = max(8, int(wt_px * 6))
    oid = el.get("objectId", "x")[-6:]
    defs, me, ms = "", "", ""
    if ea != "NONE":
        defs += (f'<defs><marker id="e{oid}" viewBox="0 0 10 10" refX="9" refY="5"'
                 f' markerWidth="{ms_px}" markerHeight="{ms_px}" markerUnits="userSpaceOnUse" orient="auto">'
                 f'<path d="M0,0 L10,5 L0,10z" fill="{color}"/></marker></defs>')
        me = f' marker-end="url(#e{oid})"'
    if sa != "NONE":
        defs += (f'<defs><marker id="s{oid}" viewBox="0 0 10 10" refX="1" refY="5"'
                 f' markerWidth="{ms_px}" markerHeight="{ms_px}" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                 f'<path d="M0,0 L10,5 L0,10z" fill="{color}"/></marker></defs>')
        ms = f' marker-start="url(#s{oid})"'
    style = "position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;overflow:visible"
    return (f'<svg style="{style}" viewBox="0 0 {_PX_W} {_PX_H}">'
            f'{defs}<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{wt_px}"{me}{ms}/></svg>')


def _render_table(el: dict, l: float, t: float, w: float, h: float) -> str:
    tbl  = el.get("table", {})
    rows = []
    for row in tbl.get("tableRows", []):
        cells = "".join(
            f'<td style="padding:0;vertical-align:middle">{text_html(c.get("text", {}))}</td>'
            for c in row.get("tableCells", [])
        )
        rows.append(f"<tr>{cells}</tr>")
    rcs   = _rot_css(el)
    style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%;overflow:visible{rcs}"
    tbl_s = 'style="width:100%;height:100%;border-collapse:collapse"'
    return f'<div class="absolute" style="{style}"><table {tbl_s}><tbody>{"".join(rows)}</tbody></table></div>'


def render_element(el: dict, slide_w: float, slide_h: float,
                   assets_dir: pathlib.Path | None, img_n: list[int],
                   ph_sizes: dict[str, int] = {}, ph_valign: dict[str, str] = {},
                   ph_weight: dict[str, int] = {}, ph_color: dict[str, str] = {},
                   ph_family: dict[str, str] = {}, is_master: bool = False) -> str | None:
    """Render any page element to HTML. Returns None if element has no visual output."""
    if "elementGroup" in el:
        pt    = el.get("transform", {})
        parts = []
        for child in el["elementGroup"].get("children", []):
            child = dict(child)
            child["transform"] = compose_transforms(pt, child.get("transform", {}))
            block = render_element(child, slide_w, slide_h, assets_dir, img_n,
                                   ph_sizes, ph_valign, ph_weight, ph_color, ph_family, is_master)
            if block:
                parts.append(block)
        return "\n".join(parts) or None

    if "line" in el: return _render_line(el, slide_w, slide_h)

    l, t, w, h = _bounds(el, slide_w, slide_h)

    if "image" in el:
        url = el["image"].get("contentUrl", "")
        if not url:
            return None
        img_n[0] += 1
        ref = url
        if assets_dir:
            saved = _download(url, assets_dir / f"img_{img_n[0]:03d}")
            if saved:
                ref = f"./assets/{saved.name}"
        rcs  = _rot_css(el)
        crop = el["image"].get("imageProperties", {}).get("cropProperties", {})
        lc   = crop.get("leftOffset", 0); rc = crop.get("rightOffset", 0)
        tc   = crop.get("topOffset",  0); bc = crop.get("bottomOffset", 0)
        if lc or rc or tc or bc:
            vw, vh = max(1-lc-rc, 0.01), max(1-tc-bc, 0.01)
            wrap = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%;overflow:hidden;position:absolute{rcs}"
            ipos = f"position:absolute;left:{-lc/vw*100:.1f}%;top:{-tc/vh*100:.1f}%;width:{100/vw:.1f}%;height:{100/vh:.1f}%"
            return f'<div style="{wrap}"><img src="{ref}" style="{ipos}" /></div>'
        style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%{rcs}"
        return f'<img src="{ref}" class="absolute" style="{style}" />'

    if "shape" in el: return _render_shape(el, l, t, w, h, ph_sizes, is_master, ph_valign, ph_weight, ph_color, ph_family)
    if "table" in el: return _render_table(el, l, t, w, h)
    return None
