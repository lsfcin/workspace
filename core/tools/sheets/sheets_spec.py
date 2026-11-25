# sheets_spec.py — a sheet's look written as JSON: a format spec (style, borders, sizes, conditional rules, validation) → Sheets API batchUpdate requests
from sheets_a1 import color, grid_range

# One vocabulary for both places a condition appears — a conditional format and a validation rule —
# because the API itself uses one BooleanCondition for both, and two spellings would drift.
_OPS = {
    "<": "NUMBER_LESS", "<=": "NUMBER_LESS_THAN_EQ", ">": "NUMBER_GREATER",
    ">=": "NUMBER_GREATER_THAN_EQ", "=": "NUMBER_EQ", "!=": "NUMBER_NOT_EQ",
    "between": "NUMBER_BETWEEN", "not-between": "NUMBER_NOT_BETWEEN",
    "contains": "TEXT_CONTAINS", "not-contains": "TEXT_NOT_CONTAINS",
    "starts": "TEXT_STARTS_WITH", "ends": "TEXT_ENDS_WITH", "is": "TEXT_EQ",
    "empty": "BLANK", "not-empty": "NOT_BLANK",
    "before": "DATE_BEFORE", "after": "DATE_AFTER", "date": "DATE_IS_VALID",
    "list": "ONE_OF_LIST", "range": "ONE_OF_RANGE", "checkbox": "BOOLEAN",
}
_ALIGN = {"left": "LEFT", "center": "CENTER", "right": "RIGHT"}
_VALIGN = {"top": "TOP", "middle": "MIDDLE", "bottom": "BOTTOM"}
_WRAP = {"wrap": "WRAP", "clip": "CLIP", "overflow": "OVERFLOW_CELL"}
_BORDER = {"solid": "SOLID", "solid-medium": "SOLID_MEDIUM", "solid-thick": "SOLID_THICK",
           "dashed": "DASHED", "dotted": "DOTTED", "double": "DOUBLE", "none": "NONE"}
_SIDES = {"top": ["top"], "bottom": ["bottom"], "left": ["left"], "right": ["right"],
          "inner-h": ["innerHorizontal"], "inner-v": ["innerVertical"],
          "outer": ["top", "bottom", "left", "right"],
          "inner": ["innerHorizontal", "innerVertical"],
          "all": ["top", "bottom", "left", "right", "innerHorizontal", "innerVertical"]}
_TEXT = {"bold": "bold", "italic": "italic", "underline": "underline", "strike": "strikethrough"}
KEYS = {"range", "font", "size", "color", "bg", "align", "valign", "wrap", "number", "rotate",
        "borders", "merge", "height", "width", "freeze", "when", "gradient", "validate", "help",
        "strict", *_TEXT}


def condition(spec) -> dict:
    """`"=$B2<5"` → a custom formula; `[op, *values]` → that operator over those values.

    `range` takes an A1 range as its value (the list of allowed answers lives in the sheet).
    """
    if isinstance(spec, str):
        if not spec.startswith("="):
            raise ValueError(f"a condition string must be a formula starting with '=': {spec!r}")
        return {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": spec}]}
    op, *values = spec
    if op not in _OPS:
        raise ValueError(f"unknown condition {op!r}; known: {', '.join(_OPS)} or a '=formula'")
    if op == "range":
        values = [v if str(v).startswith("=") else f"={v}" for v in values]
    out: dict = {"type": _OPS[op]}
    if values:
        out["values"] = [{"userEnteredValue": str(v)} for v in values]
    return out


def _cell_format(entry: dict) -> dict:
    """The userEnteredFormat an entry's style keys ask for."""
    out: dict = {}
    text: dict = {}
    if "font" in entry:
        text["fontFamily"] = entry["font"]
    if "size" in entry:
        text["fontSize"] = entry["size"]
    if "color" in entry:
        text["foregroundColor"] = color(entry["color"])
    for key, api in _TEXT.items():
        if key in entry:
            text[api] = bool(entry[key])
    if text:
        out["textFormat"] = text
    if "bg" in entry:
        out["backgroundColor"] = color(entry["bg"])
    if "align" in entry:
        out["horizontalAlignment"] = _ALIGN[entry["align"]]
    if "valign" in entry:
        out["verticalAlignment"] = _VALIGN[entry["valign"]]
    if "wrap" in entry:
        out["wrapStrategy"] = _WRAP[entry["wrap"]]
    if "rotate" in entry:
        out["textRotation"] = {"angle": entry["rotate"]}
    if "number" in entry:
        num = entry["number"]
        out["numberFormat"] = num if isinstance(num, dict) else {"type": "NUMBER", "pattern": num}
    return out


def _mask(fmt: dict) -> str:
    """The `fields` mask: only what the entry sets, so every other property of the cell survives."""
    parts = []
    for key, value in fmt.items():
        if key == "textFormat":
            parts += [f"userEnteredFormat.textFormat.{k}" for k in value]
        else:
            parts.append(f"userEnteredFormat.{key}")
    return ",".join(parts)


def _borders(rng: dict, borders: dict) -> dict:
    """{"outer": "solid-thick", "inner": "dotted", "color": "#000"} → one updateBorders."""
    border_color = color(borders.get("color", "#000000"))
    out: dict = {"range": rng}
    for side, style in borders.items():
        if side == "color":
            continue
        if side not in _SIDES:
            raise ValueError(f"unknown border side {side!r}; known: {', '.join(_SIDES)}")
        for api in _SIDES[side]:
            out[api] = {"style": _BORDER[style], "color": border_color}
    return {"updateBorders": out}


def _dimensions(rng: dict, entry: dict) -> list:
    out = []
    for key, dim, lo, hi in (("height", "ROWS", "startRowIndex", "endRowIndex"),
                             ("width", "COLUMNS", "startColumnIndex", "endColumnIndex")):
        if key in entry:
            span = {"sheetId": rng["sheetId"], "dimension": dim}
            if lo in rng:
                span["startIndex"] = rng[lo]
            if hi in rng:
                span["endIndex"] = rng[hi]
            out.append({"updateDimensionProperties": {
                "range": span, "properties": {"pixelSize": entry[key]}, "fields": "pixelSize"}})
    return out


def _conditional(rng: dict, entry: dict) -> dict:
    if "gradient" in entry:
        stops = entry["gradient"]
        names = ["minpoint", "midpoint", "maxpoint"] if len(stops) == 3 else ["minpoint", "maxpoint"]
        kinds = ["MIN", "PERCENTILE", "MAX"] if len(stops) == 3 else ["MIN", "MAX"]
        points = [{"type": k, "color": color(c), **({"value": "50"} if k == "PERCENTILE" else {})}
                  for k, c in zip(kinds, stops)]
        rule = {"ranges": [rng], "gradientRule": dict(zip(names, points))}
    else:
        fmt = _cell_format({k: v for k, v in entry.items() if k in ("bg", "color", *_TEXT)})
        rule = {"ranges": [rng], "booleanRule": {"condition": condition(entry["when"]), "format": fmt}}
    return {"addConditionalFormatRule": {"rule": rule, "index": 0}}


def _validation(rng: dict, entry: dict) -> dict:
    rule: dict = {"condition": condition(entry["validate"]), "strict": entry.get("strict", True),
                  "showCustomUi": True}
    if "help" in entry:
        rule["inputMessage"] = entry["help"]
    return {"setDataValidation": {"range": rng, "rule": rule}}


def requests(spec: list[dict], sheets: dict[str, int], default: str) -> list:
    """A format spec → batchUpdate requests, in spec order.

    One entry is one range plus what to do to it. An entry with `when` or `gradient` is a
    conditional rule, and its colours apply only where the rule holds; without them the same keys
    format the cells outright. `freeze` acts on the tab its range names.
    """
    out = []
    for entry in spec:
        unknown = set(entry) - KEYS
        if unknown:
            raise ValueError(f"unknown key(s) {sorted(unknown)} in entry for {entry.get('range')!r}")
        rng = grid_range(entry["range"], sheets, default)
        if "when" in entry or "gradient" in entry:
            out.append(_conditional(rng, entry))
        elif fmt := _cell_format(entry):
            out.append({"repeatCell": {"range": rng, "cell": {"userEnteredFormat": fmt},
                                       "fields": _mask(fmt)}})
        if "borders" in entry:
            out.append(_borders(rng, entry["borders"]))
        if entry.get("merge"):
            kind = {"rows": "MERGE_ROWS", "cols": "MERGE_COLUMNS"}.get(entry["merge"], "MERGE_ALL")
            out.append({"mergeCells": {"range": rng, "mergeType": kind}})
        out += _dimensions(rng, entry)
        if "freeze" in entry:
            frozen = {"frozenRowCount": entry["freeze"].get("rows", 0),
                      "frozenColumnCount": entry["freeze"].get("cols", 0)}
            out.append({"updateSheetProperties": {
                "properties": {"sheetId": rng["sheetId"], "gridProperties": frozen},
                "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
        if "validate" in entry:
            out.append(_validation(rng, entry))
    return out
