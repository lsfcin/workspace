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
- F17 A2 still shows loading on several slides → S1.

## Method (Lucas, 2026-10-02 — after A3 came out worse than A2 and ignored >70% of this list)
- **A2 is the base.** A3 is discarded (an automatic pass, `settle`, made frames per change instead of a decision per
  slide). Its one hit is R6.
- **One demo per session, 100% closed.** Order: S1 performance → demo 2 (tela infinita) → demo 1 (map: many of its
  points were ignored) → 3, 4, 5, 6, 35 → drawing subskill, covers (F16), crises audit.
- **Each demo session, four steps:** (1) a table in the chat before any code — one row per slide: what moves, what
  appears and when, click or chained, how it reads in the PDF, which list ids it closes; every id of that demo is in
  it; Lucas approves. (2) Build that demo alone, in a small file. (3) Before upload, show each row against the image of
  its frame; nothing ships with a row open. (4) Lucas tests.
- Opus at high effort for demo sessions.

## C · Canva as the home — own track, before S1 (2026-10-02; facts in `specs` § PowerPoint and Canva)
Lucas: Canva's editor is "absurdamente" better than PowerPoint online; he leans to Canva, decided after C3. Bench:
`outputs/.drafts/rodada7/bench_canva.py` (k1–k7, `--k8`); designs v1 `DAHW5Bas3GY` (untouched), v2 `DAHW5CmArj8`, k8 `DAHW5QQvKZY`, k9 `DAHW5Y9MKkk`.
- C1 The plan is `core/ROADMAP.md` § Canva leaf (design approved 2026-10-03 with Lucas's conditions; draft
  `outputs/canva-poder-desenho.md`; swarm material `outputs/.drafts/canva-poder/`). Never an MCP plugged into an agent.
- C3 k10: the agent does k1 alone — seed copy by `merges`, edits by the MCP endpoint — and the oracle verifies; Lucas
  applies nothing (Combinar is inherited from a seed page).
- C4 SVG only when needed, with a warning before converting a slide's shapes (colour editing and arrow connection
  points are lost). Diagrams need their own strategy before the build. Text stays native.
- C5 The draft Apps SDK app (native shapes, lines, connectors, colour) is the candidate for diagrams — test first.
- C6 Pro trial active since 2026-10-03: verify whether anything used needs Pro; if so, say which feature and why.
- C8 A shared deck: Lucas and the agent both edit everything, in turns; no "my slide / your slide".
- C7 k4.b 31→32: a shrinking group leaves thin ghost lines at its old place (Lucas's GPU).

## S1 · performance — own session, after C decides the home (research, then A/B with defined metrics)
- Research how PowerPoint online draws a show (canvas/WebGL? are shapes rasterised? Microsoft's own limits and
  guidance for Morph and heavy slides) before any new hypothesis.
- Metrics, not the fan: per transition, CPU and GPU peak and duration, dropped frames or FPS, loading spinner
  yes/no, time to advance — logged by a script while Lucas clicks (`intel_gpu_top`, `nvidia-smi dmon`, a browser
  performance trace). Lucas's experience still counts.
- **Brave crashed more than once and Ubuntu logged Lucas out, closing every app.** Find the cause (`journalctl`:
  OOM, GPU hang?) and make tests safe first (a separate profile, a memory cap such as `systemd-run --user -p MemoryMax`).
- Hypotheses carried from bench 2: B2 the "3" (c3 built: text, vector, PNG — untested); B3 zoom budget (40 shapes at
  30× never finish, 15× loads); B4/B5 fields and crowds as one image; B6 weight per deck (`perf.split` cuts one file
  per demo); B7 NVIDIA offload (Brave: `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia
  __VK_LAYER_NV_optimus=NVIDIA_only`, check `brave://gpu`).
- A3 lessons: the crowd as one cropped image came out stretched and blurred (A3 s32); a fused group with overlapping
  subpaths rendered with holes (A3 s38). Lucas: the zoom-in frame need not hold what is off screen; the zoom-out frame
  adds what shrinks into view.
- P4 Lucas saw fused groups as "incoherent" (squares in one row not grouped). They are fused by style plus the span of frames plus riding the camera, not by meaning; explain, and group by meaning if it matters for motion.

## R · A3 feedback, by demo (A3 numbers; the content says where it is in A2)
- R1 demo 2, gradient ball: the small light mark of the old position is already under the big ball the moment it
  arrives, so it stays behind when the ball leaves. Never shown after the next move.
- R2 demo 2, s21→22: the arrow's base slides off the ball's centre during Morph. Test the same arrow moved and turned
  by an animation inside one slide against Morph.
- R3 demo 2, visit order (A3 s38→40): too many slides. 38 is one click; what 40 shows is slide 39, its texts entering
  by animation on it. Solve the blink first (c1: an entrance on a Morph target blinks) — bench inside the session.
- R4 demo 4, match cut: A3 s60 broken; s61 and s65–66 overuse Morph (the PDF reads oddly).
- R5 demo 5, 3D turn: A3 changed nothing — F12 all open.
- R6 keep: demo 4 retina, A3 s73→74 — the cyan circles ride the zoom (kept at alpha 0 in the frame before). Right.
- R7 Morph is not the default: a new slide when the camera or a shape's geometry moves; text appearing in place is an
  animation on the same slide. Where Morph misbehaves (R2), test another animation type.

## P · open
- P7 (Lucas) A slides pipeline of established rules, each checked twice: in planning (before building) and in verification (after). Tag each skill rule with its checker — `lint` (zero-token, from the XML: Morph pairs, entrance on a Morph target, static-waits-for-motion, item/point budget, text size, fonts, overlap/touching), `model` (a small-model pass over contact sheets, for checks with a yes/no answer), `human` (taste). Own session.
- P5 An HTML port (pptx → HTML for phones) is a fallback path: first optimise in PowerPoint. Scope it later.

## I · new strategies and ideas (home: estr)
- I1 A new slide type and animation: a document, article or conversation. The whole doc stays in the background (blurred or low opacity), with the highlight in the foreground. Like Jornal Nacional, but stylish, not cheesy.
- I2 The exploded view can open vertically, laterally, or in all directions at once: direction is a parameter.
- I3 The flood slide should show the water rising (see F8).
- I4 Strategy 47, section strips (deck E, own session): a section is a strip — next slide pushes in from the right, with a border or colour band continuous between neighbours of one section. A new section's cover slides in from the right OVER the current slide without pushing (H), or pushes it up entering from below (V). Demo H and V side by side.

## Closing the slides run (after everything above)
- Full audit of the ai4good deck `lucassf.pages.dev/ai4good/crises`, content and look, against the `slides` skill and the teaching specs and templates (`SPECS-aulas.md`, `academy/teaching/classes/ai4good/disciplina.md`, `plano-refino.md`): the overall narrative, cuts, updates (news on every point), revisions and additions. Its own session.
