#!/mnt/workspace/.venv/bin/python3
# google_auth.py — Shared OAuth2 auth for workspace Google services (drive, calendar, gmail)
import json, pathlib
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

_GMAIL_CONFIG = pathlib.Path.home() / ".config" / "workspace-gmail"


def config_dir(service: str) -> pathlib.Path:
    d = pathlib.Path.home() / ".config" / f"workspace-{service}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _credentials_file(service: str) -> pathlib.Path:
    """Find credentials.json: service dir first, then gmail dir (same GCP project)."""
    for d in (config_dir(service), _GMAIL_CONFIG):
        f = d / "credentials.json"
        if f.exists():
            return f
    raise FileNotFoundError(
        f"credentials.json not found. Place it in {config_dir(service)}/ "
        f"(download from GCP console → APIs & Services → Credentials)."
    )


def get_accounts() -> list:
    """Read accounts.json from gmail config (canonical source for all Google services)."""
    f = _GMAIL_CONFIG / "accounts.json"
    return json.loads(f.read_text()).get("accounts", []) if f.exists() else []


def primary_aliases() -> list:
    return [a["aliases"][0] for a in get_accounts() if a.get("aliases")]


def resolve_alias(alias: str) -> str:
    for acct in get_accounts():
        if alias in acct.get("aliases", []):
            return acct["aliases"][0]
    return alias


def auth(alias: str, service: str, scopes: list) -> Credentials:
    """OAuth2 flow for alias+service. Tokens stored per-service per-alias."""
    d = config_dir(service)
    token_path = d / f"{alias}.token.json"
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(_credentials_file(service)), scopes
            )
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds
