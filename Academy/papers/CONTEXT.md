# Papers
> LaTeX papers, submissions, and manuscript workflows

Each paper lives in its own subdirectory with its own git repo (Overleaf as remote). Local compilation is primary; Overleaf is the sync/checkpoint copy for final validation.

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
relationships:
  this_paper: "<how this reference relates to the current manuscript>"
notes: ~  # free-form: cross-paper lineage, group connections, anything cross-file
```

**Tag categories** (flat list, role tags always first):
- **Role** (1–2): `foundational` · `survey` · `competing-work` · `baseline` · `ground-truth` · `method-source` · `tool` · `application`
- **Metric/physics**: `schwarzschild` · `kerr` · `newtonian` · `special-relativity` · `general-relativity` · `numerical-relativity`
- **Integration method**: `geodesic-tracing` · `analytic-approx` · `rk4-integrator` · `euler-integrator`
- **Platform/content**: `gpu` · `cpu` · `cuda` · `vulkan` · `real-time` · `offline` · `visualization` · `benchmark` · `education` · `textbook` · `astrophysics` · `gravitational-lensing` · `doppler-shift` · `accretion-disk`

Use `notes` for cross-paper prose (lineage, group affiliations) instead of adding `<other-key>:` entries under `relationships:`.

## Feynman CLI

`feynman` accelerates research — not a source of truth. Always verify primary sources before committing claims or citations.

```bash
feynman lit "<topic>"           # candidate papers
feynman deepresearch "<topic>"  # research brief
feynman review "<draft claim>"  # simulate reviewer objections
```

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
