---
name: install
description: >
  Install this workspace on the machine you are running on: probe every step in SETUP.md, report
  what is missing, and execute it. Invoke with /install [feature slug, or blank for everything].
---

# Install

Arguments: $ARGUMENTS — a feature slug to install just one feature, or empty for all of them.

---

## What you are

**You are the installer.** There is no install script and there is not going to be one: an
installer would have to be ported to every harness, while the newcomer's own agent works on
whichever harness they already opened. That is you.

**This skill is a door, not a copy.** The procedure is [`SETUP.md`](../../SETUP.md) at the workspace
root plus the `SETUP-<slug>.md` shards it routes to, and it stands alone — a stranger on another
agent has no skill loaded and installs from those files directly. Never restate a command from it here or in your reply; read it and run it.
If you catch yourself explaining a step, you are drifting into a second copy that will disagree
with the first one.

## Protocol

1. **Read `SETUP.md`, then every shard its routing table names.** The index carries the contract each
   step follows — `> feature:`, **Precondition**, **Install**, **Verify** — plus what is already
   wired and the whole-install probe; it holds **no steps of its own**. The steps live in the
   `SETUP-<slug>.md` siblings, between each one's `<!-- steps:start -->` and `<!-- steps:end -->`
   markers, one `##` section each. Nothing outside those markers is a step. `SETUP-clone.md` runs
   first; the rest are independent.

2. **Run every step's Precondition first, before installing anything.** Then print one table and
   stop:

   | Step | Feature | Status |
   |---|---|---|
   | … | … | `installed` · `missing` · `needs-you` |

   `needs-you` is any step marked `agent: no`. Do not attempt those and do not skip them silently.

3. **Ask which missing steps to run** — default to all of the `agent: yes` ones. If `$ARGUMENTS`
   named a feature slug, filter to steps declaring it and say what you filtered out.

4. **Execute each chosen step, then run its Verify probe.** A step is done when its probe passes.
   **Never report a step done because its config looks right** — SETUP's own RTK step exists
   because a wiring that read as correct was silently dropping every multi-line call for weeks.
   If a probe fails, stop that step, show the probe's real output, and move to the next step.

5. **Hand over the rest.** For each `needs-you` step, quote the one thing it says to ask for — an
   API key, a consent-screen click, a device pairing. Ask for the secret itself and write the config
   yourself; never hand Lucas a command to run. A pasted secret goes into a file through a pipe or
   an environment variable, never on a command line.

6. **Close with the whole-install probe** in SETUP.md § Verification, and report its real output.

## Rules

- **Idempotent or ask.** Every Install block is written to be safely re-runnable. If one is not
  obviously so, run its Precondition again rather than guessing.
- **Report failures as failures.** A missing dependency, a red probe, a skipped step — say so
  plainly with the output. An install that reports success it did not verify is worse than one that
  reports the gap.
- **A step that will not fit the contract is a finding**, not a nuisance: it means the procedure is
  not executable, and it belongs at the end of `brain/INBOX.md`.
