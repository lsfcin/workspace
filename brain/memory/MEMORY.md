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
- [Feedback: provider-agnostic naming](feedback_provider_agnostic_naming.md) — nunca nome de provider/modelo em
  arquivos/verbos/dirs; função no nome, provider como dado
- [Feedback: background bash reliability](feedback_background_bash_reliability.md) — backgrounded Bash chains can die
  silently across a ScheduleWakeup pause; prefer foreground or unchained calls for sweeps the user is waiting on
- [Feedback: delete weak features](feedback_delete_weak_features.md) — sinal fraco = deletar por completo (código, docs,
  deps, menções), deixando só uma nota curta de rejeição; nunca manter rebaixado a "dica"
- [Feedback: material de aula é aditivo](feedback_additive_course_material.md) — em deck do Lucas, intercalar e refinar
  no lugar; nunca substituir, pular ou reordenar
- [Feedback: explore before cutting](feedback_explore_before_cutting.md) — enquanto a decisão de design está aberta,
  manter todas as variantes; cortar só depois do veredito de Lucas
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
- [Feedback: contexto na pergunta](feedback_question_context.md) — toda escolha oferecida ao Lucas explica contexto,
  problema e tradeoffs na própria pergunta e em cada opção; ele "passa direto" no que não está ali
- [Feedback: plain language](feedback_plain_language.md) — plain words over jargon (ledger/seam/probe are out); one idea
  one word; language IS the system when the reader is an LLM; say what a session decided alone
- [Feedback: concise WOS](feedback_concise_wos.md) — cada sessão deve deixar MENOS linhas do que
  achou; feature nova paga com o corte que a financia; nunca resumir uma lei até ela deixar de valer
- [Feedback: multiharness essencial](feedback_multiharness_essential.md) — nunca excluir um harness (otimizar a cópia,
  não a função); e nenhum hook morre sem placar de disparos
