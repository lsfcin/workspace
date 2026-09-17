---
name: grafo-conhecimento
description: >
  Grafos e árvores do conhecimento — Novak, Gagné, KST e Peer Instruction: DAGs conceituais, âncoras cognitivas e passos WHY-WHAT-HOW.
---

# /prof grafo-conhecimento

> Grafos e árvores do conhecimento — Novak, Gagné, KST e Peer Instruction: DAGs conceituais, âncoras cognitivas e passos WHY-WHAT-HOW.

---

## Fundamentos & Evidências Científicas

- **Joseph Novak & David Ausubel** (*Aprendizagem Significativa*, 1968, 1998):
  - Conhecimento não é uma lista sequencial de tópicos, mas uma rede conceitual integrada de significados.
  - Para haver retenção profunda, a nova informação deve se ancorar em conceitos prévios relevantes (*subsunçores*). Sem essa âncora, o conhecimento degrada em memorização mecânica volátil.
- **Robert Gagné** (*The Conditions of Learning*, 1965/1985):
  - Habilidades intelectuais complexas possuem pré-requisitos lógicos obrigatórios. Pular etapas do grafo gera lacunas cognitivas cumulativas e sensação de incapacidade.
- **Jean-Paul Doignon & Jean-Claude Falmagne** (*Knowledge Spaces*, Springer 1999):
  - **Knowledge Space Theory (KST)**: Modela a competência como um grafo acíclico direcionado (DAG) de dependências. Permite o diagnóstico exato do nó de bloqueio do estudante, substituindo a reprovação genérica pela intervenção cirúrgica.
- **Eric Mazur** (1997) e **Beth Simon & Leo Porter** (SIGCSE 2013, 2016):
  - **Peer Instruction em Computação**: Votação individual sobre o nó conceitual crítico, debate ativo em duplas e revotação. Reduz reprovações em cursos introdutórios de computação à metade.

---

## Casos Reais de Sucesso (Benchmarks de Vanguarda)

- **Peer Instruction em Ciência da Computação** (Beth Simon & Leo Porter, UCSD):
  - Aplicação de questões conceituais rápidas com debate entre pares em turmas de CS1/CS2 com milhares de alunos. Cortou o índice histórico de reprovação de ~31% para ~15%, aumentou o engajamento e fechou disparidades de desempenho entre grupos sub-representados.
- **ALEKS (Assessment and LEarning in Knowledge Spaces)** (Doignon & Falmagne):
  - Sistema de tutoria inteligente baseado na teoria dos espaços de conhecimento adotado por milhões de estudantes no ensino superior. Mapeia a posição exata do estudante no DAG e sugere exatamente o próximo nó em que ele tem 85%+ de chance de maestria imediata.
- **Mapas Conceituais em Engenharia na Cornell** (Joseph Novak):
  - Décadas de acompanhamento longitudinal comprovando que a navegação explícita por grafos de conceitos gera retenção a longo prazo e capacidade de transferência para problemas inéditos 40% superior à organização linear tradicional de ementas.

---

## Protocolo Operacional para o Professor e Agentes

### 1. O Grafo da Disciplina como Bússola Visual
- **Toda Disciplina tem um Grafo Explícito**: Um mapa de nós (habilidades/conceitos) e arestas direcionadas (dependências/pré-requisitos).
- **Sinalização de Rota**: No início de toda aula e entrega, projetar o grafo e destacar:
  - *Onde estivemos* (nós verdes já dominados).
  - *Onde estamos hoje* (o nó em exploração ativa).
  - *Para onde vamos* (os nós futuros que dependem desta aula).

### 2. O Passo a Passo Conceitual: WHY $\to$ WHAT $\to$ HOW
Para cada nó ou tópico ensinado, seguir rigorosamente os três passos:
1. **WHY (A Ancoragem no Chão)**: Por que a humanidade inventou este conceito? Qual problema prático era impossível de resolver sem ele? O que quebra se não usarmos isso?
2. **WHAT (A Estrutura e Formalização)**: A definição formal, o modelo matemático, a invariante lógica, o contrato e a assinatura precisa.
3. **HOW (A Operação e Implementação)**: Como isso roda em código, testes automatizados, exceções tratadas e evidência empírica de funcionamento.

### 3. A Regra dos Três Formatos (Redundância & Sinergia)
- Cada conceito central deve ser apresentado em **pelo menos 3 formatos complementares**, garantindo acessibilidade cognitiva (UDL):
  1. *Visual*: Diagrama de arquitetura, fluxo de dados ou mapa mental.
  2. *Narrativo / Empírico*: História real, caso de uso da indústria ou contradição social.
  3. *Formal / Lógico*: Fórmula matemática, pseudocódigo ou tipagem rigorosa.
  4. *Executável*: Código real rodando com testes e saída observável.
  5. *Dinâmico*: Experimentação interativa, gráfico com sliders ou simulação.

### 4. Checagem Ativa de Nós via Peer Instruction (10 min)
- No momento de transição entre o WHAT e o HOW, lançar uma pergunta de escolha múltipla focada no modelo mental:
  - 1 min de reflexão individual e votação.
  - 3 min de discussão ativa em duplas para convencer o colega com argumentos técnicos.
  - Revotação e fechamento pelo professor.

---

## Checklist de Auditoria

- `[ ]` A aula ou entrega está explicitamente mapeada em um nó do grafo da disciplina?
- `[ ]` Os pré-requisitos necessários foram ativados antes de introduzir o novo conceito?
- `[ ]` A explicação respeita a tríade WHY $\to$ WHAT $\to$ HOW?
- `[ ]` O conteúdo oferece redundância e sinergia através de pelo menos 3 formatos distintos?
- `[ ]` Há momentos de checagem ativa de pré-requisitos e discussão em pares (Peer Instruction)?
- `[ ]` O fechamento consolida o vocabulário técnico e amarra as pontas no grafo?
