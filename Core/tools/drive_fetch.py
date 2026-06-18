#!/mnt/workspace/.venv/bin/python3
# drive_fetch.py — Google Drive API auth and file operations for Core/tools/drive
import io, pathlib
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import google_auth

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

EXPORT_MIME = {
    "application/vnd.google-apps.document":     "application/pdf",
    "application/vnd.google-apps.spreadsheet":  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.presentation": "application/pdf",
}

FILE_FIELDS = "id,name,mimeType,modifiedTime,size,parents,webViewLink"


def get_service(alias: str):
    return build("drive", "v3", credentials=google_auth.auth(alias, "drive", SCOPES))


def list_files(alias: str, folder_id: str = "root", page_size: int = 50) -> list:
    svc = get_service(alias)
    q = f"'{folder_id}' in parents and trashed=false"
    res = svc.files().list(q=q, pageSize=page_size, fields=f"files({FILE_FIELDS})").execute()
    return res.get("files", [])


def search_files(alias: str, query: str, page_size: int = 20) -> list:
    svc = get_service(alias)
    q = f"fullText contains '{query}' and trashed=false"
    res = svc.files().list(q=q, pageSize=page_size, fields=f"files({FILE_FIELDS})").execute()
    return res.get("files", [])


def recent_files(alias: str, page_size: int = 30) -> list:
    svc = get_service(alias)
    res = svc.files().list(
        pageSize=page_size,
        orderBy="modifiedTime desc",
        fields=f"files({FILE_FIELDS})",
        q="trashed=false",
    ).execute()
    return res.get("files", [])


def download_file(alias: str, file_id: str, dest_dir: pathlib.Path) -> pathlib.Path:
    """Download or export file. Returns saved path."""
    svc = get_service(alias)
    meta = svc.files().get(fileId=file_id, fields="name,mimeType").execute()
    name, mime = meta["name"], meta["mimeType"]

    dest_dir.mkdir(parents=True, exist_ok=True)

    if mime in EXPORT_MIME:
        export_mime = EXPORT_MIME[mime]
        ext = ".pdf" if "pdf" in export_mime else ".xlsx"
        req = svc.files().export_media(fileId=file_id, mimeType=export_mime)
        name = name + ext
    else:
        req = svc.files().get_media(fileId=file_id)

    path = dest_dir / name
    with open(path, "wb") as fh:
        dl = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            _, done = dl.next_chunk()

    return path
