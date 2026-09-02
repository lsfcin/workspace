# Hooks — Specs
> What must be true of the enforcement layer, and why: what each gate blocks, what the hooks write,
> and the contract a new agent's shim must satisfy.

Companion to [`CONTEXT.md`](CONTEXT.md), which says what this directory *is* and routes into it.
Installing the toolchain these gates depend on: [`SETUP.md`](../../SETUP.md).

## The law lives in file_law.py / schema_law.py / limits.env, never in a checker

A checker that restates any of these is the drift the checkers exist to catch, and it has bitten
three times. **The dangerous shape never looks like drift: a tool that knows it is overriding the
law has found a gap in the law, not a special case of its own.** The tell is a checker whose
docstring explains why it disagrees with what it just asked — `core/tools/wos/wrap` carried exactly
that for YAML frontmatter, honest and documented and still wrong, because the law kept flagging
lines the tool refused to touch and each file read correctly alone.

## What a working install looks like

Behavioural assertions — what the gates promise, and the list a new shim is tested against. The
commands that check the toolchain itself are in [`SETUP.md`](../../SETUP.md) § Verification.

- edit a `.py` / `.js` / `.ts` / `.dart` file → its interface regenerates immediately
- edit a `.tex` file → `.texif` **and** `labels.md` regenerate; a `.bib` edit warns about bib keys
  with no `reviews/<key>.yaml`
- read a source file whose interface is current → blocked, interface first
- grow a code file past 200 lines → the edit is blocked
- create a new file with no first-line comment → the Write is blocked
- edit a file already missing that comment → a reminder prints, the edit stands
- commit a new file the routing table could not describe → the commit is rejected
- commit a 200+ line code file → the commit is rejected
- commit any staged code file → its `CONTEXT.md` routing block is updated and staged

## Git pre-commit (`pre-commit`)

Applied globally via `core.hooksPath`, so it fires on every `git commit` in **every** repo under this
workspace.

- Warns on code files ≥ 150 lines, blocks ≥ 200. Thresholds in [`limits.env`](limits.env); which
  extensions count is [`file_law.py`](file_law.py)'s answer, never a checker's.
- Warns when a newly staged code file lacks its first-line description comment.
- Hard-blocks cross-module imports that bypass the facade, via `facade/check-facade-imports.py`.
- Auto-syncs the `CONTEXT.md` routing block for every directory with staged files, and stages it.
- Auto-generates and stages `.pyi` (stubgen), `.d.ts` (tsc), `.dart.api`.
- Runs `checks/line_counts.py` over staged files — the same module that runs standalone for a
  workspace-wide audit.
- `verify:fast` contract: a project declaring that script must be green, or the commit is blocked.
- `checks/check-duplication.py`: jscpd over the committing repo, blocking clones that involve staged
  files (75 tokens / 10 lines).
- Spec-driven module gate: a new `CONTEXT.md` under `code/` must declare `> spec: <file>` or
  `> spec: none`. Ratchet — existing modules are grandfathered.
- `checks/type-gate.py`: a staged `.md` must be a known type or a well-shaped instance, sitting where
  its type is allowed. Ratchet — only what a commit **adds**. Law parsed from
  [`../SCHEMA.md`](../SCHEMA.md), never restated.
- `checks/citation-gate.py`: a roadmap item number (`Front 4.1`, and the bare `Front 9`) may not
  appear outside `ROADMAP.md` / `ROADMAP-<slug>.md`. **Not a ratchet** — the corpus was swept to zero
  on 2026-08-16. Completion is deletion here, so a cited number becomes a pointer to nothing the day
  the item lands; point at the `SPECS.md` / `SCHEMA.md` section that owns the rule instead. The gate
  also owns the `Frente`→`Front` rename by matching the citation *shape* rather than the word,
  because `frente` is ordinary Portuguese and a bare-word retired token fired on honest prose.
- `git/gitignore-self-heal.sh`: a new domain subdirectory carrying a `CONTEXT.md` gets its
  `!<domain>/<dir>/` allow line written automatically, and **it then stops the commit** if that
  directory holds files git could not see — staging happened before this hook ran, so the commit
  would ship a `CONTEXT.md` without the content it describes. It heals, names the directory, and asks
  for one `git add` and a re-run. Ruled 2026-08-19 (Lucas), against the hook staging the files
  itself: **a commit hook that stages what the caller did not is worse than the bug it fixes.**

### Branch drift

**HEAD is shared mutable state between parallel sessions.** A parallel session switches the shared
checkout mid-flight and your commit lands on *their* branch, auto-pushed there. **The branch reads
correct at session start**, which is why no start-of-session check can catch it.

[`git/branch-marker.sh`](git/branch-marker.sh) records the branch at `SessionStart` and the
pre-commit path warns when HEAD no longer matches. Three properties carry the design: **warn, never
block**, because a deliberate mid-session switch is legitimate; **warn once per divergence**, since a
warning that repeats after being understood is one people learn to skip; and **one marker per repo,
not per session**, because `check` runs inside a git hook with no session id to pair with — a repo
with no marker is silent, so nested repos and non-agent commits are unaffected.

Recovery is non-destructive and the warning prints it: confirm a fast-forward with
`git merge-base --is-ancestor <your-branch> HEAD`, then `git branch -f <your-branch> HEAD` and push
**yours**. Never reset or force-push theirs, and never `git checkout` your branch back — that yanks
HEAD out from under them, the same defect pointed the other way. One worktree per session removes the
shared HEAD entirely and is the better end state, but every session must adopt it before it protects
anything, and a checked-out worktree makes `git branch -d` refuse. Ruled 2026-08-14 (Lucas): the
warning now, worktrees as a later opt-in.

**No exemptions for vendored third-party code.** Anything brought into the workspace complies with
the same gates as our own. A `.vendor` marker that switched them off was rejected (2026-07-23, Lucas:
*"even thirdparty solutions, once brought to our w-os should comply with our rules. opening
exceptions is quite dangerous"*). Vendoring means adopting and adapting: split what is too big, and
record the deviations so a future re-sync knows what it is merging against.

## A marker is asked about, never string-matched across the shell/Python boundary

**Whichever side WRITES a session marker answers questions about it.** A gate that records a path
in one hook and reads it in the next must not compare that path as text from the other language:
Python's `Path.resolve()` yields `C:\Users\…`, a hook payload arrives as `c:\Users\…`, and
`readlink -f` between them gives `c:/Users/…`. Three spellings of one file, and `grep -qxF` matches
none — so the gate blocks every read while the message promises that reading the interface unlocks
it. **A gate that can only block is the mirror of one that can only pass**, and both read as
working.

The CONTEXT.md chain gate never had this defect because both of its ends are Python calling the
same normalisation. So the rule is not "spell the path more carefully"; it is that **the module
owning the marker owns the comparison** — `hook_input` holds both stores and every reader asks it.
The shell caller had to be handed a query CLI arm to reach that answer; porting it (2026-09-02)
deleted the arm and the question with it, which is the difference between working around a seam and
removing one.

## Agent lifecycle gates

Bound from `.claude/settings.json`, and by the equivalent registration in each other provider's
shim. Every one of them spawns through [`../run`](../run), which is the shim contract in one line:

```
sh ${CLAUDE_PROJECT_DIR}/core/run <path-relative-to-core/> [args]
```

The path is relative to `core/`, not to this directory, since 2026-08-29: the launcher moved up so
a tool could be spawned the same way a gate is — `core/run tools/video/video`. See
[`core/tools/SPECS.md`](../tools/SPECS.md) § The interpreter for what that replaced.

**A shim carries no machine-specific string, and that is the whole reason `run` exists.** The
harness expands `${CLAUDE_PROJECT_DIR}`, and `run` picks whichever venv layout is present —
`.venv/Scripts/python.exe` by asking the filesystem which is there — so a shim is versioned verbatim
and no install step rewrites it. It is also the only file besides `platform_law.py` allowed to know
both venv layouts, and `test_corpus_ratchet.py` exempts it by name for that reason.

`run --python` **prints** that interpreter instead of running anything, and it exists so the
exemption stays an exemption. A shell script that must spawn Python *inline* — a `-c` one-liner, a
heredoc — cannot pass through the arm above and otherwise spells a venv path itself, which is how
the bare word `python3` reached fourteen shell sites. Every one of them swallowed the Store alias's
advert with `2>/dev/null` or `|| exit 0`, so `post-edit.sh` and its four stages, the interface-first
read gate and `precompact-wipe.py` had **never run** on a Windows clone while reading as green.
That gate is Python now and cannot spell the word at all, which is the shape of the real fix and the
reason the port was worth doing rather than the spelling being corrected in place. Held at zero by
`test_no_shell_hook_spawns_the_bare_word_python3`, which is a floor and not a ceiling because a
hook that can only ever pass is indistinguishable from one that works.
`run` also exports `PYTHONIOENCODING=utf-8`, because every gate prints ⛔ ✓ ⚠ and a Python encoding
stdout as the console codepage dies *inside its own message*, showing a traceback where a verdict
belonged.

**Why the bare word `python3` is banned here.** On Windows it reaches a Microsoft Store execution
alias that prints an advert and exits 9009: the gate never runs, and the caller reads the advert as
the gate's own output. Every hook in this workspace was spelled that way until 2026-08-28, so on a
Windows clone the enforcement layer had never once fired while both configs read as correct. The
paths a shim names are checked by `test_shim_paths.py`, which now reads `.claude/settings.json` too
— it did not until that day, which is precisely how twenty dead commands survived in the one file
the test existed to guard.

| Script | Trigger | Behaviour |
|--------|---------|-----------|
| `checks/pre-edit.py` | PreToolUse: Edit, Write | **Blocks** an edit pushing a code file past 200 lines; **blocks** Write of a new file with no first-line description comment |
| `facade/facade-scan.py` | PreToolUse: Write (new files in `code/`) | **Informs** — prints the exports the target module's facade already declares, warns if that list is empty |
| `facade/facade-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Blocks** edits to a `code/` module file until the nearest facade was Read this session |
| `facade/facade-tracker.py` | PostToolUse: Read | Records facade reads, consumed by `facade-gate.py` |
| `read/context-gate.py` | PreToolUse: Read, Edit, Write, Grep, NotebookEdit | **Blocks** file access until the target subtree's `CONTEXT.md` chain was Read this session; on a Read the message also names the current stub, so one batch clears both read gates. Session-deduped; `CONTEXT.md`/`AGENTS.md` targets exempt |
| `read/bash-context-gate.py` | PreToolUse: Bash | **Blocks** Bash commands naming workspace files in subtrees whose chain is unread — this is what closes the `cat`/`grep` bypass |
| `checks/heredoc-gate.py` | PreToolUse: Bash | **Warns, never blocks** — a heredoc writing a workspace file (`cat >`/`tee`) meets none of the `Edit\|Write` gates. Silent for stdin-to-an-interpreter, which writes nothing |
| `compact/bash-compact-rewrite.py` | PreToolUse: Bash | **Rewrites, never blocks** — sends every line of a multi-line command through rtk, which parses line 1 only; delegates any payload it cannot split safely |
| `read/pre-read.py` | PreToolUse: Read | **Blocks** reading a source file while its interface is current, naming the unread `CONTEXT.md` chain alongside it — both read gates exit 2 on one Read and the harness reports only the first, so each names the whole set; warns when the interface is stale. Reading the interface unlocks the source for the session |
| `read/context-tracker.py` | PostToolUse: Read | Records `CONTEXT.md` reads and interface reads — the state both gates above consume |
| `read/spec-read-gate.py` | PreToolUse: Edit, Write (`code/` files) | **Blocks** editing a spec-locked module (`CONTEXT.md` `> spec:` + `SPECS.md` `status: locked`) until its `SPECS.md` was Read this session; nudges on new files in spec-less `code/` modules |
| `read/agent-context.py` | PreToolUse: Agent, SubagentStart | **Induces, never blocks** — hands a spawned worker the `>` line of each subtree its prompt names |
| `checks/issues-gate.py` | PreToolUse: Edit, Write (`ISSUES.md`) | **Blocks** flipping a bug to FIXED without a matching `test/**/b<N>-*` regression spec |
| `post-edit.sh` | PostToolUse: Edit, Write | Regenerates interfaces, scaffolds `jsconfig.json`/`tsconfig.json` if missing, reminds about a missing first-line comment, runs the routing sync |
| `session/precompact-wipe.py` | PreCompact | Wipes the seen-markers, so the `CONTEXT.md` chain is re-read after compaction |
| `session/session-prune.py` | SessionStart | Prunes session marker files older than 2 days |
| `session/mirror-heal.py` | SessionStart | **Heals, and reports** — regenerates the skill mirrors a `git pull` brought sources for but no copies of (one line, only when it acted); **warns without writing** when a harness permission config no longer matches `core/profile.txt`, because a level arriving over the network is Lucas's call |

**Why one of them only warns.** A `PreToolUse` hook fires *after* the model has emitted the tool call,
so by the time `heredoc-gate.py` sees a 3,000-character `cat >` payload those tokens are already
billed and already in the thread. Blocking cannot recover them — it makes the turn emit the same
content again as a `Write`. So the gate exists to change turn N+1. **Any gate whose subject is what
was already sent has this shape; a gate whose subject is what is about to happen on disk should still
block.**

**How a hook warns without blocking**, and two harness facts verified by running it (Claude Code
2.1.218, neither documented):

- `PreToolUse` delivers `hookSpecificOutput.additionalContext` **to the model**, on exit 0, with the
  tool still running. That is the only non-blocking channel that reaches the model — exit-0 stdout is
  transcript-only and `systemMessage` addresses Lucas, not the agent. **Every "Informs" hook uses
  it**, asserted by `test_an_informing_hook_speaks_on_the_channel_that_reaches_the_model`.
- **A `.claude/settings.json` hook edit is live in the session that made it.** Registration is not
  captured at session start.

Why a subagent is exempt from the context gate, and why the briefing needs two events:
[`../SPECS.md`](../SPECS.md) § AD-13.

## Generated artifacts

### Interface files

Every save of a supported source file produces its interface unconditionally — universal, no
per-project config.

| Language | Output | Tool | Notes |
|----------|--------|------|-------|
| Python | `.pyi` | `stubgen` | on every edit and every commit |
| JavaScript | `.d.ts` | `tsc --allowJs --emitDeclarationOnly` | `jsconfig.json` auto-scaffolded if missing (IDE use only) |
| TypeScript | `.d.ts` | `tsc --emitDeclarationOnly` | `tsconfig.json` auto-scaffolded if no ancestor config is found |
| Dart | `.dart.api` | `stubgen/dart-api-extract.py` | public class/mixin/method signatures; needs Python 3 only, no Dart SDK |
| LaTeX | `.texif` | `stubgen/tex-interface-gen.py` | structure, full equations, floats, citations, TODOs, section opening sentences. Also regenerates `labels.md`; a `.bib` edit warns about missing `reviews/<key>.yaml` |

**To bypass the size gate temporarily**, edit `BLOCK_LINES` in [`limits.env`](limits.env), do the
operation, revert. Both `checks/pre-edit.py` and `checks/line_counts.py` read it immediately.

### A file a tool writes is not a file anyone authored

A file is **authored** — every size, shape and first-line rule applies — or **vendored** and exempt
because upstream chose its layout, or **generated**, which is neither and needed its own answer.

[`generated.txt`](generated.txt) declares what our tools write, on the same contract as its sibling
— a **named, reviewed glob list, never a heuristic**, each entry naming its generator — and
`file_law.is_authored()` is the one question every size and shape gate asks. **Why the exemption is
safe here and not in general:** the artifact has a test that its generator reproduces it byte for
byte (`--check`). An entry without that property is a hand-edited file wearing a generated file's
coat.

### The `CONTEXT.md` routing block

`routing/context_synchronizer.py` runs on every edit (via `post-edit.sh`, which also re-syncs the
parent directory) and every commit, keeping each directory's `## Routing` block true unmaintained:

- **adds** a new file, taking its description from the first source that answers: the first-line
  comment (code, below any shebang), a module docstring's first line (`.py`), `description:`
  frontmatter then the line-2 `> ` blurb (`.md`), or the ` — ` usage comment (extensionless scripts)
- **removes** entries for deleted files, and **links** interfaces to their source
- **folds** a leaf directory under `WARN_FILES` into the parent block; **links** one at or above it,
  or one that carries its own `CONTEXT.md`
- **warns** when a directory exceeds `WARN_FILES` direct files

**Never edit inside the `<!-- routing:start/end -->` sentinels** — the next sync overwrites it.
**Renames are not tracked**: the old entry disappears and the new file arrives with a placeholder.

**Hoisted text is bounded and rebased; authored text is not.** A `.md` blurb and a subdirectory blurb
were written to sit under their own heading, so [`routing/hoist.py`](routing/hoist.py) rebases their
links and cuts them at `DESC_LIMIT`. A code file's first-line comment goes in untouched: it was
authored as this table's one-liner.

### First-line descriptions

Every scanned file begins with a one-line description, because `context_synchronizer.py` reads it as
the canonical description. Enforced at **Write** (`pre-edit.py` blocks), at **Edit** (a reminder
prints, the edit stands), and at **commit** — `entropy_context.check_description`, run by
`checks/type-gate.py` over the files the commit adds.

**The commit gate is the load-bearing one.** `pre-edit.py` only fires under
`if not os.path.exists(file_path)`, so it covers creation through Edit/Write and nothing else: a file
written by a generator, a shell heredoc, `git checkout`, or an agent not running our hooks is never
asked. **An edit-time check only covers the harness path; the staged set is what covers everyone.**

**The check asks the generator, never its own pattern table.** `check_description` calls
`workspace_meta.file_description()` — the same call whose empty return makes the generator write the
placeholder — and `workspace_scanner.is_scanned()` to decide who is asked, so the gate's scope and the
table's scope are one definition. **A marker is not evidence of a discipline problem until the
generator has been asked whether it can answer it**: check the extension's entry in
`routing/workspace_meta.py` before writing any description by hand, because a hand sweep gets
re-filled.

**A file that cannot carry a comment gets its description written into the table instead.**
`parse_preserved_files` keeps any non-placeholder description across a re-sync, so the row is the
place to answer for a file whose *content is data a parser reads*. Found 2026-08-20 on seven DSL
fixtures, where **adding the comment is not merely useless but destructive**: the parse test passed
with a `#` first line while the round-trip test went red, because the parser silently drops the line.
That parse-only green is exactly the silent pass [`core/SPECS.md`](../SPECS.md) § Conventions warns
about.

### Finished-work prose is blocked on what a commit adds

`entropy/entropy_ledger.py` carries the detector — strikethrough, a dated completion report, a
settled-marker, and a ticked item inside a ledger — and `checks/type-gate.py` calls it on
`staged_added_files()`. So a file **arriving** with a corpse in it is rejected, while the inherited
queue stays the dashboard's and rides the ceiling in `test_corpus_ratchet.py`. That split is the rule
for every Tier 0 check here: **a gate that fails on the day it lands trains its reader to ignore it.**
Completion is deletion (`core/SCHEMA.md` § No archive types), and [`core/SPECS.md`](../SPECS.md) §
AD-15 makes blocking — not the mere existence of a detector — what licenses deleting the prose.

## Canonical behaviour, provider shims

Canonical behaviour lives in neutral files under `core/hooks/` and [`AGENTS.md`](../../AGENTS.md).
Provider-specific files are shims, discovery points, or startup wiring — never a second copy of a
rule. Three words classify any of them: **ENFORCED**, the hook can block a read, an edit or a commit;
**INDUCED**, the file only injects guidance and the agent may ignore it; **SKIPPED**, present for
compatibility with no enforcement effect.

| File | Why it exists | Behaviour |
|------|---------------|-----------|
| `AGENTS.md` | canonical workspace policy + startup anchor for every agent | **INDUCED** |
| `.github/copilot-instructions.md` | one-line Copilot shim pointing to `AGENTS.md` | **INDUCED** |
| `.github/hooks/workspace-policy.json` | VS Code hook registration for Copilot lifecycle events | **ENFORCED** |
| `.vscode/settings.json` | limits hook discovery to the workspace path, not user-level `.claude` hooks | **INDUCED** |
| `opencode.json` | opencode config: the `AGENTS.md` instructions anchor + skill discovery paths | **INDUCED** |
| `.opencode/plugins/workspace-policy.js` | opencode hook registration — the plugin translating `tool.execute.*` and `experimental.session.compacting` to the canonical gates | **ENFORCED** |
| `.opencode/skills/` | opencode discovery point for the skill library, generated by `sync-skills` | **INDUCED** |
| `.zcode/config.json` | ZCode hook registration — direct spawns of the canonical scripts, no adapter | **ENFORCED*** |
| `.zcode/skills/` | ZCode discovery point for the skill library, generated by `sync-skills` | **INDUCED** |
| `.agents/hooks.json` | Antigravity hook registration — delegates to `antigravity_policy.py` | **ENFORCED** |
| `.agents/skills/` | Antigravity discovery point for the skill library, generated by `sync-skills` | **INDUCED** |
| `GEMINI.md` | one-line Gemini / Antigravity shim pointing to `AGENTS.md` | **INDUCED** |

*Registered but measured **inert** until workspace trust is granted in the ZCode client —
[`core/experiments/zcode-hook-protocol.md`](../experiments/zcode-hook-protocol.md). No zcode cell
below reads ✅ until a post-trust probe run earns it.

## The contract a new agent's shim must satisfy

Three hook points cover the whole surface:

```
PreTool (Read)  → sh   core/run hooks/read/pre-read.py
PreTool (Edit)  → sh   core/run hooks/checks/pre-edit.py
                  sh   core/run hooks/facade/facade-scan.py   (write/create only)
                  sh   core/run hooks/facade/facade-gate.py
PostTool (Edit) → bash core/hooks/post-edit.sh
PostTool (Read) → sh   core/run hooks/facade/facade-tracker.py
```

Every canonical hook expects `file_path` (absolute), the `CLAUDE_TOOL_NAME` env var (`"Read"`,
`"Edit"` or `"Write"`), the JSON payload on **stdin** for pre-hooks and in **`CLAUDE_TOOL_INPUT`** for
post-hooks, and treats exit code **2** as a hard block with stdout as the message shown to the agent.

**A shim must pass a session-stable id** or the markers never dedupe and every gate fires on every
call. Claude Code takes `session_id` from the stdin JSON; the Copilot shims derive `copilot<host-pid>`.
`facade-gate` and `facade-tracker` additionally key on the process PID to isolate parallel sessions —
a new agent adapts `get_session_id()` in those two scripts. Worked examples:
`copilot/copilot-pre-tool.py`, `copilot/copilot-post-tool.py`, and
`.opencode/plugins/workspace-policy.js`.

### Coverage across agents

| Hook | Git | Claude Code | Copilot | opencode | zcode | Antigravity |
|------|-----|-------------|---------|----------|-------|-------------|
| Pre-read (interface redirect) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Pre-edit (size / description) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Pre-edit facade-scan (new files) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Pre-edit facade-gate (`code/` edits) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Post-edit (stubs / context sync) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Post-read facade-tracker | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Context-gate (`CONTEXT.md` chain) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Bash context-gate (cat/grep bypass) | — | ✅ | ✅ (terminal hints) | ✅ (bash + grep tools) | ⏸ | ✅ (`run_command`) |
| Context / interface read tracker | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| ISSUES gate (FIXED needs a spec) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Spec-read-gate (spec-locked modules) | — | ✅ | ✅ | ✅ | ⏸ | ✅ |
| Size / facade import / stub gen / context sync | ✅ | — | — | automatic (git) | automatic (git) | automatic (git) |
| Spec-driven new-module gate | ✅ block | — | — | automatic (git) | automatic (git) | automatic (git) |
| Duplication gate (jscpd) | ✅ block | — | — | automatic (git) | automatic (git) | automatic (git) |
| `verify:fast` contract gate | ✅ block | — | — | automatic (git) | automatic (git) | automatic (git) |
| ESLint R1-R6 (TS under `code/`) | ✅ block | ✅ warn | ❌ gap | ❌ gap | ❌ gap | ❌ gap |
| Prettier auto-format (TS under `code/`) | — | ✅ | ❌ gap | ❌ gap | ❌ gap | ❌ gap |

The six ❌ are the live gaps: Copilot, opencode and zcode get no lint enforcement at all, so a TS
violation authored there is caught only at commit, by git. **⏸ means registered, not firing** — the
trust gate above holds the zcode column inert, and it flips only when a post-trust probe verifies each
row. Event remaps: no `SubagentStart` in zcode, so `agent-context.py` rides PreToolUse `Agent|Task`;
no `PreCompact`, so `precompact-wipe.py` rides SessionStart `^compact$`.

## A ✅ in that table is a claim, and `test_shim_paths.py` is what checks it

Every path a shim spawns must resolve, and that test asserts it — its own header carries why, and
what the check does *not* buy: it proves a path **resolves**, never that the gate **fires**.

**So a new runtime's shim owes two things**, not one: the contract above, and an entry in `SHIMS` in
`core/tools/test/workspace/test_shim_paths.py` naming its files and how a spawn names a script. A
shim with no entry is unchecked, which is the state opencode and Copilot were both in.
