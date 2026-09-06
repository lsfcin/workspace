# hook-latency
> What does the enforcement layer cost per tool call, and how much of that is work nobody asked for?

## Method

```
core/run hooks/trigger/hooktime.py --reps 5            # and once per harness, via --config
```

The measurement is the **median** wall time of one hook process, per capability, plus a `TOTAL`
row summing only the hooks whose matcher actually fires for that capability. Median, not mean:
the first run of any hook pays the filesystem cache and would otherwise set the number.

`hooktime` reads the registrations out of `.claude/settings.json` rather than holding a list, so
a hook added to the config appears here without the bench being edited. `--config` points it at
another harness's file, and it lives beside `trigger_law.py` because both answer a question about
the registrations rather than about a file's location. `--reps` sets the sample count.

One canonical payload per capability, matching what `hook_input.capability()` asks of a real one:
`read` = a path alone, `write` = a path plus new content, `shell` = a command line, `other` = a
payload naming no path at all (a Grep, a TodoWrite).

## Results

Per **tool call**, summing PreToolUse and PostToolUse — the number a session actually pays.

| Date | Machine · harness | read | write | shell | other | Note |
|---|---|---|---|---|---|---|
| 2026-09-05 | dell-g15 Linux · claude | 0.211 s | 0.308 s | 0.221 s | 0.222 s | three PostToolUse registrations, each its own process |
| 2026-09-05 | dell-g15 Linux · claude | 0.116 s | 0.273 s | 0.121 s | 0.118 s | PostToolUse collapsed into the dispatcher |
| 2026-09-05 | dell-g15 Linux · zcode | 0.109 s | 0.260 s | 0.119 s | 0.114 s | same tree, the other harness's config |

Floor, same runs: `sh core/run --python` **0.007-0.009 s**, a bare interpreter start
**0.026-0.031 s**. So roughly **60% of any hook's cost is CPython starting**, before a gate reads
a byte — which is why the fix that pays is removing processes, not making gates faster.

Per-hook, after the change: `dispatch.py` 0.049-0.061 s (all capabilities), `post-edit.sh`
0.170 s (write only), the two trackers 0.043-0.052 s each (read only).

## What changed

**PostToolUse collapsed into `dispatch.py`**, which PreToolUse already was (`bf46b96`).
`gates.txt` gained a **moment** column, so one table now says which gate runs at which moment for
which capability, and the two trackers moved into it. A tool call runs one dispatcher per moment
instead of three separate hooks — **1.9x on `other`, 1.8x on `shell` and `read`.**

**`post-edit.sh` refuses in shell, before resolving the interpreter.** It cannot move into the
dispatcher (it is bash, and the table's rows are imported into the dispatcher's process), so it
keeps its `.*` registration and pays for its own exit — now a `case` over the raw payload for the
keys that make a call a write, rather than a fresh Python that imports `hook_input` to ask
`capability()`. 0.058 s → 0.009 s on every non-write call.

**The narrow fix was tried first and refused, which is the part worth keeping.** Matching the tool
names each hook serves — `Edit|Write` on `post-edit.sh`, `Read` on the trackers — measured *better*
than the collapse (0.054 s on `shell`) and was reverted:
`test_b20260901_a_second_shell_tool_walks_past_every_read_gate` refuses a matcher naming tools, and
is right. A tracker that misses a harness's tool is worse than one that runs too often, because the
gate it feeds goes on demanding a CONTEXT.md the session already read and the agent cannot clear
it. **The saving had to come from fewer processes, never from fewer tools.** A side finding from
the same attempt: an unanchored `Write` matcher also matches **TodoWrite**.

**Both harnesses measured, and they agree.** `.zcode/config.json` had been carrying
`Edit|Write|ApplyPatch` and `Read` on its PostToolUse hooks — the whitelist shape, live, in a
config the b20260901 spec never looked at because it reads `.claude/settings.json` alone. Now both
register the dispatcher on `.*`.

Guarded by
[`test_b20260905_hooks_and_tools_suspected_of_paying_more_time_than_needed.py`](../tools/test/workspace/gates/test_b20260905_hooks_and_tools_suspected_of_paying_more_time_than_needed.py),
which asserts the *shape* — no matcher wider than the hook's declared capability, and no
divergence between the two harnesses — never a wall-clock threshold.

## Limitations

- **Linux only.** The Windows clone is where Lucas reports the problem is worse, and no row here
  is from it. The mechanism is known and needs no OS branch to explain: nothing on the hook path
  asks which operating system this is — only the platform seam may, and it is not on that path —
  so the penalty is MSYS's emulated `fork()` against the 4-6 forks each `core/run` invocation
  makes. Unmeasured there. **Run this on that clone and add the row.**
- **A bench is not a session.** `hooktime` spawns hooks back to back on a warm cache; a real call
  interleaves them with the model, the harness and the filesystem in whatever state it left them.
  Read these as a floor and as a ratio, never as a session's true bill.
- **Only two of five harnesses are measured.** The Copilot, Antigravity and opencode shims run the
  two trackers by path rather than through the dispatcher, so they still work and still pay three
  processes — and each is a hand-copy of the table `gates.txt` exists to be the only copy of.
  Routing them through the dispatcher is unstarted; `hooktime --config` cannot read them, because
  they are code rather than a registration file.
- **A write still costs 0.26-0.27 s, and almost all of it is `post-edit.sh` doing real work**
  (0.155-0.172 s): stub regeneration, the first-line check, the CONTEXT.md sync, lint. That is the
  next thing to look at, and it is a different question from this one — what the layer costs when
  it fires, rather than what it costs when it does not.
- The `write` row runs `post-edit.sh` against a real workspace file, so it includes whatever
  stubgen and the lint stage do for **that** file. A write to a `.ts` file in a project with a
  `tsconfig.json` costs more, and is not measured.
