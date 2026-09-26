# vlm-describe
> Which model describes a PDF figure with the most of its facts and the fewest inventions, and can a free check tell a bad description from a good one?

## Method

`core/run tools/pdf/bench/describers.py tmp/pdf-bench/vlm/set --describers agy,claude,local` — each describer alone on every image, through the production backends in [`core/tools/describe.py`](../tools/describe.py), with the figure prompt `describe.FIGURE_PROMPT`.

**Measurement.** Facts hit: an image's answer key (`keys.json` beside the images) lists facts as regex alternatives, and a fact counts when any alternative appears in the description. Seconds per image. The free check, the OCR cross-check, is the share of the figure's own tesseract words (≥4 letters, confidence ≥60) that the description contains, and a figure is flagged below 0.5. Set: 14 figures cut from our PDFs, easy to hard (photo, logo, chart, flowchart, diagrams, heatmap, graph, equations, table, render grid, floor plan, scanned page), 189 facts in total. The set stays local because the images come from private PDFs.

## Results

| Date | Describer | Facts hit / 189 | s / image | Notes |
|---|---|---|---|---|
| 2026-09-25 | agy (Gemini 3.8 Flash) | 188 | 20–394 | the floor plan took 394 s |
| 2026-09-25 | claude sonnet | 187 | 12–37 | |
| 2026-09-25 | qwen3.5:9b (ollama, part CPU) | 180 | 11–169 | misses by omission, never invents |
| 2026-09-25 | claude haiku | 173 | 13–28 | |
| 2026-09-25 | Qwen3-VL-2B (transformers) | 159 | 3–63 | invented a floor-plan legend |
| 2026-09-25 | gemma3:4b | 53 | 3–43 | invents whole figures; cut |
| 2026-09-25 | qwen3-vl:8b | — | ~110 | returns empty (thinking); cut |
| 2026-09-25 | OCR cross-check, raw tesseract | flagged every invention and every empty answer | — | on qwen3.5, flagged only the floor plan |
| 2026-09-25 | cross-check on 25 real figures (c4, c5), raw tesseract | 2 flagged, both false: agy's description was right, and the OCR was junk from small type | — | fixed: words need confidence ≥60, best of scales 1×/2×/3× |
| 2026-09-25 | same 25 figures, filtered OCR | 0 flagged; the 5 checkable figures overlap 0.86–1.00 | ~1 s OCR | |

The first seven rows came from the Phase 0 harness in `tmp/pdf-bench/vlm/bench.py`. The last two are hand-checks of the production cross-check.

## What changed

The describer became a parameter, `--describer agy|local|claude`. **Lucas chose agy as the default** (cheap for him, best quality), with claude as the fallback. The cross-check runs on every describer: an answer below 0.5 goes to the next describer in the chain, and when the chain runs out the twin gets `needs_review`. The video tool moved onto the same describer, and its Qwen3-VL-2B left, together with torch, transformers and accelerate in `.venv`.

## Limitations

- The answer keys were written by Claude, the same vendor as one of the arms. A key can miss a fact that none of the describers mention.
- Images larger than 1920 px on the long side were shrunk to that before describing.
- The cross-check can only judge figures with at least 3 OCR words of 4+ letters. A photo or a pure diagram is never flagged, whatever the description says.
- One run per cell; agy's latency varies by an order of magnitude between runs.
