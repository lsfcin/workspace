# SPECS | disciplinas
> metodologia macro semestral de condução, ciclos de projeto, avaliação e acompanhamento.
> governs: todas as disciplinas de graduação e pós ministradas por Lucas (techedu, ai4good, etc)

## 1. objetivos

1. **visão de mundo e de contribuição**
   - *cenário micro:* escutar os alunos, suas histórias, experiências, dificuldades, desejos, visões, como funcionam, como aprendem, quais os perfis.
   - *calibrar visão macro:* conectar com a realidade ampla com foco na verdade, no estudo, na ciência e não em opinião rasa.
   - *reperar agência:* fortalecer a capacidade, a capacidade de atuação, impulsionar a autoestima, coletividade e criatividade.
2. **desenvolvimento de habilidades**
   - *problemáticas:* conectar o ferramental teórico-prático a ser desenvolvido com problemáticas relevantes à atualidade e ao contexto dos alunos.
   - *habilidades técnicas e comportamentais:* definir de antemão o conjunto de habilidades alvo da disciplina.
   - *grafo de conhecimento:* conectar o conjunto de habilidades de forma estruturada, dependências e sinergias.
   - *etapas:* conduzir aprendizagem com instrução direta prévia, entregar starter kits, receitas, passos construtivos explícitos, cada peça conecta com a seguinte. aprendizagem sem mistério, simplicidade como valor central.
   - *verificação:* critérios de avaliação fornecidos de antemão, verificação continuada. permitir ritmos diferentes de aprendizagem. recapitular e reavaliar.
3. **produção de artefatos**
   - *demonstração wow:* conduzir alunos a produzirem soluções com tom de novidade e utilidade que impressionem terceiros que os deixem orgulhosos.
   - *relatório técnico:* desenvolver com rigor metodológico que gere relatórios que vamos submeter para veículos científicos.
   - *apresentação:* para bancas avaliadoras para ter discussão e conexão externa servindo de preparatório para pitchs em editais e eventos.

---

## 2. calendário canônico (4 arcos: ~30 encontros | 15 semanas)

```
[ARCO 1: INICIALIZAÇÃO] (semanas 01–02)
  ├── escuta e partilha de experiências relevantes
  ├── contrato pedagógico e problemáticas alvo
  └── setup instrumental guiado
[ARCO 2: FERRAMENTAL E PROBLEMATIZAÇÃO] (semanas 03–06)
  ├── estudo das técnicas, apropriação, estrapolação
  └── estudo das problemáticas relevantes, macro
[ARCO 3: CICLOS DE CONSTRUÇÃO DA SOLUÇÃO] (semanas 07–12)
  ├── definição de macro-áreas de interesse, para problema e técnica
  ├── prototipação da técnica base, garantir código funcional
  ├── levantamento de competidores, na indústria e academia
  ├── ideação da contribuição para a literatura e sociedade
  ├── diagrama da solução técnica, módulos, entradas e saídas
  ├── definição de métricas e desenho dos experimentos
  ├── desenvolvimento, iterativo incremental, foco no diferencial
  └── aplicação de testes, coleta dos resultados e avaliação
[ARCO 4: PREPARAÇÃO E DEFESA PÚBLICA] (semanas 13–15)
  ├── refinamento geral, solução e experimentos
  ├── revisão e ajustes da demonstração, vídeo que causa efeito wow
  ├── revisão e ajustes do relatório técnico, pronto para submissão
  ├── refinamento da apresentação
  └── banca examinadora e encerramento
```

---

## 3. anatomia das entregas (materiais e métodos)

toda entrega (checkpoint) de disciplina é direcionada por dois documentos canônicos (materiais e métodos), gerados a partir de modelos-base em markdown (.md) estruturados por artefatos:

1. **documento de métodos (`templates/template-metodologia.md`):**
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
3. **Distribuição, Visualização Rica & Edição Online (Stack Leve):**
   - **Fonte Canônica:** Arquivos `.md` mantidos em `academy/teaching/<disciplina>/` no workspace do professor.
   - **Distribuição (Cloudflare Pages):** Espelhamento estático no repositório público `lsf-links` (`outputs/links/`).
   - **Visualização Rica (Humano/Mobile):** `https://lucassf.pages.dev/<disciplina>/<slug>` renderizado pelo
     visualizador nativo (`viewer.js` + `viewer.css` + `marked.min.js`), com suporte a alertas GitHub, tabelas
     responsivas e tema dark/light, sem dependências de CDN externa.
   - **Visualização Direta (IAs/Harnesses):** `https://lucassf.pages.dev/<disciplina>/<slug>.md` (ou botão "Copiar p/
     Agente (RAW)" no topo da página), permitindo ingestão via `curl -s` ou cópia com 1 clique.
   - **Edição Online (Zero Custo / Zero Limites):** Botão "Editar (github.dev)" na barra superior, abrindo o VS Code no
     navegador diretamente no arquivo no GitHub. Commits vão direto para a branch `main` e o Cloudflare Pages
     atualiza em segundos.

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
8. `[ ]` Os artefatos estão publicados no Cloudflare Pages com páginas de visualização rica e endpoints RAW para
   harnesses de agentes?
