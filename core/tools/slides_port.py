#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown

import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slides_text import text_html
from slides_shapes import render_element

# Placeholder types overridden by slides — skip from master rendering
_SKIP_MASTER_PH = {"TITLE", "CENTERED_TITLE", "BODY", "SUBTITLE",
                   "SLIDE_NUMBER", "DATE_AND_TIME", "FOOTER"}


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
                   master_els: list[dict]) -> str:
    blocks: list[str] = []
    # Master elements first (background layer)
    for el in master_els:
        b = render_element(el, slide_w, slide_h, assets_dir, img_n)
        if b:
            blocks.append(b)
    # Slide elements (foreground)
    for el in slide.get("pageElements", []):
        b = render_element(el, slide_w, slide_h, assets_dir, img_n)
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

    master_els = _master_elements(presentation)
    img_n: list[int] = [0]
    bodies: list[str] = []

    for slide in presentation.get("slides", []):
        bodies.append(
            _convert_slide(slide, slide_w, slide_h, assets_dir, img_n, master_els)
        )

    header = f'---\ntheme: default\ntitle: "{title}"\nlayout: none\n---\n\n'
    return header + "\n\n---\n\n".join(bodies)
