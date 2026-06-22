#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown

import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slides_text import text_html
from slides_shapes import render_element
from slides_style import _rgb, set_theme_colors

# Placeholder types that slides override — skip these from master rendering
_SKIP_MASTER_PH = {"TITLE", "CENTERED_TITLE", "BODY", "SUBTITLE",
                   "SLIDE_NUMBER", "DATE_AND_TIME"}


def _ph_sizes_from_els(elements: list) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for el in elements:
        ph = el.get("shape", {}).get("placeholder", {}).get("type", "")
        if not ph:
            continue
        for te in el.get("shape", {}).get("text", {}).get("textElements", []):
            if "textRun" in te:
                mag = (te["textRun"].get("style", {}).get("fontSize") or {}).get("magnitude")
                if mag and ph not in sizes:
                    sizes[ph] = int(mag)
    return sizes


def _layout_ph_sizes(presentation: dict) -> dict[str, dict[str, int]]:
    """layout_objectId → {ph_type: font_size_pt}, with master as base."""
    base = _ph_sizes_from_els(
        presentation.get("masters", [{}])[0].get("pageElements", [])
    )
    result: dict[str, dict[str, int]] = {}
    for layout in presentation.get("layouts", []):
        sizes = {**base, **_ph_sizes_from_els(layout.get("pageElements", []))}
        result[layout["objectId"]] = sizes
    return result


def _ph_valign_from_els(elements: list) -> dict[str, str]:
    """ph_type → contentAlignment from a list of page elements."""
    out: dict[str, str] = {}
    for el in elements:
        shape = el.get("shape", {})
        ph = shape.get("placeholder", {}).get("type", "")
        if not ph:
            continue
        ca = shape.get("shapeProperties", {}).get("contentAlignment", "")
        if ca:
            out[ph] = ca
    return out


def _layout_ph_valign(presentation: dict) -> dict[str, dict[str, str]]:
    """layout_objectId → {ph_type: contentAlignment}, with master as base."""
    master_els = presentation.get("masters", [{}])[0].get("pageElements", [])
    base = _ph_valign_from_els(master_els)
    result: dict[str, dict[str, str]] = {}
    for layout in presentation.get("layouts", []):
        valign = {**base, **_ph_valign_from_els(layout.get("pageElements", []))}
        result[layout["objectId"]] = valign
    return result


def _master_ph_styles(presentation: dict) -> tuple[dict[str, int], dict[str, str], dict[str, str]]:
    """Extract (weight, color, family) defaults from master placeholder text runs."""
    master = presentation.get("masters", [{}])[0]
    weights: dict[str, int] = {}
    colors:  dict[str, str] = {}
    families: dict[str, str] = {}
    for el in master.get("pageElements", []):
        shape = el.get("shape", {})
        ph = shape.get("placeholder", {}).get("type", "")
        if not ph:
            continue
        for te in shape.get("text", {}).get("textElements", []):
            if "textRun" not in te:
                continue
            s  = te["textRun"].get("style", {})
            wf = s.get("weightedFontFamily", {})
            if ph not in weights and wf.get("weight"):
                weights[ph] = wf["weight"]
            if ph not in families and wf.get("fontFamily"):
                families[ph] = wf["fontFamily"]
            if ph not in colors:
                fc = s.get("foregroundColor", {})
                c  = _rgb(fc.get("opaqueColor", {})) if fc else None
                if c:
                    colors[ph] = c
    for src, dst in [("TITLE", "CENTERED_TITLE"), ("BODY", "SUBTITLE")]:
        for d in (weights, families, colors):
            if src in d and dst not in d:
                d[dst] = d[src]  # type: ignore[assignment]
    return weights, colors, families


def _master_elements(presentation: dict) -> list[dict]:
    """Return master page elements that appear as background on every slide."""
    master = presentation.get("masters", [{}])[0]
    out = []
    for el in master.get("pageElements", []):
        ph = el.get("shape", {}).get("placeholder", {}).get("type", "")
        if ph not in _SKIP_MASTER_PH:
            out.append(el)
    return out


def _slide_notes(slide: dict) -> str:
    notes_page = slide.get("slideProperties", {}).get("notesPage", {})
    for nel in notes_page.get("pageElements", []):
        ns = nel.get("shape", {})
        if ns.get("placeholder", {}).get("type") == "BODY":
            html = text_html(ns.get("text", {}))
            from slides_text import has_content
            if has_content(html):
                return html
    return ""


def _convert_slide(slide: dict, slide_w: float, slide_h: float,
                   assets_dir: pathlib.Path | None, img_n: list[int],
                   master_els: list[dict], layout_sizes: dict[str, dict[str, int]],
                   layout_valign: dict[str, dict[str, str]],
                   ph_weight: dict[str, int],
                   ph_color: dict[str, str],
                   ph_family: dict[str, str]) -> str:
    layout_id = slide.get("slideProperties", {}).get("layoutObjectId", "")
    ph_sizes  = layout_sizes.get(layout_id, {})
    ph_valign = layout_valign.get(layout_id, {})
    blocks: list[str] = []
    # Master elements first (background layer) — skip ghost filter
    for el in master_els:
        b = render_element(el, slide_w, slide_h, assets_dir, img_n, is_master=True)
        if b:
            blocks.append(b)
    # Slide elements (foreground)
    for el in slide.get("pageElements", []):
        b = render_element(el, slide_w, slide_h, assets_dir, img_n,
                           ph_sizes, ph_valign, ph_weight, ph_color, ph_family)
        if b:
            blocks.append(b)
    inner = "\n".join(blocks)
    # Clip all elements to slide bounds (lines/groups can overflow otherwise)
    body = f'<div style="position:absolute;inset:0;overflow:hidden">\n{inner}\n</div>'
    notes = _slide_notes(slide)
    if notes:
        body += f"\n\n::notes::\n{notes}"
    return body


def convert(presentation: dict, assets_dir: pathlib.Path | None = None) -> str:
    """Convert Google Slides presentation JSON to Slidev markdown."""
    title   = presentation.get("title", "Untitled")
    ps      = presentation.get("pageSize", {})
    slide_w = ps.get("width",  {}).get("magnitude", 9144000)
    slide_h = ps.get("height", {}).get("magnitude", 5143500)

    if assets_dir:
        assets_dir.mkdir(parents=True, exist_ok=True)

    set_theme_colors(
        presentation.get("masters", [{}])[0]
        .get("pageProperties", {}).get("colorScheme", {}).get("colors", [])
    )
    master_els    = _master_elements(presentation)
    layout_sizes  = _layout_ph_sizes(presentation)
    layout_valign = _layout_ph_valign(presentation)
    ph_weight, ph_color, ph_family = _master_ph_styles(presentation)
    img_n: list[int] = [0]
    bodies: list[str] = []

    for slide in presentation.get("slides", []):
        bodies.append(
            _convert_slide(slide, slide_w, slide_h, assets_dir, img_n,
                           master_els, layout_sizes, layout_valign,
                           ph_weight, ph_color, ph_family)
        )

    header = f'---\ntheme: default\ntitle: "{title}"\nlayout: none\nmouseWheel: true\n---\n\n'
    return header + "\n\n---\n\n".join(bodies)
