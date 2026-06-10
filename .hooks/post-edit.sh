#!/usr/bin/env bash
# PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md

file=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c \
	"import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)

[ -z "$file" ] || [ ! -f "$file" ] && exit 0

dir=$(dirname "$file")

# Locate tsc (PATH or ~/.local/bin fallback)
TSC=""; command -v tsc &>/dev/null && TSC="tsc"
[ -z "$TSC" ] && [ -x "$HOME/.local/bin/tsc" ] && TSC="$HOME/.local/bin/tsc"

# Walk up to nearest tsconfig.json, stopping at git root
find_tsconfig() {
	local d="$1"
	while [ "$d" != "/" ]; do
		[ -f "$d/tsconfig.json" ] && echo "$d/tsconfig.json" && return
		{ [ -f "$d/.git" ] || [ -d "$d/.git" ]; } && return
		d=$(dirname "$d")
	done
}

# ── Interface regeneration ──────────────────────────────────────────────────────
case "$file" in
	*.py)
		STUBGEN="/mnt/workspace/.venv/bin/stubgen"
		[ -x "$STUBGEN" ] && "$STUBGEN" "$file" -o "$dir" --quiet 2>/dev/null \
			&& printf "✓ .pyi: ${file%.py}.pyi\n"
		;;
	*.js)
		if [ -n "$TSC" ]; then
			"$TSC" --allowJs --checkJs false --declaration --emitDeclarationOnly \
						 --declarationDir "$dir" --target ES2020 "$file" 2>/dev/null \
				&& printf "✓ .d.ts: ${file%.js}.d.ts\n"
		fi
		if [ ! -f "$dir/jsconfig.json" ]; then
			cat > "$dir/jsconfig.json" << 'EOF'
{
	"compilerOptions": {
		"allowJs": true, "checkJs": false,
		"declaration": true, "emitDeclarationOnly": true,
		"outDir": ".", "target": "ES2020"
	},
	"include": ["*.js"]
}
EOF
			printf "✓ jsconfig.json scaffolded: %s\n" "$dir"
		fi
		;;
	*.ts)
		if [ -n "$TSC" ]; then
			tsconfig=$(find_tsconfig "$dir")
			if [ -n "$tsconfig" ]; then
				proj_root=$(dirname "$tsconfig")
				decl_cfg="$proj_root/tsconfig.declarations.json"
				if [ -f "$decl_cfg" ]; then
					# Project-specific declarations config — handles complex typeRoots (e.g. Foundry VTT).
					# noEmitOnError:false allows partial emission despite unresolved globals; suppress
					# diagnostic noise since errors are expected (Foundry globals are bundler-only).
					"$TSC" -p "$decl_cfg" >/dev/null 2>&1 || true
					printf "✓ .d.ts regenerated: %s\n" "$proj_root"
				else
					"$TSC" --declaration --emitDeclarationOnly \
								 --declarationDir "$dir" --target ES2020 --skipLibCheck \
								 "$file" 2>/dev/null \
						&& printf "✓ .d.ts: ${file%.ts}.d.ts\n"
				fi
			else
				"$TSC" --declaration --emitDeclarationOnly \
							 --declarationDir "$dir" --target ES2020 --skipLibCheck \
							 "$file" 2>/dev/null \
					&& printf "✓ .d.ts: ${file%.ts}.d.ts\n"
				cat > "$dir/tsconfig.json" << 'EOF'
{
	"compilerOptions": {
		"declaration": true, "emitDeclarationOnly": true,
		"outDir": ".", "target": "ES2020", "strict": true
	}
}
EOF
				printf "✓ tsconfig.json scaffolded: %s\n" "$dir"
			fi
		fi
		;;
	*.csv|*.tsv)
		python3 /mnt/workspace/Core/tools/inspect "$file" 2>/dev/null \
			&& printf "✓ .csvif: %sif\n" "$file"
		;;
	*.dart)
		python3 /mnt/workspace/.hooks/dart-api-extract.py "$file" 2>/dev/null
		;;
	*.tex)
		python3 /mnt/workspace/.hooks/tex-interface-gen.py "$file" 2>/dev/null
		# Term consistency check (warn-only; requires terms.yaml in paper root)
		paper_root="$dir"
		while [ "$paper_root" != "/" ] && [ ! -f "$paper_root/terms.yaml" ]; do
			paper_root=$(dirname "$paper_root")
		done
		if [ -f "$paper_root/terms.yaml" ] && [ -x "/mnt/workspace/Core/tools/terms" ]; then
			/mnt/workspace/Core/tools/terms "$paper_root" 2>/dev/null | grep -E "^[[:space:]]|^⚠" || true
		fi
		;;
	*.bib)
		python3 /mnt/workspace/.hooks/tex-interface-gen.py --bib-check "$file" 2>/dev/null
		;;
esac

# ── First-line description reminder ────────────────────────────────────────────
if [ "$CLAUDE_TOOL_NAME" = "Edit" ]; then
	first=$(head -1 "$file" 2>/dev/null)
	missing=false
	case "$file" in
		*.py)                   echo "$first" | grep -qE '^\s*#'    || missing=true ;;
		*.js|*.ts|*.tsx|*.dart) echo "$first" | grep -qE '^\s*//'   || missing=true ;;
		*.css|*.scss)           echo "$first" | grep -qE '^\s*/\*'  || missing=true ;;
		*.html)                 echo "$first" | grep -qE '^\s*<!--' || missing=true ;;
		*.yaml|*.yml|*.toml)    echo "$first" | grep -qE '^\s*#'   || missing=true ;;
		*.tex)                  echo "$first" | grep -qE '^\s*%'   || missing=true ;;
		*.md)                   echo "$first" | grep -qE '^\s*#'   || missing=true ;;
	esac
	$missing && printf "💬 FIRST-LINE MISSING: %s\n   Add a description comment as line 1.\n" "$file"
fi

# ── CONTEXT.md line-2 description reminder ─────────────────────────────────────
if [ "$(basename "$file")" = "CONTEXT.md" ]; then
	line2=$(sed -n '2p' "$file" 2>/dev/null)
	printf '%s' "$line2" | grep -qE '^>\s*\S' \
		|| printf "💬 CONTEXT.md DESCRIPTION MISSING: %s\n   Add '> One-line description' as line 2.\n" "$file"
fi

# ── Sync CONTEXT.md Routing block — walk up to workspace root ─────────────────
walk="$dir"
while [ "$walk" != "/" ]; do
    { [ -f "$walk/CONTEXT.md" ] || [ -f "$walk/WORKSPACE.md" ]; } \
        && python3 /mnt/workspace/.hooks/context_synchronizer.py "$walk" 2>/dev/null
    [ -f "$walk/WORKSPACE.md" ] && break
    walk=$(dirname "$walk")
done

exit 0
