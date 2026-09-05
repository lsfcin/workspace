# checks
> Standalone blocking checks the commit and edit hooks run.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`check-duplication.py`](check-duplication.py) | [`check-duplication.pyi`](check-duplication.pyi) | `main` | Pre-commit duplication gate — jscpd over the repo; blocks when a clone involves a staged file. No baseline: touching a file with a legacy clone means extracting it now (ROADMAP-verify.md W2). |
| [`citation-gate.py`](citation-gate.py) | [`citation-gate.pyi`](citation-gate.pyi) | `citation_exempt_paths`, `staged_files`, `citation_hits`, `main` | Tier 0: a roadmap item number is not a citable identifier outside the roadmap family. |
| [`heredoc-gate.py`](heredoc-gate.py) | [`heredoc-gate.pyi`](heredoc-gate.pyi) | `targets`, `body_writes`, `in_workspace`, `written_paths`, `main` | PreToolUse: Bash — a shell heredoc that writes a workspace file meets none of the file gates. |
| [`issues-gate.py`](issues-gate.py) | [`issues-gate.pyi`](issues-gate.pyi) | `bug_ids`, `fixed_ids`, `repo_root`, `has_spec`, `main` | PreToolUse: Edit|Write on ISSUES.md — the FIXED gate. A bug may not leave this file without executable proof: flipping one to FIXED, or deleting its section outright, requires a matching regression spec (a file named *b<N>[_-]* under a test/ directory of this repo). Deleting an open bug used to bypass the flip check — the gate reads the removal too. See ROADMAP-verify.md I2. |
| [`line_counts.py`](line_counts.py) | [`line_counts.pyi`](line_counts.pyi) | `report`, `main` | The line-count gate: warn at 150 code lines, block at 200. |
| [`pre-edit.py`](pre-edit.py) | [`pre-edit.pyi`](pre-edit.pyi) | `block` | PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description. |
| [`type-gate.py`](type-gate.py) | [`type-gate.pyi`](type-gate.pyi) | `check_name`, `failures_for`, `main` | Tier 0 gate (core/SCHEMA.md § The .md type system): a staged file must be a known .md type or a well-shaped instance, must sit where its type is allowed to live, must give the routing table something to write about it, and a CONTEXT.md must not hand-list files. Zero-token, no LLM. |
<!-- routing:end -->
