# Projects
> Where does each internal project live — here, and outside?

Each of these is **its own git repo**, ignored by the workspace's git rather than nested as a
submodule. That is why they are listed by hand: nothing the root repo carries knows their remotes,
and the workspace's own [`ISSUES.md`](ISSUES.md) deliberately does not count them (ruled 2026-09-04)
— a count of what happens to be cloned on one machine is a fact about that disk, not about the
workspace. **Each project keeps its own `ISSUES.md`**, written by its own pre-commit, where the
reader who can fix a finding already is.

The `Path` column is the declaration: it must match the project block in
[`.gitignore`](.gitignore) exactly, which is what makes this table the same on every clone whether
or not that project is checked out here. `Home` is where the work really lives when it is not
GitHub — Overleaf for a paper drafted with co-authors, Drive for a folder of documents.

| Path | Remote | Home |
|------|--------|------|
| `academy/papers/2027-CHI-cria` | [Overleaf](https://git.overleaf.com/6a4c847e31d1ceaba2e92283) | Overleaf is authoritative |
| `academy/papers/ai4good` | [Overleaf](https://git.overleaf.com/6a4d01f88e85188bc8e7684b) | Overleaf is authoritative |
| `academy/papers/mechanism-search` | [github](https://github.com/lsfcin/mechanism-search) | — |
| `academy/papers/mutual-credit-ai` | [github](https://github.com/lsfcin/mutual-credit-ai) | — |
| `academy/papers/pls-pix` | [github](https://github.com/lsfcin/pls-pix) | — |
| `academy/papers/wos-ablation` | [github](https://github.com/lsfcin/wos-ablation) | — |
| `branches/casinhas` | [github](https://github.com/lsfcin/casinhas) | [Drive `personal`](https://drive.google.com/drive/folders/1PeE-3Rf3fBJi20AR8QJZZE0Hfd-l2RUM) |
| `branches/instituto` | [github](https://github.com/lsfcin/instituto) | — |
| `code/aiwbot` | [github](https://github.com/lsfcin/aiwbot) | — |
| `code/apptime` | [github](https://github.com/lsfcin/apptime) | — |
| `code/corpora` | [github](https://github.com/lsfcin/corpora) | — |
| `code/cria` | [github](https://github.com/lsfcin/cria) | — |
| `code/dobra` | [github](https://github.com/lsfcin/dobra) | — |
| `code/flows` | [github](https://github.com/lsfcin/flows) | — |
| `code/freeai` | [github](https://github.com/lsfcin/freeai) | — |
| `code/futebots` | — | not cloned here |
| `code/gira` | [github](https://github.com/lsfcin/gira) | — |
| `code/isometric-perspective` | — | not cloned here |
| `code/isoroll-content` | [github](https://github.com/lsfcin/isoroll-content) | — |
| `code/isoroll-module` | [github](https://github.com/lsfcin/isoroll) | repo name differs from the path |
| `code/laplata` | [github](https://github.com/lsfcin/laplata) | — |
| `code/ppc` | [github](https://github.com/lsfcin/ppc) | — |
| `code/shortvid` | — | not cloned here |
| `code/spacemantics` | [github](https://github.com/lsfcin/spacemantics) | — |
| `code/statem` | — | not cloned here |
| `code/voti` | [github](https://github.com/lsfcin/voti) | — |

A `—` under `Remote` means this clone could not be asked: the project is declared and is not checked
out here. That is a question for whoever has it, never a value to invent — an address written from
memory is worse than an empty cell, because the empty one asks.

What each project is, and what it is for, stays in its own `CONTEXT.md`; the routing tables in
[`code/`](code/CONTEXT.md), [`academy/`](academy/CONTEXT.md) and [`branches/`](branches/CONTEXT.md)
are where you go to read that. This file answers only where it lives.
