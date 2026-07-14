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
> [ ] [whatsapp-inbox-bot] WhatsApp bot as continuous-capture front door: forward a msg/photo/audio/PDF → bot appends (or lightly pre-triages) it into brain/INBOX.md, so life-updates flow in without a dedicated session. Path: WhatsApp Cloud API (Meta) or self-host (Baileys/whatsapp-web.js) → webhook → writes to INBOX. Voice notes = biggest win (transcribe). Supersedes/absorbs [whatsapp-link].  
> [ ] [telegram-link] connect workspace to Telegram — bot or channel for daily nudges (easier bot API than WhatsApp; fallback if WhatsApp Cloud API friction too high)  
> [ ] [skill-collapse] collapse brain skills to just /inbox + /compass — fold brain-finished into /compass (mark-done + advance is a compass move). Two verbs, fits entry-point principle.  
> [ ] [inbox-refresh-goals] /inbox runs the goals-sync refresh (brain_stats.py) as its last step, not only on commit — dashboard never goes stale between commits.  
> [ ] [compass-on-inbox] /inbox offers to run /compass, but only when it detects a trigger (an anchor crossed <3 weeks, or a goal flipped to stalled) — cheap capture stays cheap; compass fires on signal, never auto every call.  
> [ ] [goal-routing-populate] populate the new per-goal `>**routing**` tier·effort field (spec in brain/SPECS.md, vocab shared with core/skills/prepare.md) and wire the router/prepare to read it.  
> [ ] [entry-point] entry-point principle: workspace must ease communication/entry — never require Lucas to remember what exists (discoverability via skills, nudges, routing)  
> [ ] [roadmap-entrypoint] cada projeto = 1 único entrypoint de roadmap; auditar padrões (workspace cresceu)  
> [ ] [enforce-standards] enforcement não-ignorável: nomes/pastas/repos/gitflow, wiring de hooks + wiring paper↔code, uso de skills, fluxo inbox→todo→goals, anti-scattering  
> [x] [goals-sync] FIXED 2026-07-11 — .hooks/brain_stats.py existia mas quebrado: `Path("Brain")` + hook grep `^Brain/goals/` vs dir real `brain/` (case mismatch Linux) → nunca rodava; + parser de título só aceitava header 2-campos, ignorando os 3-campos canônicos → tabela active-goals mostrava 1 de 50. Ambos corrigidos, dashboard atualiza. Falta: wiring no /inbox (ver [inbox-refresh-goals]).  
> [ ] [provider-fallback] mitigar instabilidade do opencode via configs do workspace — skills/hooks/.md provider-agnostic + chaveamento de provider (openrouter → chave nvidia quando créditos acabarem)  

## done

<!-- done:start -->
> [x] [gmail-link] `core/tools/gmail` + `core/skills/gmail-triage.md` — read-only Gmail across 3 accounts, routes to INBOX/TODO/goals/drafts/attachments. Pending: Google Cloud OAuth setup by Lucas.
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-11  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       4 |
| trimester   |       4 |
| semester    |       4 |
| year        |       4 |
| 2-year      |       4 |
| 4-year      |       4 |
<!-- stats:end -->
