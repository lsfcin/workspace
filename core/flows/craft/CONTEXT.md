# Craft Flows
> The engineering cluster owned by the `loops` skill — build work in file-relayed loops. Invoked as `/loops`.

**Vocabulary.** "Flow" is the canonical word for a procedure that connects agents (decided
2026-07-23, [`core/SCHEMA.md`](../../SCHEMA.md) § Composition and cycles). "Loop" survives here only
in its literal sense — one bounded repeat, i.e. a single numbered step of `craft.md` run in a fresh
session. The files were `loop-engineering` · `loop-router` · `loop-architecture` · `LOOP-TREE`.

| File | Role | Loaded |
|------|------|--------|
| [`TREE.md`](TREE.md) | the map — which subtree a task goes to, and why each is its own shape | once, when choosing a subtree |
| [`route.md`](route.md) | the trunk: classify a `/loops` task by type, hand off. Does no work itself | every run, orchestrator |
| [`craft.md`](craft.md) | the build flow: padaria shortcut + the contract-first feature spine | every loop |
| [`architect.md`](architect.md) | design/technology decisions → a recorded ADR, not code | architecture subtree only |
| [`routing.md`](routing.md) | tier → concrete model per provider; availability probe; delegation direction | once per chain, orchestrator only |
| [`runtimes.md`](runtimes.md) | spawn recipes per runtime (`opencode run`, Claude Code `Agent`, …) | once, and only your runtime's section |
| [`prior-art.md`](prior-art.md) | lineage (Reflexion/LATM/Voyager), research provenance, one worked case study | never, to run — only to change or defend the flow |

**Stratified by access pattern, not chopped up.** `craft.md` was one ~52 KB file mixing the
always-loaded protocol with tables and history each loop paid for eight times. The split follows
what is actually read when: always-needed stays in one file; per-chain and never-needed become
subfiles. This is deliberately *not* blind fragmentation — the whole spine (Core Principle, Carry,
Autorouting, Return Flags, Loops 0–6.5, Cost Gate, Field Practice) is still one file, because a
loop executor needs all of it.

Entry point is always the `loops` skill ([`core/skills/loops.md`](../../skills/loops.md)), never a
file here directly — the skill loads the shared discipline first.

**Schema status.** This cluster declares its own tier routing and is **exempt** from flow-layer
validation (`sync-skills validate_flows` skips `flows/craft/`). That exemption is a known
asymmetry — `engineering` is not in the `type` enum — and is queued in
[`core/ROADMAP.md`](../../ROADMAP.md). The `uses:` DAG check does **not** exempt it: every flow
file is a node in that graph.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`TREE.md`](TREE.md) | — | — | The Craft Tree |
| [`architect.md`](architect.md) | — | — | Architecture-decision subtree of the craft tree — turn a design/technology choice into a recorded decision (problem → options → trade-offs → decision → ADR). Produces a durable decision record, not code. |
| [`craft.md`](craft.md) | — | — | Looped engineering flow — development in file-relayed loops with model autorouting; each loop runs in a fresh, cheap session that reads exactly one file. |
| [`prior-art.md`](prior-art.md) | — | — | Craft — Prior Art, Provenance, and Case Study |
| [`route.md`](route.md) | — | — | Loop router — classify a /loops task by TYPE and dispatch to the right subtree flow (padaria · feature/SDD · research · architecture). Thin: it classifies and hands off, it does not do the work. |
| [`routing.md`](routing.md) | — | — | Craft — Provider Routing |
| [`runtimes.md`](runtimes.md) | — | — | Craft — Runtime Spawn Recipes |
<!-- routing:end -->
