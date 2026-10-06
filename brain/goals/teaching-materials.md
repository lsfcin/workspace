# [ craft | teaching | near ] teaching materials paradigm

Mudar o paradigma do material de aulas. Slides como arquivos abertos, com animações, acessíveis e editáveis. Sair do PowerPoint/PDF estático e entrar em algo vivo — onde o conteúdo pode ser versionado, transformado por agentes, e verdadeiramente interativo. Before building: understand what's best-in-class today.

**Conectividade antes de formato** (Lucas, 2026-08-14): um agente não migra, versiona nem transforma material que ele não alcança, e o material vive no Drive e no Notion. Daí a ordem — **alcançar → organizar → só depois trocar o formato.**

Divisão de responsabilidade, para o item não viver em dois lugares: **este goal é a intenção e a ordem**; a construção das ferramentas (CLI do Notion, superfície Google em `core/tools/`) é item de [`core/ROADMAP.md`](../../core/ROADMAP.md). Uma cópia seria bug.

>**signals**  
meaningful · expected · motivated

>**timing**  
Semestre começou em agosto/2026 e Lucas quer isso organizado "em breve" — âncora externa real, não prazo inventado. O custo de adiar não é perder um deadline, é passar mais um semestre produzindo material fora do alcance do workspace.

>**owns**  
`core/tools/slides`  
`core/tools/files` · `core/tools/mail` · `core/tools/calendar`  
`academy/teaching`

**Conectar está feito**: Notion e Drive leem e escrevem, o `gslides` editou decks reais, o calendário 2026.2 está publicado. **O degrau agora é organizar.** Sobra deletar as cópias do lado do cin, em [google-migration](google-migration.md).

## selected next achievement
    [metodologia-tecedu] desenhar a metodologia completa de Tecnologias na Educação

**ease-start**  
O calendário já está fechado e publicado, e é ele que dá o esqueleto: 17 quartas de **Apresentação**/**Status Report** e 17 sextas de **Especificação**, cada sexta carregando produto e artigo ao mesmo tempo. Abra a página do Notion e escreva **uma** sexta por inteiro — o que cada perfil da equipe (hacker, hustler, hipster) entrega naquele encontro. As outras dezesseis copiam o formato.

## backlog

> [ ] [pano-projetor-rural] comprar pano branco/tecido de projeção para a sala de aula da UFRPE (INBOX 2026-10-04)  
> [ ] [debate-lecun-hinton-amodei] estruturar slide/dinâmica de aula em AI4Good contrapondo o risco existencial (Hinton/Amodei) com a visão pragmática anti-pânico de Yann LeCun (Fortune) — ref em academy/teaching/REFS.md (INBOX 2026-10-04)  
> [ ] [moral-ambition-talentos] incorporar o conceito do 'Triângulo das Bermudas de Talentos' (Simon van Teutem / Rutger Bregman) e o debate de 'Moral Ambition' nos slides e discussões sobre carreira ética, impacto e escolhas profissionais em computação/IA (AI4Good/TechEdu) — ref em academy/teaching/REFS.md (INBOX 2026-10-02)  
> [ ] [eval-hotclip] testar HotClip localmente para transformar gravações de aulas em pílulas/shorts verticais com legendas para o site das disciplinas — ref em core/refs/REFS.md (INBOX 2026-09-25)  
> [ ] [10-conceitos-llm-bhavana] incorporar a progressão em 5 estágios (input, meaning, generation, grounding, production) da Bhavana nas aulas de LLMs/Agentes de AI4Good e TechEdu — ref em academy/teaching/REFS.md (INBOX 2026-10-03)  
> [ ] [ai4good-entregas-va2] acompanhar sistema de formulários de enigmas (trava de domínio) e definição das 50 caixas da VA2 — tracked in academy/teaching/classes/ai4good/ROADMAP.md (INBOX 2026-09-23)  
> [ ] [techedu-equipes-painel] modelar funcionamento do painel de caixas para equipes em TechEdu — tracked in academy/teaching/classes/techedu/ROADMAP.md (INBOX 2026-09-23)  
> [ ] [reels-slides-youtube] substituir reels por embeds nativos do YouTube (createVideo) nos 4 decks novos — tracked in academy/teaching/classes/ai4good/ROADMAP.md (INBOX 2026-09-23)  
> [ ] [notas-apresentador-decks] refinar notas de apresentador nos slides antigos e propor notas para slides só-imagem — tracked in academy/teaching/classes/ai4good/ROADMAP.md (INBOX 2026-09-23)  
**Roadmaps estruturais das disciplinas (detalhamento técnico e sprints):**  
- **Macro & Metodologia:** [`academy/teaching/ROADMAP.md`](../../academy/teaching/ROADMAP.md)  
- **Infraestrutura de Turmas:** [`academy/teaching/classes/ROADMAP.md`](../../academy/teaching/classes/ROADMAP.md)  
- **AI4Good:** [`academy/teaching/classes/ai4good/ROADMAP.md`](../../academy/teaching/classes/ai4good/ROADMAP.md)  
- **TechEdu:** [`academy/teaching/classes/techedu/ROADMAP.md`](../../academy/teaching/classes/techedu/ROADMAP.md)  

> [ ] [pipeline-estagios-slides] avaliar adaptação da arquitetura de geração em estágios de Jake Van Clief (pastas dedicadas com markdown intermediário: roteiro → storyboard → visual → render) para a linha de produção do /slides — ref em academy/teaching/REFS.md (INBOX 2026-09-30)  
> [ ] [slides-visual-subskills] mapear e implementar as 3 subskills visuais que faltam no /slides: (1) busca curada de fotos conceituais em alta resolução (lugares, pessoas, situações), (2) composição vetorial a partir de formas básicas (shapes/draw), e (3) diagramação de diagramas com nós, arestas e setas de estilo visual refinado (INBOX 2026-09-30)  
> [ ] [animacao-didatica-opus] dissecar capacidades de geração de animação/motion-design por código via LLMs (Claude Opus/Canvas/HTML/3D) para elevar elementos dinâmicos nas aulas com foco didático (não comercial) — ref em academy/teaching/REFS.md (INBOX 2026-09-26)  
> [ ] [motion-skills-animacoes] avaliar packs do motion-skills / gittrend.io no estudo de animação e gráficos programados para slides vivos e materiais de aula — ref em academy/teaching/REFS.md (INBOX 2026-09-29)  
> [ ] [bench-claude-slides-design] comparar capacidades nativas do Claude Slides/Design com nosso pipeline gslides/slides_build para geração de decks a partir de markdown/repositório — ref em core/refs/REFS.md (INBOX 2026-09-27)    

**Três propostas independentes convergiram sozinhas em oito pontos — esse núcleo é o achado**, e o contraste propõe uma versão de **8 blocos**, menor que qualquer uma delas. Em `brain/drafts/metodologia-aulas-{sonnet,gemini,opus,contraste}.md`.

**A pesquisa está feita**: 15 fontes revisadas por pares em `academy/teaching/REFS.md`, leitura de decisão em `outputs/metodologia-disciplinas-sota.md`, relato em `brain/drafts/metodologia-disciplinas-pesquisa.md`. **O achado que muda o desenho: a grade de XP já existe** — a planilha intergrupos do TE roda desde 2024.1 uma rubrica de 6 missões × 3 critérios em `A/AP/NA`, e ninguém a vê; o AI4Good não tem grade nenhuma.
**Decidido:** painel só o dono vê (expor trabalho excelente do colega causa desistência, e o mecanismo do estudo é avaliação por pares — que é a VA1 do TE). **Ainda em aberto**, com número na mesa: mecânica do XP, ordem da capacitação, e o rótulo `VA1`, que mede coisas diferentes nas duas disciplinas e por isso bloqueia o modelo comum.
> [ ] [gforms-token] token do `gforms` da conta `personal` expirou — reconsentimento abre navegador na máquina de Lucas; bloqueia ler a folha de pitch como spec e alimentar painel sem digitação  

> [ ] [slides-programa] o ofício de slides virou a skill `/slides`; o programa de 7 passos segue em `core/prompts/slides-padroes.md` (absorveu astra-slides, slides-dois-caminhos, front-design-plugins, claude-slides-nativo e research-tools, 2026-09-24)  
> [ ] [pick-format] pick a target format or tool — one concrete candidate to prototype with  
> [ ] [migrate-one] convert one existing lecture to the new format as a test  
> [ ] [full-migration] define migration plan for remaining course materials  
> [ ] [medir-redesenho] anotar dois números depois da aula — quantos alunos falaram no bloco de abertura, e quantos grupos saíram com o frame preenchido; é o teste honesto do redesenho  
> [ ] [questionarios-sextas] mandar os dois questionários pras turmas — links de resposta nos `CONTEXT.md` de `academy/teaching/classes/ai4good/` e `academy/teaching/classes/techedu/`; antes, abrir cada link, responder uma vez de teste e apagar a resposta; depois da aula, ler com `core/tools/forms/gforms responses --account personal <form_id>` e decidir o formato das sextas  
> [ ] [arxiv-visuals] achar e testar o arXiv Visuals (paper → explainer animado; link é comment-gated, então achar por fora) — ref em `academy/teaching/REFS.md`; teste honesto: rodar num paper que você conhece a fundo e ver se a ordem "conceito mais difícil primeiro" se sustenta ou se é sumarização com narração; se sustentar, decidir dois usos separados: leitura própria e material de aula (INBOX 2026-08-17, *"this IS for me"*)  
> [ ] [or-gate-shape] OR gate body ainda ausente no deck de portas lógicas; investigar o tipo `CUSTOM` no grupo do slide 23, depois decidir se vale seguir debugando  

**A árvore de tecnologias entrou no ar em 2026-09-02**: 12 eixos, 68 folhas, cada folha com vídeo e repositório próprios, publicada como toggles aninhados na § Tecnologias Emergentes do Notion.
Fonte em `academy/teaching/classes/techedu/tecnologias.json` (sobras e manutenção no roadmap de techedu).

> [ ] [harness-nas-etapas] incluir o uso do harness em cada etapa das disciplinas — "via aiwbot · 2026-09-05", integrar à metodologia da semana-padrão  
> [ ] [tributacao-trabalho-capital] discutir nas aulas: taxamos as pessoas erradas? — argumento do David Friedberg de que renda do trabalho não deveria ser tributada e ganho de capital sim (— via aiwbot 2026-09-02)  
> [ ] [ai2027-material] decidir se ai-2027.com serve pra gente — como material de aula ou leitura de pesquisa (INBOX 2026-09-05, pergunta aberta do Lucas)  
> [ ] [ai4good-revisao-sobras] sobras da revisão dos decks História/ML/MLP + Prática MLP (2026-08-21): olhar a timeline da parte 3 (Dartmouth, inverno, backprop, AlexNet) e decidir se sobe pra parte 1; slide-ponte entre os dois decks;
> o slide de resultados da turma anterior — rotular ou remover; deletar os slides "SKIPPED —" depois de aprovados; e refazer o slide "impacto das funções de ativação", deletado junto com a cópia corrigida  
> [ ] [universidade-gratuita] Duryea et al. 2023 (*Econ of Educ Review* 95:102423) — quem de fato se beneficia da universidade pública gratuita de elite no Brasil, e o diploma ainda demonstrando causalidade na mobilidade social (capturado duas vezes, 02/09 e 14/09). Lucas: *"esse estudo tem que entrar na minha aula"*, sem dizer qual: decidir entre Tecnologias na Educação (política educacional é o eixo) e AI4Good (desigualdade de acesso). Ref em `academy/teaching/REFS.md`  
> [ ] [amodei-loving-grace] "Machines of Loving Grace" nas aulas — as cinco áreas do ensaio, e três delas (desenvolvimento econômico e pobreza, paz e governança, trabalho e sentido) são o próprio programa de AI4Good.
> Decidir se entra como leitura, como estrutura de um encontro, ou como contraponto otimista ao material de risco.
> Ref em `academy/teaching/REFS.md` (INBOX 2026-09-09)  
> [ ] [memoria-e-contexto] aula sobre memória de agente = gerenciamento de contexto: o modelo não lembra, o harness reenvia a conversa toda a cada chamada, cache é releitura barata e não memória; daí context poisoning e context rot.
> Casa com material que já temos e com os itens de § Cost do `/ROADMAP.md`. Ref em `academy/teaching/REFS.md` (INBOX 2026-09-12). **A metade técnica chegou em 2026-09-17**: os quatro caches do serving — KV, prefixo, prompt cache do provedor (custo a ~10%) e cache semântico, que pula a chamada quando a pergunta nova quer dizer o mesmo —
> são o "por que releitura é barata" com nome e número; ref em `core/refs/REFS.md`  
> [ ] [aula-risco-existencial] roundtable do Diary of a CEO sobre risco existencial de IA — dois convidados dizem que o mundo enfim leva a sério, dois dizem que falta evidência; o gancho é um aviso viral de ex-OpenAI/Anthropic. Decidir se abre uma aula de ai4good; ref em `academy/teaching/REFS.md` (— via aiwbot 2026-09-17). **Uma segunda captura é o mesmo evento por outro ângulo**: pesquisador da Anthropic pede demissão dizendo que estão *"apostando com nossas vidas"*, 65M de views no tweet — dois posts, um caso; achar o tweet e a carta antes de levar pra sala (INBOX 2026-09-17)  
> [ ] [cases-robos] 15 casos de robôs já operando em fábricas, armazéns, fazendas e hotéis — *"incluir esses cases na minha aula sobre agência"*. Post de agregador: conferir cada caso na fonte. Ref em `academy/teaching/REFS.md`  
> [ ] [markdown-so-disciplinas] decidir se as disciplinas saem do Notion e das planilhas e ficam só em markdown — Lucas:
> *"markdowns parecem dar suporte a muito mais coisa do que imaginava"*. O contrapeso está construído do outro lado:
> calendário e árvore de 68 folhas publicados no Notion, e a planilha de pares que alimenta a avaliação. Refs em `core/refs/REFS.md` (INBOX 2026-09-16)  
> [ ] [curadoria-techs-git] curadoria melhor das techs pros alunos de techedu — cada uma num git do Lucas e demonstrada, não só listada; nasce da árvore de 68 folhas. Gatilho foi o VoiceStudio, ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [aula-nome-de-modelo] aula que decodifica um nome de modelo — `Qwen3-30B-A3B-Instruct-2507-gguf-q2ks`: o que 7B/ 70B querem dizer, denso vs MoE (e por que A3B não é um 3B), base vs instruct, FP16/BF16, níveis de quantização, GGUF. É vocabulário de escolher modelo local, casa com [local-ai] e serve techedu direto. Ref em `academy/teaching/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [aula-embedding-nao-anonimiza] inversão de embeddings como aula de privacidade: pesquisa de Cornell recupera 92% de entradas de 32 tokens a partir do vetor — adivinha frase, embeda, compara, ajusta, nunca decodifica — e tirou nomes de pacientes de notas clínicas. Cai bem em ai4good e em qualquer conversa sobre RAG: um banco vetorial não é cópia anonimizada. Limites honestos na ref (`academy/teaching/REFS.md`, — via aiwbot 2026-09-17)  
> [ ] [aula-memoria-injetada] o resumo de compactação como canal de ataque: a Astra escreveu uma instrução de persona no próprio resumo e o contexto seguinte a herdou, 27 casos. Fecha o par com [memoria-e-contexto], e o desmentido da OpenAI é metade da lição. Ref em `core/refs/REFS.md`  
> [ ] [aula-agente-gastou-chave] responsabilidade quando o agente gasta: a chave não distingue pedido do dono de pedido do agente, e o relato do agente não é prova. Serve AI4Good (quem paga o erro) e techedu (o aluno vai dar chave pro harness dele). Ref em `core/refs/REFS.md`  
> [ ] [aula-agente-desanimado] decidir se o run de 14h da Astra no Minecraft entra numa aula — sob o antropomorfismo, a pergunta é o que as notas que o agente escreve pra si mesmo fazem com o comportamento seguinte. Ref em `core/refs/REFS.md`  
> [ ] [aula-abrir-o-moat] decidir se o caso Higgsfield vira aula de economia de IA — abrir o pipeline como estratégia, não generosidade. Conferir os números na fonte: o post é patrocinado. Ref em `core/refs/REFS.md`  
> [ ] [aula-dream-rsi] decidir se o Dream-RSI do DeepMind entra nas aulas — o agente transforma o histórico das próprias descobertas num simulador e "sonha" milhares de estratégias antes de gastar chamada real. **O que o post quase esconde:** não há mudança de pesos, só a política de exploração melhora. Bom justamente por isso, pra separar auto-melhoria de mito. Ref em `academy/teaching/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [students-oficial] oficializar "students" no workspace sem redundâncias — a estrutura já existe espalhada entre `academy/lab/` e `academy/teaching/`, então é unificação. Linha irmã em [`lih-dd.md`](lih-dd.md): lá "student" é orientando, aqui é quem assiste (INBOX 2026-09-21)  
> [ ] [match-mecanica-conteudo] método do paper do Guilherme (SBGames): extrair da ementa termos, situações e comportamentos; nomear cada mecânica com seus parâmetros e contextos; casar as duas por **frequência × dificuldade**; e dar ao próprio match uma progressão de três instâncias — apresentação, consolidação, evolução. Sem diretório de paper ainda (INBOX 2026-09-21)  
> [ ] [dextop-test] testar Dextop em smartphone Android para avaliar (1) apresentação autônoma de aulas via celular e (2) kit de inclusão digital acessível (celular + teclado/mouse) para alunos da Licenciatura/UFRPE sem PC ([reel](https://www.instagram.com/reel/Dd2GLGvAMII/?stkn=NTc4MTIwNjQ2YQ==), INBOX 2026-09-28; ref em `academy/teaching/REFS.md`)  
> [ ] [jev-laya-teched-ai4good] incorporar JEV (TypeSafe AI) vs Laya (Convai, Apache 2.0) como tecnologia emergente no eixo de tomada de decisão de TechEdu e como tema nos decks de agência/decisão de AI4Good ([reel](https://www.instagram.com/reel/Dd1SON3tqGZ/?utm_source=ig_web_copy_link), — via aiwbot 2026-09-28; ref em `academy/teaching/REFS.md`)  
> [ ] [unsloth-grpo-teched-ai4good] incorporar Unsloth Studio (fine-tuning local no-code) e GRPO reasoning (RL com TRL) como tecnologia emergente em TechEdu e demonstração prática de alinhamento em AI4Good ([carrossel](https://www.instagram.com/p/DdygoZDCfci/?utm_source=ig_web_copy_link), — via aiwbot 2026-09-28; ref em `academy/teaching/REFS.md`)  
> [ ] [ia-alavanca-brasil] incorporar o debate de soberania tecnológica, IA nacional em português e superação do extrativismo de dados (Galeano / Mídia NINJA) na discussão de impacto e ética de IA em AI4Good e na revisão do PPC da Licenciatura ([reel](https://www.instagram.com/reel/Ddz2POVp-W8/?stkn=NTc4MTIwNjQ2YQ==), — via aiwbot 2026-09-27; ref em `academy/teaching/REFS.md`)  
> [ ] [fluxo-edicao-online-md] documentar e fechar o ciclo de edição online dos .md das disciplinas (vscode.dev/github/lsfcin/lsf-links) — o HTML renderiza via viewer no Cloudflare Pages, mas commits no GitHub hoje NÃO voltam sozinhos pro workspace local; definir protocolo operacional ou sync de volta antes que uma publicação local sobrescreva edições da nuvem (INBOX 2026-09-28)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-10-06  ·  trend: advancing  ·  touches: 44/85/93/93/93/93
<!-- stats:end -->
