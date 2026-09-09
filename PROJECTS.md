# Projects
> Where does each internal project live — here, and outside?

The workspace itself is one repo, [`lsfcin/workspace`](https://github.com/lsfcin/workspace). Every
project below is **its own git repo**, ignored by that one rather than nested as a submodule, which
is why nothing the root repo carries knows their remotes and the workspace's own
[`ISSUES.md`](ISSUES.md) deliberately does not count them (ruled 2026-09-04) — a count of what
happens to be cloned on one machine is a fact about that disk, not about the workspace. **Each
project keeps its own `ISSUES.md`**, written by its own pre-commit, where the reader who can fix a
finding already is.

**Which rows exist is not read off this disk.** The `Path` column comes from the project block in
[`.gitignore`](.gitignore), which is tracked and therefore says the same thing on every clone
whether or not a given project is checked out. `Remote` is where the work is versioned — GitHub, or
Overleaf for a paper drafted with co-authors. `Drive` is a folder holding the same work, and `sync`
means a `drive_sync.json` declares it, so [`core/tools/files/gdrive`](core/tools/files/CONTEXT.md)
can reach it; a Drive home with no `sync` is mirrored by hand.

The table is redrawn at every session close by
[`core/tools/wos/close/repomap.py`](core/tools/wos/close/CONTEXT.md), which fills a cell from what
it can confirm here and **never blanks one it cannot**. That is why a `—` is trustworthy: an address
written from memory is worse than an empty cell, because the empty one asks — and an address erased
because one machine lacks the clone is worse than either. A row for a project not checked out here
keeps whatever the machine that has it wrote.

<!-- projects:start -->
| Path | Remote | Drive |
|------|--------|-------|
| `academy/papers/2026-JBCS-relativistic_raytracer` | [Overleaf](https://git.overleaf.com/6a06aab5ad89bc3e2628f977) | — |
| `academy/papers/2026-SIBGRAPI-relativistic_raytracer` | [Overleaf](https://git.overleaf.com/6a0cbc7958195756380a96cb) | — |
| `academy/papers/2027-CHI-cria` | [Overleaf](https://git.overleaf.com/6a4c847e31d1ceaba2e92283) | — |
| `academy/papers/2027-ICLR-dobra` | [Overleaf](https://git.overleaf.com/6a48660e2fa100e8e2c6bc04) | — |
| `academy/papers/ai4good` | [Overleaf](https://git.overleaf.com/6a4d01f88e85188bc8e7684b) | — |
| `academy/papers/mechanism-search` | [github](https://github.com/lsfcin/mechanism-search) | — |
| `academy/papers/mutual-credit-ai` | [github](https://github.com/lsfcin/mutual-credit-ai) | — |
| `academy/papers/pls-pix` | [github](https://github.com/lsfcin/pls-pix) | — |
| `academy/papers/spacemantics` | [Overleaf](https://git.overleaf.com/6a5430c59a5fe10adf1fc68b) | — |
| `academy/papers/wos-ablation` | [github](https://github.com/lsfcin/wos-ablation) | — |
| `branches/casinhas` | [github](https://github.com/lsfcin/casinhas) | [`personal`](https://drive.google.com/drive/folders/1PeE-3Rf3fBJi20AR8QJZZE0Hfd-l2RUM) |
| `branches/instituto` | [github](https://github.com/lsfcin/instituto) | — |
| `code/aiwbot` | [github](https://github.com/lsfcin/aiwbot) | — |
| `code/apptime` | [github](https://github.com/lsfcin/apptime) | — |
| `code/corpora` | [github](https://github.com/lsfcin/corpora) | — |
| `code/cria` | [github](https://github.com/lsfcin/cria) | — |
| `code/dobra` | [github](https://github.com/lsfcin/dobra) | — |
| `code/flows` | [github](https://github.com/lsfcin/flows) | — |
| `code/freeai` | [github](https://github.com/lsfcin/freeai) | — |
| `code/futebots` | — | — |
| `code/gira` | [github](https://github.com/lsfcin/gira) | — |
| `code/isometric-perspective` | — | — |
| `code/isoroll-content` | [github](https://github.com/lsfcin/isoroll-content) | — |
| `code/isoroll-module` | [github](https://github.com/lsfcin/isoroll) | — |
| `code/laplata` | [github](https://github.com/lsfcin/laplata) | — |
| `code/obra` | [github](https://github.com/lsfcin/obra) | — |
| `code/ppc` | [github](https://github.com/lsfcin/ppc) | — |
| `code/shortvid` | — | — |
| `code/spacemantics` | [github](https://github.com/lsfcin/spacemantics) | — |
| `code/statem` | — | — |
| `code/voti` | [github](https://github.com/lsfcin/voti) | — |
<!-- projects:end -->

`code/isoroll-module` is the one path whose repo carries another name: the remote is `lsfcin/isoroll`.
A `—` under `Remote` means this clone could not be asked, and the project is declared without being
checked out here. That is a question for whoever has it, never a value to invent.

Two things on this disk are deliberately not rows. `outputs/links` is a clone and not a project: it
is the publish target [`core/tools/links/cfpages`](core/tools/links/CONTEXT.md) rebuilds whole from
`links.txt`, and [`.gitignore`](.gitignore) keeps all of `outputs/` out of the workspace. And
[`academy/teaching/ai4good/`](academy/teaching/CONTEXT.md) is the one folder with a live Drive sync
and no repo of its own — the workspace tracks it directly, so it has no line here to hang a row on.

What each project is, and what it is for, stays in its own `CONTEXT.md`; the routing tables in
[`code/`](code/CONTEXT.md), [`academy/`](academy/CONTEXT.md) and [`branches/`](branches/CONTEXT.md)
are where you go to read that. This file answers only where it lives.
