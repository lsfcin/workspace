# sheets — specs

What the Sheets API takes, and the compact form this family writes instead.

## A1 in, GridRange out

A person reads `'Aba 2'!B2:C3`; every `batchUpdate` request wants `{sheetId: 7, startRowIndex: 1, endRowIndex: 3, startColumnIndex: 1, endColumnIndex: 3}` — a numeric tab id, 0-based, end-exclusive. [`sheets_a1.py`](sheets_a1.py) is the one translation. An open side stays open (`A:A`, `2:4`): an absent index is the whole extent, rows added later included. A tab whose title is also a column span (`Notas`) is the tab, as in the UI. An unknown tab is refused naming the real ones. The values endpoints (`read`, `set`, `append`) take A1 directly and need none of this.

## Format spec

A JSON array; one entry is one `range` plus what to do to it. Unknown keys are refused — a misspelt `colour` doing nothing in silence is the failure a spec exists to prevent. `--dry-run` prints the requests.

```json
[
  {"range": "Notas!A1:F1", "bold": true, "font": "Arial", "size": 11, "color": "#ffffff",
   "bg": "#1a73e8", "align": "center", "valign": "middle", "wrap": "wrap",
   "borders": {"outer": "solid-thick", "inner": "dotted", "color": "#000000"},
   "height": 32, "freeze": {"rows": 1}},
  {"range": "Notas!A1:C1", "merge": true},
  {"range": "Notas!B:B", "width": 80, "number": "0.0"},
  {"range": "Notas!F2:F60", "when": ["<", 5], "bg": "#f4cccc", "color": "#990000"},
  {"range": "Notas!A2:F60", "when": "=$F2>=7", "bold": true},
  {"range": "Notas!E2:E60", "gradient": ["#f4cccc", "#fff2cc", "#d9ead3"]},
  {"range": "Notas!D2:D60", "validate": ["list", "presente", "falta", "justificada"], "help": "Escolha uma opção"},
  {"range": "Notas!B2:B60", "validate": ["between", 0, 10]},
  {"range": "Notas!G2:G60", "validate": ["checkbox"]}
]
```

- **Style** (`font size color bold italic underline strike bg align valign wrap rotate number`) becomes one `repeatCell` whose `fields` mask names only those keys, so setting bold never wipes a size chosen by hand. `number` is a pattern string, or a whole `numberFormat` object.
- **Borders**: sides `top bottom left right inner-h inner-v`, groups `outer inner all`; styles `solid solid-medium solid-thick dashed dotted double none`.
- **Sizes**: `height` (rows) and `width` (columns) in pixels over the range's span; `merge` is `true`, `"rows"` or `"cols"`; `freeze` acts on the range's tab.
- **Conditions** are one vocabulary for `when` and `validate`, because the API uses one `BooleanCondition` for both: a string starting with `=` is a custom formula; otherwise `[op, *values]` with `< <= > >= = != between not-between contains not-contains starts ends is empty not-empty before after date list range checkbox`. `range` takes an A1 source of allowed answers.
- With `when` or `gradient`, the entry is a **conditional rule** and its colours apply only where the rule holds — never a `repeatCell` painting the whole range. A rule is inserted at index 0, so the last one written wins ties.
- `validate` defaults to `strict: true` (a wrong value is refused, not flagged); `help` is the message shown on the cell.

## Auth

Two grants in [`../auth/grants.txt`](../auth/grants.txt): `sheets` (`spreadsheets.readonly`, `drive.readonly` — `list` is a Drive call, on this row's own token) and `sheets-write` (`spreadsheets`). The write row is deliberately **without** `drive.file`: the ufrpe token was consented to `spreadsheets` alone (the CAPD sheet), and a token holding less than its row asks for warns and wants re-consent. The price is that `new` cannot file into a folder; a spreadsheet lands in Drive's root and is moved by hand. The day a folder is needed, widen the row and re-consent once.
