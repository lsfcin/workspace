# Reflow vs cutting
> How many lines does undoing the dead width limit remove, and why does none of it count as reduction?

`AGENTS.md` rules that **reflowing is not cutting** (2026-08-31): a file is held to lines AND to characters, so reshaping the same words satisfies neither. The document cap then replaced a per-line width limit on 2026-09-14 (`core/hooks/limits.env`), which left every paragraph written before that date wrapped to a width nothing measures. Undoing that is worth doing and is worth **nothing** against `core/norms/reduce.md`, and this file exists so the next session reading a 19% drop does not mistake it for a debt paid.

## Method

```
core/run tools/wos/size                                    # before
git ls-files '*.md' | grep -v '^academy/' | xargs core/run tools/wos/reflow --write
core/run tools/wos/size                                    # after
```

The measurement is the `.md` line total `size` prints, before and against after. Words removed is asserted rather than measured: `reflow` rewrites a file only when its words come back identical (`words()`), so the count is zero by construction and a non-zero one would be a refusal, not a row here.

## Results

| Date | Files rewritten | Breaks removed | Lines before | Lines after | Words removed |
|---|---|---|---|---|---|
| 2026-09-18 | 278 | 4,801 | 25,098 | 20,289 | 0 |

## What changed

The corpus reads as one paragraph per paragraph, and `size` fell 19% in one run without a single deletion — which is the whole point of writing this down. The three-field shape of a `ROADMAP.md` item survived because the rule joins only mid-sentence; the literal reading of "one paragraph, one line" fused those fields and was rejected the same day, by eye, after the round-trip assertion passed on the damage.

**The baseline for `reduce.md` moved and nothing was paid.** Any future claim that the workspace got smaller has to be measured against 20,289, not against 25,098.

## Limitations

- **This says nothing about whether the corpus got better to read.** It counts lines. Whether a paragraph on one line is easier or harder for Lucas and for a model than one wrapped at 95 columns is not measured here and was not asked.
- `academy/` was excluded: a parallel session was writing in it. Its breaks are uncounted and still there.
- A diff is now paragraph-granular in reflowed prose — a one-word change rewrites the whole line. That cost is real, was not measured, and is the standard argument for semantic line breaks that this run decided against.
- Nothing proves the 4,801 breaks were all artificial. The rule is conservative in one direction only: it never joins across a full stop, so it under-counts and cannot over-reach.
