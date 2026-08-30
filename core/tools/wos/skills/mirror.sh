# Mirror generation for the skill library: listing, symlink mirrors, command-file
# copies, and orphan pruning. Sourced by core/tools/wos/sync-skills — a FRAGMENT that relies
# on $SRC, $MIRRORS and $COMMANDS_DIR from the caller.

# Skill name is the basename without .md, excluding non-skill files.
is_skill() {
  local name="$1"
  # AGENTS.md: UPPERCASE.md is a TYPE, lowercase.md is an instance. A skill is an
  # instance, so no type is ever one — this used to name CONTEXT alone, and the first
  # SPECS.md written inside core/skills/ was read as a skill with no frontmatter and
  # failed the commit for every staged core/skills/*.md, not just its own.
  case "$name" in
    _template)  return 1 ;;
    [A-Z]*)     return 1 ;;
    *.original) return 1 ;;
    *)          return 0 ;;
  esac
}

# A command (slash command) is a top-level skill — NOT a sub-skill.
# Sub-skills have names like "foundry-canvas" where "foundry" is also a skill;
# they're reference docs loaded by the parent router, not invocable commands.
is_command() {
  local name="$1" prefix
  [[ "$name" == *-* ]] || return 0
  prefix="${name%%-*}"
  is_skill "$prefix" && [[ -f "$SRC/$prefix.md" ]] && return 1
  return 0
}

# The whole `skills` group's wiring point (core/SPECS.md § AD-14). A skill is markdown and calls
# no function, so its only real "off" is the mirror declining to publish it — which means one
# filter here switches all fourteen rows, and the honesty test is a behavioural probe rather than
# a grep for a call site that could not exist. Queried once, not once per skill: `--disabled` is
# one subprocess where a loop over `--enabled` would be fourteen.
_WOS_OFF=
_WOS_OFF_LOADED=
skill_disabled() {
  if [[ -z "$_WOS_OFF_LOADED" ]]; then
    _WOS_OFF="$("$(sh "$WORKSPACE/core/run" --python)" "$WORKSPACE/core/hooks/feature_law.py" --disabled 2>/dev/null)"
    _WOS_OFF_LOADED=1
  fi
  [[ -n "$_WOS_OFF" ]] && grep -qxF "$1" <<<"$_WOS_OFF"
}

list_skills() {
  local f name
  for f in "$SRC"/*.md; do
    name="$(basename "$f" .md)"
    if is_skill "$name" && ! skill_disabled "$name"; then
      printf '%s\n' "$name"
    fi
  done
}

list_commands() {
  local name
  while IFS= read -r name; do
    is_command "$name" && printf '%s\n' "$name"
  done < <(list_skills)
}

# A MIRROR IS A COPY, AND THE CHECK ASKS ABOUT ITS CONTENT.
#
# These were symlinks, and `ln -s` under Git Bash silently COPIES unless MSYS=winsymlinks:
# nativestrict, which needs Developer Mode. So the writer produced files, the checker demanded
# links, and every mirror reported `MISSING link` — the skills stage of the pre-commit pipeline
# then refused every commit that touched a skill. It is the only gate in the workspace that can
# refuse a commit for a reason the commit did not cause, and S4 had to stash a skill to land at
# all. Worse, git had already materialised the tracked mirrors as ordinary files holding their
# target's PATH TEXT, eleven characters where a skill body belonged, so the library was dark in
# this clone while every file was present and every link check that could run said nothing.
#
# Copying removes the per-OS axis instead of adding an arm for it — the port's own thesis, and
# ISSUES.md B8's decision. What a symlink bought was freshness, and freshness is now a
# regeneration at the moments that change a skill (core/hooks/commit/generators.py at commit),
# not a property of the file kind.
sync_mirror() {
  local mirror="$1"
  mkdir -p "$mirror"
  local name
  while IFS= read -r name; do
    mkdir -p "$mirror/$name"
    cp -f "$WORKSPACE/core/skills/$name.md" "$mirror/$name/SKILL.md"
  done < <(list_skills)
}

check_mirror() {
  local mirror="$1" rc=0 name copy source
  while IFS= read -r name; do
    copy="$mirror/$name/SKILL.md"
    source="$WORKSPACE/core/skills/$name.md"
    if [[ ! -f "$copy" ]]; then
      echo "MISSING mirror: $copy"; rc=1
    elif ! cmp -s "$copy" "$source"; then
      echo "STALE mirror: $copy (differs from $source)"; rc=1
    fi
  done < <(list_skills)
  return $rc
}

# A command file is the skill body relocated to a different directory depth, so a
# straight `cp` leaves every relative link pointing at nothing: `../flows/x.md` in
# core/skills/ means core/flows/x.md, but from .claude/commands/ it resolves to
# .claude/flows/x.md. All 6 relative links across the mirrors were dead this way
# (found 2026-07-30). Rewrite them against the source dir on the way out; the
# staleness check compares the same rendered form, or every file reads as stale.
render_command() {
  # PYTHONIOENCODING for the same reason core/run exports it: this script prints "→",
  # and a Python encoding stdout as the console codepage dies on it mid-message.
  PYTHONIOENCODING=utf-8 "$(sh "$WORKSPACE/core/run" --python)" - "$1" "$SRC" "$COMMANDS_DIR" <<'PY'
import os, re, sys

src_file, src_dir, dst_dir = sys.argv[1:4]


# Code spans and fences quote syntax rather than link to it — `[what it is](url)`
# in core/skills/inbox.md is the shape a ref entry must take, not a path to fix.
PROTECTED_OR_LINK = re.compile(r'(```.*?```|`[^`\n]+`)|\]\(([^)\s]+)\)', re.DOTALL)


def rewrite(match):
    if match.group(1):
        return match.group(0)
    path, sep, frag = match.group(2).partition('#')
    if not path or path.startswith(('http://', 'https://', 'mailto:')):
        return match.group(0)
    absolute = os.path.normpath(os.path.join(src_dir, path))
    return '](' + os.path.relpath(absolute, dst_dir) + sep + frag + ')'


text = open(src_file, encoding='utf-8').read()
sys.stdout.write(PROTECTED_OR_LINK.sub(rewrite, text))
PY
}

sync_commands() {
  mkdir -p "$COMMANDS_DIR"
  local name
  while IFS= read -r name; do
    render_command "$SRC/$name.md" > "$COMMANDS_DIR/$name.md"
  done < <(list_commands)
}

check_commands() {
  local rc=0 name cmd src
  while IFS= read -r name; do
    cmd="$COMMANDS_DIR/$name.md"
    src="$SRC/$name.md"
    if [[ ! -f "$cmd" ]]; then
      echo "MISSING command: $cmd"; rc=1
    elif ! diff -q <(render_command "$src") "$cmd" >/dev/null 2>&1; then
      echo "STALE command: $cmd (differs from rendered $src)"; rc=1
    fi
  done < <(list_commands)
  return $rc
}

# A mirror dir or command file with no corresponding source skill is an orphan.
# Orphans are the failure that dangles symlinks and breaks opencode startup.
orphans() {
  local action="$1" rc=0 mirror d c name
  for mirror in "${MIRRORS[@]}"; do
    [[ -d "$mirror" ]] || continue
    for d in "$mirror"/*/; do
      [[ -d "$d" ]] || continue
      name="$(basename "$d")"
      # A switched-off skill's leftover mirror is an orphan too: publishing is the only thing
      # "off" means here, so a stale link would leave the feature half-disabled.
      if ! is_skill "$name" || [[ ! -f "$SRC/$name.md" ]] || skill_disabled "$name"; then
        if [[ "$action" == prune ]]; then rm -rf "$d"; echo "pruned orphan mirror: $d"
        else echo "ORPHAN mirror (no source skill): $d"; rc=1; fi
      fi
    done
  done
  for c in "$COMMANDS_DIR"/*.md; do
    [[ -f "$c" ]] || continue
    name="$(basename "$c" .md)"
    if [[ ! -f "$SRC/$name.md" ]] || ! is_command "$name" || skill_disabled "$name"; then
      if [[ "$action" == prune ]]; then rm -f "$c"; echo "pruned orphan command: $c"
      else echo "ORPHAN command (no source skill): $c"; rc=1; fi
    fi
  done
  return $rc
}

