# gates
> What a blocking gate must say, and who it must fire for. Named for `core/hooks/gates/` and
> deliberately wider than it.

**Not a mirror, and the name is the drift.** It also holds the tests for hooks in `read/`, `checks/`,
`git/` and `compact/`; the split that would retire the mismatch is named in
[`test_entropy_fanout.py`](../../law/entropy/test_entropy_fanout.py)'s BASELINE.

The questions here are independent, which is why they are separate files: a hook can block the right
agent for the wrong reason, the wrong agent with a perfect message, or rewrite shell it had no
business touching.

Why each one exists, and the one place a test reads source instead of running it: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Why each hook test exists, and the one structural exception to running the real hook. |
| [`issues_gate_harness.py`](issues_gate_harness.py) | [`issues_gate_harness.pyi`](issues_gate_harness.pyi) | `repo_with`, `edit_issue`, `spec_file` | Shared harness for the issues-gate tests: a throwaway repo with an ISSUES.md, and the gate run over an Edit payload the way the hook protocol delivers it. One copy, two consumers — the duplication gate refused the second inline duplicate. |
| [`test_agent_context.py`](test_agent_context.py) | [`test_agent_context.pyi`](test_agent_context.pyi) | `prompt_id` | T0 the agent-context briefing (core/hooks/SPECS.md): the orchestrator's duty, done by a hook. |
| [`test_auto_push.py`](test_auto_push.py) | [`test_auto_push.pyi`](test_auto_push.pyi) | — | T0 the auto-push hook's diagnosis. core/hooks/post-commit is the only place most sessions ever learn that pushing failed, so what it names as the cause is the whole of what the operator knows. |
| [`test_b20260831_silent_stub_gate.py`](test_b20260831_silent_stub_gate.py) | [`test_b20260831_silent_stub_gate.pyi`](test_b20260831_silent_stub_gate.pyi) | — | b20260831-silent-stub-gate regression — a gate that is OFF must say so. |
| [`test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.py`](test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.py) | [`test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.pyi`](test_b20260901_a_mirror_never_reaches_the_machine_that_pulled_it.pyi) | — | b20260901-a-mirror-never-reaches-the-machine-that-pulled-it regression. |
| [`test_b20260901_a_read_gate_races_the_tracker_that_clears_it.py`](test_b20260901_a_read_gate_races_the_tracker_that_clears_it.py) | [`test_b20260901_a_read_gate_races_the_tracker_that_clears_it.pyi`](test_b20260901_a_read_gate_races_the_tracker_that_clears_it.pyi) | — | b20260901-a-read-gate-races-the-tracker-that-clears-it regression — a parallel batch of reads loses none of its marks. |
| [`test_b20260901_the_codegraph_nudge_only_fires_when_a_stub_is_stale.py`](test_b20260901_the_codegraph_nudge_only_fires_when_a_stub_is_stale.py) | [`test_b20260901_the_codegraph_nudge_only_fires_when_a_stub_is_stale.pyi`](test_b20260901_the_codegraph_nudge_only_fires_when_a_stub_is_stale.pyi) | `indexed_project` | b20260901-the-codegraph-nudge-only-fires-when-a-stub-is-stale regression — a suggestion about the PROJECT fires for the project, not for the one file whose stub happens to be out of date. |
| [`test_b20260901_the_facade_set_is_written_out_in_four_places.py`](test_b20260901_the_facade_set_is_written_out_in_four_places.py) | [`test_b20260901_the_facade_set_is_written_out_in_four_places.pyi`](test_b20260901_the_facade_set_is_written_out_in_four_places.pyi) | — | b20260901-the-facade-set-is-written-out-in-four-places regression — what a file IS has one home. |
| [`test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.py`](test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.py) | [`test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.pyi`](test_b20260904_an_interpreter_heredoc_writes_any_file_past_every_edit_gate.pyi) | — | b20260904 regression — a write performed inside an interpreted heredoc body is seen. |
| [`test_b7_durable_bug_slugs.py`](test_b7_durable_bug_slugs.py) | [`test_b7_durable_bug_slugs.pyi`](test_b7_durable_bug_slugs.pyi) | — | B7 regression — a bug id is a durable slug, and never borrowed. Ids here used to be positional; completion deleted them and every close renumbered, so a citation of "B6" resolved to a bug that no longer was the one meant (the ZCode trust gate citation was the sighting). Since 2026-08-31 new ids are slugs, `b<YYYYMMDD>-<slug>`; a numeric id dies with its fix. The gate matches ids to specs across the hyphen/underscore seam — a slug id and its test_b<...> file name are the same string in two notations — and an id ends at a non-alphanumeric boundary, so b1 never borrows b19's proof. |
| [`test_bash_compact_rewrite.py`](test_bash_compact_rewrite.py) | [`test_bash_compact_rewrite.pyi`](test_bash_compact_rewrite.pyi) | `rtk_path` | T0 the multi-line rtk shim: it must reach lines 2+, and must never reshape shell it cannot read. |
| [`test_bash_context_gate.py`](test_bash_context_gate.py) | [`test_bash_context_gate.pyi`](test_bash_context_gate.pyi) | — | T0 the bash context gate reads the COMMAND, never the text the command carries. Zero-token, runs in verify-fast. |
| [`test_branch_debt.py`](test_branch_debt.py) | [`test_branch_debt.pyi`](test_branch_debt.pyi) | `git`, `commit`, `repo`, `cloned` | T0 the branch-debt signals: a repo is a finding when work lives in only one place, and never otherwise. Zero-token, runs in verify-fast. |
| [`test_branch_marker.py`](test_branch_marker.py) | [`test_branch_marker.pyi`](test_branch_marker.pyi) | `marker_path`, `repo`, `run` | T0 the branch-drift warning (core/hooks/SPECS.md § Branch drift): HEAD moving under a session must be said out loud, exactly once, and must never block. |
| [`test_gate_messages.py`](test_gate_messages.py) | [`test_gate_messages.pyi`](test_gate_messages.pyi) | — | T0: a hook must speak on the channel its class is read on. Two mirrored rules, one subject. |
| [`test_heredoc_gate.py`](test_heredoc_gate.py) | [`test_heredoc_gate.pyi`](test_heredoc_gate.pyi) | `run` | T0 the heredoc gate: a shell write to a workspace file must not walk past the file gates. |
| [`test_issues_gate_removal.py`](test_issues_gate_removal.py) | [`test_issues_gate_removal.pyi`](test_issues_gate_removal.pyi) | — | Regression — the issues gate reads removals, not only FIXED flips. A session deleted four fixed bug sections and one OPEN one from the workspace ISSUES.md; the gate only fired on the literal word FIXED, so an open bug (B4) left the ledger without a fix or a spec. Since 2026-08-31 a section may not leave ISSUES.md — by deletion or by a FIXED flip — without a matching regression spec, and a spec for B19 does not pay B1's debt: the id ends at the name boundary. |
| [`test_read_gate_prerequisites.py`](test_read_gate_prerequisites.py) | [`test_read_gate_prerequisites.pyi`](test_read_gate_prerequisites.pyi) | — | T0: a blocking read gate names every prerequisite of the read, not the one it happens to own. |
| [`test_subagent_gate.py`](test_subagent_gate.py) | [`test_subagent_gate.pyi`](test_subagent_gate.pyi) | — | T0 the subagent exemption (core/hooks/SPECS.md): a worker is not made to read the routing chain. |
<!-- routing:end -->
