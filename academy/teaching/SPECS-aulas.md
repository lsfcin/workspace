# SPECS | aulas
> contrato de planejamento e auditoria para aulas teóricas e práticas (nível micro).
> governs: toda aula teórica ou prática ministrada por lucas

## princípio & ritmo

toda aula parte de um contexto real, conexão com problemática fácil de se relacionar e aponta para um horizonte positivo, deixando fácil e mastigado entender por que estamos ali reunidos dedicando nosso tempo a estudar.

é encorajado em todas as aulas, sem exceção, trazer os alunos para junto, falar de problemas da realidade deles e do impacto daquele conteúdo na sua formação: como aquilo pode ajudar no futuro próximo, quais oportunidades se abrem e como eles podem se tornar mais capazes de se diferenciar, intervir e transformar o seu entorno.

duração padrão de encontro: **70 a 90 minutos**.

---

## aulas teóricas (até 20% de prática)

o fluxo narrativo das aulas teóricas é crítico e deve ser organicamente conectado. para cada aula, selecionar se o fluxo será linear (linha do tempo), macro $\to$ micro ou micro $\to$ macro. a aula sempre fecha com o que começou, conectando as duas pontas.

estruturada em 5 blocos rítmicos com timebox visível:

```
[15 min] kickoff problematizador + termômetro de pulso
abertura do formulário de presença ativa e reflexão, projetando o qr code nos slides. fica aberto até o fechamento da aula.
automação obrigatória usando `gforms`: criação do formulário com variações paramétricas, inserção do qr code no material, abertura/fechamento programado, análise dos dados e crédito na planilha de notas.
no kickoff, trazer um dilema real que ressoe nos estudantes: cena problemática, notícias, estatísticas de impacto, contradições éticas ou histórias pessoais, abrindo escuta autêntica para 2 ou 3 alunos. proibição absoluta de discurso superficial, artificial ou motivacional vazio ("coach").

[50 min] núcleo conceitual com pausa ativa
em 1 a 3 blocos ancorados no grafo de conhecimento (dag) da disciplina:
1. fluxo narrativo: definir a direção dos blocos (linear, macro -> micro ou micro -> macro).
2. ciclo why-what-how: para cada item e subitem, explicitar o propósito (why), a formalização rigorosa (what) e a aplicação prática (how).
3. regra dos 3 formatos: apresentar cada conceito por ao menos 3 vias complementares para redundância e sinergia pedagógica (udl). exemplos de formatos:
   - evidência empírica ou dados reais,
   - fórmulas, definições e formalizações,
   - lógica matemática ou de fluxo,
   - narrativa e histórias contextualizadas,
   - diagramas e arquiteturas,
   - imagens, animações e vídeos curtos,
   - casos de uso e aplicações industriais/sociais,
   - experimentação rápida de código e testes ao vivo,
   - dinâmicas ativas individuais ou em grupo.
4. pausa ativa (peer instruction, 3 a 5 min): entre os blocos teóricos, destacar no telão uma questão conceitual desafiadora do formulário. os estudantes debatem a lógica em duplas ou trios; como o formulário traz variações paramétricas automáticas, a discussão foca no raciocínio e cada um submete sua resposta individual.

[5 min] síntese & glossário
fechamento da árvore conceitual, mapa visual e consolidação de termos novos. amarra o conteúdo ao grafo de conhecimento da disciplina e fixa o vocabulário técnico.

[10 min] gatilho da prática
apresentação do alvo prático da próxima sessão e preparação das equipes. alinha papéis, detalha a entrega da aula de estúdio e antecipa dependências de ambiente e ferramentas.
```

---

## aulas práticas (até 20% de teoria)

estruturada para eliminar a desorientação e garantir entrega funcional incremental:

```
[20 min] motivação e resultado esperado
o que vai existir hoje que não existia antes, por que fazer isso e como sabemos que está pronto.
contextualizar a prática e o produto dela no roadmap da disciplina, mantendo os estudantes cientes de onde estão e para onde vão.
apresentar a tríade de materiais: o modelo, o exemplo de excelência e o exemplo quase bom / sem alma (ai slop).
apresentar a metodologia como guia estruturado, permitindo autonomia para variações criativas. no caso de equipes, propor um caminho viável de divisão de atividades.
apresentar a matriz de verificação com critérios atômicos e binários, explicitando como a avaliação acontecerá.

[40 min] execução supervisionada & epistemologia do debugging
o professor circula ativamente pela sala, acolhendo dúvidas e travamentos.
o erro de código ou bug é tratado explicitamente como hipótese de trabalho e ferramenta de investigação pedagógica (debugging epistêmico), nunca como falha punitiva ou sinal de incapacidade.

[10 min] status e acordo da entrega
compartilhamento do status das equipes, validação do método adotado e consolidação do que foi acordado como entrega (prazo, formato e critérios de aceite).
```

---

## aulas avaliativas

momento em que os estudantes apresentam resultados e recebem feedback formativo:

```
[10 min] relembrar o acordo e formato da entrega
revisitar a matriz de verificação e os critérios combinados. explicitar o timebox rígido, as restrições e a ordem das apresentações.

[50 min] rodadas de apresentações e avaliações estruturadas
cumprimento estrito do timebox por equipe (ex.: 5 min de pitch + 3 min de perguntas e arguição). avaliação guiada por rubrica atômica preenchida em tempo real.

[10 min] encerramento e lançamento de pontos em tempo real
fechamento reflexivo da sessão. durante os 10 minutos finais, o professor e monitores consolidam as marcações na planilha mestre privada.
os estudantes saem da sala vendo os pontos de xp cumulativo creditados no seu ambiente institucional (sigaa), sentindo o impacto imediato do trabalho realizado.
```

---

## análise por agentes

### teóricas
ao revisar ou planejar um deck ou roteiro de aula teórica, o agente deve validar:
1. `[ ]` o kickoff problematizador existe? é relevante, ancorado em dilema real ou soa como discurso superficial/coach?
2. `[ ]` o formulário (termômetro de pulso) está pronto, automatizado via `gforms`, com variações paramétricas e qr code nos slides?
3. `[ ]` a aula está explicitamente vinculada ao grafo de conhecimento (dag) da disciplina?
4. `[ ]` o fluxo didático global é evidente (linear, macro $\to$ micro ou micro $\to$ macro)?
5. `[ ]` cada tópico segue o ciclo why $\to$ what $\to$ how?
6. `[ ]` cada conceito utiliza ao menos 3 formatos complementares para sinergia e redundância (udl)?
7. `[ ]` a pausa ativa (peer instruction) de 3 a 5 min em duplas está prevista no núcleo de 50 min?
8. `[ ]` há síntese visual de fechamento, glossário técnico e gatilho explícito para a prática?
9. `[ ]` há versão acessível da aula em markdown limpo e resumo em áudio/podcast gerado via notebooklm (skill `accessible-deck`)?

### práticas
ao revisar ou planejar um roteiro de aula prática, o agente deve validar:
1. `[ ]` está clara a relevância da atividade e o produto funcional resultante (o que existe hoje que não existia antes)?
2. `[ ]` o modelo de partida está estruturado com lacunas coerentes?
3. `[ ]` o exemplo de excelência está lapidado e representa um padrão-ouro autêntico?
4. `[ ]` o exemplo quase bom antecipa com precisão as armadilhas de ai slop, superficialidade e falta de substância ("sem alma")?
5. `[ ]` a metodologia detalha entradas, etapas, saídas e inclui instruções socráticas para ias em comentários ocultos (`<!-- guia-ia -->`)?
6. `[ ]` o protocolo de execução supervisionada normaliza o erro como hipótese pedagógica (debugging epistêmico)?
7. `[ ]` os critérios de aceite binários estão definidos e o prazo é factível no calendário?

### avaliativas
ao auditar uma aula avaliativa, o agente deve validar:
1. `[ ]` a matriz de critérios atômicos e o formato da apresentação foram divulgados com antecedência?
2. `[ ]` o sistema de pontuação opera com critérios binários objetivos (feito / não feito)?
3. `[ ]` o lançamento em tempo real dos pontos nos 10 minutos finais está operacional na planilha mestre privada e sincronizado ao SIGAA?
4. `[ ]` a privacidade individual dos alunos está resguardada, sem projeção de ranqueamentos públicos nominais?
