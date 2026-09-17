# SPECS | ensino
> o que deve ser verdade em toda aula teórica ou prática e em toda condução de disciplina.
> contrato de planejamento e auditoria para o professor e agentes (antigravity, claude code, etc.).
> governs: todo material, planejamento e condução de ensino sob academy/teaching/

## manifesto & tom docente

o ensino ministrado por lucas recusa tanto a pedagogia bancária tradicional quanto a frieza do tecnicismo estéril. o objetivo central de cada disciplina e de cada encontro é promover uma educação acolhedora, transformadora e conscientizadora:
- **hospitalidade radical e zona livre de julgamento:** acolher a vulnerabilidade do aluno iniciante. a sala de aula é um ambiente psicologicamente seguro (amy edmondson), livre de elitismo técnico ou intimidação. ninguém é ridicularizado por perguntar ou por errar.
- **autoeficácia real pelo fazer (albert bandura):** a confiança técnica do estudante não nasce de discursos de autoajuda vazios ("coach"), mas da experiência concreta de construir artefatos funcionais desde o primeiro encontro (quick wins). o aluno deve sair da aula sentindo-se capaz de aprender, programar e resolver desafios complexos.
- **alunos sonhadores e utopias práticas:** a tecnologia digital e a teoria entram como instrumentos de agência e emancipação popular (paulo freire e paulo blikstein). exercitar a imaginação crítica, desenhar futuros possíveis e viáveis (o inédito viável) e pavimentar o caminho prático do hoje para esse horizonte. formar profissionais tecnicamente rigorosos, conscientes e sonhadores.
- **ia como copiloto socrático reflexivo:** inteligência artificial não é atalho para terceirizar o pensamento ou gerar trabalhos superficiais ("ai slop"). o uso de agentes deve provocar o raciocínio crítico do estudante, estimulando autoria e responsabilidade ética.

---

## princípio e horizonte

toda atividade de ensino parte do chão e aponta para o horizonte:
- **ancoragem real (o chão):** conecta direto com as dores, contradições e problemas concretos que os alunos e a sociedade vivem hoje. nada de teoria abstrata sem dono ou cruds fictícios descartáveis.
- **horizonte crível (a direção):** desenha futuros possíveis e melhores nos quais dá para acreditar e trabalhar para construir. a técnica é ferramenta de transformação material e social, nunca um fim em si mesma.

---

## desenho inclusivo

acessibilidade universal como princípio de arquitetura pedagógica, não como pós-processamento:
- **auditoria de turma (arco 1):** no início de cada semestre, registrar demandas específicas de acessibilidade, bagagem prévia e equipamentos dos estudantes matriculados.
- **adaptação para deficiência visual e neurodivergência:**
  - **áudio / podcasts:** gerar obrigatoriamente um resumo conceitual em áudio / podcast explicativo para cada aula (via google notebooklm ou equivalente), narrando a lógica dos conceitos e slides.
  - **audiodescrição ativa:** ao projetar diagramas, imagens e fluxogramas, verbalizar explicitamente a estrutura e as relações conceituais em vez de usar expressões vazias como "vejam essa seta ligando nisso aqui".
  - **artefatos em markdown semântico:** código, roteiros e textos de apoio devem estar em markdown limpo, com hierarquia de cabeçalhos bem definida para leitura imediata por leitores de tela e sintetizadores de voz.

---

## análise por agentes

todo o material em teaching é projetado para consumo dual: por seres humanos e por agentes autônomos:
- documentos canônicos incluem seções explícitas de "análise por agentes" com critérios de auditoria.
- instruções específicas de harness e tutoria socrática são inseridas como comentários ocultos para humanos (`<!-- guia-ia -->` ou `<!-- agents -->`).
- agentes que atuam como tutores devem desafiar o aluno a justificar escolhas conceituais, recusando a entrega de código mastigado sem diálogo reflexivo prévio.

<!-- routing:start -->
## routing

| documento | descrição | governa |
|-----------|-----------|---------|
| [`SPECS-aulas.md`](SPECS-aulas.md) | contrato de planejamento e auditoria para aulas teóricas, práticas e avaliativas (nível micro). | toda aula teórica, prática ou avaliativa ministrada por lucas |
| [`SPECS-disciplinas.md`](SPECS-disciplinas.md) | metodologia macro semestral de condução, ciclos de projeto em 4 arcos, avaliação formativa e acompanhamento via sigaa. | todas as disciplinas de graduação e pós ministradas por lucas (tecedu, ai4good) |
<!-- routing:end -->
