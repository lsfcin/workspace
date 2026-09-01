# Papers
> LaTeX papers, submissions, manuscript workflows

Each paper is its own subdirectory with its own git repo (Overleaf as remote). Local compilation is
primary; Overleaf is the sync/checkpoint for final validation.

Every rule that constrains a paper — naming, file size, first-line comments, the `.texif` interface,
the `refs/` schema and tag vocabulary, writing quality, evidence discipline, git — plus how to
scaffold a new paper and how to build one: [SPECS.md](SPECS.md).

## Research

`/research lit "topic"` · `/research review sections/03_related_work.tex` · plus the CLI tools in
[core/tools/CONTEXT.md](../../core/tools/CONTEXT.md) (`papers`, `search`, `fetch`). Workflow
protocols: [core/flows/](../../core/flows/CONTEXT.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`2026-JBCS-relativistic_raytracer/`](2026-JBCS-relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |
| [`2026-SIBGRAPI-relativistic_raytracer/`](2026-SIBGRAPI-relativistic_raytracer/CONTEXT.md) | SIBGRAPI 2026 paper on relativistic raytracing benchmarking |
| [`2027-CHI-cria/`](2027-CHI-cria/CONTEXT.md) | Hybrid human-AI ideation as mechanism design — classroom study. Targets: LBW CHI 2027 (piloto), full CHI 2028. |
| [`2027-ICLR-dobra/`](2027-ICLR-dobra/CONTEXT.md) | Context folding + SLMs on consumer hardware — research twin of `code/dobra`. Target: ICLR 2027 (~Sep 2026 deadline). |
| [`ai4good/`](ai4good/CONTEXT.md) | Visão + sistema + piloto: o papel moral da IA — da captura de atenção e da guerra à reconfiguração das lógicas sociais. Sessão Opus dedicada pendente. |
| [`mechanism-search/`](mechanism-search/CONTEXT.md) | Paper embrião: busca de mecanismos sociais com LLMs ancorada em dados de fluxo financeiro — método do motor de ideação do instituto (`branches/instituto/MOTOR.md`), flagship metodológico do LIH.DD. Alvo: EAAMO / CSCW / Collective Intelligence. Estágio: pré-venue, sem LaTeX. |
| [`mutual-credit-ai/`](mutual-credit-ai/CONTEXT.md) | Paper embrião: agentes de IA resolvendo a iliquidez de moedas complementares — clearing multi-hop e matching contínuo em circuito local (feira agroecológica). Twin de pesquisa do núcleo circuito (`branches/instituto/nucleo-circuito.md`) e de `code/gira`. Alvo: EAAMO / complexity econ. Estágio: pré-venue, sem LaTeX. |
| [`pls-pix/`](pls-pix/CONTEXT.md) | Paper embrião: prize-linked savings via Pix contra o dreno das bets no Brasil — desenho de mecanismo + piloto. Twin de pesquisa do núcleo virada (`branches/instituto/nucleo-virada.md`). Alvo: EAAMO / dev econ. Estágio: pré-venue, sem LaTeX (rodar paper-scaffold.py ao promover). |
| [`spacemantics/`](spacemantics/CONTEXT.md) | Benchmark+method paper: a verifiable spatial DSL lifts LLM spatial capability across 2D/2.5D/3D/4D and across models |
| [`wos-ablation/`](wos-ablation/CONTEXT.md) | Paper embrião: does an enforced agent workspace actually make an AI coding agent better? Ablation over this repo's own gates, skills and hooks. Alvo: AIware / ICSE-SEIP / FSE-Industry. Estágio: pré-venue, sem LaTeX (rodar paper-scaffold.py ao promover). |

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Papers Roadmap |
| [`SPECS.md`](SPECS.md) | What must be true of every paper under `academy/papers/`, and why. Extracted from `CONTEXT.md` on 2026-07-30: `context-gate` forces the whole CONTEXT.md chain before any file access, so a constraint written there was a tax on every session in the subtree — opening one `.tex` cost 2.4k tokens. SPECS is loaded on demand. |
<!-- routing:end -->
