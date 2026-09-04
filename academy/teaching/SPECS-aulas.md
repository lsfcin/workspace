# SPECS | Aulas
> Contrato de planejamento e auditoria para aulas teóricas e práticas (nível micro).
> governs: toda aula teórica ou prática ministrada por Lucas

## 1. Princípio & Ritmo

Toda aula parte do chão (ancoragem em dores reais) e aponta para o horizonte (direção emancipatória).
Duração padrão de encontro: **70 a 90 minutos**.

---

## 2. Aula Teórica (até 20% de prática)

Estruturada em 5 blocos rítmicos com timebox visível:

```
[00-10 min] Kickoff & Escuta (Dilema real, cena problemática, escuta autêntica de 2 a 3 alunos)
[10-15 min] QR Code de Retenção (Abertura do formulário de acompanhamento contínuo)
[15-55 min] Núcleo Conceitual (1 a 3 tópicos da Árvore Didática: WHY-WHAT-HOW + Ângulos)
[55-65 min] Síntese & Glossário (Fechamento da árvore, mapa visual e termos novos)
[65-75 min] Gatilho da Prática (Apresentação do alvo e preparação das equipes)
```

### Regras dos Blocos Teóricos
1. **Kickoff (10 min cravados):** Abre com dilema autêntico. Ouve 2 a 3 alunos antes de conceituar.
2. **Formulário de Retenção (QR Code):** 3 a 5 itens objetivos/reflexivos. Fica aberto até o final do dia.
   Automação obrigatória via especificação `gforms` integrada à planilha mestre. Bonificação, não punição.
3. **Núcleo Conceitual (35 a 40 min):** Fluxo WHY-WHAT-HOW. Pausa ativa de 2 min para debate em dupla
   (Peer Instruction).
4. **Biblioteca de Ângulos (Dupla Codificação):** Selecionar 3 a 4 ângulos por conceito (narrativa, semântica,
   formalização, diagramas, evidência empírica, imagens, animações/transições, casos de uso, experimentação).
5. **Síntese & Glossário (10 min):** Amarra a árvore didática e fixa o vocabulário técnico novo.
6. **Gatilho da Prática (10 min):** Alinha papéis, detalha a entrega da próxima aula prática e dependências de ambiente.

---

## 3. Aula Prática (até 20% de teoria)

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
8. `[ ]` Há versão acessível gerada (roteiro para áudio/podcast ou audiodescrição)?

### Modo 2: Planejar Nova Aula
Ao planejar uma nova aula do zero, o agente deve gerar:
1. **Árvore Didática:** Diagrama ou mapa mental dos nós conceituais.
2. **Roteiro dos Slides:** Estrutura slide a slide associando cada tela a um nó e ao ângulo correspondente.
3. **Spec do Formulário de Retenção:** Arquivo `.json` compatível com o gerador `gforms`.
4. **Pacote Prático (se aplicável):** Alvo, Starter Template, Exemplo Bom/Ruim e Checklist.
5. **Roteiro Acessível:** Base textual para gerar o áudio/podcast da aula via IA.
