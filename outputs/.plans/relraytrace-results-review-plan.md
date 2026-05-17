# Review Plan: relativistic-raytracer results section

**Artifact:** `Academy/papers/relativistic_raytracer/sections/06_results.tex` (and subsections)
**Source type:** Local LaTeX manuscript (JBCS submission)
**Slug:** `relraytrace-results`
**Scope:** Results section ONLY (§6 and all `06_results/` subsections + referenced tables)

## Review criteria

| Criterion | Checked against |
|-----------|----------------|
| Novelty of claims | Related-work table + prior GPU geodesic literature |
| Empirical rigor | Internal consistency of reported numbers; methodology note |
| Baselines | Comparison to Euler-Large as throughput anchor; RK4 as accuracy anchor |
| Reproducibility | Canonical benchmark config; hardware table; missing data (†) |
| Claims validity | Statistical methodology; measurement incompatibility |
| Figures/tables | Size, caption accuracy, label consistency |
| Metrics | PSNR/SSIM averaging strategy; PSNR=∞ issue |
| Related work | Citations in §6 match related-work survey |
| Writing quality | Terminology consistency; typos; cross-references |

## Verification checks needed

1. Step-size values: methods (h=0.10/0.05/0.01) vs table comments (h=260/52/1) vs experiments (h=260/52/1)
2. Measurement methodology: Vulkan GPU-side timestamp vs Unity wall-clock — is platform comparison valid?
3. PSNR=∞ rows: does the averaging conflate all-black baseline pairs with real quality data?
4. Missing Vulkan 720p Kerr RK4 datum — reason stated?
5. Extra closing braces `}}` in figure \includegraphics lines
6. Section label `sec:platform_parity` vs content "Newton Baseline Gallery"
7. Typo: "Unatural" / "UnaturalSpinSpeed" (should be "Unnatural")
8. fps_ratio = Vulkan/Unity at 144p: paper claims Unity faster due to lower CPU dispatch cost — is this logic coherent given different timing methodologies?
9. Christoffel-term count: paper says Newton has "no curvature terms", Schwarzschild "four non-zero independent terms", Kerr "thirteen independent terms" — verify against GR
10. Table overflow: tables 5, 6, 7, 8, 9 vs column widths
