# scripts
> Compression CLI behind `/caveman compress <file>` — detect file type, call the model, validate, retry. Vendored verbatim.

Run from the parent directory: `python3 -m scripts <absolute-filepath>`.

Third-party code — see [`../.vendor`](../.vendor) and the attribution in
[`../CONTEXT.md`](../CONTEXT.md). Exempt from the workspace size gate; do not split these files
to satisfy the line limit, it would fork them from upstream.

| File | Role |
|------|------|
| `__main__.py` · `cli.py` | entry point and argument handling |
| `detect.py` | file-type detection (no model tokens spent) |
| `compress.py` | the compression pass |
| `validate.py` | post-check; on failure, cherry-picked fixes, up to 2 retries |
| `benchmark.py` | measures the savings |

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`__init__.py`](__init__.py) | — | — | **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — **facade** — ← add first-line comment |
| [`__main__.py`](__main__.py) | — | — | ← add first-line comment |
| [`benchmark.py`](benchmark.py) | — | `count_tokens`, `benchmark_pair`, `print_table`, `main` | ← add first-line comment |
| [`cli.py`](cli.py) | — | `print_usage`, `main` | ← add first-line comment |
| [`compress.py`](compress.py) | — | `call_claude`, `compress_file` | Caveman memory compression orchestrator: compress, back up, validate, retry, restore. |
| [`detect.py`](detect.py) | — | `detect_file_type`, `should_compress` | Detect whether a file is natural language (compressible) or code/config (skip). |
| [`extract.py`](extract.py) | — | `read_file`, `extract_headings`, `extract_code_blocks`, `extract_urls`, `extract_paths` | Markdown extractors: pull out the structures compression must not disturb. |
| [`prompts.py`](prompts.py) | — | `build_compress_prompt`, `build_fix_prompt` | Prompt bodies for the compress and fix passes — text only, no I/O. |
| [`safety.py`](safety.py) | — | `is_sensitive_path`, `strip_llm_wrapper` | Refuse-before-read denylist: files that must never be shipped to a third-party API. |
| [`validate.py`](validate.py) | — | `ValidationResult`, `validate_headings`, `validate_code_blocks`, `validate_urls`, `validate_paths` | Post-compression checks: what the model was forbidden to touch must be identical. |
<!-- routing:end -->
