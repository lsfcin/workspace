# Metodologia de aula — proposta consolidada (Gemini, 2026-09-01)

> **Disciplinas:** *Tecnologias na Educação* e *AI4Good* (UFRPE / CIn-UFPE)  
> **Regime:** Quarta (Teórica: 1h10–1h30) | Sexta (Prática Assistida por IA: 1h10–1h30)  
> **Meta Semestral:** Demonstração WOW + Artigo Científico (SBC/IEEE) ao longo de 17 semanas práticas.  
> **Princípio de Design:** *Menos é mais* — alta robustez temporal, zero sobrecarga de preparação e foco na autonomia construtiva do aluno.

---

## 1. Trilha Teórica (Quarta-feira: 70 a 90 min)

Estruturada em **5 blocos rítmicos** para evitar a hiperfragmentação e garantir tempo real de assimilação:

| Bloco | Tempo | Nome Simples | Descrição de 1 Linha | Base Teórica & Evidência | Nota Crítica / Cuidado |
|---|---|---|---|---|---|
| **T1** | 8–10 min | **Gancho Real & Escuta Ativa** | Conecta o tema anterior a um dilema real e abre 3 min de escuta genuína da leitura de mundo dos alunos. | *Retrieval Practice* (Roediger & Karpicke, 2006); *Problematização Freiriana* (Freire, 1968). | Ter teto rígido na fala do professor; a escuta da turma deve ser real, não retórica. |
| **T2** | 5 min | **Pulso Diagnóstico** | Apresenta uma questão conceitual contraintuitiva sobre o tema do dia antes de qualquer explicação teórica. | *Pre-testing Effect* (Richland, Kornell & Kao, 2009; Kornell et al., 2009). | O erro no pré-teste é desejável (*desirable difficulty*); não tem peso de nota punitiva. |
| **T3** | 30–35 min | **Núcleo Conceitual em Dupla Codificação** | Explica o conceito em 2 micro-blocos, integrando diagramas estruturais, dados e modelagem explícita. | *Multimedia Learning* (Mayer, 2014); *Cognitive Load Theory* (Sweller, 2011). | Slides limpos: priorizar esquemas visuais e dados; eliminar parágrafos de texto corrido. |
| **T4** | 15–20 min | **Peer Instruction & Votação** | Turma vota individualmente num *Concept Test*, debate 2 min com o colega ao lado e vota novamente. | *Peer Instruction* (Crouch & Mazur, 2001, ganho conceitual normalizado $d > 0.70$). | A discussão entre pares ativa a ZPD (Vygotsky); o professor só intervém no fechamento. |
| **T5** | 5–10 min | **Ponte de Transferência & Encomenda** | Conecta a teoria a uma das 7 alavancas e define o entregável e critério de aceite da sexta-feira. | *Transfer of Learning* (Barnett & Ceci, 2002); *First Principles - Integration* (Merrill, 2002). | A encomenda precisa ser cristalina para que a turma chegue à prática com objetivo definido. |

---

## 2. Trilha Prática (Sexta-feira: 70 a 90 min)

Estruturada para **eliminar a sensação de desorientação** e garantir a escrita contínua do artigo:

| Bloco | Tempo | Nome Simples | Descrição de 1 Linha | Base Teórica & Evidência | Nota Crítica / Cuidado |
|---|---|---|---|---|---|
| **P1** | 10–15 min | **Critério de Aceite & Modelagem** | Exibe o critério de sucesso do dia e demonstra 5 min do processo (*think-aloud*) antes da turma começar. | *Cognitive Apprenticeship - Modeling* (Collins et al., 1989); *Goal-Setting* (Locke & Latham, 2002). | O slide mostra o *o quê*, a modelagem ao vivo mostra o *como*; sem isso os alunos travam. |
| **P2** | 30 min | **Sprint Focado por Papéis** | Equipes constroem seus artefatos com papéis claros (Hacker: código/IA, Hustler: validação, Hipster: UX/texto). | *Cooperative Learning* (Johnson & Johnson, 2009); *Deliberate Practice* (Ericsson, 1993). | Professor e monitores circulam nos primeiros 5 minutos para cortar bloqueios de ambiente/prompt. |
| **P3** | 10 min | **Radar de Desbloqueio** | Pausa rápida de sala inteira para o professor sanar publicamente os 2 maiores gargalos comuns do dia. | *Formative Assessment in Action* (Black & Wiliam, 1998). | Interrompe o efeito bola de neve em que grupos passam metade da aula travados numa API ou bug. |
| **P4** | 20–25 min | **Consolidação & Redação do Artigo** | Equipes integram o micro-artefato e redigem o parágrafo/seção correspondente no relatório técnico. | *Writing-to-Learn* (Bangert-Drowns et al., 2004); *POGIL* (Process-Oriented Guided Inquiry). | Redação incremental semanal elimina o pânico e a desarticulação do artigo no fim do período. |
| **P5** | 5 min | **Show & Commit do Dia** | Demonstração relâmpago de 1 minuto de uma equipe e registro do commit/avanço no repositório. | *Self-Efficacy & Progress Principle* (Bandura, 1986; Amabile & Kramer, 2011). | Visibilidade do progresso real gera sensação palpável de conquista e autoeficácia. |

---

## 3. Fundamentação e Decisões Críticas

### A. Paulo Freire × Instrução Explícita
* **Problema autêntico (Freire):** A definição do tema e a investigação de impacto social emergem da problematização da realidade dos alunos (Fase 1).
* **Ferramental técnico (Instrução Direta / Rosenshine):** O método científico, a arquitetura e a escrita acadêmica recebem modelagem explícita e scaffolding. O professor compartilha sua visão como *hipótese provocadora aberta à práxis e ao teste*, nunca como dogma.

### B. Eixos de Conteúdo: Camadas de Dupla Codificação (Paivio & Mayer)
Refutamos os "estilos de aprendizagem" (Pashler et al., 2008). O conteúdo é desenhado em **camadas complementares para toda a turma**:

| Camada | Função Pedagógica | Quando Aplicar |
|---|---|---|
| **Definição** | Precisão semântica (1 frase direta) | Sempre no início do conceito |
| **Visual** | Esquema estrutural, fluxo ou gráfico | Conceitos relacionais e arquiteturais |
| **História / Gancho** | Ancoragem em memória episódica | Abertura problematizadora da aula |
| **Dado** | Evidência empírica e peso de realidade | Justificativa do problema / Resultados |
| **Aplicação** | Conexão com sistemas do mundo real | Fechamento do bloco e ponte com a prática |

### C. Sustentabilidade do Preparo (Zero-Overhead)
* **Sem formulários infinitos:** Os pulsos teóricos e o *Peer Instruction* utilizam votação gestual, cartões de cor ou levantamento de mãos a partir de 1-2 slides de *Concept Test*.
* O formulário versionado (`gforms`) é reservado para marcos consolidados de entrega e autoavaliação periódica.

---

## 4. O Arco de 17 Semanas (Projeto: Artigo Científico + Demonstração WOW)

```
[Semanas 01-04] FASE 1: Problematização Freiriana & As 7 Alavancas
└── Foco: Investigação temática, escolha do problema autêntico, aplicação das 7 alavancas.
└── Entregável do Artigo: Seção 1 (Introdução) + Motivação Social + Hipótese da Alavanca.

[Semanas 05-08] FASE 2: Fundamentação & Arquitetura / Design
└── Foco: Revisão bibliográfica sistemática com IA, modelagem arquitetural e mockups.
└── Entregável do Artigo: Seção 2 (Trabalhos Relacionados) + Seção 3 (Metodologia e Arquitetura).

[Semanas 09-13] FASE 3: Desenvolvimento Ágil & Experimentação com IA
└── Foco: Construção do protótipo funcional, testes com usuários/dados reais, ablação.
└── Entregável do Artigo: Seção 4 (Resultados Experimentais & Análise de Impacto).

[Semanas 14-17] FASE 4: Refinamento WOW & Submissão
└── Foco: Polimento da interface para a Demo WOW (efeito visual claro), fechamento do artigo.
└── Entregável Final: Artigo Completo Formatado (SBC/IEEE) + Pitch & Demonstração WOW ao vivo.
```

---

## 5. Referências Empíricas

- **Amabile, T., & Kramer, S. (2011).** *The Progress Principle*. Harvard Business Review Press.
- **Bandura, A. (1986).** *Social Foundations of Thought and Action: A Social Cognitive Theory*.
- **Bangert-Drowns, R. L., et al. (2004).** The effects of school-based writing-to-learn interventions on academic achievement: A meta-analysis. *Review of Educational Research*, 74(1), 29-58.
- **Collins, A., Brown, J. S., & Newman, S. E. (1989).** Cognitive Apprenticeship: Teaching the craft of reading, writing and mathematics. *Knowing, Learning, and Instruction*.
- **Crouch, C. H., & Mazur, E. (2001).** Peer Instruction: Ten years of experience and results. *American Journal of Physics*, 69(9), 970-977.
- **Freire, P. (1968).** *Pedagogia do Oprimido*. Paz e Terra.
- **Kirschner, P. A., Sweller, J., & Clark, R. E. (2006).** Why minimal guidance during instruction does not work. *Educational Psychologist*, 41(2), 75-86.
- **Locke, E. A., & Latham, G. P. (2002).** Building a practically useful theory of goal setting and task motivation. *American Psychologist*, 57(9), 705.
- **Mayer, R. E. (2014).** *The Cambridge Handbook of Multimedia Learning*. Cambridge University Press.
- **Pashler, H., et al. (2008).** Learning styles: Concepts and evidence. *Psychological Science in the Public Interest*, 9(3), 105-119.
- **Richland, L. E., Kornell, N., & Kao, L. S. (2009).** The pretesting effect: Do unsuccessful retrieval attempts enhance learning? *Journal of Experimental Psychology: Applied*, 15(3), 243.
- **Roediger, H. L., & Karpicke, J. D. (2006).** Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249-255.
- **Rosenshine, B. (2012).** Principles of Instruction: Research-based strategies that all teachers should know. *American Educator*, 36(1), 12.
- **Sweller, J. (2011).** Cognitive load theory. *Psychology of Learning and Motivation*, 55, 37-76.
