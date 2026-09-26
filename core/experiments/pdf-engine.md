# pdf-engine
> Which engine turns our real PDFs into markdown with the most of their words, their tables and their figures, at what cost?

## Method

`core/run tools/pdf/bench/engines.py tmp/pdf-bench/corpus` — every PDF in the folder through the production worker ([`core/tools/pdf/pdf_engine.py`](../tools/pdf/pdf_engine.py)), one row per PDF × engine.

**Measurement.** Word coverage: the share of the PDF's own words, counted with repeats, that the markdown keeps. The reference is `pdftotext`, or tesseract `por+eng` on pages with no text layer. Also: figures found, tables, seconds, and peak VRAM above idle. Corpus: 8 real PDFs (c1 resolution, c2 DOU, c3 law, c4 two-column paper, c5 scan, c6 bylaws, c7 floor plan, c8 slides), kept local because some are private.

## Results

| Date | Arm | Coverage (7 with text) | Scan (c5) | Tables | s / PDF | VRAM | Verdict |
|---|---|---|---|---|---|---|---|
| 2026-09-25 | docling 2.130.0 (CLI) | 0.92–1.00 | 0.92, accents right | 16 | 13–55 | 1.4–2.2 GB | main engine |
| 2026-09-25 | pymupdf4llm 1.28.2 | ≈1.00 | 0.74 (English-only OCR) | — | seconds, CPU | 0 | fast path |
| 2026-09-25 | pdftotext (baseline) | 0.97–1.00 | 0.00 | 0 | <0.1 | 0 | reference only |
| 2026-09-25 | opendataloader | 0.00–1.00 | 0.00 | 0 | 0.3–2.3 | 0 | cut: refused c1 (broken xref), 0 on the scan |
| 2026-09-25 | Marker v2 (fast) | 0.00 on 6 of 8 | 0.00 | 0 | 9–320 | ≤1.1 GB | cut: needs Docker + vLLM |
| 2026-09-25 | MinerU 4 | 0.00 on 8 of 8 | 0.00 | 0 | — | — | cut: needs a separate parse server |

| 2026-09-26 | docling 2.130.0 (worker, instrument above) | 0.92–1.00, c8 0.57 | 0.92 | 16 | 13–92 | 0.8–1.4 GB | c8 is the reference, not the engine: see Limitations |
| 2026-09-26 | pymupdf4llm 1.28.2 + pymupdf-layout (worker) | 0.95–1.00, c8 0.83 | 0.94 (RapidOCR) | 7 | 4–79 | 0–0.7 GB | its scan reading caught up; still no tables on c6 |

The 2026-09-25 rows came from the Phase 0 harness in `tmp/pdf-bench/engines.py`, which ran the docling CLI and not the worker. Rows from the instrument above are appended under the same columns.

## What changed

`core/tools/pdf/` was built with two leaves: `docling` is the default and `pymupdf` is the CPU path. The PDF branch of `core/tools/paper/parse` (pdftotext + tesseract) was deleted. Marker, MinerU and opendataloader were cut, and its ref left `core/refs/REFS.md`.

## Limitations

- Coverage counts words, not order: two columns read in the wrong order still score 1.00. Reading order was judged by eye on c4, once.
- The reference for a scan is tesseract's reading, so on c5 a coverage number means "agrees with tesseract", not "correct".
- A page with under 10 text-layer words is OCRed whole for the reference, raw and unfiltered, so a slide page contributes image text and junk. The same docling output scores 0.94 against pdftotext alone and 0.57 against that reference on c8. The twin adds its figures' OCR to what it counts, which only partly closes the gap, so slide decks get flagged `needs_review` conservatively.
- "Tables" counts markdown table blocks; nobody checked whether their cells are right.
- One machine (RTX 3050 6 GB laptop), one corpus of 8, one run per cell.
