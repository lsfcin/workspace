# test
> The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token, no network.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`law/`](law/CONTEXT.md) | Tier 0: what a file is, what a name may be, and how big a session may get. |
| [`video/`](video/CONTEXT.md) | T1 unit tests for the video tool. Fixtures live here; network-marked cases are excluded from verify-fast. |
| [`workspace/`](workspace/CONTEXT.md) | Tier 0 workspace-wide invariants: pointers resolve, .gitignore self-heals, imports do not shadow. |
| [`wos/`](wos/CONTEXT.md) | What the workspace declares about itself, and what the session-close ritual really does. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`conftest.py`](conftest.py) | [`conftest.pyi`](conftest.pyi) | `pytest_configure` | conftest.py — the one place the suite learns where things are: workspace root, core/tools, and the enforcement layer. Also registers the network marker for the video tests. |
| [`test_docs.py`](test_docs.py) | [`test_docs.pyi`](test_docs.pyi) | `paragraph` | T1 docs: an index a document reports must still mean that place when the edit is applied. |
| [`test_forms.py`](test_forms.py) | [`test_forms.pyi`](test_forms.pyi) | — | T1 forms: a form written as JSON must reach the API as the form that was written. |
| [`test_gauth.py`](test_gauth.py) | [`test_gauth.pyi`](test_gauth.pyi) | `accounts` | T1 auth recovery: a dead Google token must hand Lucas a runnable fix, not a traceback. |
| [`test_notion.py`](test_notion.py) | [`test_notion.pyi`](test_notion.pyi) | `block` | T1 notion: an id survives any form it is pasted in, and a failure hands back a runnable fix. |
| [`test_notion_write.py`](test_notion_write.py) | [`test_notion_write.pyi`](test_notion_write.pyi) | — | T1 notion write: a batch lands whole or not at all, and a link keeps the name it shows. |
| [`test_slides.py`](test_slides.py) | [`test_slides.pyi`](test_slides.pyi) | — | T1 slides: the geometry a deck reports must be the geometry the write path accepts. |
<!-- routing:end -->
