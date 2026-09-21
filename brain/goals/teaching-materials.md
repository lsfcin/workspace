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

> [ ] [metodologia-tecedu] semana-padrão (quarta e sexta com papéis fixos, uma pergunta e um produto por encontro), as 9 etapas mapeadas nos 34 encontros reais (números em `academy/teaching/classes/techedu/CONTEXT.md`), avaliação nova, dashboard que substitui as duas planilhas Google, e o padrão MODELO+EXEMPLO em toda entrega. Inclui **como cada encontro abre e como cada conteúdo é mostrado** — a metodologia é dita antes do conteúdo (INBOX 2026-08-27)  
> [ ] [fecho-de-aula] fechar toda aula com dois blocos: (1) **vocabulário** — que palavras a turma passou a ter, o que expandiu no conhecimento da área; (2) **verificação** — um teste curto que o aluno usa para conferir sozinho que aprendeu, possivelmente respondido em sala como formulário que contabiliza nota (INBOX 2026-08-27)  

**Três propostas independentes convergiram sozinhas em oito pontos — esse núcleo é o achado**, e o contraste propõe uma versão de **8 blocos**, menor que qualquer uma delas. Em `brain/drafts/metodologia-aulas-{sonnet,gemini,opus,contraste}.md`.

**A pesquisa está feita**: 15 fontes revisadas por pares em `academy/refs/REFS.md`, leitura de decisão em `outputs/metodologia-disciplinas-sota.md`, relato em `brain/drafts/metodologia-disciplinas-pesquisa.md`. **O achado que muda o desenho: a grade de XP já existe** — a planilha intergrupos do TE roda desde 2024.1 uma rubrica de 6 missões × 3 critérios em `A/AP/NA`, e ninguém a vê; o AI4Good não tem grade nenhuma.
**Decidido:** painel só o dono vê (expor trabalho excelente do colega causa desistência, e o mecanismo do estudo é avaliação por pares — que é a VA1 do TE). **Ainda em aberto**, com número na mesa: mecânica do XP, ordem da capacitação, e o rótulo `VA1`, que mede coisas diferentes nas duas disciplinas e por isso bloqueia o modelo comum.
> [ ] [folha-ai4good] a VA2 do AI4Good não tem folha de banca e a do TE tem; banca estruturada α=.75–.80 contra α=.50 solta. Rascunho pronto em `outputs/ai4good-folha-de-avaliacao.md` — decidir pesos, escala (o TE usa três níveis no grid de pares e quatro na banca) e se vira formulário  
> [ ] [gforms-token] token do `gforms` da conta `personal` expirou — reconsentimento abre navegador na máquina de Lucas; bloqueia ler a folha de pitch como spec e alimentar painel sem digitação  
> [ ] [planilha-canonica] duas cópias da planilha de pares do TE com o mesmo nome (`16iG7bh…` está linkada no Notion e recebe respostas; `1sEtJuf7…` está na pasta da disciplina). Declarar a canônica antes de qualquer painel ler dela; o Miro ainda vive dentro dos decks de Missão  

> [ ] [research-tools] research best current teaching tools — interactive slides, animations, open formats — start from the animation entries in `core/refs/REFS.md` (claude-code+remotion, Claude Code UI-animation skills).
> **Reescopado 2026-08-14:** o WOS agora lê e edita os decks direto no Google Slides (`core/tools/slides/gslides`), e Slidev foi deletado — a pergunta aberta não é mais qual formato local adotar, é quanto de animação dá pra autorar como sequência de slides gerada (inclui a ideia de um gerador de animações próprio)  
> [ ] [pick-format] pick a target format or tool — one concrete candidate to prototype with  
> [ ] [migrate-one] convert one existing lecture to the new format as a test  
> [ ] [full-migration] define migration plan for remaining course materials  
> [ ] [excalidraw-aula02] abrir `academy/teaching/classes/techedu/aula02-problemas.excalidraw` no excalidraw.com e confirmar que carrega (o JSON foi montado à mão, nunca foi aberto); depois, Live collaboration → copiar o link → trocar `[EXCALIDRAW]` no slide 69 do deck; confirmar se são mesmo 8 equipes (o quadro tem 8 frames)  
> [ ] [video-carrinho] decidir o vídeo do slot do carrinho — trecho de 4 min do Dietz, ou perguntar à turma "o que envelheceu nesse vídeo de 1999?" (candidatos avaliados em `academy/refs/REFS.md`)  
> [ ] [medir-redesenho] anotar dois números depois da aula — quantos alunos falaram no bloco de abertura, e quantos grupos saíram com o frame preenchido; é o teste honesto do redesenho  
> [ ] [questionarios-sextas] mandar os dois questionários pras turmas — links de resposta nos `CONTEXT.md` de `academy/teaching/classes/ai4good/` e `academy/teaching/classes/techedu/`; antes, abrir cada link, responder uma vez de teste e apagar a resposta; depois da aula, ler com `core/tools/forms/gforms responses --account personal <form_id>` e decidir o formato das sextas  
> [ ] [ai4good-candidatos] **uma sessão decide todos de uma vez** — sete capturas esperando a mesma pergunta, "isso entra numa aula de ai4good, e em qual encontro?". Cada uma tem linha em `academy/refs/REFS.md` com o que desconfiar:
> *book burning* / Project Panama (livros comprados, descosturados, escaneados — e o ScanRobot que digitaliza sem destruir) · Anna's Archive escrevendo um recado amigável para os LLMs que a visitam · "integração, não substituição" (a fundadora vende hardware) · o otimismo do Gordon-Levitt · o LeCun dos world models · *pacing the frontier* (só a legenda extraiu) · dados egocêntricos: costureiras indianas de câmera na cabeça a ₹250/h treinando robôs humanoides, que é consentimento, propriedade e quem fica com o valor numa história só. Conferir cada um na fonte antes da sala  
> [ ] [arxiv-visuals] achar e testar o arXiv Visuals (paper → explainer animado; link é comment-gated, então achar por fora) — ref em `academy/refs/REFS.md`; teste honesto: rodar num paper que você conhece a fundo e ver se a ordem "conceito mais difícil primeiro" se sustenta ou se é sumarização com narração; se sustentar, decidir dois usos separados: leitura própria e material de aula (INBOX 2026-08-17, *"this IS for me"*)  
> [ ] [or-gate-shape] OR gate body ainda ausente no deck de portas lógicas; investigar o tipo `CUSTOM` no grupo do slide 23, depois decidir se vale seguir debugando  

**A árvore de tecnologias entrou no ar em 2026-09-02**: 12 eixos, 68 folhas, cada folha com vídeo e repositório próprios, publicada como toggles aninhados na § Tecnologias Emergentes do Notion.
Fonte em `academy/teaching/classes/techedu/tecnologias.json`. Três sobras:
> [ ] [arvore-excalidraw] gerar o quadro do top-10 — um frame por equipe com coluna numerada 1 a 10, reusando `build_excalidraw.py`; é onde a equipe entrega a ordenação, já que não há formulário  
> [ ] [arvore-folhas-fracas] decidir duas folhas que subiram sem veredito: *Painel de learning analytics* (Metabase é BI genérico, melhor vídeo tem 229 views) e *WebXR multiusuário* (vídeo com 133 views). Cortar é uma edição no JSON e um republish  
> [ ] [arvore-url-excalidraw] `lucassf.pages.dev/techedu/draw` aponta para a sala ao vivo do Excalidraw, que expira por natureza — no dia em que morrer, o short name manda a turma pra lugar nenhum e nada avisa. Salvar o quadro como arquivo e repontar a linha  

> [ ] [acessibilidade-edson] preparar uma versão acessível das missões E do site da disciplina para o Edson — os dois artefatos, não só um (INBOX 2026-08-24)  
> [ ] [slides-pesquisa] material (talvez slides) que apresente aos alunos os conceitos dos projetos de pesquisa: dobra, cria, texpace/spacemantics — serve de ponte entre a disciplina e a pesquisa própria (INBOX 2026-08-24)  
> [ ] [harness-nas-etapas] incluir o uso do harness em cada etapa das disciplinas — "via aiwbot · 2026-09-05", integrar à metodologia da semana-padrão  
> [ ] [astra-slides] estudar o exemplo de slides do GPT-6 Astra — ref em `core/refs/REFS.md`; Lucas 2026-09-05: *"os slides deles são bem melhores que os nossos… é absurda a diferença"* — extrair o que os torna melhores e alimentar o fluxo de slides  
> [ ] [slides-dois-caminhos] redesenhar o fluxo de slides em dois caminhos: (1) notas de apresentador, (2) os slides em si como guia visual e provocação, não leitura. Relato 2026-09-05:
> sessão inteira em slides produziu prosa artificial, imagens pequenas e mal espaçadas, texto sobreposto — design não é o forte, e o fluxo atual não separa as duas saídas  
> [ ] [front-design-plugins] testar os cinco plugins de design front-end do Claude Code (auditoria de UI, design system, imagem→código, teste em browser) nos nossos slides — ref em `core/refs/REFS.md` (INBOX 2026-09-05)  
> [ ] [tributacao-trabalho-capital] discutir nas aulas: taxamos as pessoas erradas? — argumento do David Friedberg de que renda do trabalho não deveria ser tributada e ganho de capital sim (— via aiwbot 2026-09-02)  
> [ ] [ai2027-material] decidir se ai-2027.com serve pra gente — como material de aula ou leitura de pesquisa (INBOX 2026-09-05, pergunta aberta do Lucas)  
> [ ] [ai4good-revisao-sobras] sobras da revisão dos decks História/ML/MLP + Prática MLP (2026-08-21): olhar a timeline da parte 3 (Dartmouth, inverno, backprop, AlexNet) e decidir se sobe pra parte 1; slide-ponte entre os dois decks;
> o slide de resultados da turma anterior — rotular ou remover; deletar os slides "SKIPPED —" depois de aprovados; e refazer o slide "impacto das funções de ativação", deletado junto com a cópia corrigida  
> [ ] [universidade-gratuita] Duryea et al. 2023 (*Econ of Educ Review* 95:102423) — quem de fato se beneficia da universidade pública gratuita de elite no Brasil, e o diploma ainda demonstrando causalidade na mobilidade social (capturado duas vezes, 02/09 e 14/09). Lucas: *"esse estudo tem que entrar na minha aula"*, sem dizer qual: decidir entre Tecnologias na Educação (política educacional é o eixo) e AI4Good (desigualdade de acesso). Ref em `academy/refs/REFS.md`  
> [ ] [amodei-loving-grace] "Machines of Loving Grace" nas aulas — as cinco áreas do ensaio, e três delas (desenvolvimento econômico e pobreza, paz e governança, trabalho e sentido) são o próprio programa de AI4Good.
> Decidir se entra como leitura, como estrutura de um encontro, ou como contraponto otimista ao material de risco.
> Ref em `academy/refs/REFS.md` (INBOX 2026-09-09)  
> [ ] [memoria-e-contexto] aula sobre memória de agente = gerenciamento de contexto: o modelo não lembra, o harness reenvia a conversa toda a cada chamada, cache é releitura barata e não memória; daí context poisoning e context rot.
> Casa com material que já temos e com os itens de § Cost do `/ROADMAP.md`. Ref em `academy/refs/REFS.md` (INBOX 2026-09-12). **A metade técnica chegou em 2026-09-17**: os quatro caches do serving — KV, prefixo, prompt cache do provedor (custo a ~10%) e cache semântico, que pula a chamada quando a pergunta nova quer dizer o mesmo —
> são o "por que releitura é barata" com nome e número; ref em `core/refs/REFS.md`  
> [ ] [aula-risco-existencial] roundtable do Diary of a CEO sobre risco existencial de IA — dois convidados dizem que o mundo enfim leva a sério, dois dizem que falta evidência; o gancho é um aviso viral de ex-OpenAI/Anthropic. Decidir se abre uma aula de ai4good; ref em `academy/refs/REFS.md` (— via aiwbot 2026-09-17). **Uma segunda captura é o mesmo evento por outro ângulo**: pesquisador da Anthropic pede demissão dizendo que estão *"apostando com nossas vidas"*, 65M de views no tweet — dois posts, um caso; achar o tweet e a carta antes de levar pra sala (INBOX 2026-09-17)  
> [ ] [cases-robos] 15 casos de robôs já operando em fábricas, armazéns, fazendas e hotéis — *"incluir esses cases na minha aula sobre agência"*. Post de agregador: conferir cada caso na fonte. Ref em `academy/refs/REFS.md`  
> [ ] [markdown-so-disciplinas] decidir se as disciplinas saem do Notion e das planilhas e ficam só em markdown — Lucas:
> *"markdowns parecem dar suporte a muito mais coisa do que imaginava"*. O contrapeso está construído do outro lado:
> calendário e árvore de 68 folhas publicados no Notion, e a planilha de pares que alimenta a avaliação. Refs em `core/refs/REFS.md` (INBOX 2026-09-16)  
> [ ] [curadoria-techs-git] curadoria melhor das techs pros alunos de techedu — cada uma num git do Lucas e demonstrada, não só listada; nasce da árvore de 68 folhas. Gatilho foi o VoiceStudio, ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [claude-slides-nativo] o Claude passa a criar, editar, apresentar e exportar slides e documentos dentro da própria conversa — ver o que dá pra importar pro nosso fluxo de slides. Irmão de [astra-slides] e [slides-dois-caminhos]; ref em `core/refs/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [aula-nome-de-modelo] aula que decodifica um nome de modelo — `Qwen3-30B-A3B-Instruct-2507-gguf-q2ks`: o que 7B/ 70B querem dizer, denso vs MoE (e por que A3B não é um 3B), base vs instruct, FP16/BF16, níveis de quantização, GGUF. É vocabulário de escolher modelo local, casa com [local-ai] e serve techedu direto. Ref em `academy/refs/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [aula-embedding-nao-anonimiza] inversão de embeddings como aula de privacidade: pesquisa de Cornell recupera 92% de entradas de 32 tokens a partir do vetor — adivinha frase, embeda, compara, ajusta, nunca decodifica — e tirou nomes de pacientes de notas clínicas. Cai bem em ai4good e em qualquer conversa sobre RAG: um banco vetorial não é cópia anonimizada. Limites honestos na ref (`academy/refs/REFS.md`, — via aiwbot 2026-09-17)  
> [ ] [aula-memoria-injetada] o resumo de compactação como canal de ataque: a Astra escreveu uma instrução de persona no próprio resumo e o contexto seguinte a herdou, 27 casos. Fecha o par com [memoria-e-contexto], e o desmentido da OpenAI é metade da lição. Ref em `core/refs/REFS.md`  
> [ ] [aula-agente-gastou-chave] responsabilidade quando o agente gasta: a chave não distingue pedido do dono de pedido do agente, e o relato do agente não é prova. Serve AI4Good (quem paga o erro) e techedu (o aluno vai dar chave pro harness dele). Ref em `core/refs/REFS.md`  
> [ ] [aula-agente-desanimado] decidir se o run de 14h da Astra no Minecraft entra numa aula — sob o antropomorfismo, a pergunta é o que as notas que o agente escreve pra si mesmo fazem com o comportamento seguinte. Ref em `core/refs/REFS.md`  
> [ ] [aula-abrir-o-moat] decidir se o caso Higgsfield vira aula de economia de IA — abrir o pipeline como estratégia, não generosidade. Conferir os números na fonte: o post é patrocinado. Ref em `core/refs/REFS.md`  
> [ ] [aula-dream-rsi] decidir se o Dream-RSI do DeepMind entra nas aulas — o agente transforma o histórico das próprias descobertas num simulador e "sonha" milhares de estratégias antes de gastar chamada real. **O que o post quase esconde:** não há mudança de pesos, só a política de exploração melhora. Bom justamente por isso, pra separar auto-melhoria de mito. Ref em `academy/refs/REFS.md` (— via aiwbot 2026-09-17)  
> [ ] [students-oficial] oficializar "students" no workspace sem redundâncias — a estrutura já existe espalhada entre `academy/lab/` e `academy/teaching/`, então é unificação. Linha irmã em [`lih-dd.md`](lih-dd.md): lá "student" é orientando, aqui é quem assiste (INBOX 2026-09-21)  
> [ ] [match-mecanica-conteudo] método do paper do Guilherme (SBGames): extrair da ementa termos, situações e comportamentos; nomear cada mecânica com seus parâmetros e contextos; casar as duas por **frequência × dificuldade**; e dar ao próprio match uma progressão de três instâncias — apresentação, consolidação, evolução. Sem diretório de paper ainda (INBOX 2026-09-21)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-09-21  ·  trend: advancing  ·  touches: 66/97/105/105/105/105
<!-- stats:end -->
