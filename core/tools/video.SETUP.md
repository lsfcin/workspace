# video tool — setup
> Dependencies for `core/tools/video` (link → navigable text). See goal workspace-os / TODO:121.

## Installed (M1 — L0 metadata + L1 captions)
- `yt-dlp` — in workspace venv: `.venv/bin/pip install yt-dlp` ✓ (2026.07.04)

## Pending (M2 speech + M3 OCR) — need system installs (sudo)
```bash
sudo apt-get install -y ffmpeg tesseract-ocr tesseract-ocr-por
.venv/bin/pip install faster-whisper pytesseract
```
- `ffmpeg` — audio extraction (M2) + frame sampling (M3)
- `faster-whisper` — local transcription backend (model name is config data, default `base`)
- `tesseract-ocr` + `-por` — burned-in text OCR (M3), Portuguese language pack

## Deferred (M4)
- local VLM (moondream / `models/`) for pure-visual captioning + relevance embeddings.

## Test
```bash
.venv/bin/pytest core/tools/test/ -m "not network"   # T0+T1, no network (verify:fast)
.venv/bin/pytest core/tools/test/ -m network         # T2, real URLs (on-demand)
```
