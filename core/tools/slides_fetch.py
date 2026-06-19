#!/mnt/workspace/.venv/bin/python3
# slides_fetch.py — Google Slides API read-only for workspace OS
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from googleapiclient.discovery import build
import google_auth

SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]


def get_service(alias: str):
    return build("slides", "v1", credentials=google_auth.auth(alias, "slides", SCOPES))


def get_presentation(alias: str, presentation_id: str) -> dict:
    """Fetch full presentation JSON from Google Slides API."""
    return get_service(alias).presentations().get(
        presentationId=presentation_id
    ).execute()


def list_presentations(alias: str, name: str = "") -> list:
    """List presentations from Drive. Optionally filter by name substring."""
    from googleapiclient.discovery import build as _build
    drive_creds = google_auth.auth(alias, "drive",
                                   ["https://www.googleapis.com/auth/drive.readonly"])
    svc = _build("drive", "v3", credentials=drive_creds)
    q = "mimeType='application/vnd.google-apps.presentation' and trashed=false"
    if name:
        q += f" and name contains '{name}'"
    res = svc.files().list(
        q=q,
        pageSize=100,
        fields="files(id,name,modifiedTime,webViewLink)",
        orderBy="modifiedTime desc",
    ).execute()
    return res.get("files", [])
