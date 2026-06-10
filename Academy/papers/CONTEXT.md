# Papers
> LaTeX papers, submissions, manuscript workflows

Each paper: own subdirectory, own git repo (Overleaf as remote). Local compilation primary; Overleaf = sync/checkpoint for final validation.

- Use `/research <flow> <query>` to invoke (e.g. `/research lit "topic"`, `/research review file.tex`).

## Folder Naming Convention

All paper folders follow pattern `YEAR-VENUE-paper_name`. Example:
- `2026-JBCS-relativistic_raytracer`

Use for both `paper-scaffold.py new` and manual creation.

## Starting a New Paper

```bash
python3 /mnt/workspace/.hooks/paper-scaffold.py new <paper-name>
```

Creates `Academy/papers/<name>/` with full standard layout: `main.tex`, `.latexmkrc`, `.gitignore`, `CONTEXT.md`, `LABELS.md`, subdirectory `CONTEXT.md` files for `sections/`, `reviews/`, `lib/`, `images/`, `tables/`, `outputs/`. `reviews/CONTEXT.md` pre-filled with tag schema and workflow.

Add missing scaffold files to **existing** paper without overwriting:

```bash
python3 /mnt/workspace/.hooks/paper-scaffold.py adapt <path-to-paper>
```

`post-edit` hook warns with adapt command if `reviews/CONTEXT.md` missing when `.tex` file saved.

## Behavioral Cues

- Evidence-first: no claims without explicit source, experiment, or derivation.
- Reproducibility: every number traces back to script, table, or log.
- Revision discipline: small reviewable commits over large rewrites.

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
├── images/               ← paper figures (prefer source scripts over bare images)
├── tables/               ← extracted table .tex files when a table exceeds ~30 lines
├── outputs/              ← all research artifacts: metrics, analysis, planning docs, generated reports
└── build/                ← all LaTeX artifacts (gitignored, managed by latexmk)
```

`main.tex` contains no prose. `lib/` never manually edited. `build/` freely deletable.

## File Size

**200 LOC per section file** — enforced by workspace hook (warning at 150, hard-block at 200). Split by extracting subsection inputs or moving content to `tables/*.tex` / `figures/*.tex`. `main.tex` stays orchestration only. `.bib` has no LOC limit.

## First-Line Description

Every new `.tex` file must open with `%` comment — hook blocks new files without it:

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

Use XeLaTeX for document classes requiring `fontspec` (e.g. SBC/JBCS). Artifacts go to `build/`; PDF lands at root.

## LaTeX Interface System

Every `.tex` file gets `.texif` sibling on save. **Read `.texif` before source** — `pre-read` hook hard-blocks direct reads when interface is current. Contents: section/subsection structure with line numbers, equations and labels, figure/table captions, `\cite{}` keys, TODO comments.

`LABELS.md` at paper root: all `\label{}` definitions and dangling `\ref{}` warnings. Check before adding cross-references.

## Reference Reviews (`reviews/`)

Each bib entry gets `reviews/<key>.yaml` — create or update when adding `\cite{key}`. `post-edit` hook warns when `.bib` edited. Read review before making claims about paper.

**YAML schema:**
```yaml
key:           # bib key (matches lib/refs.bib)
type:          # article | book | conference | preprint | thesis
year:
venue:
url:
citations:
contributions: # list — what the paper achieves
gaps:          # list — limitations relevant to this work
tags:          # flat list — role tags first, then domain tags
relevance: "..." # how this relates to the manuscript (required)
notes: ~       # cross-paper lineage, group connections, anything cross-file
```

**Tag categories (flat list, role tags always first):**
- **Role** (1–2, mandatory): `foundational` · `survey` · `competing-work` · `baseline` · `ground-truth` · `method-source` · `tool` · `application`
- **Domain**: defined per-paper in `reviews/CONTEXT.md` — add `## Domain Tags` section once domain is clear.

`baseline` = directly benchmarked in experiments; `competing-work` = same problem space, no direct benchmark. Use `notes` for cross-paper lineage and group affiliations.

## Writing Quality Standards

Hold every paragraph to all five before committing.

- **Argumentative nuance** — scope claims precisely; replace vague intensifiers with measured language ("30% lower latency at 1080p"). Never over- or understate.
- **Long-term coherence** — define each term once, use consistently. Introduction's gap must be same gap conclusion closes.
- **Semantical compression** — each sentence carries exactly one new unit of meaning. Cut throat-clearing openers, redundant figure restatements, motivation paragraphs restating section headings.
- **Academic taste** — cite seminal work even when old; use community vocabulary; for regional venues, explicitly acknowledge local work.
- **Reviewer simulation** — read each paragraph as hostile reviewer seeking rejection. Write pre-emptive counter-arguments into prose; name limitations before reviewer does.

## Research Tools

```bash
Core/tools/papers "Schwarzschild geodesics" --cat gr-qc --n 15
Core/tools/papers 2501.12345                           # fetch specific arXiv paper
Core/tools/search "benchmark topic"
Core/tools/fetch "https://arxiv.org/abs/2501.12345"
/research lit "topic"                                  # literature review
/research review sections/03_related_work.tex          # reviewer simulation
```

See [Core/tools/CONTEXT.md](../../Core/tools/CONTEXT.md) for all tools and [Core/flows/](../../Core/flows/) for workflow protocols. Always verify primary sources before committing claims or citations.

## Git

- Source files (`.tex`, `.bib`, figures, `lib/`) live in paper repo; push to Overleaf remote.
- `build/` and `main.pdf` gitignored. Version `CONTEXT.md` alongside manuscript.
- Workspace repo tracks only `CONTEXT.md`; all other paper files belong to paper repo.
- Overleaf remote authoritative — co-authors edit there directly. Always git pull --rebase before pushing; in conflicts, preserve remote edits and reapply local additions on top.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`2026-JBCS-relativistic_raytracer/`](2026-JBCS-relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |
| [`2026-SIBGRAPI-relativistic_raytracer/`](2026-SIBGRAPI-relativistic_raytracer/CONTEXT.md) | SIBGRAPI 2026 paper on relativistic raytracing benchmarking |
| [`megatruth/`](megatruth/CONTEXT.md) | Hybrid intelligence paper — crowd truth aggregation via mechanism design |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ROADMAP.md`](ROADMAP.md) | — | — | Papers Roadmap |
<!-- routing:end -->
