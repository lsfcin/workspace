# inbox.py — capture plain text/media into brain/INBOX.md ($0, no backend call).
from __future__ import annotations
import pathlib
import sys
from datetime import datetime
from telegram.ext import ContextTypes

from .config import WORKSPACE_ROOT

sys.path.insert(0, str(WORKSPACE_ROOT / "core" / "tools"))
import attachments_util  # noqa: E402
import tool_law  # noqa: E402

BRAIN_ATTACHMENTS = WORKSPACE_ROOT / "brain" / "attachments"
INBOX_FILE = WORKSPACE_ROOT / "brain" / "INBOX.md"
INBOX_MARKER = "<!-- add entries below, newest first -->"


def append_entry(entry: str) -> None:
    # The switch, at the moment the feature does its one job: writing into the workspace.
    # `telegram-capture` read `-` in core/features.txt for as long as this code lived in a repo
    # the workspace did not version, because a wiring path into a nested repo would have made a
    # Tier 0 test of the workspace assert on a stranger. Absorbing aiwbot is what made the line
    # writable (2026-09-12). It guards here rather than at the bot's entrypoint so switching the
    # feature off stops the CAPTURE without stopping the bot's other surfaces.
    tool_law.require('telegram-capture')
    text = INBOX_FILE.read_text(encoding='utf-8')
    marker_pos = text.index(INBOX_MARKER) + len(INBOX_MARKER)
    updated = text[:marker_pos] + f"\n\n{entry}" + text[marker_pos:]
    INBOX_FILE.write_text(updated, encoding='utf-8', newline='\n')


def build_entry(body: str, attachment_path: pathlib.Path | None, *, forwarded: bool = False) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    lines = []
    if forwarded:
        # Lucas typed it himself in every other case (this bot has one allowed chat_id) —
        # a forward carries someone else's content, so it's quoted data, never a command.
        lines.append("[src: telegram-fwd]")
    lines.append(body)
    if attachment_path is not None:
        lines.append(f"[attachment: {attachment_path.relative_to(WORKSPACE_ROOT)}]")
    lines.append(f"— via aiwbot · {date}")
    return "\n".join(lines)


async def save_media(file_id: str, context: ContextTypes.DEFAULT_TYPE, suffix: str) -> pathlib.Path:
    tg_file = await context.bot.get_file(file_id)
    month_dir = attachments_util.month_dir(BRAIN_ATTACHMENTS)
    filename = attachments_util.safe_name(f"aiwbot-{file_id}{suffix}")
    filepath = attachments_util.unique_path(month_dir / filename)
    await tg_file.download_to_drive(str(filepath))
    return filepath
