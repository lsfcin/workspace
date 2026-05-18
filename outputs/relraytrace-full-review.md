# Peer Review: Relativistic Raytracer — A GPU Benchmark Across Metrics, Integrators, and Platforms

**Manuscript:** "Relativistic Raytracer: A GPU Benchmark Across Metrics, Integrators, and Platforms"
**Authors:** A. R. Cavalcanti, L. S. Figueiredo
**Target venue:** JBCS special issue, SVR 2026
**Review date:** 2026-05-17
**Review type:** Full pre-submission review — correctness, consistency, submission readiness

---

## Summary Assessment

The paper presents a systematic GPU benchmark comparing Unity and Vulkan as platforms and Euler (three step sizes) versus RK4 as integrators for relativistic raytracing across three spacetime metrics (Newton, Schwarzschild, Kerr), six scenes, and three resolutions. The core idea is sound, the dataset is large (16,083 timed renders), and the practical configuration recommendations are useful. The paper is close to submittable but has **five blocking issues** that will cause immediate reviewer rejection or embarrassing LaTeX compile errors, plus a physics error that an astrophysics-literate reviewer will catch. Most of these are internal consistency failures, not new experimental work — they can be resolved with careful editing passes.

**Current assessment:** Not yet submission-ready. Fix the five critical issues before submission; the major issues should also be addressed. Estimated revision time: one focused session.

---

## Strengths

1. **Large, well-designed dataset.** 16,083 individual timed renders across a full factorial design is thorough; the multi-body scaling result (Scene 6) is genuinely new and the fps-ratio vs. body-count data is the paper's strongest novel finding.

2. **Practical guidance is well-grounded.** The four operating points (§7.4) are directly derived from the data and follow from the SSIM/throughput trade-offs. This is actionable for the target audience (developers of educational tools and interactive visualizations).

3. **Measurement methodology clearly distinguished.** The paper is careful to state that Vulkan timestamps measure GPU-only latency while Unity measures wall-clock including readback overhead, and that direct millisecond comparison is not meaningful. This transparency is commendable and pre-empts a common reviewer objection.

4. **Multi-body scaling is novel.** No prior GPU relativistic benchmark (GRay2, Odyssey, Astray) reports how throughput scales with gravitating-body count. The 7× RK4 collapse from single-body to two-body, and the asymmetric Euler/RK4 scaling in Scene 6, are the most surprising and technically interesting findings.

5. **Related work is honest about scope.** The paper correctly frames its contribution as narrower than the scientific rendering pipeline papers it surveys, and does not claim to validate against astrophysical data.

---

## Critical Issues (must fix before submission)

### C1 — Abstract falsely claims Vulkan consistently outperforms Unity

**Location:** Abstract, second-to-last sentence.

**Current text:** "Vulkan's explicit compute pipeline achieves consistently lower per-frame render times than Unity across all configurations, with the advantage widening under the computationally intensive Kerr metric at 720p."

**Problem:** Results §6.2 explicitly reports that at 144p, Unity is faster: Vulkan/Unity fps ratios are 0.62–0.71 (Unity wins). The resolution-crossover finding is one of the paper's interesting non-obvious results. The abstract directly contradicts it.

**Fix:** Replace with a qualified claim:
> "Vulkan's explicit compute pipeline achieves lower per-frame render times than Unity at 480p and 720p, with the advantage widening under the computationally intensive Kerr metric; at 144p, low GPU occupancy reverses this relationship."

---

### C2 — Abstract attributes spurious artifacts to RK4

**Location:** Abstract, last sentence.

**Current text:** "RK4 reduces the empty-pixel artifacts that emerge with large Euler steps near high-curvature regions at moderate resolutions, although it introduces sampling noise and dark artifacts in extreme vorticity scenarios."

**Problem:** The entire Results section treats RK4 as the reference / ground truth for image quality. The paper never reports RK4 producing its own artifacts. The stress-test figure (Fig. stress_gallery) shows extreme-spin degradation under **Euler-Large**, not under RK4. The sentence "introduces sampling noise and dark artifacts" is unsupported by any data in the paper and contradicts the Discussion and Conclusion, which describe RK4 as "mandatory" for scientific-quality Kerr rendering.

**Fix:** Remove the subordinate clause entirely:
> "RK4 eliminates the empty-pixel artifacts that emerge with large Euler steps near the photon sphere and ergosphere boundaries, at the cost of 95–130× lower throughput relative to Euler-Large at 480p."

---

### C3 — Scene descriptions radically inconsistent between §4 Methods and §5 Experiments

**Location:** Table~\ref{tab:scenes} in §4 vs. scene-design paragraphs in §5.

**Conflict — Scenes 4 and 5:**
- §4 table: Scene 4 = "Rotating BH (a=0.99)" at r=10M equatorial; Scene 5 = same metric, polar. Both imply **single** black holes.
- §5 text: Scene 4 = "Two equal-mass rotating black holes placed symmetrically at ±50 km on the x-axis"; Scene 5 = "Identical configuration to Scene~4 with Milky Way skybox."

**Conflict — Scene 6:**
- §4 table: Scene 6 = "Rotating BH, close stress test (a=0.99)" at r=6M equatorial. Single black hole.
- §5 text: Scene 6 = "ten-body solar system, stress test" (Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune).
- §6 results (multiple places): Scene 6 = "twelve gravitating bodies" / "twelve-body solar system."

**Fix:** The §4 scene table is outdated. Update it to match the actual scenes used in §5 and §6. Specifically: update Scene 4/5 descriptions to say "Binary Kerr BH" and update Scene 6 to say "Ten-body solar system" (or twelve, if two additional bodies exist — this must also be resolved, see C4).

---

### C4 — Scene 6 body count: 10 named bodies vs. "twelve gravitating bodies"

**Location:** §5 Experiments lists 10 bodies by name; §6.1, §6.3, §6.4 all say "twelve" in multiple figure captions and the scene-complexity table.

**Fix:** Either name all twelve bodies in §5 (add the two missing ones with a note explaining the discrepancy from the ten canonical planets) or change all "twelve" references to "ten." Pick one and make it consistent everywhere. The scene complexity table caption must match whatever number is in the experiments section.

---

### C5 — LaTeX compile error: broken table cross-reference

**Location:** Sections §6.3 and §6.4.

**Problem:**
- Table in `04_euler_platform.tex` is defined with `\label{tab:quality}`.
- Both `03_integrator_comparison.tex` and `04_euler_platform.tex` reference it as `Table~\ref{tab:integrator_quality}`.
- The label `tab:integrator_quality` is never defined. All references to it will render as "**??**" in the compiled PDF.

**Fix:** Either rename the table label from `tab:quality` to `tab:integrator_quality`, or find-replace all `\ref{tab:integrator_quality}` with `\ref{tab:quality}`. Verify with a clean rebuild after fixing.

---

## Major Issues

### M1 — Physics error: ergosphere claim in §4 Methods

**Location:** §4, Scene 6 description: "the Kerr metric at r=6M (within the ergosphere boundary for a=0.99, where r_+ = 1 + √(1-a²) ≈ 1.14M)"

**Problem:** This is incorrect GR. The ergosphere (ergoregion) in Kerr spacetime is bounded by the static limit (outer boundary) and the outer event horizon (inner boundary). In the equatorial plane, the static limit is at r_SL = 2M for any spin value; the outer event horizon is at r_+ = M + √(M²−a²) ≈ 1.14M for a=0.99M. The ergosphere occupies r ∈ [1.14M, 2M] at the equator. A camera at **r=6M is entirely outside the ergosphere** — it is three times farther than the ergosphere's outer boundary. Furthermore, the text says "within the ergosphere boundary, where r_+ ≈ 1.14M," confusing the outer event horizon (r_+) with the ergosphere's outer boundary (r_SL). These are different surfaces.

**Fix:** Remove the parenthetical entirely. Replace with an accurate characterization: "in the strong-field Kerr regime near the outer photon orbit (r ≈ 4M for retrograde photons at a=0.99), maximising path length and Christoffel-symbol computation."

---

### M2 — Duplicate LaTeX label: sec:integrators

**Location:** `02_technical_background.tex` line ~70 and `sections/06_results/03_integrator_comparison.tex` first line.

**Problem:** Both define `\label{sec:integrators}` — one for "Numerical Integration of Geodesics" (§2) and one for "Integrator Performance--Accuracy Tradeoff" (§6.3). LaTeX will silently duplicate-label warn and resolve all `\ref{sec:integrators}` to one section, causing cross-references in the Discussion to point to the wrong place.

**Fix:** Rename the §6.3 label to `\label{sec:integrator_perf}` and update all references to it.

---

### M3 — Discussion throughput multipliers not labelled as Kerr-specific

**Location:** Discussion §7.2.

**Numbers:** Discussion says "Euler-BigStep offers the highest throughput (141× over RK4)" and "Euler-MediumStep... 66× throughput gain over RK4." Results §6.3 says the Euler-Large/RK4 gap is "95× (Newton), 102× (Schwarzschild), and 130× (Kerr)"; Euler-Medium is described as "110--135× faster than RK4" (metric-averaged range).

**Analysis:** The 66× for Euler-Medium is the Kerr-specific value (0.73 ms at 480p / 49.4 ms RK4 ≈ 67.7×). The 141× for Euler-Large appears to come from a different scene or configuration than the 130× reported in §6.3 for Kerr. The discrepancy is not explained.

**Fix:** Add "(Kerr)" after the multipliers in §7.2, and reconcile the 141× with the 130× from §6.3 — either correct the Discussion value or explain which specific configuration yields 141×.

---

### M4 — Conclusion claims Vulkan advantage "largest at 1080p" but 1080p was not benchmarked

**Location:** §8 Conclusion: "Vulkan consistently outperforms Unity in per-frame render time, with the advantage largest for the computationally intensive Kerr metric at 1080p."

**Problem:** §5 Experiments explicitly states: "Resolution 1080p was used exclusively for qualitative figure production and is not included in the timing tables." No timing data at 1080p exists in the paper. The conclusion cannot claim advantage "largest at 1080p" without data. Additionally, "consistently" is again false at 144p.

**Fix:** Replace with: "Vulkan consistently outperforms Unity at 480p and 720p, with the advantage largest for the Kerr metric at 720p; at 144p, dispatch overhead reverses this relationship."

---

### M5 — Step-size unit inconsistency (flagged in submission checklist §B2, still unresolved)

**Location:** §2 Technical Background, §4 Methods, §5 Experiments.

**Conflict:** §2 lists h=260, 52, 1 (km, implied) and RK4 h=1.00. §4 lists h=0.10, 0.05, 0.01 (unlabelled units) and RK4 h=0.05. §5 factorial table lists h=260, 52, 1 km and RK4 h=1 km. The conversion 1 km ≈ 0.07M means the §4 values (0.10, 0.05, 0.01) do not equal the §5 geometrized equivalents (17.6M, 3.52M, 0.07M). Furthermore, §4 says RK4 uses h=0.05 (Euler-Medium value), while §5 and §2 say RK4 uses h=1 km (Euler-Small value) — a direct contradiction about which step size RK4 uses.

**Fix:** Adopt the km values from §5 as canonical (they appear in the factorial table and are consistent with §2). Update §4 Method to use km units: "large: h=260 km; medium: h=52 km; small: h=1 km; RK4: h=1 km (same step as Euler-Small)." The claim in §4 that RK4 uses "h=0.05, chosen to be smaller than the medium Euler step" is wrong on both counts (it equals the small step, not the medium) and must be corrected.

---

### M6 — Related work: Introduction retains absolute gap claim

**Location:** §1 Introduction: "No prior study has jointly characterised these two axes — platform and integrator — under the same controlled experimental conditions, across multiple spacetime metrics and a range of rendering resolutions."

**Problem:** Absolute "no study" claims are the highest-risk sentences in any submission. A reviewer familiar with Kuchelmeister et al. (2012), Astray (2022), or papers not in this survey will use this sentence to reject the novelty claim.

**Fix (from prior review):** "To our knowledge, no prior study jointly characterises both platform and integrator choice under identical geodesic kernels across multiple spacetime metrics with both performance and visual-quality evaluation."

---

## Minor Issues

### m1 — Introduction roadmap misleads on section structure

§1: "Section~\ref{sec:results} reports timing...while Section~\ref{sec:visual_artifacts} analyses visual artifacts." The label `sec:visual_artifacts` is a **subsection** of `sec:results`, not an independent top-level section. The roadmap implies parallel sections. Fix: "Section~\ref{sec:results} reports performance results (§6.1--6.3) and visual quality analysis (§6.4--6.7)."

### m2 — Related work: "most visible demonstration" for DNGR

§3 Applications: "Interstellar and its DNGR pipeline remain the most visible demonstration that Kerr lensing can matter aesthetically." Prior review flagged this as a risky superlative. Change to "most widely cited" or "the highest-profile public demonstration."

### m3 — Structural redundancy: §6.4 and §6.5

`04_euler_platform.tex` (label: sec:euler_artifacts) and `05_visual_artifacts.tex` (label: sec:visual_artifacts) both analyze Euler step-size artifacts on the same scenes with the same figures. The current arrangement has §6.4 referencing `Table~\ref{tab:integrator_quality}` (broken) and `Section~\ref{sec:visual_artifacts}` (which follows it) — a forward reference to an immediately following subsection. These two subsections overlap significantly and should either be merged into one or clearly demarcated as separate views (quantitative vs. visual).

### m4 — GYOTO comparison is qualitative only

§6.5 states "The GYOTO solver... serves as a qualitative reference" and confirms photon ring position. No GYOTO renders are shown in figures (only referenced). The submission checklist flags this as requiring real renders to replace placeholders. If figures remain placeholders at submission, this will be flagged by reviewers and JBCS copy editors.

### m5 — Scene 6 camera note: ergosphere boundary vs. photon orbit region

Even after fixing C3 (scene table), the §4 text describing Scene 6 as "the Kerr metric at r=6M" should note what r=6M means physically in Kerr (e.g., near the retrograde photon orbit region for a=0.99, or equivalent to the Schwarzschild ISCO), since the erroneous ergosphere reference appears in this context.

### m6 — Discussion §7.2 phrasing: "at less than half the fps ratio cost"

"A 21% improvement over BigStep at less than half the fps ratio cost" is ambiguous and mixes concepts. Replace with a direct statement: "Euler-Medium reduces Euler-Large artifacts by 21% in SSIM at the cost of a 2.1× throughput reduction (from ~2,600 fps to ~1,200 fps at 480p, Kerr, Vulkan)."

### m7 — Declarations incomplete

`main.tex` still has placeholders: `[Funding sources to be declared.]`. JBCS requires funding and all declarations for publication. Fill before submission.

### m8 — Data availability statement is provisional

"Source code and rendering scripts will be made available upon acceptance." JBCS and most modern venues require a data availability statement pointing to current DOI/URL. The dataset URL (Zenodo) should appear here now.

---

## Reproducibility and Verification

**Dataset:** 16,083 timed renders + 17,308 PNG images. Zenodo link referenced elsewhere in workspace (`Datasets/relativistic_raytracer/CONTEXT.md`). Should be cited in the manuscript's Data Availability statement.

**Code:** Two GitHub repositories listed in CONTEXT.md (Unity: `tucoff/Relativistic-Raytracing-Unity`; Vulkan: `tucoff/Project-RayTracing-Vulkan`). Must appear in the manuscript. "Will be made available upon acceptance" is insufficient for modern reproducibility standards.

**Timing methodology:** Clearly described and differentiated between platforms. The distinction between GPU-only latency (Vulkan) and wall-clock readback time (Unity) is disclosed, which prevents a common reviewer objection.

**Image quality scripts:** `scripts/image_metrics.py` exists but is not referenced in the manuscript. Add a footnote or methods note pointing to it.

**1080p renders for figures:** Submission checklist item B (replace example-image placeholders in §6.5–6.7) was flagged but status unverified. If any figure still contains `example-image-a/b/c`, the submission will be rejected by JBCS copy editors on sight.

---

## Inline Annotations by Section

**Abstract:** Rewrite sentences about Vulkan ("consistently") and RK4 ("dark artifacts") — both are factually wrong. [C1, C2]

**§1 Introduction:** Soften "No prior study" claim to "to our knowledge." [M6] Fix section roadmap to not imply visual artifacts is a top-level section. [m1]

**§2 Technical Background:** Step sizes h=260/52/1 listed here without units label — add "(km)". Verify RK4 h=1.00 here matches §5 h=1 km. [M5]

**§3 Related Work:** Change "most visible demonstration" to "most widely cited" for DNGR. [m2] The section is otherwise substantially improved from the prior Feynman review.

**§4 Methods (Scene table):** Update Scenes 4, 5 to say "Binary Kerr BH"; update Scene 6 to say "Solar-system stress test (10 or 12 bodies)." [C3] Remove/fix Scene 6 ergosphere parenthetical. [M1]

**§4 Methods (Integrators §4.3):** Fix step sizes to km and fix RK4 step to h=1 km (= Euler-Small). [M5]

**§5 Experiments:** Resolve body count for Scene 6 — 10 named vs. 12 claimed. [C4] Verify no remaining `\ref{sec:visual}` links (appear resolved but confirm).

**§6 Results:** Fix `\label{tab:quality}` → `\label{tab:integrator_quality}` (or vice versa). [C5] Rename `\label{sec:integrators}` in `03_integrator_comparison.tex`. [M2] Consider merging §6.4 and §6.5 or clearly demarcating them. [m3]

**§7 Discussion:** Add "(Kerr-specific)" qualifier to throughput multipliers. Reconcile 141× with 130×. [M3] Fix §7.3 mass units — "M_⊙" should be "kg" if referencing the Scene 6 mass sweep. Verify SSIM values at specific gravity levels are consistent with §6.3 (0.47 for BigStep Kerr matches Table~\ref{tab:quality}). [M3]

**§8 Conclusion:** Fix "consistently" and "at 1080p" claims. [M4]

---

## Recommendation

**Major revision required before submission.** The five critical issues (C1–C5) are blocking: two create false claims in the abstract, one is a LaTeX compile error producing "??" in the PDF, and two are irreconcilable factual conflicts between sections about what scenes were tested. These will be caught immediately by any reviewer or copy editor.

The major issues (M1–M6) are high-priority but fixable in an editing session. The paper's underlying science is sound — the dataset is real, the platform comparison is interesting, and the multi-body scaling result is novel. The problems are editorial and structural, not experimental.

**Priority order for a single revision session:**
1. Rewrite abstract (C1, C2) — 15 min
2. Update scene table §4 (C3) — 10 min
3. Resolve Scene 6 body count throughout (C4) — 10 min
4. Fix table label `tab:quality` → `tab:integrator_quality` (C5) — 5 min (grep-and-replace)
5. Remove/fix ergosphere parenthetical §4 (M1) — 5 min
6. Rename duplicate `sec:integrators` label (M2) — 5 min (grep-and-replace)
7. Fix step-size unit inconsistency §4 (M5) — 15 min
8. Fix Conclusion claims (M4) — 5 min
9. Soften "No prior study" in §1 (M6) — 2 min
10. Clarify Discussion multipliers as Kerr-specific (M3) — 5 min
11. Fill Declarations placeholders, add dataset DOI (m7, m8) — 10 min
12. Clean rebuild and PDF check — 5 min

Total estimated time: ~90 minutes.

---

## Sources

### Files read
- `main.tex` — preamble, structure, declarations
- `sections/01_introduction.tex` through `sections/08_conclusion.tex` — all sections
- `sections/06_results/01_resolution_scaling.tex` through `07_platform_parity.tex` — all results subsections
- `lib/refs.bib` — all bibliography entries
- `plans/submission-checklist.md` — prior to-do list
- `outputs/related_work_honest_review_2026-05-17.md` — prior §3 peer review

### Hallucination check
- All cited bib keys verified as present in `lib/refs.bib` with author/title/year/venue.
- `chen2023` (Chen et al., "Black hole images: A review", Science China 2023, DOI 10.1007/s11433-022-2059-5): legitimate published review paper; specific claim that it uses "solid-color backgrounds throughout" is unverified but plausible for a review article.
- `wang2004ssim` (Wang et al., IEEE TIP 2004): standard SSIM paper, well-established.
- `gravlensx2025`: bib entry present (Sun et al., ICCV 2025 context); claim is limited to "explored a learned surrogate" — low risk.
- No citations appear to be hallucinated (absent from bib or assigned wrong authorship/year).
- The claim that RK4 "introduces dark artifacts" in the abstract is the only unsupported empirical claim; it is contradicted by the paper's own results.
- The ergosphere claim (M1) is a physics error, not a hallucination about a citation.
