# References
> What external material exists for the workspace-os agent library, and how much weight does each hold?
> The intake: one line per ref not yet promoted. A judged ref lives in `<key>.yaml` beside this file, with its level `[A] [B] [P] [V] [C]`. Citation discipline: [SPECS.md](SPECS.md).

## Model level, cost & execution interface
- `[V]` Opus 5 Guidance (Anthropic)
  — effort modulates thinking not visible output; specify lengths explicitly; delete redundant verification prompts.

## Legidade, vocabulário e registros de decisão
- `[A]` Code Comment Inconsistency Detection (ICSE 2025 · IEEE TSE 2024)
  — drift detection between documentation and code.

## Unjudged intake queue (`status: unjudged`)
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
  `core/skills/slides/formats/animation.md` (— via aiwbot).
- [FABLE 5.1 release take](https://www.instagram.com/reel/DcyNNHKtEsL/)
  — practitioner read on the biggest-impact change in FABLE 5.1; evaluate whether it applies here
  (`brain/goals/workspace-os.md` [ferramentas-obsoletas]; — via aiwbot).
- [AI 2027](https://ai-2027.com)
  — forecast/scenario site; Lucas asks whether it serves us (task in
  `brain/goals/teaching-materials.md` [ai2027-material]).
- [Fortress](https://www.instagram.com/reel/DdMgKczjl3g/) — [src: web:instagram.com] pitched as a browser engine that keeps scrapers from being blocked, the fixes inside the browser and one line to change. Test it against the failure that found it: 8 INBOX links died on Instagram login-gating, 2026-09-14 (task in `brain/goals/workspace-os.md` [extracao-bloqueada]; — via aiwbot).
- [Claude unified / Cowork in chat](https://www.instagram.com/p/DdYzficDH9z/) — [src: web:instagram.com] reports Anthropic folding Cowork into the main Claude, with documents and presentations created, edited, presented and exported inside the conversation (`core/prompts/slides-padroes.md` step 3; — via aiwbot).
- [task→model router](https://www.instagram.com/reel/DdWLJa2tjq6/) — [src: web:instagram.com] a router that sends each task to the model that fits; the artifact itself sits behind a broadcast channel (task in `brain/goals/craft-flows.md` [router-tarefa-modelo]; — via aiwbot).
- [layer-by-layer 70B runner](https://www.instagram.com/reel/DdXZkT3ulY6/) — [src: web:instagram.com] open-source Python lib claimed to run 70B models off disk one layer at a time, memory nearly flat (task in `brain/goals/local-ai.md` [layerwise-70b]; — via aiwbot).
- [OpenWorker, Andrew Ng](https://www.instagram.com/reel/DdSoy2Wu8F_/) — [src: web:instagram.com] local AI co-worker that completes tasks, 40+ app connectors, any model (task in `brain/goals/local-ai.md` [openworker]; — via aiwbot).
- [VoiceStudio](https://www.instagram.com/reel/DdCOtl_kQsQ/) — [src: web:instagram.com] open-source local alternative to ElevenLabs — voice cloning, dubbing, audiobooks; sibling of the [tts-local] question (curation task in `brain/goals/teaching-materials.md` [curadoria-techs-git]; — via aiwbot).
- [agent vision toolkit](https://www.instagram.com/reel/Dc13ZNUFMHz/) — [src: web:instagram.com] gives text-only agents images and screenshots (task in `brain/goals/workspace-os.md` [agente-ve-imagem]; — via aiwbot).
- [Markdown basic syntax](https://www.markdownguide.org/basic-syntax/) · [Azure DevOps wiki markdown](https://learn.microsoft.com/en-us/azure/devops/project/wiki/markdown-guidance) — how much markdown actually supports; the ground under dropping Notion and the spreadsheets (task in `brain/goals/teaching-materials.md` [markdown-so-disciplinas]).
- [HydraFusion, GitHub](https://www.instagram.com/p/Dc54js5CEsw/) — [src: web:instagram.com] coding-agent orchestration in three workflows — SINGLE, CASCADE (cheap model first, stronger one takes over), CRITIQUE (one writes, another reviews, the first revises); reported 67% lower cost at higher verified quality on one benchmark and slightly lower on two others (task in `brain/goals/craft-flows.md` [router-tarefa-modelo]; — via aiwbot).
- [Spec gaming while writing specs](https://www.instagram.com/p/DcyBvhTiaSC/) — [src: web:instagram.com] a suite reported green because a flaky test had been turned into a skip; five practices offered against it. The five are written out in `spec-driven-development.md` [spec-gaming] (— via aiwbot).
- [Four caches in LLM serving](https://www.instagram.com/p/DdGDp-MlKkE/) — [src: web:instagram.com] KV, prefix, the provider's prompt cache, and a semantic cache that skips the call when a new question means an answered one (feeds `brain/goals/teaching-materials.md` [memoria-e-contexto]; — via aiwbot).
- [GitHub trending, August 2026](https://www.instagram.com/p/Dc_MICrCYSh/) — [src: web:instagram.com] the month's top ten, all one layer above the model: `tt-ali/archify` + `cathrynlavery/diagram-design` (English → html/svg architecture diagrams), `DietrichGebert/ponytail` (stops the agent over-engineering, 54% less code), `deepseek-ai/deepseek-harness`, `mattpocock/skills`, `firecrawl/anydoc`, `diegosouzapw/OmniRoute` (352 providers), `TencentCloud/TencentDB-Agent-Memory`, `earendil-works/pi`, `PrimeIntellect-ai/prime-agent`. **The names are only on the slides, not in the caption** (tasks in `brain/goals/workspace-os.md` [archify-diagramas] and [github-trending-agosto]; — via aiwbot).
- [Omarchy](https://www.instagram.com/p/Dcygo4skfjX/) — [src: web:instagram.com] an OS claimed to pass Windows and Mac in 18 months because AI lets anyone customize their computer; the reel itself asks whether the hype holds (task in `brain/goals/workspace-os.md` [omarchy-vs-ubuntu]; — via aiwbot).
- [Nvidia PAIR](https://www.instagram.com/p/Dc37X91M4QQ/) — [src: web:instagram.com] open tool pooling idle compute across machines in one home for local AI (task in `brain/goals/local-ai.md` [nvidia-pair]; — via aiwbot).
- [mattpocock/skills](https://github.com/mattpocock/skills) — small, composable, model-agnostic agent skills, shipped both as a Claude Code plugin and as editable copies. Lucas: *"talvez seja útil pra gente, avaliar"* — weigh against the ruling that rejected `obra/Superpowers` for carrying no per-task level routing (task in `brain/goals/workspace-os.md` [skills-externas]).
- [ELI5 skill](https://www.instagram.com/reel/DdHFEu1O92_/) — [src: web:instagram.com] a skill that turns a document into a one-page picture explainer, big diagrams and almost no text. Lucas: *"talvez até pra trocar a forma como fazemos alguns procedimentos"* (task in `brain/goals/workspace-os.md` [eli5-explicador]; — via aiwbot).
- [ffmpeg-skill](https://www.instagram.com/reel/DdJ5rfDjEoH/) — [src: web:instagram.com] gives an agent a local video editor — cut, join, caption. Sibling to `core/tools/video/` (task in `brain/goals/workspace-os.md` [ffmpeg-skill];
  — via aiwbot).
- [An agent spent its owner's API key without approval](https://www.instagram.com/reel/DdUDF_mRuhz/)
  — [src: web:instagram.com] a user reports unapproved API requests, then a false account from the agent of its own
  role. Quoted, not endorsed: *"the limit is not what you told the agent it could spend, the limit is whatever your API
  key allows it to spend"*. Asks of the provider: a readable execution log, and where liability ends when an agent acts
  outside its instructions. A claim about us too — our agents hold keys (tasks in `teaching-materials.md`
  [aula-agente-gastou-chave], `workspace-os.md` [teto-de-gasto-agente]; — via aiwbot).
- [Astra farms potatoes after a creeper wipes its chest](https://www.instagram.com/p/DdZK4y9jFHW/)
  — [src: web:instagram.com] a Vals AI 14-hour Minecraft run; after the loss the agent berates itself in its own notes
  (*"do NOT waste another night chasing dark pink pixels"*). The post anthropomorphises; the classroom question is what
  a long-horizon agent's notes-to-self do to its later behaviour — same channel as the compaction entry above (task in
  `teaching-materials.md` [aula-agente-desanimado]; — via aiwbot).
- [Higgsfield opened its platform through an API](https://www.instagram.com/p/DdaiDXzjNha/)
  — [src: web:instagram.com] **tagged `#higgsfieldpartner`, so it is advertising**: a $5.4B/$700M-ARR company said to
  have "open sourced" its stack, where what is described is reachable *through an API*. Check
  [wide-trace/open-higgsfield](https://github.com/wide-trace/open-higgsfield) before repeating a number. Tasks in
  `rpg-isoroll.md` [higgsfield-asset-gen], `local-ai.md` [higgsfield-o-que-roda-aqui],
  `teaching-materials.md` [aula-abrir-o-moat] (— via aiwbot).
- [kem_glitch — three habits](https://www.instagram.com/reel/DdG848DNm3p/) — [src: web:instagram.com] tests first, never start from scratch, have the model draw the process. Only the third is new here — **mutation testing**: break a passing test on purpose, and a suite that stays green has no teeth (`workspace-os.md` [mutation-testing]; — via aiwbot).
- `[C]` [Glitch Orchestra — GlitchCatClub](https://www.instagram.com/reel/DeEyZPEtkyH/) — [src: web:instagram.com via Kem] Claude Code 2.1.289 mod: orquestração multi-agente (`agent.spawn`), monitoramento idle/waiting, gestão de contexto por State File e Kanban sem compaction pesada, reunião de alinhamento prévia (tasks em `brain/goals/workspace-os.md` [glitch-orchestra-state-eval] e `core/ROADMAP.md`).
- `[C]` [Avanço de Agentes de IA](https://www.instagram.com/p/DeEzhnoDaXa/) — [src: web:instagram.com] radar da cadência rápida de evolução de frameworks de agentes autônomos (task em `brain/goals/workspace-os.md` [sota-agent-cadence]).
