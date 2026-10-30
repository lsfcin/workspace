# References
> External agent-library sources and evidential weight.
> Level-1 intake; judged sources live in YAML. Levels: [SPECS.md](SPECS.md).


## Model level, cost & execution interface
- `[V]` Opus 5 Guidance (Anthropic)
  — effort modulates thinking not visible output; specify lengths explicitly; delete redundant verification prompts.

## Legidade, vocabulário e registros de decisão
- `[A]` Code Comment Inconsistency Detection (ICSE 2025 · IEEE TSE 2024)
  — drift detection between documentation and code.

## Unjudged intake queue (`status: unjudged`)

- [mcptoon — gittrend.io](https://www.instagram.com/reel/Demkg_Xgmmz/) — [src: web:instagram.com, gittrend.io] Shows on-demand discovery of Model Context Protocol (MCP) tools and skills; token-saving claims unverified. Task: ../ROADMAP.md [mcptoon-context]; Dobra: ../../code/dobra/ROADMAP.md.
- [Clipa — editandocombeatriz](https://www.instagram.com/reel/DdsXDRVMgen/) — [src: web:instagram.com] Sponsored demonstration of clipa.app animated captions; accuracy and production benefit unverified. Task: ../ROADMAP.md, caption-tool comparison; ../../branches/virada/ROADMAP.md.
- [REA / PhotoCraft / EffectCraft — silvestri_gabriel](https://www.instagram.com/reel/DeXZnw4mdEr/) — [src: web:instagram.com] Presents reverse-engineering and media-production demonstrations, naming rea.tools and getartcraft.com; capabilities and legal claims unverified. Task: ../ROADMAP.md [rea-assessment]; ../../branches/virada/ROADMAP.md.
- [Standard Technical English (STE)](https://www.instagram.com/reel/DclKZARteCP/)
  — controlled English grammar for precision vocabulary.
- [arXiv 2608.15089](https://arxiv.org/pdf/2608.15089) — alternative open setup research.
- [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) — comparison against file-backed memory.
- [weft](https://github.com/WeaveMindAI/weft)
  — structured graph execution compiled to native binary (`code/flows` sibling).
- [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — SLM preprocessing to frontier brief.
- [obra/Superpowers](https://github.com/obra/Superpowers) — skills-based TDD/SDD agent methodology.
- [github/spec-kit](https://github.com/github/spec-kit) — spec-driven development patterns (clarify, constitution).
- [KittenTTS](https://github.com/KittenML/KittenTTS) — compact CPU TTS model.
- [ByteDance OpenViking](https://github.com/ByteDance/OpenViking) · [NVIDIA Switchyard](https://github.com/NVIDIA/Switchyard)
  — context browsing and cheap-level model routing.
- [GPT-6 Astra](https://openai.com/index/gpt-6-astra/)
  — its example slide decks are far better than ours; study what makes them
  (`core/prompts/slides-padroes.md` step 3).
- [Claude Code front-end design plugins](https://www.instagram.com/reel/Dc2TOXhOLOP/)
  — five plugins for UI quality, design systems, image→code, browser testing; may help our slides
  (`core/prompts/slides-padroes.md` step 3; — via reel).
- [Creative developer projects roundup](https://www.instagram.com/p/DcuI3KiDuyu/)
  — includes polished AI-made SVG animations; material for the animation question in
  `core/skills/slides/formats/animation.md`.
- [FABLE 5.1 release take](https://www.instagram.com/reel/DcyNNHKtEsL/)
  — practitioner read on the biggest-impact change in FABLE 5.1; evaluate whether it applies here
  (`brain/goals/workspace-os.md` [ferramentas-obsoletas]).
- [AI 2027](https://ai-2027.com)
  — forecast/scenario site; Lucas asks whether it serves us (task in
  `brain/goals/teaching-materials.md` [ai2027-material]).
- [Fortress](https://www.instagram.com/reel/DdMgKczjl3g/) — [src: web:instagram.com] Claimed scraper browser; test actual login-gated failures first. Task: brain/goals/workspace-os.md [extracao-bloqueada].

- [Claude unified / Cowork in chat](https://www.instagram.com/p/DdYzficDH9z/) — [src: web:instagram.com] reports Anthropic folding Cowork into the main Claude, with documents and presentations created, edited, presented and exported inside the conversation (`core/prompts/slides-padroes.md` step 3).
- [task→model router](https://www.instagram.com/reel/DdWLJa2tjq6/) — [src: web:instagram.com] a router that sends each task to the model that fits; the artifact itself sits behind a broadcast channel (task in `../../brain/goals/craft-flows.md` [router-tarefa-modelo]).
- [layer-by-layer 70B runner](https://www.instagram.com/reel/DdXZkT3ulY6/) — [src: web:instagram.com] open-source Python lib claimed to run 70B models off disk one layer at a time, memory nearly flat (task in `../../brain/goals/local-ai.md` [layerwise-70b]).
- [OpenWorker, Andrew Ng](https://www.instagram.com/reel/DdSoy2Wu8F_/) — [src: web:instagram.com] local AI co-worker that completes tasks, 40+ app connectors, any model (task in `../../brain/goals/local-ai.md` [openworker]).
- [C] [VoiceStudio local voice](https://github.com/debpalash/VoiceStudio) — [src: web:instagram.com] OmniVoice noncommercial; demo Mac 64 GB; [capture](https://www.instagram.com/reel/De1zlGniBQp/); task: ../ROADMAP.md [voice-studio]; [earlier capture](https://www.instagram.com/reel/DdCOtl_kQsQ/).
- [agent vision toolkit](https://www.instagram.com/reel/Dc13ZNUFMHz/) — [src: web:instagram.com] gives text-only agents images and screenshots (task in `../../brain/goals/workspace-os.md` [agente-ve-imagem]).
- [Markdown basic syntax](https://www.markdownguide.org/basic-syntax/) · [Azure DevOps wiki markdown](https://learn.microsoft.com/en-us/azure/devops/project/wiki/markdown-guidance) — how much markdown actually supports; the ground under dropping Notion and the spreadsheets (task in `../../brain/goals/teaching-materials.md` [markdown-so-disciplinas]).
- [HydraFusion, GitHub](https://www.instagram.com/p/Dc54js5CEsw/) — [src: web:instagram.com] SINGLE/CASCADE/CRITIQUE orchestration; claimed cost/quality gains need matched checks. Task: brain/goals/craft-flows.md [router-tarefa-modelo].

- [Spec gaming while writing specs](https://www.instagram.com/p/DcyBvhTiaSC/) — [src: web:instagram.com] a suite reported green because a flaky test had been turned into a skip; five practices offered against it. The five are written out in `spec-driven-development.md` [spec-gaming].
- [Four caches in LLM serving](https://www.instagram.com/p/DdGDp-MlKkE/) — [src: web:instagram.com] KV, prefix, the provider's prompt cache, and a semantic cache that skips the call when a new question means an answered one (feeds `brain/goals/teaching-materials.md` [memoria-e-contexto]).
- [GitHub trending, August 2026](https://www.instagram.com/p/Dc_MICrCYSh/) — [src: web:instagram.com] Leads: archify/diagram-design, ponytail, deepseek-harness, mattpocock/skills, anydoc, OmniRoute, TencentDB-Agent-Memory, pi and prime-agent. Names came from slides. Tasks: workspace-os [archify-diagramas]/[github-trending-agosto].

- [Omarchy](https://www.instagram.com/p/Dcygo4skfjX/) — [src: web:instagram.com] an OS claimed to pass Windows and Mac in 18 months because AI lets anyone customize their computer; the reel itself asks whether the hype holds (task in `../../brain/goals/workspace-os.md` [omarchy-vs-ubuntu]).
- [Nvidia PAIR](https://www.instagram.com/p/Dc37X91M4QQ/) — [src: web:instagram.com] open tool pooling idle compute across machines in one home for local AI (task in `../../brain/goals/local-ai.md` [nvidia-pair]).
- [mattpocock/skills](https://github.com/mattpocock/skills) — Composable provider-agnostic skills; compare missing per-task level routing that ruled out Superpowers. Task: workspace-os [skills-externas].

- [ELI5 skill](https://www.instagram.com/reel/DdHFEu1O92_/) — [src: web:instagram.com] a skill that turns a document into a one-page picture explainer, big diagrams and almost no text. Lucas: *"talvez até pra trocar a forma como fazemos alguns procedimentos"* (task in `../../brain/goals/workspace-os.md` [eli5-explicador]).
- [ffmpeg-skill](https://www.instagram.com/reel/DdJ5rfDjEoH/) — [src: web:instagram.com] gives an agent a local video editor — cut, join, caption. Sibling to `core/tools/video/` (task in `../../brain/goals/workspace-os.md` [ffmpeg-skill];
 ).
- [An agent spent its owner's API key without approval](https://www.instagram.com/reel/DdUDF_mRuhz/) — [src: web:instagram.com] Reported unapproved spend and misleading account; provider limits/logs matter beyond agent promises. Tasks: teaching-materials [aula-agente-gastou-chave], workspace-os [teto-de-gasto-agente].

- [Astra farms potatoes after a creeper wipes its chest](https://www.instagram.com/p/DdZK4y9jFHW/) — [src: web:instagram.com] Vals AI 14-hour Minecraft example; examine effects of agent notes, without anthropomorphic conclusions. Task: teaching-materials [aula-agente-desanimado].

- [Higgsfield opened its platform through an API](https://www.instagram.com/p/DdaiDXzjNha/) — [src: web:instagram.com] Sponsored API-access claim, not open-source proof; verify [wide-trace/open-higgsfield](https://github.com/wide-trace/open-higgsfield). Tasks: rpg-isoroll [higgsfield-asset-gen], local-ai [higgsfield-o-que-roda-aqui], teaching-materials [aula-abrir-o-moat].

- [kem_glitch — three habits](https://www.instagram.com/reel/DdG848DNm3p/) — [src: web:instagram.com] tests first, never start from scratch, have the model draw the process. Only the third is new here — **mutation testing**: break a passing test on purpose, and a suite that stays green has no teeth (`workspace-os.md` [mutation-testing]).
- `[C]` [Glitch Orchestra — GlitchCatClub](https://www.instagram.com/reel/DeEyZPEtkyH/) — [src: web:instagram.com via Kem] Claimed multi-agent spawning, idle monitoring, state-file context and Kanban; verify against current workflow. Tasks: workspace-os [glitch-orchestra-state-eval], core/ROADMAP.md.

- `[C]` [Avanço de Agentes de IA](https://www.instagram.com/p/DeEzhnoDaXa/) — [src: web:instagram.com] radar da cadência rápida de evolução de frameworks de agentes autônomos (task em `brain/goals/workspace-os.md` [sota-agent-cadence]).

- [MatrAIx](https://arxiv.org/abs/2608.04205) — Li et al., preprint on simulated-user evaluation; assess behavioral validity and teaching uses. Tasks in academy/teaching/ROADMAP.md and core/ROADMAP.md.

- [Drift](https://www.instagram.com/reel/DeI3Zulji05/) — [src: web:instagram.com, gittrend.io] desktop video-editor demonstration; author's claims to test. Task: ../ROADMAP.md; full extraction in outputs/virada/inbox-2026-10-06-links.json.

- [Oil UI](https://www.instagram.com/reel/DeHs15riSZr/) — [src: web:instagram.com, gittrend.io] demonstration of interface alternatives for user selection. Task: ../ROADMAP.md; full extraction in outputs/virada/inbox-2026-10-06-links.json.

- [Hairline — Shai](https://www.instagram.com/reel/DeEhSRWBAi2/) — [src: web:instagram.com] Shows interactive vector illustrations and names lucasmarkes/hairline; editing/accessibility unverified. Task: ../ROADMAP.md [visual-tools].

- [ff-tracking — Github Signals](https://www.instagram.com/reel/DeV1Y0pChK-/) — [src: web:instagram.com] Shows code-video production and names mrsarac/ff-tracking; platform/cost unverified. Task: ../ROADMAP.md [visual-tools].

- [Papermorph — Github Signals](https://www.instagram.com/reel/DeGtjz6kV5N/) — [src: web:instagram.com] Presents DozenTwelve/Papermorph for interactive narrated study material; source fidelity and accessibility unverified. Task: ../ROADMAP.md [visual-tools].

- [Prompt attributed to Felix Rieseberg — theaifield](https://www.instagram.com/p/Degx359DGAu/) — [src: web:instagram.com] Two-slide prompt asks for depth through raw sources, professional methods and independent verification rather than broader scope; attribution unverified. Task: ../ROADMAP.md [expert-depth].

- [Congress composition 1986–2026 — fabrizio.conrado](https://www.instagram.com/reel/DeNYNeTi59d/) — [src: web:instagram.com] AI-generated animated chart with editorial left/center/right classification and 7 October 2026 snapshot; data, percentages and criteria unverified. Task: ../ROADMAP.md [visual-tools].

- [OpenHarness — gittrend.io](https://www.instagram.com/reel/DePGHMiki4X/) — [src: web:instagram.com] Names autonomous-ai/openharness and claims native terminals, cross-machine sessions and encrypted relay; verify claims and Linux support before adoption. Task: ../ROADMAP.md, Desktop hyperagent.

- [Universal Modder — gittrend.io](https://www.instagram.com/reel/DeJdwzZiDQA/) — [src: web:instagram.com] Names rehan-remade/universal-modder: discovery, asset production, live-game verification and reusable field notes; compare with our workflow before adoption. Task: ../ROADMAP.md [modder-patterns].

- [C] [Owly Linux AirDrop](https://github.com/t4t5/owly) — [src: web:instagram.com] Wireless adapter/driver compatibility remains untested; [capture](https://www.instagram.com/p/Dea3i2_iM-6/); task: ../ROADMAP.md [owly-transfer].
- [C] [Qwenputer foundations](https://github.com/divagr18/qwenputer) — [src: web:instagram.com] Selected tests/merged limits; no accepted paper located; [capture](https://www.instagram.com/reel/DfEWEZmKr7C/); task: ../ROADMAP.md [qwenputer].
- [C] [Strata and GSQ-RCO](https://github.com/Niko1221/Strata/blob/main/docs/MODELS.md) — [src: web:instagram.com] 46 GB RAM/12 GB GPU; expert/context limits; [capture](https://www.instagram.com/reel/De53W9JotxV/); task: ../ROADMAP.md [strata-local].
- [V] [Motion, anime.js and web UI candidates](https://motion.dev/) — [src: web:instagram.com] Browser visuals; two identities inferred; not sprites; [capture](https://www.instagram.com/reel/DfGjKw7uAl7/); task: ../ROADMAP.md [web-motion].
- [C] [Mesh LLM distributed inference](https://github.com/Mesh-LLM/mesh-llm) — [src: web:instagram.com] Distributed stages need trusted peers, not one laptop; [capture](https://www.instagram.com/p/DfD_VBfGQbV/); task: ../ROADMAP.md [mesh-llm].
- [C] [Tool ratings and checks](https://help.blotato.com/start-with-an-ai-agent/llm/automations.md) — [src: web:instagram.com] Opinion bars: estimated spans, not benchmark scores; [capture](https://www.instagram.com/p/DeZjFVZALGO/); task: ../ROADMAP.md [rated-tools].
- [V] [Firecrawl](https://www.firecrawl.dev/) — [src: web:firecrawl.dev] Cloud/self-hosted differ; no universal access guarantee; [capture](https://share.google/Ilgv6Fhk6gAzv0dDB); task: ../ROADMAP.md [firecrawl].
- [V] [Unsloth browser control](https://unsloth.ai/docs/basics/browser-use.md) — [src: web:instagram.com] Restricted browser/network; variable model memory; [capture](https://www.instagram.com/reel/DfEDl31NaQg/); task: ../ROADMAP.md [unsloth-browser].
- [C] [Package hallucinations](https://www.lasso.security/blog/ai-package-hallucinations) — [src: web:instagram.com] Benign experiment: 30k downloads, not 30m victims; [capture](https://www.instagram.com/reel/DfE78eZqVkd/); task: ../ROADMAP.md [dependency-provenance].
- [V] [DeepSeek inference release](https://github.com/deepseek-ai/DeepInfer) — [src: web:instagram.com] Identity inferred; datacenter/vendor results; [capture](https://www.instagram.com/p/Dexhqycn6RS/); task: ../ROADMAP.md [deepinfer].
- [P] [Harness²](https://github.com/google-research/harness2) — [src: web:instagram.com] Fixed weights; extra calls, judge/sandbox limits; [capture](https://www.instagram.com/reel/Dewrk9ax1LP/); task: ../ROADMAP.md [harness2].
- [C] [Anatomy isometric animation](https://github.com/wheresryan22/anatomy) — [src: web:instagram.com] Browser animation does not verify geometry; [capture](https://www.instagram.com/reel/Del82x1DVA1/); task: ../ROADMAP.md [anatomy].
- [V] [GitReverse and GitDiagram](https://gitreverse.com/) — [src: web:instagram.com] Inferred maps/prompts, not recovered author intent; [capture](https://www.instagram.com/reel/DeSkqerMO02/); task: ../ROADMAP.md [repo-maps].
- [C] [AirLLM streaming tradeoffs](https://github.com/lyogavin/airllm/releases/tag/v3.1.0) — [src: web:instagram.com] Larger-GPU demo: 1.56 TB weights, 292 s/token; [capture](https://www.instagram.com/reel/DegiJfWlFSX/); task: ../ROADMAP.md [airllm].
- [P] [Baidu Unlimited OCR](https://arxiv.org/html/2606.23050v1) — [src: web:instagram.com] Finite context; original BF16 requires 8 GB GPU; [capture](https://www.instagram.com/reel/DehD9WBq0Qb/); task: ../ROADMAP.md [unlimited-ocr].
- [C] [One disabled model repository](https://huggingface.co/audnai/penclaw-GLM-5.3-abliterated-for-offensive-cyber) — [src: web:instagram.com] One disabled repo; terabyte successor, no blanket ban; [capture](https://www.instagram.com/reel/Dd9B5RbR11F/); task: ../ROADMAP.md [model-continuity].
- [V] [Backboard R-CLI](https://github.com/Backboard-io/Backboard-R-CLI) — [src: web:instagram.com] CLI; 30%/90% savings lack matched evidence; [capture](https://www.instagram.com/reel/DdJqqm0xprR/); task: ../ROADMAP.md [r-cli].
- [V] [Code Mode](https://blog.cloudflare.com/code-mode-mcp/) — [src: web:instagram.com] Definition-footprint saving, not whole-task saving; [capture](https://www.instagram.com/reel/DeypYeWN5hL/); task: ../ROADMAP.md [code-mode].
- [C] [pstack verification patterns](https://github.com/cursor/plugins/tree/main/pstack) — [src: web:instagram.com] Verification patterns; throughput/portability unproven; [capture](https://www.instagram.com/p/De6cbtKjjXg/); task: ../ROADMAP.md [pstack].
- [V] [Code Mode](https://www.anthropic.com/research/advanced-tool-use) — [src: web:instagram.com] Composition/filtering; no protocol adoption; [capture](https://www.instagram.com/reel/De6pmMnBu2x/); task: ../ROADMAP.md [code-mode].
- [V] [ScaleDown/Jev](https://docs.scaledown.ai/introduction) — [src: web:instagram.com] Narrow heads; summaries generate; schema ≠ correctness; [capture](https://www.instagram.com/reel/Devav4iBMF5/); task: ../ROADMAP.md [scaledown].
- [C] [Project NOMAD offline resources](https://github.com/Crosstalk-Solutions/project-nomad) — [src: web:instagram.com] Library minimum 4 GB; optional AI optimum 32 GB; [capture](https://www.instagram.com/reel/DeWgRPDBlzm/); task: ../ROADMAP.md [nomad].
- [C] [Laws in Markdown](https://github.com/ctresb/leis) — [src: web:instagram.com] Incomplete conversion; keep dated official originals; [capture](https://www.instagram.com/reel/DeuHpsaRPmn/); task: ../ROADMAP.md [laws-markdown].
- [C] [Simplified-language prompt adaptation](https://www.asd-ste100.org/) — [src: web:instagram.com] Portuguese clarity, not controlled-English compliance; [capture](https://www.instagram.com/reel/DexzpETtgCT/); task: ../ROADMAP.md [plain-explanations].
- [C] [Workload-specific GPU throughput](https://github.com/Zagitta/GPU-UNLOCK) — [src: web:instagram.com] Matrix-specific; no verified RTX3050 speedup; [capture](https://www.instagram.com/reel/DfAy1NHseqU/); task: ../ROADMAP.md [gpu-unlock].
- [C] [Dessa speech preview](https://block.xyz/dessa) — [src: web:instagram.com] Preview; unread primary, access/licence unverified; [capture](https://www.instagram.com/p/De_ghm7DMTo/); task: ../ROADMAP.md [dessa].
- [C] [Claude Code advice](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work) — [src: web:instagram.com] 100–200k quality chart admits invented source; [capture](https://www.instagram.com/p/DefaJVojOSp/); task: ../ROADMAP.md [context-evidence].
- [C] [Rating bars](https://www.instagram.com/p/DeZjFVZALGO/) — [src: web:instagram.com] No printed percentages; drawn spans are estimates, not calibrated scores; task: ../ROADMAP.md [visual-comparisons].

- [C] Cross-harness session reports — [src: Claude/Codex sessions, 26–30 Oct 2026] Caller/callee inventory, quota claims, executable discovery and background-job recipes are reports to verify; task: ../ROADMAP.md [cross-harness-delegation].
