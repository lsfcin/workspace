# Evidence Notes — Relativistic Raytracer Full Review

## 1. Scene Description Inconsistencies

### Scene 4 and 5
- **Methods §4 Table~\ref{tab:scenes}:** Scene 4 = "Rotating BH (a=0.99)" at r=10M equatorial; Scene 5 = "Rotating BH (a=0.99)" at r=10M polar. Both described as **single** Kerr black holes.
- **Experiments §5:** Scene 4 = "Two equal-mass rotating black holes placed symmetrically at ±50 km on the x-axis" (binary); Scene 5 = "Identical configuration to Scene~4 with the Milky Way skybox substituted" (also binary).
- **Verdict:** Irreconcilable. Methods describes single BH; Experiments and Results treat them as binary/multi-body. The scene table in Methods is wrong or outdated.

### Scene 6
- **Methods §4 Table~\ref{tab:scenes}:** Scene 6 = "Rotating BH, close stress test (a=0.99)" with camera at r=6M equatorial. Single black hole.
- **Experiments §5:** Scene 6 = "ten-body solar system, stress test" naming Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune.
- **Results §6.4 (tab:scene_complexity):** "Solar system (12 bodies)"
- **Results §6.1 figures and §6.3 figures:** "twelve-body solar system", "twelve solar-system bodies"
- **Verdict:** Three-way conflict. Methods §4 is completely inconsistent with Experiments and Results.

### Body count in Scene 6
- Experiments §5 names 10 bodies (Sun + 8 planets + Moon).
- Results consistently say "twelve gravitating bodies" and "twelve-body solar system."
- Difference: 2 bodies unaccounted for. Either Saturn's rings count separately, or two bodies were added (e.g., Pluto, a second Moon, or two additional moons). No explanation given.

## 2. Step-Size Unit Inconsistency (Critical)

### Technical Background §2
- Lists step sizes as: Large h=260.00, Medium h=52.00, Small h=1.00 (units: internal simulation km, confirmed by §5)
- RK4 uses h=1.00

### Methods §4.3 (\ref{sec:method_integrators})
- Lists step sizes as: large h=0.10, medium h=0.05, small h=0.01 (dimensionless or geometrized M?)
- RK4 uses h=0.05 "chosen to be smaller than the medium Euler step"

### Experiments §5 factorial table
- Euler-Large: h=260 km; Euler-Medium: h=52 km; Euler-Small: h=1 km; RK4: h=1 km
- Step-size note: 1 km ≈ 0.07M → Euler-Large ≈ 17.6M, Euler-Medium ≈ 3.52M, Euler-Small ≈ 0.07M

### Inconsistencies:
1. Methods says RK4 h=0.05 (= Euler-Medium), but §2 and §5 say RK4 h=1 km (= Euler-Small). **Contradictory.**
2. Methods' dimensionless values (0.10/0.05/0.01) don't match geometrized-unit conversion (17.6/3.52/0.07). Neither mapping works.
3. Results §6.3, §6.4, §6.5 use dimensionless labels (h=0.10, h=0.05, h=0.01) consistent with Methods §4 but not the km values in §5.

**Source (submission checklist §B2):** This inconsistency was previously identified and flagged as requiring author resolution before submission.

## 3. Abstract Claims vs. Actual Results

### Claim: "Vulkan consistently lower per-frame render times than Unity across all configurations"
- **Results §6.2:** At 144p, Vulkan/Unity fps ratios = 0.62–0.71 (Unity is FASTER at 144p).
- Contradiction is explicit and directly falsifies "consistently" and "across all configurations."

### Claim: "RK4 reduces the empty-pixel artifacts... although it introduces sampling noise and dark artifacts in extreme vorticity scenarios"
- **Results §6 (entire results section):** RK4 is always the reference/ground truth. Paper never reports RK4 introducing its own artifacts. The stress-test gallery (Fig~\ref{fig:stress_gallery}) shows the extreme-spin render under Euler-Large, not RK4.
- **Discussion §7.3:** RK4 is described as "mandatory" for scientific accuracy — never described as defective.
- **Verdict:** The "RK4 introduces dark artifacts" claim is unsupported and appears to be an incorrect characterization. The paper's data shows the opposite: RK4 is consistently superior.

## 4. Discussion Numbers vs. Results Numbers

### Euler-Large throughput advantage (Kerr 480p Vulkan)
- **Results §6.3 (03_integrator_comparison.tex):** "The performance gap between Euler-Large and RK4 at 480p spans 95× (Newton), 102× (Schwarzschild), and 130× (Kerr)."
- **Discussion §7.2:** "Euler-BigStep offers the highest throughput (141× over RK4)"
- 141× vs 130× (Kerr) — inconsistent by ~8.5%.

### Euler-Medium throughput advantage (Kerr 480p Vulkan)
- **Results §6.3:** "Euler-Medium (h=0.05) occupies a useful middle tier: 0.73--0.90 ms at 480p (110--135× faster than RK4)."
- **Discussion §7.2:** "Euler-MediumStep occupies a practical sweet spot: a 66× throughput gain over RK4."
- 66× vs 110–135× — wildly inconsistent. The 110–135× range covers all three metrics; 66× applies to Kerr specifically (0.73ms / 49.4ms ≈ 67.7×). The Discussion's 66× is Kerr-specific; Results §6.3's 110–135× is metric-averaged. Not clearly stated in Discussion.

### Summary: Results text uses metric-averaged ranges; Discussion uses Kerr-specific values without explicitly stating this. Creates the appearance of inconsistency.

## 5. Physics Error: Ergosphere Claim

### Claim in Methods §4
"Scene 6 is the stress test: the Kerr metric at r=6M (within the ergosphere boundary for a=0.99, where r_+ = 1 + √(1-a²) ≈ 1.14M)"

### Analysis
- The **ergosphere** (ergoregion) is bounded by the **static limit** (outer boundary) and the **outer event horizon** (inner boundary).
- For Kerr in Boyer-Lindquist, the static limit (outer ergosphere boundary) in the equatorial plane is: r_SL = M + √(M² − a²cos²θ). At θ=π/2 (equatorial): r_SL = M + M = 2M (independent of spin!).
- The outer event horizon: r_+ = M + √(M² - a²). For a=0.99M: r_+ = M(1 + √(1−0.99²)) = M(1 + 0.141) ≈ 1.141M. This matches the text.
- **Camera at r=6M is FAR outside the ergosphere** (ergosphere extends from r≈1.14M to r=2M in the equatorial plane).
- The text confuses the outer **event horizon** (r_+ ≈ 1.14M) with the **ergosphere boundary**. These are different surfaces.
- Additionally, r_+ is the INNER boundary of the ergosphere (the outer event horizon), not the outer boundary. The claim "within the ergosphere boundary, where r_+ ≈ 1.14M" is doubly confused.
- **Verdict:** Physics error. The camera at r=6M is well outside both the ergosphere and event horizon. The parenthetical should be removed or corrected to say "in the strong-field region near the photon orbit (prograde photon orbit at r ≈ rph_pro for a=0.99)."

## 6. Duplicate Label: sec:integrators

- **Technical Background §2:** `\subsection{Numerical Integration of Geodesics}` → `\label{sec:integrators}` (line 70 of 02_technical_background.tex)
- **Results §6.3:** `\subsection{Integrator Performance--Accuracy Tradeoff}` → `\label{sec:integrators}` (03_integrator_comparison.tex)
- LaTeX will silently resolve all `\ref{sec:integrators}` to one of these. Discussion references like "Section~\ref{sec:integrators}" will point to wrong section.
- **Verdict:** Duplicate label, causes incorrect cross-referencing. One must be renamed.

## 7. Broken Table Cross-Reference

- **04_euler_platform.tex (§6.4):** Defines table labeled `\label{tab:quality}`; paragraphs within that same file say "Table~\ref{tab:integrator_quality}".
- **03_integrator_comparison.tex (§6.3):** References "Table~\ref{tab:integrator_quality}" in two places.
- `\label{tab:integrator_quality}` is never defined anywhere in the manuscript.
- **Verdict:** All `\ref{tab:integrator_quality}` will render as "??" in the compiled PDF.

## 8. Conclusion Claims Unsupported by Data

### "advantage largest for the computationally intensive Kerr metric at 1080p"
- The paper explicitly states 1080p was used **only for qualitative figure production** and not included in timing tables (Experiments §5): "Resolution 1080p (1920×1080) was used exclusively for qualitative figure production... and is not included in the timing tables."
- No 1080p timing data exists in the paper. The claim about Vulkan advantage "at 1080p" has no data support.

## 9. Related Work Residual Issues

### "most visible demonstration" for DNGR/Interstellar
- §3 Applications: "Interstellar and its DNGR pipeline~\cite{james2015} remain the most visible demonstration that Kerr lensing can matter aesthetically as well as scientifically."
- The 2026-05-17 honest review flagged this as a high-risk superlative. Still unremedied.

### "no study jointly characterises" gap claim
- §3 still makes implicit absolute claims via table structure; the 2026-05-17 review flagged remaining overconfidence. The current text avoids the absolute phrasing in the Introduction: "No prior study has jointly characterised..." — §1 uses absolute phrasing. §3 is more qualified but still risky via table buckets.
- §1 Introduction still says: "No prior study has jointly characterised these two axes — platform and integrator — under the same controlled experimental conditions."

## 10. Structural Duplicate in Results

- `sections/06_results/04_euler_platform.tex` (label: sec:euler_artifacts) describes visual quality analysis of Euler step size on Scene 4, includes Table~\ref{tab:quality}.
- `sections/06_results/05_visual_artifacts.tex` (label: sec:visual_artifacts) covers the same analysis: photon-ring Euler artifacts, RK4 reference, metric dependence.
- Both sections reference `\fig{fig:euler_artifacts}` but the figure is defined only in `05_visual_artifacts.tex`. The `04_euler_platform.tex` references figures defined in the following subsection — reverse order problem.
- The two sections are redundant and should be merged; the current arrangement creates confusion and broken forward-references.

## 11. Introduction Section Roadmap Inaccuracy

- §1: "Section~\ref{sec:results} reports timing and comparative benchmark results, while Section~\ref{sec:visual_artifacts} analyses visual artifacts and fidelity."
- `sec:visual_artifacts` is a **subsection** of `sec:results`, not an independent section. The sentence implies parallel top-level sections.
- This is a minor presentation issue but will mislead readers about paper structure.

## 12. "DNGR is the field's most-cited rendering reference" / citation quality
- Not explicitly stated in the current §3 (the text says "most visible demonstration"), but the risk noted in previous reviews remains.
- `chen2023` (Chen et al., "Black hole images: A review", Science China 2023, DOI 10.1007/s11433-022-2059-5) — legitimate reference in bib with proper DOI.
- `wang2004ssim` (Wang et al., IEEE TIP 2004, SSIM) — legitimate, DOI present.
- All bib entries verified as having proper author/title/year; no bib-level hallucinations detected.

## 13. Section 5 Cross-Reference Integrity
- §5 references `\ref{sec:quality_metrics}` — this label exists (defined in §5 itself). ✓
- §5 Experiments references `\ref{sec:visual_artifacts}` indirectly through results; §6 label exists. ✓
- Introduction references `\ref{sec:visual_artifacts}` — exists as subsection label. ✓
- Submission checklist items C (stale `\ref{sec:visual}`) appear to have been resolved.

## 14. Vulkan Missing Data Point
- "Vulkan Kerr RK4 at 720p was not completed in the present benchmark (marked † in Table~\ref{tab:integrators})"
- §6.3 provides an extrapolated estimate of ~111 ms. Extrapolation from linear scaling, clearly flagged.
- This is acceptable disclosure, not a problem.
