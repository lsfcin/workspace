# design-system
> The owner's slide tokens — palette by family, fonts by role, sizes, layouts. Edit a row here and regenerate; nothing else holds these values.

Shape is general, values are the owner's (Lucas, set 2026-09-26 from the taste rounds in `brain/drafts/taste-galeria-1.md`). To change a choice: edit the row, then `core/run tools/slides/pptx template` and `gdrive put --slides` (commands in `core/tools/slides/CONTEXT.md`). `style-system.md` applies these tokens; `accessibility.md` owns the contrast rule they obey.

## Palette
One **family** per section: a deck section gets one family, and one master per family carries the same layouts, so a new colour never multiplies layouts. `chosen` is the owner's hex; `in use` is it shifted in lightness only (hue kept) until text on it is firm — revert by copying `chosen` over. Text on a fill: **≥ 4.5 for titles, ≥ 7 for small text** (weak projector, bright room, glass board).

| family | role | name | chosen | in use | text on it |
|---|---|---|---|---|---|
| verde | light | menta | `#70c38c` | `#70c38c` | black 9.9 |
| verde | main | esmeralda | `#009d72` | `#00aa7b` | black 7.0 |
| verde | dark | pinho | `#327e77` | `#26615b` | white 7.1 |
| azul | light | céu | `#5cb8e6` | `#5cb8e6` | black 9.5 |
| azul | main | azul | `#336db3` | `#2a5a93` | white 7.0 |
| azul | dark | oceano | `#315f8b` | `#2f5b85` | white 7.1 |
| roxo | main | ametista | `#8647b3` | `#773f9f` | white 7.0 |
| roxo | dark | uva | `#6c517f` | `#684e7a` | white 7.1 |
| laranja | main | âmbar | `#e8a13f` | `#e8a13f` | black 9.6 |
| vermelho | main | urucum | `#c65640` | `#c65640` | black 4.8 — titles only |
| vermelho | dark | terracota | `#b2543e` | `#8e4331` | white 7.0 |
| neutro | main | ardósia | `#3f4b5c` | `#3f4b5c` | white 8.9 |
| neutro | ink | grafite | `#3a3b40` | `#3a3b40` | white 11.2 |
| neutro | ink | preto | `#000000` | `#000000` | white 21.0 |

Page: white with preto text by default (triad t2: it wins in his rooms — weak projector, glass board); a **dark ground** (preto or ardósia, white text) is offered too, per deck or per slide.

**Use.** `main` is the section's bar, full fill and split block; `light` is a split's calm side or a fill behind a diagram; `dark` is emphasis inside the section (one bold term, one highlighted bar). **Ardósia** is the dark ground for impact slides and the neutral family's section. Footer text: ardósia.

**Avoid.** Two families on one content slide unless the colour IS the comparison · a family's light and main as two different sections (they read as one) · urucum and terracota as two sections (same hue, 10°) · ametista and uva likewise · colour as the only signal: menta, céu and âmbar share a lightness (~2.1), so a colour-blind viewer needs the label or the position too · text on urucum below title size.

## Fonts
Two roles: **text** (the lesson body; must read on a weak projector) and **impact** (section, one-sentence statement, a few moments per deck). Round 3 votes (2026-09-26), final pick open:

| role | yes | maybe | no | not voted |
|---|---|---|---|---|
| text | Atkinson Hyperlegible · Source Sans 3 ("easier to read") | Open Sans · Figtree | IBM Plex Sans | — |
| impact | Anton | Archivo Black | Bebas Neue · Bricolage Grotesque · Syne | Unbounded · Fraunces · Big Shoulders Display |

Code: IBM Plex Mono. Footer: the text family, light. Until the pick: Open Sans.

## Sizes (pt)
display 54 · title 36 · statement 40 · body 24 · code 18 · footer 10. Text never shrinks to fit: overflow means a second slide.

## Layouts
Every family's master carries all of these. `split` names where the colour sits and its share; the sequence 70/30 → 60/40 → 50/50 → thin bar is a zoom into the section (the owner's idea): the bar is what remains of the split.

| kind | variants |
|---|---|
| cover | course above (24, muted), topic below and larger (48, bold) |
| section | full fill, English line in italic below, optional hook image |
| split | 30 · 40 · 50 · 60 · 70 × left · right · top · bottom |
| content | thin bar: none · left · bottom (optional, fine); the bar never recolours the footer text |
| statement | one sentence, one bold term |
| number | numeral in main + stacked title |
| quote | portrait bleeding off an edge, one sentence, author below |
| definition | term, definition, source |
| image | full bleed · half (any side) |
| compare | two images with labels, one pair per slide |
| canvas | footer only — for diagrams that grow slide by slide |
| code | one function per slide |

Content slides: the title is the footer anchor (1–3 words); footer name right, link centred.
