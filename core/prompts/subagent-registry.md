# subagent-registry
> Every harness knows, without searching, which outside workers it can call, what each is good and bad at, and the one command that calls it. Audit what exists, then redesign it. Delete when the deliverable lands.

Level: high. Language with Lucas: pt-br. Interview him before any design choice, with the outside panel's verdict beside each option (`core/run tools/panel/ask`).

## Why (Lucas, 2026-11-19)
Sessions keep saying "codex is not installed". It is, inside the ChatGPT desktop app and off PATH, and `core/run tools/panel/ask` already finds it. The norm named the tool only on 2026-11-19, after the fix spent two days stranded on an unmerged branch. Lucas also does not know how the panel is wired today, and wants to understand it.

## What exists, scattered
- `core/tools/panel/ask`: a read-only verdict, falling back Codex GPT → agy Gemini Argon → Flash.
- `core/agents/SPECS.md`: the call table, with the traps of each harness (flags, stdin, sandbox).
- `core/levels.txt` + `core/tools/wos/levels`: which concrete model fills a level, per harness. That is the only place a model id may appear.
- `core/harnesses.txt`: which harnesses are supported, and where their mirrors live.
- The `core/hooks/{codex,copilot,antigravity}/` shims.

## Deliverable
1. **Audit, written for Lucas.** How a call reaches each vendor today, where the knowledge lives, what is duplicated, and what is stale. Cover Claude Code, Codex, agy/Antigravity, opencode and ZCode.
2. **One table**: each worker, its strengths and weaknesses, its cost and quota, and its exact call. Generated from the installed CLIs and model lists (at the close or at session start), so a new model shows up without a session searching for it. It must not load the full context of any session.
3. **One line in AGENTS.md** pointing at the table, so no harness ever forgets that outside workers exist. It makes them easy to reach and never mandatory.
4. **One wrapper** that resolves binary, flags, sandbox and fallback, beyond a read-only verdict (for example, a worker that writes one output file). Prompt slots, so the caller never rebuilds a call by hand.
5. **A test** that fails when any harness shim cannot reach the wrapper.

Cut while doing it: whatever the table makes redundant leaves `core/agents/SPECS.md` (REDUCING IS THE WAY).
