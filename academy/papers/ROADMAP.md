# Papers Roadmap

Roadmap for scaling `academy/papers` into a repeatable publication workflow.

## Phase 2 - Manuscript Architecture

- [ ] Define figure/table source traceability convention.

## Phase 3 - Quality Gates (Lightweight)

- [ ] Add optional lint checks (`chktex`) for warnings, without hard blocking commits.
- [ ] Add optional preflight script: compile + bibliography + missing references report.
- [ ] Add section-level checklist for contribution statement, limitations, and reproducibility.

## Phase 4 - Research Acceleration

- [ ] Add a standard Feynman usage playbook (`lit`, `compare`, `review`) per paper phase.
- [ ] Define citation verification workflow: claim -> source -> excerpt -> paper sentence.
- [ ] Before a `refs/<name>.yaml` is filled, download the PDF and convert it to text an AI can read
      end to end — tables kept, figures replaced by their descriptions, zero images — so the yaml is
      written from the paper rather than from its abstract (Lucas, INBOX 2026-08-31).
- [ ] Build reusable prompt snippets for related work and rebuttal preparation.

## Phase 5 - Submission Readiness

- [ ] Add venue-specific checklists (JBCS/SVR): formatting, metadata, anonymization, required statements.
- [ ] Add final pre-submission script/checklist: clean build, figure resolution, bibliography pass, PDF sanity.
- [ ] Add camera-ready delta checklist to track changes after reviews.

## Pesquisa & Ideias Conceituais

- [ ] **Alinhamento intrínseco vs. guardrails: o espaço latente sob a ótica do Vipassana** — investigar se o pré-treinamento não envenena o espaço latente com medos e aversões intrínsecos humanos, tornando os guardrails pós-treino cosméticos; explorar a tese de treinamento fundamentado em equanimidade/harmonia intrínseca (Lucas, INBOX 2026-10-01). Draft de ensaio em `branches/writing/drafts/vipassana-ia-harmonia.md` e potencial seção no manifesto AI4Good (`academy/papers/ai4good/`).

