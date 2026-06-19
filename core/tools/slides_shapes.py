#!/mnt/workspace/.venv/bin/python3
# slides_shapes.py — Element rendering (shapes, lines, tables, images, groups) for slides_port

import pathlib, urllib.request, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slides_text import text_html, has_content

# Approximate theme color map (Simple Light theme defaults)
_THEME = {
    "DARK1": (0,0,0), "DARK2": (32,18,77), "TEXT1": (0,0,0), "TEXT2": (32,18,77),
    "LIGHT1": (255,255,255), "LIGHT2": (232,232,232),
    "BACKGROUND1": (255,255,255), "BACKGROUND2": (232,232,232),
    "ACCENT1": (103,78,167), "ACCENT2": (213,166,189), "ACCENT3": (100,180,100),
    "ACCENT4": (200,150,50), "ACCENT5": (50,150,200), "ACCENT6": (200,100,50),
}


def _fill_color(solid_fill: dict) -> str | None:
    color = solid_fill.get("color", {})
    rgb   = color.get("rgbColor", {})
    if rgb:
        r, g, b = (round(rgb.get(k, 0) * 255) for k in ("red", "green", "blue"))
        a = solid_fill.get("alpha", 1.0)
        return f"rgba({r},{g},{b},{a:.2f})" if a < 1 else f"rgb({r},{g},{b})"
    tc = color.get("themeColor", "")
    return f"rgb{_THEME[tc]}" if tc in _THEME else None


def _bounds(el: dict, slide_w: float, slide_h: float) -> tuple[float, float, float, float]:
    t  = el.get("transform", {})
    s  = el.get("size", {})
    sx = t.get("scaleX", 1.0);  sy = t.get("scaleY", 1.0)
    return (
        round(t.get("translateX", 0)                          / slide_w * 100, 2),
        round(t.get("translateY", 0)                          / slide_h * 100, 2),
        round(s.get("width",  {}).get("magnitude", 0) * sx   / slide_w * 100, 2),
        round(s.get("height", {}).get("magnitude", 0) * sy   / slide_h * 100, 2),
    )


def _download(url: str, dest_base: pathlib.Path) -> pathlib.Path | None:
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            ct  = r.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
            ext = {"image/jpeg":"jpg","image/png":"png","image/gif":"gif","image/webp":"webp"}.get(ct,"jpg")
            dest = dest_base.with_suffix(f".{ext}")
            dest.write_bytes(r.read())
            return dest
    except Exception:
        return None


def _render_shape(el: dict, l: float, t: float, w: float, h: float) -> str | None:
    shape = el["shape"]
    sp    = shape.get("shapeProperties", {})
    css: list[str] = []

    solid = sp.get("shapeBackgroundFill", {}).get("solidFill", {})
    fc = _fill_color(solid)
    if fc:
        css.append(f"background:{fc}")

    outline = sp.get("outline", {})
    if outline.get("propertyState") != "NOT_RENDERED":
        sc  = _fill_color(outline.get("outlineFill", {}).get("solidFill", {}))
        wt  = outline.get("weight", {}).get("magnitude", 0)
        if sc and wt:
            css.append(f"border:{round(wt/12700,1)}pt solid {sc}")

    stype = shape.get("shapeType", "")
    if stype == "ELLIPSE":
        css.append("border-radius:50%")
    elif "ROUND" in stype:
        css.append("border-radius:6px")

    ph_type  = shape.get("placeholder", {}).get("type", "")
    is_title = ph_type in {"TITLE", "CENTERED_TITLE"}
    inner    = text_html(shape.get("text", {}), is_title=is_title)

    if not has_content(inner) and not css:
        return None

    style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%" + (";" + ";".join(css) if css else "")
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
    tbl = el.get("table", {})
    rows = []
    for row in tbl.get("tableRows", []):
        cells = "".join(f"<td>{text_html(c.get('text',{}))}</td>"
                        for c in row.get("tableCells", []))
        rows.append(f"<tr>{cells}</tr>")
    style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%;overflow:auto"
    return f'<div class="absolute" style="{style}"><table>{"".join(rows)}</table></div>'


def render_element(el: dict, slide_w: float, slide_h: float,
                   assets_dir: pathlib.Path | None, img_n: list[int]) -> str | None:
    """Render any page element to HTML. Returns None if element has no visual output."""
    if "elementGroup" in el:
        pt = el.get("transform", {})
        parts = []
        for child in el["elementGroup"].get("children", []):
            ct = child.get("transform", {})
            # Compose parent+child transforms (scale+translate only; shear ignored)
            child = dict(child)
            child["transform"] = {
                "scaleX":     pt.get("scaleX", 1.0) * ct.get("scaleX", 1.0),
                "scaleY":     pt.get("scaleY", 1.0) * ct.get("scaleY", 1.0),
                "shearX":     ct.get("shearX", 0),
                "shearY":     ct.get("shearY", 0),
                "translateX": pt.get("translateX", 0) + pt.get("scaleX", 1.0) * ct.get("translateX", 0),
                "translateY": pt.get("translateY", 0) + pt.get("scaleY", 1.0) * ct.get("translateY", 0),
                "unit": "EMU",
            }
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
        if assets_dir:
            saved = _download(url, assets_dir / f"img_{img_n[0]:03d}")
            ref   = f"./assets/{saved.name}" if saved else url
        else:
            ref = url
        style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%"
        return f'<img src="{ref}" class="absolute object-contain" style="{style}" />'

    if "line" in el:
        return _render_line(el, l, t, w, h)

    if "shape" in el:
        return _render_shape(el, l, t, w, h)

    if "table" in el:
        return _render_table(el, l, t, w, h)

    return None  # video, sheetsChart, etc. — not portable
