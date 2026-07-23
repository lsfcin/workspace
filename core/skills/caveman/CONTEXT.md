# caveman
> Ultra-compressed communication mode — vendored suite: router skill, mode subfiles, hooks, scripts.

## Attribution

Upstream: **[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)** — the caveman modes,
the commit/review/compress skills, the cavecrew presets, and the activate / mode-tracker / stats /
statusline hooks all originate there. Vendored into this workspace on **2026-07-23** and adapted;
the upstream project keeps the credit for the idea and the original implementation.

## Why it lives here

It was installed globally under `~/.agents/skills/` + `~/.claude/hooks/`, outside version control:
invisible to the second machine, lost on a fresh clone, and unmodifiable without editing untracked
files in `$HOME`. Vendoring it makes the workspace the source of truth — the same rule the rest of
`core/` already follows. `core/tools/sync-global-skills` (re)creates the global symlinks, so setting
up a new computer is one command.

## Layout — this is a folder-shaped skill, not a flat one

`core/tools/sync-skills` mirrors flat `core/skills/*.md` files only, so this directory is **not**
mirrored into `.claude/skills/` — deliberately. The suite is exposed **globally** (every project),
which is how it worked before and what it is for. One registration, no project/user name collision.

| Path | Role |
|------|------|
| `SKILL.md` | the router — argument table, base rules, intensity table, boundaries |
| `modes.md` | worked examples per intensity level; `hooks/activate.js` filters it to the active one |
| `commit.md` · `review.md` · `compress.md` · `cavecrew.md` | independent modes — own output style, base rules do not stack |
| `scripts/` | the `caveman compress` Python package (`python3 -m scripts <file>`) |
| `hooks/` | see below. `ENTRYPOINTS` declares which files get linked into `~/.claude/hooks` |

**`hooks/` layering** — entrypoints on the left, helpers on the right; nothing imports upward:

| Entrypoint | Trigger | Helpers |
|---|---|---|
| `activate.js` | SessionStart | `config.js` |
| `mode-tracker.js` | UserPromptSubmit | `config.js` |
| `stats.js` | run by mode-tracker on `/caveman stats` | `stats-data.js` · `stats-pricing.js` · `stats-format.js` · `config.js` |
| `statusline.sh` | statusLine | — (reads a pre-rendered file) |

`config.js` resolves the default mode and re-exports flag I/O from `flagfile.js`, which sits on
`safepath.js` (symlink-safe path handling). Every hook imports only `./config`.

## Local adaptations (keep this list short — it is the re-sync cost)

1. **Seven skills folded into one.** `caveman-commit/-review/-compress/-help/-stats` and `cavecrew`
   became subfiles here; their frontmatter was stripped (a subfile is not a skill).
2. **Four files split to satisfy the workspace size gate** (≤200 lines), behaviour verified
   unchanged: `config.js` (274) → `config` + `flagfile` + `safepath`; `stats.js` (346) → `stats` +
   `stats-data` + `stats-pricing` + `stats-format`; `compress.py` (254) → `compress` + `prompts` +
   `safety`; `validate.py` (213) → `validate` + `extract`. Two of these removed genuine duplication
   (the symlink-safety block was copied between `safeWriteFlag` and `appendFlag`; the savings math
   was copied across three formatters). Public APIs are re-exported, so importers were untouched.
   **No exemption was taken** — a `.vendor` marker that would have switched the gates off was tried
   and rejected: vendored code complies with our rules like everything else.
3. **`hooks/mode-tracker.js`** — added `/caveman <sub>` dispatch and a legacy map so the old
   per-command spellings still resolve; `crew`/`help` are one-shot and never write the flag.
4. **`hooks/activate.js`** — resolves `SKILL.md` one level up (vendored layout) with the old plugin
   path as fallback; strips the router table + `$ARGUMENTS` from the SessionStart injection; pulls
   the worked examples from `modes.md` so a session loads one level instead of six.
5. **Hook filenames** lost their `caveman-` prefix (`activate.js`, not `caveman-activate.js`) — the
   directory already says caveman. The `$HOME` links keep the prefixed names `settings.json` expects.
6. **`scripts/benchmark.py` glob mode is dead** and was left alone. It resolves
   `parents[3]/tests/caveman-compress`, a path from the upstream repo layout that exists in neither
   the old global install nor here. Explicit-pair mode (`benchmark_pair(orig, comp)`) works. Fix it
   upstream, not locally, or the next re-sync conflicts.

## Commands

`/caveman [lite|full|ultra|wenyan-lite|wenyan|wenyan-ultra]` sets the level; `/caveman commit`,
`review`, `compress <file>`, `crew`, `help`, `stats` reach the subfiles. The pre-fold spellings
(`/caveman-commit`, `/cavecrew`, …) are still mapped by `hooks/mode-tracker.js`.

`stats` never reaches the model: the hook blocks the prompt and returns the numbers directly.

## Wiring

`~/.claude/settings.json` points at `~/.claude/hooks/caveman-*.js|sh`, which are symlinks into
`hooks/` here. Re-create every link with:

```bash
core/tools/sync-global-skills            # link
core/tools/sync-global-skills --check    # verify (exit 1 if stale/broken/missing)
```

Editing anything under `~/.claude/hooks/caveman-*` or `~/.agents/skills/caveman` means editing this
directory — they are links, not copies.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`hooks/`](hooks/CONTEXT.md) | — |
| [`scripts/`](scripts/CONTEXT.md) | Compression CLI behind `/caveman compress <file>` — detect file type, call the m |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SKILL.md`](SKILL.md) | — | — | Ultra-compressed communication mode — router. Cuts token usage ~75% by speaking like a smart caveman while keeping full technical accuracy. Intensity levels: lite, full (default), ultra, wenyan-lite, wenyan-full, wenyan-ultra. Sub-commands: /caveman commit, review, compress, stats, crew, help. Use when the user says "caveman mode", "talk like caveman", "less tokens", "be brief", or invokes /caveman. Also auto-triggers when token efficiency is requested. |
| [`cavecrew.md`](cavecrew.md) | — | — | Cavecrew — Delegating to Caveman Subagents |
| [`commit.md`](commit.md) | — | — | Caveman — Commit Messages |
| [`compress.md`](compress.md) | — | — | Caveman — Compress a Prose File |
| [`modes.md`](modes.md) | — | — | Caveman — intensity levels, worked |
| [`review.md`](review.md) | — | — | Caveman — Code Review Comments |
<!-- routing:end -->
