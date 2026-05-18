# Review Plan — Relativistic Raytracer Paper (Full Submission Review)
> slug: relraytrace-full

## Artifact

- **Type:** LaTeX manuscript (multi-file, SBC/JBCS class)
- **Location:** `/mnt/workspace/Academy/papers/relativistic_raytracer/`
- **Entry point:** `main.tex` + eight sections under `sections/`
- **Target venue:** JBCS special issue, SVR 2026
- **Status:** Pre-submission; submission checklist exists but several items unresolved

## Review Criteria

1. **Novelty / gap claim validity** — are the claimed contributions defensible?
2. **Empirical rigor** — do numbers in Results / Discussion / Abstract / Conclusion agree?
3. **Baselines and comparisons** — are prior-art comparisons fair and correctly described?
4. **Reproducibility** — dataset, code, and measurement protocol adequately described?
5. **Claims validity** — are physics claims correct? Any hallucinated or unsupported statements?
6. **Figures / tables** — cross-references intact? Placeholders present?
7. **Metrics** — SSIM, PSNR, L∞, MAE — correctly defined and consistently reported?
8. **Related work** — citations accurate? Gap claims qualified?
9. **Writing quality** — internal consistency of step-size units, section labels, body counts

## Verification Checks Needed

- Step-size values: §2 Technical Background vs §4 Methods vs §5 Experiments factorial table
- Scene descriptions: §4 Methods scene table vs §5 Experiments scene paragraphs vs §6 Results
- Body count (Scene 6): named 10 planets in §5 vs "twelve" in §6 multiple places
- Abstract claims vs Results findings (Vulkan "consistently" faster; RK4 "introduces dark artifacts")
- Throughput multipliers in Discussion vs Results tables
- Physics claim: "within the ergosphere boundary" for camera at r=6M with a=0.99
- Duplicate labels: sec:integrators (defined in both §2 and §6.3); tab:quality vs tab:integrator_quality
- Conclusion claims about 1080p advantage (1080p not benchmarked, only used for figures)
- Related work: absolute "no study" claims; "most visible demonstration" for DNGR
- Figure and table cross-reference integrity

## Files Inspected

- `main.tex`, `sections/01_introduction.tex` through `sections/08_conclusion.tex`
- `sections/06_results/01_resolution_scaling.tex` through `07_platform_parity.tex`
- `lib/refs.bib` (all entries)
- `plans/submission-checklist.md`
- `outputs/related_work_honest_review_2026-05-17.md`
