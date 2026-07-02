#!/usr/bin/env bash
# SessionStart — prune stale session marker files (context seen-markers, facade reads,
# codegraph nudges) older than 2 days. See VERIFY.md W1.
find /tmp -maxdepth 1 \( -name 'claude_ctx_seen_*' -o -name 'claude_facades_*' -o -name 'claude_cg_nudged_*' \) -mmin +2880 -delete 2>/dev/null
exit 0
