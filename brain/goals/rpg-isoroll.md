# [ fun | rpg | near ] isoroll

Foundry extension for isometric perspective — hades-like look — with automated content generation. UPDATE 2026-07-13: **painter grammar FROZEN** @ feel-rig v16.2 (19 design rounds; per-voxel scene, sloped groups roofs+stairs, opening voxels) — P6.5 ✅. P5 strategy pivoted to render→restyle lane (flat-shaded render → NB whole-sheet restyle; test-to-kill pre-registered). Now executing post-freeze plan: DSL v2 parsers (Python+TS twins) → P7 painter MVP ×2 loops → P5 arms test (Lucas web-app NB) → P8/P9. Canonical spec: `code/isoroll-content/SCENE-CREATION.md`; grammar log: `design/PAINTER-UX.md`.

>**signals**  
transformative · expected · thrilled

>**dynamics**  
pragmatic mode · stalled motion · intrinsic source

>**fears**  
*what · losing progress again — spending time rebuilding what was already built  
when · looking at recovered files without the context of what they were doing  
why · setup loss erases the environment but not the memory — the gap between what you had and what you can immediately run is frustrating  
how · avoiding the rebuild because it feels like repetition, not progress*

>**analysis**  
Stalled by a concrete obstacle — not motivation, not clarity, just a missing environment. The rebuild is the gate. Documenting the setup this time is the real lesson: this shouldn't be able to happen twice. Get ComfyUI running, document the workflow, then return to where the code was.

## selected next achievement
    [scene-seam] close the generate→play seam (program P2): manifest export from content + import into module — gray l-room loaded and playable in live Foundry

**ease-start**  
Nothing to set up — the seam pilot runs via `/loops export-manifest` in `code/isoroll-content` (Fable session 2026-07-09 orchestrates). Your part is the checkpoint after: open Foundry, eyeball the l-room, walls should block vision.

## backlog

> [ ] [scene-seam] = program P2 (export-manifest + module-walls-import + e2e Foundry)  
> [ ] [scene-painter] in-Foundry grid painter MVP = program P7 (needs P4 assembler + P6 floor/fog spike)  
> [ ] [kit-paint] NB paints the dimetric kit = program P5 (Lucas runs NB batches; ☐ checkpoint)  
> [ ] [multiview-8+1] view switching, dimetric remap + cardinal batch = program P8 (DECIDED 8+1, 2026-07-09)  
> [ ] [alpha-pipeline] background transparency — largely resolved for tiles (per-cell rembg, S0-E6-fix5); still open for characters  
> [ ] [8dir-sprites] 8-direction views per character — after tiles ship (NB cardinal weakness returns for tokens)  
> [ ] [anim-pipeline] animate characters: idle, attack, defend, hurt, cast, crouch  
> [ ] [sprite-atlas] atlas packing for Foundry export  
> ~~[setup-rebuild]~~ superseded 2026-07: ComfyUI = utility rail only, symlinks fixed (env-utility-repair); NB is primary  
> ~~[face-detailer] [hand-detailer]~~ superseded: local SD generation dead (kill-log) — revisit only if a character lane needs local refinement  
> ~~[tile-generation]~~ absorbed into S0/SCENE-CREATION (kit batches)  
> ~~[foundry-review] [iso-prototype]~~ done long since: isoroll-module is mature (slicing, depth sort, walls, fog, gizmos)  
> ~~[content-gen-reconnect]~~ = [scene-seam] above  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-21  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       5 |
| trimester   |       6 |
| semester    |       6 |
| year        |       6 |
| 2-year      |       6 |
| 4-year      |       6 |
<!-- stats:end -->
