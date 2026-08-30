# The intake queue
> Captured but not yet judged: a link earns its tier when promoted.
> answers: what has been captured and still owes a tier marker

## Unjudged — `status: unjudged`

Candidates to try, not references to read. Nothing here has been assessed, so nothing here may be
cited or used to justify a decision. Promote a winner by moving its line up into a judged section
with a tier marker; kill the rest by deleting the line.

### Frameworks / methods
- [arXiv 2608.15089](https://arxiv.org/pdf/2608.15089) — **captured twice** (INBOX 2026-08-21 and
  again 2026-08-24), which is itself the signal. Lucas's two notes together: *"adicionar aos refs e
  testar"* and *"paper que pode ser importante pra gente, pra trazer um setup alternativo gratuito"*.
  So the assessment is not "is it good" but **does it yield a free setup we do not already have** —
  which makes it `code/freeai`'s question, not the scaffold's. Nothing here has been read yet; the
  title is not even recorded, so step one is opening it.
- [akitaonrails — "harness/loop/graph engineering são
  bullshit"](https://akitaonrails.com/2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit/)
  · [his LLM benchmark
  post](https://akitaonrails.com/2026/08/15/llm-benchmarks-qwen-3-8-glm-5-3-gemini-3-7/) — a hostile
  read of exactly what this workspace is. Lucas (INBOX 2026-08-21): *"vamo aproveitar a provocação,
  estudar com carinho"*, then classify every WOS feature as useful or noise **in levels** (leve /
  médio / alto). Assessment task lives on `ROADMAP.md` item 1 — it is ablation input,
  not a separate study. **Read the benchmark post as a method, not as numbers**: model ids in it
  went stale the week it was written.
- [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) — captured with one question
  attached (Lucas, same capture): does it *help* the WOS or *duplicate* it? `brain/memory/` already
  has a measured answer to the fold-it-away question
  (`core/experiments/context-window.md`), so the honest comparison is against that, not against
  nothing. Assessment task: same roadmap row.
- [weft](https://github.com/WeaveMindAI/weft) · [node docs](https://weavemind.ai/docs/nodes) — node
  language; test the principles or the language itself. **Captured a second time 2026-08-19** —
  Lucas: *"weave again, we should at least try it at some point"*; the repeat is itself the signal.
  Claimed shape, per the source: build AI systems as structured graphs instead of thousands of lines
  of Python, compiled to native Rust. That is `code/flows` restated by someone else, which is what
  makes it worth an hour — assessment task tracked in `code/flows/ROADMAP-flows.md`
- [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) — assistant framework
- [claude-code + remotion animations (van
  Clief)](https://www.skool.com/cliefnotes/classroom/d3907117?md=f7a33a9888604a08a7e48bb876682691) —
  tutorial; feeds the animation-generator project idea
- Jake van Clief — folders-replace-agents method:
  [classroom](https://www.skool.com/cliefnotes/classroom/036893d9?md=2b4a8ab7461c4f6d828e21c0eb196a6a)
  · [folder structure
  video](https://www.skool.com/cliefnotes/new-video-how-i-structure-folders-to-replace-ai-agents)
- [Claude Code skills for UI animation](https://www.instagram.com/p/Da7y0g3DLWT/) — 3D scenes,
  scroll effects, Lottie. ⚠ DM-bait post, no links delivered; the *idea* is the value
- [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — cheap model reads
  everything and compresses to one briefing, expensive model sees only the briefing. Same tiering
  the craft flow does
- [Charlie Hills — match-the-model-to-the-job routing](https://www.instagram.com/p/DbHGtXoCOm-/) —
  9-step workflow: high tier plans, mid builds, low does grunt work, then **two judges** review and
  every catch is logged back so the setup compounds. The two-judge review and log-every-catch angles
  are the new bits
- [opensession.co — PRD-driven agent
  orchestration](https://www.instagram.com/opensession.co/reel/DXwl0ryhbgV/) — PRDs → task briefs,
  planning over hundreds of tasks, configurable model routing; 22 agents / 11 commands / 8 skills.
  Compare against our flows before importing
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) +
  [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) — Lucas: *"muito
  ruído, mas talvez algo útil pro wos"*
- [meta-harness (Yoonho Lee)](https://yoonholee.com/meta-harness/) — Lucas: *"VERY INTERESTING,
  maybe an alternative or improvement over Claude Code"*; read seriously as a harness-design
  candidate
- [Vyzual — weekly ship log](https://www.instagram.com/p/DbIo0eaErW9/) — per-agent effort levels
  (low→max) as the cheapest multi-agent lever, live simulator pane, screen-reader mode,
  security-scanner plugin. Effort levels bear directly on our subagent cost

### Data / ingestion
- [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) — 0.015s/page
  PDF parsing on CPU. Candidate backend for `core/tools/paper/parse`, which exists and is slower.
  **Parse, not OCR** — does not solve the image-only PDFs

### Models / runtimes
- [Echo](https://www.instagram.com/reel/Db1fYnbyoAX/) — claims it beat Claude Fable on a coding
  benchmark at 40% less cost by running several open-weight models at once, allocating compute
  dynamically and merging outputs. Lucas: *"será que vale um teste?"* ⚠ vendor claim relayed by a
  third-party account, no benchmark named — assessment task tracked in `/ROADMAP.md`
- [seven open-source releases, week of 2026-08-17](https://www.instagram.com/reel/DcJ3PUDyIvS/) —
  relayed claim of a Chinese Opus-level model running fully local and free, plus releases from Meta,
  xAI, Zhipu and Alibaba; watermark removal and browser-driven site cloning among the tools. Lucas:
  *"interessado especialmente nos casos em que podemos rodar algo localmente"* ⚠ no model named, no
  benchmark — the value is the pointer to that week, not the claim — backlog item in
  `brain/goals/local-ai.md`
- kimi 2.6 · kimi 2.7 · GLM-5.2 · moonshot AI · qwen code
- airLLM + Qwen3.6 (14B–20B) and/or Laguna XS.2; LFM2.5
- turbovec (google compressions, 31b → 4b)
- [Qwen3.6-27B 1-bit / ternary](https://www.instagram.com/reel/Da0UiHfsvUk/) — 54GB fp16 → 3.9GB at
  1-bit, 5.9GB ternary, architecture untouched. Phone-viable
- [KittenTTS](https://github.com/KittenML/KittenTTS) — TTS under 25MB, CPU, free. ⚠ pt-BR support
  unverified — check that first, it decides everything

### Agents / tools
- claude council · ECC · odysseus (pewdiepie) · hermes agent · higgsfield mcp
- [five repos that gained 20k stars in a week](https://www.instagram.com/p/DcURStsG5o8/) — [src:
  web:instagram.com] as claimed by the post, unverified: **diagram-design** (Claude Code skill, 39
  editorial diagram types), **omarchy** (DHH), **Cactus Compute** (14MB tool-calling model, runs on a
  Pi), **ByteDance OpenViking** (context database an agent browses like a filesystem; claims Claude
  Code recall 57% → 80%), **NVIDIA Switchyard** (routes easy agent calls to cheap models, −74% task
  cost in their own eval). The last two touch fronts we own — memory, and cheap-tier routing

### Shipping an agent-written app
- `[C]` [20 things to have Claude do before launching your
  app](https://www.instagram.com/reel/Db9aX8rhfhU/) — Michael Ly's pre-launch security checklist for
  vibe-coded apps, quoted from the reel: hide API keys, purge git secrets, public DB key only,
  enable RLS, encrypt sensitive data, enforce server-side auth, block record access + field
  tampering, secure session cookies, hash passwords, rate-limit login, bot protection, parameterize
  queries, validate all input, escape user content, restrict file uploads, trim API responses,
  security headers, force HTTPS, scan dependencies — assessment task tracked in
  `brain/goals/workspace-os.md` `[security-gates]` (INBOX 2026-08-13)

- `[C]` [github/spec-kit](https://github.com/github/spec-kit) — GitHub's Spec-Driven Development
  toolkit. Lucas, INBOX 2026-08-16: *"pra ajudar a gente a aplicar o SDD. vale a pena pesquisar bem
  pra não pegar a primeira opção sem pensar"*. **Read 2026-08-17, and the verdict is partial
  adoption, not wholesale**: it installs `.specify/` artifacts and `/speckit.*` commands across 30+
  agents, but it **enforces nothing** — no hooks, no gates, no CI, only prompts and templates. Ours
  is enforced at five points, so adopting it as-is would trade ENFORCED for INDUCED, which is this
  workspace's whole bet backwards. What it has that we do not is the front half: `constitution`,
  `clarify` and `converge` (assess a codebase against its spec). Mine those three for SPEC v1; leave
  the rest. Paired task: `code/ROADMAP-spec-drive.md` § P5a.

### Adversarial review as a standard (INBOX 2026-08-16, paired item in /ROADMAP.md)
Three reels from the same practitioner, captured together because Lucas's note is one idea across
all of them: *"have adversarials as our standards, maybe enforced… e.g., a plan that doesn't have
any adversarial steps is rejected"*.
- `[C]` [Do you even adversarial bro?!](https://www.instagram.com/reel/DbsInXVNmjZ/) — Kem @
  GlitchCatClub. The framing reel; no method in the caption
- `[C]` [How I do mine — great but can be a death loop](https://www.instagram.com/reel/DcB57k9tigG/)
  — same author, method doc at
  `https://claude.ai/code/artifact/915ce49a-bdb8-4723-8f14-638c6d1b1391`. **The caveat is the useful
  half**: he says the technique can become a death loop, which is the failure mode to design
  against, not a footnote
- `[C]` [Less AI slop — 26 gates you can implement
  today](https://www.instagram.com/reel/Dbk11QVtZB8/) — same author, doc at
  `https://claude.ai/code/artifact/18822ddb-3982-41b3-bcb6-2bd68fd84243`. Directly comparable to
  this workspace's own gate set

⚠ **Both artifact docs are unread.** `WebFetch` refuses them: *"this artifact is served to you as a
public (non-member) reader, and reading public artifacts that way is not enabled yet"*, and
`core/tools/web/fetch` gets only the disclaimer line — the page is JS-rendered. So the two entries
above are captured on their captions alone. **Nothing here is evidence about what the docs say.**
Lucas can open them in a browser and paste the content, which is the only path that currently works.

### Agent methodologies to evaluate against our own
- `[C]` [obra/Superpowers](https://github.com/obra/Superpowers) — *"a complete software development
  methodology for your coding agents, built on top of a set of composable skills"*. Same shape as
  our craft flow: interview for intent → spec in readable chunks → implementation plan written for
  *"an enthusiastic junior engineer with poor taste, no judgement, no project context, and an
  aversion to testing"* → subagent-driven execution with red/green TDD, YAGNI, DRY. Installs
  per-harness across 14 agents (Claude Code, opencode, Pi, Copilot, Gemini, Cursor…), so it is
  provider-agnostic the same way we are. Lucas, INBOX 2026-08-16: *"será que eu deveria usar o
  superpowers?"* — the honest comparison is against `core/flows/craft/` and `/craft`, which already
  do this, and the question is whether theirs is better rather than whether it is good. Paired
  assessment item in /ROADMAP.md

### How a goal is written, and how a claim is weighed
- [50 years of motivation science](https://www.instagram.com/reel/DcQpCU_JkmU/) — Shadé Zahrai,
  summarising six findings: specific goals over vague intentions (Locke & Latham), progress as the
  driver of persistence (Amabile), self-directed meaning over willpower (Deci & Ryan), environment and
  cues over resolve (Wood), social accountability, and implementation intentions — *if this happens,
  then I will* (Gollwitzer). Lucas: *"podemos talvez aproveitar essas máximas no design do WOS, dos
  goals."* ⚠ a reel summarising six literatures; **the named researchers are the citable trail, this
  link is not** — assessment task tracked in `/ROADMAP.md`
- [repeated claims read as independent confirmation](https://www.instagram.com/reel/DcNQt9juXpA/) —
  claim that the model counts the same assertion across many sites as many confirmations even when all
  copies trace to one anonymous source. ⚠ no study cited, and its proposed fix is a prompt line, which
  `/ROADMAP.md` already rejects as INDUCED — kept as a specimen of the failure, never as
  a candidate cure

### Offline resilience (parked, see /ROADMAP.md)
- [Reticulum](https://github.com/markqvist/Reticulum) — E2E-encrypted network stack that keeps
  working with no internet or infrastructure
- **Kiwix** — all of Wikipedia offline; almost certainly the "NOMAD project" Lucas half-remembered
