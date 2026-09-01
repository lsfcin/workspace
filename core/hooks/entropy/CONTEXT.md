# entropy
> The Tier 0 checks that count what the tree has drifted into. One question each.

Each module here answers one question about the corpus and hands back findings; nothing here
prints, blocks or renders. Two callers consume them, and the split between those callers is the
design: [`../checks/type-gate.py`](../checks/CONTEXT.md) **blocks**, on what a commit adds, and
[`dashboard/`](dashboard/CONTEXT.md) **reports**, on everything, so a repo that inherited a
violation is visible without being unable to commit.

[`entropy_corpus.py`](entropy_corpus.py) is the odd one and stays: it answers *which files a check
may look at*, which every check needs before it can count anything.

**This directory sits over the fanout signal and holds there** — ruled 2026-08-24 (Lucas), after the
candidate seam was costed: splitting on what each check *reads*, the tree's shape (`corpus`,
`naming`, `fanout`, `size`) against its text (`context`, `ledger`, `stores`, `vendor`), would have
made the dashboard import from two places to remove less table than the hop adds. The name has not
drifted — every module here really does answer one question — so the signal is the cost of the
design working, and the baseline carries it rather than a rising threshold.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`dashboard/`](dashboard/CONTEXT.md) | The entropy report: running every check over the whole tree, and what the findings look like. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy_context.py`](entropy_context.py) | [`entropy_context.pyi`](entropy_context.pyi) | `check_inventory`, `context_head`, `check_misplaced_answer`, `check_description`, `check_truncation` | Tier 0 CONTEXT.md rules, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_corpus.py`](entropy_corpus.py) | [`entropy_corpus.pyi`](entropy_corpus.pyi) | `staged_added_files`, `tracked_files`, `tracked_paths`, `nested_repos`, `is_generated_mirror` | Which files the Tier 0 checks look at, and which of them are allowed to name what the checks forbid. Split from entropy_ledger.py 2026-07-30 at the 150-line warn: enumerating the corpus is a different job from asserting things about it. |
| [`entropy_fanout.py`](entropy_fanout.py) | [`entropy_fanout.pyi`](entropy_fanout.pyi) | `fanout_counts`, `fanout_signals` | Directory fanout: how many files one directory asks a reader to hold at once. |
| [`entropy_fields.py`](entropy_fields.py) | [`entropy_fields.pyi`](entropy_fields.pyi) | `field_hits` | Does a header field that names our own code name something that exists? Zero-token, deterministic. |
| [`entropy_ledger.py`](entropy_ledger.py) | [`entropy_ledger.pyi`](entropy_ledger.pyi) | `retired_hits`, `item_slugs`, `duplicate_slugs`, `finished_work_hits`, `unanswered_placeholders` | Tier 0 ledger and vocabulary checks, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_naming.py`](entropy_naming.py) | [`entropy_naming.pyi`](entropy_naming.pyi) | `check_shape`, `untracked_routing_targets`, `check_dirs`, `check_placement` | Tier 0 naming and placement, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_size.py`](entropy_size.py) | [`entropy_size.pyi`](entropy_size.pyi) | `size_signals`, `stub_signals` | How big a file got, and whether anything can read its interface. Zero-token, deterministic. |
| [`entropy_stores.py`](entropy_stores.py) | [`entropy_stores.pyi`](entropy_stores.pyi) | `experiment_hits`, `ref_tier_hits` | Tier 0 for the two stores that record what we know and how sure we are: core/experiments/ and core/refs/REFS.md. Zero-token, deterministic. |
| [`entropy_vendor.py`](entropy_vendor.py) | [`entropy_vendor.pyi`](entropy_vendor.pyi) | `is_ledger`, `vendor_directive_hits` | Does a ledger assign a vendor's model where it should assign a tier? Zero-token, deterministic. |
<!-- routing:end -->
