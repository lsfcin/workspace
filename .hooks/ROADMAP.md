# Interface Policy — Implementation Roadmap
> Universal interface generation and enforcement across all supported languages

## Phases 1–5 — Complete ✓

| Phase | What | Status |
|-------|------|--------|
| 1 | Generation: `.py`→`.pyi`, `.js`/`.ts`→`.d.ts`, `.dart`→`.dart.api` via post-edit.sh | ✓ |
| 2 | Enforcement: pre-read.sh hard-blocks source reads when interface is current | ✓ |
| 3 | Dart extractor: `dart-api-extract.py` — public signatures, no Dart SDK required | ✓ |
| 4 | context_synchronizer.py: correct interface lookup for all languages | ✓ |
| 5 | Docs: SETUP.md, Code/CONTEXT.md updated | ✓ |

---

## Phase 6 — LaTeX Interface System (`.tex.if`) + Reference Reviews (`reviews/`)

### Design decisions
- Interface files use `.tex.if` extension (analogous to `.pyi` for Python)
- Applies to **all** `.tex` files — no folder filtering, no exclusions
- `LABELS.md` at paper root: cross-file label registry + dangling `\ref{}` detection
- `reviews/<key>.yaml` per bib entry: curated reference analysis
- `.bib` edits trigger a check warning about missing `reviews/*.yaml` files

### `.tex.if` content (auto-extracted)
- Structure tree: `\section` / `\subsection` / `\subsubsection` with line numbers
- Equations: full content + label + environment type
- Figures: full caption + label + line number
- Tables: full caption + label + line number
- Listings: caption + language + label + line count + first 5 lines
- Citations: sorted unique list of `\cite{}` keys (bridges to `reviews/`)
- TODO comments: line number + text
- Subsection openings: first 10 words of the first prose paragraph per `\subsection`

### `reviews/<key>.yaml` schema
```yaml
key: <bib-key>
type: article | book | conference | preprint | thesis
year: <year>
venue: "<journal/conference>"
url: "<DOI or canonical link>"
citations: <count or "~N">
contributions:
  - <main contribution>
gaps:
  - <limitation or gap>
tags: [<method>, <domain>, <role-tag>]
  # role tags: foundational | baseline-we-beat | method-we-extend | survey | competing-work | tool
relationships:
  this_paper: "<how this work relates to the manuscript>"
  <other-bib-key>: "<relationship>"
```

### Enforcement vs. induction
| Behavior | Level |
|----------|-------|
| `.tex.if` generated on `.tex` write | Enforced — `post-edit.sh` |
| `pre-read` blocks `.tex` when `.tex.if` current | Enforced — `pre-read.sh` |
| `pre-read` warns when `.tex.if` stale | Enforced — `pre-read.sh` |
| `LABELS.md` regenerated on any `.tex` write | Enforced — `tex-interface-gen.py` |
| `.tex.if` in CONTEXT.md Interface column | Enforced — `workspace_scanner.py` |
| `reviews/CONTEXT.md` synced on `.yaml` write | Enforced — `context_synchronizer.py` |
| Missing `reviews/*.yaml` warned on `.bib` edit | Induced — `post-edit.sh` bib-check |
| Agent creates `reviews/*.yaml` for new `\cite{}` | Induced — `Academy/papers/CONTEXT.md` cues |

### Phase 6 tasks
- [x] `.hooks/ROADMAP.md` — this document
- [x] `.hooks/tex-interface-gen.py` — new script (parser, LABELS, bib-check)
- [x] `.hooks/post-edit.sh` — `.tex)` and `.bib)` cases added
- [x] `.hooks/pre-read.sh` — `.tex)` case added
- [x] `.hooks/workspace_scanner.py` — `.tex` → `.tex.if` in `interface_for()`
- [x] `Academy/papers/CONTEXT.md` — behavioral cues for `.tex.if` and `reviews/`
- [x] `relativistic_raytracer/reviews/` — folder + CONTEXT.md + 22 initial YAML files
- [x] Initial `.tex.if` seeded for all existing `.tex` files
- [x] Initial `LABELS.md` generated
