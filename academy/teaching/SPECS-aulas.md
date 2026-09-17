# SPECS | aulas
> contrato de planejamento e auditoria para aulas teóricas e práticas (nível micro).
> governs: toda aula teórica ou prática ministrada por Lucas

## princípio & ritmo

toda aula parte de um contexto real, conexão com problemática fáceil de se relacionar e aponta para o um horizonte positivo, deixar fácil, mastigado, entender por que a gente está alí reunido dedicando nosso tempo estudando.

então é encorajdo em todas as aulas, sem excessão, trazer os alunos pra junto, falar de problemas da realidade deles e falar do impacto daquele conteúdo na formação deles, como aquilo pode ajudar eles no futuro próximo, quais oportunidades se relacionam com aquilo, como eles podem se tornar mais capazes de se diferenciar e de ajudar o entorno.

duração padrão de encontro: **70 a 90 minutos**.

---

## aulas teóricas (até 20% de prática)

o fluxo narrativo das aulas teóricas é crítico, deve ser muito bem conectado. para cada aula selecionar se o fluxo será linear (ex.: linha do tempo), macro -> micro ou micro -> macro. a aula tem que fechar com o que começou, conectar as duas pontas.

estruturada em 5 blocos rítmicos com timebox visível:

```
[15 min] QR code de retenção + kickoff
abertura do formulário com questões, usado para acréscimo da nota e para a validar a frequência / chamada. fica aberto até o final da aula. tornar obrigatória a automação usando `gforms` da criação do form, adicição do qr code no material das aulas, abertura e fechamento do form, análise dos resultados e pontuação na planilha de notas.
incluir QR code visível nos slides durante a parte do kickoff, disponível.
no kickoff trazer um dilema real que ressoe nos alunos, cena problemática, notícias, estatísticas, histórias pessoais, escuta autêntica de alguns alunos. ter cuidado para não soar superficial, fake, ou como coach.

[50 min] núcleo conceitual
em 1 a 3 blocos com tópicos do grafo de conhecimento da disciplina, decidir fluxo dos blocos (linear, macro -> micro, micro -> macro) e para cada item e subitem usar os passos WHY-WHAT-HOW. é muito importante explorar diferentes formatos de apresentação de conteúdos visto que cada aluno pode ter mais facilidade com um ou com outro, então aqui buscamos redundância e sinergia. diria que o ideal é usar pelo menos 3 formatos para cada item. exemplos de formatos são:
- evidência empírica, 
- fórmulas, definições, formalizações, 
- lógica,
- narrativa, histórias, 
- diagramas,
- imagens, animações/transições, vídeos
- casos de uso, 
- experimentação, testes
- dinâmicas, grupos, indivíduos

[5 min] síntese & glossário
fechamento da árvore, mapa visual e termos novos. amarra a ao grafo de conhecimento da disciplina e fixa o vocabulário técnico novo.

[10 min] gatilho da prática 
apresentação do alvo e preparação das equipes. alinha papéis, detalha a entrega da próxima aula prática e dependências de ambiente.
```

---

## aulas práticas (até 20% de teoria)

Estruturada para eliminar desorientação e garantir entrega funcional incremental:

```
[00-10 min] Alvo & Especificação Enxuta (Critério de aceite claro: 1 frase testável no quadro)
[10-20 min] Modelagem com Contraste (Demonstração think-aloud + Exemplo Bom vs. Exemplo Ruim)
[20-65 min] Sprints Guiados com Checklist (Execução em blocos de 15 a 20 min com cronômetro)
[65-75 min] Verificação de Compartilhamento & Fecho (Garantia de acesso ao artefato e demo relâmpago)
```

### Regras dos Blocos Práticos
1. **Alvo Enxuto:** O que vai existir hoje que não existia antes e como sabemos que está pronto.
2. **Modelagem com Contraste (Obrigatória):** O professor demonstra a primeira fatia pensando em voz alta
   e exibe o par **Exemplo Bom vs. Exemplo Ruim** para antecipar armadilhas frequentes.
3. **Modelo e Roteiro Obrigatórios:** Nenhuma prática inicia sem Starter Template (código/documento/Excalidraw)
   e roteiro passo a passo com tempo estimado por micro-etapa.
4. **Sprints & Checklist Binário:** Trabalho em blocos temporizados com critérios binários (Sim/Não).
5. **Verificação de Compartilhamento:** Validação obrigatória de permissão de acesso ao repositório ou documento.
6. **Fecho (5 a 10 min):** Demonstração relâmpago de 60 segundos de 1 ou 2 equipes para reforçar autoeficácia.

---

## aulas avaliativas

momento em que os estudantes apresentam resultados e são avaliados

```
[00-10 min] Alvo & Especificação Enxuta (Critério de aceite claro: 1 frase testável no quadro)
[10-20 min] Modelagem com Contraste (Demonstração think-aloud + Exemplo Bom vs. Exemplo Ruim)
[20-65 min] Sprints Guiados com Checklist (Execução em blocos de 15 a 20 min com cronômetro)
[65-75 min] Verificação de Compartilhamento & Fecho (Garantia de acesso ao artefato e demo relâmpago)
```

### Regras dos Blocos Práticos
1. **Alvo Enxuto:** O que vai existir hoje que não existia antes e como sabemos que está pronto.
2. **Modelagem com Contraste (Obrigatória):** O professor demonstra a primeira fatia pensando em voz alta
   e exibe o par **Exemplo Bom vs. Exemplo Ruim** para antecipar armadilhas frequentes.
3. **Modelo e Roteiro Obrigatórios:** Nenhuma prática inicia sem Starter Template (código/documento/Excalidraw)
   e roteiro passo a passo com tempo estimado por micro-etapa.
4. **Sprints & Checklist Binário:** Trabalho em blocos temporizados com critérios binários (Sim/Não).
5. **Verificação de Compartilhamento:** Validação obrigatória de permissão de acesso ao repositório ou documento.
6. **Fecho (5 a 10 min):** Demonstração relâmpago de 60 segundos de 1 ou 2 equipes para reforçar autoeficácia.

---

## 4. Contrato para Agentes (Auditoria e Planejamento de Aulas)

### Modo 1: Avaliar Aula Existente
Ao revisar um deck ou roteiro de aula, o agente deve auditar:
1. `[ ]` O kickoff parte de um problema concreto e respeita o teto de 10 min?
2. `[ ]` Existe QR code / spec de formulário de retenção vinculado?
3. `[ ]` Há uma Árvore Didática explícita (cada slide cuida de um nó)?
4. `[ ]` Os conceitos utilizam 3 a 4 ângulos da biblioteca sem saturação?
5. `[ ]` Há micro-pausas ativas (discussão em par) previstas entre tópicos?
6. `[ ]` Existe glossário/resumo visual de fechamento e gatilho para a prática?
7. `[ ]` Na prática: há Alvo claro, Exemplo Bom vs. Ruim, Modelo, Roteiro e Checklist?
8. `[ ]` Há versão acessível gerada no padrão Tri-Bloco (via skill `accessible-deck` para leitor de tela e podcast no Google NotebookLM)?

### Modo 2: Planejar Nova Aula
Ao planejar uma nova aula do zero, o agente deve gerar:
1. **Árvore Didática:** Diagrama ou mapa mental dos nós conceituais.
2. **Roteiro dos Slides:** Estrutura slide a slide associando cada tela a um nó e ao ângulo correspondente.
3. **Spec do Formulário de Retenção:** Arquivo `.json` compatível com o gerador `gforms`.
4. **Pacote Prático (se aplicável):** Alvo, Starter Template, Exemplo Bom/Ruim e Checklist.
5. **Roteiro Acessível:** Base textual pareada aos slides no padrão Tri-Bloco (Resumo Conceitual, Audiodescrição Estrutural de Diagramas e Exemplos Práticos Extras) gerada via [`core/skills/accessible-deck.md`](../../core/skills/accessible-deck.md), pronta para áudio/podcast no NotebookLM.
