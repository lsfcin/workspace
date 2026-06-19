#!/mnt/workspace/.venv/bin/python3
# slides_text.py — Text extraction + HTML rendering for Google Slides elements

import html as _html, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slides_style import _rgb

_SOFT_BREAK = "\x0b"
_TAGS = re.compile(r"<[^>]+>")


def _clean(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n").replace(_SOFT_BREAK, "\n")


def _run_html(run: dict) -> str:
    """Render a textRun as styled HTML."""
    text = _clean(run.get("content", "")).rstrip("\n")
    if not text:
        return ""
    st  = run.get("style", {})
    css: list[str] = []

    fg = _rgb(st.get("foregroundColor", {}).get("opaqueColor", {}))
    if fg and fg != "rgb(0,0,0)":
        css.append(f"color:{fg}")

    ff = st.get("weightedFontFamily", {}).get("fontFamily", "")
    if ff:
        css.append(f"font-family:'{ff}'")

    mag = st.get("fontSize", {}).get("magnitude")
    if mag:
        css.append(f"font-size:{mag}pt")

    ls = st.get("letterSpacing", {})
    if isinstance(ls, dict) and ls.get("magnitude"):
        lsm = ls["magnitude"] / (12700 if ls.get("unit", "EMU") != "PT" else 1)
        css.append(f"letter-spacing:{lsm:.2f}pt")

    text = _html.escape(text).replace("\n", "<br>")
    if css:
        text = f'<span style="{";".join(css)}">{text}</span>'
    if st.get("bold"):          text = f"<strong>{text}</strong>"
    if st.get("italic"):        text = f"<em>{text}</em>"
    if st.get("underline"):     text = f"<u>{text}</u>"
    if st.get("strikethrough"): text = f"<s>{text}</s>"
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


_ALIGN = {"CENTER": "center", "END": "right", "JUSTIFIED": "justify"}


def text_html(text_obj: dict, is_title: bool = False) -> str:
    """Render a Slides text object as HTML preserving bullets, paragraphs, styles."""
    parts: list[str] = []
    runs:  list[dict] = []
    is_bullet = False
    nesting   = 0
    para_css: list[str] = []
    in_list   = False

    def _flush():
        nonlocal in_list
        content = _join_runs(runs).strip()
        runs.clear()
        if not content:
            return
        ps = f' style="{";".join(para_css)}"' if para_css else ""
        if is_title:
            parts.append(f"<h1{ps}>{content}</h1>")
        elif is_bullet:
            if not in_list:
                parts.append("<ul>")
                in_list = True
            ni    = f"margin-left:{nesting * 1.5}em" if nesting else ""
            li_s  = ";".join(filter(None, [ni] + para_css))
            parts.append(f'<li{f" style=\"{li_s}\"" if li_s else ""}>{content}</li>')
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p{ps}>{content}</p>")

    for el in text_obj.get("textElements", []):
        if "paragraphMarker" in el:
            _flush()
            pm        = el["paragraphMarker"]
            is_bullet = "bullet" in pm
            nesting   = pm.get("bullet", {}).get("nestingLevel", 0) if is_bullet else 0
            ps        = pm.get("style", {})
            para_css  = []
            al = _ALIGN.get(ps.get("alignment", ""))
            if al:
                para_css.append(f"text-align:{al}")
            lsp = ps.get("lineSpacing")
            if lsp:
                para_css.append(f"line-height:{lsp/100:.2f}")
        elif "textRun" in el:
            runs.append(el["textRun"])

    _flush()
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def has_content(html_str: str) -> bool:
    return bool(_TAGS.sub("", html_str).strip())
