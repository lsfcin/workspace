# select
> The picker keyboards: which grid a tap opens, and what one tap costs.
> spec: none

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`__init__.py`](__init__.py) | — | — | **facade** — __init__.py — marks tests/select as a package. |
| [`test_f3c_tap_latency.py`](test_f3c_tap_latency.py) | [`test_f3c_tap_latency.pyi`](test_f3c_tap_latency.pyi) | `answer`, `edit_message_reply_markup` | test_f3c_tap_latency.py — F3c: a panel tap costs ONE Telegram round trip, not two or three. The bot-side work was measured at under 1 ms on every warm path, so the felt latency is round trips (222 ms median each from Lucas's machine). These assert the count, which is the only part we control — a client renders an inline keyboard from server state, so one is… |
| [`test_panel.py`](test_panel.py) | [`test_panel.pyi`](test_panel.pyi) | `answer`, `edit_message_reply_markup` | test_panel.py — free unit test: panel effects — scopes, applying a choice, hidden dims. |
| [`test_panelmenu.py`](test_panelmenu.py) | [`test_panelmenu.pyi`](test_panelmenu.pyi) | — | test_panelmenu.py — free unit test: panel layout — rows, controls, ordering, paging. |
<!-- routing:end -->
