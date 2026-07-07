# mechanism-search
> Busca sistemática de mecanismos sociais (estilo Waze: motivo individual → efeito coletivo) pra um ralo de dinheiro/atenção quantificado — geração com diversidade forçada, filtro humano deliberativo, saída pronta pra piloto test-to-kill.

Programa-mãe: `branches/instituto/MOTOR.md` (ler antes — ciladas e fundamentos). Fundamentos: LLMs = novidade em volume, humanos = viabilidade, piloto = verdade (Si et al. 2024, arXiv 2409.04109; gap ideação-execução, arXiv 2506.20803).

## Entrada

Um ralo quantificado (de `branches/instituto/RALOS.md` ou laplata): fluxo em R$/mês, quem perde, quem captura, mecanismo de captura.

## Agentes e sequência

1. **Corpus check** (`researcher`) — recuperar do corpus (academy/papers/mechanism-search/refs/) os 5-8 precedentes mais próximos do ralo. Se corpus vazio: rodar `/research lit` primeiro (estágio 0).
2. **Geração divergente** (3× `researcher` em paralelo, personas antagônicas — ex.: economista comportamental, organizadora comunitária, engenheira de incentivos cripto) — cada um gera 8-12 candidatos. Técnicas obrigatórias anti-colapso:
   - mutação de precedente (pegar mecanismo do corpus, trocar 1 dimensão: população, gatilho, moeda, escala)
   - analogia distante (biologia, jogos, religião, logística)
   - cota de exploração pura: ≥20% sem precedente algum
3. **Formato de candidato** (obrigatório, 6 linhas): ralo · motivo individual (por que a pessoa usa SEM altruísmo) · efeito coletivo · quem opera · por que ainda não existe · esboço de test-to-kill ≤3 meses.
4. **Dedup e agrupamento** (`writer`) — fundir near-duplicates, agrupar por família de mecanismo. NUNCA rankear por LLM como filtro final (auto-avaliação não confiável).
5. **Filtro deliberativo humano** — formato Habermas: apresentar famílias ao grupo (board/turma), coletar posições individuais, sintetizar declaração de grupo, iterar 1×. Saída: 2-3 sobreviventes com dono nomeado.
6. **Handoff** — cada sobrevivente vira entrada no ROADMAP do programa com test-to-kill detalhado. Regra de fila: não gerar de novo enquanto 2 candidatos aguardam piloto.

## Saída

`branches/instituto/` — candidatos sobreviventes anexados ao ROADMAP.md; post-mortem de pilotos mortos vai pro arquivo do núcleo ou paper. Conhecimento novo com fonte → RALOS.md.
