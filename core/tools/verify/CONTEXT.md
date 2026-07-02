# verify
> Verification contract + patterns for all code projects: tiers T0-T3, script names, dump-oracle rules. Reference implementation: code/isoroll-module/test/.

## Contract (any code project)

| Script | Tier | Content | When it runs |
|--------|------|---------|--------------|
| `verify:fast` | T0+T1 | static checks + unit/property tests, seconds | every commit — enforced by global pre-commit (blocks red) |
| `verify:full` | T2+T3 | headless functional + visual goldens | pre-merge, on demand, `/handoff` |

Declare both in `package.json` scripts (TS) or Makefile targets (other stacks). The
pre-commit gate discovers `verify:fast` by convention — no per-project wiring.

## Tier ladder

- **T0 static** — compiler + linter.
- **T1 unit** — vitest/pytest + property tests (fast-check/hypothesis) over pure or cheaply
  fakeable modules. Do NOT unit-mock the host framework (Foundry/PIXI/Android) — that tests
  the mocks. Anything host-coupled goes to T2.
- **T2 functional** — the real app headless (Playwright etc.), committed fixtures, assertions
  on structured state dumps.
- **T3 visual** — deterministic screenshots vs committed goldens (pixelmatch). Failure
  artifacts (actual+diff PNGs) in a gitignored output dir — agents read them directly.

## Dump-oracle rules

1. The app exposes a machine-readable state dump (JSON) for the subsystem under test.
2. The dump calls the same live-path functions as rendering/logic — never re-derives.
   A diagnostic with its own math is a second implementation that can lie.
3. Oracles assert on the dump, never on pixels (pixels are T3's job).
4. Every visually-confirmed bug exports its scene/state as a committed fixture.
5. Regression specs are named `b<N>-*.spec.*`; KNOWN-BUGS.md FIXED flips are hook-gated
   on their existence. Open bugs carry `xfail` specs; XPASS means the bug died — promote.

## Reference implementation

`code/isoroll-module/`: `test/unit/` (vitest+fast-check, stubs in setup.ts),
`test/e2e/` (Playwright vs live Foundry: helpers.mjs login/fixtures/oracles, run.mjs
XFAIL runner, golden.mjs pixelmatch layer). Copy and adapt; extract shared code here
only when a second consumer exists (planned: apptime, VERIFY.md A1).

<!-- routing:start -->
## Routing

<!-- routing:end -->
