# test
> The verify-fast suite: every Level 0 check plus the tool unit tests. Zero-token, no network.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`chat/`](chat/CONTEXT.md) | T1 coverage for the chat tool: what an audio line must keep, what noise must go, and what must never reach a versioned file. |
| [`delegate/`](delegate/CONTEXT.md) | T1 unit tests for the delegate tool. Every model is faked: no network, no quota. |
| [`files/`](files/CONTEXT.md) | T1 coverage for files and drive sync tooling. |
| [`google/`](google/CONTEXT.md) | T1 coverage for the Google-backed tools and the auth they share: what a person addresses must be what the API receives, and a dead token must hand back a runnable fix. No network. |
| [`law/`](law/CONTEXT.md) | Level 0: what a file is, what a name may be, and how big a session may get. |
| [`pdf/`](pdf/CONTEXT.md) | T1 unit tests for the PDF twin. The PDFs are built in bytes and the engine is faked: no GPU, no network, no model. |
| [`phone/`](phone/CONTEXT.md) | T1 unit tests for the phone tool. adb is faked and the screencaps are built in bytes: no phone, no SDK. |
| [`video/`](video/CONTEXT.md) | T1 unit tests for the video tool. Fixtures live here; network-marked cases are excluded from verify-fast. |
| [`workspace/`](workspace/CONTEXT.md) | Level 0 workspace-wide invariants: pointers resolve, .gitignore self-heals, imports do not shadow. |
| [`wos/`](wos/CONTEXT.md) | What the workspace declares about itself, and what the session-close ritual really does. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`conftest.py`](conftest.py) | [`conftest.pyi`](conftest.pyi) | `floor_of`, `git_lines`, `needs`, `carries`, `pytest_configure` | conftest.py — the one place the suite learns where things are: workspace root, core/tools, and the enforcement layer. Also registers the network marker for the video tests. |
| [`test_audio_learn.py`](test_audio_learn.py) | [`test_audio_learn.pyi`](test_audio_learn.pyi) | — | T1 audio self-learning: temporal correlation, conservative promotion, manual priority |
| [`test_audio_stt.py`](test_audio_stt.py) | [`test_audio_stt.pyi`](test_audio_stt.pyi) | `transcribe` | T1 audio STT: sttd Unix socket protocol, idle unload, client fallback, and refine |
| [`test_b20261128_ibus_deadlock.py`](test_b20261128_ibus_deadlock.py) | [`test_b20261128_ibus_deadlock.pyi`](test_b20261128_ibus_deadlock.pyi) | — | Regression test for b20261128-ibus-deadlock: async engine switch and safe WosDictateEngine fields |
| [`test_b20261128_sttd_memory_retention.py`](test_b20261128_sttd_memory_retention.py) | [`test_b20261128_sttd_memory_retention.pyi`](test_b20261128_sttd_memory_retention.pyi) | — | Regression test for b20261128-sttd-memory-retention: sttd kills worker subprocess on idle/unload |
| [`test_caveman_compress.py`](test_caveman_compress.py) | [`test_caveman_compress.pyi`](test_caveman_compress.pyi) | — | T1 caveman compress: model output reaches disk as a text file, and the default id has one home. |
| [`test_describe.py`](test_describe.py) | [`test_describe.pyi`](test_describe.pyi) | `backends` | T1 describe: an answer that ignores the image's own text is escalated, and a chain that runs out keeps its best answer flagged rather than nothing. Zero-token, no network. |
| [`test_docx_template.py`](test_docx_template.py) | [`test_docx_template.pyi`](test_docx_template.pyi) | — | T1 docx template: a filled form reads back as the fields written, with the template's defaults gone and its table found even inside a content control. |
| [`test_links.py`](test_links.py) | [`test_links.pyi`](test_links.pyi) | `mapfile`, `course`, `browser_edit` | T1 links: a short name stays sayable, a private thing never gets one, and a live link never moves. |
| [`test_links_secrets.py`](test_links_secrets.py) | [`test_links_secrets.pyi`](test_links_secrets.pyi) | — | T1 links/cfpages secrets: the delivery roster comes from the panel rows, and a course is never dropped in silence. |
| [`test_notion.py`](test_notion.py) | [`test_notion.pyi`](test_notion.pyi) | `block` | T1 notion: an id survives any form it is pasted in, and a failure hands back a runnable fix. |
| [`test_notion_write.py`](test_notion_write.py) | [`test_notion_write.pyi`](test_notion_write.pyi) | — | T1 notion write: a batch lands whole or not at all, and a link keeps the name it shows. |
| [`test_pptx.py`](test_pptx.py) | [`test_pptx.pyi`](test_pptx.pyi) | — | T1 pptx template: every section becomes a master carrying the same layouts, and every colour stays a theme slot. |
| [`test_pptx_motion.py`](test_pptx_motion.py) | [`test_pptx_motion.pyi`](test_pptx_motion.pyi) | — | T1 pptx motion: a build shows what it means to show, lint names what a room would see wrong, and flatten turns every click into a page. |
| [`test_secret_law.py`](test_secret_law.py) | [`test_secret_law.pyi`](test_secret_law.pyi) | `scan` | T1 secret law: every shape of credential is found, and the near-misses that would make anyone switch the gate off are not. Zero-token, no network. |
<!-- routing:end -->
