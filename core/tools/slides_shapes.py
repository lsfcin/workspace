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


def _render_shape(el: dict, l: float, t: float, w: float, h: float) -> str | None:
    shape = el["shape"]
    sp    = shape.get("shapeProperties", {})

    bg = sp.get("shapeBackgroundFill", {})
    if bg.get("propertyState") == "NOT_RENDERED":
        esx, esy = eff_scale(el.get("transform", {}))
        if esy < 0.4 or esx < 0.4:
            return None
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
    inner   = text_html(shape.get("text", {}), is_title=ph in {"TITLE", "CENTERED_TITLE"})
    stype   = shape.get("shapeType", "")
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
    if not has_content(inner) and not css:
        return None
    style = base + (";" + ";".join(css) if css else "")
    return f'<div class="absolute overflow-hidden" style="{style}">{inner if has_content(inner) else ""}</div>'


def _render_line(el: dict, l: float, t: float, w: float, h: float) -> str:
    lp    = el.get("line", {}).get("lineProperties", {})
    color = _fill_color(lp.get("lineFill", {}).get("solidFill", {})) or "rgb(0,0,0)"
    wt    = round(lp.get("weight", {}).get("magnitude", 9525) / 12700, 1)
    ea    = lp.get("endArrow",   "NONE")
    sa    = lp.get("startArrow", "NONE")

    ratio = h / w if w > 0.01 else 999
    if ratio < 0.05:
        x1, y1, x2, y2 = "0", "50", "100", "50"
    elif ratio > 20:
        x1, y1, x2, y2 = "50", "0", "50", "100"
    else:
        x1, y1, x2, y2 = "0", "0", "100", "100"

    oid  = el.get("objectId", "x")[-6:]
    defs, me, ms = "", "", ""
    if ea != "NONE":
        defs += f'<defs><marker id="e{oid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="{color}"/></marker></defs>'
        me = f' marker-end="url(#e{oid})"'
    if sa != "NONE":
        defs += f'<defs><marker id="s{oid}" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10z" fill="{color}"/></marker></defs>'
        ms = f' marker-start="url(#s{oid})"'

    style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%;overflow:visible"
    return (f'<svg class="absolute" style="{style}" viewBox="0 0 100 100" preserveAspectRatio="none">'
            f'{defs}<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{wt}"{me}{ms}/></svg>')


def _render_table(el: dict, l: float, t: float, w: float, h: float) -> str:
    tbl  = el.get("table", {})
    rows = []
    for row in tbl.get("tableRows", []):
        cells = "".join(f"<td>{text_html(c.get('text', {}))}</td>" for c in row.get("tableCells", []))
        rows.append(f"<tr>{cells}</tr>")
    rcs  = _rot_css(el)
    style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%;overflow:auto{rcs}"
    return f'<div class="absolute" style="{style}"><table><tbody>{"".join(rows)}</tbody></table></div>'


def render_element(el: dict, slide_w: float, slide_h: float,
                   assets_dir: pathlib.Path | None, img_n: list[int]) -> str | None:
    """Render any page element to HTML. Returns None if element has no visual output."""
    if "elementGroup" in el:
        pt    = el.get("transform", {})
        parts = []
        for child in el["elementGroup"].get("children", []):
            child = dict(child)
            child["transform"] = compose_transforms(pt, child.get("transform", {}))
            block = render_element(child, slide_w, slide_h, assets_dir, img_n)
            if block:
                parts.append(block)
        return "\n".join(parts) or None

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

    if "line"  in el: return _render_line(el, l, t, w, h)
    if "shape" in el: return _render_shape(el, l, t, w, h)
    if "table" in el: return _render_table(el, l, t, w, h)
    return None
