# References
> Level-1 capture: one line per ref. Promote to a paper's own `refs/<name>.yaml` when it becomes a citation.

- [van Clief paper — arxiv 2603.16021](https://arxiv.org/pdf/2603.16021) — study (agent/folder methodology)
- [Claude Code design space — arxiv 2604.14228](https://arxiv.org/pdf/2604.14228) — agent design space
- [Gary Stevenson — Gary's Economics](https://www.youtube.com/@GarysEconomics) — economics commentary; read + index
  where pertinent
- [Rutger Bregman — Moral Ambition](https://www.rutgerbregman.com/) — read + index where pertinent
- [World Inequality Lab — Global Justice Report](https://www.instagram.com/p/DbGep4CDGtk/) — first fully-quantified plan
  for equality + prosperity within planetary boundaries (income/wealth/power inequality reduction as a condition for
  shared prosperity, compatible with decarbonization). Lucas: usar nas aulas, provavelmente ai4good
Every reel below is `[src: web:instagram.com]`, and each carries its paired task in
`brain/goals/teaching-materials.md` under the name at the end of its line — the task holds what to do, so
these lines hold only what the reel is and what to distrust about it.

- [Luciano da Luz — mandato coletivo](https://www.instagram.com/reel/DaIgvighjQ6/) — participatory mandate: constituents
  vote on bills and track spending alongside an elected rep. Mechanism design → `brain/goals/cria.md`
  `[mandato-coletivo]`.
- [Han Shlomo — "this feels like a book burning"](https://www.instagram.com/reel/DbW7yCzkeqX/) — frames a current
  AI/knowledge-destruction moment. **Hook, not argument** — find the underlying event first. `[ai4good-book-burning]`
- [theaifield — books scanned for training data](https://www.instagram.com/p/DcQ1847jA8l/) — physical books as prime
  training data; names Anthropic's reported *"Project Panama"* (bought, unbound, scanned, recycled) against
  non-destructive scanning. **A post, not a source** — confirm before teaching. Same `[ai4good-book-burning]`.
- [RammCodes — face-recognition library](https://www.instagram.com/reel/Db03NOvo6B0/) — one API over detection,
  recognition, tracking, landmarks, gaze, parsing, anti-spoofing; fits the 3D CV material. **The reel never names it** —
  search on gaze + anti-spoofing in one package.
- [Dr. Alvaro Cintas — arXiv Visuals](https://www.instagram.com/reel/DcJQd0TRewZ/) — turns an arXiv paper into a
  narrated explainer via three agents, and claims to find the **hardest concept first** and build around teaching that.
  **Comment-gated link** — find the tool independently. `[arxiv-visuals]`
- [Kem / GlitchCatClub — pacing the frontier](https://www.instagram.com/reel/DbsJYiotcLj/) — **caption only extracted**,
  so the argument is unknown; suggests a frontier-pace / regulation angle. `[ai4good-pacing-frontier]`
- [eluna.ai — Yann LeCun](https://www.instagram.com/reel/Dbd8XDWSM1A/) — argues for AI that models how the world works
  rather than predicting the next word. `[ai4good-lecun]`
- [Asha Zimmerman — "we are pro integration"](https://www.instagram.com/reel/DcOxARouQxF/) — labs chase replacement
  because investor growth promises demand it; integration as the alternative. **The founder is selling hardware.**
  `[ai4good-integracao]`
- [Joseph Gordon-Levitt — optimism](https://www.instagram.com/reel/DcRMN_hM537/) — the challenges of AI and democracy
  can be named without concluding nothing can be done. `[ai4good-otimismo]`
- [LJ — 10 solarpunk games](https://www.instagram.com/p/Db8TS-UFC8N/) · [ria — indigenous knowledge leads
  solarpunk](https://www.instagram.com/reel/DY2wj1svR_m/) — restoring ecosystems, sustainable communities (Terra Nil,
  Loddlenaut); indigenous ecological knowledge as the movement's lead. *"solarpunk é a vibe de ai4good"* — positioning
  for the course, no task.

- [Duryea, Ribas, Sampaio, Sampaio & Trevisan — Who benefits from tuition-free, top-quality
  universities?](https://doi.org/10.1016/j.econedurev.2023.102423) — *Economics of Education Review* 95:102423, 2023.
  Evidence from Brazil on who the free elite university actually reaches. Reached via
  [reel](https://www.instagram.com/reel/DdPgPgYxjaV/) by econometriafacil; Lucas: *"esse estudo tem que entrar na minha
  aula"* — which discipline is still open (task in `brain/goals/teaching-materials.md` [universidade-gratuita]).
- [Amodei — Machines of Loving Grace](https://darioamodei.com/essay/machines-of-loving-grace) — [src:
  web:darioamodei.com] October 2024 essay sketching the upside of powerful AI across five areas: biology and physical
  health, neuroscience and mental health, economic development and poverty, peace and governance, work and meaning.
  Three of the five *are* the AI4Good syllabus. Lucas: *"falar disso nas minhas aulas"* (task in
  `brain/goals/teaching-materials.md` [amodei-loving-grace]).
- [kem_glitch — Memory = Context Management](https://www.instagram.com/reel/DdME5hsNRju/) — [src: web:instagram.com]
  practitioner explainer: the model has no memory, the harness re-sends the whole conversation every call, and caching
  is a cheaper re-read rather than memory. Names **context poisoning** (a wrong or superseded read lands, stays, and
  shapes every later answer) and **context rot** (more tokens, thinner slice of attention on what matters). Divulgação,
  not primary source. Lucas: *"colocar na minha aula"* (task in `brain/goals/teaching-materials.md`
  [memoria-e-contexto]; — via aiwbot).
- [Menezes et al. — Manacá-1B](https://arxiv.org/abs/2608.30114) — [src: web:arxiv.org] `[P]` preprint, 2026-08-31. An
  open 1.72B decoder-only model trained from scratch for Brazilian Portuguese, fully containerized, every comparison
  carrying a standard error and a paired test. Documents a concrete evaluation trap: converting a SentencePiece
  tokenizer with case-folding to the HuggingFace fast format silently drops the normalizer and sent LAMBADA-PT from
  45.3 to 25.0, invisible in aggregate metrics. Lucas: *"a gente TEM que olhar isso! não deixar pra mt longe"* (task in
  `brain/goals/local-ai.md` [manaca-1b]).

## IA e aprendizagem — o eixo novo de Tecnologias na Educação (2026-08-19)

Lidos e usados na aula 02; todos com número citável em sala.

- [Strömberg, Lei & Wu — The Generative AI Learning Penalty](https://conference.nber.org/conf_papers/f240545.pdf) — CEPR
  DP21577, 2026. 26.811 secundaristas chineses, 30 meses. Dever de casa **+18%** e tempo **−30%**; prova de livro
  fechado **−20%** em 6 meses; vestibular **−18 a −24%**, pior após ~2 anos. **Os melhores alunos perderam mais.** Quem
  usou IA mantendo esforço: perda mínima. É o dado mais forte que existe hoje para abrir uma aula sobre o assunto.
- [Choudhuri, Sanchez, Burnett & Sarma — Why Johnny Can't Think](https://arxiv.org/abs/2601.22430) — Oregon State,
  jan/2026, 299 alunos STEM em 5 universidades, PLS-SEM. Uso rotineiro + confiança em genAI → menos reflexão, menos
  necessidade de entender, menos pensamento crítico. **Tecnofilia, tolerância a risco e autoeficácia computacional
  aumentam a vulnerabilidade**; experiência prévia não protege. Chamam de *ciclo de dívida cognitiva*. Feito sob medida
  para uma turma de computação.
- [Doshi & Hauser — Generative AI enhances individual creativity but reduces the collective diversity of novel
  content](https://doi.org/10.1126/sciadv.adn5290) — Science Advances. Ideias de LLM deixam cada texto mais criativo **e
  todos mais parecidos entre si**. Dilema social. É o argumento honesto para "por que fazer design thinking antes de
  codar".
- [Caosun & Aral — The augmentation trap](https://arxiv.org/abs/2604.03501) — MIT Sloan, 2026. Ganho de produtividade de
  curto prazo corrói a expertise de que ele depende. Complemento, não lido na íntegra.
- [Epistemic authority and generative AI in learning spaces](https://doi.org/10.3389/feduc.2025.1647687) — Frontiers in
  Education 2025. Pista para o sub-eixo "crise da verdade".

## Definição de problema e disciplinas project-based (2026-08-19)

- [d.school — Point-of-View
  Madlib](https://futureofstuffchallenge.org/download/synthesize/bootleg-point-of-view-madlib.pdf) e o [handout de POV
  de Stanford](https://hci.stanford.edu/courses/dsummer/handouts/POV.pdf) — `[USER] needs to [NEED] because [SURPRISING
  INSIGHT]`. As regras que importam: *needs* são **verbos**; o insight **não pode ser a razão do need**; *"keep it sexy
  and hold the tension"*. O par ❌/✅ deles (comida nutritiva × risco social no bairro) é o melhor diagnóstico curto de um
  enunciado fraco. Base do MODELO novo da disciplina.
- [Stanford ME310 — wiki de missões 2025-26](https://our310.stanford.edu/index.php/Assignments/HomePage) — **a mina do
  desenho macro.** Missão = 🚀 data de lançamento + ✅ sub-entregas datadas com link de submissão, 16 no ano. Tem **Dark
  Horse Prototype** (fase obrigatória de perseguir a ideia arriscada — efeito wow institucionalizado), **SGM check-ins**
  (equipe apresenta e é obrigada a assistir à de outra) e contagem dura de contato com usuário (*"three new people"*). O
  relatório é **cumulativo** Fall→Winter→Spring, template Overleaf, e termina arquivado na biblioteca — projeto e artigo
  são a mesma peça crescendo. Ver também [Fall
  Documentation](https://our310.stanford.edu/index.php/Assignments/FallDocumentation), que nomeia os modos de falhar
  ("personas superficiais ou estereotipadas", "no cartoons please").
- [MIT NEET — instructor's guide (OCW
  SP.248)](https://ocw.mit.edu/courses/sp-248-the-neet-experience-fall-2025/pages/instructors-guide/) — declara a carga
  no papel: 60 min de aula + 120 min fora por semana.
- [Lim, Choi & Hong — Identify Design Problems Through Questioning](https://arxiv.org/abs/2409.07178) — KAIST, CSCW '24.
  Novatos definem problema mal porque **aceitam passivamente o feedback do professor**; treinar o *perguntar* corrige.
  Role-play com LLM reduziu a pressão social de perguntar — e gerou over-reliance.

## Simulação de população para pesquisa e para aula (2026-08-20)

- **MatrAIx / Persona 8B** (Harvard + MIT) — dataset de **8,3 bilhões de perfis digitais** montado a
  partir de dados reais e sintéticos, cobrindo psicologia, hábitos de consumo e estilo de vida (1290
  dimensões por persona). As personas interagem em surveys, chats, navegação e apps simulados;
  reportam mais de **18.000 trials** em comércio e saúde. Arquitetura anunciada em três blocos:
  construir a população → infraestrutura de avaliação com usuário simulado → tarefas e produtos de
  aplicação. Lucas, INBOX 2026-08-20: *"matraix deve entrar nas minhas aulas."*

  **Vale mais do que material de aula, e é aí que precisa de cuidado.** Um simulador de população é
  exatamente o instrumento que [`megatruth`](../papers/megatruth/CONTEXT.md) (agregação de verdade em
  multidão), [`2027-CHI-cria`](../papers/2027-CHI-cria/CONTEXT.md) (estudo de ideação com turma) e
  [`mechanism-search`](../papers/mechanism-search/CONTEXT.md) usariam para pilotar um desenho antes de
  gastar participantes reais — e é também exatamente o instrumento que **substitui evidência por
  plausibilidade** se alguém aceitar o resultado simulado como achado. Se entrar em qualquer um dos
  três, entra como *piloto de desenho*, nunca como dado.

  ⚠ Capturado de um carrossel de agregador, sem link para paper ou release; nada aqui foi verificado
  na fonte primária. Buscar a publicação de Harvard/MIT antes de citar ou de levar para sala.
  **A disciplina de destino ainda não foi decidida** — a nota do Lucas diz "minhas aulas" sem dizer
  qual, e `academy/teaching/` tem treze.

## Candidatos a substituir o vídeo do carrinho da IDEO (2026-08-19)

O carrinho ([ABC Nightline 1999, 22m03s](https://www.youtube.com/watch?v=izjhx17NuSE)) mostra o ciclo completo. Os
candidatos foram avaliados pelo *trabalho* que fazem, não pela estética.

- [Doug Dietz — The Design Thinking Journey](https://www.youtube.com/watch?v=mZWMj_H8Iqw) — TEDx 2019, **18m01s**
  (versão 2012: [19m47s](https://www.youtube.com/watch?v=jajduxPD6H4)). Projetou uma ressonância premiada, viu uma
  criança chorando a caminho dela, redesenhou **a sala** e não a máquina. **Satisfação do paciente +90%**
  ([fonte](https://thisisdesignthinking.net/2014/12/changing-experiences-through-empathy-ge-healthcares-adventure-series/)).
  ⚠️ a cifra famosa de sedação 80%→27% **não foi confirmada** — não usar sem checar. **Melhor substituto para uma aula
  de definição de problema**: mostra o momento em que o problema estava mal definido, não o processo.
- [Mark Rober — Backyard Squirrel Maze 1.0](https://www.youtube.com/watch?v=hFZFjoX2cGg) — 2020, **20m20s**. Iteração
  visível com falhas filmadas; o problema se reformula no meio. Sem usuário e sem empatia — serve à aula de
  **prototipação**, não à de problema.
- [Abstract (Netflix), episódios livres no YouTube](https://www.youtube.com/watch?v=q_k8fVNzbGU) — **46m49s**. Longo
  demais para aula; material de casa.

## Avaliação de disciplina: gamificação, nota, pares e painel (2026-09-03)

Todas revisadas por pares; o veículo em cada linha é o que diz o peso. Leitura de decisão:
`outputs/metodologia-disciplinas-sota.md`.

- [Sailer & Homner — Gamification of Learning: a Meta-analysis](https://doi.org/10.1007/s10648-019-09498-w) — *Educ
  Psych Review* 2020. g=.49 cognitivo, .36 motivacional, .25 comportamental. **Competição com colaboração** modera.
- [Li, Hew & Du — Gamification, motivação intrínseca e competência](https://doi.org/10.1007/s11423-023-10337-7) —
  *ETR&D* 2023, N=2500. Autonomia g=.638, vínculo g=1.776, **competência g=.277** — o elo fraco.
- [Rodrigues et al. — novelty effect e familiarization effect](https://doi.org/10.1186/s41239-021-00314-6) — *IJETHE*
  2021, **CS1 brasileiro, N=756, 14 semanas**. Curva em U: cai na 4ª semana, volta entre a 6ª e a 10ª.
- [Rogers & Feller — Discouraged by Peer Excellence](https://doi.org/10.1177/0956797615623770) — *Psychological
  Science* 2016, N=5.740, MOOC **com avaliação por pares**. Ver a entrega excelente do colega fez desistir do curso.
- [Sinha & Kapur — Productive Failure](https://doi.org/10.3102/00346543211019105) — *Review of Educ Research* 2021, 53
  estudos. Resolver **antes** de ensinar bate ensinar antes: g=.36 (.87 corrigido). Inverte para habilidade genérica.
- [Kalyuga — Expertise Reversal Effect](https://doi.org/10.1007/s10648-007-9054-3) — *Educ Psych Review* 2007. O
  andaime que ajuda o novato atrapalha quem já sabe: não há "um modo geral" de capacitar, há regra por nível.
- [Hackerson et al. — Alternative grading in undergraduate STEM: scoping
  review](https://doi.org/10.1186/s43031-024-00106-8) — *DISER* 2024. Specs/contract/mastery: populares, **evidência
  de resultado escassa** e sem consenso teórico. Adotar é desenho, não conclusão.
- [Panadero & Jonsson et al. — Effects of Rubrics: meta-analytic review](https://doi.org/10.1007/s10648-023-09823-4) —
  *Educ Psych Review* 2023. Desempenho g=.45; **nº de critérios e de níveis não moderou**.
- [Double, McGrane & Hopfenbeck — Peer Assessment on Academic
  Performance](https://doi.org/10.1007/s10648-019-09510-3) — *Educ Psych Review* 2020, 54 estudos. g=.31 contra nada e
  **g=.28 contra a avaliação do professor**.
- [Falchikov & Goldfinch — Peer and Teacher Marks](https://doi.org/10.3102/00346543070003287) — *Review of Educ
  Research* 2000, 48 estudos. O par bate com o professor em **julgamento global sobre critérios bem entendidos**.
- [Abuzied & Nabag — Structured viva: validade e confiabilidade](https://doi.org/10.1186/s12909-023-04524-6) — *BMC Med
  Educ* 2023. Banca com folha de critérios α=.75–.80; banca solta α=.50.
- [Paulsen & Lindsay — painéis para o estudante](https://doi.org/10.1007/s10639-023-12401-4) — *Educ Inf Technol* 2024.
  O painel útil é guiado por teoria de aprendizagem, não por log de LMS.
- [Kaliisa et al. — Have Learning Analytics Dashboards Lived Up to the
  Hype?](https://doi.org/10.1145/3636555.3636884) — *LAK '24*. **Localizada, não lida** (dl.acm.org recusa): ler antes
  de citar.
- [Cameron, Banko & Pierce — Pervasive negative effects of rewards on intrinsic motivation: the myth
  continues](https://doi.org/10.1007/BF03392017) — *The Behavior Analyst* 24:1–44, 2001. A fronteira que decide o XP:
  o dano aparece com recompensa **tangível, prometida antes e frouxamente ligada ao desempenho**; quando é **ligada ao
  nível atingido**, a motivação intrínseca sobe ou não muda. Contestado por Deci, Koestner & Ryan (1999).
- [Gorbunova, van Merriënboer & Costley — Are Inductive Teaching Methods Compatible with Cognitive Load
  Theory?](https://doi.org/10.1007/s10648-023-09828-z) — *Educ Psych Review* 35:111, 2023. Descreve **oito sequências**
  de problema e instrução e conclui que ao menos seis são compatíveis com carga cognitiva. Tira a pergunta de
  "qual campo" e põe em "qual sequência, para qual objetivo e qual aluno".
