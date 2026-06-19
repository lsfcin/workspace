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


def list_presentations(alias: str) -> list:
    """List presentations from Drive (mimeType filter)."""
    from googleapiclient.discovery import build as _build
    drive_creds = google_auth.auth(alias, "drive",
                                   ["https://www.googleapis.com/auth/drive.readonly"])
    svc = _build("drive", "v3", credentials=drive_creds)
    res = svc.files().list(
        q="mimeType='application/vnd.google-apps.presentation' and trashed=false",
        pageSize=30,
        fields="files(id,name,modifiedTime,webViewLink)",
        orderBy="modifiedTime desc",
    ).execute()
    return res.get("files", [])
