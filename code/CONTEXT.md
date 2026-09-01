# Code
> Software projects developed under this workspace

You are a SENIOR software architect, your code WILL be evaluated!

**Before editing any file:**
1. Read it first. Before modifying a function, grep for all callers. Research before you edit.
2. Read the facade (`index.ts` / `__init__.py`) of every module you'll touch.

**You enforce this — no hook can:**
- REUSE always. NEVER copy-paste: refactor, extract a function or class.
- ONE responsibility per file — SMALL IS BETTER.
- REFACTOR after each coding prompt, and report only *after* refactoring.
- Names must be guessable without reading files, functions, or inspecting variables.

**Language rules, file templates, and the R1–R6 style table:** [SPECS-style.md](SPECS-style.md) § Style Rules (R1-R6).

**Git Flow**, the branch gate's scope, and the push policy: [SPECS-git.md](SPECS-git.md).

**Hooks block automatically** — each explains itself and names the fix when it fires, so only the numbers you need
*while writing* are here: files warn at **150 lines**, hard-block at **200**. The rest (facade boundaries, missing
first-line comments, duplicated blocks, the CONTEXT.md chain, interface stubs, `verify:fast` green, an ISSUES FIXED flip
needing a `test/**/b<N>-*` spec) surface at the moment they apply. Reasoning behind them:
[ROADMAP-verify.md](ROADMAP-verify.md).

**New project**: needs `CONTEXT.md` + `README.md`. Templates: [`_templates/`](_templates/).

**CONTEXT.md files**: line 2 = `> description`, line 3 = `> spec:` for a module. The routing block is auto-managed —
never edit it by hand.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`_templates/`](_templates/CONTEXT.md) | Project scaffolding templates — CONTEXT.md, README.md, SPECS.md, ROADMAP.md skeletons |
| [`aiwbot/`](aiwbot/CONTEXT.md) | Provider-agnostic bot: control swappable coding agents (claude·opencode·copilot) from chat. |
| [`apptime/`](apptime/CONTEXT.md) | Android app to reduce phone addiction through awareness, without blocking |
| [`corpora/`](corpora/CONTEXT.md) | Real-time 3D computer vision pipeline — depth, pose, segmentation from webcam |
| [`cria/`](cria/CONTEXT.md) | Workflow executável de ideação híbrida (motores de criatividade + score de fronteira semântica + kill-tests). Twin de pesquisa: `academy/papers/2027-CHI-cria/`. |
| [`dobra/`](dobra/CONTEXT.md) | Context folding + small local models: task-tree runner where SLMs do leaf work under folded context. Paper twin: `academy/papers/2027-ICLR-dobra`. |
| [`flows/`](flows/CONTEXT.md) | Graph-based workflow engine — typed slots, YAML-defined flows, pluggable agents |
| [`freeai/`](freeai/CONTEXT.md) | Mapa das opções gratuitas para codar com IA — harnesses de CLI e IDE, provedores com free tier e modelos open-weights, em tabelas comparativas com limites reais e links oficiais. |
| [`gira/`](gira/CONTEXT.md) | Protocolo + plataforma de crédito mútuo local com matching por agentes de IA — motor do núcleo circuito do instituto (Sardex×Mumbuca com clearing multi-hop). Primeira vertical: feira agroecológica (da-feirinha). |
| [`isoroll-content/`](isoroll-content/CONTEXT.md) | Offline asset generation pipeline for the isoroll Foundry VTT module |
| [`isoroll-module/`](isoroll-module/CONTEXT.md) | Foundry VTT v14 isometric projection module — TypeScript + Vite + SCSS. |
| [`laplata/`](laplata/CONTEXT.md) | Mapa vivo dos fluxos de dinheiro no Brasil — pipeline de dados abertos (BCB, IBGE) + visualizações que revelam ralos. Infraestrutura do programa instituto (núcleo 4) e estágio 1 do motor de ideação. |
| [`obra/`](obra/CONTEXT.md) | Somar o dinheiro da obra e primar o STT com o vocabulário dela. Dados em `branches/casinhas/`. |
| [`ppc/`](ppc/CONTEXT.md) | Interactive browser tool for experimenting with LC/UFRPE curriculum redesign |
| [`spacemantics/`](spacemantics/CONTEXT.md) | Verifiable spatial DSL (texpace) + deterministic checker that lift LLM spatial capability across 2D/2.5D/3D/4D |
| [`voti/`](voti/CONTEXT.md) | Political alignment tool comparing user answers to real deputy voting records — ARCHIVED as a spec |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ROADMAP-spec-drive.md`](ROADMAP-spec-drive.md) | — | — | Enforcement rollout making the spec the contract for `code/` modules: verifiable inputs/outputs/invariants that precede and govern the code. Goal: [spec-driven-development](../brain/goals/spec-driven-development.md). |
| [`ROADMAP-verify.md`](ROADMAP-verify.md) | — | — | Testing-discipline rollout for `code/` projects: make agents verify their own results (no human eye per prompt) and enforce code centralization. Pilot: isoroll-module. Second: apptime. |
| [`SETUP.md`](SETUP.md) | — | — | Per-language setup, facade templates, and project scaffolding reference |
| [`SPECS-git.md`](SPECS-git.md) | — | — | Which branches exist, what may be committed where, and when work is pushed. |
| [`SPECS-structure.md`](SPECS-structure.md) | — | — | How a project is laid out: its files, its module specs, and its facade. |
| [`SPECS-style.md`](SPECS-style.md) | — | — | How a file is written, how big it may get, and when a directory splits. |
| [`SPECS.md`](SPECS.md) | — | — | Engineering conventions, architecture decisions, and process rules for all code/ projects. |
| [`eslint.shared.js`](eslint.shared.js) | [`eslint.shared.d.ts`](eslint.shared.d.ts) | `localPlugin`, `sharedRules`, `countCallsInSubtree`, `getChainDepth` | Shared ESLint rules for all TypeScript/JavaScript projects under code/ — R1-R6 style enforcement. |
<!-- routing:end -->
