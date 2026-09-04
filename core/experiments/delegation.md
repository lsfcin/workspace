# Delegation
> How often does this workspace actually spawn a subagent, and which agent definitions get used?

## Method

Runs against the local transcripts, no network. A worker's own transcript lives under
`<session>/subagents/`, **not** beside the parent in the flat project directory — reading only the
flat directory is what produced the retired "nothing has ever been delegated" claim.

```
cd ~/.claude/projects/-mnt-workspace
ls *.jsonl | wc -l                                  # sessions
grep -l '"name":"Agent"' *.jsonl | wc -l            # sessions that delegated at least once
grep -ho '"name":"Agent"' *.jsonl | wc -l           # spawns
find . -path '*/subagents/*.jsonl' | wc -l          # worker transcripts (must equal spawns)
grep -ho '"subagent_type"[: ]*"[a-zA-Z-]*"' *.jsonl | sed 's/.*"\([a-zA-Z-]*\)"$/\1/' \
  | sort | uniq -c | sort -rn                       # spawns by agent type
```

The hand-check this instrument owes (`SPECS.md` § The corollary the cost work paid for twice):
**worker transcripts must equal spawns**, and the per-type counts must sum to the spawn total. Both
held on the first run — 37 = 37, and 15+12+3+3+3+1 = 37 — so no spawn is unattributed and none is
double-counted.

## Results

| Date | Sessions | Delegated | Spawns | Explore | general-purpose | craft-* | Plan | `core/agents/` |
|------|---------:|----------:|-------:|--------:|----------------:|--------:|-----:|---------------:|
| 2026-08-17 | 152 | 11 (7.2%) | 37 | 15 | 12 | 9 | 1 | **0** |

Two readings, and the second is the one that matters:

- **Delegation happens.** 7.2% of sessions spawn at least once. The previous claim — *zero
  sidechain messages across 328 transcripts, nothing has ever been delegated* — was an artifact of
  scanning the wrong directory, not a finding.
- **No workspace-authored agent has ever been spawned.** 28 of 37 spawns are harness builtins
  (`Explore`, `general-purpose`, `Plan`) and 9 are the `craft-*` provider mirrors. The five roles in
  `core/agents/` — lead, researcher, writer, verifier, reviewer — are at zero, and their only
  entrypoint (`/research`) does not appear in any transcript.

## What changed

The false claim was cut from the wos ledger's agents item and replaced with a pointer here. The
item itself was **not** closed on this number: a feature that was never given a deliberate trial
is not the same as one that was tried and refused (Lucas, 2026-08-17), and this measurement cannot
tell the two apart — see Limitations.

## Limitations

- **Scoped to one project directory** (`-mnt-workspace`). Sessions run from another root are not counted.
- **Usage is not value.** Zero spawns of `core/agents/` measures reach and discovery, not worth. The
  research *tools* those flows wrap are heavily used over the same window — `core/tools/web/search`
  319, `video/` 771, `notes/` 325, `paper/parse` 163, `paper/papers` 160 — so the feature is
  exercised daily while the orchestration around it is not. That gap is the finding; its cause is
  not measured here.
- **`subagent_type` is absent on a spawn that names no type**, and every spawn in this window carried
  one. A future run where the counts stop summing to the spawn total means that changed, not that a
  spawn vanished.
- **Says nothing about outcome quality.** Whether a delegated turn produced better work than an
  inline one is not in the transcripts.
