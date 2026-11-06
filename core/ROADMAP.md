# Core Library Roadmap

> What is still unsound about the agent library itself — skills, agents, flows, tools and their schema. Workspace repo work is the wos list's, [/ROADMAP.md](../ROADMAP.md); an item belongs to exactly one of the two. Same cap, same three fields, same deletion policy, same refusal to write HOW: [/ROADMAP.md](../ROADMAP.md) states both once.

Contract: [SCHEMA.md](SCHEMA.md). Goal: [[spec-driven-development]].

## Open

**🟡 [visual-comparisons] Captured options**
*What* — Complete-image numeric extraction: retain printed values, label estimated bar fractions with uncertainty. Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Relevance/limits evidenced.

**🟡 [owly-transfer] Captured options**
*What* — Check wireless adapter/device compatibility for Owly. Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Compatibility evidenced.

**🟡 [qwenputer] Captured options**
*What* — Compare Qwenputer with deterministic tools (merged-model/selected-test limits). Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Limits evidenced.

**🟡 [tool-comparison] Captured options**
*What* — [rated-tools] Assess voice/workflow/media tools against current needs. Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Relevance evidenced.


**🟡 [document-access] Captured options**
*What* — [firecrawl] Compare Firecrawl with our existing fetch/search on representative difficult sources, recording coverage, deployment duties, access failures and total cost. [nomad] Assess a small useful offline resource bundle, language/accessibility and local memory/storage needs before adopting the optional AI stack. Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Relevance and limits are evidenced.


**🟡 [local-inference-options] Captured options**
*What* — [strata-local] Check documented memory, disk, context, quality and omitted experts against our laptop before trial. [mesh-llm] Check trusted nodes, network cost and compatibility; remote routing is not fitting weights locally. [deepinfer] Track probable DeepInfer as vendor-reported datacenter engineering; assess research relevance, not laptop deployment. [airllm] Assess streaming capacity/latency with measured hardware, terabyte storage and seconds/token before any download. [model-continuity] Check used-model source/version continuity, licence, integrity and storage; no blanket-ban inference or oversized-derivative download. [gpu-unlock] Check supported compute workloads on our hardware; distinguish precision, power and whole-task results. Refs: refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Relevance and limits are evidenced.

**🟡 [academic-evidence-tools] Academic evidence intake**
*What* — Assess paginated query/date mail search, robust long attachment names, cached-email PDF evidence and official PROGEPE/federal personnel bulletin discovery. Inspect Downloads/progressao-scripts before reuse; preserve the reported progression evidence (279/2024, 1.022/2025) as attributed leads. Shared defect: ISSUES.md [b20261024-mail-search-attachments]; Claude/Codex reports, 24–28 Oct. *Why* — RDA/progression need the same reliable intake. *Done when* — A bounded evidence search retrieves its documents with provenance.

**🟢 [mcptoon-context] Tool and skill discovery — backlog**
*What* — Compare on-demand tool/skill schema discovery with current context cost/reliability; refs/REFS.md and Dobra roadmap. *Why* — Captured lead. *Done when* — Bounded results precede adoption.


**🟢 [rea-assessment] Reverse-engineering and media demonstrations — backlog**
*What* — Identify REA/PhotoCraft/EffectCraft; compare methods, media, licences and legal claims with current tools. Refs: refs/REFS.md; Virada roadmap. *Why* — Repeated discovery/production. *Done when* — Evidenced transfer or rejection.


**🟢 [links-cleanup] lsf-links cleanup — today**
*What* — Verify orphan functions/api/lib and uncommitted functions/jsconfig.json in lsf-links (Claude, 16 Oct); commit justified cleanup separately. *Why* — Reported permission blocks. *Done when* — Disk/Git diagnosis and verification agree.


**🟢 [visual-tools] Captured visual tools — backlog**
*What* — Compare Hairline/ff-tracking/Papermorph for editing, accessibility and fidelity; [web-motion] browser visual export; [anatomy] animation and sprites; [video-motion-skills] assess HyperFrames/Remotion/Manim (Sisinty Vaibhav), p5.brush (Rishi Jain) and Scenario 3D OS agent skills (refs/REFS.md). *Why* — Better explanations, teaching and agent capabilities. *Done when* — Bounded comparisons establish transfer or rejection.

**🟢 [expert-depth] Prompt depth — backlog**
*What* — Compare the attributed Felix Rieseberg prompt with prepare/research: raw sources, methods and independent checks; refs/REFS.md. *Why* — Lucas requested assessment. *Done when* — Useful changes or rejection, no scope inflation.

**🟢 [modder-patterns] Universal Modder — backlog**
*What* — Assess Universal Modder discovery, live checks and field notes; refs/REFS.md. *Why* — Repeated discovery. *Done when* — Transfer or rejection is evidenced.

**🟢 [provider-agnostic-clarification] Provider-agnostic governance — backlog**
*What* — Clarify core/norms/storage.md, interview.md and core/CONTEXT.md: configuration and storage are provider-independent (symlink to WIS), but execution can use any provider; external review does not restrict execution. *Why* — Harness friction (ChatGPT triage 2026-11-03). *Done when* — Updated norms approved and applied.

**🟢 [subagent-watchdog] External subagent watchdog — backlog**
*What* — core/run tools/agents/watch: wrap external CLIs (codex/agy) with timeout, idle heartbeat (kill if stdout idle 90s), non-empty output check, and </dev/null default. Document codex path. *Why* — Silent empty-output failures (INBOX 2026-10-31, 2026-11-01). *Done when* — Watch wraps headless agents reliably.

**🟢 [shoot-unbundle] shoot --unbundle flag — backlog**
*What* — Add --unbundle flag to tools/web/shoot to unpack base64+gzip artifacts directly. *Why* — Avoid scratchpad scripts (INBOX 2026-10-31). *Done when* — shoot --unbundle unpacks cleanly.

**🟢 [panel-opencode-zcode] Headless opencode & zcode in panel chain — backlog**
*What* — Test headless execution for opencode (~/.opencode/bin/opencode) and zcode (/usr/bin/zcode) and integrate into tools/panel/ask. *Why* — Expand provider diversity (INBOX 2026-11-04). *Done when* — Both run headless in panel.


**🟡 Desktop hyperagent — high priority, week**
*What* — Reuse aiwbot/Dobra for voice, discovery, bounded context, routing and quotas; assess OpenHarness Linux/lineage/trust (refs/REFS.md; ../code/aiwbot/ROADMAP.md [mobile-session-relay]). [unsloth-browser] Check permissions/network and memory in one bounded browser task. [voice-studio] Compare Portuguese narration, model licence, memory, latency and export. [dessa] Verify release/access/licence and Portuguese relevance; primary page unread. *Why* — Fragmented interaction (Lucas,7 Oct; Claude,23 Oct). *Done when* — Lucas chooses a concrete design.


**🟡 MatrAIx evaluation**
*What* — Compare simulated-user testing with our checks; refs/REFS.md. *Why* — Possible behavioral coverage. *Done when* — Bounded validity/limits are recorded.


**🟡 PDF throughput**
*What* — Measure description latency and compare engines after pymupdf-layout change. Refs: refs/REFS.md ([unlimited-ocr], [laws-markdown]). *Why* — Large backfills take hours. *Done when* — Time, memory and fidelity evidenced.

**🟡 Dependency checks**
*What* — Shared installation checks; assess local spreadsheet support before adding packages. Refs: refs/REFS.md ([dependency-provenance]). *Why* — Feature switches do not prove installation. *Done when* — Missing dependencies give single diagnosis.

**🟡 [drive-doc-update] Existing document updates — backlog**
*What* — Assess in-place document replacement preserving identity/history/access, including failures. Consumer: ../academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md [drive-update]. *Why* — Missing drive_core capability reported 19 Oct. *Done when* — Authorized update verifies; norms/edit.md binds originals.


**🟡 Promotion outside session close**
*What* — Assess verified promotion without roundup. *Why* — Finished branches wait. *Done when* — Benefit and verification boundary are established.


**🟡 Research intake**
*What* — Require question/owner inventories, source ids/types/methods, denominators, figure checks, early checkpoints, search/access limits and human-only court lookup. *Why* — Recurrent omissions/loss. *Done when* — One report preserves the contract.


**🟡 Report publishing**
*What* — Assess source resolution, renumbering, Markdown-to-page and neutral named-link domain. *Why* — Repeated scratch scripts. *Done when* — Lucas selects a verified capability.


**🟡 Proved presentation utilities**
*What* — Retain proved performance/benchmark utilities if PowerPoint remains selected; exhaust native features first. *Why* — Useful work is only local. *Done when* — Retain/reject remaining pieces and rule on online measurements.


**🟡 Forms integration**
*What* — Assess settings, response export and consent preflight. *Why* — Repeated manual work/authorization. *Done when* — Required state is consistently retrieved.


**🔴 Canva leaf: the agent builds and moves a Canva deck, Match & Move included, with no human click per deck**
*What* — [subscription-review] Review ChatGPT/Canva use, billing, renewal and alternatives today before more build work. Settle editable shapes/connectors versus SVG with Lucas; verify MCP grant (Education/Enterprise documented; Pro trial reportedly ends ~2 Nov) or Apps SDK fallback. Through /craft, k10 must reproduce k1 without human clicks, oracle-verified; reread shared deck each turn. Evidence: tools/slides/SPECS.md, outputs/canva-poder-desenho.md, outputs/.drafts/canva-poder/{oracle.py,mcp_spike.py}. *Why* — Lucas prefers Canva; copied seeds retain motion. *Done when* — Verified k10 lets Lucas choose the home.


**🟡 [cross-harness-delegation] Parity and reliable delegation across harnesses**
*What* — Close Codex gaps in read completeness, worker briefs, permissions/effort, session reports/close, automations/bot, state/registry, dependencies/auth and public export. Evidence and acceptance: ../outputs/codex-audit-20261102/auditoria.md; nine public-test causes remain undiagnosed. Compare quality, tokens/cost, capability and quota on matched tasks; keep dated caller/callee commands and automatic executable discovery. Verify credentials, sandbox/network scope, unattended start, retries, process completion, stalled logs, interruption survival and duplicate prevention. [r-cli] Check memory portability. [pstack] Verify completion, invariants and throughput claims. [context-evidence] Measure context/planning/checks; reject the invented 100k cutoff. Refs: refs/REFS.md; agents/SPECS.md. *Why* — Shared quota and equivalent workspace contracts. *Done when* — Declared features have per-harness evidence, bounded completion/failure, and green source/public-clone checks without bypasses.


**🟡 evaluate UNSLOP, aihero.dev and Oil UI**
*What* — Identify UNSLOP; compare aihero.dev grill-me/implement and Oil UI on one desktop/mobile screen; refs/REFS.md. *Why* — Named leads. *Done when* — Evidenced verdicts or rejection.


**🟡 our own skills are too big, and nobody has checked whether the bulk earns anything**
*What* — Cut verbosity, repetition, ambiguity and costly steps in every core/skills file. *Why* — Invocation rereads the whole skill (Lucas, 25 Aug). *Done when* — Each retained step earns its reading/execution cost.


**🟡 every skill is invisible to a session started outside the workspace**
*What* — Make skills reachable outside this workspace or fail explicitly. *Why* — HOME sessions silently lack project-scoped commands (18 Aug). *Done when* — Lucas gets the skill or a refusal; review the trust cost of global links.


**🟡 `/roundup` ends by asking for something it could have proposed inside the plan**
*What* — Assess moving the next closing action into the plan template. *Why* — Lucas requested one fewer closing round-trip, not automatic implementation. *Done when* — Evaluation respects the one-action text rule.


**🟢 a `gslides frames` command — the capability question is already answered**
*What* — Expose element/start/end/frame-count/easing batch generation. *Why* — duplicateObject plus transforms already proved PDF-safe frame sequences (14 Aug); remaining work is ergonomics. *Done when* — Command handles both traps in tools/slides/SPECS.md.


**🟢 `main` accepts commits from anywhere and Git Flow says it should not**
*What* — Reject merges into main unless from develop/release/hotfix; align code/SPECS-git.md. *Why* — MERGE_HEAD currently bypasses the gate (Lucas, 28 Aug). *Done when* — Invalid ancestry is refused and spec agrees.


**🟢 nothing we build on Drive can be thrown away by the thing that built it**
*What* — Add trash to gdocs/gdrive using write-token access. *Why* — Their own test creations otherwise require manual cleanup. *Done when* — CLI-created files can be trashed by the CLI.


**🟢 benchmark Claude Slides and Design against our slides tooling**
*What* — Compare Claude Slides/design with gslides/slides_build. *Why* — Lucas requested repo-to-deck assessment (27 Sep). *Done when* — Useful differences and verdict are in tools/slides/SPECS.md.


**🟢 assess agent harnesses (DeepSeek Harness, Kilo Code, Cline) for WOS runner patterns**
*What* — Assess DeepSeek Harness/Cordis/bubblewrap, Kilo specialized modes and Cline against our runner/flows. *Why* — Lucas requested modular patterns (27 Sep). *Done when* — refs/REFS.md records transfer or rejection.


**🟢 evaluate systematic role prompting across WOS agents and flows**
*What* — Compare explicit roles versus none on three tasks. *Why* — Lucas questioned role consistency (27 Sep). *Done when* — Quality/token costs and task adherence are measured.


**🟢 obrigar download do PDF completo no flow de revisão de artigos**
*What* — Require full PDF download/extraction before peer-review simulation in flows/research/review.md. *Why* — Abstract/HTML-only review misses tables, equations and appendices (Lucas, 26 Sep). *Done when* — Review reads the binary and extracted text.


**🟢 handoff por domínio ou subrepositório para sessões paralelas**
*What* — Verify project-qualified handoff naming and roundup recognition. *Why* — Parallel sessions overwrote outputs/handoff.md (25 Sep). *Done when* — Session-safe paths resolve without cross-session replacement.


**🟢 arquitetura de geração em estágios (pastas/markdown) para slides e animações**
*What* — Assess script→storyboard→visual→render with intermediate Markdown. *Why* — Van Clief reference (30 Sep). *Done when* — Convention in tools/slides/SPECS.md and a pilot demonstrate it.


**🟢 três subskills visuais para geração de slides (/slides)**
*What* — Assess photo search, shape drawing and styled diagrams for /slides. *Why* — Lucas requested better visuals (30 Sep). *Done when* — Each is validated on a real deck.


**🟢 backport dos refinamentos de disciplina.md para o template canônico**
*What* — Backport proven ai4good/disciplina.md refinements to the canonical template. *Why* — Share semester learning (30 Sep). *Done when* — Template retains cfpages compatibility.


**🟡 submissão interativa de artefatos por matrícula e validação no site de disciplinas**
*What* — Assess student link submission by enrolment and teacher acceptance. *Why* — Course-page intake (30 Sep). *Done when* — Prototype works on a published disciplina.md.


**🟡 compare HotClip, Drift and Clipa for local edits and captions**
*What* — Compare HotClip, Drift and Clipa on Portuguese captions, readability, editing, export and cost; refs/REFS.md. *Why* — Classes/Virada production. *Done when* — tools/video records a verdict before adoption.


**🟢 avaliar iris (Rust CLI + MCP) como ferramenta de visão/câmera para os agentes do WOS**
*What* — Assess brijr/iris CLI screenshots of local/published pages. *Why* — Agent vision lead (25 Sep). *Done when* — tools/web/SPECS.md records compatibility and verdict.


**🟢 portar utilitários de slides_build.py para core/tools/slides/gslides**
*What* — Port deck splitting, slide copying, notes and images from ai4good/slides_build.py to gslides. *Why* — Reuse proved utilities (23 Sep). *Done when* — Subcommands have meaningful checks.


**🟡 migrar e sintetizar a skill /prof para en-us**
*What* — Cut and translate core/skills/prof to English, retaining Portuguese terms where needed. *Why* — Oversized invoked text (24 Sep). *Done when* — Guidance remains usable at lower reading cost.


**🟢 suportar espelhamento de subdiretórios de subskills no sync-skills**
*What* — Verify sync-skills mirrors prof/slides subfolders. *Why* — Relative subskill links must work across harnesses (24 Sep). *Done when* — Every target resolves the mirrored children.


**🟡 bounded orchestration through files**
*What* — Bound file-based units, briefs, approved reads, cost and checkpoints; resume from plans and project roadmaps. Assess Canva/Virada searches and AI4Good brainwriting before adding a flow. [harness2] Control calls, held-out evaluation, judges and sandbox. [code-mode] Compare composition/filtering with direct calls without Model Context Protocol adoption. [scaledown] Compare narrow heads for cost/correctness, schema versus meaning/generation/service availability. Refs: refs/REFS.md. *Why* — Long swarms lose progress; duplicate tournaments reported 19 Oct. *Done when* — A real run preserves budget/progress and states shared ownership.


**🟢 image twin: arquivo .md irmão com OCR + VLM para qualquer imagem isolada**
*What* — Assess assets/inspect --twin combining OCR, descriptions and .imgif/video captions. *Why* — Standalone images lack navigable text (25 Sep). *Done when* — A sibling Markdown is consumed by read gates.


**🟢 gdrive download com flag --out e seletor de destino**
*What* — Add gdrive download --out. *Why* — Downloads need an explicit destination (25 Sep). *Done when* — Selected paths replace mandatory Downloads/workspace-drive output.


**🟢 lint de contraste WCAG no gslides e substituição de pdftoppm por mutool**
*What* — Add WCAG contrast lint and replace cropping pdftoppm sampling with mutool draw -w. *Why* — Slide readability (25 Sep). *Done when* — Contrast is diagnosed and previews preserve page bounds.

## Blocked — waiting on a trigger

**🟢 Video-family naming** — page fallback makes this link→text, not video-only. Trigger: next related core/tools path change; tools/SPECS.md § Naming rules out an isolated third rename.

## Deferred — flows and agents, findings kept, nothing spent

Flows/agents wait for v1 (Lucas, 25 Aug); observed 24 Aug failures preserved (orchestrator reversion, router experiment gate, 18 KB routing read overhead, uncapped Loop 4b).

## Rejected

- Canva motion through PPTX: import/export reduce Match & Move to fade; use a copied seed (3 Oct).

- Outside-skill survey: DM-gated unlinked leads duplicated existing guidance; reopen from a real repository (25 Aug).
