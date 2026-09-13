# experiments
> What we measured about this workspace, when, and what changed because of it. One file per question.

**Why this exists.** *"No feature in this workspace has ever been measured"*
([/ROADMAP.md](../../ROADMAP.md)). Every instrument we own —
[`session/context`](../tools/wos/session/context), [`session/usage`](../tools/wos/session/usage),
[`ISSUES.md`](../../ISSUES.md) — prints the present and forgets; git holds the past but not a
readable trend. This directory is the readable half, and differs on purpose from
`core/SCAFFOLD-LOG.md` ([/ROADMAP.md](../../ROADMAP.md) § Rejected): that logged narrated
**changes**, redundant with git; this records **measurements over time**, which git cannot give you.

Per-file format, the rule that keeps a stored number honest, and the reporting discipline:
[`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`SPECS.md`](SPECS.md) | The format every file in this directory follows, and the discipline that keeps a stored number trustworthy. |
| [`caveman-cost.md`](caveman-cost.md) | What does keeping caveman mode on cost per session, and does the compression it buys pay for it? |
| [`confident-wrongness.md`](confident-wrongness.md) | When this workspace has been confidently wrong, what caught it — and how much of that was one of our own checks? |
| [`context-window.md`](context-window.md) | What fills a session's context window, split by source, and how much of it the workspace controls. |
| [`delegation.md`](delegation.md) | How often does this workspace actually spawn a subagent, and which agent definitions get used? |
| [`entropy-scope-vs-rot.md`](entropy-scope-vs-rot.md) | When the entropy count climbs, is the tree drifting or is the check set growing? |
| [`hook-latency.md`](hook-latency.md) | What does the enforcement layer cost per tool call, and how much of that is work nobody asked for? |
| [`output-cost.md`](output-cost.md) | Output tokens are more expensive than input — by how much, and where are ours? |
| [`read-amplification.md`](read-amplification.md) | Do our own gates make a session read the same file more than once — and what does that cost? |
| [`subagent-context-chain.md`](subagent-context-chain.md) | Does forcing an agent to read a subtree's CONTEXT.md chain change what it does — and should a subagent be forced at all? |
| [`zcode-hook-protocol.md`](zcode-hook-protocol.md) | Will ZCode execute this workspace's hook registration in `.zcode/config.json`, and what does a fired hook actually receive? |
<!-- routing:end -->
