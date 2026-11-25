---
name: sheets
description: >
  Read and edit Google Sheets in place across all configured accounts — cells by A1 address,
  values as TSV, style, conditional rules and validation as a JSON spec.
---

Google Sheets across all configured accounts (personal, cin, ufrpe): every cell read next to its own address, written back as TSV, styled from a versioned spec.

Arguments: $ARGUMENTS

## Commands

```
core/run tools/sheets/gsheets list   --name "<substring>"
core/run tools/sheets/gsheets read   --account <alias> <spreadsheet_id> ["Aba!A1:F40"] [--formulas] [--json]
core/run tools/sheets/gsheets set    --account <alias> <spreadsheet_id> "Aba!B2" values.tsv
core/run tools/sheets/gsheets append --account <alias> <spreadsheet_id> Aba rows.tsv
core/run tools/sheets/gsheets new    --account <alias> --tab Aba "Title"
core/run tools/sheets/gsheets format --account <alias> <spreadsheet_id> spec.json [--dry-run]
core/run tools/sheets/gsheets apply  --account <alias> <spreadsheet_id> requests.json
```

## How to work a sheet

1. `read` first: the tabs, their sheetIds, and the cells labelled by column letter and row number — the addresses a write takes.
2. Values: write a TSV and `set` it at the top-left cell; `=formulas` go in as formulas.
3. Look: author a format spec (`core/tools/sheets/SPECS.md` § Format spec), keep it next to the material it belongs to, `--dry-run` it, then `format`.
4. Anything the spec cannot say goes through `apply`, the Sheets API's own request list; `read --json` shows the current formats and rules in that shape.

## Notes

- Two auth grants per account — on a dead token the CLI names the fix:
  `core/run tools/sheets/gsheets auth <alias> --reauth` (add `--write` for the write grant)
- `new` lands in Drive's root: the write grant is `spreadsheets` alone, on purpose (SPECS § Auth)
- A 403 naming a project number is the Sheets API being disabled in the OAuth client's project, not a bad grant
