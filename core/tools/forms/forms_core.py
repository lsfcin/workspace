# forms_core.py — Google Forms read+write boundary (account-agnostic) for Core/tools/forms/gforms
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'auth'))
import gauth  # noqa: E402

from googleapiclient.discovery import build  # noqa: E402

# The two grants are core/tools/auth/grants.txt's `forms` row. `drive.file` rides with the write grant
# because a form the tool created is a Drive file the tool must be able to file into a folder.
def get_service(alias: str, write: bool = False):
    return build('forms', 'v1', credentials=gauth.auth(alias, 'forms', write))


def get_drive(alias: str):
    """Drive under the same write grant — only for filing a form the tool created."""
    creds = gauth.auth(alias, 'forms', write=True)
    return build('drive', 'v3', credentials=creds)


def edit_url(form_id: str) -> str:
    return f"https://docs.google.com/forms/d/{form_id}/edit"


def create(alias: str, title: str, document_title: str = "") -> dict:
    """The API accepts only a title at creation; everything else is a batchUpdate."""
    body = {"info": {"title": title}}
    if document_title:
        body["info"]["documentTitle"] = document_title
    return get_service(alias, write=True).forms().create(body=body).execute()


def get_form(alias: str, form_id: str) -> dict:
    return get_service(alias).forms().get(formId=form_id).execute()


def apply(alias: str, form_id: str, requests: list) -> dict:
    return get_service(alias, write=True).forms().batchUpdate(
        formId=form_id, body={"requests": requests}
    ).execute()


def list_responses(alias: str, form_id: str) -> list:
    svc = get_service(alias)
    out, token = [], None
    while True:
        res = svc.forms().responses().list(formId=form_id, pageToken=token).execute()
        out.extend(res.get("responses", []))
        token = res.get("nextPageToken")
        if not token:
            return out


def move(alias: str, form_id: str, folder_id: str) -> dict:
    """File the form into a Drive folder; `drive.file` reaches only files this tool created."""
    svc = get_drive(alias)
    prev = svc.files().get(fileId=form_id, fields="parents").execute()
    return svc.files().update(
        fileId=form_id,
        addParents=folder_id,
        removeParents=",".join(prev.get("parents", [])),
        fields="id,parents,webViewLink",
    ).execute()


def question_titles(form: dict) -> dict:
    """questionId → title, the join that turns a response payload into readable text."""
    titles = {}
    for item in form.get("items", []):
        q = item.get("questionItem", {}).get("question")
        if q:
            titles[q["questionId"]] = item.get("title", "(sem título)")
        for sub in item.get("questionGroupItem", {}).get("questions", []):
            titles[sub["questionId"]] = item.get("title", "(sem título)")
    return titles
