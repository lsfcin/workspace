# Materiais · CP-01: Problem-Tech Fit
> Tecnologias na Educação · 2026.2 · Entrega: 16/09/2026 (Quarta-feira, 23h59)
> Planilha Mestre: `1vf_OdrC64M7ULsEpbuv8itu7bJ_3Zm51esll5bVvhBU` (Coluna K, Linha 20)
> Metodologia & Critérios: `lucassf.pages.dev/techedu/cp01`

## Guia para IAs & Agentes (Harness dos Alunos)

Se você é um agente de IA auxiliando a equipe na produção dos artefatos deste checkpoint:
1. **Papel de Comparador Crítico:** Ao analisar rascunhos produzidos pelos alunos, contraste-os imediatamente contra os
   dois polos deste documento:
   - **Espelhamento com o Exemplo Positivo:** O rascunho possui a mesma densidade analítica, fontes primárias citadas
     (INEP, Censo Escolar, UNESCO) e clareza de escopo do exemplo excelente?
   - **Detector de Armadilhas do Exemplo Negativo:** O rascunho caiu em alguma das armadilhas apontadas nas anotações do
     professor (ex.: tarefas coletivas sem dono, soluções mágicas disfarçadas de problema, "usar IA" sem código
     compilado)?
2. **Intervenção Ativa:** Se a redação de um problema parecer um clichê de redação escolar, recuse o texto e exija que a
   equipe busque dados concretos e aplique uma das 7 alavancas contra o óbvio.

---

## 1. Visão Geral da Tríade Fechada

Cada artefato exigido neste checkpoint é apresentado através de três referências:
1. **O Modelo (Starter Kit):** Estrutura pronta em branco para preenchimento.
2. **O Exemplo Positivo (Excelente · `A`):** Cumpre plenamente o rigor com anotações críticas do professor.
3. **O Exemplo Negativo (Fraco / Superficial · `NA`):** Erros típicos e clichês com anotações explicativas.

---

## 2. Pacote de Materiais por Artefato

### Artefato 1: Quadro de Gestão de Missão (Kanban)

#### A. Modelo em Branco (Starter Kit)
- **Plataforma:** Trello ou GitHub Projects.
- **Colunas:** `Backlog`, `A Fazer (Sprint)`, `Em Andamento (WIP: 1/pessoa)`, `Revisão`, `Concluído`.
- **Template de Card:** `[Papel] [Responsável] Verbo no infinitivo + objeto direto`
  - *Descrição:* Objetivo concreto, estimativa (2h a 4h), Critério de Pronto (DoD) testável e link do artefato gerado.

#### B. Exemplo Positivo (Excelente · Atingido Plenamente)
- **Referência:** Quadro com cards atômicos devidamente distribuídos:
  - `[Hacker] [Mariana Costa] Clonar Whisper.cpp e rodar benchmark de transcrição com áudio de aula gravada (3 min)`
    - *Descrição:* Executar o modelo quantized `tiny.en` e `small` em CPU local; medir tempo de inferência e salvar o
      arquivo `.vtt` resultante na pasta `docs/benchmarks/`. Critério de pronto: arquivo de legenda gerado e script de
      reprodução versionado no Git. Estimativa: 3h.
  - `[Hipster] [Lucas Silva] Mapear jornada de dor do professor corrigindo redações dissertativas no Ensino Fundamental
    II`
    - *Descrição:* Sintetizar as 3 etapas críticas (leitura diagnóstica, anotação pontual de desvios e atribuição de
      feedback formativo) em um fluxo visual no Excalidraw. Critério de pronto: diagrama exportado e vinculado ao
      Overleaf. Estimativa: 2.5h.
  - `[Hustler] [Beatriz Lima] Levantar dados do Censo Escolar 2025 sobre número médio de alunos por turma em PE`
    - *Descrição:* Consultar microdados do INEP e extrair tabela com média de turmas de 6º a 9º ano da rede estadual de
      Pernambuco para fundamentar o Parágrafo 1 do Artigo. Critério de pronto: parágrafo escrito com citação BibTeX.
      Estimativa: 2h.
- **Anotações Críticas do Professor (Por que este exemplo cumpre a régua?):**
  > [!TIP]
  > - **Atomicidade Real:** Nenhuma tarefa é um "projeto inteiro". Cada card pode ser concluído em uma janela única de
  >   trabalho (2 a 4 horas).
  > - **Dono Nominal Único:** Não há diluição de responsabilidade. Cada card tem exatamente um nome atribuído.
  > - **Critério de Aceite Falsificável:** Qualquer membro da equipe pode auditar se o card está pronto ou não olhando o
  >   arquivo gerado.

#### C. Exemplo Negativo (Fraco / Superficial · Não Atingido)
- **Referência:**
  - Card 1: `Fazer o artigo do Overleaf (Equipe inteira)`
  - Card 2: `Programar a Inteligência Artificial`
  - Card 3: `Pesquisar sobre educação`
  - Card 4: `Ajustes gerais e slides`
- **Anotações Críticas do Professor (Por que este exemplo NÃO passa?):**
  > [!WARNING]
  > - **Tarefas Monolíticas:** "Fazer o artigo" não é uma tarefa, é a entrega inteira. Isso esconde a procrastinação e
  >   inviabiliza o acompanhamento ágil.
  > - **Tarefas de "Todo Mundo":** Tarefa com múltiplos donos ou "Equipe inteira" é tarefa de ninguém. Na prática, um
  >   aluno faz e três pegam carona.
  > - **Falta de Critério de Pronto:** O que significa "Pesquisar sobre educação"? Quando isso termina? Sem critério
  >   testável, o card é apenas decorativo.

---

### Artefato 2: Configuração de Ambiente & Harness de IA

#### A. Modelo em Branco (Starter Kit)
- **Comprovação em `docs/setup-equipe.md`:**
  - *Repositório Git & Overleaf:* Links oficiais e lista dos 4 membros com usuário GitHub e papel declarado.
  - *Harness de IA Local:* Registro de ferramenta (Claude Code, OpenCode, Antigravity, Copilot CLI) por integrante com
    captura de tela ou log de terminal no repo.

#### B. Exemplo Positivo (Excelente · Atingido Plenamente)
- **Referência:**
  - Registro de execução no terminal demonstrando a ferramenta interagindo com o repositório local:
    ```bash
    $ opencode run "auditar links de links.txt contra as specs da disciplina"
    ✓ Analisando árvore de diretórios...
    ✓ 4 arquivos inspecionados. Nenhum link quebrado encontrado.
    ```
  - Print screen de todos os 4 membros listados como colaboradores aceitos no GitHub e no Overleaf.
- **Anotações Críticas do Professor:**
  > [!TIP]
  > A equipe comprova que o instrumental de apoio de IA está plenamente operacional nas máquinas locais dos alunos, e
  > não apenas uma aba aberta de chat na web. Isso garante fluência e velocidade para os sprints seguintes.

#### C. Exemplo Negativo (Fraco / Superficial · Não Atingido)
- **Referência:**
  - Apenas um link para o GitHub onde consta apenas 1 único colaborador (o criador do repo).
  - Print de uma tela do ChatGPT no navegador feita no celular.
- **Anotações Críticas do Professor:**
  > [!WARNING]
  > Indica que o grupo não se organizou coletivamente e que o trabalho será centralizado em uma pessoa só. Viola o
  > critério de nivelamento instrumental da turma.

---

### Artefato 3: Seção de Problemas Novos no Artigo & "O Passo a Mais"

#### A. Modelo em Branco (Starter Kit)
- **Estrutura no Artigo Overleaf (2 parágrafos por problema):**
  - *Parágrafo 1:* Cenário concreto com evidência quantitativa primária (dados do Censo Escolar, INEP, UNESCO, SAEB) e
    citação bibliográfica.
  - *Parágrafo 2:* Ator diretamente afetado, limitações de tentativas anteriores, alavanca do "Passo a Mais" adotada e
    explicitação do óbvio deliberadamente abandonado.

#### B. Exemplo Positivo (Excelente · Atingido Plenamente)
- **Texto Modelo:**
  > **Contexto e Problemas Autênticos**
  >
  > Na rede pública brasileira de Ensino Fundamental II, a sobrecarga de trabalho docente na avaliação formativa é um
  > dos principais fatores de exaustão e abandono da carreira. Segundo dados do Censo da Educação Básica (INEP, 2024), a
  > média nacional nas capitais é de 31,4 alunos por turma regular, com docentes de Língua Portuguesa ministrando aulas
  > frequentemente em 5 a 8 turmas simultâneas. Essa configuração impõe ao docente a leitura e correção de mais de 200
  > redações por ciclo quinzenal, resultando em um tempo médio disponível de menos de 90 segundos por texto para
  > anotação de devolutiva formativa, gerando feedbacks genéricos que pouco auxiliam na progressão do letramento (SILVA;
  > SANTOS, 2023).
  >
  > O ator central afetado é o docente, que se vê reduzido a uma função cartorial de "atribuir nota", em detrimento da
  > tutoria individualizada. Soluções de mercado tipicamente tentam automatizar a correção através de pontuação gerada
  > por LLMs, o que gera desconfiança pedagógica e alienação do estudante. Para romper este impasse, adotamos a alavanca
  > de **Trocar quem faz o trabalho**: em vez de colocar o professor ou a IA como corretores soberanos, a tecnologia
  > transforma o próprio aluno no avaliador crítico de textos anonimizados de colegas mediante andaimes socráticos
  > orientados por rubricas. Abandonamos o óbvio (*"criar uma IA que corrige a redação e dá nota ao aluno"*) para
  > construir uma ferramenta de calibração entre pares onde a IA atua apenas como provocadora metodológica para o
  > estudante avaliador.
- **Anotações Críticas do Professor (Por que este exemplo cumpre a régua?):**
  > [!TIP]
  > - **Dados Primários Concretos:** Cita INEP 2024, média de 31,4 alunos/turma, volume quinzenal e tempo de 90
  >   segundos. É uma dor mensurável e real, não uma opinião vaga de boteco.
  > - **Atores Delimitados:** Especifica o docente de Língua Portuguesa no EF II.
  > - **O Passo a Mais Transparente:** Nomeia a alavanca (*Trocar quem faz o trabalho*), declara expressamente qual era
  >   o clichê (*"IA que corrige redação e dá nota"*) e explica por que o novo caminho é pedagogicamente superior.

#### C. Exemplo Negativo (Fraco / Superficial · Não Atingido)
- **Texto Falho:**
  > **Contexto e Problemas**
  >
  > A educação no Brasil tem muitos problemas e as escolas estão defasadas. Os alunos não prestam mais atenção nas aulas
  > porque passam o dia inteiro no TikTok e no Instagram. Os professores usam métodos tradicionais do século passado que
  > dão sono nos estudantes.
  >
  > O problema é a falta de tecnologia na sala de aula. Para resolver isso, vamos criar uma plataforma gamificada com
  > Inteligência Artificial que vai deixar o aprendizado divertido e engajador, com quizzes e pontuação para motivar os
  > alunos a estudar.
- **Anotações Críticas do Professor (Por que este exemplo NÃO passa?):**
  > [!WARNING]
  > - **Superficialidade Clichê:** Frases como "a educação tem muitos problemas" e "métodos do século passado" são
  >   clichês vazios que demonstram zero pesquisa.
  > - **Ausência Total de Evidências:** Nenhuma estatística, nenhum autor citado, nenhuma fonte oficial.
  > - **Solução Fantasiada de Problema:** A equipe diz que o problema é "falta de tecnologia" para justificar o app que
  >   eles já queriam fazer antes de conversar com qualquer professor.
  > - **O Óbvio Não Foi Abandonado:** "Gamificação com quizzes e pontos para deixar divertido" é a ideia mais óbvia e
  >   batida dos últimos 15 anos. Zero aplicação de alavanca inovadora. Nota: `NA`.

---

### Artefato 4: Ficha Técnica de Tecnologia Demonstrável com Código Compilado

#### A. Modelo em Branco (Starter Kit)
- **Campos obrigatórios em `docs/tecnologia-base.md`:**
  - *Mapeamento:* Eixo e Folha da árvore (`tecnologias.json`), URL do GitHub, stars, último commit e licença.
  - *Especificação:* Tarefa técnica, formato exato do Input de teste e formato/schema JSON do Output gerado.
  - *Reprodução & Comprovação:* Comandos de instalação/execução e link de vídeo/GIF curto (15–30s) de execução local.

#### B. Exemplo Positivo (Excelente · Atingido Plenamente)
- **Referência:** Ficha preenchida com biblioteca `faster-whisper`, demonstrando inferência local em CPU Intel i5
  rodando em 4.2 segundos para um trecho de 15 segundos de fala de professor em sala com eco. Acompanha vídeo curto de
  18 segundos no Drive com permissão aberta mostrando o terminal executando o script e gerando o JSON com timestamps
  precisos.
- **Anotações Críticas do Professor:**
  > [!TIP]
  > Prova definitiva de viabilidade. A equipe não está apenas "sonhando" com uma arquitetura: já sabe exatamente as
  > bibliotecas necessárias, o formato do dado de entrada, o custo computacional e o output esperado.

#### C. Exemplo Negativo (Fraco / Superficial · Não Atingido)
- **Referência:**
  - Ficha que diz apenas: *"Vamos usar IA generativa do OpenAI para transcrever e resumir as aulas."*
  - Sem repositório, sem especificação de inputs/outputs e sem vídeo ou evidência de código rodando localmente.
- **Anotações Críticas do Professor:**
  > [!WARNING]
  > Isso não é uma especificação técnica, é uma declaração de intenções. Não comprova viabilidade, não explora licenças
  > e não tira a equipe da zona de conforto. Reprovado com `NA`.
