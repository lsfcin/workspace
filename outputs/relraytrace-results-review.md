# Peer Review: "Relativistic Raytracer: A GPU Benchmark Across Metrics, Integrators, and Platforms"
## Results Section (§6) Only
**Reviewer role:** Expert in GPU computing and relativistic ray tracing visualisation  
**Review mode:** Blind — reviewer has no prior knowledge of this work

---

## Summary Assessment

The results section presents a structured performance and quality benchmark comparing Euler and RK4 geodesic integrators across two GPU platforms and three spacetime metrics. The organisation is logical and the writing is mostly clear. However, several issues undermine scientific rigour: a critical inconsistency in reported step-size parameters, a methodologically unsound platform comparison due to incompatible timing definitions, a flawed image-quality averaging strategy that masks real differences, and unexplained missing data. Additionally, the LaTeX source contains systematic syntax errors that prevent the manuscript from compiling as submitted. These issues must be resolved before acceptance.

---

## Strengths

1. **Systematic factorial structure.** The benchmark crosses platforms, metrics, integrators, and resolutions in a disciplined way. The "canonical benchmark" convention (Scene 1, frontal, NormalG) allows results across sections to be directly compared.

2. **Honest measurement disclaimer.** The "Measurement note" at the top of §6 and the repeat warning in §6.2 correctly flag that Vulkan GPU-side timestamps and Unity wall-clock readback are not equivalent measurements. This transparency is appreciated.

3. **Compute-bound vs bandwidth-bound analysis.** The resolution scaling analysis in §6.1 correctly identifies that Euler-Large is bandwidth-bound (fixed-overhead dominated at low pixel counts) while RK4 is compute-bound, and the ratio data (1.2× vs 24× for RK4) support this clearly.

4. **Multi-body complexity data.** The §6.3 paragraph on scene complexity and the fps_ratio data (104× → 163× → 191× as bodies increase) is the strongest novel result in the section. The claim that this is the first published multi-body Schwarzschild/Kerr benchmark at interactive resolutions is plausible given the survey in §3.

5. **Practical guidance.** The integrator selection rule at the end of §6.3 is concrete and actionable, which serves the stated audience of visualisation developers.

---

## Critical Issues

### C1 — Step-size values are internally inconsistent throughout the manuscript

This is the most serious scientific error. The paper reports three different sets of step-size values in different locations, none of which are consistent with each other:

- **Methods §4.3:** "large: h=0.10; medium: h=0.05; small: h=0.01; RK4 uses h=0.05"
- **Experiments §5 factorial table:** "Euler-large (h=260), Euler-medium (h=52), Euler-small (h=1)"
- **Table 7 caption comment:** "L h=260, M h=52, S h=1; RK4 uses h=1"
- **Results text §6.1–6.5 and Discussion §7.2:** consistently h=0.10, h=0.05, h=0.01

The ratio 260 / 0.10 = 2600, but 52 / 0.05 = 1040, and 1 / 0.01 = 100 — these are three different scale factors, ruling out a simple unit conversion. The values in {260, 52, 1} are not the same physical steps as {0.10, 0.05, 0.01} in any consistent unit system.

**Impact:** A reader cannot determine what step sizes were actually used. The Discussion (§7.2) uses h=0.10 and h=0.01 to argue sub-curvature safety (h ≪ 0.67 in geometrized units), which is physically coherent only if those values — not h=260 and h=1 — were the actual parameters. The experiments section's h=260 km is physically implausible as a geodesic integration step near a solar-mass black hole: at h=260 km, a single step would span roughly 176 Schwarzschild radii, which would not produce any credible lensing.

**Required action:** The authors must identify which values were actually used, correct all inconsistent locations, and state the unit system explicitly in each table caption.

---

### C2 — LaTeX source has systematic syntax errors that prevent compilation

In every figure environment across §6.3, §6.5, §6.6, and §6.7, `\includegraphics` calls are followed by an extra closing brace:

```latex
\includegraphics[width=0.245\textwidth]{images/kerr_euler_s6_g31_480p.png}} &
```

The double `}}` closes the `\includegraphics` argument correctly but leaves a mismatched `}` that terminates the wrong group. This error appears in approximately 26 locations across four subsection files (fig:gravity_gradient, fig:spin_gradient, fig:stress_gallery, fig:metrics_comparison, fig:gallery_newton). The submitted manuscript cannot compile, meaning the figures the paper is built around cannot be verified.

**Required action:** Remove all spurious extra `}` from `\includegraphics` calls in these figures.

---

## Major Issues

### M1 — Platform comparison is methodologically confounded

The central claim of §6.2 — that "Unity achieves higher frame rates than Vulkan at 144p" — rests on comparing measurements that the authors themselves acknowledge are not equivalent: Vulkan reports GPU-only time, Unity reports wall-clock from dispatch to CPU callback (including readback latency and driver buffering).

If Unity's 144p "frame rate" includes the time for a CPU callback to fire, and Vulkan's 144p "frame rate" is pure GPU execution time, then Unity appearing faster does not mean Unity's GPU executes faster. It could equally mean that Unity's CPU callback fires quickly because the tiny GPU workload completes before the synchronisation overhead adds up. The paper's explanation ("Unity's ComputeShader dispatch path has lower CPU-side cost") is plausible but cannot be verified from the reported data because the two timing methods measure fundamentally different things.

**Recommendation:** Either (a) harmonise the measurement methodology (instrument both platforms with GPU-side timestamps), or (b) clearly mark Table 6 and the §6.2 conclusions as *platform-overhead comparisons* rather than *frame-rate comparisons*, and explicitly state that the 144p result does not imply superior GPU throughput for Unity.

### M2 — Image quality metric strategy is statistically flawed

Table 8 (tab:integrator_quality) reports PSNR=∞ for eight of nine rows because the averaging group includes pixel-identical all-black image pairs from extreme-spin configurations. The paper correctly notes this and nominates SSIM as the primary metric. However, two deeper problems are not addressed:

1. **SSIM of near-zero-intensity images is unreliable.** The SSIM formula relies on local mean and variance. When both images are nearly black, the denominator of the SSIM luminance term approaches zero, and small differences in pixel encoding (e.g., floating-point rounding, gamma correction) can produce SSIM values far from 1 even for perceptually identical images. The paper does not report SSIM variance or standard deviation, so it is impossible to determine whether the reported values (e.g., SSIM=0.60 for Newton/Euler-L) are stable estimates.

2. **Averaging across physically heterogeneous configurations inflates or deflates the metric.** Newton/Euler-S yields SSIM=0.88 while Kerr/Euler-S yields SSIM=0.78. These values average scenes where the integrator works correctly (Newton, no photon ring) with scenes where it struggles (Kerr, photon sphere). An aggregate SSIM obscures which configurations drive quality loss.

**Recommendation:** Report SSIM separately for configurations without extreme spin (FunnySpinSpeed excluded) and for all configurations. Report at minimum the inter-quartile range.

### M3 — Missing datum is unexplained

"Vulkan Kerr RK4 at 720p was not completed in the present benchmark." No explanation is given. The two most natural reasons — a software crash or a deliberate time-budget decision — have very different implications for reproducibility. If this datum is expected at ~111 ms (the extrapolated value), it lies well within the testable range of the hardware, so its absence is surprising. The extrapolated 111 ms is reported without any confidence bound.

**Recommendation:** State the reason the experiment was not completed. If it is reproducible, complete it before final submission.

### M4 — Single-GPU scope limits all practical recommendations

The Discussion derives four operating-point recommendations from data collected on a single NVIDIA RTX 3050. Relative platform advantages (Vulkan vs Unity overhead ratio, Euler-Large bandwidth saturation regime) depend on GPU architecture, driver maturity, and memory bandwidth. AMD RDNA GPUs compile HLSL shaders via a different driver path than NVIDIA; the advantage of Vulkan's SPIR-V binary may be smaller there. The abstract and §7 make general claims ("Vulkan is strongly preferred") that are not supported by data from more than one GPU family.

**Recommendation:** Restrict all recommendations to the tested hardware in the results section. State clearly in §6 (not just §7) that the results are from a single GPU.

---

## Minor Issues

### m1 — "Unatural" / "UnaturalSpinSpeed" is a typo throughout

Correct spelling is "Unnatural." The typo appears in §6.3 body text, the spin-gradient figure caption (fig:spin_gradient), and the gravity-gradient figure caption. This must be corrected.

### m2 — Section label `sec:platform_parity` does not match content

§6.7 is titled "Newton Baseline Gallery" but is labelled `\label{sec:platform_parity}`. No platform parity data appears in this subsection. A reader following a hyperlink to `sec:platform_parity` will land in the wrong section. The label should be `sec:newton_gallery` or similar.

### m3 — Inconsistent integrator naming in figure captions

§6.3 figure captions use "Euler-Large BigStep" in one instance and "Euler-Large" elsewhere. The canonical name in the text is "Euler-Large"; "BigStep" should be removed.

### m4 — Euler-Large throughput claim imprecise

§6.3: "enabling frame rates exceeding 2000 fps at 480p and 2000 fps at 720p." This sentence repeats "2000 fps" for both resolutions, making it read as though performance is the same. The 480p Euler-L Newton rate is ~2564 fps and the 720p rate is ~2326 fps; stating both resolutions produce ">2000 fps" is correct but uninformative and slightly misleading since they are meaningfully different.

### m5 — Multi-body metric validity not flagged in results

The multi-body scene (Scene 6) is explicitly acknowledged in §4 as "physically non-standard." However, §6.1, §6.3, and §6.5 derive quality measurements and timing claims from this scene without repeating the caveat. SSIM and PSNR numbers for multi-body Schwarzschild/Kerr have no analytical ground truth; these results cannot be used to make accuracy claims about the integrators in the scientific sense, only about image-level deviation from RK4. This should be noted at least once in the Results section.

### m6 — Cross-reference in §6.3 mixes labels

The Quality paragraph at the end of §6.3 references `Table~\ref{tab:quality}` and directs readers to "Figure~\ref{fig:euler_artifacts} and discussed in Section~\ref{sec:visual_artifacts}." However, these are the immediately following section (§6.4 and §6.5). This forward-referencing structure is confusing; a brief "(see below)" or moving the summary table to §6.4 would improve flow.

---

## Reproducibility and Verification

| Check | Status |
|-------|--------|
| Hardware fully specified (Table 1) | PASS |
| Canonical benchmark config defined | PASS |
| Timing methodology described per platform | PASS |
| Step-size values internally consistent | FAIL — see C1 |
| All experiments reported or omission explained | PARTIAL — 720p Kerr RK4 unexplained |
| Source code / data available | CONDITIONAL ("will be made available upon acceptance") |
| Reference renderer comparison | FAIL — qualitative GYOTO mention only, no quantitative cross-validation |
| Figures compilable from source | FAIL — LaTeX syntax errors (see C2) |

---

## Inline Annotations

**§6.1 ¶2 ("Compute-bound vs bandwidth-bound"):** "the 480p-to-144p ratio of 12.5× for Newton and 9.9× for Schwarzschild both lie within 12% of the expected 11.1× pixel-count ratio" — the 12.5× ratio is *above* 11.1×, not within 12% in the usual sense. The phrasing "within 12% of the expected 11.1×" is ambiguous: does it mean |12.5-11.1|/11.1 = 12.6%, which barely qualifies? Be explicit about the direction of the deviation (super-linear scaling for Newton RK4 is a real observation worth explaining).

**§6.2 ¶3 ("Scene 6 reveals the maximum Vulkan advantage"):** "At 144p the platforms are essentially tied (ratio ≈ 1.0)" — this claim contradicts the measurement-incompatibility caveat. If the two timings measure different things, a ratio of ≈1.0 is coincidental, not evidence of performance parity.

**§6.3 ¶2 ("The accuracy frontier"):** "Newton and Schwarzschild cross into non-interactive territory (71.4 ms and 85.5 ms respectively)" — correct. But the claim that Kerr RK4 "remains below 33.3 ms for Kerr only at 144p" (from §6.1) is slightly inconsistent with the §6.3 accuracy paragraph, which says Kerr RK4 at 480p is 49.4 ms (non-interactive). Make sure both sections are consistent on which threshold is crossed at which resolution.

**§6.3 ¶ "Gravitational field strength amplifies Euler-L artifacts":** "SSIM drops from 0.59 to 0.33 to 0.18 to 0.20." The SSIM jumps back up from 0.18 to 0.20 at the highest mass (10^34 kg). The paper does not address this non-monotonic behaviour; either it is a measurement artefact or a genuine physical effect (e.g., at extreme mass the entire image becomes black, making two identical all-black images score SSIM=1 locally). This must be explained.

**§6.3 last paragraph ("Scene complexity widens the RK4 vs Euler gap"):** "Euler-L's single evaluation per step is masked by memory bandwidth at low scene complexity but still benefits from the same N_body^{-1} RK4 disadvantage at high complexity" — the exponent notation N_body^{-1} is confusing here. The intended meaning is that RK4 cost scales as N_body while Euler-L also scales as N_body but with a 4× smaller coefficient per step. Rephrase for clarity.

**§6.5 ¶ "Metric dependence of the artifact threshold":** "the photon-sphere curvature radius for a Schwarzschild black hole of the mass used here (r_ph = 3M) is large enough that the step sizes tested here all resolve the critical region" — this claim is asserted without supporting calculation. The discussion (§7.2) provides the calculation (h ≪ 0.67 for h=0.10); a forward reference here would strengthen the claim.

---

## Recommendation

**Major revision required.**

The manuscript must resolve issues C1 (step-size values), C2 (LaTeX syntax), M1 (measurement confound framing), M2 (quality metric methodology), and M3 (missing datum) before re-review. The underlying data appear sound — the spot-checked arithmetic is internally consistent — and the paper addresses a genuine gap. With these corrections it would be a solid contribution to the GPU relativistic visualisation literature.

---

## Sources

- Carroll, S. (2004). *Spacetime and Geometry* — Schwarzschild shadow radius formula
- Bohn et al. (2015) — Kerr shadow shape and photon ring as integrator diagnostic
- Vincent et al. (2011) — GYOTO reference solver
- Verbraeck & Eisemann (2021) — Schwarzschild precomputation baseline
- Bruneton (2020) — Fast Schwarzschild approximation baseline
- Müller & Frauendiener (2012), Müller (2014) — Interactive Schwarzschild precedents
- Kuchelmeister et al. (2012) — GPU Schwarzschild/Kerr interactive timing precedent
