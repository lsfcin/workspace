# rodada 7 list — every point Lucas made about deck A, A2 and the bench, numbered so he never repeats one

**How this file works.** Lucas's words live verbatim in [`taste-galeria-1.md`](taste-galeria-1.md) § rodada 7. This file is the index a
session works from: one line per atomic point, with an id, a home, and nothing else.
- **Routing.** When a point lands in its home (a skill rule, `core/tools/slides/SPECS.md`, `estrategias.md`, a fix in a builder),
  its line is **deleted** here. Git is the history.
- **Start of session.** Every slides session reads this file first. A point Lucas raises again that is already here is a
  failure of this file: fix the line, do not add a duplicate.

Homes:
- `skill` = `core/skills/slides/` (a rule every future deck obeys; needs Lucas's OK on wording);
- `specs` = `core/tools/slides/SPECS.md`;
- `estr` = `outputs/.drafts/rodada7/estrategias.md`;
- `A` = a fix in `build_A.py` (numbers are A2 slide numbers);
- `?` = open question for Lucas.

## R · rules for every deck (home: skill)
- R1 No traditional top titles: "ninguém lê". Stop them even in validation decks so they never become habit. A title sits near its element, placed with care, or is absent.
- R2 A static element entering, leaving or fading never animates at the same time as a dynamic element that moves, pans or zooms: the two are incompatible. It is not about text. Either the static element changes before or after the motion, or it belongs to the moving content and takes the same transform. Lucas saw this across examples, most clearly the retina circles.
- R3 One text leaves before the next arrives: no cross-fade of old title into new content. A title is never Morphed into another title (it stretches). A title vanishing so another appears in its place is hard to follow.
- R4 An element present before and after a Morph moves with the transform. It never vanishes and reappears static (retina circles, the "3").
- R5 Forward = the next node in reading order (the PDF order). Zoom out only on "back". Moving forward is a pan, at most a slight zoom out. The map slide is never cloned. Submaps are allowed.
- R6 Next in bold only rarely, never a whole block in bold. A clock-time pattern is needed (`5:20` looked wrong; `18h40` was used elsewhere).
- R7 No shadows on arrows or on any shape.
- R8 Arrow LOOK (the look is still bad; only the MOTION recipe of A2, a fixed unit line turned by `xfrm`, is approved):
  - today's PowerPoint arrows read "old slide" and amateur; the reference is Excalidraw, in both its straight/formal and sketched styles;
  - every arrow has a defined start and end, touching the node's edge (never starting in the void);
  - a thin arrow meets a thick one cleanly;
  - no square PowerPoint arrowheads.
- R9 Graphs have well-defined nodes. Test both: (a) no outline, with a label placed so it does not split the node's content; (b) the node as a circle that does not clash with its content. An edge never leaves from a label.
- R10 Drawings with shapes must be stylish, modern, refined and minimalist, not lazy. This needs a new drawing subskill.
- R11 3D and view changes never go 100% orthographic hiding the next face. Show 90/10 or 95/5 of the face to come, so the change is pure transform (no fading in of new parts).
- R12 Every mark means something and keeps that meaning. The unexplained green square or circle in the houses, and the lone light-green dot, confuse.
- R13 Spacing: a number or label never touches its element (the 56% touching the dots). Order numbers go inside or beside the element, never at a crossing.
- R14 Z-order is deliberate, and text is never behind shapes. On an exploded view, labels sit outside and connect to their regions; a slight transparency per layer may help; dashes stay light.
- R15 The footer comes from a layout without one, not from masking, and it need not exist on every slide.
- R16 Performance is critical: students use weak machines and phones, and a Dell G15 (16 GB, RTX 3050) still stalled, loaded and once crashed Ubuntu. Animations should reach students, not only the PDF.

## F · fixes in deck A (home: A, A2 slide numbers)
- F1 s2 map: graph ugly; "palavra vira número" under "gato" breaks gato+4 squares into two; edges leave from the text → R9.
- F2 s3→s4 goes back to the map: s4 must be "a rede comum esquece" (today hidden at s67) → R5.
- F3 s7 RNN: thick and thin arrows do not meet → R8. Semantics:
  - the output is one node where the input is 4, so the output is not a word;
  - arrows into one specific node do not say "shared weights". Redesign.
- F4 s9 drawings (cloud with rain, people with a circle, houses) are lazy → R10. s12: green square in Josué's house and green circle in Nena's are unexplained and repeat → R12.
- F5 s17–21: each note appears after the ball stops → R2. s21: the small trail dots blink at the start or end of the final move. ("do slide 20 pro 21 acontece um erro": narration unclear, ask.)
- F6 s22–26:
  - "Lúcia visita a família de Dona Rita" fades while the content below appears → R3;
  - "750 pessoas por agente" and "primeira visita à Ana…" appear after the zoom/pan → R2;
  - the title is placed traditionally → R1;
  - the visit order 1–4 goes inside or beside the element → R13.
- F7 s28→29: the orange "gato sujeito" rounded rect fades in during the Morph, then vanishes on arrival, then returns on click (blink). s32: the orange arrow gato→h4 blinks.
- F8 s33–36 (flood, parallax): parallax excellent, drawings horrible:
  - buildings, clouds, water gauge, wave, weeds;
  - colours;
  - the city font;
  - the meaning of the dots (people?).

  The water should RISE: thickness grows against the ruler (a planning miss). The fan runs loud on this slide.
- F9 s36: all bold; the time pattern → R6.
- F10 s42→43 match cut:
  - the second 3×3 matrix blinks;
  - the fan runs loud;
  - the "= 3": make the 3 big in the centre, drop the rest, and let the 3 shrink with the zoom out. Today a second fixed-size 3 appears mid-transition → R4.
- F11 s47–49 retina:
  - a white aliasing ring between the brown ring and the black pupil (enlarge the black circle);
  - the inside does not read as a retina;
  - the cyan circles blink on entering s48;
  - s48→49 title Morphs into title → R3;
  - the cyan circles reappear static instead of riding the zoom → R4.
- F12 s52–55 3D turn:
  - front squares → rhombi excellent;
  - the side and top rhombi look like a rotation about the wrong axis, with white shading; apply the front-face strategy to them;
  - the numbers leave before the turn → R2;
  - the axes blink.
- F13 s56–59 street → drone: the water tank crossfades square → circle instead of turning into a cylinder; the person's rectangle should become a square under the circle; the façade base becomes a dark band → R11.
- F14 push (gato):
  - a dark line of shrinking thickness appears for no reason;
  - the orange arrow subiu→gato sometimes blinks;
  - end with a zoom out to the full sentence "o gato que a vizinha adotou";
  - Bia slide: "férias caiu" and "outubro" appear after the move → R2, then a zoom out;
  - s58: the 56% touches the dots → R13.
- F15 exploded view:
  - slow on the first run;
  - arrows and lines blink on the two-layer slide;
  - "atalho soma a entrada de volta" sits over a yellow edge;
  - yellow arrows do not touch the rhombus sides → R8;
  - "12 blocos iguais": green is over white → R14;
  - block map: ellipses sprawl on the ground (make flattened cylinders); "50 °C" is behind the blue circles, so put it outside and connected → R14; dashes too strong.
- F16 Covers are ugly: too much subtitle text, plus the bold blue line; the approved earlier covers were better. Redo the cover A/B keeping font and colours, varying construction.
- F17 A2 still shows loading on several slides → P1.

## C · root causes behind many F lines (fix once, in the builder)
- C1 **Blink** (F5, F7, F10, F11, F12, F14, F15): every case is a shape with a click entrance on the Morph's target slide. The Morph draws it during the transition (it is in the slide XML), then the entrance hides it until the click. Hypothesis: such a shape must be absent from the Morph (no `!!` pair, alpha 0 at arrival) or enter as the next frame. Test on one slide first.
- C2 **Static change during motion** (F5, F6, F10, F11, F12, F14): a static element (text or shape) either rides the moving content or changes before or after the motion; the builder never puts a fade on a Morph → R2, R3.

## P · performance, open (home: specs after the next bench)
- P1 Counts up to 250 simple shapes did not hurt on Lucas's machine, yet A2 still loads and the fan runs loud on parallax, match cut and b6. The leading hypothesis is **drawn area, not count**: fused and world-sized shapes stretch far off the slide (a fused people shape is about 70 in wide, and the zoom scales veils 24×), so the renderer rasterises huge surfaces. Next bench: the same shape small, 5× and 25× the slide.
- P2 Slides 22–25 have many elements that could be ONE image (Lucas accepts images where needed); one representation near and far, per B3.
- P3 Lucas's guess: circles are heavy because of their points → replace with a glyph (●) or a polygon. b3 says points were smooth; a glyph is cheap to test in the same bench.
- P4 Lucas saw fused groups as "incoherent" (squares in one row not grouped). They are fused by style plus the span of frames plus riding the camera, not by meaning; explain, and group by meaning if it matters for motion.
- P5 An HTML port (pptx → HTML for phones) is a fallback path: first optimise in PowerPoint. Scope it later.

## I · new strategies and ideas (home: estr)
- I1 A new slide type and animation: a document, article or conversation. The whole doc stays in the background (blurred or low opacity), with the highlight in the foreground. Like Jornal Nacional, but stylish, not cheesy.
- I2 The exploded view can open vertically, laterally, or in all directions at once: direction is a parameter.
- I3 The flood slide should show the water rising (see F8).

## ? · open questions for Lucas
- Q1 A name for "easing": he refused "suavização" and proposed "deslizamento"; my alternatives are "curva de velocidade" and "arranque e freada".
- Q2 The Next font renders jagged online, and he is not happy with it. Re-open the font choice?
- Q3 "do slide 20 pro 21 acontece um erro": the narration that followed was about the map. Which error?
- Q4 The drawing subskill (R10): its scope, and whether it grows `core/skills/slides/`.
