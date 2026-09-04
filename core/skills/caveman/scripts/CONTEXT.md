# scripts
> Compression CLI behind `/caveman compress <file>` — detect file type, call the model, validate, retry. Upstream-synced
> (adapted, not verbatim).

Run from the parent directory: `python3 -m scripts <absolute-filepath>`.

Third-party code synced from upstream — attribution in [`../CONTEXT.md`](../CONTEXT.md). It
**complies with workspace rules** like first-class code: there is **no `.vendor` exemption** (one
was tried and rejected — see `../SPECS.md` § Local adaptations), so these files were **split to
satisfy the size gate**, not exempted from it. Record any re-split there so the next upstream re-sync
can diff. This package is package-shaped (`__init__.py`), so it carries **no generated `.pyi` stubs** —
they are upstream re-diff noise, and `stubgen` mangles them into a nested `scripts/scripts/` path
(known `post-edit.sh` bug: if an edit regenerates that dir, delete it, do not commit it).

**The pass is ordered so the cheapest step can refuse the expensive one**: detect the file type
locally, spending no model tokens; compress; then validate what the model was forbidden to touch and
cherry-pick fixes, up to two retries. The layering is declared in `__init__.py` — nothing imports
upward.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`__init__.py`](__init__.py) | [`__init__.pyi`](__init__.pyi) | — | **facade** — Caveman compress scripts. |
| [`__main__.py`](__main__.py) | [`__main__.pyi`](__main__.pyi) | — | Package entry point: `python3 -m scripts <filepath>` runs the compression CLI. |
| [`benchmark.py`](benchmark.py) | [`benchmark.pyi`](benchmark.pyi) | `count_tokens`, `benchmark_pair`, `print_table`, `main` | Measures what a compression pass saved: token counts before and after, as a table. |
| [`cli.py`](cli.py) | [`cli.pyi`](cli.pyi) | `print_usage`, `main` | Caveman Compress CLI |
| [`compress.py`](compress.py) | [`compress.pyi`](compress.pyi) | `call_claude`, `compress_file` | Caveman memory compression orchestrator: compress, back up, validate, retry, restore. |
| [`detect.py`](detect.py) | [`detect.pyi`](detect.pyi) | `detect_file_type`, `should_compress` | Detect whether a file is natural language (compressible) or code/config (skip). |
| [`extract.py`](extract.py) | [`extract.pyi`](extract.pyi) | `read_file`, `extract_headings`, `extract_code_blocks`, `extract_urls`, `extract_paths` | Markdown extractors: pull out the structures compression must not disturb. |
| [`prompts.py`](prompts.py) | [`prompts.pyi`](prompts.pyi) | `build_compress_prompt`, `build_fix_prompt` | Prompt bodies for the compress and fix passes — text only, no I/O. |
| [`safety.py`](safety.py) | [`safety.pyi`](safety.pyi) | `is_sensitive_path`, `strip_llm_wrapper` | Refuse-before-read denylist: files that must never be shipped to a third-party API. |
| [`validate.py`](validate.py) | [`validate.pyi`](validate.pyi) | `ValidationResult`, `validate_headings`, `validate_code_blocks`, `validate_urls`, `validate_paths` | Post-compression checks: what the model was forbidden to touch must be identical. |
<!-- routing:end -->
