# rodada 7 list — every point Lucas made about deck A, A2 and the bench, numbered so he never repeats one

**How this file works.** Lucas's words live verbatim in [`taste-galeria-1.md`](taste-galeria-1.md) § rodada 7. This file is the index a
session works from: one line per atomic point, with an id, a home, and nothing else.
- **Routing.** When a point lands in its home (a skill rule, `core/tools/slides/SPECS.md`, `estrategias.md`, a fix in a builder),
  its line is **deleted** here. Git is the history.
- **Start of session.** Every slides session reads this file first. A point Lucas raises again that is already here is a
  failure of this file: fix the line, do not add a duplicate.

Homes:
- `skill` = `core/skills/slides/`; a name in backticks (`motion`, `drawing`…) is the subskill whose rule the fix obeys;
- `specs` = `core/tools/slides/SPECS.md`;
- `estr` = `outputs/.drafts/rodada7/estrategias.md`;
- `A` = a fix in `build_A.py` (numbers are A2 slide numbers);

## F · fixes in deck A (home: A, A2 slide numbers)
- F1 s2 map: graph ugly; "palavra vira número" under "gato" breaks gato+4 squares into two; edges leave from the text → `drawing`.
- F2 s3→s4 goes back to the map: s4 must be "a rede comum esquece" (today hidden at s67) → `motion`.
- F3 s7 RNN: thick and thin arrows do not meet → `drawing`. Semantics:
  - the output is one node where the input is 4, so the output is not a word;
  - arrows into one specific node do not say "shared weights". Redesign.
- F4 s9 drawings (cloud with rain, people with a circle, houses) are lazy → `drawing`. s12: green square in Josué's house and green circle in Nena's are unexplained and repeat → `drawing`.
- F5 s17–21: each note appears after the ball stops → `motion`. s21: the small trail dots blink at the start or end of the final move → C1 (this blink is the "erro do slide 20 pro 21").
- F6 s22–26:
  - "Lúcia visita a família de Dona Rita" fades while the content below appears → `motion`;
  - "750 pessoas por agente" and "primeira visita à Ana…" appear after the zoom/pan → `motion`;
  - the title is placed traditionally → `word-choice`;
  - the visit order 1–4 goes inside or beside the element → `layout`.
- F7 s28→29: the orange "gato sujeito" rounded rect fades in during the Morph, then vanishes on arrival, then returns on click (blink). s32: the orange arrow gato→h4 blinks.
- F8 s33–36 (flood, parallax): parallax excellent, drawings horrible:
  - buildings, clouds, water gauge, wave, weeds;
  - colours;
  - the city font;
  - the meaning of the dots (people?).

  The water should RISE: thickness grows against the ruler (a planning miss). The fan runs loud on this slide.
- F9 s36: all bold; the time pattern → `typography`.
- F10 s39→40 match cut:
  - the second 3×3 matrix blinks;
  - the fan runs loud;
  - the "= 3": make the 3 big in the centre, drop the rest, and let the 3 shrink with the zoom out. Today a second fixed-size 3 appears mid-transition → `motion`.
- F11 s41–43 retina:
  - a white aliasing ring between the brown ring and the black pupil (enlarge the black circle);
  - the inside does not read as a retina;
  - the cyan circles blink on entering s48;
  - s48→49 title Morphs into title → `motion`;
  - the cyan circles reappear static instead of riding the zoom → `motion`.
- F12 s45–46 3D turn:
  - front squares → rhombi excellent;
  - the side and top rhombi look like a rotation about the wrong axis, with white shading; apply the front-face strategy to them;
  - the numbers leave before the turn → `motion`;
  - the axes blink.
- F13 s47–49 street → drone: the water tank crossfades square → circle instead of turning into a cylinder; the person's rectangle should become a square under the circle; the façade base becomes a dark band → `motion`.
- F14 push (gato):
  - a dark line of shrinking thickness appears for no reason;
  - the orange arrow subiu→gato sometimes blinks;
  - end with a zoom out to the full sentence "o gato que a vizinha adotou";
  - Bia slide: "férias caiu" and "outubro" appear after the move → `motion`, then a zoom out;
  - s58: the 56% touches the dots → `layout`.
- F15 exploded view:
  - slow on the first run;
  - arrows and lines blink on the two-layer slide;
  - "atalho soma a entrada de volta" sits over a yellow edge;
  - yellow arrows do not touch the rhombus sides → `drawing`;
  - "12 blocos iguais": green is over white → `drawing`;
  - block map: ellipses sprawl on the ground (make flattened cylinders); "50 °C" is behind the blue circles, so put it outside and connected → `drawing`; dashes too strong; a slight transparency per layer may help.
- F16 Covers are ugly: too much subtitle text, plus the bold blue line; the approved earlier covers were better. Redo the cover A/B keeping font and colours, varying construction.
  The Next font renders jagged online and Lucas is not happy with it: the font is one more variable of that A/B.
- F17 A2 still shows loading on several slides → B3–B6.

## A3 · what the builder applies next (bench 2 answered; facts in `specs`, rules in `motion`)
- B1 **Blink fix** (F5, F7, F10, F11, F12, F14, F15): every entrance on a Morph's target slide becomes the next frame, camera still (c1 variant 2 had no blink; After Previous blinked worse). Auto-advance that frame (`advTm`) when it needs no click: Lucas does not want an extra click for the "3" (c2).
- B2 **The "3"** (F10): Lucas picks c2 variant 3 (the 3 grows alone in the centre, then shrinks with the zoom out), but Morph blurs the big text all the way down. Test the 3 as a vector shape (text turned to path) and as an image rendered at its largest size; does a shape blur too?
- B3 **Zoom budget** (match cut s39): the cost is the Morph, not the frame; 40 shapes at 30× never finish, 15× loads. Cut what the zoom flings off screen to a minimum, or let it fade before the dive.
- B4 **Many circles → one image** (Lucas): rect < ellipse < ● < polygon, so glyph and polygon are out; a field of dots becomes one PNG/SVG rendered at its largest on-screen size (b13: images blur near otherwise).
- B5 **Crowds** (s22–26, was P2): fused vector looks best but peaks the GPU and loads; one image costs ~65%. Use the image, rendered at max zoom resolution.
- B6 **Weight is per deck** (b11 ran the fan resting on its cover): measure A3 as a whole; splitting the deck is back on the table. It may explain the parallax fan: s33–36 are light in themselves and strokes made no difference (b12).
- B7 Lucas's browser draws on the Intel iGPU, not the RTX 3050: try the NVIDIA offload (`__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia`) — for his machine only; students' weak machines stay the target.

## P · performance, open
- P4 Lucas saw fused groups as "incoherent" (squares in one row not grouped). They are fused by style plus the span of frames plus riding the camera, not by meaning; explain, and group by meaning if it matters for motion.
- P5 An HTML port (pptx → HTML for phones) is a fallback path: first optimise in PowerPoint. Scope it later.

## I · new strategies and ideas (home: estr)
- I1 A new slide type and animation: a document, article or conversation. The whole doc stays in the background (blurred or low opacity), with the highlight in the foreground. Like Jornal Nacional, but stylish, not cheesy.
- I2 The exploded view can open vertically, laterally, or in all directions at once: direction is a parameter.
- I3 The flood slide should show the water rising (see F8).

## Closing the slides run (after everything above)
- Full audit of the ai4good deck `lucassf.pages.dev/ai4good/crises`, content and look, against the `slides` skill and the teaching specs and templates (`SPECS-aulas.md`, `academy/teaching/classes/ai4good/disciplina.md`, `plano-refino.md`): the overall narrative, cuts, updates (news on every point), revisions and additions. Its own session.
