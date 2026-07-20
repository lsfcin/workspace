# [ career | ai | now ] loop engineering

Levar a sério e aplicar loop engineering: desenvolvimento em loops explícitos (clarificar → planejar → branch → arquitetura → TDD → codificar → user-test → commit), com autorouting — o plano de cada feature designa qual modelo/agente executa cada etapa e com qual esforço. Comunicação entre loops gravada em arquivos (`.loop/`), pra sessões de modelos menores carregarem só o necessário, nunca o histórico da conversa. Meta: economizar tokens, não gastar mais.

>**signals**  
transformative · essential · thrilled

## selected next achievement
    [opencode-reliability] (A2) executar UM chain completo no opencode (menor feature isoroll) com MESMO modelo via openrouter em paralelo com uma run Claude Code; comparar verdicts/files; decidir: ajustar plugin OU trocar provider OU scope /loops ao Claude Code só

**ease-start**  
Abrir `core/flows/loop-engineering.md` `## Field Practice` (7 runs auditados, A1 DONE nesta sessão 2026-07-16). Setup mínima: um `.loop/` chain de feature isoroll pequena, mesmo modelo (z-ai/glm-5.2 ou viewport) em opencode e Claude Code, em paralelo. Compara só os artefatos finais + verdict do Loop 6.

## backlog

> [x] [iterate] ajustar flags de retorno e tabela de roteamento após 7 usos reais — DONE 2026-07-16 (A1; ver [A1] em `## done`)
> [x] [skill-tree] montar árvore de loops pessoais — DONE 2026-07-18: loop tree = router (`core/flows/loop-router.md`) + 4 subtrees (padaria/feature/research/architecture); mapa em `core/flows/LOOP-TREE.md`. Feature subtree = SDD contract-first (painel de permissão no Loop 0, Loop 3.5 Contract Layout, revisão de simetria de conceitos no Loop 3).  
> [ ] [prompt-dsl] DSLs como contratos entre agentes: cada agente especializado usa uma DSL própria; prompt só é repassado se o parsing é perfeito (sem ambiguidade). Questão aberta: LLMs lidam bem com gramáticas novas? Avaliar acoplar tools à LLM pra facilitar parse DSL (ver [C-C] skill-library; spacemantics texpace é o caso-teste concreto)  
> [ ] [A2] [opencode-reliability] executar UM chain completo no opencode (menor feature isoroll) com MESMO modelo via openrouter em paralelo com uma run Claude Code; comparar verdicts/files; decidir: ajustar plugin OU trocar provider OU scope /loops ao Claude Code só. Dados: NENHUMA run `.loop/` em opencode hoje (todos os executor: tags são loop-low/medium/high/claude-fable-5 via Claude Code)  
> [ ] [A3] adicionar `.loop/<slug>/STATUS.md` por chain (active | blocked-flag-pending-user | abandoned | shipped) — Loop 0 cria, Loop 6 muta; `/loops --status` = `cat code/*/.loop/*/STATUS.md`. Motivação: `isoroll-module/.loop/floor-fog-spike` e `.loop/painter-mvp-1` pararam sem 6-ship e sem status visível
> [ ] [B1] second-opinion verifier em Loop 3 + Loop 6 (sessão fresh haiku, retorna `OK crit-covered:` | `GAP <id>`). Fecha o gap vs. Voyager (Wang 2023) e vs. Anthropic best-practices ("fresh subagent context... not the reasoning that produced the change"). ESPEC em `core/flows/loop-engineering.md` `## Second-opinion verifier`
> [ ] [B2] separar `## Field Practice` das field notes (LOAD-BEARING) — feito neste commit (nova seção com tabela de overrides)
> [ ] [B3] extrair `export-manifest` integration-gap catch num `## Case Study` no flow file — feito neste commit
> [ ] [C1] research-loops: variante do flow para `core/flows/{deepresearch,lit,autoresearch}` — mesmo mecanismo Carry; onde a parallel fan-out dobra é a extensão natural (Voyager continua: skill library + auto-curriculum)
> [ ] [C2] testar o flow: um tagged-fixture repo synth em `core/flows/__loop-fixture__/` + assertion que 8 loop files aparecem com executor tags corretos pós dry-run; CI-runnable
> [ ] [C-C] Loop 6.5 Skill Extraction (Voyager skill-library primitive) — spec no flow file; pilot em 1 chain real com `keep-trail: yes`
> [ ] [D1] `last-reviewed: 2026-07` + `next-review-by: 2026-10` na tabela volátil de modelos — feito neste commit
> [ ] [D2] cross-ref dobra ↔ loops: kinship Voyager/LATM; "artifact is the memory" thesis compartilhada — feito neste commit (`code/dobra/CONTEXT.md` Overview)
> [x] [iterate] ajustar flags de retorno e tabela de roteamento após 3 usos reais → DONE 2026-07-16 (ver [A1] acima; feito aos 7 usos, não aos 3)
> [ ] [opencode-reliability] investigar se drift (idioma, contexto, reasoning louco mesmo em Kimi 2.6) é do opencode ou do modelo — testar mesmo modelo via claude code/openrouter; decidir: ajustar opencode OU trocar de ferramenta pros loops não-Claude → ver [A2] acima
> [ ] [verify-step] etapa de verificação (verify) explícita no flow — usar /verify no loop 5 (user-test) → coberto por [B1] second-opinion verifier
> [ ] [skills-scan] etapa no flow: revisar melhores skills disponíveis online antes de executar
> [ ] [research-loops] variante de pesquisa do flow de loops (falta) — integrar core/flows/deepresearch|lit|autoresearch ao padrão .loop/ → ver [C1] acima
> [ ] [pipeline-step-review] adicionar etapa de pipeline dedicada (visual/usabilidade) + revisá-la
> [ ] [arch-algo-vs-lib] etapa de arquitetura: decidir algoritmo ANTES de escolher biblioteca
> [ ] [simplicity-gap] investigar por que agente (mesmo Fable) produz soluções mais complexas/tortuosas que o design humano — ex. tinyglade-like no isoroll (etapas humanas eram simples/didáticas); motiva etapas arquitetura+review  

## seed (INBOX 2026-07 — insumo da sessão Fable)

- loop 0 — clarificar: intenção, motivação, refs, arquivos, resultado esperado, ambição, criticidade/tolerância, critérios, inovação vs padaria
- loop 1 — planejar; revisar plano assumindo que modelos menores executarão; flag de retorno
- loop 2 — branch da feature; garantir lugar/código corretos
- loop 3 — arquitetura de alto nível + avaliação; flag de retorno
- loop 4a — TDD: testes antes do código; flag de retorno
- loop 4b — codificar até passar; rodar testes; flag de retorno
- loop 5 — teste de usuário complexo automatizado; avaliar; flag de retorno
- loop 6 — commit e push
- autorouting: o plano designa agente/modelo por etapa (INBOX: "um agente planeja e no plano já aparece qual outro agente deveria executar cada parte")

## done

<!-- done:start -->

> [x] [loop-tree] DONE 2026-07-18: `/loops` virou árvore. Router (`core/flows/loop-router.md`) classifica task→subtree (padaria/feature/research/architecture); mapa canônico `core/flows/LOOP-TREE.md`. Feature subtree = SDD contract-first: painel de permissão (Loop 0, default permissivo), Loop 3.5 Contract Layout (SPEC.md + stubs + grafo de conexões type-checado por `core/tools/spec-contract-check` ANTES do código), revisão de simetria de conceitos (Loop 3, checklist + codegraph + /dedup). Novo subtree de decisão arquitetural `core/flows/loop-architecture.md` (→ ADR). Gitflow enforced (`.hooks/gitflow-gate.sh`, pre-commit 1e). loops skill roteia primeiro. Fecha [skill-tree]; cobre parte de [research-loops]/[arch-algo-vs-lib].
> [x] [A1] ajustar tabela de roteamento + flag protocol após 7 usos reais (DONE 2026-07-16, sessão de avaliação /loops): `core/flows/loop-engineering.md` recebeu `## Field Practice` com tabela de overrides, `## Status` em Loop 6, `## Second-opinion verifier` em Loop 3+6, `## Loop 6.5 Skill Extraction`, `last-reviewed` na tabela volátil. /loops skill ganhou pointer de prior art. dobra cross-ref noun.
> [x] [fable-spec] sessão Fable paralela (2026-07-06) → `core/flows/loop-engineering.md` + skill `/loops` + agents loop-low/medium/high  <!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-14  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       4 |
| trimester   |       4 |
| semester    |       4 |
| year        |       4 |
| 2-year      |       4 |
| 4-year      |       4 |
<!-- stats:end -->
