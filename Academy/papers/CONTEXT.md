# Papers
> LaTeX papers, submissions, and manuscript workflows

This subtree stores paper projects that behave like small research codebases: each paper can have its own build rules, submission target, and local workflow.

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

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`relativistic_raytracer/`](relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |
<!-- routing:end -->