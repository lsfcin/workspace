# slides-padroes
> Seven-step programme Lucas dictated on 2026-09-24: a /slides skill tree, a texpace check, and an audit of his whole slide style against the world's best. Delete when step 7 lands.

Level: high, planning + research. Language with Lucas: pt-br. Branch: `feature/slides-skill`.
**Nothing below is set in stone**: every step is a discussion grounded in literature, industry AND tools; the agent acts as the expert and gives an opinion, Lucas decides (antes → depois in the chat — the popup `preview` does not render). Skills stay terse. **Keep his atomic ideas (one deck, one footer) apart from general rules.**
**Focus rule:** before any file or rule, ask "does this change a slide or a taste decision?" — if not, one INBOX line. **Tool lens:** at every step ask whether a tool (ours or external) does it; build only what pays back inside the session.

## already true (do not redo)
- ai4good decks: one per topic, `ai4good · <tema>`, Drive `material/aulas` (`11XkvpRtaougD_Bs726E97lS-PE1auLa6`); `SPECS-aulas.md` § slides rules; no batch backfill.
- [`/slides`](../skills/slides.md) router + 25 skeleton subskills + refs; research behind it on this disk only: `outputs/.drafts/talks-research-{1..5}-*.md`.
- Tools: `gslides preview --sheet` (one PDF export, contact sheets), `gslides stats` (style numbers + archetype per slide), `gslides lint` (text < 14pt, off the slide, over the logo).
- **Step 2, first half (2026-09-24):** 4 decks catalogued at two levels — deck (macro) and slide archetype (micro) — in `outputs/.drafts/slides-catalogo.md` (gitignored: rebuild with `stats` + `preview --sheet` on redes recorrentes `1j8sGfqZkzol-nxFKWDsRLdfjKlYI6wM7K5h3Tw06Pbk`, regressão linear `1XmA8_9dIaCdky66leSKl2UbE9N83fbZxINQADmlFKa8`, história `1MnhRGXDw31GqStyQ-FrsTDMTvfNNCk1w_GhnOKZInhA`, crises `1PgIp_SX2wlMYEbGT3i5MMrciRB3NUC_xzDLvCU7O6B0`).
- Decided: annotation text ≥ 14pt, lightly shortened without losing meaning, 1–2 words bold; colour = meaning (one fixed colour per concept inside a deck); `SKIPPED —` inside slide text is agent debris (remove).

## open decisions (the agent's opinion is in the chat of 2026-09-24; Lucas rules)
- **Where the annotation lives** in a progressive diagram: on the element (Lucas's value: guide the speech visually), with a fade of the previous step's note? Decks are dual-use: class, self-study, and solving the `enigma`.
- **Titles are disposable**; orientation instead from 1–2 anchor words in a slimmer footer. Atomic idea to test: footer `lucas s. figueiredo · dc/ufrpe` right-aligned, no logo.

## remaining steps
2b. Close the `taste` interview over the archetypes (the decisions above + statement, text, full-image, equation), then profiles (room & screen · audience & vibe · talk format) in `academy/talks/profiles.md`, pointed at by `slides-profiles` in `core/profile.txt`. Distil into `taste.md` + `style-system.md`.
**A/B 1 — the gate (before step 3, where the big spending starts).** Control = a clean Claude Code (no AGENTS.md, no skills) holding only the `gslides` CLI; arm = the /slides skill as it stands. Both on COPIES (`gdrive copy`), same frozen prompts below, run in parallel. Measure: `lint` count, `stats` spread (distinct sizes/colours), tokens, time, and Lucas's blind pick on contact sheets labelled A/B. **Verdict:** abort (control ≥ skill in both scenarios: the craft layer does not help), adjust (mixed: list what the control did better and port it), validate (skill wins both).
3. Collect the best slides in the world — Astra (403 to agents: open in a browser), Claude native, the two animation reels (`tools/video`).
4. Compare our patterns with them and decide what improves.
5. Pattern library per archetype + "which pattern fits what" table; fill each subskill's rules.
5½. texpace block (review language → test generic → extend for slides → evaluate tokens/time/quality; if it wins, a hook, never skill text; `render-check` is the plug).
6. Audit `SPECS-aulas.md`, `SPECS-disciplinas.md`, `structure/templates/` and the skills against everything built.
**A/B 2 — validation**, same prompts, after step 6.
7. Audit and improve ONE deck with all of it, including its 3-line notes and bilingual titles.

## A/B prompts (frozen 2026-09-24 — do not tune them toward the skill)
- **S1 new deck:** "Crie no Google Slides um deck de 8–12 slides para uma aula de 20 minutos sobre atenção (attention) em transformers, para alunos de graduação em computação que já viram RNN. pt-br."
- **S2 existing deck** (a copy of redes recorrentes): (a) refine — "melhore os slides 21–40: legibilidade e erros visuais, sem mudar o conteúdo"; (b) update — "insira um exemplo novo de RNN em previsão de série temporal onde ele couber"; (c) extend — "acrescente 3–5 slides sobre LSTM depois do slide 62".
