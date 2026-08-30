# hooks
> The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run.

Wired globally via `git config --global core.hooksPath /mnt/workspace/core/hooks`, so
`pre-commit` fires in **every** repo under this workspace, and by absolute path from
`.claude/settings.json` for the agent-side gates.

## The law lives in this directory's root, not in any checker

Three modules answer the three questions — [`file_law.py`](file_law.py) what a file **is**,
[`schema_law.py`](schema_law.py) what a name **may be**, [`feature_law.py`](feature_law.py) what
is **switched on** — and each reads its answer out of a data file rather than holding one: the
numbers, the vendored trees, the extensionless names, the `.gitignore` exceptions, and (like
`schema_law.py`, one level up in `core/`) the feature registry and its profile.

A fourth question — **when** a switched-on feature fires — is answered the same way one directory
down, in [`trigger/`](trigger/CONTEXT.md).

Which gates consult `feature_law`, and why a row that does not is a finding:
[`core/SPECS.md`](../SPECS.md) § AD-14.

**A checker that restates any of these is the drift the checkers exist to catch.** Two
incidents that shape this rule, and the test that guards the first: [`SPECS.md`](SPECS.md).

## Shape — the root holds the law, every subdirectory holds one responsibility

Only the two law modules, the shared hook-stdin parser, and the three entrypoints whose
names are dictated by git/`.claude/settings.json` (`pre-commit`, `post-commit`,
`post-edit.sh`) stay at the root. Everything else lives in a subdirectory with its own
responsibility, routed through the table below.

Two axes worth knowing before you route:

- **Sourced vs executed.** `gates/`, `generators/` and `postedit/` hold *fragments* that are
  `source`d by `pre-commit` / `post-edit.sh` and share their shell state. Every other
  directory holds standalone programs, run by path.
- **Reject vs write.** A gate exits non-zero and stops the commit or the edit; a generator
  writes an artifact and stages it. `entropy/` does neither — it reports, into
  [`ISSUES.md`](../../ISSUES.md); read that report instead of re-scanning the tree.

Python modules in a subdirectory reach the root law with
`sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`. The test suite gets the same
path set once, from `core/tools/test/conftest.py`, derived by scanning this directory.

Gate behavior, what the hooks write, and the agent-shim contract all live in
[`SPECS.md`](SPECS.md). Why the `code/` gates
exist: [`code/ROADMAP-verify.md`](../../code/ROADMAP-verify.md). Installing the toolchain they depend on:
[`SETUP.md`](../../SETUP.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`brain/`](brain/CONTEXT.md) | brain/ attention stats and the GOALS.md dashboard. |
| [`checks/`](checks/CONTEXT.md) | Standalone blocking checks the commit and edit hooks run. |
| [`commit/`](commit/CONTEXT.md) | The git pre-commit and post-commit pipeline: what runs on every commit, in what order, and the one place a commit is refused. |
| [`compact/`](compact/CONTEXT.md) | Shrink tool output before it reaches the context — the input-side twin of caveman. |
| [`copilot/`](copilot/CONTEXT.md) | Provider shim: translates Copilot hook payloads onto the canonical gates. |
| [`entropy/`](entropy/CONTEXT.md) | The Tier 0 checks that count what the tree has drifted into. One question each. |
| [`facade/`](facade/CONTEXT.md) | The facade discipline: read the facade before editing, never import around it. |
| [`git/`](git/CONTEXT.md) | Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore. |
| [`postedit/`](postedit/CONTEXT.md) | Sourced post-edit stages: regenerate interfaces, remind, sync, lint. |
| [`read/`](read/CONTEXT.md) | Who must read what before touching a subtree — and who gets handed it instead. |
| [`routing/`](routing/CONTEXT.md) | The CONTEXT.md routing-table generator, and the delimited-block writer every generator shares. |
| [`session/`](session/CONTEXT.md) | Session lifecycle: start, prune, precompact wipe, and the SessionStart nudges. |
| [`stubgen/`](stubgen/CONTEXT.md) | Interface stubs and paper scaffolding, generated on save and on commit. |
| [`trigger/`](trigger/CONTEXT.md) | When a feature fires, read from the registrations rather than from where its file sits. |
| [`zcode/`](zcode/CONTEXT.md) | ZCode-side instruments: the hook-protocol probes, and the future home of the adapter if direct registration fails fidelity. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | What must be true of the enforcement layer, and why: what each gate blocks, what the hooks write, and the contract a new agent's shim must satisfy. |
| [`extensionless.txt`](extensionless.txt) | — | — | Files allowed to have no extension because something OUTSIDE this workspace dictates the name — enforced by test_every_extensionless_tracked_file_is_explained. |
| [`feature_law.py`](feature_law.py) | [`feature_law.pyi`](feature_law.pyi) | `load_registry`, `slugs`, `load_profile`, `is_enabled`, `setting` | What is switched ON. The third law module: file_law.py says what a file IS, schema_law.py says what a name MAY BE, this one says which features are live. Like schema_law.py it reads its answer out of core/ rather than holding one — the registry is core/features.txt, the answers are core/profile.txt, and neither is restated here. |
| [`file_law.py`](file_law.py) | [`file_law.pyi`](file_law.pyi) | `is_tool_entrypoint`, `is_code_file`, `load_limits`, `allowed_extensionless`, `is_vendored` | What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py: that module parses core/SCHEMA.md, this one owns the file-shape law every size, fanout and line-count check reads. |
| [`generated.txt`](generated.txt) | — | — | Files this workspace GENERATES. Excluded from the line cap, the fanout signal and the size dashboard — an authoring rule aimed at a file nobody authored produces a finding nobody can act on, and the only honest fix would be to make the generator write worse output. |
| [`gitignore-exceptions.txt`](gitignore-exceptions.txt) | — | — | One "<domain>/<dir>" per line: a CONTEXT.md-bearing subdir Lucas deliberately wants left out of the .gitignore allowlist (reviewed, not an oversight). gitignore-self-heal.sh skips any name listed here instead of re-adding its `!<domain>/<dir>/` line. |
| [`hook_input.py`](hook_input.py) | [`hook_input.pyi`](hook_input.pyi) | `parse_stdin`, `is_subagent`, `seen_file`, `load_seen`, `mark_seen` | Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas. |
| [`limits.env`](limits.env) | — | — | Every numeric limit in the workspace, in one file. Read by core/hooks/file_law.py (Python) and sourced directly by check-line-counts.sh (shell) — same file, one law. |
| [`platform_law.py`](platform_law.py) | [`platform_law.pyi`](platform_law.pyi) | `interpreter`, `session_state`, `install_command`, `package_install`, `posix` | The platform seam: the one file in this workspace allowed to know what an operating system is. |
| [`post-commit`](post-commit) | — | — | auto-push feature/*. Same handoff as pre-commit beside it. Never blocks: git ignores a post-commit's exit status, and every failure here is a warning. |
| [`post-edit.sh`](post-edit.sh) | — | — | PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md |
| [`pre-commit`](pre-commit) | — | — | Workspace pre-commit hook. Applied globally: git config --global core.hooksPath <this directory> |
| [`schema_law.py`](schema_law.py) | [`schema_law.pyi`](schema_law.pyi) | `load_law`, `load_scopes`, `load_retired` | The law parser. Every Tier 0 check reads core/SCHEMA.md through this module, and none of them restates it — a second copy of the law inside a checker is the exact drift the checks exist to catch. |
| [`vendored.txt`](vendored.txt) | — | — | Third-party files we did not author. Excluded from the line cap, the fanout signal and the size dashboard — holding someone else's code to our authoring rules produces findings nobody can act on. |
<!-- routing:end -->
