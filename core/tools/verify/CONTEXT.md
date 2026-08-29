# verify
> Verification contract + patterns for all code projects: tiers T0-T3, script names, dump-oracle rules. Reference
> implementation: code/isoroll-module/test/.

`verify:fast` (T0+T1, every commit) and `verify:full` (T2+T3, pre-merge/on demand/`/roundup`) are
the two scripts every `code/` project declares. The pre-commit gate blocks a missing or red
`verify:fast` and names the fix when it fires.

## Tier ladder

- **T0 static** — compiler + linter.
- **T1 unit** — vitest/pytest + property tests (fast-check/hypothesis) over pure or cheaply
  fakeable modules. Mocking the host framework (Foundry/PIXI/Android) tests the mock, not the
  app — that work belongs at T2.
- **T2 functional** — the real app headless (Playwright etc.), committed fixtures, assertions
  on structured state dumps.
- **T3 visual** — deterministic screenshots vs committed goldens (pixelmatch). Failure
  artifacts (actual+diff PNGs) in a gitignored output dir — agents read them directly.

## Dump-oracle rules

1. The app exposes a machine-readable state dump (JSON) for the subsystem under test.
2. The dump calls the same live-path functions as rendering/logic. A diagnostic with its own
   math is a second implementation that can lie.
3. Oracles assert on the dump; pixels are T3's job.
4. Every visually-confirmed bug exports its scene/state as a committed fixture.
5. Regression specs are named `b<N>-*.spec.*`. Open bugs carry `xfail` specs; XPASS means the
   bug died — promote.

## Reference implementation

`code/isoroll-module/test/` — `unit/` (T1, vitest+fast-check) and `e2e/` (T2, Playwright vs live
Foundry) are the working shapes to copy; its own `CONTEXT.md` lays out the runner and the rules
as this project applies them.

## How a repo declares it

[`contract.py`](contract.py) is the one definition of *what counts as declared* and *how to run it*:
a root `verify.py`, an npm `verify:<level>` script, or a `Makefile` target, in that order. Two
consumers now share it — the pre-commit gate and `core/tools/wos/roundup` — which is the second
consumer this section used to be waiting for.

**`verify.py` leads because it is the only form that can ask which interpreter to use.** The other
two name a program that must already be installed and already spelled right for this machine: the
workspace declared `make verify-fast`, the gate discovered it, and on a machine without `make`
nothing ran while the gate stayed green.

<!-- routing:start -->
## Routing

| File | API | Description |
|------|-----|-------------|
| [`contract.py`](contract.py) | `discover`, `run` | How a repo declares its verification, and how to run what it declared. One definition. |
<!-- routing:end -->
