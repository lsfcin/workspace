#!/mnt/workspace/.venv/bin/python3
# drive_core.py — Google Drive read+write seam (account-agnostic) for Core/tools/drive
import pathlib
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import google_auth

SCOPES_READ  = ["https://www.googleapis.com/auth/drive.readonly"]
SCOPES_WRITE = ["https://www.googleapis.com/auth/drive"]

EXPORT_MIME = {
    "application/vnd.google-apps.document":     "application/pdf",
    "application/vnd.google-apps.spreadsheet":  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.presentation": "application/pdf",
}

FILE_FIELDS = "id,name,mimeType,modifiedTime,size,parents,webViewLink"

GDOC_MIME = "application/vnd.google-apps.document"


def get_service(alias: str, write: bool = False):
    """Build a Drive service for alias. Read uses the `drive` token (readonly);
    write uses a separate `drive-write` token (full scope) so it never clobbers
    the readonly one."""
    service, scopes = ("drive-write", SCOPES_WRITE) if write else ("drive", SCOPES_READ)
    return build("drive", "v3", credentials=google_auth.auth(alias, service, scopes))


# ── Reads (per-alias; build their own readonly service) ────────────────────────

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


# ── Writes (take an explicit write service so callers reuse one across ops) ─────

def list_folder(svc, folder_id: str) -> list:
    items, page_token = [], None
    while True:
        resp = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            pageSize=1000,
        ).execute()
        items.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return items


def find_or_create_folder(svc, name: str, parent_id: str, dry_run: bool = False) -> str:
    if dry_run:
        return f"[dry-run-folder:{name}]"
    resp = svc.files().list(
        q=(f"'{parent_id}' in parents"
           f" and name='{name.replace(chr(39), chr(39)+chr(39))}'"
           f" and mimeType='application/vnd.google-apps.folder'"
           f" and trashed=false"),
        fields="files(id, name)",
    ).execute()
    existing = resp.get("files", [])
    if existing:
        return existing[0]["id"]
    folder = svc.files().create(
        body={
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        },
        fields="id",
    ).execute()
    return folder["id"]


def copy_file(svc, file_id: str, name: str, parent_id: str) -> dict:
    return svc.files().copy(
        fileId=file_id,
        body={"name": name, "parents": [parent_id]},
        fields="id, webViewLink",
    ).execute()


def upload_local(svc, path: pathlib.Path, parent_id: str, as_gdoc: bool = False,
                 name: str = None) -> dict:
    """Upload a local file to parent_id. When as_gdoc, the target mimeType is a
    Google Doc so Drive converts (e.g. .docx→Google Doc) on import. Returns the
    created file's {id, name, webViewLink}."""
    path = pathlib.Path(path)
    media = MediaFileUpload(str(path), resumable=True)
    body = {"name": name or path.name, "parents": [parent_id]}
    if as_gdoc:
        body["mimeType"] = GDOC_MIME
    return svc.files().create(
        body=body, media_body=media, fields="id,webViewLink,name"
    ).execute()
