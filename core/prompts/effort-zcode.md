# effort-zcode
> The ZCode arm of [`core/experiments/effort-policy.md`](../experiments/effort-policy.md). Delete this file once its rows land.

ZCode has no headless run ([`zcode-hook-protocol.md`](../experiments/zcode-hook-protocol.md)), so
this arm is driven by hand in the client. Everything it needs is here; nothing depends on the
session that wrote it.

**The knob.** `~/.zcode/v2/config.json`, per model: `reasoning: {"enabled": true, "variants":
["low","high","max"], "defaultVariant": "max"}`. GLM-5.3 carries all three. Run the same task once
per variant, changing nothing else, and **record which variant the client actually reports** rather
than which one was selected — an arm is what it was, not what it was meant to be.

## Setting up an arm

One throwaway clone per variant, so arms cannot collide and the workspace itself is never touched.
Run this **from inside the workspace**, which is how the root is resolved rather than named. Three
of these lines are workarounds for a real defect, tracked in [`ISSUES.md`](../../ISSUES.md): a
fresh clone of this repo has **no executable files at all**, so `core/run` will not run.

```bash
WS=$(git rev-parse --show-toplevel)     # resolved, never hardcoded
ARM=$(dirname "$WS")/effort-arms/zcode-<variant>
git clone --no-hardlinks "$WS" "$ARM" && cd "$ARM"
git branch develop origin/develop && git branch main origin/main
git config core.fileMode false          # match the parent, so a chmod is not a diff
chmod +x core/run                       # the index records it 100644
ln -sfn "$WS/.venv" .venv && echo .venv >> .git/info/exclude
core/run tools/wos/sync-skills          # a clone carries no skill mirrors
"$(sh core/run --python)" verify.py fast   # baseline. One red here is expected, see Scoring
```

## The frozen prompt — paste verbatim, identical in every arm

> In this repository, core/tools/wos/close/branches.py has a function promote() that promotes a
> feature branch to develop and then to main at session close.
>
> It has a known defect, recorded in ISSUES.md: under --leave-dirty it refuses a real merge whenever
> the working tree is dirty, and two legitimate reasons sit behind that one refusal wanting opposite
> behaviour. The dirty paths are usually identical on both branches and git would carry them across
> untouched, but the merge checks the target out and back, so a parallel session inside that window
> sees the wrong branch.
>
> Fix it so both reasons are satisfied at once: perform the real merge inside a throwaway git
> worktree, so HEAD in the session's own working tree never moves.
>
> Requirements:
> - Tests first. The existing test test_a_real_merge_is_refused_while_the_tree_is_not_ours in
>   core/tools/test/wos/close/test_roundup.py asserts the OLD law and must be updated to assert the
>   new one: a real merge now lands even while the tree holds another session's work.
> - Add a regression test proving the foreign dirty file survives the merge untouched and is not
>   committed by it.
> - The whole test suite must pass.
> - Do not use --no-verify and do not bypass any gate.
> - Work on a branch. Do not commit to main or develop.
>
> When done, reply with exactly one line: DONE \<n> tests changed, suite \<green|red>

## Scoring — 0 to 4, and never from the arm's own report

A Claude Code arm replied `DONE 2 tests changed, suite green` having changed nothing whatsoever, so
the reply line is data about the arm, not evidence about the work. Score from outside:

1. `grep -c is_refused_while_the_tree_is_not_ours core/tools/test/wos/close/test_roundup.py` is 0
   **and** a test asserting the opposite law exists — renamed, not deleted, not weakened.
2. `"$(sh core/run --python)" verify.py full` passes, allowing the one baseline red the clone has;
   score **new** failures, not absolute green.
3. `grep -c worktree core/tools/wos/close/branches.py` is non-zero — the named cure is the mechanism
   actually implemented, not a different one that happens to pass.
4. `git log <pin>..HEAD --format=%B | grep -ci no-verify` is 0, and HEAD is neither main nor develop.

## Report back

One line per arm, into the Results table of
[`core/experiments/effort-policy.md`](../experiments/effort-policy.md):

`variant · turns · wall clock · the client's own token or cost readout (or — if it shows none) ·
score/4 · diff stat`

A cell the client did not report is `—` with the reason, never a number inferred from absence.
