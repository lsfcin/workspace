---
name: prof
description: >
  Pedagogia transformadora, construcionismo, gamificação séria e prática docente — router. Carrega as subskills relevantes antes de planejar, auditar ou ministrar aulas.
---

# /prof

> Router de pedagogia de excelência e prática docente. Carrega subskills modulares sob demanda para planejar, conduzir ou auditar disciplinas, aulas e materiais.

Arguments: $ARGUMENTS

## Protocol

1. Identificar o tipo de tarefa pedagógica solicitada (planejamento de aula, desenho de projeto, publicação de material, arquitetura de avaliação, auditoria contra AI slop ou acolhimento).
2. Carregar as subskills relevantes da tabela abaixo (`core/skills/prof/<subskill>.md`). Quando a tarefa envolver múltiplas dimensões, combinar 2 ou mais subskills.
3. Se invocado com argumento específico (`/prof transformacao`, `/prof pbl-cbl`, etc.), carregar diretamente a subskill correspondente.
4. Para aprofundamento empírico e citações primárias, consultar o dossiê canônico em [`academy/teaching/prof/dossie-evidencias.md`](../../academy/teaching/prof/dossie-evidencias.md).

---

## Árvore de Subskills (`core/skills/prof/`)

| Tópico | Subskill | Quando carregar |
| :--- | :--- | :--- |
| **Transformação & Práxis** | [`transformacao.md`](prof/transformacao.md) | Ancorar aula no chão da realidade, criar dilemas desorientadores, Construcionismo Freireano (Blikstein) e evitar discurso coach vazio. |
| **Construcionismo & Fazer** | [`construcionismo.md`](prof/construcionismo.md) | Desenhar laboratórios, starter kits com low floor/high ceiling, debugging epistêmico (Papert/Resnick) e abstrações do SICP. |
| **Gamificação Séria & Maestria** | [`gamificacao-seria.md`](prof/gamificacao-seria.md) | Desenhar sistemas de XP cumulativo, missões em equipes, benchmarks sérios (Foldit) e mitigar preventivamente o vale da 4ª semana. |
| **Projetos & Desafios (PBL/CBL)** | [`pbl-cbl.md`](prof/pbl-cbl.md) | Estruturar o semestre em 4 Arcos, modelo Do-Learn (Olin/Aalborg), rítmica 20-40-10, fases de Engage/Investigate/Act e bancas confiáveis. |
| **Educação Online de Excelência** | [`maestria-online.md`](prof/maestria-online.md) | Desmistificar fórmulas no estilo Andrew Ng, abordagem top-down (Fast.ai) e acolher novatos sem esnobismo no estilo Harvard CS50. |
| **Grafos de Conhecimento** | [`grafo-conhecimento.md`](prof/grafo-conhecimento.md) | Construir o DAG da disciplina, encadear pré-requisitos, ciclo WHY $\to$ WHAT $\to$ HOW com 3 formatos e checagem via Peer Instruction. |
| **IA Crítica & Anti-Slop** | [`ia-critica-antislop.md`](prof/ia-critica-antislop.md) | Criar a Tríade de Materiais (Modelo, Excelente e Quase bom / sem alma), combater a dívida cognitiva e guiar agentes com tutoria socrática. |
| **Acolhimento & Autoeficácia** | [`acolhimento-autoeficacia.md`](prof/acolhimento-autoeficacia.md) | Fortalecer as 4 fontes de autoeficácia (Bandura), segurança psicológica (Edmondson), UDL com podcasts acessíveis e inspirar sonhadores. |
| **Operação & Distribuição** | [`operacao-materiais.md`](prof/operacao-materiais.md) | Publicar no Cloudflare Pages com dual-view humanos/agentes, edição online com github.dev, formulários automatizados e podcasts. |
| **Arquitetura de Avaliação** | [`avaliacao-maestria.md`](prof/avaliacao-maestria.md) | Definir critérios atômicos binários, rito de feedback em tempo real nos 10 min finais da aula avaliativa e folhas padronizadas de banca. |

---

## Roteiro de Combinações Rápidas por Cenário

- **Planejar Aula Teórica (Micro)**: Carregar `transformacao.md` (Kickoff) + `grafo-conhecimento.md` (Núcleo WHY-WHAT-HOW com 3 formatos) + `maestria-online.md` (Desmistificação) + `operacao-materiais.md` (gforms e QR codes).
- **Planejar Aula Prática / Estúdio**: Carregar `construcionismo.md` (Starter kits e debugging) + `pbl-cbl.md` (Rítmica de 20-40-10 min) + `ia-critica-antislop.md` (Tríade de materiais e combate ao slop).
- **Conduzir Aula Avaliativa**: Carregar `avaliacao-maestria.md` (Rito dos 10 min de feedback em tempo real e critérios atômicos) + `gamificacao-seria.md` (Painel privado de maestria e proteção contra ranking público).
- **Estruturar o Semestre de Disciplina (Macro)**: Carregar `pbl-cbl.md` (4 Arcos) + `acolhimento-autoeficacia.md` (Escuta e UDL) + `avaliacao-maestria.md` (Bancas) + `operacao-materiais.md` (Arquitetura Pages/RAW).
