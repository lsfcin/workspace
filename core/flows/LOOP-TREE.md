# The Loop Tree
> Canonical map of `/loops`: a router classifies each task and dispatches to a subtree whose step-sequence fits the work. Goals: [loop-engineering](../../brain/goals/loop-engineering.md), [spec-driven-development](../../brain/goals/spec-driven-development.md).

`/loops` is not one pipeline — it is a **tree**. Different task *types* need different step *sequences*, so the trunk ([`loop-router.md`](loop-router.md)) classifies the task and hands off to the right subtree. This file is the map.

```
/loops <task>
   └── loop-router.md  ── classify by TYPE + criticality ──►
         ├── padaria       tiny, revertible change            → loop-engineering.md § Padaria shortcut
         ├── feature        build/change a module              → loop-engineering.md  (contract-first SDD)
         ├── research       investigate / gather / synthesize  → research/sota · research/literature · research/explore · research/compare · … (research/* flows)
         └── architecture   choose between designs             → loop-architecture.md  (→ ADR record)
```

## Subtrees

| Subtree | Distinct shape (why it's its own branch) | Flow | Durable output |
|---|---|---|---|
| **padaria** | no ceremony — one session plans+codes+ships | `loop-engineering.md` § Padaria | commit |
| **feature** | contract-first: panel → contracts before code → TDD → ship | `loop-engineering.md` | shipped code + module `SPEC.md` |
| **research** | plan→scale→gather→draft→cite→review→deliver | `core/flows/research/*` flows | research brief + provenance |
| **architecture** | problem→options→trade-offs→decision→record | `loop-architecture.md` | ADR entry in `SPECS.md` |

**Chaining:** "decide then build" = `architecture` → `feature` (ADR feeds the contract layout). "research then build" = `research` → `feature`. Never merge two shapes into one run.

## The feature subtree carries the SDD requirements

The `feature` subtree is the spec-driven pipeline. Its distinctive spine:

1. **Step 0 permission panel** — the interview asks which human gates the user wants; **default permissive** (agent runs unattended, saves tokens). Records `supervision: io-signoff · arch-review · arch-review-supervised` in the Carry block.
2. **Loop 3.5 Contract Layout (mandatory)** — every touched module's `SPEC.md` (Inputs/Outputs/Invariants) + interface stubs + the connection graph are laid out *before* any code; `core/tools/spec-contract-check` verifies every module has a complete contract and every edge's types match. The contract is never optional; only human *sign-off* on it is (the panel's `io-signoff`).
3. **Concept-Symmetry Review (Loop 3, recurrent)** — per the panel's `arch-review` cadence: a judgment checklist (alike-look-alike, naming coherence, boundary consistency, model soundness) + automation (`codegraph` structural outliers, `/dedup` semantic near-duplicates).
4. **TDD + ship** — tests-first, fill the placeholders against the contracts, `verify:fast` green, ship on a `feature/*` branch.

## Standing enforcement (guards every subtree's output)

- **Spec gates** ([code/SPEC-DRIVE.md](../../code/SPEC-DRIVE.md)): `spec-read-gate` (can't edit a spec-locked module without reading its SPEC), pre-commit `1d` (new module needs a `> spec:`), `spec-scan` ledger. The feature subtree is what *produces* the specs these guard.
- **Git Flow gate** (`.hooks/gitflow-gate.sh`): no direct commits to `main`/`master`/`develop`; `feature|release|hotfix/*` names only, in `code/` repos.
- **verify:fast** (pre-commit `1a`): tests must be green to commit.

## Guardrail — do not proliferate subtrees

A new subtree is justified only when a task type needs a genuinely different *step sequence*, not merely different content. The four here are distinct shapes. A fifth needs the same bar and an entry in this file.

## Provenance

Designed 2026-07-18 (session extending the SDD enforcement rollout). The tree unifies work previously tracked as `[skill-tree]` and `[research-loops]` in the loop-engineering goal. Prior art for the pipeline lineage (Reflexion/LATM/Voyager) is in `loop-engineering.md` § Prior Art; the industry parallel for the feature subtree is GitHub Spec Kit / Kiro (spec → clarify → plan → tasks → implement).
