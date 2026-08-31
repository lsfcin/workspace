# workspace
> Tier 0 workspace-wide invariants: pointers resolve, .gitignore self-heals, imports do not shadow.

Split 2026-08-15 at 8 files. What stayed is what holds for the **whole tree** rather than for one
piece of machinery: every relative link resolves, a new domain subdirectory does not fall out of the
`.gitignore` allowlist, and the suite's `sys.path` cannot silently shadow a module. The two
machineries moved into subdirectories named for the code they cover, so a surface and its coverage
are one word apart: [`gates/`](gates/CONTEXT.md) and [`generators/`](generators/CONTEXT.md), mirroring
`core/hooks/gates/` and `core/hooks/generators/`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`gates/`](gates/CONTEXT.md) | What a blocking gate must say, and who it must fire for. Named for `core/hooks/gates/` and deliberately wider than it. |
| [`generators/`](generators/CONTEXT.md) | What the generators must produce, and what they must never produce. Mirrors `core/hooks/generators/`. |
| [`harness/`](harness/CONTEXT.md) | The suite's own preconditions: nothing about the workspace, everything about the runner. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_antigravity_shim.py`](test_antigravity_shim.py) | [`test_antigravity_shim.pyi`](test_antigravity_shim.pyi) | — | T0: Antigravity provider shim unit test suite. |
| [`test_b12_run_dispatch.py`](test_b12_run_dispatch.py) | [`test_b12_run_dispatch.pyi`](test_b12_run_dispatch.pyi) | — | B12 regression — core/run runs what it says it runs. The launcher's own first line promises "the one command that runs anything in core/", but it exec'd every target with the venv interpreter, so the two bash tools died with `SyntaxError: unmatched ')'`. It now dispatches on the shebang (ruled 2026-08-31, Lucas: add capabilities, never exceptions). This spec holds both arms: a bash target runs as bash, and a python target still reaches the interpreter. |
| [`test_b13_harness_declaration.py`](test_b13_harness_declaration.py) | [`test_b13_harness_declaration.pyi`](test_b13_harness_declaration.pyi) | — | B13 regression — the harness mirror list is declared once, in a data file something reads. sync-skills carried MIRRORS=(...) in its own source; adding a harness meant editing a bash array by hand — done twice in one week. The list now lives in core/harnesses.txt, sync-skills reads it, and .gitignore restates only what the declaration says. A declaration nothing can check fails silently in the direction that leaves stale mirrors on disk; this spec is the check. |
| [`test_brain_attention.py`](test_brain_attention.py) | [`test_brain_attention.pyi`](test_brain_attention.pyi) | — | T0 the goal-file `>**owns**` block: a field ends where its block ends. Zero-token, verify-fast. |
| [`test_corpus_ratchet.py`](test_corpus_ratchet.py) | [`test_corpus_ratchet.pyi`](test_corpus_ratchet.pyi) | — | T0 corpus ratchets (core/SCHEMA.md § Placement): the .md corpus may not accumulate more of the three defects no link-checker can see. Zero-token, runs in verify-fast. |
| [`test_gitignore_self_heal.py`](test_gitignore_self_heal.py) | [`test_gitignore_self_heal.pyi`](test_gitignore_self_heal.pyi) | — | T0 self-healing .gitignore allowlist check (core/hooks/SPECS.md): a new domain subdir with a CONTEXT.md must get its `!<domain>/<dir>/` allow line added automatically, no human action. |
| [`test_pointer_integrity.py`](test_pointer_integrity.py) | [`test_pointer_integrity.pyi`](test_pointer_integrity.pyi) | `check_pointers` | T0 pointer-integrity check (Tier 0): every relative ](path) link across CONTEXT.md / ROADMAP*.md / SCHEMA.md / AGENTS.md (repo) and MEMORY.md (auto-memory) must resolve. Zero-token, runs in verify-fast. |
| [`test_port_ratchet.py`](test_port_ratchet.py) | [`test_port_ratchet.pyi`](test_port_ratchet.pyi) | — | T0 the OS-agnostic port's invariants (AD-0): the tree may not re-acquire the defects the port removed. Zero-token, runs in verify-fast. |
| [`test_setup_executable.py`](test_setup_executable.py) | [`test_setup_executable.pyi`](test_setup_executable.pyi) | — | T0 the install is a procedure, not prose (core/SCHEMA.md § The .md type system): every SETUP.md step declares its feature and carries a precondition, an install and a verify probe. |
| [`test_shim_paths.py`](test_shim_paths.py) | [`test_shim_paths.pyi`](test_shim_paths.pyi) | — | T0 the shim contract (core/hooks/SPECS.md): every canonical script a provider shim spawns must exist. Zero-token, verify-fast. |
<!-- routing:end -->
