# checks
> Coverage for `core/hooks/checks/`: the standalone blocking checks the commit and edit hooks run.

Two clusters, and each is the seam that put it here. The heredoc gate and the interpreter-heredoc
bug share a runner — one is the rule, the other is the shell shape that walked past it. The
issues-gate trio shares `issues_gate_harness.py`, a throwaway repo carrying an `ISSUES.md`: the
duplication gate refused the second inline copy, which is why the harness exists at all.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`issues_gate_harness.py`](issues_gate_harness.py) | [`issues_gate_harness.pyi`](issues_gate_harness.pyi) | `repo_with`, `edit_issue`, `spec_file` | Shared harness for the issues-gate tests: a throwaway repo with an ISSUES.md, and the gate run over an Edit payload the way the hook protocol delivers it. One copy, two consumers — the duplication gate refused the second inline duplicate. |
| [`test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.py`](test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.py) | [`test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.pyi`](test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.pyi) | — | b20260904 regression — a write performed inside an interpreted heredoc body is seen. |
| [`test_b4_gate_messages.py`](test_b4_gate_messages.py) | [`test_b4_gate_messages.pyi`](test_b4_gate_messages.pyi) | — | T0: a hook must speak on the channel its class is read on. Two mirrored rules, one subject. |
| [`test_b7_durable_bug_slugs.py`](test_b7_durable_bug_slugs.py) | [`test_b7_durable_bug_slugs.pyi`](test_b7_durable_bug_slugs.pyi) | — | B7 regression — a bug id is a durable slug, and never borrowed. Ids here used to be positional; completion deleted them and every close renumbered, so a citation of "B6" resolved to a bug that no longer was the one meant (the ZCode trust gate citation was the sighting). Since 2026-08-31 new ids are slugs, `b<YYYYMMDD>-<slug>`; a numeric id dies with its fix. The gate matches ids to specs across the hyphen/underscore seam — a slug id and its test_b<...> file name are the same string in two notations — and an id ends at a non-alphanumeric boundary, so b1 never borrows b19's proof. |
| [`test_heredoc_gate.py`](test_heredoc_gate.py) | [`test_heredoc_gate.pyi`](test_heredoc_gate.pyi) | `run` | T0 the heredoc gate: a shell write to a workspace file must not walk past the file gates. |
| [`test_issues_gate_removal.py`](test_issues_gate_removal.py) | [`test_issues_gate_removal.pyi`](test_issues_gate_removal.pyi) | — | Regression — the issues gate reads removals, not only FIXED flips. A session deleted four fixed bug sections and one OPEN one from the workspace ISSUES.md; the gate only fired on the literal word FIXED, so an open bug (B4) left the ledger without a fix or a spec. Since 2026-08-31 a section may not leave ISSUES.md — by deletion or by a FIXED flip — without a matching regression spec, and a spec for B19 does not pay B1's debt: the id ends at the name boundary. |
<!-- routing:end -->
