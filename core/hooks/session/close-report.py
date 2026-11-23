#!/usr/bin/env python3
# Stop — hand Lucas the close report that roundup armed, on the one channel the model never reads.
#
# Silent on every turn but the close: Stop fires after EVERY response (why notify.py refused it),
# so this does nothing unless core/tools/wos/close/report.py finds this session's marker. Then it
# either asks the agent once for a missing handoff block (decision: block, the only Stop channel
# that reaches the model) or emits the report as systemMessage, which addresses Lucas alone
# (core/hooks/SPECS.md). The report's content and rules live in report.py, not here.
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'wos' / 'close'))

import feature_law  # noqa: E402
from hook_input import parse_stdin  # noqa: E402


def main() -> int:
    if not feature_law.is_enabled('close-report'):
        return 0
    _raw, _tool, _tool_input, session_id, _cwd = parse_stdin()
    if not session_id:
        return 0
    import report
    try:
        result = report.deliver(session_id)
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'systemMessage': f'close report failed: {error}'}))
        return 0
    if result:
        kind, text = result
        print(json.dumps({'decision': 'block', 'reason': text} if kind == 'ask' else {'systemMessage': text}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
