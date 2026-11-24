# gauth.py — Google's leaf of the auth family: shared OAuth2 for every Google-backed tool
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'hooks'))
import tool_law  # noqa: E402
from platform_law import secure_dir, secure_file  # noqa: E402

# Guarded at IMPORT, not in a main(): this is a library with no entrypoint of its own, and
# the feature is the shared OAuth2 itself. Every Google-backed tool — mail, calendar, files,
# slides — reaches credentials through this module, so one refusal here is what "google-auth
# is off" honestly means. A per-tool guard would leave the others still authenticating.
tool_law.require('google-auth')

from google.oauth2.credentials import Credentials  # noqa: E402
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError

_GMAIL_CONFIG = pathlib.Path.home() / ".config" / "workspace-gmail"

_SCOPE = "https://www.googleapis.com/auth/"


def grants() -> dict:
    """core/tools/auth/grants.txt as {service: (read scopes, write scopes, cli or '')}."""
    table = {}
    for line in (pathlib.Path(__file__).with_name("grants.txt")).read_text(encoding="utf-8").splitlines():
        cols = line.split("\t")
        if line.startswith("#") or len(cols) != 4 or cols[0] == "service":
            continue
        read, write = ([_SCOPE + s for s in col.split(",")] if col != "-" else [] for col in cols[1:3])
        table[cols[0]] = (read, write, "" if cols[3] == "-" else cols[3])
    return table


def _grant(service: str) -> tuple:
    """(service, write?, its row) for a token directory name such as 'drive-write'."""
    base = service.removesuffix("-write")
    return base, base != service, grants().get(base)


def config_dir(service: str) -> pathlib.Path:
    d = pathlib.Path.home() / ".config" / f"workspace-{service}"
    d.mkdir(parents=True, exist_ok=True)
    secure_dir(d)
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
    return json.loads(f.read_text(encoding='utf-8')).get("accounts", []) if f.exists() else []


def primary_aliases() -> list:
    return [a["aliases"][0] for a in get_accounts() if a.get("aliases")]


def home_alias() -> str:
    """The workspace's own Google account (personal): the first in accounts.json. Never ask which."""
    return (primary_aliases() or ["personal"])[0]


def resolve_alias(alias: str | None) -> str:
    """An alias to its primary name; no alias at all means the home account."""
    if not alias:
        return home_alias()
    for acct in get_accounts():
        if alias in acct.get("aliases", []):
            return acct["aliases"][0]
    return alias


class AuthExpired(RuntimeError):
    """A token past recovery. Carries recovery text meant to be shown to Lucas verbatim."""


def account_email(alias: str) -> str:
    """The Google address an alias signs in as — the one thing the consent screen asks for."""
    primary = resolve_alias(alias)
    email = "unknown (check ~/.config/workspace-gmail/accounts.json)"
    for acct in get_accounts():
        if primary in acct.get("aliases", []):
            email = acct.get("email", email)
    return email


def recovery_text(alias: str, service: str, token_path: pathlib.Path) -> str:
    """The whole instruction: one command, and which account to sign in as."""
    _, write, row = _grant(service)
    if row and row[2]:
        step = f"core/run {row[2]} auth {alias}{' --write' if write else ''} --reauth"
    else:
        step = f"rm {token_path}   # then re-run the command that just failed"
    lines = [
        f"GOOGLE AUTH EXPIRED — service '{service}', account '{alias}'.",
        "The stored token was revoked or expired. A refresh cannot recover it; only a new",
        "consent can.",
        "",
        "AGENT: run this yourself, do not hand it to Lucas as a chore. It opens a browser",
        "on his machine, so run it in the background and tell him the address below.",
        f"    {step}",
        "",
        f"LUCAS: a browser tab opens — sign in as:  {account_email(alias)}",
        "Signing in as a different Google account succeeds and then reads the wrong",
        "mailbox/drive, which is worse than failing. Check the address on the consent screen.",
    ]
    return "\n".join(lines)


def run(main_fn) -> None:
    """Entrypoint wrapper: a dead token prints its own fix instead of a traceback."""
    try:
        main_fn()
    except AuthExpired as exc:
        sys.exit(str(exc))
    except HttpError as exc:
        # A rejected request is the API answering, not the tool crashing. The reason is in
        # the response and it is usually actionable ("object ID length should not be < 5").
        sys.exit(f"GOOGLE API REFUSED THE REQUEST ({exc.status_code}):\n    {exc.reason}")


def auth(alias: str, service: str, write: bool = False) -> Credentials:
    """OAuth2 flow for alias+service, the scopes read from grants.txt. Tokens stored per-grant per-alias:
    a read loads workspace-<service>/, a write workspace-<service>-write/, and nothing else crosses."""
    row = grants().get(service)
    if not row or (write and not row[1]):
        raise ValueError(f"no {'write ' if write else ''}grant '{service}' in core/tools/auth/grants.txt")
    scopes = row[1] if write else row[0]
    service = f"{service}-write" if write else service
    d = config_dir(service)
    token_path = d / f"{alias}.token.json"
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # A revoked token raises RefreshError (invalid_grant) here and does NOT fall
            # through to consent, so this is the one place that can name the fix.
            try:
                creds.refresh(Request())
            except RefreshError as exc:
                raise AuthExpired(recovery_text(alias, service, token_path)) from exc
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(_credentials_file(service)), scopes
            )
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding='utf-8', newline='\n')
        secure_file(token_path)

    return creds
