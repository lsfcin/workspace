# Core Library Roadmap

> What is still unsound about the agent library itself — skills, agents, flows, tools and their schema. Workspace repo work is the wos list's, [/ROADMAP.md](../ROADMAP.md); an item belongs to exactly one of the two. Same cap, same three fields, same deletion policy, same refusal to write HOW: [/ROADMAP.md](../ROADMAP.md) states both once.

Contract: [SCHEMA.md](SCHEMA.md). Goal: [[spec-driven-development]].

## Open

**🟢 [mcptoon-context] Tool and skill discovery — backlog**
*What* — Assess mcptoon discovery, on-demand schema retrieval and measured context cost against our current workflow; source claims in refs/REFS.md, Dobra assessment in ../code/dobra/ROADMAP.md. *Why* — Lucas requested evaluation of the captured demonstration. *Done when* — One bounded comparison records cost, retrieval reliability and configuration effects before adoption.

**🟢 [rea-assessment] Reverse-engineering and media demonstrations — backlog**
*What* — Identify the primary REA, PhotoCraft and EffectCraft projects and assess transferable methods and media capabilities against existing tools; refs/REFS.md, media assessment also in ../branches/virada/ROADMAP.md. *Why* — The captured demonstrations may reduce repeated discovery or production work. *Done when* — Capabilities, licensing and the author's legal claims have evidenced verdicts or rejection.

**🟢 [links-cleanup] lsf-links cleanup — today**
*What* — Verify the Claude-session report of an orphan functions/api/lib/ stub and uncommitted functions/jsconfig.json in lsf-links; review the cleanup and commit only the intended change. *Why* — The 16 Oct session reported both operations blocked by permission classification. *Done when* — The report is checked against disk and Git, and any justified cleanup is verified and committed separately.

**🟢 [visual-tools] Captured visual tools — backlog**
*What* — Compare Hairline, ff-tracking, Papermorph and the animated-data example for editability, accessibility, source fidelity and reproducibility. Sources: refs/REFS.md. *Why* — Captured demonstrations may improve workspace explanations and teaching. *Done when* — One bounded comparison records what transfers and what fails.

**🟢 [expert-depth] Prompt depth — backlog**
*What* — Assess the prompt attributed to Felix Rieseberg against prepare/research: raw sources, professional methods and independent verification; refs/REFS.md. *Why* — Lucas asked whether to include it. *Done when* — A comparison identifies useful changes or rejection without expanding scope.

**🟢 [modder-patterns] Universal Modder — backlog**
*What* — Assess transferable discovery, live verification and field-note patterns against our workflow; refs/REFS.md. *Why* — The captured example may reduce repeated discovery. *Done when* — Transferable patterns or rejection are recorded.

**🟡 Desktop hyperagent — high priority, week**
*What* — Assess voice input/output, installed harness discovery, bounded cross-session context, routing and credit/session limits, with Lucas controlling every decision; reuse aiwbot and Dobra. Compare OpenHarness (refs/REFS.md): Linux, session reuse and relay/trust boundaries. *Why* — Current sessions fragment interaction and resource management. *Done when* — Lucas compares concrete designs and selects one (INBOX 2026-10-07).

**🟡 MatrAIx evaluation**
*What* — Assess simulated-user testing against our verification practices; refs/REFS.md. *Why* — It may cover interactive behavior. *Done when* — One bounded comparison establishes coverage and limits.

**🟡 PDF throughput**
*What* — Measure description latency, skip decoration and compare current engines after the pymupdf-layout change. *Why* — Large backfills can take hours. *Done when* — A representative batch establishes time, memory and fidelity.

**🟡 Dependency checks**
*What* — Let gates consult shared installation checks. *Why* — Feature switches do not prove installation. *Done when* — Enabled-but-uninstalled features produce one diagnosis.

**🟡 Promotion outside session close**
*What* — Assess a promotion-only path with verification. *Why* — Completed branches wait for roundup. *Done when* — Its benefit and safe verification boundary are established.

**🟡 Research intake**
*What* — Require question/surface inventories, consistent source identifiers, denominators, source type/method, early checkpoints and search limits; verify ambiguous figures and record human-only court lookup limits. *Why* — Omissions and lost work recur. *Done when* — One report preserves these contracts and access limits.

**🟡 Report publishing**
*What* — Assess reusable source resolution, renumbering and Markdown-to-page output, including a neutral named-link domain. *Why* — Repeated sessions use disposable scripts. *Done when* — Lucas selects the capability and one report verifies it.

**🟡 Proved presentation utilities**
*What* — Assess remaining performance/benchmark utilities if PowerPoint stays a chosen home; exhaust native capabilities before comparison. *Why* — Proved utilities exist only locally; builders should avoid discarded content. *Done when* — Useful pieces are retained or rejected and online measurement automation has a verdict.

**🟡 Forms integration**
*What* — Assess settings support, response-table export and consent preflight. *Why* — Workflows require manual operations and repeated authorization. *Done when* — One intake retrieves the required state consistently.

**🔴 Canva leaf: the agent builds and moves a Canva deck, Match & Move included, with no human click per deck**
*What* — Settle native editable shapes/connectors versus SVG before building; warn Lucas before conversion. Confirm MCP access (documented Education/Enterprise, working on Pro trial ending ~2026-11-02) or draft Apps SDK fallback. Build the Canva leaf through `/craft`; agent-only k10 reproduces bench k1, oracle-verified, then Lucas chooses the slides home. Re-read the shared deck every turn. *Why* — Lucas prefers Canva; motion survives copied seed pages via REST/MCP. Evidence: tools/slides/SPECS.md; design: `outputs/canva-poder-desenho.md`; prototypes: `outputs/.drafts/canva-poder/oracle.py` and `mcp_spike.py`. *Done when* — k10 passes without human clicks and the home decision replaces this item.

**🟡 a subagent can run on another harness, and an agent proposes it when it saves tokens**
*What* — Assess read-only prompt-file → output-file delegation between `codex exec`, `agy -p` and Claude Code, plus when to propose it; `core/tools/describe.py` is precedent. Preserve traps: `agy --model X -p="…"` (model before prompt), headless agy needs “no tools”, and `codex exec < /dev/null` avoids waiting on stdin. *Why* — The 2026-10-14 ideation-board summary and brw examples worked at zero Claude cost. *Done when* — One call returns a file from either harness and a session proposes it on a suitable fan-out task.

**🟡 evaluate UNSLOP, aihero.dev and Oil UI**
*What* — Find the real UNSLOP repository; assess aihero.dev /grill-me and /implement, and Oil UI alternatives on one desktop/mobile screen; refs/REFS.md. *Why* — These are named leads, not a general survey. *Done when* — Each has an evidenced verdict against our workflow or a written rejection.

**🟡 our own skills are too big, and nobody has checked whether the bulk earns anything**
*What* — every `core/skills/*.md` read for verbosity, redundancy, ambiguity, and steps costing more than they save. *Why* — Lucas (2026-08-25): *"skills são úteis mas me parecem meio gigantes quase sempre."* A skill is read in full at invocation, so its length is paid every time it fires.
*Done when* — no skill is longer than the work it describes, and each one still does its job.

**🟡 every skill is invisible to a session started outside the workspace**
*What* — skills reachable from a terminal opened anywhere, or a loud failure saying they are not.
*Why* — `.claude/commands/` is project-scoped, so a session whose project is `$HOME` loads none of the fourteen and silently has no `/roundup`. Reproduced 2026-08-18. *Done when* — Lucas gets the skill or an explicit refusal, never silence. Linking them globally means a workspace skill can fire in a repo it knows nothing about; that trade is the decision, not the wiring.

**🟡 `/roundup` ends by asking for something it could have proposed inside the plan**
*What* — one fewer round-trip per session. *Why* — Lucas suggested it and flagged it himself:
*"é só uma ideia, avaliar antes de implantar."* *Done when* — evaluated against the one-action rule for agent-facing text: a closing message naming the next session's close names a second action, so the honest version may belong in the plan template rather than in roundup's last line.

**🟢 a `gslides frames` command — the capability question is already answered**
*What* — one command taking an element, start and end positions, a frame count and an easing, emitting the batch. *Why* — per-object tweens are not in the API, but `duplicateObject` plus `updatePageElementTransform` in one `batchUpdate` authors a frame sequence, proven live 2026-08-14 and PDF-safe by construction. What is left is ergonomics, not discovery. *Done when* — the command exists and the two known traps are handled; both are in [`tools/slides/SPECS.md`](tools/slides/SPECS.md).

**🟢 `main` accepts commits from anywhere and Git Flow says it should not**
*What* — `gitflow_gate.py` refusing a merge into `main` whose other parent is not `develop` (or a `release/*`/`hotfix/*`), and `code/SPECS-git.md` stating that rule where it states the rest.
*Why* — Lucas asked for it (INBOX 2026-08-28). Today the gate only blocks hand-typed commits on the protected branches; a merge exits early on `MERGE_HEAD`, and the push policy calls `main` the sync point between two machines, so a feature branch can land there and nothing says a word.
*Done when* — a merge into `main` from anything but `develop` is refused, and the spec and the gate say the same thing.

**🟢 nothing we build on Drive can be thrown away by the thing that built it**
*What* — a `trash` command on `gdocs` and `gdrive`. *Why* — both write (`new`, `push`, `mkdir`, `put`) and neither deletes, so every check an agent creates is cleanup Lucas does by hand; two are waiting on him now. *Done when* — a file created by the CLI can be trashed by it, on the write token.

**🟢 benchmark Claude Slides and Design against our slides tooling**
*What* — compare Claude Slides and `/design` canvas generation against `gslides`/`slides_build` for deck authoring. *Why* — Lucas requested inclusion in the slides roadmap (INBOX 2026-09-27); evaluate if native repo-to-deck features replace or augment our pipeline. *Done when* — comparison notes and feature assessment written in `core/tools/slides/SPECS.md`.

**🟢 assess agent harnesses (DeepSeek Harness, Kilo Code, Cline) for WOS runner patterns**
*What* — evaluate architecture patterns in DeepSeek Harness (Cordis plugin framework, bubblewrap sandboxing), Kilo Code (specialized agent modes, MCP), and Cline. *Why* — external harness survey requested (INBOX 2026-09-27) to identify modular runtime patterns without importing bulk. *Done when* — documented verdict in `core/refs/REFS.md` on whether any pattern transfers to our runner or flows.

**🟢 evaluate systematic role prompting across WOS agents and flows**
*What* — test whether assigning explicit roles to subagents/prompts activates distinct latent representations in models and improves task adherence. *Why* — Lucas flagged consistency of 'role' in WOS prompts (INBOX 2026-09-27). *Done when* — experiment measuring output quality vs token cost across 3 tasks with and without explicit role assignment.

**🟢 obrigar download do PDF completo no flow de revisão de artigos**
*What* — atualizar `core/flows/research/review.md` para exigir o download e extração completa do PDF do artigo (via arXiv/URL ou twin) antes de iniciar a simulação de peer review, sem avaliar apenas por abstract ou HTML. *Why* — Lucas solicitou obrigatoriedade (INBOX 2026-09-26); avaliações baseadas em páginas web/abstract perdem tabelas, equações, apêndices e dados empíricos cruciais. *Done when* — o passo 4 do flow declara e executa o download mandatório do binário do PDF e seu twin antes de escrever notas de evidência.

**🟢 handoff por domínio ou subrepositório para sessões paralelas**
*What* — estender a skill `/handoff` (`core/skills/handoff.md`) para aceitar ou inferir um subdiretório/tema de saída (ex.: `outputs/<repo>/handoff.md` ou `outputs/handoff-<tema>.md`), em vez de usar um caminho único e rígido. *Why* — sessões simultâneas sobrescrevem `outputs/handoff.md` uma da outra (INBOX 2026-09-25, sessão taste). *Done when* — `/handoff` gera o resumo no caminho qualificado do projeto ativo e `/roundup` reconhece o handoff específico daquela sessão.

**🟢 arquitetura de geração em estágios (pastas/markdown) para slides e animações**
decks and animations built in stages with an intermediate markdown per stage (script → storyboard → visual → render, Van Clief method); done when the convention is in `core/tools/slides/SPECS.md` and one pilot deck ran through it (INBOX 2026-09-30).

**🟢 três subskills visuais para geração de slides (/slides)**
`/slides` gains photo search, shape-based drawing and styled diagrams with good edges and arrows; done when each subskill is validated on real slides (INBOX 2026-09-30).

**🟢 backport dos refinamentos de disciplina.md para o template canônico**
carry what `academy/teaching/classes/ai4good/disciplina.md` learned this semester into the canonical template without breaking `cfpages` (INBOX 2026-09-30).

**🟡 submissão interativa de artefatos por matrícula e validação no site de disciplinas**
a student submits an artefact link with their enrolment number on the course page, and the teacher accepts items in one click; done when a prototype works on a published `disciplina.md` (INBOX 2026-09-30).

**🟡 compare HotClip, Drift and Clipa for local edits and captions**
*What* — Compare xixihhhh/hotclip, Drift and Clipa on one recording: Portuguese caption accuracy, legibility, editability, export fidelity and cost; refs/REFS.md. *Why* — Classes and project videos need accessible editing; Lucas requested Clipa for Virada videos. *Done when* — Record the verdict under tools/video/ before adopting a tool.

**🟢 avaliar iris (Rust CLI + MCP) como ferramenta de visão/câmera para os agentes do WOS**
test `brijr/iris` as MCP or CLI for the agent to screenshot local and published pages; verdict in `core/tools/web/SPECS.md` (INBOX 2026-09-25).

**🟢 portar utilitários de slides_build.py para core/tools/slides/gslides**
split a deck, copy slides between decks, insert notes and images as `gslides` subcommands with unit tests, out of `ai4good/slides_build.py` (INBOX 2026-09-23).

**🟡 migrar e sintetizar a skill /prof para en-us**
translate `core/skills/prof/` to en-us with pt-br terms in backticks, cutting its ~60 KB (INBOX 2026-09-24).

**🟢 suportar espelhamento de subdiretórios de subskills no sync-skills**
`sync-skills` mirrors `prof/` and `slides/` subfolders so relative subskill links resolve in every harness (INBOX 2026-09-24).

**🟡 bounded orchestration through files**
*What* — Use small units, visible scope, cheaper capacity for precise briefs, cost limits, early checkpoints and approved reading scopes. Start long orchestration in a fresh session from a file plan; passage state lives in the project roadmap. Reuse mechanism-search across Canva/Virada. *Why* — Long swarms exhaust quotas and lose progress. *Done when* — One real run preserves progress within its declared budget.

**🟢 image twin: arquivo .md irmão com OCR + VLM para qualquer imagem isolada**
`core/run tools/assets/inspect --twin` writes `<image>.md` with OCR and a VLM description, merging `.imgif` and the video caption, and the read gates honour it (INBOX 2026-09-25).

**🟢 gdrive download com flag --out e seletor de destino**
`gdrive download --out <path>` instead of everything landing in `Downloads/workspace-drive/` (INBOX 2026-09-25).

**🟢 lint de contraste WCAG no gslides e substituição de pdftoppm por mutool**
`gslides lint` flags low WCAG contrast, and `mutool draw -w` replaces `pdftoppm -scale-to-x`, which crops (INBOX 2026-09-25).

## Blocked — waiting on a trigger

**🟢 the `video/` family name describes less than the family delivers** — it gained a page fallback, so it offers *link → navigable text* while the directory says one medium.
→ **trigger: the next time something else opens `core/tools/` for a path change.** Two sweeps have already happened and [`tools/SPECS.md`](tools/SPECS.md) § Naming says a third is not free, so pay it alongside another reason rather than on its own.

## Deferred — flows and agents, findings kept, nothing spent

Lucas, 2026-08-25: the layer waits until the v1 repo is tight. These were found by *running* the flow on 2026-08-24, so they are evidence rather than review notes and are kept at one line each.
None is worked until the layer reopens.

- **A craft executor reverted an uncommitted orchestrator edit it did not write.** Loop 6 had been handed the dirty-tree fence and discarded the file anyway; nothing was lost only because the orchestrator still held the text. The fence is writing in a spawn prompt, which names no consequence.
- **The router has no `experiment` folder**, so a controlled measurement fell back to the padaria gate, which measures the write rather than the investigation.
- **Padaria mandates a `feature/<name>` branch off develop** while the same flow's Field Practice names "two loops, one repo" as a known hazard.
- **The flow reads 18 KB of routing and runtimes before the gate that decides it needs them.**
- **Only Loop 1 declares a cap**, and the whole-file check reads it as covering the flow — including Loop 4b, which is called *Code Until Green*.
- **`engineering` is exempted by path rather than typed**, so the cluster doing the most work is the one not schema-checked.
- **The three `craft-*` agent mirrors are hand-written twice with no source in `core/`**, which is the last provider-name-in-source violation and the hand-sync hazard `SCHEMA-layers.md` documents.

## Rejected

- **Canva motion through a .pptx** (2026-10-03) — the import collapses every transition to dissolve and Canva's own export writes Match & Move as `<p:fade/>`, so neither direction carries it; motion is inherited from a copied seed page instead (§ Canva leaf).

- **Surveying outside skills for things to import** (asked 2026-07-23, dropped 2026-08-25) — the two leads are DM-bait posts naming skills without linking them, and the named capabilities overlap what `AGENTS.md` and CONTEXT.md already do. Reopen from a real repository, never from a reel.

## Notes

- `.claude/`, `.opencode/` and `.zcode/` are generated mirrors. Never hand-edit; run `sync-skills`, which prunes orphans and writes every link relative so a clone resolves it.
