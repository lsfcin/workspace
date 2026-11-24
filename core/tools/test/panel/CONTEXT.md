# panel
> T1 unit tests for the panel tool. Every model is faked: no network, no quota.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_b20261120_classify_reads_answer_as_quota.py`](test_b20261120_classify_reads_answer_as_quota.py) | [`test_b20261120_classify_reads_answer_as_quota.pyi`](test_b20261120_classify_reads_answer_as_quota.pyi) | — | T1 regression b20261120-classify-reads-answer-as-quota: a clean, long answer that talks about quota or login is an answer, not a spent quota. |
| [`test_b20261124_worker_outlives_caller.py`](test_b20261124_worker_outlives_caller.py) | [`test_b20261124_worker_outlives_caller.pyi`](test_b20261124_worker_outlives_caller.pyi) | `fake` | T1 regression b20261124-worker-outlives-caller: a worker and everything it spawned die with its caller or at its deadline, and no worker starts when the machine has no memory to give it. |
| [`test_catalog.py`](test_catalog.py) | [`test_catalog.pyi`](test_catalog.pyi) | `unknown_models` | T0 the worker catalog: core/models.txt, core/workers.txt, core/agents/SPECS.md, core/tools/wos/levels and core/flows/craft/routing.md say one thing about which model is reached how, and a quota miss leaves the chain only for a while. |
| [`test_panel.py`](test_panel.py) | [`test_panel.pyi`](test_panel.pyi) | — | T1 panel/ask: a spent quota or a broken call falls to the next model, the first verdict wins, none at all stops with every reason, and a debate never gives two roles to one vendor. Models faked. |
<!-- routing:end -->
