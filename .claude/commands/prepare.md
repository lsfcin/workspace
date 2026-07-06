---
name: prepare
description: >
  Prepare a raw prompt for Claude Code: interview, contextualize, plan, and recommend model/effort.
  The skill first interviews the user to clarify intent, then classifies the task,
  produces a plan, and outputs the optimized prompt ready for copy-paste.
  Invoke with /prepare [your raw task]
---

# /prepare

## Protocol

### Step 1 — Interview (Intention)

Before any classification, read the following workspace context files if they exist:
- `brain/USER.md` for user profile and patterns
- `brain/GOALS.md` for active goals
- `AGENTS.md` for project-wide conventions

Then, analyze the user's raw prompt for **ambiguity indicators**:
- Multiple valid approaches (e.g., "auth" could mean OAuth, JWT, or session-based)
- Missing scope (e.g., "refactor the API" without specifying which endpoints)
- Vague success criteria (e.g., "make it faster" without a target metric)

### Step 2 — Intention Interview (conditional)

If the prompt is ambiguous or high-stakes, interview the user **before** classifying.

Ask at most **3 short, contextualized questions** based on the user's profile. Examples:
- "You previously used JWT for authentication in project X. Should we reuse that approach?"
- "Is this a refactor to learn/test, or a production migration with a hard deadline?"
- "Do you want to preserve backward compatibility, or is a breaking change acceptable?"

Stop the interview once the intent is clear. Do **not** ask about implementation details (the Claude will handle that).

### Step 3 — Classification & Planning

With clarified intent, classify the task:
- **Task type**: coding, research, writing, debugging, etc.
- **Complexity**: single-file vs multi-file, architectural, security, etc.
- **Ambiguity**: well-defined vs open-ended

Then produce a **Plan** (`plan` field):
- Outline the high-level steps to solve the task.
- Identify the key files or areas of the codebase that will be touched.
- Note any dependencies or prerequisites.

### Step 4 — Recommendation

Produce the final structured response:
- `optimized_prompt`: rewritten, specific, contextualized prompt (incorporating the interview answers)
- `plan`: high-level steps to solve the task
- `tier`: recommended model tier (`low`/`medium`/`high`/`max`)
- `effort`: recommended effort level (`low`/`medium`/`high`/`max`)
- `rationale`: one-sentence justification

### Tier guide
- `low` / `haiku`: trivial fixes, one-liners, simple searches
- `medium` / `sonnet`: standard coding, debug, refactor
- `high` / `opus`: complex architecture, multi-file, deep reasoning
- `max`: mission-critical, high-stakes, highly ambiguous

### Effort guide
- `low`: fast, terse, single-step, minimal tool use
- `medium`: balanced, some exploration, default
- `high`: thorough, multi-step, tests, edge cases
- `max`: exhaustive, full analysis, alternatives

## Example

```
User: /prepare refactor auth to jwt
System:
  [Interview]
  Q: You previously used JWT for project X. Reuse the same stack?
  A: Yes, but use refresh tokens this time.
  Q: Hard deadline or exploratory?
  A: Exploratory, but I want tests.

  optimized_prompt: "Refactor the authentication module to replace session-based auth with JWT with refresh token support. Update all login/logout endpoints, middleware, and user context propagation. Ensure existing tests pass and add tests for token expiry and refresh."
  plan: "1) Update auth middleware, 2) Add /refresh endpoint, 3) Migrate tests"
  tier: high
  effort: high
  rationale: "Multi-file architectural change with security implications."
```

## Design Notes

- Interview runs in opencode + Kimi-2.6 to spare Claude Code tokens.
- Context files (USER.md, GOALS.md) are only read once at the start of the interview.
- If the prompt is already crystal-clear, skip the interview and go straight to classification.
- `plan` is included so the user can sanity-check before sending to Claude.
