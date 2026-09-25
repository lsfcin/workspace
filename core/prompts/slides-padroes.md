# slides-padroes
> Seven-step programme Lucas dictated on 2026-09-24: a /slides skill tree, a texpace check, and an audit of his whole slide style against the world's best. Delete when step 7 lands.

Level: high, planning + research. Language with Lucas: pt-br. Branch: `feature/slides-skill`.
**Nothing below is set in stone**: every step is a discussion grounded in literature, industry AND tools; the agent acts as the expert and gives an opinion, Lucas decides (antes → depois in the chat — the popup `preview` does not render, and text between tool calls may not reach him: put what he must see in the turn's LAST message). Skills stay terse. **Keep his atomic ideas (one deck, one footer) apart from general rules.**
**Focus rule:** before any file or rule, ask "does this change a slide or a taste decision?" — if not, one INBOX line. **Tool lens:** at every step ask whether a tool (ours or external) does it; build only what pays back inside the session. **Every slip an eye catches becomes a `lint` rule.**

## already true (do not redo)
- ai4good decks: one per topic, `ai4good · <tema>`, Drive `material/aulas` (`11XkvpRtaougD_Bs726E97lS-PE1auLa6`); `SPECS-aulas.md` § slides rules; no batch backfill.
- [`/slides`](../skills/slides.md) router + 25 skeleton subskills + refs; research on this disk only: `outputs/.drafts/talks-research-{1..5}-*.md`.
- Tools: `gslides preview --sheet`, `stats`, `lint` (text < 14pt, off the slide, over the template, off the footer line: size + bottom edge + anchor). API limits (no layout create/duplicate; restyle before shrinking): `core/tools/slides/SPECS.md` § Writing.
- 4 decks catalogued (macro + archetype) in `outputs/.drafts/slides-catalogo.md` (gitignored: rebuild with `stats` + `preview --sheet` on redes recorrentes `1j8sGfqZkzol-nxFKWDsRLdfjKlYI6wM7K5h3Tw06Pbk`, regressão linear `1XmA8_9dIaCdky66leSKl2UbE9N83fbZxINQADmlFKa8`, história `1MnhRGXDw31GqStyQ-FrsTDMTvfNNCk1w_GhnOKZInhA`, crises `1PgIp_SX2wlMYEbGT3i5MMrciRB3NUC_xzDLvCU7O6B0`).
- Decided, distilled into the skills + `SPECS-aulas.md`: notes ≥ 14pt, colour = meaning, note on the element with only the previous one left in grey; title split (assertion in the body, 1–3 word pt-only footer anchor); chrome lives in master/layouts; syllabus term in **bold**, same word as the skill-tree node.
- **Footer (µ1, Lucas's):** anchor left on the content column, source link short and centred, `lucas s. figueiredo · dc/ufrpe` right on the column edge, all 10pt grey on one bottom edge, no logo. Built on the COPY `1F3XmZmGJkBWvPMwL0cBtBN7vTKNe2KoszrzlUAP2LYE` (master + layout "Title and body"); Lucas's last word was the font size, now fixed — re-show before calling it done.
- **`montador`** agent (`core/agents/montador.md`): cold read, economy + flow, never deletes, only skips on a copy. First run was good signal (Lucas): `outputs/.drafts/montagem-rnn.md` (disk only; 14 skips on the copy).

## você está aqui → next session: TASTE, done properly
Lucas's view (2026-09-24): `taste` is the **subjective** eye (what is tacky — WordArt, Comic Sans; minimal vs full; flat backgrounds; colour; fonts); the subskills are technical. It is built by interviewing him **with images**: A vs B, he picks and says why. Design:
1. Pairs from his archetypes, rendered on COPIES (`gslides apply` + `preview`), shown in both orders; plus outside references (step 3 sources).
2. Output: a ban list (his "brega"), a few dials (density, colour, background, type), and his reasons — `taste.md` stays short and points to the subskills it steers.
3. Check: the agent predicts his pick on held-out pairs; agreement is the measure.
Seeds: DesignPref (arXiv 2511.20513: taste is personal, α=0.25 across designers) · TASTE (arXiv 2605.20731: pairwise, 9 criteria) · Taste Skill (tasteskill.dev: dials + banned patterns) · LLM-simulated preference distorts (arXiv 2605.18311).
Then: profiles (room & screen · audience & vibe · talk format) in `academy/talks/profiles.md`, pointed at by `slides-profiles` in `core/profile.txt`.

## remaining steps
2c. **Deck-template:** turn the copy's master/layouts into `template · lucas` in Drive (layouts: clean, footer = default, section); a new deck is a `gdrive copy` of it.
**A/B 1 — the gate**, in a clean session. Control = a clean Claude Code (no AGENTS.md, no skills) holding only `gslides`; arm = /slides as it stands. Both on COPIES, same frozen prompts, in parallel. Measure: `lint` count, `stats` spread, tokens, time, Lucas's blind pick on A/B contact sheets. **Verdict:** abort (control ≥ skill in both), adjust (mixed: port what the control did better), validate (skill wins both).
3. Collect the best slides in the world — Astra (403 to agents: open in a browser), Claude native, the two animation reels (`tools/video`).
4. Compare our patterns with them and decide what improves.
5. Pattern library per archetype + "which pattern fits what"; fill each subskill. `lint` candidate: the same element repeated on N slides outside the template.
5½. texpace block (review language → test generic → extend for slides → evaluate tokens/time/quality; if it wins, a hook, never skill text; `render-check` is the plug).
5¾. Simulated audience (`audience` agent): research first, then a prototype, calibrated on a real class. A persona gets a CLOSED list of what it knows (background, past classes via the skill tree); a term outside it and undefined in the deck = "did not understand"; attention per slide; profiles interested / detached / missing the basics. It compares versions and finds missing prerequisites; it does not measure learning. Ref to confirm: Generative Students (Lu & Wang 2024).
6. Audit `SPECS-aulas.md`, `SPECS-disciplinas.md`, `structure/templates/` and the skills against everything built.
**A/B 2 — validation**, same prompts, after step 6; `montador` and `audience` join as blind judges beside Lucas.
7. Audit and improve ONE deck with all of it — redes recorrentes, starting from `montagem-rnn.md` — including its 3-line notes. Lucas approved: the skip-gram slides (12–17) become a new embeddings deck; embeddings, RNN, LSTM and transformers need clear worked uses (translation, autocomplete, Q&A).

## A/B prompts (frozen 2026-09-24 — do not tune them toward the skill)
- **S1 new deck:** "Crie no Google Slides um deck de 8–12 slides para uma aula de 20 minutos sobre atenção (attention) em transformers, para alunos de graduação em computação que já viram RNN. pt-br."
- **S2 existing deck** (a copy of redes recorrentes): (a) refine — "melhore os slides 21–40: legibilidade e erros visuais, sem mudar o conteúdo"; (b) update — "insira um exemplo novo de RNN em previsão de série temporal onde ele couber"; (c) extend — "acrescente 3–5 slides sobre LSTM depois do slide 62".
