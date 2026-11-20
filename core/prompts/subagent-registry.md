# subagent-registry
> Execute v0 of ROADMAP.md § Workers: one call module, model ids out of code, a declared worker catalog with a live check, panel roles, one AGENTS.md line, a shim-reach test. Delete when v0 lands; v1 and v2 stay in the ROADMAP item.

Level: high. Language with Lucas: pt-br. Designed and approved 2026-11-20 (plan, audit and both panel verdicts in that session). Ask Lucas only about what is not settled below, with the panel's verdict beside each option.

## Why, in Lucas's order (2026-11-20)
Quality (panels, opposing and mediating subagents, research, summarizers), then saving the Claude Code limit (local models, tools, hooks), then provider independence, then the "infinite use" harness; speed, disk and RAM cut any option that breaks them. Delegated work is 2.5% of spend (`core/experiments/delegation.md`), so the gain is quality and quota spread, not the delegated bill.

## What the audit found
- Two independent vendor callers: `core/tools/panel/ask` and `core/tools/describe.py` (own agy call with `--dangerously-skip-permissions`, `which` without the app-path fallback, its own `claude -p` and ollama call).
- Model ids outside `core/tools/wos/levels`: `panel/ask:64,80-82`, `core/agents/SPECS.md:8`, `wos/session/session_cost.py:25`, `flows/craft/routing.md:117`, `flows/craft/runtimes.md:54` (stale Claude versions). `wos/levels` maps Claude only; its `CODEX` maps effort, not models.
- `core/features.txt:159` claims levels renders `.opencode/agents`; it does not. `harnesses.txt` lacks copilot.
- No test proves a shim reaches the panel. Installed: codex 0.167 at `/usr/lib/chatgpt/resources/codex` (off PATH), agy 1.5.10, opencode `~/.opencode/bin`, ollama 0.24 (`qwen3.5:9b`, `qwen3:4b`, `gemma3:4b`, `qwen2.5:7b`), zcode without a documented headless run.

## Decided
- Catalog: `core/workers.txt`, TSV, declared by hand (worker, harness, level, strength, weakness, cost class, mode, help-verified version, call-verified version, date). A live check (binary, login, model list) runs on demand and is never committed.
- `panel/` becomes `core/tools/workers/` in v1; v0 keeps the `panel/ask` entrypoint and moves the shared code.
- Robustness, in the panel's order: machine output only (`codex exec --json` / `-o`, `claude -p --output-format json`; keep stderr) → zero-token `--help` check in verify-fast → error classes as data per provider, with `unknown`, never "quota" by default. Plus: fake executables with recorded answers for offline tests, one normalized result contract, kill the process tree on timeout, a worker with a proven break leaves the chain until re-verified.

## Deliverable
1. **One call module** used by `panel/ask` and `describe.py`: resolve, call, classify (missing / no-login / quota / timeout / unknown / ok). Drop agy's `--dangerously-skip-permissions`.
2. **Ids from adapters** in `core/tools/wos/levels` (`CODEX`, `AGY`, `OLLAMA`: level → id or alias); fix the stale ids listed above; fix `features.txt:159`.
3. **`core/workers.txt`** + `core/run tools/panel/ask --list` (catalog joined with the live check) + `--check` (catalog names a worker whose binary or flags are gone).
4. **Panel roles**: `--role advocate|opponent|mediator|summarizer`, one short template each; the debate is two vendors in opposite roles and a third mediating.
5. **One norm** in `core/norms/` that generates the AGENTS.md line: outside workers exist (GPT, Gemini, local), `core/run tools/panel/ask --list`, never mandatory.
6. **Cut** from `core/agents/SPECS.md` whatever the catalog now holds.
7. **Test** in `core/tools/test/workspace/shims/`: from each harness in `harnesses.txt`, the shim's environment reaches `panel/ask --help` and finds codex off PATH. It must fail with the app-path fallback removed.
8. **Telemetry**: each call logs who answered, duration and the miss reason.

Done when: verify-fast green; zero model ids outside `wos/levels` (`entropy_vendor`); `panel/ask --only codex` answers with an id read from the adapter; the new shim test fails when it should.
