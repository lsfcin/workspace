# Academy Setup
> LaTeX toolchain and papers compilation workflow for academy/papers

## LaTeX Toolchain

For local PDF builds (without Overleaf):

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

For paper templates requiring `Times New Roman` via `fontspec` (e.g. `\setmainfont{Times New Roman}`):

```bash
printf 'ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true\n' | sudo debconf-set-selections
sudo apt-get install -y ttf-mscorefonts-installer
```

Verify:

```bash
latexmk --version
xelatex --version
```

## Papers Quick Start

Use local-first compilation, Overleaf as sync/checkpoint:

```bash
cd /mnt/workspace/academy/papers/<paper-folder>
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
```

Clean rebuild:

```bash
latexmk -C
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
```
