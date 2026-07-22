# [ craft | research | now ] spacemantics — capacidade espacial/visual verificável para agentes

LLMs são fracos em tarefas espaciais/visuais (posição, camadas, pontos de vista, oclusão, coordenadas 2D/2.5D/3D/4D). Tese: não é incapacidade intrínseca, é falta de **interface** — uma **DSL espacial verificável** chamada **texpace** (text+space; relações espaciais E temporais entre qualquer conteúdo, múltiplos sistemas de âncora: world/group/locale), **skills** com convenções + guardas de failure-mode, e um **checker de código** que é o dono da verdade geométrica (o "olho do modelo nunca afirma geometria"). Move do prepose (DSL de gestos + análise Z3) generalizado da pose corporal pra cognição espacial de agentes, e estendido a **4D (tempo)** → animação/vídeo. Entregável primeiro: **paper benchmark + método** provando o ganho cross-dimensional (2D/2.5D/3D/4D) e cross-model (Haiku/Sonnet/Opus/Fable + GLM/DeepSeek via opencode). Investiga também **CV como ponte visuais→semântica** (segmentação, profundidade, detecção, classificação, tracking) — reusa `code/corpora/`.

Casas: `code/spacemantics/` (engine: dsl + checker + perception + tasks + bench, ROADMAP M0-M3), `academy/papers/spacemantics/` (paper twin benchmark+método), `core/skills/spacemantics/` (skills geom-text/iso-text/spatial-3d-text/motion-text, crescem de `core/skills/iso-visual.md`), e talvez `core/tools/` (wrapper `spatial-check`). Origem: item `[visual-semantics]` em [[loop-engineering]]. Dogfood futuro (M3): isoroll (layout DSL / DepthSorter), casinhas `build_ifc.py`, slides/animação. Ramo UI cruza [[startapps-ux-guidelines-ai]]. Precedente estrutural: [[cria]] (um goal, casa em code/ + paper twin).

>**signals**  
transformative · essential · thrilled

>**dynamics**  
immersed mode · emerging motion · intrinsic source  
2026-07-12 compass: promovido de semente `[visual-semantics]` (loop-engineering:22) pra projeto de 4 casas após sessão de scoping. Landscape confirmado (VLMs quase-aleatórios em perspectiva/rotação; gap de benchmark de *construção* geométrica — GeoGramBench; direção DSL+checker validada mas single-domain — SpatialGrammar/HDSL/SceneCraft). Diferencial: cross-dimensional (inclui 4D-tempo) + cross-model + ablado + checker opcionalmente CV-grounded.

## selected next achievement
    [m1-slice] fatia vertical 2.5D end-to-end (texpace DSL profile + checker + 1 família de tasks + runner cross-model) → primeiros números de lift C0→C3

**ease-start**  
Abrir `academy/papers/spacemantics/outputs/texpace-foundations.md` §6 (princípios de design v0) + `code/spacemantics/ROADMAP.md` M1. texpace core já destilado: `{DIR(frame), DIST, TOP, PATH} × {AT|OVER} + {SEQ,PAR,ALT} + {REPEAT,HOLD}`; checker verifica cena definida numericamente (RCC-8 + Rectangle Algebra + Allen), O(n²). Começar pelo profile 2.5D (mais reuso do isoroll). 10 min relendo §6 antes de escrever a gramática v0.

## backlog

> [ ] [m1-slice] fatia vertical 2.5D + skeleton do paper (intro/método/related work a partir das fontes já coletadas)  
> [ ] [iif-format] INFORMED IMAGE FORMAT (*.iif) — DSL para descrever imagens (builds on spacemantics + texpace); toda imagem aberta/criada pelo agente vem acoplada à sua descrição IIF (read-or-write bound)
> [ ] [m2-widen] ampliar pra 2D + 3D + 4D; sweep completo de modelos; go/no-go do CV-grounding por dimensão; escolher venue  
> [ ] [m3-dogfood] fiar as skills em isoroll + casinhas build_ifc.py + skill de slides/animação  
> [ ] [cv-go-nogo] quais primitivas CV sobrevivem (detecção/segmentação 2D, profundidade 2.5D/3D, tracking 4D) ou fica synthetic-only

## done

<!-- done:start -->
> [x] [m0-scaffold] 2026-07-12: 4 casas criadas (goal, code/spacemantics, academy/papers/spacemantics, +core/skills planejado M1), routing sincronizado, semente [visual-semantics] promovida; DSL nomeada **texpace**  
> [x] [m05-research] 2026-07-12: deepresearch (5 subagentes Q1-Q5) → `outputs/texpace-foundations.md` + provenance; veredito: aposta SUSTENTADA (ganho vem do checker/loop, não da sintaxe); texpace core destilado `{DIR(frame),DIST,TOP,PATH}×{AT|OVER}+{SEQ,PAR,ALT}+{REPEAT,HOLD}`; 28 refs verificadas em refs/  
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-21  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       3 |
| trimester   |       3 |
| semester    |       3 |
| year        |       3 |
| 2-year      |       3 |
| 4-year      |       3 |
<!-- stats:end -->
