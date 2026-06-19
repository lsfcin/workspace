---
name: brain-finished
description: >
  Mark an achievement done, advance to the next selected achievement, write a new ease-start.
---

Mark an achievement done, advance to the next selected achievement, write a new ease-start.

Arguments: $ARGUMENTS

Parse $ARGUMENTS as an achievement short-id (e.g. `exp-ablation`).

## Protocol

1. Find the goal file containing `> [ ] [<id>]` in its backlog
2. In that file:
   a. Change `> [ ] [<id>]` → `> [x] [<id>]` in `## backlog`
   b. Move `> [x] [<id>] ...` line to top of `<!-- done:start -->...<!-- done:end -->` block
   c. Find next `> [ ]` item in backlog — this is the new selected achievement
   d. Update `## selected next achievement` heading and description to match the new item
   e. Write a new `**ease-start**` — read the goal context, `>**fears**`, and the new achievement; craft the smallest action that bypasses the emotional or cognitive barrier
   f. Update `>**dynamics**` motion field to `advancing`
3. Acknowledge the win — one short genuine sentence before moving on
4. Present the new ease-start and ask if it feels right
