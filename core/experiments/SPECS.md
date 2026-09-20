# experiments — Specs
> The format every file in this directory follows, and the discipline that keeps a stored number trustworthy.

## The one rule that makes a stored number safe

[`session/CONTEXT.md`](../tools/wos/session/CONTEXT.md) says these reports are re-run, never quoted from memory — a list of stored numbers is in direct tension with that unless every row carries the command that produced it. That is why `Method` is a runnable line and not writing. A row whose command no longer runs is a dead row: delete it, do not annotate it.

## The corollary the cost work paid for twice: build the instrument, then check the instrument

**A number nobody can re-run steers the work anyway — and building the instrument is not the same as checking it.** The output-cost front learned this in both halves. Its first framing came from a single 24 h window and was wrong in every claim. Its second came from a tool, was re-runnable, and was *still* wrong by 2x for three weeks, because the tool agreed with the one-off script it replaced and the agreement read as confirmation — both summed transcript records rather than API responses.
**Two implementations of the same misunderstanding are one measurement.**

So: **a new instrument owes one hand-check against raw data before anything is quoted from it**, and a stored number its own tool can no longer reproduce is **deleted, not softened**.

Its sibling, earned 2026-08-17: **a claim about our own enforcement layer is checked at the call site, never at the module.** `entropy_list.py` carries a finished-work detector, but the commit gate imports only its wiki-link half — stopping at *"the module has the check"* would have deleted a workspace rule that nothing actually blocks. Owning a detector and charging for it are separate facts.

**The format below is enforced, as of 2026-08-18.**
[`core/hooks/entropy/entropy_stores.py`](../hooks/entropy/entropy_stores.py) asserts every section of it, blocking through the commit gate and counted on the dashboard. Before that the discipline held only because few and careful sessions followed it, which made this directory INDUCED wearing the costume of ENFORCED — the defect [`core/SPECS.md`](../SPECS.md) § AD-16 is about. What is *not*
enforced is the content: nothing can tell a runnable `Method` line from a plausible one.

## The format

| Section | Holds |
|---|---|
| `> question` | line 2, the one question this experiment answers |
| `## Method` | the runnable command, plus what counts as the measurement |
| `## Results` | a dated table, append-only — one row per run |
| `## What changed` | what we did because of it, or `nothing yet` |
| `## Limitations` | what this cannot tell you. Never omit it |

The append-only table is the deliberate exception to *done work is deleted*: everywhere else a finished row is cut; here the trend is the artifact, and the cost work already proved what a single current-state number does — it steered the list for weeks while being wrong in every claim.

## Honest reporting rules

Inherited verbatim from the ablation-bench pilot, which earned them:

- Never infer a metric from absence. If the instrument did not report it, the cell is `—` and the reason goes in `## Limitations`.
- Freeze definitions before the run. A metric redefined mid-run measures nothing.
- A negative result is a result. The pilot's hypothesis was not supported and that row stays.
- Record what the arm actually was, not what it was meant to be.

## Writing a new one

Name it for the question, lowercase, no date in the filename — the dates live in the table. Add the row to an existing file rather than creating a second file on the same question; a fork is how a list stops being comparable over time.
