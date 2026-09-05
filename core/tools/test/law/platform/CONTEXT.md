# platform
> The platform seam's coverage: the one module allowed to know what an operating system is, and
> the credential-tightness ruling that rides on it.

Split from [`../`](../CONTEXT.md) 2026-08-31 at the fanout signal, on a seam the directory's own
head already names: the file-shape law (what a file is, what a name may be) is a different
responsibility from what machine this is. The regression spec for the token modes lives beside the
seam tests because the ruling is about the seam's answer, not about Google.

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_b11_token_modes.py`](test_b11_token_modes.py) | [`test_b11_token_modes.pyi`](test_b11_token_modes.pyi) | B11 regression — a credential file is written tight, by the writer, on every system. The Google token directories landed at 775 with 664 token files: any local account could read a live refresh token, and nothing in the workspace set a mode when it wrote. platform_law owns the seam (secure_dir / secure_file) and gauth applies it where it writes. Ruling 2026-08-31 (Lucas): tightening must not break multi-user local use — tokens live per-HOME, so another account's own tool runs keep working; what stops is every other account reading THIS one's. |
| [`test_b20260901_a_git_symlink_is_a_text_file_on_windows.py`](test_b20260901_a_git_symlink_is_a_text_file_on_windows.py) | [`test_b20260901_a_git_symlink_is_a_text_file_on_windows.pyi`](test_b20260901_a_git_symlink_is_a_text_file_on_windows.pyi) | b20260901 regression — no tracked file in this workspace is a git symlink. |
| [`test_b20260901_one_answers_file_is_shared_by_two_operating_systems.py`](test_b20260901_one_answers_file_is_shared_by_two_operating_systems.py) | [`test_b20260901_one_answers_file_is_shared_by_two_operating_systems.pyi`](test_b20260901_one_answers_file_is_shared_by_two_operating_systems.pyi) | b20260901 regression — this machine's answers override the shared ones and never travel. |
| [`test_platform_law.py`](test_platform_law.py) | [`test_platform_law.pyi`](test_platform_law.pyi) | T0/T1 the platform seam: the one module allowed to know what an operating system is, and until now the only law module with no test of its own. |
<!-- routing:end -->
