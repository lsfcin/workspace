# Papers
> LaTeX papers, submissions, and manuscript workflows

This subtree stores paper projects that behave like small research codebases: each paper can have its own build rules, submission target, and local workflow.

## Behavioral Cues

- Local-first workflow: edit and compile locally first, then sync to Overleaf.
- Evidence-first writing: avoid claims without explicit source, experiment, or derivation.
- Reproducibility by default: every number in the manuscript should map to script, table, or log.
- Section ownership: each `.tex` file should have a clear purpose (intro, methods, experiments, discussion).
- Revision discipline: prefer small, reviewable commits over large rewrites.

## Recommended Project Layout

Prefer splitting long manuscripts into section files and keeping `main.tex` as orchestration:

```text
main.tex
sections/
	01_intro.tex
	02_background.tex
	03_methods.tex
	04_experiments.tex
	05_results.tex
	06_conclusion.tex
figures/
tables/
refs.bib
```

For this first paper we keep the existing structure and evolve incrementally.

## File Size Guidance

This is a soft policy for writing quality and maintainability, not a hard hook gate.

- `.tex`: target under 250 LOC per section file; warning at 400 LOC.
- `main.tex`: should stay mostly orchestration (`\input` / `\include`) and preamble.
- `.bib`: no strict LOC limit (intentionally monolithic by design), but keep entries consistently formatted.
- Figure data and generated artifacts: avoid manual edits; keep source scripts where possible.

Local PDF builds should use the installed CLI toolchain, not Overleaf as the primary compiler. The following tools are installed on this machine and available in PATH:

```bash
latexmk
xelatex
lualatex
pdflatex
```

For this paper template, use XeLaTeX as default because the class depends on `fontspec` and `Times New Roman`. The practical local command is:

```bash
cd /mnt/workspace/Academy/papers/<paper-folder>
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
```

If you want a clean rebuild:

```bash
cd /mnt/workspace/Academy/papers/<paper-folder>
latexmk -C
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
```

Keep Overleaf as the sync/checkpoint copy for final validation.

## Feynman CLI In This Workflow

`feynman` is installed and can accelerate paper development when used as a research assistant, not a source of truth.

Useful commands:

```bash
feynman status
feynman lit "<topic>"
feynman deepresearch "<topic>"
feynman compare "<topic>"
feynman review "<artifact or draft claim>"
```

Practical usage pattern:

1. Use `feynman lit` or `deepresearch` to gather candidate sources and claims.
2. Manually verify primary sources before inserting any claim in the paper.
3. Use `feynman review` near milestones to simulate reviewer objections.
4. Convert accepted insights into concrete manuscript changes with citations.

## Git Hygiene For Papers

- Track source files (`.tex`, `.bib`, figures, class/style files).
- Ignore local build artifacts (`.aux`, `.log`, `.xdv`, generated PDFs, etc.).
- Commit from the paper repo itself and push to Overleaf remote.
- Keep workflow docs (`CONTEXT.md`, `ROADMAP.md`) versioned when useful to the writing process.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`relativistic_raytracer/`](relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ROADMAP.md`](ROADMAP.md) | — | — | Papers Roadmap |
<!-- routing:end -->
