# Workspace Root
> Canonical workspace entrypoint. Read before any task.

<!-- norms:start -->
- FILESYSTEM = source of truth. No memory, no assumptions.
- **PROVIDER-AGNOSTIC STORAGE**: the workspace owns its state, never a harness; if it insists,
symlink the path into WIS.
- **SECRETS STAY OUT OF GIT**: passwords, tokens, CPF/CNPJ go in a gitignored
`<subtree>/segredos.env`; the text keeps the label.
- IMPROVE WOS, after finishing MICRO (particular task), take a step back and review and refine MACRO
(structure). if it ain't feasible to do it on this session, WRITE ISSUES DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- EXPAND ACRONYMS on first use. Aliases: [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary.
- EDIT > CREATE: refine / improve **wins over** creating new, except for prototyping. Avoid scattering.
- A FILE OVER THE CAP IS CUT, NOT SPLIT. A `TYPE-<slug>.md` sibling is a last resort, and Lucas's
explicit OK. The line cap outranks the column cap (ruled 2026-08-31): wrapping to fit the column
never justifies a file over the line cap — the way out is cutting, not reflowing.
- SYMMETRY IS A CORE VALUE, semantic and structural. When you find an asymmetry, write it down.
- **DONE WORK IS DELETED. GIT IS THE HISTORY.** No strikethrough, no annotated corpses.
- USE OUR TOOLS: we want those to be useful and perfected.
- REDUCING IS THE WAY: improve/extend by cutting size; growing the workspace takes Lucas's OK first.
<!-- norms:end -->

Git Flow, the branch gate's scope, the `--no-verify` protocol, and the push policy:
[`code/SPECS-git.md`](code/SPECS-git.md). *Gated by `core/hooks/git/gitflow_gate.py`.*
What the hooks block, and the contract a new agent's shim must satisfy:
[`core/hooks/SPECS.md`](core/hooks/SPECS.md). Installing the toolchain they need — stubgen, tsc,
caveman, rtk: [SETUP.md](SETUP.md).
What we intend to build: [`ROADMAP.md`](ROADMAP.md). What is currently untrue that we know about —
open issues, the entropy findings, the last verification result: [`ISSUES.md`](ISSUES.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`academy/`](academy/CONTEXT.md) | Research, teaching, academic work |
| [`brain/`](brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`branches/`](branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`code/`](code/CONTEXT.md) | Software projects developed under this workspace |
| [`core/`](core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`models/`](models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
