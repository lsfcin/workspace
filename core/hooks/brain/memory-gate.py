#!/usr/bin/env python3
# PreToolUse, capability write — an agent's fact goes to the file that owns it, never to a store:
# a harness memory store is refused outright, and brain/INBOX.md (Lucas's capture, AGENTS.md
# § IMPROVE) only lets an agent DELETE — triage passes, a new or reworded line is refused.
#
# WHY. A harness memory index is folded into the system prompt of EVERY session, including the nine
# in ten it has nothing to do with, and harnesses write to it unprompted. Lucas ruled 2026-09-15 that
# the store goes, with `brain/USER.md`: AGENTS.md, the CONTEXT.md chain, core/ and brain/ carry what
# an agent needs; each rule the store carried now lives with its owner.
#
# The harness path `~/.claude/projects/<name>/memory` stays a symlink onto `brain/memory/`, so a
# write arrives here spelled either way and resolving makes the two one target. Without the
# symlink the write would land outside the workspace, where nothing sees it.
#
# The refusal offers no switch: offered, it became the path — an agent passed the question to
# Lucas instead of routing the fact (2026-09-24). The refusal names the owner instead, because a
# gate that only says no gets the same text written again a turn later.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'checks'))
from write_payload import WORKSPACE_ROOT, block, target  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
import platform_law  # noqa: E402

if not feature_law.is_enabled('memory-gate'):
    sys.exit(0)

file_path, data = target()
if not file_path:
    sys.exit(0)

try:
    written = platform_law.rel(Path(file_path).resolve(), WORKSPACE_ROOT)
except OSError:
    sys.exit(0)



def added(data: dict, path: Path) -> list:
    """Non-blank lines this write would put in the file that were not there before."""
    pairs = [(e.get('old_string', ''), e.get('new_string', '')) for e in data.get('edits') or [data]]
    if 'content' in data:
        pairs = [(path.read_text(encoding='utf-8') if path.is_file() else '', data['content'])]
    return [line for old, new in pairs for line in new.splitlines()
            if line.strip() and line not in old.splitlines()]


inbox = written == 'brain/INBOX.md' and added(data, Path(file_path))
if written.startswith('brain/memory/') or inbox:
    block(f"⛔ MEMORY GATE — {written}: " + ("INBOX.md is Lucas's capture; an agent only deletes "
          "from it." if inbox else "this workspace keeps no memory store."),
          "   Put the fact where its readers already are:",
          "     a rule the agent must obey      -> core/norms/, or the SPECS.md that owns it",
          "     something untrue about the repo -> ISSUES.md",
          "     work still to do                -> ROADMAP.md",
          "     what a folder holds or routes   -> that folder's CONTEXT.md",
          "   Pick the destination yourself and write it there. Do not ask Lucas about memory.")

sys.exit(0)
