# Papers
> LaTeX papers, submissions, and manuscript workflows

Each paper lives in its own subdirectory with its own git repo (Overleaf as remote). Local compilation is primary; Overleaf is the sync/checkpoint copy for final validation.

## Starting a New Paper

```bash
python3 /mnt/workspace/.hooks/paper-scaffold.py new <paper-name>
```

This creates `Academy/papers/<name>/` with the full standard layout: `main.tex`, `.latexmkrc`, `.gitignore`, `CONTEXT.md`, `LABELS.md`, and subdirectory `CONTEXT.md` files for `sections/`, `reviews/`, `lib/`, `figures/`, `tables/`, `plans/`. The `reviews/CONTEXT.md` is pre-filled with the tag schema and workflow.

To add missing scaffold files to an **existing** paper without overwriting anything:

```bash
python3 /mnt/workspace/.hooks/paper-scaffold.py adapt <path-to-paper>
```

The `post-edit` hook warns with the adapt command if `reviews/CONTEXT.md` is missing whenever a `.tex` file is saved.

## Behavioral Cues

- Evidence-first: avoid claims without explicit source, experiment, or derivation.
- Reproducibility: every number in the manuscript must trace back to a script, table, or log.
- Revision discipline: prefer small, reviewable commits over large rewrites.

## Project Layout

```text
<paper>/
├── main.tex              ← orchestration only: preamble + \input of sections
├── main.pdf              ← compiled output (gitignored, stays at root)
├── .latexmkrc            ← engine config: aux_dir=build, out_dir=.
├── .gitignore / CONTEXT.md
├── sections/             ← one .tex per section, 200 LOC limit
│   └── 01_intro.tex, 02_methods.tex, ...
├── lib/                  ← venue template files (cls, sty, bst, bib) — do not edit
├── figures/              ← paper figures (prefer source scripts over bare images)
├── tables/               ← extracted table .tex files when a table exceeds ~30 lines
├── plans/                ← research notes, feynman output, literature summaries
└── build/                ← all LaTeX artifacts (gitignored, managed by latexmk)
```

`main.tex` contains no prose. `lib/` is never manually edited. `build/` can be freely deleted.

## File Size

**200 LOC per section file** — enforced by the workspace hook (warning at 150, hard-block at 200). Split by extracting subsection inputs or moving content to `tables/*.tex` / `figures/*.tex`. `main.tex` stays orchestration only. `.bib` has no LOC limit.

## First-Line Description

Every new `.tex` file must open with a `%` comment — the hook blocks new files without it:

```latex
% Methods: scene design, GPU platforms, and numerical integrators.
\section{Methods}
```

## Building

```bash
cd /mnt/workspace/Academy/papers/<paper-folder>
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
latexmk -C && latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex  # clean rebuild
```

Use XeLaTeX for document classes that require `fontspec` (e.g. SBC/JBCS). Artifacts go to `build/`; PDF lands at root.

## LaTeX Interface System (`.texif`)

Every `.tex` file automatically gets a `.texif` sibling generated on save. These are
auto-generated — do not edit them directly.

**Mandatory workflow:**
- **Read `.texif` before reading or editing any `.tex` source file.** The `pre-read` hook
  hard-blocks direct source reads when the interface is current. Always start with the interface.
- The interface contains: section/subsection structure with line numbers, full equation content
  and labels, figure/table captions and labels, listing previews, all `\cite{}` keys used,
  TODO comments, and subsection opening sentences.
- `LABELS.md` at the paper root lists all `\label{}` definitions across every `.tex` file and
  flags dangling `\ref{}` usages. Check it before adding cross-references.

## Reference Reviews (`reviews/`)

Each bib entry must have a corresponding `reviews/<key>.yaml` with structured analysis.
The `post-edit` hook warns about missing review files whenever the `.bib` is edited.

**Mandatory workflow:**
- When adding a new `\cite{key}` to any section, create or update `reviews/key.yaml`.
- When editing the `.bib` file, respond to any REVIEWS MISSING warnings before finishing.
- Read `reviews/<key>.yaml` (via `reviews/CONTEXT.md` for routing) before making claims
  about a paper — the review captures contributions, gaps, and how it relates to this manuscript.

**YAML schema** (`reviews/<key>.yaml`):
```yaml
key: <bib-key>
type: article | book | conference | preprint | thesis
year: <year>
venue: "<journal/conference name>"
url: "<DOI URL or canonical link>"
citations: <exact count or "~N">
contributions:
  - <main contribution — one bullet per distinct claim>
gaps:
  - <limitation or gap relevant to this paper>
tags: [<role-tags-first>, <metric-tags>, <method-tags>, <platform-tags>]
relevance: "<how this reference relates to the current manuscript>"
notes: ~  # free-form: cross-paper lineage, group connections, anything cross-file
```

**Tag categories** (flat list, role tags always first):
- **Role** (1–2): `foundational` · `survey` · `competing-work` · `baseline` · `ground-truth` · `method-source` · `tool` · `application`
- **Metric/physics**: `schwarzschild` · `kerr` · `newtonian` · `special-relativity` · `general-relativity` · `numerical-relativity`
- **Integration method**: `geodesic-tracing` · `analytic-approx` · `rk4-integrator` · `euler-integrator`
- **Platform/content**: `gpu` · `cpu` · `cuda` · `vulkan` · `real-time` · `offline` · `visualization` · `benchmark` · `education` · `textbook` · `astrophysics` · `gravitational-lensing` · `doppler-shift` · `accretion-disk`

Use `notes` for cross-paper prose (lineage, group affiliations) instead of adding `<other-key>:` entries under `relationships:`.

## Related Work Craft

A related work section in a graphics/systems benchmark paper must do three jobs: (1) show the reviewer you know the field completely, (2) build the gap argument brick by brick until it feels inevitable, and (3) explicitly cover the host community's own literature. Failure on any one of these is the most common reason for a "reject, insufficient positioning" decision.

### Subsection structure

Organise by *conceptual axis*, not chronologically. For a benchmark paper the canonical skeleton is:

1. **Implementations** — prior renderers ordered by approach family (numerical integration → precomputed/analytic → learned/neural), then by metric complexity. Within each family, move from offline → interactive → real-time.
2. **Validation / Ground Truth** — how others verified correctness; sets up your own validation section.
3. **Applications** — ordered from highest-profile to most niche (entertainment → science → education). Starting with the highest-profile example (e.g. Interstellar) anchors the field's stakes.

A short closing paragraph (3–5 sentences) synthesises all three subsections into the single gap your paper fills. Name the axes explicitly — do not let the reviewer infer them.

### Three citation tiers

**Tier 1 — Gap-forming (mandatory):** Papers that get closest to your contribution on one axis but not both. Cite these precisely: say what each paper measures and what it omits. A reviewer who knows these papers will check that you described them accurately.

**Tier 2 — Community coverage (non-negotiable for Brazilian venues):** For JBCS/SVR submissions, include at minimum one SIBGRAPI paper, one C&G/Computers & Graphics special-issue paper, and the most relevant SBGAMES paper if one exists. Reviewers from the programme committee will notice their community's work is absent. The IMPA/VISGRAF group (Novello, da Silva, Velho) is the canonical Brazilian reference for GPU non-Euclidean rendering.

**Tier 3 — Frontier (recency signal):** One or two papers from the last 12–18 months that mark where the field is heading. A single sentence is enough; it signals to reviewers that the survey is not stale.

### Making the gap argument tight

- Name the two (or more) axes your benchmark spans. Then for each prior paper show which axes it covers and which it leaves open. A comparison table at the end of the section makes this visual and is appropriate in benchmark papers.
- Use concrete language: "reports performance without quality analysis" beats "does not fully characterise". Feynman's rule — precision over impression.
- Define terminology once (e.g. "real-time: ≥24 fps at 1080p") and use it consistently. Inconsistent use of "real-time" / "near-real-time" / "interactive" is a frequent minor critique.
- Every citation must do exactly one job. If you cannot state in one clause why a paper is cited, it does not belong.

### Reviewer-proofing checklist

Before finalising the section, run through these:

- [ ] Is the Interstellar / DNGR paper (James et al. 2015, CQG) cited? It is the field's most-cited rendering paper.
- [ ] Is every GPU API mentioned in your paper (CUDA, OpenGL, Vulkan, Unity, WebGPU) represented in the related work?
- [ ] Is at least one SIBGRAPI paper cited?
- [ ] Is at least one C&G/Computers & Graphics paper cited?
- [ ] Is there a paper ≤ 2 years old?
- [ ] Does the closing paragraph name your specific axes (platform × integrator, or whatever they are)?
- [ ] Are "real-time", "interactive", and "near-real-time" used consistently with a defined threshold?
- [ ] Does the comparison table (if present) have a row for every paper in Tier 1?

### Getting the venue reviewer form

Reviewer forms for JBCS and SVR are not publicly available — they live inside JEMS (SBC's submission system) and are only visible to registered reviewers. Two practical workarounds:

1. **Ask a colleague who has reviewed for SVR/JBCS** to share the form's dimension titles (they are not NDA'd). Typical dimensions: *Originality*, *Technical Quality*, *Significance*, *Clarity*, *Related Work Coverage*, *Reproducibility*.
2. **Use `/research review "<claim>"` to simulate reviewer objections** on each subsection. This is the most efficient substitute.

JBCS's published criteria (from submissions page): scientific soundness and coherence · originality (no duplication) · clarity · significance. SVR adds: "consolidated research ideas with strong evaluation evidence." Map every paragraph in the related work to at least one of these.

### Images in related work

In computer graphics papers, one carefully composed figure in the related work is welcome and often strengthens the reviewer's confidence that you understand the visual output of prior work. The recommended approach: a labelled mosaic (2–3 columns × 2 rows) showing renders from representative prior systems side by side with your own, with a caption that points out the visual differences (photon ring fidelity, Doppler colour shift, artifact pattern). Keep it to one figure; do not pad. Omit it entirely if you cannot obtain or reproduce an image from at least two prior systems — a partial mosaic is worse than none.

## Writing Quality Standards

These apply to every section, not just related work. Hold every paragraph to all five before committing.

**Argumentative nuance** — claims must be precisely scoped, hedged where uncertainty exists, and logically entailed by the evidence that precedes them. Replace vague intensifiers ("very fast", "significantly better") with measured language ("30% lower latency at 1080p"). Never overstate; never understate. A claim that a careful reviewer could re-scope to something weaker is a claim that will get a comment.

**Long-term coherence** — terminology, notation, and the central argument must be stable across the entire manuscript. Define each concept once; use the same word every time. The introduction's gap statement must be the same gap the conclusion closes. If a new section redefines a term or silently changes scope, it will confuse reviewers and lose the thread for readers who read non-linearly.

**Semantical compression** — academic writing earns its length. Each sentence must carry exactly one new unit of meaning that could not be inferred from the previous sentence. Eliminate throat-clearing openers ("It is important to note that…"), redundant restatement of figures, and motivation paragraphs that say what the section headings already say. The test: can you cut this sentence without losing any information a reviewer would miss?

**Academic taste** — writing registers the author's awareness of the community. This means: cite seminal work even when it is old, because omitting it signals ignorance not modernity; use the community's own vocabulary rather than inventing synonyms; calibrate boldness to evidence (exploratory claims belong in future work, not contributions). For Brazilian venues (JBCS, SVR, SIBGRAPI) explicitly acknowledge Brazilian work in the area — omission reads as oversight even when unintentional.

**Reviewer simulation** — before finalising any paragraph, read it as a hostile reviewer looking for a reason to reject. Common objections: "is this actually novel, or just X applied to Y?", "where is the ablation?", "this claim is not supported by the experiment shown". Write pre-emptive counter-arguments into the prose. A well-positioned limitation paragraph is a shield; a reviewer who spots your limitation and finds you already named it becomes less hostile.

## Research Tools

Use `/research` to invoke the workspace research system, or call tools directly:

```bash
# Paper search
Core/tools/papers "Schwarzschild geodesics" --cat gr-qc --n 15
Core/tools/papers 2501.12345                           # fetch specific arXiv paper

# Web / code search
Core/tools/search "relativistic renderer benchmark"
Core/tools/fetch "https://arxiv.org/abs/2501.12345"

# Full research workflows (via slash command)
/research lit "relativistic raytracing"                # literature review
/research deepresearch "GPU geodesic integration"      # full research brief
/research review sections/03_related_work.tex          # reviewer simulation
```

See [Core/tools/CONTEXT.md](../../Core/tools/CONTEXT.md) for all tools and [Core/flows/](../../Core/flows/) for workflow protocols. Always verify primary sources before committing claims or citations.

## Git

- Source files (`.tex`, `.bib`, figures, `lib/`) live in the paper repo; push to Overleaf remote.
- `build/` and `main.pdf` are gitignored. Version `CONTEXT.md` alongside the manuscript.
- Workspace repo tracks only `CONTEXT.md`; all other paper files belong to the paper repo.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`relativistic_raytracer/`](relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ROADMAP.md`](ROADMAP.md) | — | — | Papers Roadmap |
<!-- routing:end -->
