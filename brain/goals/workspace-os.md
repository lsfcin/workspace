# [ health | mental | year ] workspace OS

A centralized personal operating system: all thoughts, projects, demands, full-life organization in one place. Automated setup that eases how life gets managed, reduces mental pressure, and enables goals and dreams to move from idea to action. Reliable, productive, and genuinely used — not just designed. Currently in MVP prototyping phase. First validated version expected in ~6 months.

>**signals**  
transformative · essential · thrilled

>**dynamics**  
immersed mode · advancing motion · intrinsic source

## selected next achievement
    [mvp-gaps] identify the 3 most important gaps still missing from the current workspace

**ease-start**  
Write a list: what does the workspace do well today, and what still breaks — where does friction appear that the system should be absorbing but isn't. 10 minutes, no structure needed.

**findings so far (2026-07-20, from freewrite via INBOX)** — 2 of the 3 gaps:
1. overengineering smell somewhere in the workspace — not yet localized, needs a pass to find where
2. workspace/git feels messy — suspected redundant/conflicting `.md` files scattered around. Overlaps with existing [enforce-standards] backlog item but is a distinct *feeling* worth chasing concretely (which files, where)
3rd gap still open.

>**timing**  
*target · first validated version in ~6 months (around November 2026)  
anchor · none external  
closure · using the system daily without friction, all domains covered, trust established  
tolerance · timeline is aspirational — what matters is direction, not date  
fallback · iterate — MVP can always be extended*

## backlog

> [ ] [mvp-gaps] identify the 3 most important gaps still missing from the current workspace  
> [ ] [todo-integration] establish TODO.md as consistent daily practice  
> [ ] [compass-cadence] run compass review on a regular rhythm — at least 2x/month  
> [ ] [brain-full-files] all GOALS.md stubs have actual goal files  
> [ ] [branches-coverage] branches/ covers all active life domains  
> [ ] [mvp-validate] use system daily for 30 days, assess: does it reduce mental load?  
> [ ] [gdrive-integration] define strategy to bring Google Drive into workspace — link, sync, or selective copy  
> [ ] [courses-import] bring course materials into workspace — define folder structure and import strategy  
> [ ] [todo-accountability] design accountability layer for TODO.md — calendar reminders, daily review, or notification hook so tasks don't silently expire  
> [ ] [gcal-link] link workspace to Google Calendar — deadlines and events visible in context  
> [x] [gmail-link] link workspace to Gmail — surface relevant emails as context for goals and tasks  
> [ ] [whatsapp-inbox-bot] WhatsApp bot as continuous-capture front door — superseded by [telegram-link], which shipped the same capture behavior via the much lower-friction Telegram Bot API. Revisit only if Telegram proves insufficient.  
> [x] [telegram-link] connect workspace to Telegram — bot or channel for daily nudges (easier bot API than WhatsApp; fallback if WhatsApp Cloud API friction too high)  
> [ ] [remote-session-control] Phase 1 (claude backend) SHIPPED 2026-07-20 — `telegram_daemon.py` dispatches `/sessions /new /c /use /status /stop /latest /notify` to control Claude Code sessions via the CLI binary bundled in the VSCode extension (`~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude`, version-agnostic glob, PATH override checked first). Plain text still → INBOX unchanged (explicit `/`-prefix, no ambiguity with capture). **Cost model, learned live**: every `-p --resume` call is a real inference call (~$0.11 for a trivial cold-cache reply) — no way around that for a genuinely new turn. Split the design in two so nothing spends by accident: read-only commands (`/sessions`, `/latest [N]`, `/notify`) are pure reads of the transcript files every session already writes to `~/.claude/projects/-mnt-workspace/*.jsonl` — **$0**, confirmed live (`/latest` correctly pulled real session text from disk with zero API calls). `/notify on` (default off) polls those files every 20s and free-pushes any finished turn from *any* local session — interactive VSCode included, not just bot-dispatched — to Telegram; replying to any bot message (push or command reply) continues that exact session via `/c`-equivalent, no `/use` needed. Only `/new`, `/c`, and replies trigger real spend, and always as a deliberate action. Added `_safe_reply` (2-attempt retry) + this note after a live network-timeout on `/sessions` turned out to be a transient Telegram-API blip during daemon restart, not a logic bug — daemon stayed up, reply just silently dropped since no error handler was registered before this fix. **Open**: Lucas still needs to live-test `/new`, `/use`, `/c`, `/status`, `/stop`, `/notify on` + reply-to-continue end-to-end via the paired phone. Phase 2 (opencode, already on PATH: `opencode run -s <id> --format json`) and Phase 3 (copilot — **now installed + logged in** by Lucas 2026-07-20; flags `-p`, `-r/--resume[=ID]`, `--session-id`, `-s`) not started — same dispatch + free-read pattern reusable. Full design: plan mode session 2026-07-20 (superseded — this entry is canonical).  
> [ ] [aiwbot] PROVIDER-AGNOSTIC REBUILD — new project `code/aiwbot/` (own git repo, gitflow, currently on `develop`; named after the @lsfaiwbot handle). **Why the pivot** (research 2026-07-21): the bot control-of-sessions problem is solved *natively and better* by two official Anthropic features — **Remote Control** (`claude --remote-control`/`/rc`: one local session mirrored real-time across terminal+phone+web, the "Google Doc" dream, zero code) and **Channels** (`/plugin install telegram@claude-plugins-official`: official Telegram bridge pushing DMs into the one open session, with native `reply`/`react`/`edit_message` tools — already does the threading/working-edit UX we hand-built). BUT both lock 100% into Claude Code → rejected per [[feedback_provider_agnostic_naming]] ("não quero ser refém do claude code"). Landscape: 3 architecture patterns — A. CLI-wrapper (our old bot: fork/divergence), B. Agent-SDK single-process (linuz90/claude-telegram-bot 451★, MIT — its whole Anthropic coupling is ONE `session.ts` `query()` call; frames Claude Code as a personal-assistant-pointed-at-a-CLAUDE.md-folder = our brain concept; closest reference), C. official session-native (Remote Control/Channels, lock-in). Community leaders: RichardAtCT/claude-code-telegram 2735★, grinev/opencode-telegram-bot 946★. **Chosen direction**: Padrão B with a swappable backend seam, Python, reusing the old bot's provider-agnostic plumbing — providers = interchangeable data. **Phase A SHIPPED + PROVEN live 2026-07-21**: `AgentBackend.send()→AsyncIterator[AgentEvent]` seam, `CliBackend` holds the subprocess loop once, `claude`+`opencode` backends pass end-to-end with single-lineage resume (`make smoke`), 6 free fixture tests (`make test`). **AD-3 (key finding)**: claude forks a new session id per turn (`--fork-session` mandatory — registered agents refuse plain --resume), opencode keeps the same id (`-s`); frontend must chase `result.session_id` uniformly. **Next = Phase B**: Telegram frontend on the seam, reusing old-bot plumbing (INBOX $0 capture, allowlist, reply_map, md→TG-HTML). Read `code/aiwbot/ROADMAP.md` + `SPECS.md` before continuing. The old bot ([remote-session-control]/[bot-conversational-ux]) stays committed (workspace `468ad0e`) as the running INBOX-capture bot + reuse source; its conversational-UX rewrite is superseded by this rebuild.  
> [ ] [bot-conversational-ux] make the Telegram bot feel more natural/conversational (INBOX 2026-07-20, Lucas's own words, sent live via the bot mid-session): "captured" replies aren't threaded to the message they captured; ack phrasing is a single robotic word, wants ~10 natural 2-5-word variations; `/latest` output format unclear how to interact with; typing session ids by hand feels painful; wants the whole bot in PT-BR. **Partial fix already shipped same session** (2026-07-20, see [remote-session-control] below) — reply-to-any-bot-message now continues that session, so the "painful id typing" complaint may already be resolved pending Lucas's live test. Still open: thread `"captured"` as an actual reply to the source message (currently a separate message), phrase variety bank (~10 variations, PT-BR), clarify `/latest`'s read-only nature in its own reply copy, full PT-BR pass across all bot strings. Lucas explicitly asked for assessment + brainstorm + plan — do that at the start of next session before coding, in `core/tools/telegram_daemon.py`.  
**Plan (finalized 2026-07-20-c, ready to code — supersedes 2026-07-20-b)** — full redesign from a live back-and-forth with Lucas, not just string tweaks. Root cause of "not threaded": `_safe_reply` calls `msg.reply_text(text)` with no `do_quote`; PTB doesn't auto-quote in private chats. Everything below builds on that fix.

**Final command surface**: `/new`, `/select`, `/notify`, `/stop`, `/help` (`/sessions`, `/latest`, `/use`, `/c` all retired — folded into `/select` or replaced by reply-to-continue). `/status` untouched, out of scope, kept as a manual diagnostic escape hatch.

1. **`_safe_reply` → `do_quote=True`** (foundation — every message below depends on real Telegram threading working).
2. **Header formatter (shared util)** — every session-originated message gets `[XXX] TÍTULO\n<corpo>`: `XXX` = first 3 hex chars of session id, uppercase, **cosmetic only** — real resolution always via full id (button `callback_data` or existing `_resolve_session` prefix-match for typed fallback), so a display collision at 3 chars is harmless. `TÍTULO` = first 3 words of the session's `name` from `claude agents --json`, uppercased; falls back to `(SEM TÍTULO)` if `name` is empty. Same util also converts the body: markdown pipe-tables (Telegram renders zero table syntax, no parse_mode fixes that) → monospace `<pre>` block via `parse_mode="HTML"`; other basic markdown (`**bold**`, `` `code` ``) converted to HTML tags too, same code path.
3. **`/new`** — replace the single 1.5s-sleep-then-diff with a poll at **t = 2s, 5s, 10s, 30s, 60s** since dispatch (elapsed-since-dispatch checkpoints, early-exit on first match), diffing `claude agents --json` each time; only says "couldn't confirm" after the 60s check fails too.
4. **`/select`** (merges old `/use` + `/latest`) — no-arg or `/select N`: inline keyboard (`InlineKeyboardMarkup` + `CallbackQueryHandler`) listing sessions, each button label `[XXX] TÍTULO — <10 primeiras palavras> … <10 últimas palavras>` of that session's last response (reuse `_last_assistant_text`). Tapping a button → bot sends the full header + full last-response text as its own message, registers it in `reply_map`, **and sets that session as focused**. Typed fallback (`/select <id-prefix>`) still resolves directly via existing `_resolve_session`, no picker needed.
5. **Reply-to-continue also auto-focuses** — `_handle_reply_continue` currently only continues the target session; add the same `telegram_config.save_config(claude_focused_session=sid)` `/select` does. This is what lets `/c` disappear entirely: every session that ever spoke through the bot (via `/new`, `/select` tap, `/notify` push) already has a taggable message to reply to.
6. **Drop `/c`, `/use`, `/sessions`, `/latest`** from the `handlers` dict — replaced by `/select` + reply-only continuation per above.
7. **`/notify`** — apply the new header format to pushed messages (currently `f"— {sid[:8]} —\n{snippet}"`, becomes the shared header util), still registers `reply_map` so replying to a push works same as any other session message. Behavior otherwise unchanged: any bot-dispatched prompt (`/new`, reply-continue) **always** gets its answer back in Telegram as a real threaded reply, regardless of `/notify` on/off — `/notify` only covers unprompted pushes from sessions nobody asked via the bot.
8. **Capture ack** — fixed single phrase, no rotation: `"Guardado em brain/INBOX.md."` (mentions the actual file, per Lucas: skip the "dubbed movie line" phrase-bank idea entirely).
9. **`/help`** — new command, PT-BR: lists `/new /select /notify /stop /help` with one-line natural-language descriptions each, plus explains that any plain text/photo/voice/document sent without `/` goes straight to `brain/INBOX.md`.
10. **Telegram native `/`-autocomplete** — `app.bot.set_my_commands([...])` in `_post_init`, registers the 5 commands + short descriptions so Telegram's own UI shows them on typing `/`.
11. **`/stop`** — stays exactly as a standalone command (Lucas confirmed: no picker button, keep it simple), just gets PT-BR copy.
12. **Full PT-BR pass** on everything remaining (`/new`, `/select`, `/notify`, `/stop`, `/help`, `unknown command`, `error:`, `⏳ working…` → `⏳ trabalhando…`) — do last so earlier steps don't need re-touching strings twice.

Build + verify in the order above, live-testing each numbered step via the paired phone before moving to the next — bot has no test harness, manual smoke test is the verification contract per [remote-session-control].  
> [ ] [skill-collapse] collapse brain skills to just /inbox + /compass — fold brain-finished into /compass (mark-done + advance is a compass move). Two verbs, fits entry-point principle.  
> [ ] [inbox-refresh-goals] /inbox runs the goals-sync refresh (brain_stats.py) as its last step, not only on commit — dashboard never goes stale between commits.  
> [ ] [compass-on-inbox] /inbox offers to run /compass, but only when it detects a trigger (an anchor crossed <3 weeks, or a goal flipped to stalled) — cheap capture stays cheap; compass fires on signal, never auto every call.  
> [ ] [goal-routing-populate] populate the new per-goal `>**routing**` tier·effort field (spec in brain/SPECS.md, vocab shared with core/skills/prepare.md) and wire the router/prepare to read it.  
> [ ] [entry-point] entry-point principle: workspace must ease communication/entry — never require Lucas to remember what exists (discoverability via skills, nudges, routing)  
> [ ] [roadmap-entrypoint] cada projeto = 1 único entrypoint de roadmap; auditar padrões (workspace cresceu)  
> [ ] [enforce-standards] enforcement não-ignorável: nomes/pastas/repos/gitflow, wiring de hooks + wiring paper↔code, uso de skills, fluxo inbox→todo→goals, anti-scattering  
> [x] [goals-sync] FIXED 2026-07-11 — .hooks/brain_stats.py existia mas quebrado: `Path("Brain")` + hook grep `^Brain/goals/` vs dir real `brain/` (case mismatch Linux) → nunca rodava; + parser de título só aceitava header 2-campos, ignorando os 3-campos canônicos → tabela active-goals mostrava 1 de 50. Ambos corrigidos, dashboard atualiza. Falta: wiring no /inbox (ver [inbox-refresh-goals]).  
> [ ] [provider-fallback] mitigar instabilidade do opencode via configs do workspace — skills/hooks/.md provider-agnostic + chaveamento de provider (openrouter → chave nvidia quando créditos acabarem)  
> [ ] [nested-gitlink-gate] pre-commit gate que BLOQUEIA gitlinks (mode 160000) não declarados em .gitmodules — `git add -A` no workspace repo embutiu 10 projetos com .git próprio (academy/papers/*, branches/*, code/*) como gitlinks quebrados; exigiu git rm --cached + amend pre-push (2026-07-11)  
> [ ] [stats-split-or-exempt] .hooks/brain_stats.py tem 392 linhas (> BLOCK_LINES=200 do pre-edit gate) → Edit recusa net-zero edits, só Bash contorna. Decidir: splitar em parse/stats/dashboard/done-log OU isentar .hooks/ do gate (2026-07-11 compass)  
> [ ] [anti-capital-case] gate anti-capital-case em nomes de dir de topo (mesmo padrão Models/ ressurgindo; ComfyUI suspeito); suspeita de sessão que recria dirs capital-case (2026-07-11)  
> [ ] [pre-edit-silent-fail] pre-edit.py falha SILENCIOSA ("No stderr output") em Write de arquivos novos em certos paths (scratchpad .html, test/*.py novo em isoroll-content) — bloqueia Write sem dizer por quê; workaround = heredoc via Bash. Investigar crash do hook (provável exceção não tratada em path fora do esperado) (2026-07-16)  

## done

<!-- done:start -->
> [x] [gmail-link] `core/tools/gmail` + `core/skills/gmail-triage.md` — read-only Gmail across 3 accounts, routes to INBOX/TODO/goals/drafts/attachments. Pending: Google Cloud OAuth setup by Lucas.
> [x] [telegram-link] `core/tools/telegram` (CLI: init/send/status) + `core/tools/telegram_daemon.py` (systemd --user service `workspace-telegram-bot`, auto-restart) — bot @lsfaiwbot. Outbound: `telegram send <text>` for nudges (content/cadence still to design — this ships the transport). Inbound: text/photo/voice/document from the paired chat_id append directly to brain/INBOX.md (no confirmation gate — single trusted sender, unlike gmail's AI-triage flow); attachments saved to brain/attachments/YYYY-MM/. Voice notes saved untranscribed for now (2026-07-20).
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-14  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       4 |
| trimester   |       5 |
| semester    |       5 |
| year        |       5 |
| 2-year      |       5 |
| 4-year      |       5 |
<!-- stats:end -->
