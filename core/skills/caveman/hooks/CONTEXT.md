# hooks
> Claude Code lifecycle hooks for the caveman suite — activation, mode tracking, stats, statusline.

These are **standalone scripts run by node/bash**, not an importable module: `~/.claude/settings.json`
names four of them by absolute path (through the symlinks `core/tools/sync-global-skills` creates).
That is why there is no facade here — nothing outside this directory imports it.

[`ENTRYPOINTS`](ENTRYPOINTS) declares which files get linked into `~/.claude/hooks`. Add a helper
module and it stays internal; add an entrypoint and it must be listed there **and** wired in
`settings.json`.

| File | Role |
|------|------|
| `activate.js` | SessionStart — writes the flag, injects the ruleset filtered to the active level |
| `mode-tracker.js` | UserPromptSubmit — parses `/caveman …`, updates the flag, re-injects the reminder |
| `stats.js` | CLI, run by mode-tracker on `/caveman stats`; splits into `stats-data` / `stats-pricing` / `stats-format` |
| `statusline.sh` | statusLine — renders the badge from a pre-rendered suffix file |
| `config.js` | default-mode resolution + the flag API every hook imports |
| `flagfile.js` · `safepath.js` | flag/history I/O and the symlink-safe path handling under it |

Read [`../CONTEXT.md`](../CONTEXT.md) for attribution and the list of local adaptations.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`activate.js`](activate.js) | [`activate.d.ts`](activate.d.ts) | — | caveman — Claude Code SessionStart activation hook |
| [`config.js`](config.js) | [`config.d.ts`](config.d.ts) | `getConfigDir`, `getConfigPath`, `getDefaultMode`, `readFlag` | caveman — shared configuration resolver, and the façade the hooks import |
| [`flagfile.js`](flagfile.js) | [`flagfile.d.ts`](flagfile.d.ts) | `safeWriteFlag`, `readFlag`, `appendFlag`, `readHistory` | caveman — reads and writes of the mode flag and the lifetime history log |
| [`mode-tracker.js`](mode-tracker.js) | [`mode-tracker.d.ts`](mode-tracker.d.ts) | — | caveman — UserPromptSubmit hook to track which caveman mode is active |
| [`safepath.js`](safepath.js) | [`safepath.d.ts`](safepath.d.ts) | `debugLog`, `resolveSafeDir`, `isWritableTarget`, `prepareTarget`, `withFd` | caveman — symlink-safe path resolution shared by every flag-file writer |
| [`stats-data.js`](stats-data.js) | [`stats-data.d.ts`](stats-data.d.ts) | `findRecentSession`, `parseSession`, `findCompressedPairs`, `summarizeCompressed`, `aggregateHistory` | caveman — collection: read session transcripts, the history log, and compressed |
| [`stats-format.js`](stats-format.js) | [`stats-format.d.ts`](stats-format.d.ts) | `formatHistory`, `formatShare`, `savingsBlock`, `formatStats` | caveman — rendering: turn collected numbers into the three printed views. |
| [`stats-pricing.js`](stats-pricing.js) | [`stats-pricing.d.ts`](stats-pricing.d.ts) | `priceForModel`, `formatUsd`, `deriveSavings`, `parseDuration`, `humanizeTokens` | caveman — savings math: compression ratios, model pricing, derived estimates |
| [`stats.js`](stats.js) | [`stats.d.ts`](stats.d.ts) | `reportLifetime`, `recordSnapshot`, `main` | caveman stats — read the active Claude Code session log, print real token usage |
<!-- routing:end -->
