# delegate
> Hand a task to another vendor's model through one contract, read-only for now. Leaf: `ask` (answer mode, an outside verdict included); the chain it walks is `core/workers.txt`.

`core/run tools/delegate/ask --out outputs/<topic>-panel.md prompt.md`. The calls and their traps: [`../../agents/SPECS.md`](../../agents/SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`ask`](ask) | ask an outside panel (another vendor's model), falling to the next model when one gives no verdict |
<!-- routing:end -->
