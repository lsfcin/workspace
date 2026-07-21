# to do
> practical layer. tasks for today, week, month. each may link to a goal achievement — or not.  
> fill freely. clear when done. agent and Lucas both write here.

---

## today

- [x] [workspace-os / mvp-gaps] 10-min freewrite: what works, what still breaks
- [ ] sleep by 00:30 — streak-3 starts tonight

## tomorrow

- [x] [sibgrapi / sib-01] message Artur → get corrected dataset link
- [x] [sibgrapi / sib-02–04] rerun metrics, update paper text + figures
- [ ] [sibgrapi / sib-05–06] adjust figures
- [ ] [sibgrapi / sib-05–06] manual review → give Artur ok to submit

## programacao1 — simulador social

- [ ] criar repo GitHub `lsfcin/programacao1-simulador` (novo, separado de `programming-101`)
- [ ] `git init` em `code/programacao1/` + git flow (main → develop)
- [ ] começar coding: `src/setup.py` + `src/qualidade.py` (Milestone 1 no ROADMAP.md)

## week

- [ ] revisar artigo do svr — prazo ~25/07
- [ ] falar com Paulo e Maigan sobre as férias (amarrado ao retiro vipassana 1–12 ago)
- [ ] [banca] fechar procedimentos da banca de Artur
- [ ] responder megatruth
- [ ] [finances] pedir mudança da data de pagamento do aluguel: dia 5 → dia 10
- [ ] [ufrpe] PDA — plano de desenvolvimento (Lenina cobrou); é simples, fazer logo
- [ ] [pandeiro / show-up] confirm Pandeirada time, show up Saturday
- [ ] [sleep / streak-3] 3 consecutive nights in bed by 00:30
- [ ] [brain] set up mobile inbox access for Android — recover 2 app options from prior Claude conversation, pick one for Xiaomi Redmi Note 10 Pro
- [ ] check IC scholarship deadline at UFRPE — recent edital closing soon, open application if still open
- [ ] [workspace-os / todo-accountability] design TODO accountability layer — what would make you actually check it daily?

## month

- [ ] [cnpq] submeter proposta chamada UNIVERSAL — **deadline 03/08** (https://www.gov.br/cnpq/pt-br/assuntos/noticias/cnpq-em-acao/chamada-universal-vai-financiar-r-300-milhoes-em-projetos-de-pesquisa-em-todo-pais-inscricoes-vao-ate-03-08)
- [ ] [casinhas] averbação do terreno
- [ ] [vipassana] retiro 1–12 agosto; mover férias (ver goal vipassana)
- [ ] [ufrpe] ajudar Paulo (coordenador) a montar o PPC — atualizar formato da lista de ementas, com IA
- [ ] [slides / portas-logicas] OR gate body still missing — see KNOWN-BUGS.md; investigate `CUSTOM` shape type in slide 23 group, then decide if worth further debugging
- [ ] standardize workspace folder names to lowercase — update on Ubuntu and Windows
- [ ] fix downloads folder — some programs bypassing workspace path, still writing to ~/Downloads by default
- [ ] set up shared Downloads folder across smartphone + both computers, unify all apps/configs to /mnt/workspace/Downloads/
- [ ] [workspace] remove duplicate Models/ dir (capital-M); keep only models/ lowercase
- [ ] [workspace-os] split large `.md` files into smaller ones — SETUP.md flagged as example (INBOX 2026-07-20, via telegram); related to existing file-trees backlog item above but distinct scope (splitting big docs vs. converting specific docs to trees)

## drive migration (cin → local workspace)

> scaffold done. download each folder, then triage loose/Unorganized items.

### academy/
- [ ] cv/ ← Professional/Curriculo/
- [ ] talks/ ← Professional/Geral/Talks/
- [ ] classes/programacao-1/_material ← UFRPE/Disciplinas/P1/
- [ ] classes/programacao-2/_material ← UFRPE/Disciplinas/P2/
- [ ] classes/projeto-interdisciplinar-1/_material ← UFRPE/Disciplinas/PI1/
- [ ] classes/projeto-interdisciplinar-2/_material ← UFRPE/Disciplinas/PI2/
- [ ] classes/projeto-interdisciplinar-3/_material ← UFRPE/Disciplinas/PI3/
- [ ] classes/inteligencia-artificial/_material ← UFRPE/Disciplinas/IA/
- [ ] classes/computacao-grafica/_material ← UFRPE/Disciplinas/Computacao Grafica/
- [ ] classes/motores-graficos/_material ← UFRPE/Disciplinas/Motores Graficos/
- [ ] classes/gerencia-de-projetos/_material ← UFRPE/Disciplinas/PGP/
- [ ] classes/ai4good/_material ← UFRPE/Disciplinas/AI4Good/
- [ ] classes/tecnologias-na-educacao/_material ← UFRPE/Disciplinas/Tec. na Educacao/
- [ ] classes/intro-informatica/_material ← UFRPE/Disciplinas/Intro a Informatica/
- [ ] students/active/ + students/past/ ← Professional/Alunos/ (classify first)
- [ ] lab/neoeduc/ ← UFRPE/Projetos/NeoEduc/
- [ ] lab/ai-dungeon-master/ ← UFRPE/Projetos/AI Dungeon Master/
- [ ] lab/bancas/ ← 3 loose Banca PDFs in UFRPE/ (Antonio, AIDungeonMaster, NeoEduc)
- [ ] administration/comissoes/ ← UFRPE/Comissoes/
- [ ] administration/coordenacao-lc/ ← UFRPE/Coordenacao de LC/ (Drive side)
- [ ] administration/pe-de-meia/ ← UFRPE/Pe de Meia/
- [ ] administration/cpesq/ ← UFRPE/CPESQ/
- [ ] administration/burocracia/ ← UFRPE/Burocracia/ + loose UFRPE docs (regulamentos, PPC, planos)

### branches/
- [ ] health/ ← Personal/Saude/
- [ ] music/ ← Personal/Musicas/
- [ ] rpg/ ← Personal/RPG/
- [ ] bureaucracy/ ← Personal/Bureaucracy/
- [ ] writing/drafts/ ← Personal/Escritos/
- [ ] writing/notes/ ← Personal/Notes/

### triage (do last)
- [ ] Unorganized/ folder — route each item to correct local destination
- [ ] loose root files — pessoas.csv, figuras pptx, old 2016 docs, recovery codes

---

## backlog

- [ ] [workspace-os] TODO: anotar modelo/tier recomendado por tarefa + rastrear datas de criação/atribuição p/ flagrar tarefas paradas
- [ ] [workspace-os] SPECS.md / KNOWN-BUGS.md / ROADMAP.md como file-trees em vez de arquivo único
- [ ] [workspace-os] fix stubgen p/ TODOS os projetos — `.py` criados fora de Edit/Write não geram `.pyi` (pre-commit sweep?) — INBOX
- [ ] [workspace-os] detecção de alto acoplamento / import-graph — pilotar em isoroll → política workspace-wide (discutir antes)
- [ ] [workspace-os] policy: conectar CONTEXT.md de cada projeto ao seu goal file — formato `> goal: [slug](../../brain/goals/<slug>.md)` na linha 3; backfill ~15 projetos PRIMEIRO, depois enforce via post-edit hook (warn→block); dobra não tem goal (criar ou `> goal: none`); reverse link `> project:` no goal file opcional
- [ ] [workspace-os] context_synchronizer: pular CONTEXT.md com `## Routing` manual sem sentinelas — hoje ANEXA um bloco duplicado (bug); fix robusto protege CONTEXT hand-curados. brain/CONTEXT.md já convertido p/ markers nesta sessão
- [ ] [workspace-os] triggers pós-janela de limites do Claude — always-on aproveitando limites diário/semanal. `ScheduleWakeup` (dynamic /loop) já cobre parcialmente dentro de uma sessão viva — falta o caso "sessão morreu, limite renovou, ninguém acorda o agente"
- [ ] [workspace-os] monitor de tamanho de sessão (hook avisa ~40%/50% p/ avaliar handoff) — roundup + inbox-nudge já feitos; falta o %-monitor; 80% propenso a descartar — discutir
- [ ] [workspace-os] detecção de drift de contexto — recall-probe objetivo (plantar fato verificável cedo, re-checar periodicamente) + amarrar ao %-monitor. Ideia do "canary me-chama-de-Lucas" é proxy fraco/confundido (caveman suprime, sinal baixo, auto-reportado) — manter só como tell passivo grátis, não construir infra em cima
- [ ] [code] novo projeto: gerador de animações (claude-code + remotion) — separado do shortvid
- [x] [workspace-os] integrações: telegram — DONE 2026-07-20, `core/tools/telegram` + `telegram_daemon.py`, ver workspace-os.md. Whatsapp superseded por telegram (não faz mais sentido separado)
- [x] [slides] setup Slidev + Vue locally — Slidev 52.16.0, Node 24.16.0 ✓
- [x] [slides] build `core/tools/slides` CLI (new, serve, build, port from Google Slides JSON)
- [x] [slides] conversor Google Slides API JSON → Slidev `.md` — `core/tools/slides_port.py`
- [ ] [slides] templates base: aula, talk acadêmico, projeto
- [ ] [workspace-os] habilitar Google Slides API no GCP project 1048141740528 (mesmo projeto drive/calendar)
- [ ] [workspace-os] symlinks `.claude/commands/drive.md` e `calendar.md` — commit ainda pendente
- [ ] [sipac] assinar 2 documentos no SIPAC Portal Admin → Protocolo → Assinar Documento (pendente desde 11/06)
- [ ] [docusign] assinar contrato de estágio Natalie Santos / Netcon Americas
- [ ] [sbc-cotas] checar isenção e prazos — email andreza.leite@ufrpe.br
