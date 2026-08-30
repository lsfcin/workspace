# Codex shim
> Adapts Codex lifecycle payloads to the canonical workspace hooks; configuration lives in the project `.codex/` directory.

The canonical policy stays one level up in `core/hooks/`. This directory only translates Codex's
`apply_patch` payload into the `Read` / `Edit` / `Write` contract those gates already use.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`codex-policy.py`](codex-policy.py) | Codex PreToolUse/PostToolUse adapter: derives changed paths from apply_patch and invokes canonical gates. |
<!-- routing:end -->
