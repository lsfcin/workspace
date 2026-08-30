# zcode
> ZCode-side instruments: the hook-protocol probes, and the future home of the adapter if direct registration fails
> fidelity.

The registration itself lives outside this tree, in
[`.zcode/config.json`](../../../.zcode/config.json) — direct spawns of the canonical gates,
mirroring `.claude/settings.json` one-to-one (no adapter, no second copy of a rule). What is
true of it, including the measured trust gate that holds it inert and the open protocol
questions: [`../../../.zcode/CONTEXT.md`](../../../.zcode/CONTEXT.md) and the experiment
[`experiments/zcode-hook-protocol.md`](../../experiments/zcode-hook-protocol.md). The shim
contract every runtime owes: [`SPECS.md`](../SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`probe-deny.sh`](probe-deny.sh) | Exit-2 fidelity probe: block with a PLAIN-TEXT stdout reason, to learn whether ZCode shows a non-JSON block reason to the agent (the canonical core/hooks gates emit plain text on exit 2). Registered only on a matcher for a sacrificial tool. Temporary — see probe.sh. |
| [`probe.sh`](probe.sh) | ZCode hook-protocol probe: dump what a ZCode hook event delivers (stdin payload, filtered env, cwd, ppid) into /tmp/zcode_probe/, so the shim is designed on measured fact rather than documentation. Analysis lands in core/experiments/zcode-hook-protocol.md. Temporary — deleted once the shim replaces it. |
<!-- routing:end -->
