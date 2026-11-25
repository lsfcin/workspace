# google
> T1 coverage for the Google-backed tools and the auth they share: what a person addresses must be what the API receives, and a dead token must hand back a runnable fix. No network.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_docs.py`](test_docs.py) | [`test_docs.pyi`](test_docs.pyi) | `paragraph` | T1 docs: an index a document reports must still mean that place when the edit is applied. |
| [`test_forms.py`](test_forms.py) | [`test_forms.pyi`](test_forms.pyi) | — | T1 forms: a form written as JSON must reach the API as the form that was written. |
| [`test_gauth.py`](test_gauth.py) | [`test_gauth.pyi`](test_gauth.pyi) | `accounts`, `consent` | T1 auth recovery: a dead Google token must hand Lucas a runnable fix, not a traceback. |
| [`test_sheets.py`](test_sheets.py) | [`test_sheets.pyi`](test_sheets.pyi) | `rng` | T1 sheets: a cell addressed the way a person reads it must reach the API as that same cell, and a format spec must change only what it names. |
| [`test_slides.py`](test_slides.py) | [`test_slides.pyi`](test_slides.pyi) | — | T1 slides: the geometry a deck reports must be the geometry the write path accepts. |
<!-- routing:end -->
