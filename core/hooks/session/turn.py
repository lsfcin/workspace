# turn.py — UserPromptSubmit: stamp each of Lucas's prompts, so a write plan knows whether he answered it
"""core/tools/write_approval.py records this stamp in the plan it prints and refuses `--approve` while the
stamp is still the same: a plan approved in the very turn that made it was never seen by Lucas.
Only the harness can tell a prompt from a tool call, so the stamp has to come from a hook."""
import json, pathlib, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from feature_law import is_enabled  # noqa: E402
from platform_law import session_state  # noqa: E402


def main() -> None:
    if not is_enabled("write-approval"):
        return
    try:
        sid = json.loads(sys.stdin.read() or "{}").get("session_id", "")
    except json.JSONDecodeError:
        return
    if sid:
        session_state(f"turn_{sid}").write_text(str(time.time_ns()), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
