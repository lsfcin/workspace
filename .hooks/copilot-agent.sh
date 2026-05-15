#!/usr/bin/env bash
# Copilot wrapper that honors .agentrc.json and runs session-start and hooks
set -euo pipefail

workspace_root=$(cd "$(dirname "$0")/.." && pwd)
cfg="$workspace_root/.agentrc.json"

if [ ! -f "$cfg" ]; then
  echo "No .agentrc.json found at $cfg"
  exit 1
fi

start_session=$(python3 - <<PY
import json
cfg=json.load(open('.agentrc.json'))
print(cfg.get('start_session',''))
PY
)

if [ -z "$start_session" ]; then
  echo "no start_session defined in .agentrc.json"
  exit 1
fi

echo "Running workspace session-start: $start_session"
# If PowerShell Core is available and a PS1 start file exists, use it.
if command -v pwsh >/dev/null 2>&1 && [ -f "$workspace_root/.hooks/start-session.ps1" ]; then
  pwsh -NoProfile -File "$workspace_root/.hooks/start-session.ps1"
else
  bash "$workspace_root/$start_session"
fi

exit 0
