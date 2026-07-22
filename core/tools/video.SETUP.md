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

## M4 — Instagram cookies (login-gated posts)
`video_core._run` auto-attaches `--cookies <path>` when a cookies file exists at
`~/.config/workspace-video/cookies.txt` (Netscape format, outside repo — never gitignore
needed since it's outside `/mnt/workspace`). No file → tool behaves exactly as before.

To populate: export cookies from a logged-in IG session via a browser extension
("Get cookies.txt LOCALLY" or similar), save to that path. Consider a burner account —
this is a manual step, can't be automated headlessly.

Verified failure mode without cookies (2026-07-22): `DbBDnp6DcKV` — "Instagram sent an
empty media response" (login-gated). Retest same URL once cookies.txt exists.

## M4 — L4 visual captioning (pure-visual content, no speech/on-screen text)
`caption_frames()` in `video_media.py`, wired as the `visual` level in `assemble()`
(escalates after OCR fails / with `--level visual` or `full`).

Model: `Qwen/Qwen3-VL-2B-Instruct` (Apache-2.0), natively supported by `transformers`
(`Qwen3VLForConditionalGeneration` — no `trust_remote_code`, so it won't break when the
shared workspace venv's `transformers` gets upgraded by another tool).

Rejected: `moondream2` / `moondream-2b-*-4bit` — smaller (2.3-4GB VRAM vs Qwen3-VL's
~4.3GB) but both revisions' `trust_remote_code` custom modeling files are already broken
by workspace's `transformers==5.9.0` (API drift: `int4_weight_only` removed from
`torchao`, `all_tied_weights_keys` renamed upstream). Not worth chasing pinned-version
compat in a shared venv other tools also upgrade.

Deps (already in venv as of 2026-07-22, only `accelerate`/`torchao` were missing):
```bash
.venv/bin/pip install accelerate      # required for device_map=
```
`torch`, `transformers`, `pillow` already present (whisper/general deps).

Measured on RTX 3050 6GB Laptop: ~4.3GB VRAM peak, fp16, ~1.7s/frame after model load
(first load downloads ~4GB weights, cached after in `~/.cache/huggingface`). Model is
config data (`model_id` param), swap freely.

## Deferred (M4 remaining)
- relevance() — local sentence-transformers embeddings vs brain/GOALS.md.
- /inbox auto-route on video links.

## Test
```bash
.venv/bin/pytest core/tools/test/ -m "not network"   # T0+T1, no network (verify:fast)
.venv/bin/pytest core/tools/test/ -m network         # T2, real URLs (on-demand)
```
