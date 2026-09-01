# Memory Index

- [User Profile](user_profile.md) — Lucas, CS professor at UFRPE/CIn-UFPE, research in Hybrid Intelligence, Mechanism
  Design, AR, 3D CV — file lives at brain/USER.md (symlinked)
- [Feedback: bug tracking](feedback_bug_tracking.md) — isoroll bugs go in code/isoroll-module/ISSUES.md, not memory
- [Feedback: parallel sessions](feedback_parallel_sessions.md) — partition workspace by subtree across concurrent
  sessions; check git status AND the current branch right before committing; stage explicitly, commit often
- [Feedback: visual eyeball gate](feedback_visual_eyeball_gate.md) — image-producing steps need Lucas's visual OK
  (artifact board) before advancing; shortest path to visible content
- [Fable Quota Strategy](fable_quota_strategy.md) — "Fable decides, Opus writes, Sonnet executes"; multiview is
  consumed, its F1 spine lives on develop; instituto prompt is in its final window
- [Feedback: provider-agnostic naming](feedback_provider_agnostic_naming.md) — never a provider or model name in
  files, verbs or directories; the function is the name, the provider is data
- [Feedback: background bash reliability](feedback_background_bash_reliability.md) — backgrounded Bash chains can die
  silently across a ScheduleWakeup pause; prefer foreground or unchained calls for sweeps the user is waiting on
- [Feedback: delete weak features](feedback_delete_weak_features.md) — weak signal = delete outright (code, docs,
  deps, mentions), leaving only a short rejection note; never keep it demoted to a "hint"
- [Feedback: course material is additive](feedback_additive_course_material.md) — in Lucas's deck, interleave and
  refine in place; never replace, skip or reorder
- [Feedback: explore before cutting](feedback_explore_before_cutting.md) — while the design decision is open, keep
  every variant; cut only after Lucas rules
- [Reference linuz90 bot](reference_linuz90_bot.md) — linuz90/claude-telegram-bot source read: SDK plain-resume
  single-lineage design + UX feature set; the aiwbot reference
- [Feedback: full-workflow thinking](feedback_full_workflow_thinking.md) — plan from the user workflow not artifacts;
  loose ends are isoroll's recurring failure; convert every eye-catch into a code invariant
- [Feedback: inbox ref→task pairing](feedback_inbox_ref_task_pairing.md) — actionable refs must spawn a paired
  assessment task, never land ref-only; policy in core/skills/inbox.md
- [Reference: texpace = spacemantics](reference_texpace_is_spacemantics.md) — route "texpace" captures to
  code/spacemantics
- [Feedback: agent runs auth](feedback_agent_runs_auth.md) — agent runs every auth command itself; ask Lucas only for
  provider-UI clicks, consent screens, minting a secret; pasted secrets go in via builtin pipe, never argv
- [Feedback: context in the question](feedback_question_context.md) — every choice put to Lucas explains context,
  problem and tradeoffs in the question itself and in each option; he "passa direto" past what is not there
- [Feedback: plain language](feedback_plain_language.md) — plain words over jargon (ledger/seam/probe are out); one idea
  one word; language IS the system when the reader is an LLM; say what a session decided alone
- [Feedback: concise WOS](feedback_concise_wos.md) — every session must leave FEWER lines than it found; a new
  feature pays with the cut that funds it; never summarize a law until it stops holding
- [Feedback: multi-harness is essential](feedback_multiharness_essential.md) — never delete a harness (optimize the
  copying, not the function); and no hook dies without a scoreboard of what it fired on
