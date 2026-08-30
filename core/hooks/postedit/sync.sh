# Keep generated indexes fresh: the CONTEXT.md routing block and the codegraph.
# Sourced by core/hooks/post-edit.sh — a FRAGMENT, not a standalone script:
# it relies on $file, $dir, $TSC and find_tsconfig from the caller.

# ── Sync the routing blocks: the directory's CONTEXT.md, and the index of a sharded type ──
# The FILE is passed, not its directory. Both are needed and only the file carries both: the
# synchronizer derives the directory itself, and a shard's index is found from the shard's own
# name. Passing "$dir" behind a CONTEXT.md test also meant a workspace-root .md never synced
# at all, since the root's routing block lives in AGENTS.md.
sh "$RUN" hooks/routing/context_synchronizer.py "$file" 2>/dev/null

# ── codegraph sync — keep index fresh after every source edit ─────────────────
if [[ "$file" == "$WORKSPACE_ROOT"/code/* ]]; then
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
				proj_root=$(echo "$file" | grep -oP "^${WORKSPACE_ROOT}/code/[^/]+")
				[ -n "$proj_root" ] && printf "⚠️  no codegraph index — run: codegraph init %s\n" "$proj_root"
			fi
			;;
	esac
fi
