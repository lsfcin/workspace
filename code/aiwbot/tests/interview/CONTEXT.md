# interview
> The agent asking Lucas a question mid-turn: the broker, the transport, and the bubble it draws.
> spec: none

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`__init__.py`](__init__.py) | — | **facade** — __init__.py — marks tests/interview as a package. |
| [`test_f4_ask.py`](test_f4_ask.py) | [`test_f4_ask.pyi`](test_f4_ask.pyi) | test_f4_ask.py — F4 Stage 4: the broker. One asyncio.Future per question, the chat UX that resolves it (tap or reply), and the rule Lucas set — a wait always ends in TEXT the agent can act on, never in an MCP error, because an error aborts the turn and loses its work. |
| [`test_f4_ask_wiring.py`](test_f4_ask_wiring.py) | [`test_f4_ask_wiring.pyi`](test_f4_ask_wiring.pyi) | test_f4_ask_wiring.py — F4 Stage 4: the transport and the CLI wiring around the broker. Every constant asserted here was measured against the real binary on 2026-07-27 rather than read off documentation: `claude -p` re-runs `initialize` several times per invocation, kills a tool call at 60 s unless MCP_TOOL_TIMEOUT lifts it, and refuses MCP tools outright in… |
| [`test_f6_interview_shape.py`](test_f6_interview_shape.py) | [`test_f6_interview_shape.pyi`](test_f6_interview_shape.pyi) | test_f6_interview_shape.py — what the chat looks like when the agent interviews Lucas mid-turn (2026-07-29, from his first real interview). A question is its own message, so everything the agent writes after it has to land BELOW it — the answer to a question must never appear above the question — and the status line must not sit there claiming work that is… |
| [`test_f7_opencode_ask.py`](test_f7_opencode_ask.py) | [`test_f7_opencode_ask.pyi`](test_f7_opencode_ask.pyi) | test_f7_opencode_ask.py — opencode parity: the ask transport and the retry vocabulary. Every constant here was measured against opencode 1.18.7 on 2026-07-29 (SPECS AD-31), the way AD-27 was measured for claude: `opencode run` has NO MCP flag, the config rides in OPENCODE_CONFIG_CONTENT, and the tool call dies at ~60 s unless the per-server `timeout` lifts… |
| [`test_f8_ask_answer_shape.py`](test_f8_ask_answer_shape.py) | [`test_f8_ask_answer_shape.pyi`](test_f8_ask_answer_shape.pyi) | test_f8_ask_answer_shape.py — what an interview looks like in the chat, from Lucas reading a real one on his phone (2026-07-29): the option buttons were cut off ("Cada mensagem vira sessão nov…"), and once he answered, nothing in the chat said what he had answered. |
<!-- routing:end -->
