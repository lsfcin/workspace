#!/usr/bin/env bash
# Neutral session-start entrypoint

set -euo pipefail

workspace_root=$(cd "$(dirname "$0")/.." && pwd)

printf '== WORKSPACE.md ==\n'
sed -n '1,120p' "$workspace_root/WORKSPACE.md"
