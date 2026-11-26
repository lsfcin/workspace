# write_approval.py — no write token loads until Lucas approved the exact plan it carries out
"""Two steps, one plan. Step 1: a write verb calls gate() without --approve; the plan prints with a
one-time CODE and the process exits 75 (EX_TEMPFAIL) — never 0, and never 1 or 2, which an agent
reads as "retry". Step 2: Lucas reads the plan in chat and says ok; the agent reruns the same command
with --approve CODE, and the harness asks him a second time (core/permissions.txt approve-remote-edit).

Design, the panel's verdicts and Lucas's choices (2026-11-25): outputs/remote-edit-gate-plan.md."""
import atexit, hashlib, json, os, pathlib, secrets, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'hooks'))
from feature_law import is_enabled  # noqa: E402
from platform_law import secure_file, session_state  # noqa: E402

AWAITING = 75          # EX_TEMPFAIL: the plan is printed and waits for Lucas
TTL_S = 15 * 60        # a plan older than this is refused: long enough to read, short enough to rot
# Grants whose write token gauth refuses without an approved plan. It grows one service per slice
# until it holds every write grant; then the set, and this comment, are deleted.
GATED = frozenset({"sheets", "drive", "docs"})
SHOWN = 75             # diff lines a plan prints; the rest is saved where the plan names it


def take_code(argv: list) -> str:
    """Remove `--approve CODE` from argv in place, so no CLI's argparse ever sees it."""
    for i, arg in enumerate(argv):
        if arg.startswith("--approve="):
            del argv[i]
            return arg.split("=", 1)[1]
        if arg == "--approve":
            if i + 1 >= len(argv):
                sys.exit("--approve needs the CODE the plan printed")
            code = argv[i + 1]
            del argv[i:i + 2]
            return code
    return ""


_code = take_code(sys.argv)
_gated = False      # some verb in this process called gate()
_approved = ""      # the digest gate() verified
_consumed = False   # gauth already unlinked the plan for this process


def _warn_unused() -> None:
    if _code and not _gated:
        print(f"WRITE APPROVAL: --approve {_code} reached a command that writes nothing; it was ignored.",
              file=sys.stderr)


if _code:
    atexit.register(_warn_unused)


def pending_path() -> pathlib.Path:
    """One plan at a time: a new plan replaces the old one (Lucas, 2026-11-25)."""
    return session_state("pending_write.json")


def turn() -> str:
    """The stamp core/hooks/session/turn.py writes on each of Lucas's prompts; '' where no harness writes one."""
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    path = session_state(f"turn_{sid}") if sid else None
    return path.read_text(encoding="utf-8").strip() if path and path.exists() else ""


def digest(action: str, target: str, revision, payload) -> str:
    blob = json.dumps([action, target, revision, payload], sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def request_lines(requests: list) -> list:
    """A batchUpdate shown as one compact JSON line per request: no renderer per request type to rot."""
    return [f"{i}. {json.dumps(r, ensure_ascii=False, separators=(',', ':'))}" for i, r in enumerate(requests, 1)]


def diff_lines(old: str, new: str, name: str) -> list:
    """A whole-body replace shown as its unified diff: counts, the first SHOWN lines, and the path of
    the full diff — a deletion past line SHOWN must still be readable before --approve (2026-11-26)."""
    import difflib
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), "atual", "novo", lineterm=""))
    if not diff:
        return []
    full = session_state("pending_write.diff")
    full.write_text("\n".join(diff) + "\n", encoding="utf-8", newline="\n")
    body = diff[2:]
    plus = sum(1 for d in body if d.startswith("+"))
    minus = sum(1 for d in body if d.startswith("-"))
    shown = [f"{name}: +{plus} / -{minus} linhas"] + body[:SHOWN]
    return shown + ([f"… {len(body) - SHOWN} linhas a mais — diff completo em {full}"] if len(body) > SHOWN else [])


def _refuse(why: str) -> None:
    sys.exit(f"WRITE APPROVAL REFUSED: {why}\n    Nothing was written. Run the command again WITHOUT --approve for a fresh plan.")


def gate(action: str, target: str, payload, lines: list, revision="") -> None:
    """Call BEFORE loading a write token. No CODE: print the plan and exit 75. CODE: verify or refuse."""
    global _gated, _approved
    _gated = True
    if not is_enabled("write-approval"):
        return
    want = digest(action, target, revision, payload)
    path = pending_path()
    if not _code:
        code = secrets.token_hex(3)
        path.write_text(json.dumps({"code": code, "digest": want, "created": time.time(), "turn": turn(),
                                    "action": action, "target": target}), encoding="utf-8", newline="\n")
        secure_file(path)
        print(f"WRITE PLAN — {action} {target}")
        print("\n".join(f"    {line}" for line in lines) or "    (no change)")
        print(f"\n[PLAN READY — AWAITING LUCAS] CODE {code}. Stop here: show this plan to Lucas and end your turn."
              f"\n    Only after he answers, rerun the same command with --approve {code}.")
        sys.exit(AWAITING)
    plan = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if plan.get("code") != _code:
        _refuse(f"no pending plan has CODE {_code}.")
    if time.time() - plan["created"] > TTL_S:
        _refuse(f"the plan is older than {TTL_S // 60} min.")
    if plan["digest"] != want:
        _refuse("the plan changed since it was shown — the remote document moved, or the payload differs.")
    if plan["turn"] and plan["turn"] == turn():
        _refuse("the plan was made in this same turn; Lucas has not answered it yet.")
    _approved = want


def consent() -> None:
    """`auth --write` loads the write token only to consent to it, and writes nothing: no plan to
    approve. Without this a dead write token of a gated grant could never be renewed."""
    global _consumed
    _consumed = True


def consume(grant: str) -> None:
    """gauth.auth(write=True) calls this, so a verb that forgot gate() is refused, never left unguarded.
    The first write unlinks the approved plan; later writes in the same process reuse that approval."""
    global _consumed
    if grant not in GATED or _consumed or not is_enabled("write-approval"):
        return
    path = pending_path()
    plan = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not _approved or plan.get("digest") != _approved or plan.get("code") != _code:
        raise PermissionError(f"WRITE APPROVAL: no approved plan for a '{grant}' write in this process — "
                              "the verb must call write_approval.gate() before loading its write token.")
    path.unlink()
    _consumed = True
