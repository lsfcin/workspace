#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown

_SOFT_BREAK = ""  # Google Slides Shift+Enter within a paragraph


def _clean(s: str) -> str:
    """Normalize line endings; replace soft breaks with \n for later splitting."""
    return s.replace("\r\n", "\n").replace("\r", "\n").replace(_SOFT_BREAK, "\n")


def _extract_text(text_obj: dict) -> list[str]:
    """Extract lines from a Slides text object. Handles bullets and soft line breaks."""
    lines = []
    current: list[str] = []
    is_bullet = False

    def _flush():
        if not current:
            return
        joined = "".join(current).rstrip()
        for subline in joined.split("\n"):
            subline = subline.rstrip()
            if subline:
                lines.append(f"- {subline}" if is_bullet else subline)
        current.clear()

    for el in text_obj.get("textElements", []):
        if "paragraphMarker" in el:
            _flush()
            is_bullet = "bullet" in el["paragraphMarker"]
        elif "textRun" in el:
            content = _clean(el["textRun"].get("content", ""))
            if content and current:
                prev = "".join(current)
                if prev and prev[-1].isalnum() and content[0].isalnum():
                    content = " " + content
            current.append(content)

    _flush()
    return lines


def _extract_notes(slide: dict) -> str:
    notes_page = slide.get("slideProperties", {}).get("notesPage", {})
    for el in notes_page.get("pageElements", []):
        shape = el.get("shape", {})
        if shape.get("placeholder", {}).get("type") == "BODY":
            lines = _extract_text(shape.get("text", {}))
            return "\n".join(lines)
    return ""


_TITLE_TYPES = {"TITLE", "CENTERED_TITLE"}
_BODY_TYPES = {"BODY", "SUBTITLE"}


def convert(presentation: dict) -> str:
    """Convert Google Slides presentation JSON to Slidev markdown."""
    title = presentation.get("title", "Untitled")
    out: list[str] = [f"---\ntheme: default\ntitle: \"{title}\"\n---\n"]

    for i, slide in enumerate(presentation.get("slides", [])):
        if i > 0:
            out.append("---\n")

        title_lines: list[str] = []
        body_parts: list[list[str]] = []

        for el in slide.get("pageElements", []):
            shape = el.get("shape", {})
            ph_type = shape.get("placeholder", {}).get("type", "")
            text = shape.get("text", {})
            lines = _extract_text(text)
            if not lines:
                continue
            if ph_type in _TITLE_TYPES:
                title_lines = lines
            elif ph_type in _BODY_TYPES or ph_type == "":
                body_parts.append(lines)

        if title_lines:
            out.append(f"# {' '.join(title_lines)}\n")
        for part in body_parts:
            out.extend(part)
            out.append("")

        notes = _extract_notes(slide)
        if notes:
            out.append(f"\n::notes::\n{notes}\n")

    return "\n".join(out)
