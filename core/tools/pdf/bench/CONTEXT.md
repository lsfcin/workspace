# bench
> The two bake-offs behind the PDF twin, re-runnable: which engine converts, and which describer reads figures. Results live in core/experiments/.

Both scripts measure the production path — the engine worker and the describer backends the leaves use — so a number here is a number about the tool. Neither ships a corpus: the PDFs, the figure images and the answer keys are real and some are private, so they are passed in as a folder and never versioned.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`describers.py`](describers.py) | [`describers.pyi`](describers.pyi) | `hits`, `run`, `main` | Usage: core/run tools/pdf/bench/describers.py <set-dir> [--describers agy,claude,local] — describe every image in a set with each describer ALONE (no chain), then score facts hit against <set-dir>/keys.json and the OCR cross-check; one TSV row per image×describer and a total |
| [`engines.py`](engines.py) | [`engines.pyi`](engines.pyi) | `measure`, `main` | Usage: core/run tools/pdf/bench/engines.py <corpus-dir> [--engines docling,pymupdf] — convert every PDF in a folder with each engine through the production worker; one TSV row per PDF×engine: coverage, figures, tables, seconds, peak VRAM |
| [`relevance_sheet.py`](relevance_sheet.py) | [`relevance_sheet.pyi`](relevance_sheet.pyi) | `main` | Usage: core/run tools/pdf/bench/relevance_sheet.py <out-dir> <profile-dir> — one HTML page of every figure in <out-dir>/signals.tsv: the crop, its label, what its twin said, and the verdict the profile's weights give it, the disagreements first |
| [`relevance_signals.py`](relevance_signals.py) | [`relevance_signals.pyi`](relevance_signals.pyi) | `described`, `rows`, `main` | Usage: core/run tools/pdf/bench/relevance_signals.py <listing> <out-dir> [--relevance <profile-dir>] — every figure of every PDF in the listing, through the production engine, as one TSV row of pdf_relevance signals, with its crop and the description its twin already holds |
| [`relevance_train.py`](relevance_train.py) | [`relevance_train.pyi`](relevance_train.pyi) | `labelled`, `out_of_fold`, `bar`, `fit_all`, `write` | Usage: core/run tools/pdf/bench/relevance_train.py <out-dir> [--recall 0.98] [--write <profile-dir>] — fit pdf_relevance's weights on <out-dir>/signals.tsv and labels.tsv, leaving one document out at a time, and print what the bar would skip and miss |
<!-- routing:end -->
