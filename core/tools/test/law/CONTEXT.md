# law
> Tier 0: what a file is, what a name may be, and how big a session may get.

What stays here is the law **itself** — the definitions every other check reads through, and the
gate that admits a filename. The checks that consume it moved into
[`entropy/`](entropy/CONTEXT.md) on 2026-08-15, so this directory answers *what is legal* and that
one answers *what the tree actually contains*.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`entropy/`](entropy/CONTEXT.md) | What each entropy check counts, and where it must stay silent. **One file per check, not one per module** — so a name here answers to a question, and only sometimes to a file next door. |

| File | Interface | Description |
|------|-----------|-------------|
| [`test_b11_token_modes.py`](test_b11_token_modes.py) | [`test_b11_token_modes.pyi`](test_b11_token_modes.pyi) | B11 regression — a credential file is written tight, by the writer, on every system. The Google token directories landed at 775 with 664 token files: any local account could read a live refresh token, and nothing in the workspace set a mode when it wrote. platform_law owns the seam (secure_dir / secure_file) and gauth applies it where it writes. Ruling 2026-08-31 (Lucas): tightening must not break multi-user local use — tokens live per-HOME, so another account's own tool runs keep working; what stops is every other account reading THIS one's. |
| [`test_citation_gate.py`](test_citation_gate.py) | [`test_citation_gate.pyi`](test_citation_gate.pyi) | T0 roadmap item numbers may not be cited outside a roadmap. Zero-token, runs in verify-fast. |
| [`test_column_cap.py`](test_column_cap.py) | [`test_column_cap.pyi`](test_column_cap.pyi) | T0 column cap: how wide one authored .md line may be, and the three shapes exempt from it. Zero-token, runs in verify-fast. |
| [`test_context_meter.py`](test_context_meter.py) | [`test_context_meter.pyi`](test_context_meter.pyi) | T0 context meter (core/SPECS.md § AD-09): the session-size signal that decides when to hand off. Zero-token, runs in verify-fast. |
| [`test_description_gate.py`](test_description_gate.py) | [`test_description_gate.pyi`](test_description_gate.pyi) | T0 description check: a file this commit adds must be able to describe itself. Zero-token, verify-fast. |
| [`test_file_law.py`](test_file_law.py) | [`test_file_law.pyi`](test_file_law.pyi) | T0 file law (core/hooks/SPECS.md). Zero-token, runs in verify-fast. |
| [`test_platform_law.py`](test_platform_law.py) | [`test_platform_law.pyi`](test_platform_law.pyi) | T0/T1 the platform seam: the one module allowed to know what an operating system is, and until now the only law module with no test of its own. |
| [`test_type_gate.py`](test_type_gate.py) | [`test_type_gate.pyi`](test_type_gate.pyi) | T0 type gate (Tier 0, law in core/SCHEMA.md): the uppercase allowlist. Zero-token, runs in verify-fast. |
<!-- routing:end -->
