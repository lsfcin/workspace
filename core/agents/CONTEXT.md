# Agents
> Agent definitions; load as system prompt to spawn a specialist worker.

Each file is a complete operating context for one agent role. In Claude Code, spawn a worker by passing the file content as the system prompt via the Agent tool.

**A worker can run on another harness, from any harness, through bash: prompt in, one file out, read-only.** Lucas prefers GPT and spends `gpt-6.1-sol` before any other worker (2026-10-19); the spawner writes files from the output, never the worker.

| Harness | Call (verified 2026-10-19) | Traps |
|---|---|---|
| Codex (GPT) | `/usr/lib/chatgpt/resources/codex exec -s read-only -m gpt-6.1-sol -C /mnt/workspace --ephemeral -o <out> "<prompt>" < /dev/null` | off PATH; without `< /dev/null` it waits on stdin; `-s read-only` reads the tree and writes nothing; refuses to generate or rank political persuasion aimed at a voter group (6 of 9 generators and the judge, 2026-10-19), and offers source, clarity and feasibility checks instead; `-c tools.web_search=true` makes it a working fact-checker with primary URLs |
| agy (Gemini) | `agy --disable-slash-commands --model <id> -p "<prompt with the files inlined>"` | model before prompt; headless needs no tools; `--dangerously-skip-permissions` is refused by Claude Code's auto-mode classifier; `agy models` lists ids and says whether it is logged in |
| Claude Code | `claude -p "<prompt>"` | not run on 2026-10-19; spends Claude quota, the one these calls exist to save |

**One pipeline, in order: `writer` drafts from evidence `researcher` gathered, `verifier` adds the citations afterward, `reviewer` grades the result.** Who each one is, is the routing table's job —
it reads their frontmatter, which is the same text their spawner gets.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`_template.md`](_template.md) | One line — what evidence or output this worker produces. |
| [`lead.md`](lead.md) | Orchestrates research workflows; plans tasks, delegates to worker agents, synthesizes results. |
| [`montador.md`](montador.md) | Cut what a talk does not need and fix its flow — proposes, never destroys: a per-slide cut list, and skips on a copy. |
| [`researcher.md`](researcher.md) | Gather primary evidence across papers, web sources, repos, docs, and local artifacts. |
| [`reviewer.md`](reviewer.md) | Simulate a tough but constructive AI research peer reviewer with inline annotations. |
| [`verifier.md`](verifier.md) | Post-process a draft to add inline citations and verify every source URL. |
| [`writer.md`](writer.md) | Turn research notes into clear, structured briefs and drafts. |
<!-- routing:end -->
