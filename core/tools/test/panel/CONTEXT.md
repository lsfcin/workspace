# panel
> T1 unit tests for the panel tool. Every model is faked: no network, no quota.

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_b20261120_classify_reads_answer_as_quota.py`](test_b20261120_classify_reads_answer_as_quota.py) | [`test_b20261120_classify_reads_answer_as_quota.pyi`](test_b20261120_classify_reads_answer_as_quota.pyi) | T1 regression b20261120-classify-reads-answer-as-quota: a clean, long answer that talks about quota or login is an answer, not a spent quota. |
| [`test_panel.py`](test_panel.py) | [`test_panel.pyi`](test_panel.pyi) | T1 panel/ask: a spent quota or a broken call falls to the next model, the first verdict wins, none at all stops with every reason, and a debate never gives two roles to one vendor. Models faked. |
<!-- routing:end -->
