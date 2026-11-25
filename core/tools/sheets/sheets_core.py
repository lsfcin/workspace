# sheets_core.py — Google Sheets read+write boundary (account-agnostic) for core/tools/sheets/gsheets
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'auth'))
import gauth  # noqa: E402

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


def set_values(alias: str, spreadsheet_id: str, a1: str, rows: list) -> dict:
    """USER_ENTERED: the cell is parsed as if typed, so `=formula`, dates and numbers are real."""
    return get_service(alias, write=True).spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=a1, valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()


def append_values(alias: str, spreadsheet_id: str, a1: str, rows: list) -> dict:
    return get_service(alias, write=True).spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=a1, valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS", body={"values": rows},
    ).execute()


def create(alias: str, title: str, tab_titles: list | None = None) -> dict:
    body: dict = {"properties": {"title": title}}
    if tab_titles:
        body["sheets"] = [{"properties": {"title": t}} for t in tab_titles]
    return get_service(alias, write=True).spreadsheets().create(
        body=body, fields="spreadsheetId,spreadsheetUrl,sheets.properties(sheetId,title)",
    ).execute()


def apply(alias: str, spreadsheet_id: str, requests: list) -> dict:
    return get_service(alias, write=True).spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests},
    ).execute()
