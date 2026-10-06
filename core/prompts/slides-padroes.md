# slides-padroes
> The whole slides programme in one sequence: Lucas's seven steps of 2026-09-24 merged with everything since, re-ordered around the Canva bet (2026-10-04). Delete when phase 7 lands.

Level: high, planning + research. Language with Lucas: pt-br. Branch: `feature/slides-skill`.
**Nothing below is set in stone**: every step is a discussion grounded in literature, industry AND tools; the agent acts as the expert and gives an opinion, Lucas decides (antes → depois in the chat — the popup `preview` does not render, and text between tool calls may not reach him: put what he must see in the turn's LAST message). Skills stay terse. **Keep his atomic ideas (one deck, one footer) apart from general rules.**
**Focus rule:** before any file or rule, ask "does this change a slide or a taste decision?" — if not, one INBOX line. **Tool lens:** at every step ask whether a tool (ours or external) does it; build only what pays back inside the session. **Every slip an eye catches becomes a `lint` rule.**
**Provider rule (Lucas, 2026-10-04):** if Canva becomes the home, the items marked **[PPT/GS]** — they exist only for PowerPoint or Google Slides — are deleted, not ported. Providers stay interchangeable otherwise, and decks migrate one at a time, never in batch.

## already true (do not redo)
- ai4good decks: one per topic, `ai4good · <tema>`, Drive `material/aulas` (`11XkvpRtaougD_Bs726E97lS-PE1auLa6`); `SPECS-aulas.md` § slides rules; no batch backfill of notes or bilingual titles.
- [`/slides`](../skills/slides.md) router + 25 skeleton subskills + refs (step 1a: the tree exists, most leaves are empty); research on this disk only: `outputs/.drafts/talks-research-{1..5}-*.md`.
- Tools: `gslides preview --sheet`, `stats`, `lint`; `pptx` motion, `lint` (motion, text size, item and path-point budget), `flatten`; `onedrive put|pdf|rm`. Facts: [`core/tools/slides/SPECS.md`](../tools/slides/SPECS.md).
- 4 decks catalogued (macro + archetype) in `outputs/.drafts/slides-catalogo.md` (gitignored: rebuild with `stats` + `preview --sheet` on redes recorrentes `1j8sGfqZkzol-nxFKWDsRLdfjKlYI6wM7K5h3Tw06Pbk`, regressão linear `1XmA8_9dIaCdky66leSKl2UbE9N83fbZxINQADmlFKa8`, história `1MnhRGXDw31GqStyQ-FrsTDMTvfNNCk1w_GhnOKZInhA`, crises `1PgIp_SX2wlMYEbGT3i5MMrciRB3NUC_xzDLvCU7O6B0`).
- Decided, distilled into the skills + `SPECS-aulas.md`: notes ≥ 14pt, colour = meaning, note on the element with only the previous one left in grey; title split (assertion in the body, 1–3 word pt-only footer anchor); chrome lives in master/layouts; syllabus term in **bold**, same word as the skill-tree node; round-7 rules R1–R16 in `visuals/motion.md` and `visuals/drawing.md`.
- **Footer (µ1, Lucas's):** anchor left on the content column, source link short and centred, `lucas s. figueiredo · dc/ufrpe` right on the column edge, all 10pt grey, regular weight, lowercase, on one bottom edge; a link is named (the site, short: `medium`, `arxiv`), never a raw url, in the footer's face, size and light weight, not underlined, no logo, no grey wedge. On the COPY `1F3XmZmGJkBWvPMwL0cBtBN7vTKNe2KoszrzlUAP2LYE`. Open: the cover's size order (title vs subtitle — a discussion, not a decision).
- **`montador`** agent (`core/agents/montador.md`): cold read, economy + flow, never deletes, only skips on a copy. First run: `outputs/.drafts/montagem-rnn.md` (disk only; 14 skips on the copy).
- **Taste** is the subjective eye: page https://claude.ai/artifact/N1W9HSAcmBehecrXyzxZSB, his words verbatim in [`brain/drafts/taste-galeria-1.md`](../../brain/drafts/taste-galeria-1.md) (fonts Atkinson Hyperlegible Next + Anton; push-as-pan, reveal-with-20%, sparing fly survive; cube, gallery, flip on white, object zoom are "brega"). Tokens: [`core/skills/slides/design-system.md`](../skills/slides/design-system.md), the one file he edits. Seeds: DesignPref (arXiv 2511.20513) · TASTE (arXiv 2605.20731) · Taste Skill (tasteskill.dev) · LLM-simulated preference distorts (arXiv 2605.18311).

## phase 0 — the home: Canva leaf (você está aqui)
The plan and its order are [`core/ROADMAP.md`](../ROADMAP.md) § Canva leaf (C1 diagram strategy → C2 Pro check → C3 build `core/tools/slides/canva` through `/craft` → C4 k10 passes the oracle with no human click → C5 decide the home); design `outputs/canva-poder-desenho.md`, open points `brain/drafts/rodada7-list.md` § C. History: PowerPoint online became the home on 2026-09-28 because Canva's .pptx import drops motion; the 2026-10-03 swarm found motion is inherited from a seed page copied by REST and edited over MCP, and Lucas finds Canva's editor far better. Test designs live in the Canva folder `canva-tmp` (the REST cannot delete).
When C5 lands: rename the `/slides` surface and `core/tools/slides/CONTEXT.md` to the home (`ISSUES.md`), and delete the **[PPT/GS]** items below if Canva won.

## phase 1 — visual system (original step 2)
- Decide the research plans A-1…A-6 / B-1…B-5 (`outputs/slides-design-system-sota.md`, `outputs/slides-espacialidade-sota.md`, disk only) — never approved.
- **Design each layout in HTML until he approves**, then generate it in the home (master/layouts; in Canva, seed pages) and compare side by side — the first generated master was a design gap, not a tool limit.
- The home's tool reads `design-system.md` directly.
- 2c **Deck-template** `template · lucas`, generated from `design-system.md`; a new deck is a copy of it. Plus an examples deck (neutral content AND his lessons).
- Profiles (room & screen · audience & vibe · talk format) in `academy/talks/profiles.md`, pointed at by `slides-profiles` in `core/profile.txt`.

## phase 2 — animation (taste round 7)
Every open point lives in [`brain/drafts/rodada7-list.md`](../../brain/drafts/rodada7-list.md), read first in every slides session: its method (one demo per session, 100% closed: table approved before code → build alone → each row checked against its frame → Lucas tests), its order, F1–F17 and R1–R7 (fixes to deck A2; in Canva they become requirements of the rebuilt demo), I1–I4, P5, P7. Pipeline and briefs: `outputs/.drafts/rodada7/` (disk only).
- Order: S1 performance → demo 2 (tela infinita) → demo 1 (map) → 3, 4, 5, 6, 35 → drawing subskill, covers (F16).
- S1 as written measures PowerPoint online **[PPT/GS]**; in Canva it becomes the same metrics on Canva's player, and the Brave crash / Ubuntu logout is found and fenced first either way.
- Groups B–G: 45 strategies × {técnico, livre} = 90 demos, plus 44 (timeline as navigation) and 46 (a canvas built up during the talk). **Hard rule: the PDF stays as intuitive as the slides.**
- P7 rule pipeline (each rule tagged `lint` / `model` / `human`, checked in planning and in verification) — today `pptx lint` **[PPT/GS]**; in Canva, the same checks over `canva read`.
- Three visual subskills from the ROADMAP (curated photos, drawing from shapes, node-and-arrow diagrams) — diagrams wait for C1.

## phase 3 — A/B 1, the gate (after C5)
In a clean session. Control = a clean Claude Code (no AGENTS.md, no skills) holding only the home's tool; arm = /slides as it stands. Both on COPIES, the frozen prompts below with "Google Slides" replaced by the home, in parallel. Measure: `lint` count, `stats` spread, tokens, time, Lucas's blind pick on A/B contact sheets. **Verdict:** abort (control ≥ skill in both), adjust (mixed: port what the control did better), validate (skill wins both).

## phase 4 — excellence (original steps 3–4)
- Collect the best slides in the world — Astra (403 to agents: open in a browser), Claude native, the two animation reels (`tools/video`).
- Benchmark Claude Slides and `/design` against our tooling (ROADMAP item).
- Compare our patterns with them and decide what improves.

## phase 5 — pattern library (original step 5)
- Pattern library per archetype + "which pattern fits what"; fill each subskill. `lint` candidate: the same element repeated on N slides outside the template.
- Staged generation (roteiro → storyboard → visual → render, Van Clief method; ROADMAP item).
- 5½ texpace (original 1b): review the language (`academy/papers/spacemantics/`) → test generic → extend for slides → evaluate tokens/time/quality; if it wins, a hook, never skill text; `render-check` is the plug.
- 5¾ simulated audience (`audience` agent): research first, then a prototype, calibrated on a real class. A persona gets a CLOSED list of what it knows (background, past classes via the skill tree); a term outside it and undefined in the deck = "did not understand"; attention per slide; profiles interested / detached / missing the basics. It compares versions and finds missing prerequisites; it does not measure learning. Ref to confirm: Generative Students (Lu & Wang 2024).

## phase 6 — audit (original step 6) + A/B 2
- Audit `SPECS-aulas.md`, `SPECS-disciplinas.md`, `structure/templates/` and the skills against everything built.
- **A/B 2 — validation**, same prompts; `montador` and `audience` join as blind judges beside Lucas.

## phase 7 — apply (original step 7; Lucas 2026-10-04: RNN first, then crises)
- Redes recorrentes, starting from `montagem-rnn.md`, including its 3-line notes and bilingual titles. Lucas approved: the skip-gram slides (12–17) become a new embeddings deck; embeddings, RNN, LSTM and transformers need clear worked uses (translation, autocomplete, Q&A).
- Then the full audit of crises (`lucassf.pages.dev/ai4good/crises`), which closes the round-7 run (`rodada7-list.md` § Closing).

## provider odds and ends
- `gslides frames` and porting `slides_build.py` into `gslides` (ROADMAP) **[PPT/GS]** — kept only if gslides stays a live provider.
- `sync_skills` mirroring the `slides/` subfolders (ROADMAP) — provider-neutral, stays.

## A/B prompts (frozen 2026-09-24 — do not tune them toward the skill)
- **S1 new deck:** "Crie no Google Slides um deck de 8–12 slides para uma aula de 20 minutos sobre atenção (attention) em transformers, para alunos de graduação em computação que já viram RNN. pt-br."
- **S2 existing deck** (a copy of redes recorrentes): (a) refine — "melhore os slides 21–40: legibilidade e erros visuais, sem mudar o conteúdo"; (b) update — "insira um exemplo novo de RNN em previsão de série temporal onde ele couber"; (c) extend — "acrescente 3–5 slides sobre LSTM depois do slide 62".
