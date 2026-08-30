# Legibility
> Documentation that decays, naming things once, and how people read a system.
> answers: knowledge decay, controlled vocabulary, decision records, HCI framing

## Documentation & knowledge decay (software-engineering literature)

> The peer-reviewed home of "our CONTEXT.md / ROADMAP claims drifted from the filesystem".

- `[A]` Code Comment Inconsistency Detection and Rectification Using an LLM — ICSE 2025, 17 cites.
- `[A]` Code Comment Inconsistency Detection Based on Confidence Learning — IEEE TSE 2024, 23 cites.
- `[A]` [Detecting Code Comment Inconsistency using Siamese Recurrent
  Network](https://doi.org/10.1145/3387904.3389252) — ICPC 2020, 36 cites; the pre-LLM baseline.
- `[P]` [CCISolver: End-to-End Detection and Repair of Method-Level Code-Comment
  Inconsistency](https://arxiv.org/abs/2506.20558) (2025).

- `[C]` [nocodealex — "your CLAUDE.md is making Claude worse"](https://www.instagram.com/reel/DcQfL4Zty0L/) — [src:
  web:instagram.com] claims Anthropic cut over 80% of Claude Code's own system prompt for the Claude 5 generation with
  no measured coding-eval loss, calling what it had become *over-constraining*, and reports transcripts where one
  request carried contradicting instructions. Its named symptoms — slower answers, simple rules ignored once rules
  conflict, hallucination under long prescriptive blocks — describe this corpus. ⚠ a reel, no study linked; it also
  warns that the repo-specific rules are the load-bearing ones. Lucas asked whether to go the whole way for opus
  (INBOX 2026-08-21) — that variant is named in `/ROADMAP.md`'s ablation item, which is what settles it.

## Standards & practitioner specs

- `[C]` [AGENTS.md](https://agents.md/) · [openai/agents.md](https://github.com/openai/agents.md) —
  the portable agent-instruction file convention our workspace root already follows.
- `[C]` [Anthropic Agent Skills spec](https://github.com/anthropics/skills) — SKILL.md packaging;
  `core/skills/` mirrors it.
- `[C]` [Deterministic Enforcement in Probabilistic LLM Systems: the case for Claude Code
  hooks](https://medium.com/neuralnotions/deterministic-enforcement-in-probabilistic-llm-systems-the-engineering-case-for-claude-code-hooks-64a4196c7d32)
  — the argument our `core/hooks/` layer already embodies; we are ahead of practice here.

## Legibility prior art — decision records & controlled vocabulary

> Evidence behind the legibility work in [/ROADMAP.md](../../ROADMAP.md). Captured 2026-08-18.
> The *measurable* side of legibility — context bloat lowers agent task success and costs >20% more,
> primacy bias means bloat degrades adherence to the earliest rules — is the § Context engineering
> evidence above (Gloaguen/ETH Zurich 2602.11988; *When AGENTS.md Backfires*). Its corollary is the
> one that governs this front: **the fix is subtraction, not more scaffolding.** This section adds the
> *practice* literature for the words and the decisions.

- `[C]` [ADR org / templates](https://adr.github.io/) ·
  [log4brains](https://github.com/thomvaill/log4brains) · [Sherman — Architecture Decision
  Records](https://www.neilsherman.co.uk/blog/architecture-decision-records.html) — the ADR pattern
  (Nygard): one immutable file per decision (Status / Context / Decision / Consequences); a changed
  mind writes a **new** ADR that "supersedes" the old, nothing deleted. Reconciles with WOS's
  hard-delete because it logs *why* — the rejected option space git commit messages lose — not
  work-product, so it is a parallel, much smaller, append-only reasoning log. One decision per file
  keeps superseding clean. Feeds the decision-record work. **Reject** MADR's option-matrix ceremony
  and CI tooling; keep the 3-field core, scoped to consequential decisions only.
- `[A]` [ISO 704 — Terminology work: principles and
  methods](https://www.iso.org/standard/38109.html) · [DDD ubiquitous
  language](https://www.dddcommunity.org/resources/ddd_terms/) · [Hilton — living
  glossaries](https://hilton.org.uk/blog/living-glossary) — term selection trades **precision
  (semantic transparency) over economy**, with clarity a hard constraint and intelligibility the
  tiebreaker — which is exactly Lucas's *"best word wins, simpler breaks the tie."* One term, one
  meaning, enforced by usage; a single canonical glossary (we have `core/SCHEMA.md` § Vocabulary —
  resist forking a second). Feeds the vocabulary work. **Reject** DDD's cross-stakeholder
  term-negotiation workshops — irrelevant for a solo owner.

## Adjacent — HCI framing (thin, worth a dedicated pass)

- `[A]` [Kairotask: Probing the Bridge Between Vague Intents and Spatiotemporal
  Contexts](https://programs.sigchi.org/chi/2026/program/content/230059) (CHI 2026) — vague intent →
  actionable task; the `/inbox` problem, studied.
- `[A]` [From Conversation to Human-AI Common Ground: Extracting Cognitive Workflows for
  Reuse](https://programs.sigchi.org/chi/2026/program/content/222599) (CHI 2026) — reusable workflow
  extraction from sessions; adjacent to `/roundup`.
- `[P]` [One Is Not Enough: How People Use Multiple AI Models in Everyday
  Life](https://arxiv.org/abs/2603.26107) (2026) — multi-model practice; supports the
  provider-agnostic stance.
