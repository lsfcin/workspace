# SPECS | Disciplinas
> Metodologia macro semestral de condução, ciclos de projeto, avaliação e acompanhamento.
> governs: todas as disciplinas de graduação e pós ministradas por Lucas (TecEdu, AI4Good)

## 1. Princípios & Sequenciamento Pedagógico

1. **Regra de Sequenciamento por Tipo de Conhecimento:**
   - *Habilidade instrumental / setup de ambiente:* Instrução direta prévia (receita, starter kit e andaime explícito).
   - *Conceito novo / modelagem de problema:* Problema autêntico antes da técnica (PS-I). A equipe enfrenta o dilema
     na prática de sexta; a fundamentação teórica de quarta formaliza o desbloqueio conceitual.
2. **Alinhamento Construtivo & Stage-Gate:** Todo entregável intermediário é uma fatia funcional do produto final
   (Artigo no formato SBC/IEEE + Demonstração WOW funcional). Tarefas decorativas ou isoladas são proibidas.

---

## 2. O Calendário Canônico (Os 4 Arcos — 34 Encontros / 17 Semanas)

```
[ARCO 1: PROBLEMATIZAÇÃO & FERRAMENTAL] (Semanas 01–04 / Encontros 01–08)
  ├── Enquadramento do tema real, contrato pedagógico e setup instrumental guiado
  └── Exploração de dores autênticas com as 7 alavancas contra o óbvio
[ARCO 2: CONSTRUÇÃO & PROVA DE CONCEITO] (Semanas 05–09 / Encontros 09–18)
  ├── GATE 1 (Fechamento preliminar): Pitch gravado/ao vivo + Termo de Projeto + Persona
  └── Ciclos de arquitetura, prototipagem inicial e verificação parcial (Módulos A e B)
[ARCO 3: SPRINT EXPERIMENTAL & REDAÇÃO] (Semanas 10–14 / Encontros 19–28)
  ├── Execução de experimentos sistemáticos (ablação, métricas, testes com usuários)
  └── GATE 2 (Status Report): Demo funcional preliminar + Seções 1 a 3 do artigo
[ARCO 4: IMPACTO & DEFESA PÚBLICA] (Semanas 15–17 / Encontros 29–34)
  └── GATE 3 (Final): Banca examinadora com folha estruturada + Demo WOW + Artigo SBC/IEEE
```

---

## 3. A Anatomia da Entrega (A Tríade Fechada & O Par de .md)

Toda entrega (Checkpoint) de disciplina opera sob dois links canônicos na Planilha Mestre, gerados a partir de
modelos-base em Markdown (.md) estruturados por artefatos:

1. **Documento de Metodologia (`templates/template-metodologia.md`):**
   - Racional pedagógico ancorado (Chão $\to$ Horizonte, Doshi & Hauser).
   - Guia explícito para IAs & Agentes (harness dos alunos) atuarem como tutores sem dar respostas prontas.
   - Grafo de dependência entre os artefatos da entrega (entradas e saídas encadeadas).
   - Pipeline de construção passo a passo por artefato (sprints guiados).
   - Matriz de critérios de verificação ($A/AP/NA$) alinhada à coluna de verificação da planilha.
2. **Documento de Materiais (`templates/template-materiais.md`):**
   - **Modelo (Starter Kit):** Template com lacunas estruturadas para cada artefato exigido.
   - **Exemplo Positivo (Excelente):** Referência que cumpre a régua, acompanhada das anotações críticas do professor
     explicando o porquê do mérito.
   - **Exemplo Negativo (Fraco / Superficial / Irreal):** Referência com erros típicos e armadilhas frequentes,
     acompanhada das anotações críticas explicando por que seria reprovado / $NA$.

---

## 4. Acompanhamento & Maestria ("XP Sério")

1. **Privacidade do Painel (Estritamente Privado):**
   * Cada aluno visualiza **exclusivamente a sua própria barra** e a da sua equipe (via link seguro ou token).
   * Proibido projetar rankings ou comparações nominais em sala (risco de desmotivação e evasão, Rogers & Feller).
   * Comparações externas limitam-se à mediana agregada da turma, sem identificação.
2. **Dupla Camada de Progresso:**
   * *Progresso da Missão (Equipe):* Conquista dos Gates 1, 2 e 3 (base do projeto).
   * *Maestria Individual:* Alimentada semanalmente pelos formulários de retenção (QR Code das aulas teóricas)
     e avaliação por pares intragrupo calibrada.
3. **Avaliação Binária nas Etapas Intermediárias:** Eliminação de notas fracionadas soltas (ex.: 7,3 ou 8,1).
   O marco é classificado como `Completo/Aprovado` ou `Revisão Pendente` com base no checklist.

---

## 5. Equalização TecEdu ↔ AI4Good

1. **Unificação da Grade de Critérios:** O AI4Good adota a mesma grade de 3 critérios objetivos ($A/AP/NA$) por entrega
   já praticada nas missões do TecEdu.
2. **Folha de Banca Estruturada:** O AI4Good adota obrigatoriamente a folha estruturada de critérios para a banca
   examinadora (`outputs/ai4good-folha-de-avaliacao.md`), garantindo concordância interavaliadores ($\alpha \ge 0.75$).
3. **Unificação Semântica dos Rótulos de Nota:**
   * **`VA1`:** *Ciclo de Processo & Descoberta* (Gates 1 e 2 + grade de critérios verificados).
   * **`VA2`:** *Ciclo de Produto & Artigo Final* (Gate 3 com Banca examinadora, Demo WOW e Artigo).

---

## 6. Regra de Transição para 2026.2 (~27 Encontros Restantes)

* O calendário oficial já publicado no Notion é preservado integralmente.
* A exigência do par *Exemplo Bom / Ruim* e a régua de 3 critérios objetivos passam a valer para as entregas
  remanescentes do semestre.
* A folha de banca estruturada entra em vigor para os seminários e defesas finais de ambas as turmas.

---

## 7. Contrato para Agentes (Auditoria e Planejamento de Disciplinas)

Ao auditar ou planejar a condução de uma disciplina, o agente deve validar:
1. `[ ]` Cada entrega do calendário possui o par de `.md` estruturado pelos modelos canônicos
   (`templates/template-metodologia.md` e `templates/template-materiais.md`)?
2. `[ ]` A Metodologia decompõe a entrega em artefatos com entradas e saídas explícitas e traz a seção `Guia para IAs &
   Agentes`?
3. `[ ]` O documento de Materiais cobre a Tríade (Modelo, Exemplo Positivo e Exemplo Negativo) acompanhada de anotações
   críticas do professor para cada artefato?
4. `[ ]` O sequenciamento respeita a regra: ferramentas com andaime prévio, conceitos novos com PS-I?
5. `[ ]` O acompanhamento de notas opera com visibilidade estritamente privada por aluno/equipe?
6. `[ ]` A banca final possui folha estruturada com subitens explícitos vinculados a pesos objetivos?
7. `[ ]` Há alinhamento do requisito "Um passo a mais" (declaração da alavanca e do óbvio abandonado)?
