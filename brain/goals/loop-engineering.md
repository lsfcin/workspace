# [ career | ai | now ] loop engineering

Levar a sério e aplicar loop engineering: desenvolvimento em loops explícitos (clarificar → planejar → branch → arquitetura → TDD → codificar → user-test → commit), com autorouting — o plano de cada feature designa qual modelo/agente executa cada etapa e com qual esforço. Comunicação entre loops gravada em arquivos (`.loop/`), pra sessões de modelos menores carregarem só o necessário, nunca o histórico da conversa. Meta: economizar tokens, não gastar mais.

>**signals**  
transformative · essential · thrilled

## selected next achievement
    [pilot] pilotar o flow numa feature real pequena (isoroll-content) via /loops, com Sonnet executando

**ease-start**  
Escolher a menor feature pendente do isoroll-content e rodar `/loops <feature>`. O flow já existe (`core/flows/loop-engineering.md` + skill `/loops` + agents loop-low/medium/high) — só usar.

## backlog

> [ ] [pilot] pilotar o flow numa feature real pequena (isoroll-content) via /loops, com Sonnet executando → EM EXECUÇÃO 2026-07-09: seam pilot P2 do programa scene-creation (`export-manifest` → `module-walls-import`), Fable orquestra; spec `code/isoroll-content/SCENE-CREATION.md`  
> [ ] [iterate] ajustar flags de retorno e tabela de roteamento após 3 usos reais  
> [ ] [opencode-reliability] investigar se drift (idioma, contexto, reasoning louco mesmo em Kimi 2.6) é do opencode ou do modelo — testar mesmo modelo via claude code/openrouter; decidir: ajustar opencode OU trocar de ferramenta pros loops não-Claude  
> [ ] [verify-step] etapa de verificação (verify) explícita no flow — usar /verify no loop 5 (user-test)  
> [ ] [skills-scan] etapa no flow: revisar melhores skills disponíveis online antes de executar  
> [ ] [research-loops] variante de pesquisa do flow de loops (falta) — integrar core/flows/deepresearch|lit|autoresearch ao padrão .loop/  
> [ ] [visual-semantics] skills que traduzem semântica espacial/visual ↔ texto (geom-text, iso-text, image-text, 3D-text, UI-text) — agentes fracos em visual/geometria; UI-text cruza [[startapps-ux-guidelines-ai]] → PRIMEIRO ARTEFATO 2026-07-09: `core/skills/iso-visual.md` (convenções isoroll + failure modes + regra "geometria via manifests/QC, nunca pixels")  
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
> [x] [fable-spec] sessão Fable paralela (2026-07-06) → `core/flows/loop-engineering.md` + skill `/loops` + agents loop-low/medium/high  
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-11  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       2 |
| trimester   |       2 |
| semester    |       2 |
| year        |       2 |
| 2-year      |       2 |
| 4-year      |       2 |
<!-- stats:end -->
