# sheets_a1.py — a sheet's cells addressed as people write them: A1 ranges ↔ GridRange, TSV ↔ values, hex ↔ colour
import csv
import io
import re

# A1 is what a person reads off the screen; the batchUpdate API takes none of it. Every request it
# accepts wants a GridRange — a numeric sheetId and 0-based, end-exclusive indices — so the
# translation lives here once, tested, instead of being redone by hand in every requests.json.
_CELL = re.compile(r"^([A-Za-z]*)(\d*)$")


def col_index(letters: str) -> int:
    """'A' → 0, 'Z' → 25, 'AA' → 26."""
    n = 0
    for ch in letters.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def col_letters(index: int) -> str:
    """0 → 'A', 26 → 'AA' — the inverse of col_index."""
    out = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        out = chr(65 + rem) + out
    return out


def split_a1(a1: str) -> tuple[str | None, str]:
    """"'Aba 1'!B2:C3" → ('Aba 1', 'B2:C3'); "B2:C3" → (None, 'B2:C3'); "Notas" → ('Notas', '')."""
    if "!" in a1:
        sheet, cells = a1.rsplit("!", 1)
        if sheet.startswith("'") and sheet.endswith("'"):
            sheet = sheet[1:-1].replace("''", "'")
        return sheet, cells
    if a1 and all(_CELL.match(part) and part for part in a1.split(":")):
        return None, a1
    return a1, ""


def quote(title: str) -> str:
    """A tab title as A1 wants it: quoted when it is not a bare word."""
    return title if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", title) else "'" + title.replace("'", "''") + "'"


def grid_range(a1: str, sheets: dict[str, int], default: str) -> dict:
    """An A1 range → GridRange. `sheets` maps title → sheetId; `default` is the first tab's title.

    Open sides stay open (`A:A` has no row bound, `2:4` no column bound), exactly as the API reads
    an absent index: the whole extent, including rows added later.
    """
    # "Notas" is also a valid column span (NOTAS:NOTAS); a tab of that name wins, as in the UI.
    sheet, cells = (a1, "") if a1 in sheets else split_a1(a1)
    title = sheet if sheet is not None else default
    if title not in sheets:
        raise ValueError(f"no tab named {title!r}; the tabs are: {', '.join(sheets)}")
    out: dict = {"sheetId": sheets[title]}
    if not cells:
        return out
    start, _, end = cells.partition(":")
    end = end or start
    m1, m2 = _CELL.match(start), _CELL.match(end)
    if not (m1 and m2 and start and end):
        raise ValueError(f"not an A1 range: {a1!r}")
    (c1, r1), (c2, r2) = m1.groups(), m2.groups()
    if r1:
        out["startRowIndex"] = int(r1) - 1
    if r2:
        out["endRowIndex"] = int(r2)
    if c1:
        out["startColumnIndex"] = col_index(c1)
    if c2:
        out["endColumnIndex"] = col_index(c2) + 1
    return out


def read_tsv(text: str) -> list[list[str]]:
    """TSV → rows of strings. Cells go as typed: the API parses numbers, dates and `=formulas`."""
    return list(csv.reader(io.StringIO(text), delimiter="\t"))


def write_tsv(rows: list[list]) -> str:
    buf = io.StringIO()
    csv.writer(buf, delimiter="\t", lineterminator="\n").writerows(rows)
    return buf.getvalue()


def grid(rows: list[list], top: int = 1, left: int = 0) -> str:
    """Values as navigable text: a header of column letters, every row led by its number,
    so any cell read here is addressed by what is printed next to it."""
    if not rows:
        return "  (vazio)\n"
    width = max(len(r) for r in rows)
    head = [""] + [col_letters(left + i) for i in range(width)]
    body = [[str(top + n)] + list(r) for n, r in enumerate(rows)]
    return write_tsv([head, *body])


def color(hex_code: str) -> dict:
    """'#1a73e8', '1a73e8' or '#fff' → the API's 0–1 floats."""
    h = hex_code.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"not a hex colour: {hex_code!r}")
    return {k: int(h[i:i + 2], 16) / 255 for k, i in (("red", 0), ("green", 2), ("blue", 4))}
