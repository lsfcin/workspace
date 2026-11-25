# sheets
> Spreadsheets, read and edited in place. Provider leaf: `gsheets` (Google Sheets API).

```bash
core/run tools/sheets/gsheets list   --name "notas"
core/run tools/sheets/gsheets read   --account ufrpe <spreadsheet_id>              # tabs + every cell, labelled by its address
core/run tools/sheets/gsheets read   --account ufrpe <spreadsheet_id> "'Aba 2'!B2:F40" --formulas
core/run tools/sheets/gsheets set    --account ufrpe <spreadsheet_id> "Notas!B2" valores.tsv
core/run tools/sheets/gsheets append --account ufrpe <spreadsheet_id> Notas linhas.tsv
core/run tools/sheets/gsheets new    --account personal --tab Notas --tab Faltas "Turma 2026.2"
core/run tools/sheets/gsheets format --account personal <spreadsheet_id> estilo.json [--dry-run]
core/run tools/sheets/gsheets apply  --account personal <spreadsheet_id> requests.json
```

**`read` prints every cell next to its own address** — a header of column letters, each row led by its number — so what is read is already the A1 a `set` takes. `--json` gives the raw grid with formats, conditional rules and validation: the input side of `apply`.

**Values go in as TSV, typed as a person would type them** (`USER_ENTERED`): `=MÉDIA(B2:B9)` becomes a formula, `7,5` a number in a pt-BR sheet.

**`apply` is the real boundary; `format` is a convenience over it.** The format spec — style, borders, sizes, merges, freeze, conditional rules, validation — is A1-addressed JSON that `sheets_spec.py` turns into the GridRange requests the API takes: [`SPECS.md`](SPECS.md) § Format spec, alongside the two auth grants and why `new` cannot file into a folder.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | sheets — specs |
| [`gsheets`](gsheets) | — | — | Google Sheets CLI: auth, list, read, set, append, new, format, apply |
| [`sheets_a1.py`](sheets_a1.py) | [`sheets_a1.pyi`](sheets_a1.pyi) | `col_index`, `col_letters`, `split_a1`, `quote`, `grid_range` | sheets_a1.py — a sheet's cells addressed as people write them: A1 ranges ↔ GridRange, TSV ↔ values, hex ↔ colour |
| [`sheets_core.py`](sheets_core.py) | [`sheets_core.pyi`](sheets_core.pyi) | `get_service`, `edit_url`, `list_spreadsheets`, `tabs`, `get_values` | sheets_core.py — Google Sheets read+write boundary (account-agnostic) for core/tools/sheets/gsheets |
| [`sheets_spec.py`](sheets_spec.py) | [`sheets_spec.pyi`](sheets_spec.pyi) | `condition`, `requests` | sheets_spec.py — a sheet's look written as JSON: a format spec (style, borders, sizes, conditional rules, validation) → Sheets API batchUpdate requests |
<!-- routing:end -->
