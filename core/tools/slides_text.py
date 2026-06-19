#!/mnt/workspace/.venv/bin/python3
# slides_text.py — Text extraction + HTML rendering for Google Slides elements

import html as _html, re

_SOFT_BREAK = "\x0b"
_TAGS = re.compile(r"<[^>]+>")


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
    """Concatenate textRun HTML with spaces injected at word-adjacent run boundaries."""
    out, prev_raw = "", ""
    for run in runs:
        raw = _clean(run.get("content", ""))
        rh  = _run_html(run)
        if not rh:
            continue
        pr = prev_raw.rstrip("\n")
        if pr and raw and pr[-1].isalnum() and raw[0].isalnum():
            out += " "
        out += rh
        prev_raw = raw
    return out


def text_html(text_obj: dict, is_title: bool = False) -> str:
    """Render a Slides text object as HTML preserving bullets, paragraphs, styles."""
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


def has_content(html_str: str) -> bool:
    return bool(_TAGS.sub("", html_str).strip())
