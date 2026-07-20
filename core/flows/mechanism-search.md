---
description: Busca sistemática de mecanismos sociais (motivo individual → efeito coletivo) para um ralo quantificado — geração com diversidade forçada, filtro humano deliberativo, saída pronta para piloto test-to-kill.
args: <ralo>
type: domain
confirm: plan
agents: researcher, writer
---
## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set. See `core/tools/` for runtime-specific mappings.

- Search: use `web_search`
- Fetch URLs: use `fetch_content`
- Paper search: use available paper-search tools or `alpha` via `bash`
- Agent delegation: use `subagent` when available
- If a tool returns `Tool not found`, map to the canonical visible tool or record the capability as blocked.

# mechanism-search
> Busca sistemática de mecanismos sociais (estilo Waze: motivo individual → efeito coletivo) pra um ralo de dinheiro/atenção quantificado — geração com diversidade forçada, filtro humano deliberativo, saída pronta pra piloto test-to-kill.

Programa-mãe: `branches/instituto/MOTOR.md` (ler antes — ciladas e fundamentos). Fundamentos: LLMs = novidade em volume, humanos = viabilidade, piloto = verdade (Si et al. 2024, arXiv 2409.04109; gap ideação-execução, arXiv 2506.20803).

## Entrada

Um ralo quantificado (de `branches/instituto/RALOS.md` ou laplata): fluxo em R$/mês, quem perde, quem captura, mecanismo de captura.

## Artefatos obrigatórios

Derivar um slug curto do ralo (minúsculas, hífens, ≤5 palavras). Toda rodada deve deixar em disco:

- `outputs/.plans/<slug>.md` — plano + checagem da regra de fila
- `outputs/.drafts/<slug>-gen-{1,2,3}.md` — candidatos por persona
- `outputs/<slug>-familias.md` — famílias deduplicadas (material do filtro humano)
- sobreviventes anexados a `branches/instituto/ROADMAP.md` (só após o filtro humano)

Depois que a geração começa, nunca terminar só em chat. Se uma capacidade falhar, continuar em modo degradado e registrar o bloqueio no plano.

## Plano (parar para confirmação)

Antes de qualquer geração:
1. **Regra de fila** — checar `branches/instituto/ROADMAP.md`: não gerar de novo enquanto 2 candidatos aguardam piloto. Se a fila está cheia, parar e reportar.
2. **Corpus check** (`researcher`) — recuperar do corpus (`academy/papers/mechanism-search/refs/`) os 5-8 precedentes mais próximos do ralo. Se corpus vazio: rodar `/research lit` primeiro (estágio 0).
3. Escrever `outputs/.plans/<slug>.md` (ralo, precedentes, personas escolhidas, ledger). Resumir e pedir confirmação explícita antes de spawnar geradores.

## Agentes e sequência

1. **Geração divergente** (3× `researcher` em paralelo, personas antagônicas — ex.: economista comportamental, organizadora comunitária, engenheira de incentivos cripto) — cada um gera 8-12 candidatos em `outputs/.drafts/<slug>-gen-N.md`. Técnicas obrigatórias anti-colapso:
   - mutação de precedente (pegar mecanismo do corpus, trocar 1 dimensão: população, gatilho, moeda, escala)
   - analogia distante (biologia, jogos, religião, logística)
   - cota de exploração pura: ≥20% sem precedente algum
2. **Formato de candidato** (obrigatório, 6 linhas): ralo · motivo individual (por que a pessoa usa SEM altruísmo) · efeito coletivo · quem opera · por que ainda não existe · esboço de test-to-kill ≤3 meses.
3. **Dedup e agrupamento** (`writer`) — fundir near-duplicates, agrupar por família de mecanismo em `outputs/<slug>-familias.md`. NUNCA rankear por LLM como filtro final (auto-avaliação não confiável).
4. **Filtro deliberativo humano** — formato Habermas: apresentar famílias ao grupo (board/turma), coletar posições individuais, sintetizar declaração de grupo, iterar 1×. Saída: 2-3 sobreviventes com dono nomeado.
5. **Handoff** — cada sobrevivente vira entrada no ROADMAP do programa com test-to-kill detalhado.

## Integridade

- Precedente citado deve existir no corpus ou vir com URL de fonte — nunca inventar precedente, número de fluxo ou resultado de piloto.
- O filtro final é humano; a saída do LLM é sempre proposta, nunca decisão.

## Saída

`branches/instituto/` — candidatos sobreviventes anexados ao ROADMAP.md; post-mortem de pilotos mortos vai pro arquivo do núcleo ou paper. Conhecimento novo com fonte → RALOS.md.
