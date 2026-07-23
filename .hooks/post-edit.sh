#!/usr/bin/env bash
# PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md

input_json="${CLAUDE_TOOL_INPUT:-$(cat)}"
file=$(echo "$input_json" | python3 -c \
	"import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input'); ti=ti if isinstance(ti,dict) else d; print(ti.get('file_path',''))" 2>/dev/null)

[ -z "$file" ] || [ ! -f "$file" ] && exit 0

dir=$(dirname "$file")

# Vendored third-party code (a `.vendor` marker in the dir or an ancestor) gets no
# generated interfaces: the stubs are noise we would have to re-diff on every upstream
# update, and stubgen mangles the layout for package-shaped vendored code. Same marker
# the size gate reads (.hooks/check-line-counts.sh, .hooks/pre-edit.py).
is_vendored() {
	local d; d=$(cd "$1" 2>/dev/null && pwd) || return 1
	while [ -n "$d" ] && [ "$d" != "/" ]; do
		[ -f "$d/.vendor" ] && return 0
		{ [ -f "$d/.git" ] || [ -d "$d/.git" ]; } && return 1
		d=$(dirname "$d")
	done
	return 1
}
VENDORED=0; is_vendored "$dir" && VENDORED=1

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

# ── Interface regeneration (skipped entirely for vendored code) ─────────────────
[ "$VENDORED" = 1 ] || case "$file" in
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
		python3 /mnt/workspace/core/tools/inspect "$file" 2>/dev/null \
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
		if [ -f "$paper_root/terms.yaml" ] && [ -x "/mnt/workspace/core/tools/terms" ]; then
			/mnt/workspace/core/tools/terms "$paper_root" 2>/dev/null | grep -E "^[[:space:]]|^⚠" || true
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

# ── Facade reminder ────────────────────────────────────────────────────────────
case "$file" in
	*.ts|*.tsx|*.js|*.jsx|*.py|*.dart)
		has_facade=false
		for _f in "$dir/index.ts" "$dir/index.tsx" "$dir/index.js" "$dir/__init__.py" "$dir/index.dart"; do
			[ -f "$_f" ] && has_facade=true && break
		done
		if ! $has_facade; then
			_n=$(find "$dir" -maxdepth 1 -type f \
				\( -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.py" -o -name "*.dart" \) \
				! -name "index.*" ! -name "__init__.py" ! -name "*.d.ts" ! -name "*.pyi" \
				2>/dev/null | wc -l)
			[ "$_n" -ge 1 ] && printf "💬 NO FACADE: %s has %d file(s) — add index.ts / __init__.py / index.dart\n" "$dir" "$_n"
		fi
		;;
esac

# ── CONTEXT.md line-2 description reminder ─────────────────────────────────────
if [ "$(basename "$file")" = "CONTEXT.md" ]; then
	line2=$(sed -n '2p' "$file" 2>/dev/null)
	printf '%s' "$line2" | grep -qE '^>\s*\S' \
		|| printf "💬 CONTEXT.md DESCRIPTION MISSING: %s\n   Add '> One-line description' as line 2.\n" "$file"
fi

# ── CONTEXT.md project-goal-link reminder — code/<proj>/CONTEXT.md only ───────
if [ "$(basename "$file")" = "CONTEXT.md" ] && [ "$(dirname "$dir")" = "/mnt/workspace/code" ]; then
	line3=$(sed -n '3p' "$file" 2>/dev/null)
	printf '%s' "$line3" | grep -qE '^>\s*goal:\s*(\[[^]]+\]\([^)]+\)|none)\s*$' \
		|| printf "💬 CONTEXT.md GOAL LINK MISSING: %s\n   Add '> goal: [slug](../../brain/goals/<slug>.md)' or '> goal: none' as line 3.\n" "$file"
fi

# ── Sync CONTEXT.md Routing block — leaf dir only ─────────────────────────────
[ -f "$dir/CONTEXT.md" ] \
    && python3 /mnt/workspace/.hooks/context_synchronizer.py "$dir" 2>/dev/null

# ── codegraph sync — keep index fresh after every source edit ─────────────────
if [[ "$file" == /mnt/workspace/code/* ]]; then
	case "$file" in
		*.pyi|*.d.ts|*.dart.api|*.texif|*.csvif) : ;;  # generated — skip
		*.py|*.js|*.ts|*.tsx|*.dart|*.jsx)
			cg_root=""; cg_dir=$(dirname "$file")
			while [ "$cg_dir" != "/" ]; do
				[ -d "$cg_dir/.codegraph" ] && cg_root="$cg_dir" && break
				cg_dir=$(dirname "$cg_dir")
			done
			if [ -n "$cg_root" ]; then
				codegraph sync "$cg_root" 2>&1 | head -1
			else
				proj_root=$(echo "$file" | grep -oP '^/mnt/workspace/code/[^/]+')
				[ -n "$proj_root" ] && printf "⚠️  no codegraph index — run: codegraph init %s\n" "$proj_root"
			fi
			;;
	esac
fi

# ── ESLint + Prettier for TypeScript projects under code/ (R1-R6) ─────────────
if [[ "$file" == /mnt/workspace/code/* ]] && [[ "$file" == *.ts ]] && [[ "$file" != *.d.ts ]]; then
	# Walk up to nearest eslint.config.js (ESLint 9 flat config = full R1-R6 enforcement)
	proj_dir=""
	_d=$(dirname "$file")
	while [ "$_d" != "/" ]; do
		if [ -f "$_d/eslint.config.js" ]; then
			proj_dir="$_d"
			break
		fi
		_d=$(dirname "$_d")
	done
	if [ -n "$proj_dir" ]; then
		PRETTIER_BIN="$proj_dir/node_modules/.bin/prettier"
		ESLINT_BIN="$proj_dir/node_modules/.bin/eslint"
		if [ -x "$PRETTIER_BIN" ]; then
			(cd "$proj_dir" && "$PRETTIER_BIN" --write "$file" 2>/dev/null) \
				&& printf "✓ prettier: %s\n" "$(basename "$file")"
		fi
		if [ -x "$ESLINT_BIN" ]; then
			LINT_OUT=$(cd "$proj_dir" && "$ESLINT_BIN" "$file" 2>&1 | head -40)
			[ -n "$LINT_OUT" ] && printf "⚠️  ESLint (R1-R6):\n%s\n" "$LINT_OUT"
		fi
	fi
fi

exit 0
