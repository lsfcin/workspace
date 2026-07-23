# Craft — Provider Routing
> Which concrete model fills each tier, per provider; the availability probe; the delegation
> direction; and how to refresh the table. **VOLATILE** — model ids and prices go stale.

Load this **once per chain**, in the orchestrator, before Loop 0 — it is what fills the Carry
block's `provider:` / `tier-map:` fields. Executors never need it: they are handed a resolved
`model=` in the spawn prompt. Keeping it out of [`craft.md`](craft.md) is the point — a per-loop
session that loads these tables pays for them eight times.

Tier semantics (low/medium/high/max) and the escalation rules live in
[`craft.md`](craft.md) § Autorouting. This file only maps tier → concrete model.

## Tier → provider → model mapping — VOLATILE

Tiers are vertical (low/medium/high/max) — work capacity. Provider selects *which* models fill the tiers and never cross-contaminates billing across a single chain. The orchestrator resolves the active provider **once, up front**, before Loop 0; every executor in that chain runs on the same provider unless delegation is explicitly downward (see `Provider delegation` below).

**Fastest provider detection (use this):**

```bash
opencode models 2>&1 | grep -E "^\S" | sed 's#/.*##' | sort -u        # all providers configured
# Identify the orchestrator's own provider:
echo "$OPENCODE_MODEL" 2>/dev/null                                    # opencode sets the active model env-style; not always exported
opencode status 2>&1 | grep -iE 'model|provider'                      # live session reveals active model + provider
# Fallback — read the opencode config file's "model" key:
rtk grep -A0 -E '"model":\s*"[^/]+' ~/.config/opencode/opencode.json[c]? opencode.json[c]? 2>/dev/null
```

The active model id is `<provider>/<model-id>`. Take the **provider prefix** (everything before the first `/`) — that is the chain's provider and the row of the table below that fills its tiers. Detection must happen *before* Loop 0 so the Carry block can record it (see `## Carry` `provider:` field).

### Provider availability — verify BEFORE filling tiers

A provider exists for routing **only if it appears in `opencode models`** (i.e. its API key is configured and at least one model resolves). Pinning a tier to an unavailable model fails the loop with `Tool not found` / `model_not_found`. So the very first orchestrator action — before Loop 0 — is the availability probe:

```bash
opencode models 2>&1 | awk -F/ '{print $1}' | sort -u     # which providers responded with keys
opencode models 2>&1 | grep -E '^<provider>/' | grep -ivE 'safety|rerank|embed|guard|tts|voice|flux|gemma|paligemma|cosmos|bevformer|gliner|whisper|image|translate|drive|streampetr|sparsedrive|usd'   # coding-capable text models on <provider>
```

**As of 2026-07-16 (this workspace), the configured opencode providers are:**

```
alibaba-coding-plan, google, nvidia, ollama-cloud, opencode (Zen free), openrouter
```

`anthropic` and `copilot` are **NOT** opencode providers here — the anthropic tier (opus/sonnet/haiku) and the copilot tier exist only when the chain runs under the **Claude Code** or **Copilot CLI** runtimes respectively. Inside opencode those models are reachable **only via the `openrouter/anthropic/*` and `openrouter/.../...` cross-listed endpoints** — and reaching them consumes openrouter credits, never a flat-fee anthropic clock. The provider delegation hierarchy below reflects this: in opencode, "anthropic" reduces to "openrouter/anthropic/* on credits" — so it sits **below** openrouter-only models only when cheaper, which is rarely the case.

### Per-provider tier maps — filled from availability + benchmarks

For each configured provider, the tier is filled with the **best available** coding-capable text model on that provider, ranked by ArtificialAnalysis agentic_index → coding_index → intelligence_index, then cost (cheaper wins ties). If a tier has **no** available coding-capable model on that provider, the row reads `NONE` — that tier **cannot be served on this provider**, and the orchestrator must either (a) delegate that loop downward to a provider that has it (cost-direction permits), or (b) escalate the loop to the user as blocked. **Never substitute a non-coding/embed/safety/vision/TTS model into a tier — those exist on nvidia et al. but cannot run code loops.**

| Provider | low | medium | high | max | Billing | Notes |
|---|---|---|---|---|---|---|
| **nvidia** | `nvidia/deepseek-ai/deepseek-v4-flash` | `nvidia/deepseek-ai/deepseek-v4-pro` | `nvidia/z-ai/glm-5.2` | `nvidia/nvidia/nemotron-3-ultra-550b-a55b` | free (rate/time-limited) | **No Kimi, no Claude on nvidia** — only the deepseek-v4 family + glm-5.2 + nemotron-3 line qualify for coding tiers. All other nvidia models (qwen-coder, mistral, gpt-oss, step, minimax, llama) are *available* but rank below on agentic_index, so they are reserves, not defaults. |
| **openrouter** | `openrouter/deepseek/deepseek-v4-flash` (or `opencode/deepseek/deepseek-v4-flash:free` for free quota) | `openrouter/deepseek/deepseek-v4-pro` · alt `openrouter/moonshotai/kimi-k2.6` (kimi has higher coding_index 61.8 vs ds-pro 59.4 but far weaker agentic 30.3 vs 36.4 — pick kimi for purely-coding medium loops, ds-pro for agent work) | `openrouter/z-ai/glm-5.2` | `openrouter/anthropic/claude-opus-4.8` (or `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` for free max) | credits (per-token) | Widest selection; **most expensive**. Always prefer downward delegation when running here. |
| **opencode (Zen, free)** | `opencode/deepseek-v4-flash-free` | `opencode/mimo-v2.5-free` · alt `opencode/hy3-free` | `opencode/north-mini-code-free` | `opencode/nemotron-3-ultra-free` | free (Zen) | All-Zen keeps the chain free; treat like nvidia (rate-limited, hard ceiling at its own max). |
| **anthropic (Claude Code runtime only)** | `anthropic/claude-haiku-4.5` | `anthropic/claude-sonnet-5` | `anthropic/claude-opus-4.8` | Fable-class, gated | flat-fee monthly | Reachable ONLY under Claude Code. Inside opencode, anthropic models come via `openrouter/anthropic/*` on credits — never silently pulled. |
| **copilot (Copilot CLI runtime only)** | (GitHub Models free tier) | (GitHub Models free tier) | (GitHub Models free tier) | — | included w/ Copilot sub | Reachable ONLY under Copilot CLI; stands between anthropic and nvidia in delegation rank because of its free-ish allocation. |
| **alibaba-coding-plan** | (per alibaba-coding-plan `opencode models` list — qwen/glm/kimi re-sellers) | ... | ... | ... | per-plan | Filled from its `opencode models` listing — qwen3-coder-next, glm-5, kimi-k2.5, minimax-m2.5. Map tiers the same way (agentic_index first), verify availability before relying. |
| **google / ollama-cloud** | (per their `opencode models` listings) | ... | ... | ... | mixed | Fill only if a chain explicitly runs on these providers; defaults below assume nvidia/openrouter/opencode. |

**Default provider per orchestrator runtime (chicken-egg resolved):** the orchestrator inherits its own runtime's provider — Claude Code → anthropic, Copilot CLI → copilot, opencode → detected via the probe above (nvidia by default in this workspace, as the active model is `nvidia/z-ai/glm-5.2`).

**Benchmarks driving tier selection (ArtificialAnalysis indices: intelligence / coding / agentic / cost $/1M-out, source `openrouter.ai/api/v1/models`):**

| Model | intel | coding | agentic | $/M out | Recommended tier |
|---|---|---|---|---|---|
| claude-opus-4.8 | 55.7 | 74.3 | 47.2 | $25 | high (anthropic / openrouter-as-max) |
| claude-sonnet-5 | 53.4 | 71.5 | 46.7 | $10 | medium (anthropic) |
| glm-5.2 (z-ai) | 51.1 | 68.8 | 43.1 | $2.94 | **high (nvidia)** — agentic winner among free options |
| deepseek-v4-pro | 44.3 | 59.4 | 36.4 | $0.87 | **medium (nvidia / openrouter)** |
| kimi-k2.6 (moonshot) | 44.2 | 61.8 | 30.3 | $4.00 | medium (openrouter, agentic-emphasis alt) |
| deepseek-v4-flash | 40.3 | 56.2 | 31.1 | $0.20 | **low (nvidia / openrouter)** — fastest, cheapest |
| claude-haiku-4.5 | 29.6 | 43.9 | 16.4 | $5.00 | low (anthropic only — Haiku is premium-tier-only) |
| nemotron-3-ultra (550b) | — | — | — | (free on nvidia) | max (nvidia) — reasoning-heavy, fallback for unsolvable high-tier cases |

User instinct confirmed: **GLM 5.2 > DeepSeek V4 Pro > DeepSeek V4 Flash** for nvidia. Source data above; rerun the snippet under `## Provider routing provenance` to refresh quarterly.

## Provider delegation — cost-directional, downward only

Delegation across providers is **strongly directional**: an orchestrator on a paid/scarce provider may delegate loops **downward** to cheaper/free subagents to save cost; a free provider may **never** silently pull up to a paid one.

```
openrouter  →  anthropic  →  copilot  →  nvidia
   credits        flat-mo                 free
```

| Orchestrator provider | May spawn subagents on | May NOT spawn on |
|---|---|---|
| openrouter (credits) | nvidia, anthropic, copilot (downward to save cost) | — |
| anthropic (flat-fee) | copilot, nvidia | openrouter (direct $ waste vs flat-fee anthropic equivalence) |
| copilot | nvidia | openrouter, anthropic |
| nvidia (free) | — (nothing — nvidia is the ceiling) | openrouter/anthropic/copilot — **stop on max-tier failure, surface to user** |

**Rules:**

1. A single chain stays within one provider by default.
2. Downward delegation is *encouraged* (cost-saving, never blocked) — e.g., an openrouter orchestrator may run all 8 loops on nvidia sub-agents and pay nothing. Audit tag on the loop file: `executor: loop-N model=<nvidia/...> tier=<tier> deleg=openrouter→nvidia`.
3. **Upward promotion** (a max-tier escalation that would land on a higher-billing provider) **requires explicit user consent every time** — surface the evidence line + the cost delta (e.g. `loop-3 escalated to max → would spend ~$X of openrouter credits; OK?`). The orchestrator never silently crosses upward.
4. **nvidia is a hard ceiling.** If `nvidia/.../nemotron-3-ultra` (max tier) still cannot satisfy the loop, the orchestrator does NOT auto-escalate upward — it sets `STATUS.md` to `blocked-flag-pending-user, reason=max-on-nvidia-failed` and stops. The user either runs it themselves on openrouter/anthropic, or overrides.
5. opencode-Zaen free-tier (provider `opencode`) is treated like nvidia for delegation purposes — rate-limited free, downward-only target, hard ceiling at its own max.

## Provider routing provenance

The `Tier → provider → model` table above is filled from `openrouter.ai/api/v1/models` benchmarks + the local `opencode models` availability probe, on the date stamped in the table. To refresh quarterly (or when a provider adds/removes a model):

```bash
# 1. Re-probe local opencode availability (which providers + coding-capable models are live NOW):
opencode models 2>&1 | awk -F/ '{print $1}' | sort -u
opencode models 2>&1 | grep -E '^<provider>/' | grep -ivE 'safety|rerank|embed|guard|tts|voice|flux|gemma|paligemma|cosmos|bevformer|gliner|whisper|image|translate|drive|streampetr|spargedrive|usd'

# 2. Pull fresh benchmarks + pricing from openrouter for the candidate models:
curl -sS 'https://openrouter.ai/api/v1/models' | python3 -c "
import sys,json
d=json.load(sys.stdin)
want={'deepseek/deepseek-v4-flash','deepseek/deepseek-v4-pro','z-ai/glm-5.2','moonshotai/kimi-k2.6','anthropic/claude-opus-4.8','anthropic/claude-sonnet-5','anthropic/claude-haiku-4.5'}
for m in d.get('data',[]):
  if m['id'] in want:
    b=m.get('benchmarks',{}).get('artificial_analysis') or {}
    p=m.get('pricing',{})
    print(f\"{m['id']:35s} intel={b.get('intelligence_index')} coding={b.get('coding_index')} agentic={b.get('agentic_index')} out=\\$\" + ('{:.2f}'.format(float(p.get('completion','0'))*1e6) if p.get('completion') else '?'))
"
```

Update the `last-reviewed` date in the table after re-running. If availability or ranking changed materially (a provider added a better coding model, a model was retired), bump both the table AND the frontmatter of any pinned executor files that drift from what's actually running — `grep executor .loop/<slug>/*.md` is your post-hoc audit.