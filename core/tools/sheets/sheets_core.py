# sheets_core.py — Google Sheets read+write boundary (account-agnostic) for core/tools/sheets/gsheets
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'auth'))
import gauth  # noqa: E402
import write_approval  # noqa: E402  — on the path gauth put there
from sheets_a1 import col_index, col_letters, split_a1  # noqa: E402

from googleapiclient.discovery import build  # noqa: E402

# The two grants are core/tools/auth/grants.txt's `sheets` row. The read row carries drive.readonly
# for `list`; the write row is `spreadsheets` alone — the ufrpe token consented to exactly that,
# and widening it would demote a working token to a re-consent (see SPECS.md § Auth).
def get_service(alias: str, write: bool = False):
    return build('sheets', 'v4', credentials=gauth.auth(alias, 'sheets', write))


def edit_url(spreadsheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"


def list_spreadsheets(alias: str, name: str = "") -> list:
    svc = build("drive", "v3", credentials=gauth.auth(alias, "sheets"))   # its own row carries drive.readonly
    q = "mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
    if name:
        q += " and name contains '" + name.replace("\\", "\\\\").replace("'", "\\'") + "'"
    res = svc.files().list(q=q, pageSize=100, orderBy="modifiedTime desc",
                           fields="files(id,name,modifiedTime,webViewLink)").execute()
    return res.get("files", [])


def tabs(alias: str, spreadsheet_id: str) -> dict:
    """The spreadsheet's title and its tabs, without a single cell: what every A1 needs resolved."""
    return get_service(alias).spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="properties.title,sheets.properties(sheetId,title,index,gridProperties)",
    ).execute()


def get_values(alias: str, spreadsheet_id: str, ranges: list, formulas: bool = False) -> list:
    """[{range, values}] per requested range; FORMULA shows `=SUM(...)` where a value would be."""
    res = get_service(alias).spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=ranges,
        valueRenderOption="FORMULA" if formulas else "FORMATTED_VALUE",
    ).execute()
    return res.get("valueRanges", [])


def get_full(alias: str, spreadsheet_id: str, ranges: list | None = None) -> dict:
    """The raw grid with formats, rules and validation — the input side of `apply`."""
    return get_service(alias).spreadsheets().get(
        spreadsheetId=spreadsheet_id, ranges=ranges or [], includeGridData=bool(ranges),
    ).execute()


def version(alias: str, spreadsheet_id: str) -> str:
    """Drive's file version, read on the sheets READ token (drive.readonly rides in that row)."""
    drive = build('drive', 'v3', credentials=gauth.auth(alias, 'sheets'))
    return drive.files().get(fileId=spreadsheet_id, fields='version').execute()['version']


def cell_lines(value_range: dict, rows: list) -> list:
    """`Tab!B3: 'old' → 'new'` for every cell that changes — the plan a `set` is approved on."""
    tab, cells = split_a1(value_range["range"])
    start = cells.split(":")[0]
    letters = start.rstrip("0123456789")
    top, left = int(start[len(letters):] or 1), col_index(letters)
    old = value_range.get("values", [])
    lines = []
    for r, row in enumerate(rows):
        for c, new in enumerate(row):
            was = old[r][c] if r < len(old) and c < len(old[r]) else ""
            if str(was) != str(new):
                lines.append(f"{tab}!{col_letters(left + c)}{top + r}: {was!r} → {new!r}")
    return lines


def set_values(alias: str, spreadsheet_id: str, a1: str, rows: list) -> dict:
    """USER_ENTERED: the cell is parsed as if typed, so `=formula`, dates and numbers are real.
    The revision is the old cells themselves: Drive's version moves on a mere recalculation."""
    old = get_values(alias, spreadsheet_id, [a1], formulas=True)[0]
    write_approval.gate("sheets set", f"{spreadsheet_id} {a1}", rows, cell_lines(old, rows),
                        revision=old.get("values", []))
    return get_service(alias, write=True).spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=a1, valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()


def append_values(alias: str, spreadsheet_id: str, a1: str, rows: list) -> dict:
    """The table's current cells are the revision: where the rows land depends on them."""
    old = get_values(alias, spreadsheet_id, [a1], formulas=True)[0].get("values", [])
    write_approval.gate("sheets append", f"{spreadsheet_id} {a1}", rows,
                        [f"+ {' | '.join(map(str, row))}" for row in rows], revision=old)
    return get_service(alias, write=True).spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=a1, valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS", body={"values": rows},
    ).execute()


def create(alias: str, title: str, tab_titles: list | None = None) -> dict:
    body: dict = {"properties": {"title": title}}
    if tab_titles:
        body["sheets"] = [{"properties": {"title": t}} for t in tab_titles]
    write_approval.gate("sheets new", alias, body,
                        [f"+ cria planilha {title!r}" + (f" com abas {', '.join(tab_titles)}" if tab_titles else "")])
    return get_service(alias, write=True).spreadsheets().create(
        body=body, fields="spreadsheetId,spreadsheetUrl,sheets.properties(sheetId,title)",
    ).execute()


def apply(alias: str, spreadsheet_id: str, requests: list) -> dict:
    """A structural batch is checked against Drive's version: there no cell values are the revision."""
    write_approval.gate("sheets apply", spreadsheet_id, requests, write_approval.request_lines(requests),
                        revision=version(alias, spreadsheet_id))
    return get_service(alias, write=True).spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests},
    ).execute()
