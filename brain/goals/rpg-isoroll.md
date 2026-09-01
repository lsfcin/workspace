# [ fun | rpg | near ] isoroll

Foundry extension for isometric perspective with automated content generation. Look target revised 2026-07-29:
**Dead-Cells production model** (geometry rendered offline to sprites), Feather-3D / Tiny Glade aesthetic — not literal
Hades, which is hand-painted at artist cost. **REPLAN 2026-07-29 (MVP-first)**: renderer seam frozen, content strategy
demoted from prerequisite to an A/B behind it, after four review rounds stalled on arm-A stair enclosure masks. Order:
freeze seam → **playable in Foundry with ugly pixels and all 8+1 views** → content bake-off (kit-sprite vs scene-cell
render vs NB textures) → props/lighting. Painter grammar stays FROZEN @ feel-rig v16.2 (19 rounds). Live plan:
`code/isoroll-content/ROADMAP.md`; spec: `SCENE-CREATION.md`; grammar log: `design/PAINTER-UX.md`.

>**signals**  
transformative · expected · thrilled

>**owns**  
`code/isoroll-content` · `code/isoroll-module` · `core/skills/iso-visual.md`

>**dynamics**  
pragmatic mode · stalled motion · intrinsic source

>**fears**  
*what · losing progress again — spending time rebuilding what was already built  
when · looking at recovered files without the context of what they were doing  
why · setup loss erases the environment but not the memory — the gap between what you had and what you can immediately
run is frustrating  
how · avoiding the rebuild because it feels like repetition, not progress*

>**analysis**  
Stalled by a concrete obstacle — not motivation, not clarity, just a missing environment. The rebuild is the gate.
Documenting the setup this time is the real lesson: this shouldn't be able to happen twice. Get ComfyUI running,
document the workflow, then return to where the code was.

## selected next achievement
    [playable] paint a room in live Foundry, walk a token, rotate all 9 views — ugly pixels accepted, look judged later

**ease-start**  
Nothing to set up on your side. The seam freeze + cabin fixture run in `code/isoroll-content` (ROADMAP § SEAM), then the
module work closes the painter. Your part is one checkpoint: open Foundry, paint a room, walk a token, rotate through
the views. Walls, vision, fog and z-order must be right; the art is deliberately ugly at that gate.

## backlog

> [ ] [playable] = ROADMAP § PLAYABLE — painter MVP + manifest walls/vision/fog + 8+1 view switching + DepthSorter +
> 8-dir token selection  
> [ ] [bakeoff] content arms compared behind the frozen seam: A kit-sprite (baseline) vs B scene-cell world-uv render
> (continuity by construction) vs C NB-painted textures — your style score 1–5 decides, boarded side by side on the same
> cabin  
> [ ] [props-mesh] props + characters via image→3D → render 9 views (Hunyuan3D / TripoSR) — multiview by geometry, never
> by generation  
> [ ] [lighting] baked AO + ink + edge highlight + colour grade + clutter — where the perceived style budget actually
> lives; refs captured 2026-07-23 in `code/isoroll-content/refs/REFS.md` § Technique (seamless tileable painting, normal
> maps on 2D sprites)  
> [ ] [alpha-pipeline] background transparency — largely resolved for tiles (per-cell rembg, S0-E6-fix5); still open for
> characters  
> [ ] [8dir-sprites] 8-direction views per character — after tiles ship (NB cardinal weakness returns for tokens)  
> [ ] [anim-pipeline] animate characters: idle, attack, defend, hurt, cast, crouch  
> [ ] [sprite-atlas] atlas packing for Foundry export  
> [ ] [nvidia-imagegen] testar geração de imagem via opencode + chave NVIDIA — nanobanana com a key falhou algumas
> vezes; validar esse caminho alternativo (INBOX 2026-07-24)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-31  ·  trend: decelerating  ·  touches: 31/502/623/623/623/623
<!-- stats:end -->
