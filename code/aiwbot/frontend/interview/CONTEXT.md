# interview
> The agent asking Lucas a question mid-turn: the broker, its transport, and the bubble it draws.
> spec: ../SPECS.md

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`__init__.py`](__init__.py) | — | — | **facade** — __init__.py — facade: the agent asking Lucas a question mid-turn: the broker, its transport, and the bubble it draws. |
| [`ask.py`](ask.py) | [`ask.pyi`](ask.pyi) | `new_token`, `register`, `unregister`, `question_of`, `answer` | ask.py — the bot side of ask_user: hold a running turn open on a question until Lucas answers. The agent's tool call blocks inside the daemon (askserver hands it here), so an answer resumes the SAME turn rather than starting a new one — that is the whole point of the MCP round trip. |
| [`askserver.py`](askserver.py) | [`askserver.pyi`](askserver.pyi) | `url`, `port`, `handle_rpc`, `start` | askserver.py — the daemon's own MCP server: one HTTP endpoint per live turn, JSON-RPC by hand. linuz90's ask_user works because the SDK runs the agent IN-process; aiwbot drives a subprocess CLI, so a stdio MCP server would be a child of that CLI and could never reach the bot's Telegram state. Hosting the server here inverts it: the CLI is pointed at the… |
| [`askshape.py`](askshape.py) | [`askshape.pyi`](askshape.pyi) | `markup`, `bubble_text`, `answer_note`, `close` | askshape.py — what a question LOOKS like in the chat: its bubble, its keys, and how it closes. Split out of ask.py when registering the answer pushed that file past the size gate. The line the cut follows is the one the gate exposed: ask.py is the broker (tokens, futures, who is waiting), and this is the view (what Lucas reads and taps). Nothing here knows… |
<!-- routing:end -->
