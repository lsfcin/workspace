#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown

import pathlib, urllib.request

_SOFT_BREAK = "\x0b"  # Google Slides Shift+Enter (vertical tab)


def _clean(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n").replace(_SOFT_BREAK, "\n")


def _extract_text(text_obj: dict) -> list[str]:
    """Extract lines from a Slides text object. Handles bullets and soft breaks."""
    lines: list[str] = []
    current: list[str] = []
    is_bullet = False

    def _flush():
        if not current:
            return
        for sub in "".join(current).rstrip().split("\n"):
            sub = sub.rstrip()
            if sub:
                lines.append(f"- {sub}" if is_bullet else sub)
        current.clear()

    for el in text_obj.get("textElements", []):
        if "paragraphMarker" in el:
            _flush()
            is_bullet = "bullet" in el["paragraphMarker"]
        elif "textRun" in el:
            c = _clean(el["textRun"].get("content", ""))
            if c and current:
                prev = "".join(current)
                if prev and prev[-1].isalnum() and c[0].isalnum():
                    c = " " + c
            current.append(c)
    _flush()
    return lines


def _bounds(el: dict, slide_w: float, slide_h: float) -> tuple[float, float, float, float]:
    """Return (left%, top%, width%, height%) from element transform+size."""
    t = el.get("transform", {})
    s = el.get("size", {})
    x  = t.get("translateX", 0)
    y  = t.get("translateY", 0)
    sx = t.get("scaleX", 1.0)
    sy = t.get("scaleY", 1.0)
    w  = s.get("width",  {}).get("magnitude", 0) * sx
    h  = s.get("height", {}).get("magnitude", 0) * sy
    return (
        round(x / slide_w * 100, 2),
        round(y / slide_h * 100, 2),
        round(w / slide_w * 100, 2),
        round(h / slide_h * 100, 2),
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
            lines = _extract_text(el["shape"].get("text", {}))
            if not lines:
                continue
            ph_type  = el["shape"].get("placeholder", {}).get("type", "")
            is_title = ph_type in {"TITLE", "CENTERED_TITLE"}
            content  = "\n".join(f"# {ln}" if is_title else ln for ln in lines)
            blocks.append(
                f'<div class="absolute overflow-hidden" style="{style}">\n\n{content}\n\n</div>'
            )

    return "\n\n".join(blocks)


def convert(presentation: dict, assets_dir: pathlib.Path | None = None) -> str:
    """Convert Google Slides presentation JSON to Slidev markdown."""
    title  = presentation.get("title", "Untitled")
    ps     = presentation.get("pageSize", {})
    slide_w = ps.get("width",  {}).get("magnitude", 9144000)
    slide_h = ps.get("height", {}).get("magnitude", 5143500)

    if assets_dir:
        assets_dir.mkdir(parents=True, exist_ok=True)

    img_n: list[int] = [0]
    slide_bodies: list[str] = []

    for slide in presentation.get("slides", []):
        body = _convert_slide(slide, slide_w, slide_h, assets_dir, img_n)
        notes_page = slide.get("slideProperties", {}).get("notesPage", {})
        for nel in notes_page.get("pageElements", []):
            ns = nel.get("shape", {})
            if ns.get("placeholder", {}).get("type") == "BODY":
                nl = _extract_text(ns.get("text", {}))
                if nl:
                    body += "\n\n::notes::\n" + "\n".join(nl)
                break
        slide_bodies.append(body)

    header = f'---\ntheme: default\ntitle: "{title}"\nlayout: none\n---\n\n'
    return header + "\n\n---\n\n".join(slide_bodies)
