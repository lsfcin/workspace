#!/usr/bin/env bash
# SessionStart — prune stale session marker files (context seen-markers, facade reads,
# codegraph nudges) older than 2 days. See code/ROADMAP-verify.md W1.
# `rm -rf`, not `-delete`: a seen-marker is a DIRECTORY of one file per entry since 2026-09-02 —
# an append to a shared file lost 22% of its marks under a parallel Read batch (hook_input.py).
# `-delete` refuses a non-empty one, silently, which would leave every store here forever.
find /tmp -maxdepth 1 \( -name 'claude_ctx_seen_*' -o -name 'claude_iface_seen_*' -o -name 'claude_facades_*' -o -name 'claude_cg_nudged_*' -o -name 'claude_nostub_*' -o -name 'claude_branch_*' \) -mmin +2880 -exec rm -rf {} + 2>/dev/null
exit 0
