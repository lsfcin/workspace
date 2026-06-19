#!/mnt/workspace/.venv/bin/python3
# slides_port.py — Convert Google Slides API JSON to Slidev markdown


def _extract_text(text_obj: dict) -> list[str]:
    """Extract paragraph lines from a Slides text object. Detects bullet list items."""
    lines = []
    current: list[str] = []
    is_bullet = False
    for el in text_obj.get("textElements", []):
        if "paragraphMarker" in el:
            if current:
                line = "".join(current).rstrip()
                if line:
                    lines.append(f"- {line}" if is_bullet else line)
                current = []
            is_bullet = "bullet" in el["paragraphMarker"]
        elif "textRun" in el:
            content = el["textRun"].get("content", "").replace("\n", "")
            if content and current:
                prev = "".join(current)
                if prev and prev[-1].isalnum() and content[0].isalnum():
                    content = " " + content
            current.append(content)
    if current:
        line = "".join(current).rstrip()
        if line:
            lines.append(f"- {line}" if is_bullet else line)
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
