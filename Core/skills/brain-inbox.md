Triage Brain/INBOX.md — route each entry to a goal file, existing backlog, or delete.

Arguments: $ARGUMENTS

## Protocol

Read `Brain/INBOX.md`. If empty, say so and stop.

For each entry:
1. Understand intent — new goal seed · achievement for existing goal · discard
2. Propose route:
   - **new goal** → suggest `# [ area | horizon ] title` + first backlog item
   - **add to existing** → name the goal file and the exact backlog line to add
   - **delete** → one-line reason
3. Present all proposed routes first. Wait for confirmation. Act only after Lucas confirms.

After confirmation:
- Write new goal files or append items to confirmed backlogs
- Clear confirmed entries from INBOX.md — leave unconfirmed entries untouched
