# Research Summary: Prompt Optimization & Model Selection

## 1. Automatic Prompt Optimization (APO)

Active research area with significant progress:
- **TextGrad (2024)**: Automatic "differentiation" via text — backpropagates natural-language feedback through LLM computation graphs.
- **OPRO (2023)**: LLM proposes better prompts given prior candidates + scores; 8–50% improvement over human prompts.
- **PromptAgent (2024)**: Monte Carlo tree search over prompt space for strategic planning.
- **MPCO (2025)**: Industrial metaprompting generating task-specific prompts across diverse LLMs; 19% performance gain.
- **DSPy (2023+)**: Declarative LLM pipelines — compiles and jointly optimizes all prompts and few-shot demos.

Key challenge: prompts optimized for one LLM often fail with others (cross-model prompt engineering bottleneck).

## 2. LLM Routing / Model Selection

Well-established research area with multiple converging approaches:
- **RouteLLM (ICLR 2025)**: trains router on human preference data (Chatbot Arena) to predict best model for a query.
- **SELECT-THEN-ROUTE (EMNLP 2025)**: classify task via lightweight taxonomy, then route through confidence-escalating cascade.
- **LLMRouter**: open-source library with 16+ routing models.

Key insight: lightweight classification + routing is feasible and cost-effective.

## 3. Industry Effort Levels / Thinking Levels

Major LLM providers have standardized on reasoning/effort control parameters:
- **Anthropic (Claude)**: `thinking: {type: "adaptive"}` `effort`: `low`, `medium`, `high`, `xhigh`, `max`.
- **OpenAI**: `reasoning: {effort: "low|medium|high|xhigh"}`.

Shift is from manual budget to adaptive + effort levels.

## 4. Risks of Intermediate LLM Optimization

| Failure Mode | Description |
|-------------|-------------|
| **Prompt Drift** | Otimizador desvia prompt do intent original |
| **Cross-model incompatibility** | Prompt para um modelo falha em outro |
| **Over-optimization** | Bom no teste, ruim em edge cases |
| **Latency/Cost overhead** | Imposto do roteador |
| **Compounding errors** | Erros pequenos se amplificam em cascata |

Mitigations: human-in-the-loop, A/B testing, few-shot grounding, constraint enforcement.
