# Metodologia de Aulas — Especificação Raiz
> O que deve ser verdade em toda aula teórica ou prática, independente da disciplina.
> Contrato de planejamento e auditoria para o professor e agentes (Antigravity, Claude Code, etc.).

## 1. Princípio & Horizonte

Toda aula parte do chão e aponta para o horizonte:
- **Ancoragem real (o chão):** conecta direto com as dores, contradições e problemas concretos que
  os alunos vivem hoje. Nada de teoria abstrata sem dono.
- **Horizonte crível (a direção):** desenha futuros possíveis e melhores nos quais dá para
  acreditar e trabalhar para construir. A tecnologia e a teoria entram como ferramentas de agência e
  emancipação, nunca como fim em si mesmas.

---

## 2. Aula Teórica (até 20% de prática)
*Duração padrão: 70 a 90 minutos.*

Estruturada em 5 blocos rítmicos com timebox visível:

```
[00-10 min] Kickoff & Escuta (Dilema real, cena problemática, escuta autêntica)
[10-15 min] QR Code de Retenção (Abertura do formulário de acompanhamento contínuo)
[15-60 min] Núcleo Conceitual (1 a 3 tópicos da Árvore Didática: WHY-WHAT-HOW + Ângulos)
[60-65 min] Síntese & Glossário (Fechamento da árvore, mapa visual e termos novos)
[65-75 min] Gatilho da Prática (Apresentação do alvo e preparação das equipes)
```

### Regras dos Blocos Teóricos
1. **Kickoff (10 min cravados):** Abre com uma cena problemática real (dado alarmante, história
   autêntica, imagem-gatilho ou contradição prática). Ouve 2 a 3 reações reais dos alunos antes de
   qualquer definição.
2. **Formulário de Retenção (QR Code):**
   - Projetado logo após o kickoff; fica aberto para resposta única até o final do encontro.
   - Contém 3 a 5 itens objetivos/reflexivos sobre os conceitos-chave do dia.
   - Serve como incentivo e pontuação extra (bonificação formativa, não punição).
   - **Automação obrigatória:** formulário padronizado gerado via spec (`gforms`), integrado à
     planilha de notas da disciplina para consolidação automática.
3. **Núcleo Conceitual (35 a 45 min):**
   - Focado em 1 a 3 tópicos subordinados a um macro-tema do calendário.
   - Cada tópico segue o fluxo **WHY** (por que isso importa/motivação), **WHAT** (o que é /
     semântica raiz), **HOW** (como funciona / aplicação).
   - Entre tópicos, pausa ativa de 2 min: pergunta conceitual para debate em dupla (Peer Instruction).
4. **Biblioteca de Ângulos (Dupla Codificação):** Para cada conceito, selecionar de 3 a 4 ângulos
   dominantes (nunca todos os 9 na mesma aula):
   - *Narrativa:* histórias, contexto histórico, personagens reais.
   - *Semântica:* definições precisas em uma frase, etimologia, conceitos raiz.
   - *Formalização:* fórmulas, matemática, pseudo-código ou código-fonte real.
   - *Diagramas:* arquitetura, esquemas relacionais, árvores de fluxo.
   - *Evidência:* dados brutos, benchmarks, estatísticas do mundo real.
   - *Imagens:* fotografia documental, cenas de impacto, ilustração de exemplo.
   - *Animações/Transições:* demonstração passo a passo de estados em sequência.
   - *Casos de Uso:* aplicação direta na indústria ou impacto social.
   - *Experimentação:* mini-teste ou simulação imediata.
   - *Dinâmica:* desafio, momento colaborativo ou competitivo, interação social.
5. **Síntese & Glossário (5 min):** Amarra a árvore didática, revisa visualmente os nós e fixa o
   vocabulário técnico consolidado.
6. **Gatilho da Prática (10 min):** Apresenta o desafio da próxima aula prática. Os alunos usam
   esses minutos para alinhar papéis, entender o que será pedido e baixar dependências/modelos.

---

## 3. Aula Prática (até 20% de teoria)
*Duração padrão: 70 a 90 minutos.*

Estruturada para eliminar desorientação e garantir entrega funcional:

```
[00-10 min] Alvo & Especificação Enxuta (Critério de aceite claro)
[10-20 min] Modelagem com Contraste (Exemplo bom vs. exemplo ruim ao vivo)
[20-60 min] Ciclos 1 Guiado com Checklist (Execução mínima, garante entendimento)
[60-75 min] Ciclo 2 com Checklist Iniciado (Tarefa completa, ciclo 1 é base)
```

### Regras dos Blocos Práticos
1. **Alvo Enxuto (5 a 10 min):** Uma frase testável no quadro/slide: o que vai existir hoje que não
   existia antes e como sabemos que está pronto.
2. **Modelagem com Contraste (10 min):**
   - Professor demonstra a execução da primeira fatia pensando em voz alta (*think-aloud*).
   - Apresenta o par **Exemplo Bom vs. Exemplo Ruim** para que a turma identifique armadilhas
     comuns antes de começar.
3. **Modelo e Roteiro Obrigatórios:** Nenhuma prática começa sem:
   - **Modelo (Starter):** repositório base, template de documento, quadro pré-formatado
     (Excalidraw/Notion) ou esqueleto de código.
   - **Roteiro:** guia passo a passo com tempo sugerido por micro-etapa.
4. **Ciclo 1 & Checklist de Verificação:**
   - Trabalho em bloco de até 40 min para garantir que os alunos dominam as ferramentas da 
   atividade extensa/completa (Ciclo 2).
   - **Lista de Verificação (Checklist):** critérios binários (sim/não) para cada etapa.
5. **Ciclo 2 Iniciado:** 
   - A partir daqui fica claro pra equipe qual é a missão completa (que não se encerra na aula). 
   - Se possível sempre usar o ciclo 1 como base. Ou seja, repetindo o ciclo 1 porém com variações, 
   é possível atingir o resultado completo final.

---

## 4. Acessibilidade Universal & Desenho Inclusivo

Acessibilidade não é pós-processamento, é requisito de projeto:
- **Auditoria de Turma:** No início de cada semestre, registrar demandas específicas de
  acessibilidade dos alunos matriculados.
- **Adaptação para Deficiência Visual (ex.: alunos cegos):**
  - **Áudio / Podcasts:** Gerar obrigatoriamente um resumo em áudio / podcast explicativo para cada
    aula (via NotebookLM, Gemini Notebook ou equivalente), narrando a lógica conceitual dos slides.
  - **Audiodescrição Ativa:** Ao apresentar diagramas, imagens e quadros, verbalizar explicitamente
    a estrutura e as relações em vez de usar expressões vazias como "vejam aqui" ou "essa seta liga
    nisso".
  - **Artefatos Legíveis por Leitores de Tela:** Código, roteiros e textos de apoio devem estar em
    markdown limpo, estruturados com níveis hierárquicos de cabeçalho bem definidos.

---

## 5. Contrato para Agentes (Auditoria e Planejamento)

Agentes que manipulam aulas neste repositório devem seguir este protocolo:

### Modo 1: Avaliar Aula Existente
Ao receber um deck ou roteiro de aula para revisar, o agente deve auditar:
1. `[ ]` O kickoff parte de um problema concreto e respeita o teto de 10 min?
2. `[ ]` Existe QR code / spec de formulário de retenção vinculado?
3. `[ ]` Há uma Árvore Didática explícita (cada slide cuida de um nó)?
4. `[ ]` Os conceitos utilizam 3 a 4 ângulos da biblioteca sem saturação?
5. `[ ]` Há micro-pausas ativas (discussão em par) previstas entre tópicos?
6. `[ ]` Existe glossário/resumo visual de fechamento e gatilho para a prática?
7. `[ ]` Na prática: há Alvo claro, Exemplo Bom vs. Ruim, Modelo, Roteiro e Checklist?
8. `[ ]` Há versão acessível gerada (roteiro para podcast / audiodescrição)?
*Se faltar algo, o agente cria placeholders comentados ou preenche a seção faltante.*

### Modo 2: Planejar Nova Aula
Ao planejar uma nova aula do zero, o agente deve gerar:
1. **Árvore Didática:** diagrama ASCII ou mapa mental dos nós conceituais.
2. **Roteiro dos Slides:** estrutura slide a slide associando cada tela a um nó da árvore e ao ângulo
   didático correspondente.
3. **Spec do Formulário de Retenção:** arquivo `.json` compatível com o gerador `gforms`.
4. **Pacote Prático (se aplicável):** Alvo, Starter Template, Exemplo Bom/Ruim e Checklist.
5. **Roteiro de Áudio / Prompt de Podcast:** base textual para gerar o áudio acessível da aula.
