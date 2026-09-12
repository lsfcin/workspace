# seam
> The AgentBackend seam: a CLI's output becomes AgentEvents, and a turn's options reach its argv.
> spec: none

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`__init__.py`](__init__.py) | — | — | **facade** — __init__.py — marks tests/seam as a package. |
| [`test_b2_opencode_error.py`](test_b2_opencode_error.py) | [`test_b2_opencode_error.pyi`](test_b2_opencode_error.pyi) | — | test_b2_opencode_error.py — regression spec for [b2]: opencode failures collapsing to the useless "no text event". The fixture is a REAL payload captured off the CLI (b2 asked for exactly that, twice unsuccessfully): `opencode run --format json -m <bogus model>`, which streams a type=error line AND exits 0 — the pair that made the old code fall silent. |
| [`test_b4_opencode_cwd.py`](test_b4_opencode_cwd.py) | [`test_b4_opencode_cwd.pyi`](test_b4_opencode_cwd.pyi) | `communicate` | test_b4_opencode_cwd.py — regression spec for [b4]: turns ran in the daemon's launch directory. Measured live 2026-07-29: `cwd=` on the subprocess is not enough, because opencode trusts `PWD` over `getcwd()` — a daemon started from /home/lucas filed every Telegram opencode session there and pointed its file/shell tools at it, while /resume listed the… |
| [`test_dispatch.py`](test_dispatch.py) | [`test_dispatch.pyi`](test_dispatch.pyi) | — | test_dispatch.py — free unit test: AgentEvent list -> TurnResult, using Phase A fixtures. |
| [`test_parse_claude.py`](test_parse_claude.py) | [`test_parse_claude.pyi`](test_parse_claude.pyi) | — | test_parse_claude.py — free unit test: claude fixture -> normalized AgentEvents satisfy the contract. |
| [`test_parse_opencode.py`](test_parse_opencode.py) | [`test_parse_opencode.pyi`](test_parse_opencode.pyi) | — | test_parse_opencode.py — free unit test: opencode JSONL fixture -> AgentEvents satisfy the contract. |
| [`test_target.py`](test_target.py) | [`test_target.pyi`](test_target.pyi) | — | test_target.py — free unit test: model/effort reach the argv, and each backend's declaration. |
<!-- routing:end -->
