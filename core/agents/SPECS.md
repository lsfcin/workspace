# Agents — Specs
> How a worker runs on another harness, and the traps each call has.

**A worker can run on another harness, from any harness, through bash: prompt in, one file out, read-only.** An outside panel is one call, `core/run tools/delegate/ask --out <file> <prompt>`, which walks the chain declared in [`core/workers.txt`](../workers.txt) and skips a model that gave no verdict; `--list` shows every worker with its live check and call stats. Each worker's id is its row's `id` there; what its model can do is [`core/models.txt`](../models.txt). The spawner writes files from the output, never the worker. One row below per harness in `core/workers.txt`, held by a test.

| Harness | Call (verified 2026-10-19 unless dated) | Traps |
|---|---|---|
| Codex (GPT) | `codex exec -s read-only -m <id> -C <workspace> --ephemeral -o <out> "<prompt>" < /dev/null` | the binary ships inside the ChatGPT desktop app's `resources/`, off PATH; without `< /dev/null` it waits on stdin; `-s read-only` reads the tree and writes nothing; refuses to generate or rank political persuasion aimed at a voter group (6 of 9 generators and the judge, 2026-10-19), and offers source, clarity and feasibility checks instead; `-c tools.web_search=true` makes it a working fact-checker with primary URLs |
| Codex with Google auth | same call with `-s workspace-write -c sandbox_workspace_write.network_access=true --add-dir ~/.config/workspace-<service>` in place of `-s read-only` (verified 2026-10-26) | `read-only` cuts the network and the token refresh's write; a token expired outside the sandbox still needs `auth <alias> --reauth` from the spawner |
| agy (Gemini) | `agy --disable-slash-commands --model <id> -p "<prompt with the files inlined>"` | model before prompt; headless needs no tools; `--dangerously-skip-permissions` is refused by Claude Code's auto-mode classifier; `agy models` lists ids and says whether it is logged in |
| OpenCode (DeepSeek, GLM) | `opencode run --pure --format json -m <id> "<prompt>" < /dev/null` (verified 2026-11-20) | the answer is the `text` events of the JSON stream; the free GLM returned a server error on every call (2026-11-20) |
| Ollama (local) | `ollama run <id> "<prompt>"` (2026-11-20) | text only, no tools; a 9B model describes and does not judge |
| Claude Code | `claude -p "<prompt>"` | the host harness: `core/tools/workers.py` has no adapter for it; spends the quota the other calls exist to save |
