# [ career | ai | now ] loop engineering

Levar a sério e aplicar loop engineering: desenvolvimento em loops explícitos (clarificar → planejar → branch → arquitetura → TDD → codificar → user-test → commit), com autorouting — o plano de cada feature designa qual modelo/agente executa cada etapa e com qual esforço. Comunicação entre loops gravada em arquivos (`.loop/`), pra sessões de modelos menores carregarem só o necessário, nunca o histórico da conversa. Meta: economizar tokens, não gastar mais.

>**signals**  
transformative · essential · thrilled

## selected next achievement
    [pilot] pilotar o flow numa feature real pequena (isoroll-content) via /loops, com Sonnet executando

**ease-start**  
Escolher a menor feature pendente do isoroll-content e rodar `/loops <feature>`. O flow já existe (`core/flows/loop-engineering.md` + skill `/loops` + agents loop-low/medium/high) — só usar.

## backlog

> [ ] [pilot] pilotar o flow numa feature real pequena (isoroll-content) via /loops, com Sonnet executando  
> [ ] [iterate] ajustar flags de retorno e tabela de roteamento após 3 usos reais  
> [ ] [opencode-reliability] investigar se drift (idioma, contexto, reasoning louco mesmo em Kimi 2.6) é do opencode ou do modelo — testar mesmo modelo via claude code/openrouter; decidir: ajustar opencode OU trocar de ferramenta pros loops não-Claude  

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
<!-- stats:end -->
