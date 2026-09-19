# [ craft | workspace | year ] workspace OS

A centralized personal operating system: all thoughts, projects, demands, full-life organization in one place. Automated setup that eases how life gets managed, reduces mental pressure, and enables goals and dreams to move from idea to action. Reliable, productive, and genuinely used — not just designed. Currently in MVP prototyping phase. First validated version expected in ~6 months.

>**signals**  
transformative · essential · thrilled

>**owns**  
`core` · `ROADMAP.md` · `SETUP.md` · `AGENTS.md` · `verify.py` · `ISSUES.md`

>**dynamics**  
immersed mode · advancing motion · intrinsic source  
2026-08-13 compass: **confirmed #1 for a second cycle, and the numbers back it — 29 of 29 workspace commits in 14 days landed here.** The gate held honest under all of it: criterion 3 went *backwards* on purpose when a re-audit across 25 repos found three remotes missing, rather than staying a green tick that was false. What is left is not build — it is **one decision and one mechanical front**. This is a finish.

## selected next achievement
    [v1] pass the four-criterion v1 gate — Tier 0 anti-entropy live · one list, no duplicates · everything pushed and
    gitflow-shaped · clonable by a student

**All build work lives in [/ROADMAP.md](../../ROADMAP.md)** — the single wos list, each step tagged with model level and impact flag. This file holds only why, signals, dynamics, and timing. Plans do not live in goal files (AGENTS.md).

> **The governing constraint, Lucas 2026-08-16:** *"definitivamente, quero zerar o roadmap do WOS o quanto antes. já usamos demasiado tempo e esforço na infraestrutura."*
>
> This outranks completeness. It is not a request to work faster — it is a filter on what may be in the list at all. Three consequences, in the order they bite: **an item that another repo owns is refiled there, not held here**; **an item that does not gate v1 is a candidate for the Rejected list, not the backlog**; and a finding worth keeping goes into the `SPECS.md` or `SCHEMA.md` section that owns the rule, because writing the rule there is what closing an item *is*. The repo is a means. Time spent on it past v1 is time not spent on the work it exists to serve.
>
> **Sharpened 2026-08-25, and this is the version to read first.** Lucas: *"semanas completas estourando o uso do claude code com o opus 5 para um progresso duvidoso… realmente vejo que o WOS virou um problema por si só."* The measurement backs the feeling: 50 commits in 30 days, nearly all in `core/` and the roadmaps, **zero in `code/`**. The repo spent the month maintaining itself.
>
> **What v1.0 means from here, in his words:** zero loose ends · minimum coupling · hooks and tools working as advertised on zero-token strategies · small `.md` files · roadmaps small enough that a sibling file is an exception. **Agents, flows and loops wait**; v1 is the `AGENTS.md`/`CONTEXT.md` tree, hooks, tools and `brain/`.
>
> **The two rules he gave that change how sessions write:** a roadmap item carries *what*, *why* and *the verification*, and **never the how** — that is the job of the session that takes the item, and writing it here is what made the roadmaps long and stale at once. And *"LLMs are good at writing even when it isn't useful"*, so length is never evidence of care.
>
> **How the work gets pulled, Lucas 2026-08-27:** *"a partir de cada demanda da vida resolver não somente a demanda mas toda a infraestrutura relacionada a ela e assim seguimos progredindo no micro e no macro."* A real demand is what opens a session; the repo it touches is fixed in the same pass. Nothing here is worked for its own sake.
>
> **Two things he ruled are NOT on the table**, both because they cut capability rather than fat:
> deleting a harness (multi-harness is essential — optimise the copy, never the function) and cutting any hook before a scoreboard of what it actually blocked exists.

**ease-start**  
**All four v1 criteria are green, and nothing in the list is waiting on you.** The drain is agent work now: the remaining items carry their own model level and none of them is blocked on a decision.
So the easy start is not a decision to make — it is a session to hand off.

Two items do want you, and both are **conversations to schedule, not questions to answer in five minutes** (you said so yourself on 2026-08-17, in both cases): giving flows and agents a fair trial before judging them, and the knowledge graph, which is its own front and needs research plus a design sitting. Neither belongs at the end of a drain session. Put one on the calendar; do not squeeze it.

The genuinely free move, when you want the number to fall without spending judgment: open [/ROADMAP.md](../../ROADMAP.md), take the mechanical items, and hand them to a sonnet session. The list's length is the measure, and those items shorten it without you in the loop.

**Known risk — dataset with no live backup:** `datasets/relativistic_raytracer` (5.8 GB) is the sole surviving copy of its data — Zenodo record 20240662 returns HTTP 410 ("personal-data"), gone since 2026-05-24. The `datasets/*/CONTEXT.md` convention of "re-download from the Zenodo link" breaks whenever the link goes dead with no live copy behind it.

**Root read**: ordering by motivation wins over deadline pressure — the gentle-resurfacing rhythm that capture alone couldn't provide now lives in `/compass`.

>**timing**  
*target · first validated version in ~6 months (around November 2026)  
anchor · none external  
closure · using the system daily without friction, all domains covered, trust established  
tolerance · timeline is aspirational — what matters is direction, not date  
fallback · iterate — MVP can always be extended*

## backlog

> [ ] [v1] the four-criterion gate — see [/ROADMAP.md](../../ROADMAP.md)  
> [ ] [mvp-validate] use the system daily for 30 days, then assess: does it reduce mental load? By definition post-v1 —
> this is the achievement v1 exists to make measurable  
> [ ] [daily-use] the practical layer actually gets used — TODO redesign, dashboard freshness, mobile capture (ROADMAP § The list discipline)  
> [ ] [domain-coverage] `branches/` covers all active life domains and every `GOALS.md` stub has a real goal file (ROADMAP § the .md type system)  
> [ ] [content-in] course materials and Google Drive brought in under a decided strategy (ROADMAP § Parked, until v1)  
> [ ] [offline-resilient] survives a world without internet — Reticulum for network, Kiwix for corpus (parked, ROADMAP § Parked)  
> [ ] [checkup-metodo] checkup de rotina do workspace (INBOX 2026-07-30) — rodar `core/tools/test/verify-fast`, ler `ISSUES.md` § Entropy (a contagem, nunca uma cópia), e auditar os 4 critérios de v1 no `/ROADMAP.md` contra o que é verdade hoje; o que virar trabalho vira item de lá, não daqui. E precisa de método: *"testar as nossas features do wos… uma forma válida de fazer isso"* — usar as features de verdade, não só verificar que passam  
> [ ] [fable-credito] confirmar se o crédito Fable (100 usd até setembro) ainda consome do limite por turno/semanal, ou se é isento (INBOX 2026-07-24)  
> [ ] [plan-mode-default] deixar o plan mode como default de sessão nova na extensão VSCode do Claude Code (INBOX 2026-08-16) — config do harness, não do workspace: checar se há setting em `.claude/settings.json` ou se é só na UI da extensão; se for setting, é one-liner e a skill `update-config` cobre. Casa com a mudança do `/roundup`, que agora fecha pedindo *plan*, não *continue*  
> [ ] [security-gates] decidir quais dos 20 itens da checklist pré-lançamento viram gate de verdade para os projetos que vão pro ar (gira, voti, ppc) — vários já cobertos (secret-scan no pre-commit, skill `security-review`); o que sobra é auth server-side, RLS, rate-limit e headers, que nenhum gate nosso vê. Ref em `core/refs/REFS.md`, na linha sobre shipping de app escrito por agente (INBOX 2026-08-13)  
> [ ] [jcode-custo] o JCode (harness do Claude Code reescrito em Rust) levanta duas perguntas, e a segunda vale mais:
> a ferramenta presta, e **é o harness que deixa caro ou é o modelo?** A segunda se mede aqui sem instalar nada —
> tokens de scaffolding vs tokens de conteúdo numa sessão nossa. Responder junto com *"vale usar rust em vez de python"* nas nossas `core/tools/`, que é a mesma medição. Ref em `core/refs/REFS.md`  
> [ ] [zcode-trust] aceitar o trust do workspace no ZCode (Settings, ou o prompt ao abrir /mnt/workspace) — **só o Lucas pode**; sem isso os hooks do shim ficam inertes. Depois abrir sessão nova e re-rodar a sonda de `core/experiments/zcode-hook-protocol.md`, que decide se o registro direto fica ou vira adaptador (INBOX 2026-08-21)  
> [ ] [zero-sum-linhas] avaliar gate de orçamento zero-sum no WOS: nenhum commit adiciona linhas sem que diminua de outro canto — é viável medir e impor? (INBOX 2026-09-05)  
> [ ] [ferramentas-obsoletas] de tempos em tempos, checar se alguma ferramenta nossa deve ser atualizada ou abandonada porque os modelos e harnesses melhoraram — o WOS existe para contornar fraquezas do modelo, então cada fraqueza corrigida upstream é código nosso que virou peso morto. Mesmo raciocínio do estudo de ablação, em cadência menor (INBOX 2026-08-21)  
> [ ] [mutation-testing] quebrar de propósito um teste que passa e ver se a suíte fica verde — se ficar, o teste não tem dente. Vale rodar como auditoria da nossa suíte inteira, não como gate: o bug do `line_counts.py` (ISSUES § Open)
> passou justamente por ter teste sem dente. Ref em `core/refs/REFS.md` (INBOX 2026-09-10)  
> [ ] [extracao-bloqueada] **resolvido em 2026-09-17, e o que sobra é o alarme.** O jar de cookies tinha os dez cookies anônimos do Instagram e **nenhum `sessionid`**, então reel público passava (metadata anônima) e post `/p/` caía em `/accounts/login/` — o que fez a falha parecer seletiva e não parecer auth por três triagens, custando 8 entradas em 14/09 e 12 em 17/09. Reexportar do Brave trouxe o `sessionid` e as 12 leram na hora. Falta a lição:
> `video` reporta jar inútil como `(no text extracted)`, igual a um post sem texto. Fazer o tool **checar o `sessionid` e dizer o nome da falha**; o teste é `awk -F'\t' '$6=="sessionid"' ~/.config/workspace-video/cookies.txt` vir vazio. Avaliar o Fortress só depois disso; ref em `core/refs/REFS.md`  
> [ ] [ocr-lixo-nao-e-texto] **o mesmo buraco da parada precoce, um nível abaixo, achado ao OCRar os 24 links de 17/09.** Em carrossel de design pesado o tesseract devolve só título e marca d'água — `[2/8] @ Autopilot` sete vezes, `A/ Bnalytics` — e o `auto` trata isso como texto encontrado, então **nunca escala pro VLM**, que é justamente quem leria aquele slide. O corpo do post fica invisível com a escada inteira verde. Decidir o critério de "texto de verdade" (o mesmo nome repetido em todo slide não é conteúdo) e escalar quando ele não for atingido  
> [ ] [skills-externas] avaliar `mattpocock/skills` — skills pequenas, componíveis, model-agnostic, em plugin ou em cópia editável. Pesar contra a regra que já rejeitou `obra/Superpowers` (sem roteamento de nível por tarefa): a pergunta é se essas trazem o que faltava lá, ou se de novo só o trigger vale ser importado. Ref em `core/refs/REFS.md` (INBOX 2026-09-10)  
> [ ] [eli5-explicador] avaliar a skill ELI5 — documento vira explicador visual de uma página. Lucas: *"talvez até pra trocar a forma como fazemos alguns procedimentos"*. O candidato óbvio é o que a gente já desenha (o diagrama de roteamento, o quadro de saúde do § Legibility do ROADMAP). Ref em `core/refs/REFS.md` (INBOX 2026-09-08)  
> [ ] [ffmpeg-skill] avaliar `ffmpeg-skill` — editor de vídeo local pro agente (cortar, juntar, legendar). Irmão do `core/tools/video/`, que hoje só extrai. Ref em `core/refs/REFS.md` (INBOX 2026-09-08)  
> [ ] [md-preview-vscode] deixar a visualização formatada de `.md` como default no VSCode, e descobrir se dá pra **editar** nessa visualização. Config do harness/editor, não do workspace — mesma forma do `[plan-mode-default]` (INBOX 2026-09-09)  
> [ ] [hookspath-fora-da-arvore] o gate de tipo do pre-commit recusou um repositório de teste descartável porque `core.hooksPath` é global e alcança qualquer repo criado sob o workspace, inclusive um `tmp_path` do pytest. Hoje cada teste contorna apontando `core.hooksPath` pra um diretório vazio. Decidir: o pre-commit deveria se recusar a rodar num repo fora da árvore do workspace, em vez de cada teste ter de lembrar de desligá-lo?  
> [ ] [deriva-roteamento-academy] regerar todas as tabelas de roteamento de uma vez piorou duas coisas em `academy/`:
> um `.json` ganha `← add first-line comment`, dívida impagável naquele arquivo porque o gerador não consulta `core/hooks/described.txt` nesse caso; e em `tecnologias-na-educacao/` o blurb do arquivo vence a descrição escrita à mão (`cp01-materiais.md` passa a anunciar um id de planilha). Revertido em 2026-09-11 sem commitar; volta no próximo save naqueles diretórios  
> [ ] [memory-higiene] medir se `brain/memory/MEMORY.md` é mesmo lido em toda sessão e, se for, fazer higiene nele —
> mesma régua de `core/run tools/wos/session/reads`: linha que não muda o que o agente faz, sai (INBOX 2026-09-17)  
> [ ] [auditar-sempre-lido] auditar `AGENTS.md` e os `CONTEXT.md`: o que é de fato obedecido vs o que é ignorado. Custo é por sessão, então medir antes de cortar; irmão de [memory-higiene] (INBOX 2026-09-17)  
> [ ] [auditar-testes] auditar os ~890 testes — são muitos e vários são antigos, então alguns podem não descrever mais o que o workspace faz. Casa com [mutation-testing]: teste sem dente e teste obsoleto são o mesmo custo (INBOX 2026-09-17)  
> [ ] [vocabulario-gate-nudge] trocar "gate" por "block" no WOS, inclusive nos nomes de arquivo — mais direto sobre o impacto — e achar substituto pra "nudge" que traduza (o agente já soltou 'nudge' no meio de uma conversa em português). Cada troca ganha linha em `core/SCHEMA.md` § Retired tokens, que é o que fecha a renomeação. A terceira palavra do pedido já foi aposentada nessa tabela em 17/09 — estava em zero arquivos, só na fala do agente, e o workspace já tinha o verbo simples pra ela (INBOX 2026-09-17)  
> [ ] [painel-arquitetura] `ARCHITECTURE.html` entrega pouco: tabela gigante e vazia não ajuda. Relembrar o propósito profundo do painel e o valor que ele pode dar, trocar a tabela por lista ordenada por cor e/ou símbolo, e iterar de novo no Claude Design (INBOX 2026-09-17)  
> [ ] [agente-ve-imagem] avaliar o toolkit que dá visão — imagens e screenshots — a agente text-only; Lucas: *"será que é melhor que o que temos"*, e o que temos é o caption VLM do `core/tools/video`. Ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [archify-diagramas] **`tt-ali/archify`** (rank 04, com `cathrynlavery/diagram-design`): skills que viram conversa em diagrama html/svg limpo, *"from plain English to architecture in seconds"*. É o pedido do Lucas e encaixa exato em [painel-arquitetura] e no diagrama de roteamento — testar nos nossos dois painéis antes de redesenhar à mão  
> [ ] [github-trending-agosto] o resto do top 10 de agosto/2026, tudo na camada acima do modelo:
> `DietrichGebert/ponytail` (rank 05, skill que impede o agente de over-engineerar — 54% menos código; o irmão direto da nossa norma de reduzir), `deepseek-ai/deepseek-harness` (rank 07), `mattpocock/skills` (rank 02, já rastreado em [skills-externas]), `firecrawl/anydoc` + parser de PDF que pula OCR (rank 06, encosta em `core/tools/paper/parse`), `diegosouzapw/OmniRoute` (rank 08, gateway sobre 352 provedores), `TencentCloud/TencentDB-Agent-Memory`, `earendil-works/pi`, `PrimeIntellect-ai/prime-agent`. Ref em `core/refs/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [compaction-injection] o resumo de compactação é canal de entrada, e o nosso está aberto: a Astra escreveu uma instrução de persona no próprio resumo e o contexto seguinte a herdou (27 casos). Aqui, `core/hooks/session/precompact-wipe.py` está **desligado** — a própria descrição dele diz que os marcadores sobrevivem à compactação e a cadeia não é relida. Decidir o que o resumo pode carregar e o que é sempre relido da árvore; o `/handoff` é o mesmo canal por outro nome. Ref em `core/refs/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [teto-de-gasto-agente] o teto de gasto de um agente nosso é o que a chave permite, não o que a gente disse a ele.
> Conferir se alguma chave em uso aqui tem limite duro no provedor, e se existe log de execução legível — o relato do agente sobre o que fez não serve de prova. Nasce de um caso relatado, não medido aqui. Ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [omarchy-vs-ubuntu] comparar o Omarchy com o Ubuntu e decidir se vale trocar — a tese do post é que ele passa Windows e Mac em 18 meses porque a IA deixa qualquer um customizar o sistema. É hype de criador de conteúdo, então o comparativo é o trabalho: o que muda pro nosso uso real. Ref em `core/refs/REFS.md` (— via aiwbot 2026-09-05)  

## done

<!-- done:start -->

> [x] [mvp-gaps] DONE 2026-07-22 — all 3 gaps localized with hard numbers: (1) `core/hooks` (~40 files),
>   (2) workspace-root cruft, (3) gentle-resurfacing rhythm → shipped as `/compass`. Closed via `/compass`.
> [x] [v1-strong] DONE 2026-07-29 — superseded by explicit [v1] gate. Cruft reclaimed (6.6 GB), hooks
>   de-overengineered, telegram_daemon retired into `code/aiwbot`.
> [x] [roadmap-entrypoint] DONE 2026-07-29 — wos work collapsed from four overlapping lists into one: `/ROADMAP.md`.
>   Deletion policy set: hard delete, git is the history.<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-09-17  ·  trend: advancing  ·  touches: 445/752/792/792/792/792
<!-- stats:end -->
