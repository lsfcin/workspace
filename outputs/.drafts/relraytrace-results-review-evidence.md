# Review Evidence: relraytrace-results

## Source files inspected

- `sections/06_results.tex` (root + 7 subsections)
- `tables/results_resolution_scaling.tex` (tab:res_scaling)
- `tables/results_platform_comparison.tex` (tab:platform_comparison)
- `tables/results_integrators.tex` (tab:integrators + tab:integrator_quality)
- `sections/04_methods.tex`, `sections/05_experiments.tex` (context)
- `sections/07_discussion.tex`, `sections/01_introduction.tex` (context)

---

## E1 — Step-size inconsistency (CRITICAL)

**Methods §4.3:** "The Euler scheme is tested at three step sizes (large: h=0.10; medium: h=0.05; small: h=0.01). RK4 uses a fixed step size h=0.05."

**Experiments §5 factorial table:** "Euler-large (h=260), Euler-medium (h=52), Euler-small (h=1)"

**results_integrators.tex caption comment:** "Euler step labels: L h=260, M h=52, S h=1; RK4 uses h=1 with four Christoffel evaluations per step"

**Results text (§6.1, §6.3, §6.4, §6.5):** consistently uses h=0.10, h=0.05, h=0.01.

**Discussion §7.2:** "h=0.10 (Euler-large) is borderline and h=0.01 (Euler-small) is safely sub-curvature" — in geometrized units where M=1, rs=2.

**Arithmetic check:** 260/0.10 = 2600; 52/0.05 = 1040; 1/0.01 = 100 — no consistent scale factor, so these are not the same values in different units. They are genuinely inconsistent.

**Conclusion:** The experiments section and integrators table caption use one set of values (h=260/52/1 in km) while the methods section, results text, and discussion use a different set (h=0.10/0.05/0.01 in geometrized units). The paper was updated to geometrized units in narrative sections but not in the experimental factorial design description and table captions. Both cannot be correct simultaneously for the same runs.

---

## E2 — Measurement methodology confound (MAJOR)

**§6 opening "Measurement note":** "Vulkan timings are GPU-side latencies… Unity timings are wall-clock intervals… These two metrics are not directly equivalent."

**§6.2 ¶1:** Same warning repeated.

**Table 6 (tab:platform_comparison):** Reports fps for both platforms directly in the same table as "Vulkan fps" and "Unity fps" with a ratio column. No footnote in the table itself warns the reader.

**Problem:** If Unity timing includes CPU readback latency, then at 144p (sub-ms GPU work), Unity's wall-clock is dominated by readback/sync overhead rather than GPU time. The claim that "Unity achieves higher frame rates than Vulkan" at 144p would mean Unity's readback overhead is paradoxically lower than Vulkan's dispatch overhead — this is plausible but requires more direct evidence (e.g., CPU profiling) to support. The paper's explanation ("Unity's ComputeShader dispatch path has lower CPU-side cost") is speculative given the measurement differences.

---

## E3 — PSNR=∞ averaging methodology (MAJOR)

**§6.3 quality paragraph:** "PSNR is ∞ for most rows because the comparison groups include pixel-identical all-black image pairs from extreme-spin scenes (FunnySpinSpeed); SSIM, which distinguishes structural similarity even between near-zero-intensity images, is the primary quality metric throughout."

**tab:integrator_quality:** Newton/Euler-L: PSNR=∞, SSIM=0.60; Schwarzschild/Euler-L: PSNR=∞, SSIM=0.54; Kerr/Euler-L: PSNR=12.4, SSIM=0.47.

**Problem:** When a group average includes pixel-identical all-black pairs (RK4 produces all-black AND Euler produces all-black for extreme FunnySpinSpeed), those pairs contribute PSNR=∞ with weight equal to other pairs, pulling the group-average PSNR to ∞. This means the PSNR statistic cannot distinguish between:
  (a) a group where all renders are high-quality, and
  (b) a group where some renders are garbage but also produce all-black output.
The SSIM values provided are the primary metric, but SSIM of near-uniform images can also be unreliable. The paper does not discuss this limitation.

Additionally, Euler-S for Newton has SSIM=0.88 while Euler-L for Newton has SSIM=0.60 — yet both have PSNR=∞. This suggests the comparison includes scenes where the renders differ (SSIM < 1) but happen to share pixel-identical all-black pairs in some extreme-spin subset. The averaging strategy mixes apples and oranges.

---

## E4 — Missing Vulkan 720p Kerr RK4 datum

**§6.3:** "Vulkan Kerr RK4 at 720p was not completed in the present benchmark (marked † in Table~\ref{tab:integrators}); based on the linear scaling observed for other metrics, an extrapolated time of approximately 111 ms is expected."

**Observation:** The paper does not explain WHY this measurement was not taken. A reviewer will ask: was it a time/resource constraint, a software crash, or a hardware limitation? Without explanation, this looks like selective omission. The extrapolation (111 ms) is offered without confidence interval or error bounds.

---

## E5 — LaTeX syntax errors in figures (BLOCKING for compilation)

**03_integrator_comparison.tex lines 101–104:**
```
\includegraphics[width=0.245\textwidth]{images/kerr_euler_s6_g31_480p.png}} &
```
Double `}}` — one extra closing brace after `\includegraphics{...}`. This pattern is repeated across:
- 03_integrator_comparison.tex: fig:gravity_gradient (4 instances), fig:spin_gradient (4 instances)
- 05_visual_artifacts.tex: fig:stress_gallery (6 instances)
- 06_metric_comparison.tex: fig:metrics_comparison (6 instances)
- 07_platform_parity.tex: fig:gallery_newton (6 instances)

Total: ~26 extra braces that will cause LaTeX group-mismatch errors.

---

## E6 — Section label/content mismatch

**07_platform_parity.tex:** Section titled "Newton Baseline Gallery", labelled `\label{sec:platform_parity}`. The label name suggests platform parity testing, but the content is a Newton-only visual gallery. The cross-reference in §6.7 ¶3 uses `\ref{sec:platform}` to point to the platform comparison section — that is correct — but the label `sec:platform_parity` will confuse any reader who follows the label name.

---

## E7 — Typographic/spelling errors

- "Unatural" / "UnaturalSpinSpeed" throughout §6.3 and figure captions → should be "Unnatural"
- "an granular" in §5.2 (methods, not results) → "a granular"
- "Euler-Large BigStep" in figure caption (fig:gravity_gradient) vs "Euler-Large" elsewhere — inconsistent naming

---

## E8 — Single-GPU generalisability

All timing results come from a single NVIDIA RTX 3050 (Table 1). The paper makes general recommendations ("Vulkan is strongly preferred for scientific-quality Kerr rendering…") without acknowledging that relative platform advantage may differ on AMD GPUs (where HLSL→SPIR-V recompilation has less overhead due to mature driver), or on integrated GPUs where memory bandwidth is shared.

---

## E9 — Physical validity of multi-body metrics

**§4 pitfalls:** "Applying Schwarzschild and Kerr metrics to multi-body systems (Scenes 4-6) is physically non-standard but was chosen to test the computational limits."

**Issue:** In the results section, SSIM/PSNR measurements for multi-body scenes are averaged together with single-body scenes without flagging which data points are physically interpretable. Visual quality claims for multi-body Schwarzschild/Kerr have no analytical ground truth.

---

## E10 — Terminology inconsistency

- "manipulated raytracing" used in §4 and §5 for standard geodesic integration — non-standard term not introduced or cited in the introduction.
- Step size for Euler-Small is both "h=0.01" (narrative) and "h=1" (tables/factorial) with no clarifying footnote in the results section itself.

---

## Claimed numbers — spot checks

- Resolution scaling ratio 480p/144p: 409920/36864 = 11.12 ✓ (matches "11.1×" in text)
- RK4 Newton 480p/144p: 37.2/2.97 = 12.5× ✓ (matches "12.5×")
- RK4 Schwarzschild 480p/144p: 39.8/4.01 = 9.9× ✓
- RK4 Newton 720p/144p: 71.4/2.97 = 24.0× ✓ (matches Scale column)
- Euler-L Newton 480p: 0.39 ms → fps = 1/0.000390 ≈ 2564 fps; paper says ">2000 fps" ✓
- Euler-L to RK4 at 480p Newton: 37.2/0.39 ≈ 95× ✓
- Kerr ratio: 49.4/0.38 ≈ 130× ✓
- Platform ratio 144p Newton: 1498/2112 = 0.709 ≈ 0.71× ✓
- Scene 6 at 480p: Vulkan 2×Unity stated — not independently verifiable from published tables (only metric-averaged table shown)

---

## Summary of severity

| ID | Issue | Severity |
|----|-------|----------|
| E1 | Step-size value inconsistency | CRITICAL |
| E5 | LaTeX extra braces (compilation-breaking) | CRITICAL |
| E2 | Measurement methodology confound | MAJOR |
| E3 | PSNR=∞ averaging flaw | MAJOR |
| E4 | Missing datum unexplained | MAJOR |
| E8 | Single-GPU generalisability | MAJOR |
| E6 | Section label mismatch | MINOR |
| E7 | Typos | MINOR |
| E9 | Multi-body metric validity | MINOR (acknowledged) |
| E10 | Terminology inconsistency | MINOR |
