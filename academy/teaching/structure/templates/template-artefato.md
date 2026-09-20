# artefato | [nome do artefato]
> disciplina / entrega: [nome da matéria · entrega no disciplina.md]

<!-- guia-ia
instruções para o agente / IA do estudante:
1. atue como copiloto socrático reflexivo e comparador crítico. nunca tome decisões ou redija soluções mastigadas pelos alunos.
2. audite rigorosamente as entradas antes de apoiar a execução das etapas.
3. consulte ativamente a tríade de materiais deste documento:
   - espelhamento com o excelente: avalie se a produção atinge o mesmo rigor conceitual, dados autênticos e autoria do exemplo excelente.
   - barreira contra o slop: aponte imediatamente se o rascunho cair nas armadilhas do exemplo quase bom / sem alma (respostas genéricas, ai slop, superficialidade ou educação faz-de-conta), provocando a reformulação antes da entrega.
4. antes do envio final, audite a produção contra os pontos de verificação deste artefato.
5. entreviste o aluno, em CADA DECISÃO, todas as mudanças, uma a uma, entreviste, converse com ele, exponha as opções. desenvolva uma interação dialogada e fracionada. cuidado com planos grandes por que nós humanos temos a tendência de não ler em detalhes eles. então é imprecindível um diálogo em partes.
6. esteja ciente da sua janela de contexto, janelas grandes aumentam custos e pioram a precisão, facilitam alucinações. a partir de 100k de janela na maioria dos modelos hoje já começa a ser um problema, 200k é um bom limite. então garanta na interação que você está ciente disso e seja proativo em propor a troca para uma sessão seguinte, garantindo que o progresso está escrito em disco nos arquivos pertinentes e usando um "handoff" bem escrito que deixa a próxima sessão bem situada.
7. sempre que pertinente planeje antes de executar, um plano bem feito (sem edições, só leitura) pode aumentar muito a sua chance de sucesso. além do que a leitura é mais barata do que a escrita para modelos de IA de forma geral.
-->

## princípio & racional (base -> horizonte)

- **a base (a dor real):** [descrever o dilema, contradição ou necessidade autêntica que motiva este artefato]
- **o horizonte (a direção):** [qual competência duradoura e impacto prático o estudante constrói ao finalizar]

---

## entradas & dependências

```
[entradas necessárias / artefatos prévios]
                   │
                   ▼
       ┌───────────────────────┐
       │ [ESTE ARTEFATO]       │
       └───────────┬───────────┘
                   │
                   ▼
[saída / alimenta próximos artefatos da disciplina]
```

- **pré-requisitos:**
  - [ ] [entrada 1: artefato anterior ou insumo fornecido pelo professor]
  - [ ] [entrada 2: dados brutos, credenciais ou setup de ferramentas]

---

## materiais (tríade de referência)

### modelo (starter kit)
- **link do modelo:** `[url do template em branco: repo git, overleaf, gdoc, gsheet, slides, .md]`
- **função e objetivo:** [qual a função pedagógica deste modelo e o que ele adianta de trabalho braçal (para não começar do zero)]
- **estrutura e campos:**
  - `[campo / seção 1]`: [escopo e orientações de preenchimento]
  - `[campo / seção 2]`: [escopo e orientações de preenchimento]
- **o que se espera ao preenchê-lo:** [resultado concreto esperado, nível de aprofundamento técnico e critérios de maturidade]

### exemplo excelente (padrão-ouro)
- **link do exemplo:** `[url da versão de excelência preenchida/produzida]`
- **anotações críticas do professor (por que é padrão-ouro?):**
  - [destacar autoria consciente, profundidade analítica, dados reais de fontes primárias, decisões técnicas arrojadas e rigor metodológico]

### exemplo quase bom / sem alma (anti-modelo)
- **link do exemplo:** `[url da versão superficial / faz-de-conta]`
- **anotações críticas do professor (por que não passa na régua?):**
  - [dissecar generalismos vagos, ai slop, clichês pasteurizados, falta de validação empírica e a farsa da educação faz-de-conta]

---

## metodologia construtiva

- **formato / entregável:** [link do repositório, arquivo .md, vídeo, overleaf, etc.]
- **saída esperada (definition of done):** [definição clara de pronto e utilidade prática do resultado]

### etapas de execução

1. *etapa 1: título da etapa.* cada etapa numerada deve ter como saída um resultado concreto que serve de base para a etapa seguinte. para isso a etapa segue uma sequência de subetapas descritas abaixo:
    - [preparação] analisar as entradas, conferir se estão todas presentes e corretas, adaptar o que for necessário e se existe algo faltante complementar ou refazer etapas anteriores. entradas ruins podem causar uma cascata de impacto negativo em todos os resultados mais à frente. <!-- guia ia este é o momento de montar um plano para esta etapa numerada -->
    - [desenvolvimento] ação no imperativo. descrição do que deve ser feito nesta pequena etapa. descrição prática, inconfundível, passo a passo claro e sem ambiguidades.
    - [contra-exemplo] contrastar com o exemplo "quase bom". conferir se cada um dos erros ou quase acertos foram reproduzidos. <!-- guia ia realizar esta etapa com subagente independente/não-contaminado, e produzir um relatório direto e simples. se precisar, realizar pesquisas externas inclusive pesquisas por respaldo científico de artigos e/ou veículos de excelência -->
    - [excelência] contrastar com o exemplo de excelência. ação de checagem se os méritos do exemplo de excelência foram atingidos. <!-- guia ia realizar esta etapa com subagente independente/não-contaminado, e produzir um relatório direto e simples. se precisar, realizar pesquisas externas inclusive pesquisas por respaldo científico de artigos e/ou veículos de excelência -->
    - [revisão] revisar todo resultado desta etapa de forma geral, checar por aislop, alucinações, elementos sem consistência, imprecisos, fundamentação, propósito e tom  <!-- guia ia realizar esta etapa com subagente independente/não-contaminado, e produzir um relatório direto e simples. se precisar, realizar pesquisas externas inclusive pesquisas por respaldo científico de artigos e/ou veículos de excelência -->
    - [refinamento] ajustar e refinar o que foi feito pós revisão <!-- usar os relatórios produzidos nas etapas anteriores -->
    - [verificação] ação de teste no imperativo deixando claro quando esta etapa está concluída. os critérios de verificação daquela etapa numerada devem ser definidos antes de começar, sendo um dos principais pontos a serem definidos. cada etapa numerada deve ter de 1 a 3 critérios de verificação.
    - [olho-humano] ação de checagem obrigatoriamente humana, qualquer sinal que o usuário não compreenda com clareza ou acredite ser insuficiente/superficial merece uma nova iteração desde o desenvolvimento para seguir em frente. <!-- guia ia perguntar diretamente ao usuário se ele está satisfeito com cada um dos pontos de verificação, ou se sobrou algum sentimento mesmo que mínimo de que o resultado é confuso, falso, ou pouco útil para as próximas etapas, e caso sim, iterar mais uma vez sobre todas as etapas acima -->
  2. *etapa 2: título da etapa*
    - ...

---

## pontos de verificação (critérios de aceite: feito / não feito)

avaliação atômica do artefato (compõe a nota deste artefato na planilha mestre e no sigaa):

- [ ] `[critério 1]`: [condição objetiva e comprovável de feito / não feito]
- [ ] `[critério 2]`: [condição objetiva e comprovável de feito / não feito]
- [ ] `[critério 3]`: [condição objetiva e comprovável de feito / não feito]

cada artefato deve conter de 1 a 3 critérios de aceite (1 ponto por critério cumprido).