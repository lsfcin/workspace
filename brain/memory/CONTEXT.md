# memory
> What the agent learned across sessions and nothing else records. Harness-written, workspace-owned.

**The harness path is a symlink into here** — `~/.claude/projects/<slug>/memory` →
`brain/memory/` — so every memory written by the agent lands in the workspace by construction,
shows up in `git status`, and can be trimmed like any other file. This gives both properties at
once: **locality** (the content is in the repo) and **control** (we can edit or delete
it). Per-file symlinks would have given only the first, leaving each *new* memory outside until
someone adopted it.

What cannot be controlled is the agent *deciding* to write one. That is fine — it lands in a diff.

| File | Role |
|------|------|
| `MEMORY.md` | The index. One line per memory; loaded into every session, so its length is a real cost (~1,198 tok — measured, see below). |
| `<slug>.md` | One fact each, with `name` / `description` / `metadata.type` frontmatter. |
| `user_profile.md` | A symlink to [`../USER.md`](../USER.md) — the profile is workspace content first and a memory second. |

Types are `user` · `feedback` · `reference`. Bodies link to each other with `[[name]]`,
and a `[[name]]` with no matching file is allowed on purpose: it marks a memory worth writing.
That is why `test_pointer_integrity` gates `](path)` links here but **not** `[[slug]]` ones.

**Cost, measured rather than assumed:** the index is ~1,198 tok of a ~27.6k session start, less than
half the skill listing. The long-standing suspicion that this store duplicates `USER.md` + `goals/`
enough to be worth folding was tested and **rejected on the numbers** —
[`core/experiments/context-window.md`](../../core/experiments/context-window.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`MEMORY.md`](MEMORY.md) | Memory Index |
| [`fable_quota_strategy.md`](fable_quota_strategy.md) | How Lucas spends remaining Fable 5 quota (won't renew) — Fable decides, Opus writes, Sonnet executes; multiview session DONE 2026-07-07 |
| [`feedback_additive_course_material.md`](feedback_additive_course_material.md) | in Lucas's course material, contributing means ADDING and refining in place — never replacing, skipping or reordering what he made |
| [`feedback_agent_runs_auth.md`](feedback_agent_runs_auth.md) | Agent runs every auth command itself; Lucas only does what has no command form (provider-UI clicks, consent screens, minting a secret) |
| [`feedback_background_bash_reliability.md`](feedback_background_bash_reliability.md) | Backgrounded Bash tool calls (run_in_background) can die silently across a ScheduleWakeup boundary, with no completion notification and no error in the redirected log. |
| [`feedback_bug_tracking.md`](feedback_bug_tracking.md) | isoroll-module bugs go in ISSUES.md, not memory |
| [`feedback_concise_wos.md`](feedback_concise_wos.md) | Lucas wants each session to leave the workspace with FEWER total lines than it found; a new feature owes the cut that pays for it |
| [`feedback_delete_weak_features.md`](feedback_delete_weak_features.md) | Lucas deletes a feature that only produces weak signal rather than keeping it as a hint — remove it from every file and mention, leaving only a short rejection note |
| [`feedback_explore_before_cutting.md`](feedback_explore_before_cutting.md) | while a design question is still open, keep every variant; delete only after Lucas rules — the exploration-phase exception to delete-weak-features |
| [`feedback_full_workflow_thinking.md`](feedback_full_workflow_thinking.md) | plan isoroll (and similar) work from the full user workflow, not from artifacts — loose ends are the recurring failure |
| [`feedback_inbox_ref_task_pairing.md`](feedback_inbox_ref_task_pairing.md) | /inbox — an actionable ref must also spawn an assessment task, never land as ref-only |
| [`feedback_multiharness_essential.md`](feedback_multiharness_essential.md) | Multi-harness is ESSENTIAL to Lucas — optimize the copying, never delete a harness; and no hook dies without a scoreboard |
| [`feedback_parallel_sessions.md`](feedback_parallel_sessions.md) | How to work safely when multiple Claude/opencode sessions edit /mnt/workspace at once |
| [`feedback_plain_language.md`](feedback_plain_language.md) | Write WOS in plain words — Lucas loses the thread when jargon accumulates, and language IS the system when the reader is an LLM |
| [`feedback_provider_agnostic_naming.md`](feedback_provider_agnostic_naming.md) | Never put provider/model names (NB, Gemini, etc.) in file names, verbs, or dirs — workspace is provider-agnostic |
| [`feedback_question_context.md`](feedback_question_context.md) | every choice put to Lucas carries the context, the problem and the tradeoffs in the question itself and in each option |
| [`feedback_visual_eyeball_gate.md`](feedback_visual_eyeball_gate.md) | Every image-producing pipeline step needs Lucas's visual review (artifact board) before advancing — loops passing their own tests is not enough for visual work |
| [`reference_linuz90_bot.md`](reference_linuz90_bot.md) | linuz90/claude-telegram-bot source read — the reference design for aiwbot; how it does session lineage + its UX feature set |
| [`reference_texpace_is_spacemantics.md`](reference_texpace_is_spacemantics.md) | texpace" routes to the spacemantics project — same thing for /inbox routing |
| [`user_profile.md`](user_profile.md) | Lucas — read before any Brain task. |
<!-- routing:end -->
