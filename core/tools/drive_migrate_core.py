#!/usr/bin/env python3
"""
Auth, config, and low-level Drive ops shared by drive_migrate.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import google_auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError  # noqa: F401 (re-exported for drive_migrate.py)

# ── Config ───────────────────────────────────────────────────────────────────

CIN_DISCIPLINAS_ID = "1xihkjDlbpIxjRmAJeCWIrBvFT37Qe6IM"

SLIDE_MIMETYPES = {
    "application/vnd.google-apps.presentation",               # native Google Slides
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
    "application/vnd.ms-powerpoint",                          # .ppt
}

FOLDER_MAP = {
    "Tec. na Educação":                 "tecnologias-na-educacao",
    "AI4Good":                          "ai4good",
    "P1":                               "programacao-1",
    "Computação Gráfica":               "computacao-grafica",
    "Motores Gráficos":                 "motores-graficos",
    "IA":                               "inteligencia-artificial",
    "P2":                               "programacao-2",
    "PGP":                              "gerencia-de-projetos",
    "PI1":                              "projeto-interdisciplinar-1",
    "PI2":                              "projeto-interdisciplinar-2",
    "PI3":                              "projeto-interdisciplinar-3",
    "Intro à Informática (Ed. Física)": "info-ed-fisica",
    "Apps p/ Gastro":                   "apps-gastronomia",
}

SCOPES_READ  = ["https://www.googleapis.com/auth/drive.readonly"]
SCOPES_WRITE = ["https://www.googleapis.com/auth/drive"]

STATE_FILE = Path("academy_migration_state.json")
MAP_FILE   = Path("academy_migration_map.json")

# ── Auth ──────────────────────────────────────────────────────────────────────

def get_cin_service():
    creds = google_auth.auth("cin", "drive", SCOPES_READ)
    return build("drive", "v3", credentials=creds)

def get_personal_service():
    # "drive-write" = separate token file; does not overwrite readonly token
    creds = google_auth.auth("personal", "drive-write", SCOPES_WRITE)
    return build("drive", "v3", credentials=creds)

# ── Drive helpers ─────────────────────────────────────────────────────────────

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


def find_or_create_folder(svc, name: str, parent_id: str, dry_run: bool) -> str:
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


def copy_file(personal_svc, cin_file_id: str, name: str, parent_id: str) -> dict:
    result = personal_svc.files().copy(
        fileId=cin_file_id,
        body={"name": name, "parents": [parent_id]},
        fields="id, webViewLink",
    ).execute()
    return result
