# SPECS | disciplinas
> metodologia macro semestral de condução, ciclos de projeto, avaliação e acompanhamento.
> governs: todas as disciplinas de graduação e pós ministradas por lucas (tecedu, ai4good, etc.)

## objetivos

1. **visão de mundo e de contribuição**
   - *cenário micro:* escutar os alunos, suas histórias, experiências, dificuldades, desejos, visões, como funcionam, como aprendem e quais seus perfis de partida.
   - *calibrar visão macro:* conectar com a realidade ampla com foco na verdade, no estudo rigoroso, na ciência e na recusa à opinião rasa e superficial.
   - *recuperar agência & autoeficácia:* fortalecer a capacidade de atuação, impulsionar a autoestima, coletividade e criatividade, formando estudantes sonhadores que vislumbram o inédito viável através da tecnologia.
2. **desenvolvimento de habilidades**
   - *problemáticas autênticas:* conectar o ferramental teórico-prático a problemáticas relevantes e reais, proibindo projetos fictícios ou cruds descartáveis sem dono.
   - *habilidades técnicas e comportamentais:* definir de antemão o conjunto de habilidades-alvo da disciplina.
   - *grafo de conhecimento:* estruturar as competências em um grafo direcionado acíclico (dag), explicitando dependências e sinergias.
   - *etapas:* conduzir a aprendizagem com instrução direta prévia, starter kits com piso baixo e teto alto (low floor / high ceiling), receitas e passos construtivos explícitos; aprendizagem sem mistério, simplicidade como valor central.
   - *verificação formativa:* critérios de avaliação atômicos fornecidos de antemão; ciclos formativos com recapitulação e oportunidade de ressubmissão orientada por feedback.
3. **produção de artefatos de impacto**
   - *demonstração wow:* conduzir alunos a produzirem soluções com novidade e utilidade palpáveis, gerando orgulho autêntico de autoria e encantando terceiros.
   - *relatório técnico:* desenvolver com rigor metodológico em formato de artigo para potencial submissão a veículos científicos.
   - *apresentação & pitch:* bancas avaliadoras externas com conexão profissional, servindo de preparação para editais, eventos e mercado.

---

## calendário (4 arcos: ~30 encontros | 15 semanas)

```
[ARCO 1: INICIALIZAÇÃO] (semanas 01–02)
  ├── escuta ativa e mapeamento de perfis/demandas de acessibilidade
  ├── contrato pedagógico e problemáticas-alvo
  ├── setup instrumental guiado
  └── vitória de domínio rápida (quick win inaugural no primeiro dia)
[ARCO 2: FERRAMENTAL E PROBLEMATIZAÇÃO] (semanas 03–06)
  ├── estudo das técnicas, apropriação e extrapolação
  ├── estudo das problemáticas relevantes no nível macro
  └── suporte preventivo no vale da 4ª semana (combate à fadiga de novidade)
[ARCO 3: CICLOS DE CONSTRUÇÃO DA SOLUÇÃO] (semanas 07–12)
  ├── definição de macro-áreas de interesse (problema e técnica)
  ├── prototipação da técnica-base, garantindo código funcional
  ├── levantamento de competidores na indústria e academia
  ├── ideação da contribuição para a literatura e sociedade
  ├── diagrama da solução técnica (módulos, entradas e saídas)
  ├── definição de métricas e desenho dos experimentos
  ├── desenvolvimento iterativo incremental com foco no diferencial (do-learn)
  └── aplicação de testes, coleta dos resultados e avaliação
[ARCO 4: PREPARAÇÃO E DEFESA PÚBLICA] (semanas 13–15)
  ├── refinamento geral da solução e dos experimentos
  ├── revisão e ajustes da demonstração (vídeo/demo funcional que causa efeito wow)
  ├── revisão e ajustes do relatório técnico (pronto para submissão)
  ├── refinamento da apresentação e ensaio de pitch
  └── banca examinadora externa com folha padronizada de critérios e encerramento
```

---

## missões (disciplina e artefatos modulares)

a arquitetura opera em **dois níveis limpos**: a **página-mestre da disciplina** (`disciplina.md`), que centraliza a visão macro e orquestra o calendário por missões, e os **artefatos modulares autocontidos** (`artefatos/<n>-<nome>.md`), gerados a partir dos modelos-base em markdown (.md):

### ontologia de entregas e artefatos

a condução pedagógica e o painel de avaliação operam sobre conceitos rigorosamente delimitados:
- **entrega (marco temporal):** o evento avaliativo ou checkpoint no cronograma que agrega um pacote de entregáveis (ex.: entrega 1: configuração; entrega 2: mlp visualizável).
- **artefato (a 'coisa' palpável):** o objeto concreto produzido e versionado pelos estudantes (um repositório git, um relatório técnico em LaTeX/Overleaf, um deck de slides, um vídeo executável). cada artefato é uma especificação modular autocontida nomeada como `<n>-<nome>.md`, onde `<n>` é o número de itens de verificação.
- **padrão de nomenclatura no painel (sufixos canônicos):**
  - configuração inicial de ambiente: `git` (repositório git) e `pdf` (projeto em LaTeX/Overleaf e acervo).
  - artefatos de miniprojetos e experimentos: nomeados pelo prefixo temático seguido do sufixo de formato:
    - `<nome>·c`: o subrepositório de código, dados e scripts no Git (ex.: `mlp·c`, `arq·c`, `arn·c`).
    - `<nome>·p`: o artigo/relatório técnico formal em LaTeX no Overleaf (ex.: `mlp·p`, `arq·p`, `arn·p`).
  - a largura do cabeçalho no painel espelha o nome do artefato, e a quantidade de caixas monospace (`◼`/`◻`) abaixo dele corresponde rigorosamente à quantidade de pontos de verificação daquele artefato.
- **pontos de verificação (critérios comprováveis vs. etapas):**
  - um ponto de verificação **não é uma etapa de processo** (ex.: evitar "rodar o modelo", "treinar a rede");
  - um ponto de verificação é uma **condição de existência comprovável**, auditável com precisão binária de feito ou não feito (ex.: "script de inferência executando com predições válidas", "tabela comparativa tripla de métricas", "dedução matemática formal com equações em LaTeX"). cada critério atendido confere 2 pontos de progresso (totalizando 100 pontos acumulados no semestre = 50 caixas de verificação).
- **enigmas teóricos (investigação em sala de aula):**
  - as aulas expositivas são desacopladas em decks granulares por tópico conceitual: um deck = um tema, com nome, link curto, notas e blocos do template definidos em [`SPECS-aulas.md`](SPECS-aulas.md) § slides.
  - cada tópico apresenta seus **enigmas**: desafios investigativos estruturados no padrão `contexto → pistas → raciocínio → resposta → resolução`.
  - os enigmas avaliam domínio de vocabulário e fundamentos matemáticos/arquiteturais, permitindo pesquisa ativa na web (buscadores, documentações, artigos), mas com restrição estrita ao uso de IAs generativas como atalho para respostas prontas. cada enigma resolvido confere 2 pontos de verificação teórica (1 caixa no painel).

*nota: o bloco `<!-- guia-ia -->` fala só com o agente do aluno, invisível para humanos: a IA faz, o aluno domina — ela escreve código e texto, o aluno decide cada escolha e precisa explicar e defender tudo. manutenção (painel, publicação) mora no bloco `<!-- publicacao -->`, que é do professor.*

### acesso, distribuição e edição

em ambos os casos usamos arquivos markdown com **visualização rica** e **edição online**:
- a **fonte canônica** dos arquivos `.md` fica em `academy/teaching/classes/<disciplina>/` no workspace do professor.
- a **distribuição** é feita pelo Cloudflare Pages, via espelhamento estático no repositório público `lsf-links` (`outputs/links/`).
- a **visualização rica** focada em humanos e mobile fica em `https://lucassf.pages.dev/<disciplina>/<name>`, renderizada pelo visualizador nativo (`viewer.js` + `viewer.css` + `marked.min.js`), com suporte a alertas github, tabelas responsivas e temas claro/escuro.
- a **visualização direta para ias / harnesses** é acessível no formato `https://lucassf.pages.dev/<disciplina>/<name>.md` (ou botão neutro `copiar p/ agente (raw)` no rodapé da página), permitindo ingestão instantânea via `curl -s` ou cópia com um clique.
- a **edição online com zero atrito** é fornecida pelo botão neutro `editar (github.dev)` no rodapé da página, abrindo o VS Code no navegador diretamente no arquivo do GitHub para correções imediatas em sala.
- a **regra de auto-documentação de publicação (autonomia do professor):** todo arquivo `.md` canônico que é espelhado para links públicos no Cloudflare Pages deve conter obrigatoriamente no seu cabeçalho um bloco de comentário `<!-- publicacao ... -->` contendo os comandos exatos de terminal (`painel.py`, `cp`, `git add`/`commit`/`push`) e as URLs resultantes (web e raw). isso garante que o professor tenha total autonomia para atualizar qualquer documento ou link de aula sem depender de IA ou ferramentas externas.
- **padrões de estilo visual de links e tabelas:**
  - *cronograma:* 5 colunas canônicas (`data | # | tipo | descrição | materiais`). células sem material ficam em branco.
  - *links de materiais:* formatados como pílulas de código embutidas: `[`[n] tipo · nome`](artefatos/n-nome.md)`.
  - *links de entregas:* formatados como pílulas de código: `[`git`](...)` · `[`artigo`](...)` · `[`slides`](...)`.
  - *links de referências:* links diretos em negrito sem backticks: `[**nome**](url) — descrição`.
  - *links de comunicação:* links embutidos no nome em código: `[`telegram`](...)`.
  - *painel monospace:* alinhamento à esquerda nos cabeçalhos, separador de 1 espaço entre colunas, legenda literal com nomes do cronograma.

---

## acompanhamento & maestria (sigaa & planilha mestre)

o modelo de acompanhamento combina a tranquilidade institucional da UFRPE com o rigor de critérios claros:
- **planilha mestre privada do professor:** centraliza toda a vida prática da disciplina. decompõe cada entrega em critérios atômicos e binários (feito / não feito) e calcula o **xp cumulativo** (o estudante parte de zero e acumula progresso a cada entrega validada, eliminando o estresse da perda de notas).
- **lançamento no sigaa (ufrpe):** as notas são lançadas diretamente no SIGAA oficial, particionadas em subavaliações transparentes correspondentes aos checkpoints e atividades do semestre, com automação do cálculo e exportação.
- **privacidade individual rigorosa:** cada estudante consulta seu progresso unicamente no ambiente institucional autenticado do SIGAA. é expressamente proibida a exposição de ranqueamentos públicos nominais ou murais abertos de notas, protegendo a segurança psicológica e a autoeficácia dos novatos.

---

## folha de banca examinadora (arco 4)

a banca externa de defesa pública opera com uma folha padronizada com critérios explícitos, garantindo alta confiabilidade e feedback construtivo:
1. *autenticidade e relevância do problema:* o desafio abordado responde a uma dor concreta de comunidade ou usuário real?
2. *rigor e funcionalidade da solução:* o protótipo/software funciona ao vivo de verdade ou é apenas demonstração estática?
3. *comunicação e síntese:* o pitch foi claro, persuasivo e cumpriu rigorosamente o timebox?
4. *domínio técnico na arguição:* a equipe sustenta e justifica tecnicamente suas escolhas de arquitetura e dados perante a banca?

---

## análise por agentes

ao auditar ou planejar a condução de uma disciplina, o agente (harness) deve validar:
1. `[ ]` a disciplina possui a página-mestre (`disciplina.md`, via `template-disciplina.md`) com banner, canais, propósito, regras de 100 pts/50 caixas, cronograma de 5 colunas e catálogo de entregas?
2. `[ ]` cada artefato exigido possui arquivo modular próprio (`artefatos/<n>-<nome>.md`, via `template-artefato.md`) com critérios de existência objetivos e binários?
3. `[ ]` as dependências entre artefatos respeitam a regra de sequenciamento (entradas geradas previamente)?
4. `[ ]` há uma vitória de domínio rápida (quick win) garantida no primeiro encontro (arco 1)?
5. `[ ]` há previsão de suporte e acolhimento intensivo contra a queda de motivação na 4ª semana (arco 2)?
6. `[ ]` a banca examinadora do arco 4 conta com folha padronizada de avaliação cobrindo as 4 dimensões canônicas?
7. `[ ]` o acompanhamento respeita a privacidade individual dos alunos via SIGAA, sem exposição de rankings públicos nominais?
8. `[ ]` todos os conteúdos estão publicados no Cloudflare Pages com páginas de visualização rica e endpoints RAW para harnesses de agentes?
