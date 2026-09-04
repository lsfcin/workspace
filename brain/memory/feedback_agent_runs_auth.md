---
name: feedback-agent-runs-auth
description: "Agent runs every auth command itself; Lucas only does what has no command form (provider-UI clicks, consent screens, minting a secret)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 033c382b-a3de-4840-ae82-2e5d6db0a6b8
  modified: 2026-08-14T20:12:00.922Z
---

Any auth/setup flow: **the agent runs it**. Lucas is asked only for what genuinely cannot be done
from here — a click inside the provider's own UI, picking an account on a consent screen, a secret
minted inside his account. A secret he pastes into the conversation gets stored by the agent
through a builtin pipe (`printf '%s\n' '<secret>' | <tool> auth <alias>`), never as a CLI argument.

**Why:** handing him a command to type is a chore the agent could have absorbed. He made this
correction twice on 2026-08-14 — first for Google OAuth, then for the Notion token: *"run it for
me and ask me to do only what only I myself can do... write it down so we don't have this
discussion again"*. The second time cost a round trip that the first should have prevented, which
is the point: the rule is provider-agnostic, not a per-tool detail.

**How to apply:** it is written into the workspace at `core/tools/SPECS.md` § An auth failure
names its own fix (provider-agnostic paragraph) and `core/SPECS.md` AD-12, and enforced by
`core/tools/test/test_notion.py::test_lucas_is_only_ever_asked_for_what_happens_inside_notion`
— no CLI path may appear above the `AGENT:` line of an instruction. A new provider tool inherits
this without re-litigating it. Related: [[feedback-provider-agnostic-naming]], [[project-wos-fanout-split]].
