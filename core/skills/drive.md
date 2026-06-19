---
name: drive
description: >
  List, search, and download files from Google Drive across all configured accounts (personal, cin, ufrpe).
  Invoke with /drive [intent].
---

# Drive skill

Arguments: $ARGUMENTS

---

## Overview

Access Google Drive (read-only) across 3 accounts via `core/tools/drive`.

## Commands

```bash
core/tools/drive recent [--account all|personal|cin|ufrpe] [--limit 20]
core/tools/drive list   [--account ...] [--folder <id>]
core/tools/drive search [--account ...] <query>
core/tools/drive download --account <alias> <file_id>
core/tools/drive auth <alias>   # first-time per account
```

## Auth (first-time setup)

Tokens stored at `~/.config/workspace-drive/{alias}.token.json`. Run once per account:

```bash
core/tools/drive auth personal
core/tools/drive auth cin
core/tools/drive auth ufrpe
```

## Workflow

1. User asks about a Drive file → run `search` or `recent`.
2. Found file → show name, date, link. Ask if should download.
3. Download → file lands in `~/Downloads/workspace-drive/`. Google Docs/Slides exported as PDF; Sheets as .xlsx.
4. If file needs processing (PDF, text) → read and summarize.

## Accounts

Same aliases as Gmail: `personal` (lsf.cin@gmail.com), `cin` (lsf@cin.ufpe.br), `ufrpe` (lucas.sfigueiredo@ufrpe.br).
