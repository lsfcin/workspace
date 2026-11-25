# T1 sheets: a cell addressed the way a person reads it must reach the API as that same cell, and a format spec must change only what it names.
import pytest

import sheets_a1
import sheets_spec

TABS = {"Notas": 0, "Aba 2": 7, "O'Neil": 9}


def rng(a1):
    return sheets_a1.grid_range(a1, TABS, "Notas")


@pytest.mark.parametrize("letters,index", [("A", 0), ("Z", 25), ("AA", 26), ("AZ", 51), ("BA", 52)])
def test_a_column_letter_and_its_index_are_one_mapping(letters, index):
    assert sheets_a1.col_index(letters) == index
    assert sheets_a1.col_letters(index) == letters


def test_a_cell_is_zero_based_and_end_exclusive():
    """B2 is row 1, column 1, and exactly one cell wide: the off-by-one every hand-built request gets wrong."""
    assert rng("B2") == {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2,
                         "startColumnIndex": 1, "endColumnIndex": 2}


def test_a_tab_name_with_spaces_or_a_quote_reaches_its_own_sheet_id():
    assert rng("'Aba 2'!A1:C3")["sheetId"] == 7
    assert rng("'O''Neil'!A1")["sheetId"] == 9


def test_an_open_side_stays_open():
    """A:A must cover rows added later, so no row bound may be invented for it."""
    assert rng("A:A") == {"sheetId": 0, "startColumnIndex": 0, "endColumnIndex": 1}
    assert rng("2:4") == {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 4}


def test_a_tab_named_like_a_column_span_is_the_tab():
    """'Notas' is also a valid A1 column span; the tab wins, as it does in the Sheets UI."""
    assert rng("Notas") == {"sheetId": 0}


def test_an_unknown_tab_is_refused_naming_the_real_ones():
    with pytest.raises(ValueError, match="Aba 2"):
        rng("Notass!A1")


def test_a_tsv_round_trip_keeps_formulas_and_empty_cells():
    rows = [["nome", "nota", ""], ["Ana", "=MÉDIA(B2:B9)", "7,5"]]
    assert sheets_a1.read_tsv(sheets_a1.write_tsv(rows)) == rows


def test_the_printed_grid_labels_every_cell_with_its_own_address():
    text = sheets_a1.grid([["a", "b"]], top=5, left=2)
    head, row = text.splitlines()
    assert head.split("\t") == ["", "C", "D"]
    assert row.split("\t") == ["5", "a", "b"]


def test_a_style_entry_masks_only_what_it_sets():
    """Setting bold must not wipe the font size someone chose by hand."""
    [req] = sheets_spec.requests([{"range": "A1:B1", "bold": True, "bg": "#fff"}], TABS, "Notas")
    assert req["repeatCell"]["fields"] == "userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColor"
    assert req["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"] == {"red": 1, "green": 1, "blue": 1}


def test_outer_borders_draw_four_sides_and_no_inner_line():
    [req] = sheets_spec.requests([{"range": "A1:C3", "borders": {"outer": "solid-thick"}}], TABS, "Notas")
    sides = set(req["updateBorders"]) - {"range"}
    assert sides == {"top", "bottom", "left", "right"}
    assert req["updateBorders"]["top"]["style"] == "SOLID_THICK"


def test_a_conditional_entry_colours_only_where_its_rule_holds():
    """With `when`, bg is the rule's format — never a repeatCell that paints the whole range."""
    reqs = sheets_spec.requests([{"range": "B2:B40", "when": ["<", 5], "bg": "#f4cccc"}], TABS, "Notas")
    assert [next(iter(r)) for r in reqs] == ["addConditionalFormatRule"]
    rule = reqs[0]["addConditionalFormatRule"]["rule"]["booleanRule"]
    assert rule["condition"] == {"type": "NUMBER_LESS", "values": [{"userEnteredValue": "5"}]}


def test_a_formula_condition_is_a_custom_formula():
    assert sheets_spec.condition("=$B2<5")["type"] == "CUSTOM_FORMULA"
    with pytest.raises(ValueError):
        sheets_spec.condition("B2<5")


def test_a_validation_list_and_a_range_source():
    [lst] = sheets_spec.requests([{"range": "C2:C40", "validate": ["list", "sim", "não"]}], TABS, "Notas")
    assert lst["setDataValidation"]["rule"]["condition"]["type"] == "ONE_OF_LIST"
    assert lst["setDataValidation"]["rule"]["strict"] is True
    src = sheets_spec.condition(["range", "'Aba 2'!A1:A9"])
    assert src["values"] == [{"userEnteredValue": "='Aba 2'!A1:A9"}]


def test_sizes_and_freeze_act_on_the_named_tab():
    reqs = sheets_spec.requests([{"range": "'Aba 2'!A1:A3", "height": 40, "freeze": {"rows": 1}}], TABS, "Notas")
    dims = reqs[0]["updateDimensionProperties"]["range"]
    assert dims == {"sheetId": 7, "dimension": "ROWS", "startIndex": 0, "endIndex": 3}
    assert reqs[1]["updateSheetProperties"]["properties"]["sheetId"] == 7


def test_an_unknown_key_is_refused_rather_than_ignored():
    """A misspelt `colour` silently doing nothing is the failure a spec exists to prevent."""
    with pytest.raises(ValueError, match="colour"):
        sheets_spec.requests([{"range": "A1", "colour": "#000"}], TABS, "Notas")
