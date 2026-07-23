---
name: loops
description: >
  Run the craft flow: develop a feature in file-relayed loops with model autorouting
  (clarify → plan → ground → architecture → TDD → code → user test → ship).
  Invoke with /loops [task or feature request].
---

# /loops

Arguments: $ARGUMENTS

---

## Protocol

0. **Route first (the craft tree).** `/loops` is a tree, not one pipeline. Read [`core/flows/craft/route.md`](../flows/route.md) and classify the task into a subtree — `padaria` · `feature` · `research` · `architecture` (map + rationale: [`core/flows/craft/TREE.md`](../flows/TREE.md)). Record `subtree:` in the Carry block / STATUS. Then run that subtree's flow:
   - `feature` / `padaria` → the craft flow below (feature is contract-first: Step 0 permission panel → Loop 3.5 Contract Layout → Loop 3 concept-symmetry review → TDD → ship).
   - `research` → the matching `core/flows/research/{sota,literature,explore,compare,recipe,replicate,review,summarize,watch,audit}.md` or `core/flows/mechanism-search.md`.
   - `architecture` → [`core/flows/craft/architect.md`](../flows/architect.md) (emits an ADR; chain into `feature` if it needs building).

   The steps below are the **feature/padaria** subtree. For research/architecture, hand off and stop.

1. **Resolve provider before Loop 0 (fastest identification):**
   ```bash
   opencode models 2>&1 | awk -F/ '{print $1}' | sort -u          # configured providers
   echo "active: ${OPENCODE_MODEL:-?}"                            # orchestrator's own model (provider prefix = chain provider)
   rtk grep -E '"model":\s*"[^/]+' ~/.config/opencode/opencode.json[c]? opencode.json[c]? 2>/dev/null   # fallback
   ```
   Select the active provider's tier-map row from `core/flows/craft/craft.md` § `Tier → provider → model mapping` (or, if the runtime is Claude Code/Copilot CLI, the anthropic/copilot row). If you plan **downward delegation** (e.g. orchestrator on openrouter → all loops on nvidia free), pick the tier-map row of the *delegate* provider and record `chain-deleg: deleg=<from>→<to>` in the Carry block. Fill the Carry `provider:` / `tier-map:` / `chain-deleg:` fields at Loop 0 — a chain without them is undefined.

2. Read `core/flows/craft/craft.md` in full (sections: Core Principle, Autorouting, `Tier → provider → model mapping`, `Provider delegation`, Return Flags, Orchestration, Runtime portability, Provider routing provenance, Loop 0..6).
3. Execute it with the task: $ARGUMENTS. This session is the orchestrator. You hold only verdict lines and the chain's provider+map — never paste loop file contents here.
4. Spawn each loop as a subagent per the flow's Orchestration section — pinned agent types `craft-low` / `craft-medium` / `craft-high`; pass the per-loop model from the resolved tier-map (or rely on the frontmatter default). The executor's self-report tag is `executor: loop-<tier> model=<provider/model-id> tier=<tier> deleg=<none|from→to>` — that is your per-loop cost/routing audit (`grep executor <project>/.loop/<slug>/*.md`).
5. Tier `max` is never auto-spawned: pause and tell the user (max-tier quota is scarce and, on nvidia, a hard ceiling — `Provider delegation` rule 4 may surface the cost delta or stop the chain).
6. Hold only verdict lines in this session. Never paste loop file contents here.

## Why this is provider-aware (one-liner for the next reader)

Each configured provider has its own coding-capable model list (`opencode models` probe); the `Tier → provider → model` table fills tiers **from availability first, benchmarks second, cost third**. A chain stays inside one provider by default; downward delegation (openrouter→anthropic→copilot→nvidia) is cost-saving and encouraged; upward cross-provider promotion requires your explicit consent every time. nvidia's max is a hard ceiling — nvidia cannot silently pull Kimi or Opus.

## Prior art & lineage

This flow is a production realization of Reflexion (Shinn 2023, <https://arxiv.org/abs/2303.11366> — verbal-reflection memory → durable append-only loop files), **LATM** (Cai 2023, <https://arxiv.org/abs/2305.17126> — two-tier tool-maker/tool-user cost-spreading → the Autorouting table), and **Voyager** (Wang 2023, <https://arxiv.org/abs/2305.16291> — iterative environment-feedback prompting + skill library → the Loop 5 user-test and Loop 6.5 Skill Extraction). Full citations and the explicit override-mapping vs. the Autorouting table live in `core/flows/craft/craft.md` (`## Prior Art` and `## Field Practice`).
