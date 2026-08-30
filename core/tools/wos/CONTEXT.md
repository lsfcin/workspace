# wos
> Tools that act on the workspace itself: spec ledger, contract check, skill mirrors.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`close/`](close/CONTEXT.md) | What a session close writes, and what it does with each artifact afterwards. |
| [`diagram/`](diagram/CONTEXT.md) | The workspace drawn from its own declarations: one generated HTML picture, zero tokens, no model. |
| [`session/`](session/CONTEXT.md) | What a session costs and what fills it, read from the local transcripts. No network, no model. |

| File | Description |
|------|-------------|
| [`skills/mirror.sh`](skills/mirror.sh) | Mirror generation for the skill library: listing, symlink mirrors, command-file copies, and orphan pruning. Sourced by core/tools/wos/sync-skills — a FRAGMENT that relies on $SRC, $MIRRORS and $COMMANDS_DIR from the caller. |
| [`skills/validate.sh`](skills/validate.sh) | Frontmatter validation for every layer of the agent library — skills, flows, the flow composition DAG, and agents. The law itself is core/SCHEMA.md; these only enforce it. Sourced by core/tools/wos/sync-skills; relies on $SRC and $WORKSPACE from the caller. |
| [`sync-global-skills`](sync-global-skills) | link workspace-vendored global skills into $HOME |
| [`sync-skills`](sync-skills) | regenerate skill mirrors from core/skills/*.md |
<!-- routing:end -->
