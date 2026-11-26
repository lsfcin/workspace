# Core Library Roadmap

> Agent-library work; workspace work and list policy: [/ROADMAP.md](../ROADMAP.md).

Contract: [SCHEMA.md](SCHEMA.md). Goal: [[spec-driven-development]]. Evidence: [refs/REFS.md](refs/REFS.md).

## Open

**🟢 [graphify-audit] Graphify use and cost — backlog**
*What* — Assess actual Graphify use, maintenance/context cost and value against current repository navigation. *Why* — Lucas questions whether it earns its overhead (INBOX 31 Oct). *Done when* — Lucas reviews evidence before retention/removal.

**🟡 [visual-comparisons] Printed values**
*What* — Retain printed image values; label bar estimates with uncertainty. *Done when* — Fit evidenced.

**🟡 [owly-transfer] Wireless compatibility**
*What* — Check wireless adapter/device compatibility for Owly. *Done when* — Compatibility checked.

**🟡 [qwenputer] Foundations**
*What* — Compare Qwenputer with deterministic tools (merged-model/selected-test limits). *Done when* — Limits evidenced.

**🟡 [tool-comparison] Tool fit**
*What* — [rated-tools] Assess voice/workflow/media tools. [soundbox] Check local audio clients, resources and model licences. [hex] Compare Portuguese dictation, Linux shortcuts/paste and latency; agent invocation is separate. [hob-desktop] Compare local file/tool workflows, hardware and offline limits. *Done when* — Fit evidenced.


**🟡 [document-access] Source access**
*What* — [firecrawl] Compare Firecrawl with our existing fetch/search on representative difficult sources, recording coverage, hosting, access failures and cost; include Alexandria source/citation fidelity and freshness, not guaranteed answers. [nomad] Assess useful offline resources, language/accessibility and RAM/disk before adopting optional AI. *Done when* — Fit evidenced.


**🟡 [local-inference-options] Local inference**
*What* — [colibri-streaming] Pin JustVugg/colibri version/model; check RAM/disk, latency and tokens/s before download (high priority); old GPU lead distinct. [glm52-comparison] Match model/harness/budget; compare local/hosted cost and memory semantics. [strata-local] Memory, disk, quality on our laptop. [mesh-llm] Trusted nodes, network cost. [deepinfer] Vendor datacenter research, not laptop. [airllm] Verify Kimi-in-C, storage, seconds/token before download. [model-continuity] Provenance, licence, integrity of used models. [gpu-unlock] Check supported workloads, precision, power and whole-task results. [qwen-modified] Compare provenance/licence, hardware and quality with original; fewer refusals prove no quality gain. [twil-8b] Run TwIL-8B Q4 on the laptop: total memory, latency, quality at equal context; published scores are bf16. *Done when* — Fit evidenced.

**🟡 [academic-evidence-tools] Academic evidence intake**
*What* — Assess paginated query/date mail search, robust long attachment names, cached-email PDF evidence and official PROGEPE/federal personnel bulletin discovery. Inspect Downloads/progressao-scripts before reuse; preserve the reported progression evidence (279/2024, 1.022/2025) as attributed leads. Shared defect: ISSUES.md [b20261024-mail-search-attachments]; Claude/Codex reports, 24–28 Oct. *Why* — RDA/progression need the same reliable intake. *Done when* — A bounded evidence search retrieves its documents with provenance.

**🟢 [inbox-1117] Captured workflow tools — backlog**
*What* — [sag-wiki] 10 lookups vs grep. [cl4r1t4s-watch] Weekly diff. [apiv] Craft gaps. [expired-findings] Find the source. [merge-checks] Map to our hooks; trial osv-scanner. [rune] Render-to-PNG prototype. [token-context] One craft fix, one class. Refs: refs/REFS.md. *Done when* — Each compared with a reject criterion.

**🟢 [mcptoon-context] Tool and skill discovery — backlog**
*What* — Compare on-demand tool/skill schema discovery with current context cost/reliability; Dobra roadmap. *Why* — Lead. *Done when* — Bounded results precede adoption.


**🟢 [rea-assessment] Reverse-engineering and media demonstrations — backlog**
*What* — Identify REA/PhotoCraft/EffectCraft; compare methods, media, licences and legal claims. [cadcraft] Assess agent-controlled drawing, clients and formats; construction: ../branches/casinhas/ROADMAP-obra.md. Virada roadmap. *Why* — Repeated discovery/production. *Done when* — Evidenced transfer or rejection.


**🟢 [drive-write-guard] Protected Drive ids — backlog**
*What* — A hook refuses gdrive/gdocs writes to listed Drive ids; first, the CAPD folder. *Why* — One sentence in capd/CONTEXT.md is its only guard (11 Nov). *Done when* — A write to a listed id is refused, naming why.


**🟢 [visual-tools] Captured visual tools — backlog**
*What* — Compare Hairline/ff-tracking/Papermorph for editing, accessibility and fidelity; [web-motion] browser visual export; [anatomy] animation and sprites; [motionmaxxing] Compare one teaching animation for editability/accessibility/render cost (Instagram lead; refs/REFS.md). [t3-video] Assess hardware/licence/runtime and visual/teaching fit before a trial (Instagram lead; refs/REFS.md). [video-motion-skills] assess HyperFrames/Remotion/Manim (Sisinty Vaibhav), p5.brush (Rishi Jain) and Scenario 3D OS agent skills (refs/REFS.md). *Why* — Better teaching and agent visuals. *Done when* — Fit or rejection evidenced.

**🟢 [expert-depth] Prompt depth — backlog**
*What* — Compare the attributed Felix Rieseberg prompt with prepare/research: raw sources, methods and independent checks. *Done when* — Useful cuts or rejection.

**🟢 [modder-patterns] Universal Modder — backlog**
*What* — Assess Universal Modder discovery, live checks and field notes. *Why* — Repeated discovery. *Done when* — Transfer or rejection is evidenced.

**🟢 [provider-agnostic-clarification] Provider-agnostic governance — backlog**
*What* — Clarify core/norms/storage.md, interview.md and core/CONTEXT.md: configuration and storage are provider-independent (symlink to WIS), but execution can use any provider; external review does not restrict execution. *Why* — Harness friction (ChatGPT triage 2026-11-03). *Done when* — Updated norms approved and applied.


**🟢 [shoot-unbundle] shoot --unbundle flag — backlog**
*What* — Add --unbundle flag to tools/web/shoot to unpack base64+gzip artifacts directly. *Why* — Avoid scratchpad scripts (INBOX 2026-10-31). *Done when* — shoot --unbundle unpacks cleanly.



**🟡 Desktop hyperagent — high priority, week**
*What* — Reuse aiwbot/Dobra for voice, discovery, bounded context, routing and quotas; assess OpenHarness Linux/lineage/trust (refs/REFS.md; ../code/aiwbot/ROADMAP.md [mobile-session-relay]). [unsloth-browser] Check permissions/network and memory in one bounded browser task. [voice-studio] Compare Portuguese narration, model licence, memory, latency and export. [dessa] Verify release/access/licence and Portuguese relevance; primary page unread. *Why* — Fragmented interaction (Lucas,7 Oct; Claude,23 Oct). *Done when* — Lucas chooses a concrete design.


**🟡 MatrAIx evaluation**
*What* — Compare simulated-user testing with our checks. *Why* — Possible behavioral coverage. *Done when* — Bounded validity/limits are recorded.


**🟡 PDF throughput**
*What* — Compare description engines after pymupdf-layout change on a representative long document: latency, memory, fidelity and reading order; distinguish original/v2 [unlimited-ocr]. Refs: refs/REFS.md ([unlimited-ocr], [laws-markdown]). *Why* — Backfills take hours. *Done when* — Time, memory and fidelity evidenced. [figura-v2] (Lucas, 25 Nov): px/aspect floors; describe.py call timeout; convert with `none` + resumable "describe pending" pass. 17% of irrelevant figures still pass, mostly scanned pages (area rule) [src: agent 2026-11-25].

**🟡 Dependency checks**
*What* — Shared installation checks; assess local spreadsheet support before adding packages. Refs: refs/REFS.md ([dependency-provenance]). *Why* — Feature switches do not prove installation. *Done when* — Missing dependencies give single diagnosis.

**🟡 [drive-doc-update] Existing document updates — backlog**
*What* — Assess in-place document replacement preserving identity/history/access, including failures. Consumer: ../academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md [drive-update]. *Why* — Missing drive_core capability reported 19 Oct. *Done when* — Authorized update verifies; norms/edit.md binds originals. *Open, Lucas decides* (21 Nov, CAPD Nº 22): creating a new file per change is not workable (Lucas). There are two variants. (a) The agent rewrites only a file it created, tagged at creation with `appProperties`, and only while the head revision is still the one it wrote: the agent and Lucas share one Google account, so Drive's user fields cannot tell them apart. (b) `put --replace <id>` uploads a new version on the same id, with per-act authorization.


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
*What* — Canva: review billing and alternatives before more build work. Decide shapes/connectors versus SVG with Lucas; verify MCP grant or Apps SDK fallback. Through /craft, k10 must reproduce k1 without human clicks, oracle-verified; reread shared deck each turn. Evidence: tools/slides/SPECS.md, outputs/canva-poder-desenho.md, outputs/.drafts/canva-poder/{oracle.py,mcp_spike.py}. *Why* — Lucas prefers Canva; copied seeds retain motion. *Done when* — Verified k10 lets Lucas choose the home.

**🟡 [cross-harness-delegation] Every feature works on every harness, and delegates from any of them**
*What* — **One map** (Lucas, 2026-11-24): per harness (Claude Code, Codex, Copilot, opencode, agy, ZCode, pi, DeepSeek harness), what works — skills, hooks, session id, git wrapper, headless call, workers orchestrated from it. Lucas picked (2026-11-24, panel argon): `core/harnesses.txt` gains a column per feature, each cell naming the CLI version it was proven on, flagged at the close when that CLI moves; risk: bumping versions untested. [codex-parity] Recheck 2-Nov (../outputs/codex-audit-20261102/auditoria.md). [r-cli] Memory portability. [pstack] Completion/invariants/throughput. [context-evidence] Context/planning/checks; no invented 100k cutoff. [model-regression] Pin versions, effort, context/settings. *Why* — Agnostic, unproven. *Done when* — Every cell is proven or names its ISSUES defect; source/public checks green.



**🟡 Unslop, aihero.dev and Oil UI**
*What* — Compare heydamir/unslop audit, approved direction and revisions with aihero.dev grill-me/implement and Oil UI on one desktop/mobile screen: usability, accessibility and cost. *Why* — Leads. *Done when* — Verdicts or rejection. [ux-20] Map speech→screen items, retaining gaps; compare guidance and test changes, not universal thresholds.


**🟡 Skill size and reading cost**
*What* — Cut repeated, ambiguous or costly skill steps. [prompt-audit] Assess captured cross-provider instruction audits (refs/REFS.md); preserve active checks/requirements. [authored-drafts] Account for missing ai4good-git-retro-opus.md (2-Nov report:627 lines); cut authored drafts, no vendored exemption. ../ISSUES.md [b20260924-drafts-sync]. *Why* — Repeated skill reads (Lucas,25 Aug). *Done when* — Steps earn their reading cost.


**🟡 Skill discovery outside the workspace**
*What* — Make skills reachable outside this workspace or fail explicitly. *Why* — HOME sessions silently lack project-scoped commands (18 Aug). *Done when* — Lucas gets the skill or a refusal; review the trust cost of global links.


**🟡 Closing-action planning**
*What* — Assess moving the next closing action into the plan template. *Why* — Lucas requested one fewer closing round-trip, not automatic implementation. *Done when* — Evaluation respects the one-action text rule.


**🟢 gslides frames**
*What* — Expose element/start/end/frame-count/easing batch generation. *Why* — duplicateObject plus transforms already proved PDF-safe frame sequences (14 Aug); remaining work is ergonomics. *Done when* — Command handles both traps in tools/slides/SPECS.md.



**🟢 Trash for generated Drive files**
*What* — Add trash to gdocs/gdrive using write-token access. *Why* — Their own test creations otherwise require manual cleanup. *Done when* — CLI-created files can be trashed by the CLI.


**🟢 Claude Slides/Design comparison**
*What* — Compare Claude Slides/design with gslides/slides_build. *Why* — Lucas requested repo-to-deck assessment (27 Sep). *Done when* — Useful differences and verdict are in tools/slides/SPECS.md.


**🟢 Full-PDF review input**
*What* — Require full PDF download/extraction before peer-review simulation in flows/research/review.md. *Why* — Abstract/HTML-only review misses tables, equations and appendices (Lucas, 26 Sep). *Done when* — Review reads the binary and extracted text.


**🟢 Staged slide/animation generation**
*What* — Assess script→storyboard→visual→render with intermediate Markdown. *Why* — Van Clief reference (30 Sep). *Done when* — Convention in tools/slides/SPECS.md and a pilot demonstrate it.


**🟢 Slide visual subskills**
*What* — Assess photo search, shape drawing and styled diagrams for /slides. *Why* — Lucas requested better visuals (30 Sep). *Done when* — Each is validated on a real deck.


**🟢 Course-template backport**
*What* — Backport proven ai4good/disciplina.md refinements to the canonical template. *Why* — Share semester learning (30 Sep). *Done when* — Template retains cfpages compatibility.


**🟡 submissão interativa de artefatos por matrícula e validação no site de disciplinas**
*What* — Assess student link submission by enrolment and teacher acceptance. *Why* — Course-page intake (30 Sep). *Done when* — Prototype works on a published disciplina.md.


**🟡 compare HotClip, Drift and Clipa for local edits and captions**
*What* — Compare HotClip, Drift and Clipa on Portuguese captions, readability, editing, export and cost. *Why* — Classes/Virada production. *Done when* — tools/video records a verdict before adoption.


**🟢 avaliar iris (Rust CLI + MCP) como ferramenta de visão/câmera para os agentes do WOS**
*What* — Assess brijr/iris CLI screenshots of local/published pages. *Why* — Agent vision lead (25 Sep). *Done when* — tools/web/SPECS.md records compatibility and verdict.


**🟢 portar utilitários de slides_build.py para core/tools/slides/gslides**
*What* — Port deck splitting, slide copying, notes and images from ai4good/slides_build.py to gslides. *Why* — Reuse proved utilities (23 Sep). *Done when* — Subcommands have meaningful checks.


**🟡 migrar e sintetizar a skill /prof para en-us**
*What* — Cut and translate core/skills/prof to English, retaining Portuguese terms where needed. *Why* — Oversized invoked text (24 Sep). *Done when* — Guidance remains usable at lower reading cost.


**🟢 suportar espelhamento de subdiretórios de subskills no sync-skills**
*What* — Verify sync-skills mirrors prof/slides subfolders. *Why* — Relative subskill links must work across harnesses (24 Sep). *Done when* — Every target resolves the mirrored children.


**🟡 Write approval: the live proofs left** (2026-11-26)
*What* — Live tests of slides, forms and `docs push` with its diff, Lucas approving each; `outputs/remote-edit-gate-plan.md` items (c) the hook refuses a chained `--approve` and (d) asks before quoting `~/.config/workspace-*-write`; whether the `Bash(*--approve *)` prompt shows in auto mode (asked twice, unanswered). Test leftovers in Google (`[teste] gate drive`, `[teste] gate docs`, sheet cell Z1) go only with Lucas's OK. *Why* — Sheets, drive and docs are proven; three services are not. *Done when* — Every service has one approved live write on record.

**🟡 /inbox consumes the Brain handoff** (Lucas, 2026-11-25)
*What* — `core/skills/inbox.md`: before picking a batch, run `core/run tools/wos/handoff --take brain` once per session and fold in its pending work; none pending is not a blocker; reuse it if already taken. Handoff taking is not `wos/take` branch ownership. Sync mirrors after. *Why* — The Brain handoff was skipped by hand. *Done when* — A fresh /inbox session takes it unprompted.


**🟢 image twin: arquivo .md irmão com OCR + VLM para qualquer imagem isolada**
*What* — Assess assets/inspect --twin combining OCR, descriptions and .imgif/video captions. *Why* — Standalone images lack navigable text (25 Sep). *Done when* — A sibling Markdown is consumed by read gates.


**🟢 gdrive download --out** — explicit destination instead of Downloads (25 Sep).


**🟢 gslides WCAG contrast lint; mutool draw -w for previews** — pdftoppm crops page bounds (25 Sep).

## Blocked — waiting on a trigger

**🟢 Video-family naming** — page fallback makes this link→text, not video-only. Trigger: next related core/tools path change; tools/SPECS.md § Naming rules out an isolated third rename.

## Deferred — flows and agents, findings kept, nothing spent

Flows/agents wait for v1 (Lucas, 25 Aug); observed 24 Aug failures preserved (orchestrator reversion, router experiment gate, 18 KB routing read overhead, uncapped Loop 4b).

## Rejected

- Write approval by pid or plan age (panel, 25 Nov): every run has a new pid and 5 s proves nobody read the plan; a prompt-turn stamp does (outputs/remote-edit-gate-plan.md).
- Figure OCR vs page text as relevance rule: pymupdf puts the image's OCR in the page, so all score ~1 (25 Nov).
- Figure weights shipped in tools/pdf: fit on one corpus (25 Nov).
- Canva motion through PPTX: import/export reduce Match & Move to fade; use a copied seed (3 Oct).

- Outside-skill survey: DM-gated unlinked leads duplicated existing guidance; reopen from a real repository (25 Aug).

- Handoff consumed by a post-read hook: a section appended between read and delete would vanish; `--take` under the lock is the one door (10 Nov).

- Per-file ownership check on every write, and blocking roundup after N non-promotions: a written-files log cannot prove whose a change is, and skips had real causes (10 Nov).

<!-- routing:start -->
## Routing

| Part | Description | Items |
|------|-------------|-------|
| [`ROADMAP-workers.md`](ROADMAP-workers.md) | ← add description | `orchestrate-by-default` `wos-diet` `subscription-review` |
<!-- routing:end -->
