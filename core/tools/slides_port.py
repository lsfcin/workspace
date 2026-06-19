#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown (position-aware, full styling)

import html as _html, pathlib, re, urllib.request

_TAGS = re.compile(r"<[^>]+>")

_SOFT_BREAK = "\x0b"  # Google Slides Shift+Enter (vertical tab)


def _clean(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n").replace(_SOFT_BREAK, "\n")


def _run_html(run: dict) -> str:
    """Render a textRun as styled HTML (color, size, bold, italic)."""
    text = _clean(run.get("content", "")).rstrip("\n")
    if not text:
        return ""
    st  = run.get("style", {})
    css: list[str] = []

    fg = st.get("foregroundColor", {}).get("opaqueColor", {}).get("rgbColor", {})
    if fg:
        r, g, b = (round(fg.get(k, 0) * 255) for k in ("red", "green", "blue"))
        if (r, g, b) != (0, 0, 0):
            css.append(f"color:rgb({r},{g},{b})")

    mag = st.get("fontSize", {}).get("magnitude")
    if mag:
        css.append(f"font-size:{mag}pt")

    text = _html.escape(text).replace("\n", "<br>")
    if css:
        text = f'<span style="{";".join(css)}">{text}</span>'
    if st.get("bold"):
        text = f"<strong>{text}</strong>"
    if st.get("italic"):
        text = f"<em>{text}</em>"
    return text


def _join_runs(runs: list[dict]) -> str:
    """Concatenate textRun HTML, injecting spaces at word-adjacent run boundaries."""
    out, prev_raw = "", ""
    for run in runs:
        raw = _clean(run.get("content", ""))
        rh  = _run_html(run)
        if not rh:
            continue
        if prev_raw and raw:
            pr = prev_raw.rstrip("\n")
            if pr and pr[-1].isalnum() and raw[0].isalnum():
                out += " "
        out += rh
        prev_raw = raw
    return out


def _text_html(text_obj: dict, is_title: bool = False) -> str:
    """Render a Slides text object as HTML preserving bullets, paragraphs, and styles."""
    parts: list[str] = []
    runs:  list[dict] = []
    is_bullet = False
    in_list   = False

    def _flush():
        nonlocal in_list
        content = _join_runs(runs).strip()
        runs.clear()
        if not content:
            return
        if is_title:
            parts.append(f"<h1>{content}</h1>")
        elif is_bullet:
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{content}</li>")
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p>{content}</p>")

    for el in text_obj.get("textElements", []):
        if "paragraphMarker" in el:
            _flush()
            is_bullet = "bullet" in el["paragraphMarker"]
        elif "textRun" in el:
            runs.append(el["textRun"])

    _flush()
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def _bounds(el: dict, slide_w: float, slide_h: float) -> tuple[float, float, float, float]:
    """Return (left%, top%, width%, height%) from element transform+size."""
    t  = el.get("transform", {})
    s  = el.get("size", {})
    sx = t.get("scaleX", 1.0)
    sy = t.get("scaleY", 1.0)
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
            ext = {"image/jpeg": "jpg", "image/png": "png",
                   "image/gif": "gif", "image/webp": "webp"}.get(ct, "jpg")
            dest = dest_base.with_suffix(f".{ext}")
            dest.write_bytes(r.read())
            return dest
    except Exception:
        return None


def _convert_slide(slide: dict, slide_w: float, slide_h: float,
                   assets_dir: pathlib.Path | None, img_n: list[int]) -> str:
    blocks: list[str] = []

    for el in slide.get("pageElements", []):
        l, t, w, h = _bounds(el, slide_w, slide_h)
        style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%"

        if "image" in el:
            url = el["image"].get("contentUrl", "")
            if not url:
                continue
            img_n[0] += 1
            if assets_dir:
                saved = _download(url, assets_dir / f"img_{img_n[0]:03d}")
                ref   = f"./assets/{saved.name}" if saved else url
            else:
                ref = url
            blocks.append(
                f'<img src="{ref}" class="absolute object-contain" style="{style}" />'
            )

        elif "shape" in el:
            ph_type  = el["shape"].get("placeholder", {}).get("type", "")
            is_title = ph_type in {"TITLE", "CENTERED_TITLE"}
            inner    = _text_html(el["shape"].get("text", {}), is_title=is_title)
            # skip empty or whitespace-only placeholders (e.g. slide number boxes)
            if not inner or not _TAGS.sub("", inner).strip():
                continue
            blocks.append(
                f'<div class="absolute overflow-hidden" style="{style}">{inner}</div>'
            )

    return "\n".join(blocks)


def convert(presentation: dict, assets_dir: pathlib.Path | None = None) -> str:
    """Convert Google Slides presentation JSON to Slidev markdown."""
    title   = presentation.get("title", "Untitled")
    ps      = presentation.get("pageSize", {})
    slide_w = ps.get("width",  {}).get("magnitude", 9144000)
    slide_h = ps.get("height", {}).get("magnitude", 5143500)

    if assets_dir:
        assets_dir.mkdir(parents=True, exist_ok=True)

    img_n:  list[int] = [0]
    bodies: list[str] = []

    for slide in presentation.get("slides", []):
        body = _convert_slide(slide, slide_w, slide_h, assets_dir, img_n)

        notes_page = slide.get("slideProperties", {}).get("notesPage", {})
        for nel in notes_page.get("pageElements", []):
            ns = nel.get("shape", {})
            if ns.get("placeholder", {}).get("type") == "BODY":
                nl = _text_html(ns.get("text", {}))
                if nl:
                    body += f"\n\n::notes::\n{nl}"
                break

        bodies.append(body)

    header = f'---\ntheme: default\ntitle: "{title}"\nlayout: none\n---\n\n'
    return header + "\n\n---\n\n".join(bodies)
