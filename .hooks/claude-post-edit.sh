#!/usr/bin/env bash
# PostToolUse: Edit, Write
# - Regenerates .pyi (Python) or .d.ts (JS) immediately after every save
# - Syncs CONTEXT.md File Map via ctx-sync.py

file=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)

[ -z "$file" ] || [ ! -f "$file" ] && exit 0

case "$file" in
  *.py)
    STUBGEN="/mnt/workspace/.venv/bin/stubgen"
    if [ -x "$STUBGEN" ]; then
      dir=$(dirname "$file")
      "$STUBGEN" "$file" -o "$dir" --quiet 2>/dev/null \
        && printf "✓ .pyi updated: ${file%.py}.pyi\n"
    fi
    ;;
  *.js)
    d=$(dirname "$file"); cfg=""
    while [ "$d" != "." ] && [ "$d" != "/" ]; do
      [ -f "$d/jsconfig.json" ] && cfg="$d/jsconfig.json" && break
      d=$(dirname "$d")
    done
    if [ -n "$cfg" ] && command -v tsc &>/dev/null; then
      tsc -p "$cfg" --emitDeclarationOnly 2>/dev/null \
        && printf "✓ .d.ts updated in $(dirname $cfg)\n"
    fi
    ;;
esac

# Sync CONTEXT.md File Map for the file's directory
python3 /mnt/workspace/.hooks/ctx-sync.py "$(dirname "$file")" 2>/dev/null

exit 0
