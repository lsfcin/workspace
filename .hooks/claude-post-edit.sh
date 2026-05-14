#!/usr/bin/env bash
# PostToolUse: Edit, Write
# - Regenerates .pyi (Python) or .d.ts (JS) immediately after every save
# - Reminds to add first-line description comment when editing files that lack one
# - Syncs CONTEXT.md File Map via ctx-sync.py

file=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)

[ -z "$file" ] || [ ! -f "$file" ] && exit 0

# Interface regeneration
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

# First-line description reminder (fires after editing existing files without comment)
if [ "$CLAUDE_TOOL_NAME" = "Edit" ]; then
  first=$(head -1 "$file" 2>/dev/null)
  missing=false
  case "$file" in
    *.py)                   echo "$first" | grep -qE '^\s*#'    || missing=true ;;
    *.js|*.ts|*.tsx|*.dart) echo "$first" | grep -qE '^\s*//'   || missing=true ;;
    *.css|*.scss)           echo "$first" | grep -qE '^\s*/\*'  || missing=true ;;
    *.html)                 echo "$first" | grep -qE '^\s*<!--' || missing=true ;;
  esac
  if $missing; then
    printf "💬 FIRST-LINE MISSING: %s\n   Add a description comment as line 1 before the next edit.\n" "$file"
  fi
fi

# Sync CONTEXT.md File Map for the file's directory
python3 /mnt/workspace/.hooks/ctx-sync.py "$(dirname "$file")" 2>/dev/null

exit 0
