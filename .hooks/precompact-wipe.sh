#!/usr/bin/env bash
# PreCompact — wipe the session CONTEXT.md seen-markers so the chain is re-read after
# compaction (injected context may be summarized away). See VERIFY.md W1.
sid=$(python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)
[ -n "$sid" ] && rm -f "/tmp/claude_ctx_seen_${sid}.txt"
exit 0
