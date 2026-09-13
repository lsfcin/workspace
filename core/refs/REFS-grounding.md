# References — grounding, doubt, and when a checker can refuse
> What the field knows about an agent being confidently wrong, and the mechanisms that catch it.
> The grouping is the finding: every mechanism here that can truly refuse is a parser or a solver,
> and none is a judge.

Gathered 2026-09-12 for the `ROADMAP.md` 🔴 item, by four workers over two rounds each. The reasoning
built on these, against this workspace's own incident record, is
[`../experiments/confident-wrongness.md`](../experiments/confident-wrongness.md).

## Mechanisms that can refuse — parsers and solvers, never a judge

- `[A]` [Grammar-Constrained Decoding](https://aclanthology.org/2023.emnlp-main.674/)
  (EMNLP 2023) — invalid output cannot be sampled at all; the checker is fused into decoding, not consulted after.
- `[A]` [BeliefBank](https://aclanthology.org/2021.emnlp-main.697.pdf)
  (EMNLP 2021) — a belief enters memory only after a weighted MaxSAT solver checks it against declared constraints.
- `[A]` [Conflict-Aware Memory for Embodied Agents](https://aclanthology.org/2026.acl-long.1306.pdf)
  (ACL 2026) — named Conflict Detection Rules flag conflicting memories before write; +14-15pp planner accuracy.
- `[A]` [Learn to Refuse](https://aclanthology.org/2024.emnlp-main.212/)
  (EMNLP 2024) — refuses on scope-membership against a traceable knowledge base, not on a confidence score.
- `[A]` [LLatrieval](https://aclanthology.org/2024.naacl-long.305/)
  (NAACL 2024) — gates the *evidence* before generation rather than the claim after it.
- `[B]` [ProVe](https://doi.org/10.3233/SW-233467)
  (Semantic Web Journal, 2024) — scores whether a KG triple is supported by its cited text before it is trusted.
- `[B]` [Symbolic logic validation of LLM interactions](https://link.springer.com/article/10.1007/s44427-026-00029-4)
  (Acta Univ. Sapientiae, Informatica) — Answer Set Programming over prompt and output yields a Go/NoGo plus a trace.
- `[B]` [CMVKG-Guard](https://link.springer.com/article/10.1007/s44163-026-01778-z)
  (Discover AI, Springer) — low-scoring tokens trigger a beam search substituting a grounded token: correct in place.
- `[B]` [Early Rejection with Partial Reward Modeling](https://aclanthology.org/2025.findings-emnlp.551/)
  (Findings of EMNLP 2025) — discards a beam mid-generation on a partial score; honest that a correct beam can die.
- `[C]` [Guardrails AI](https://github.com/guardrails-ai/guardrails)
  — `OnFailAction.EXCEPTION` aborts the call; refusal is opt-in, and the other actions do not refuse.
- `[C]` [factgate](https://github.com/agiwhitelist/factgate)
  — fallible model proposes claims, a deterministic layer returns VERIFIED / BLOCK / HELD.
- `[C]` [citation-abstention-rag](https://github.com/jkelly-dev1/citation-abstention-rag)
  — a claim ships only if its quote resolves to an exact span; abstains with a reason code below threshold.
- `[V]` [Azure AI groundedness detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)
  (Microsoft docs) — flags ungrounded spans before the response reaches the caller; correction is preview-only.
- `[V]` [LiteLLM judge guardrail](https://docs.litellm.ai/docs/proxy/guardrails/llm_as_a_judge)
  — a judge below threshold returns HTTP 422 instead of the response; the same config defaults to log-and-return.
- `[P]` [DSPy Assertions](https://arxiv.org/abs/2312.13382)
  — a hard `Assert` past its retry cap raises rather than returning a silently wrong output.
- `[P]` [ConsistencyGate](https://arxiv.org/abs/2607.22962)
  — write-time admission control for agent memory; admits a fact only above a support threshold.
- `[P]` [Evidence-Locked Derive-Gate-Repair](https://arxiv.org/abs/2608.07813)
  — a gate over the judge: it may override an evidence-backed consensus only with an extractive certificate.

## Checkers that only score — the field's actual default

- `[A]` [CRITIC](https://arxiv.org/abs/2305.11738)
  (ICLR 2024) — verify-then-revise with tools, but the loop's final branch returns the last candidate, never a refusal.
- `[A]` [Reflexion](https://arxiv.org/abs/2303.11366)
  (NeurIPS 2023) — verbal reflection into episodic memory and a retry next trial; a loop, not a gate.
- `[A]` [DiVeRSe](https://aclanthology.org/2023.acl-long.291/)
  (ACL 2023) — a step-aware verifier prunes reasoning chains from the vote, but something always wins and ships.
- `[A]` [MetaReflection](https://aclanthology.org/2024.emnlp-main.477/)
  (EMNLP 2024) — past reflections distilled into a semantic memory bank that conditions prompts; no emission gate.
- `[A]` [Recursive Introspection](https://arxiv.org/html/2407.18219v1)
  (NeurIPS 2024) — self-correction fine-tuned into the weights; no separate checker, so nothing can halt.
- `[A]` [MIRAGE](https://aclanthology.org/2024.emnlp-main.347/)
  (EMNLP 2024) — saliency attributes answer tokens to the documents that drove them, with nothing acting downstream.
- `[A]` [ContextCite](https://proceedings.neurips.cc/paper_files/paper/2024/hash/adbea136219b64db96a9941e4249a857-Abstract.html)
  (NeurIPS 2024) — attribution to causal context spans; the poisoning use is a demonstration, not a block.

## Against asking the model how sure it is

- `[A]` [Relying on the Unreliable](https://aclanthology.org/2024.acl-long.198/)
  (ACL 2024) — 47% error rate among responses deployed models gave as confident.
- `[A]` [Just Ask for Calibration](https://aclanthology.org/2023.emnlp-main.330/)
  (EMNLP 2023) — verbalized confidence beats raw probability post-RLHF, cutting ECE ~50%, but buys no guarantee.
- `[A]` [Linguistic Calibration of Long-Form Generations](https://proceedings.mlr.press/v235/band24a.html)
  (ICML 2024) — a rare positive shift result, and aimed at human decisions rather than an automated threshold.
- `[B]` [Investigating Selective Prediction](https://aclanthology.org/2022.findings-acl.158/)
  (ACL Findings 2022) — over 17 datasets no method beats plain softmax consistently; all degrade out of distribution.
- `[B]` [Miscalibrated In-Context Learners](https://aclanthology.org/2025.findings-acl.603/)
  (ACL Findings 2025) — miscalibration is the default in low-resource and shifted setups.
- `[P]` [Self-Evaluation Improves Selective Generation](https://proceedings.mlr.press/v239/ren23a.html)
  — **a NeurIPS 2023 *workshop* paper on a refereed-looking publisher host. Kept as the venue-guessing trap.**

## The one licensed confidence gate: conformal, precondition checked

- `[A]` [Conformal Prediction for NLP: A Survey](https://aclanthology.org/2024.tacl-1.82/)
  (TACL 2024) — only conformalized scores are guarantees, and only under exchangeability.
- `[A]` [SConU](https://aclanthology.org/2025.acl-long.934/)
  (ACL 2025) — tests whether a sample violates the exchangeability the guarantee rests on, before trusting it.
- `[A]` [CALM](https://proceedings.neurips.cc/paper_files/paper/2022/hash/6fac9e316a4ae75ea244ddcef1982c71-Abstract-Conference.html)
  (NeurIPS 2022) — a deployed control-flow gate on confidence with a distribution-free risk guarantee, i.i.d. only.
- `[B]` [ConU](https://aclanthology.org/2024.findings-emnlp.404/)
  (Findings of EMNLP 2024) — a conformal criterion over black-box self-consistency holding coverage on real output.
- `[B]` [Non-Exchangeable Conformal Language Generation](https://aclanthology.org/2024.findings-eacl.129/)
  (Findings of EACL 2024) — coverage bounded by nearest-neighbour weights, so it degrades instead of breaking.

## Agreement is not evidence of correctness

- `[A]` [Debate or Vote](https://proceedings.neurips.cc/paper_files/paper/2025/file/934252acd87f254d5d4672fbde283bd2-Paper-Conference.pdf)
  (NeurIPS 2025) — a theorem: debate induces a martingale over beliefs, so it does not raise expected correctness.
- `[A]` [Latent Self-Consistency](https://ojs.aaai.org/index.php/AAAI/article/download/40536/44497)
  (AAAI 2026) — exact-match voting misses agreement that is really there when long answers differ lexically.
- `[A]` [A-MemGuard](https://arxiv.org/html/2510.02373v1)
  (ICML 2026) — a mechanically checkable memory gate whose bar is itself a majority vote, so it inherits this section.
- `[P]` [Nine Judges, Two Effective Votes](https://arxiv.org/html/2605.29800v1)
  — a 9-judge, 7-family panel carries the value of ~2 independent votes; the best single judge matches or beats it.
- `[P]` [When LLMs Agree, Are They Right?](https://arxiv.org/html/2607.08065v2)
  — agreement predicts correctness only weakly, and worst for the most self-consistent model.

## What production ships instead: an unchecked model call at the write

- `[V]` [LangMem core concepts](https://github.com/langchain-ai/langmem/blob/main/docs/docs/concepts/conceptual_guide.md)
  — every write asks an LLM to decide against free-text instructions; the doc names over/under-extraction as unresolved.
- `[C]` [mem0](https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py)
  — `_add_to_vector_store` emits ADD/UPDATE/DELETE/NONE from one LLM call, with nothing checking it.
