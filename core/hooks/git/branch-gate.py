#!/usr/bin/env python3
# PreToolUse write and PostToolUse shell — a session writes only on the branch it chose.
#
# Before a write: refuse main/master/develop in a Git Flow repo, refuse a branch a parallel session
# switched to under this one, and name the branch on this session's first write in each repo. After
# a shell call: when it ran git switch/checkout, re-record, so this session's own switch never
# reads as someone else's. The rules and their limits live with the marker, in branch_marker.py.
#
# FAILS OPEN. Any error here passes the write: a branch gate that crashes must never cost a
# session its edits (Lucas, 2026-11-09). The off switch is the feature `branch-gate`.
import json
import re
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
import feature_law  # noqa: E402
from hook_input import capability, parse_stdin  # noqa: E402

SWITCH = re.compile(r'\bgit\b[^;&|\n]*\b(?:switch|checkout|branch\s+-[mM])\b')


def main() -> int:
    if not feature_law.is_enabled('branch-gate'):
        return 0
    raw, tool, data, session, _ = parse_stdin()
    event = str(raw.get('hook_event_name') or raw.get('hookEventName') or 'PreToolUse')
    try:
        import branch_marker
        if event == 'PostToolUse':
            if capability(tool, data) == 'shell' and SWITCH.search(str(data.get('command', ''))):
                branch_marker.follow(session)
            return 0
        if capability(tool, data) != 'write' or not data.get('file_path'):
            return 0
        refusal, note = branch_marker.verdict(Path(data['file_path']), session)
    except Exception:   # noqa: BLE001 — fail open, see the head
        return 0
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    if note:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': event, 'additionalContext': note}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
