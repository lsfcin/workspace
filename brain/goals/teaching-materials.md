# [ craft | teaching | near ] teaching materials paradigm

Mudar o paradigma do material de aulas. Slides como arquivos abertos, com animações, acessíveis e editáveis. Sair do
PowerPoint/PDF estático e entrar em algo vivo — onde o conteúdo pode ser versionado, transformado por agentes, e
verdadeiramente interativo. Before building: understand what's best-in-class today.

**A metade que faltava, dita por Lucas em 2026-08-14: conectividade antes de formato.** Hoje o
material de aula **não mora no workspace** — slides e forms estão no **Google Drive**, a página da
turma está no **Notion**. Enquanto o WOS não enxerga e não edita esses dois lugares, qualquer
discussão de formato é teórica: não há como um agente migrar, versionar ou transformar um material
que ele não alcança. Então a ordem é: **alcançar → organizar → só depois trocar o formato.**

Divisão de responsabilidade, para o item não viver em dois lugares: **este goal é a intenção e a
ordem**; a construção das ferramentas (CLI do Notion, superfície Google em `core/tools/`) é item de
[`core/ROADMAP.md`](../../core/ROADMAP.md). Uma cópia seria bug.

>**signals**  
meaningful · expected · motivated

>**timing**  
Semestre começou em agosto/2026 e Lucas quer isso organizado "em breve" — âncora externa real, não
prazo inventado. O custo de adiar não é perder um deadline, é passar mais um semestre produzindo
material fora do alcance do workspace.

>**owns**  
`core/tools/slides`  
`core/tools/files` · `core/tools/mail` · `core/tools/calendar`  
`academy/teaching`

**A conectividade caiu em 2026-08-19.** O gargalo que este goal declarava — "material fora do
alcance do workspace" — não existe mais para Tecnologias na Educação: o Notion lê (integração "WOS"
viva, página `0bd17453-ea83-4019-ba38-22a79d0114ce`), o Drive pessoal lê, e o `gslides` **escreveu
de verdade num deck real de aula** — 20 slides intercalados e 3 refinados no deck de Design
Thinking, na véspera da aula. `[roundtrip-one]` está feito. A ordem "alcançar → organizar → só
depois trocar o formato" avançou uma casa: o próximo degrau é **organizar**, não conectar.

**O WOS escreve no Notion desde 2026-08-26**, e a primeira coisa que escreveu foi o calendário
2026.2 de Tecnologias na Educação: 34 encontros conferidos contra o calendário oficial da UFRPE,
com link nomeado em cada linha, apontando para o Drive pessoal. As três seções de chips mudos
morreram junto, e o AI4Good levou o mesmo tratamento. O ciclo achou e pagou uma dívida escondida:
**a cópia de Drive de junho tinha congelado e o semestre continuou do lado do cin** — seis decks
recopiados, nove arquivos que nunca haviam sido migrados. As duas disciplinas estão inteiras no
pessoal; o que resta é deletar do lado do cin, em [google-migration](google-migration.md).

## selected next achievement
    [metodologia-tecedu] desenhar a metodologia completa de Tecnologias na Educação

**ease-start**  
O calendário já está fechado e publicado, e é ele que dá o esqueleto: 17 quartas de
**Apresentação**/**Status Report** e 17 sextas de **Especificação**, cada sexta carregando produto
e artigo ao mesmo tempo. Abra a página do Notion e escreva **uma** sexta por inteiro — o que cada
perfil da equipe (hacker, hustler, hipster) entrega naquele encontro. As outras dezesseis copiam
o formato.

## backlog

> [ ] [metodologia-tecedu] semana-padrão (quarta e sexta com papéis fixos, uma pergunta e um produto por encontro), as 9
> etapas mapeadas nos 34 encontros reais (números em `academy/teaching/tecnologias-na-educacao/CONTEXT.md`), avaliação
> nova, dashboard que substitui as duas planilhas Google, e o padrão MODELO+EXEMPLO em toda entrega. Inclui **como cada
> encontro abre e como cada conteúdo é mostrado** — a metodologia é dita antes do conteúdo (INBOX 2026-08-27)  
> [ ] [fecho-de-aula] fechar toda aula com dois blocos: (1) **vocabulário** — que palavras a turma passou a ter, o que
> expandiu no conhecimento da área; (2) **verificação** — um teste curto que o aluno usa para conferir sozinho que
> aprendeu, possivelmente respondido em sala como formulário que contabiliza nota (INBOX 2026-08-27)  

**Três propostas independentes e o contraste, em 2026-09-01**, em `brain/drafts/`
(`metodologia-aulas-sonnet.md`, `-gemini.md`, `-opus.md`, e
[`-contraste.md`](../drafts/metodologia-aulas-contraste.md)). As três convergiram sozinhas em oito
pontos — esse núcleo é o achado. O contraste corta de cada uma e propõe uma versão de **8 blocos**,
menor que qualquer uma das três. Falta só confrontar com o estado real das duas disciplinas antes
de promover pra `academy/teaching/`.
> [ ] [pesquisa-que-falta] gamificação séria (sem infantilizar), specs/contract grading, mecanismos de avaliação por
> pares com propriedades verificáveis, e venues de publicação alcançáveis por graduandos em um semestre  

> [ ] [research-tools] research best current teaching tools — interactive slides, animations, open formats — start from
> the animation entries in `core/refs/REFS.md` (claude-code+remotion, Claude Code UI-animation skills).
> **Reescopado 2026-08-14:** o WOS agora lê e edita os decks direto no Google Slides (`core/tools/slides/gslides`), e
> Slidev foi deletado — a pergunta aberta não é mais qual formato local adotar, é quanto de animação dá pra autorar como
> sequência de slides gerada (inclui a ideia de um gerador de animações próprio)  
> [ ] [pick-format] pick a target format or tool — one concrete candidate to prototype with  
> [ ] [migrate-one] convert one existing lecture to the new format as a test  
> [ ] [full-migration] define migration plan for remaining course materials  
> [ ] [excalidraw-aula02] abrir `academy/teaching/tecnologias-na-educacao/aula02-problemas.excalidraw` no excalidraw.com
> e confirmar que carrega (o JSON foi montado à mão, nunca foi aberto); depois, Live collaboration → copiar o link →
> trocar `[EXCALIDRAW]` no slide 69 do deck; confirmar se são mesmo 8 equipes (o quadro tem 8 frames)  
> [ ] [video-carrinho] decidir o vídeo do slot do carrinho — trecho de 4 min do Dietz, ou perguntar à turma "o que
> envelheceu nesse vídeo de 1999?" (candidatos avaliados em `academy/refs/REFS.md`)  
> [ ] [medir-redesenho] anotar dois números depois da aula — quantos alunos falaram no bloco de abertura, e quantos
> grupos saíram com o frame preenchido; é o teste honesto do redesenho  
> [ ] [questionarios-sextas] mandar os dois questionários pras turmas — links de resposta nos `CONTEXT.md` de
> `academy/teaching/ai4good/` e `academy/teaching/tecnologias-na-educacao/`; antes, abrir cada link, responder uma vez
> de teste e apagar a resposta; depois da aula, ler com `core/tools/forms/gforms responses --account personal <form_id>`
> e decidir o formato das sextas  
> [ ] [ai4good-book-burning] investigar o caso por trás do reel "this feels like a book burning" e decidir se entra nas
> aulas de ai4good — ref em `academy/refs/REFS.md` (INBOX 2026-07-28). Um segundo post (@theaifield, INBOX 2026-08-21)
> dá nome ao caso — a "Project Panama" atribuída à Anthropic, livros comprados, descosturados, escaneados e reciclados —
> e o contraponto técnico, o ScanRobot 2.0 da Treventus, que digitaliza sem destruir; conferir na fonte antes de usar  
> [ ] [ai4good-integracao] decidir se o argumento "integração, não substituição" entra numa aula de
> ai4good — ref em `academy/refs/REFS.md`; a fundadora vende hardware no fim do reel, então o
> argumento vale sem a fonte (INBOX 2026-08-28)  
> [ ] [ai4good-otimismo] decidir se o reel do Gordon-Levitt (otimismo é ingênuo ou necessário?) abre
> uma aula de ai4good — ref em `academy/refs/REFS.md` (INBOX 2026-08-28)  
> [ ] [ai4good-lecun] decidir se o reel do LeCun entra numa aula de ai4good — décadas em redes neurais quando a aposta
> era tida como morta, hoje em world models e não em prever a próxima palavra; ref em `academy/refs/REFS.md` (INBOX
> 2026-08-24)  
> [ ] [ai4good-pacing-frontier] assistir o reel "pacing the frontier" e decidir se entra nas aulas — ref em
> `academy/refs/REFS.md`; a extração só trouxe a legenda, então o conteúdo ainda é desconhecido (INBOX 2026-08-17)  
> [ ] [arxiv-visuals] achar e testar o arXiv Visuals (paper → explainer animado; link é comment-gated, então achar por
> fora) — ref em `academy/refs/REFS.md`; teste honesto: rodar num paper que você conhece a fundo e ver se a ordem
> "conceito mais difícil primeiro" se sustenta ou se é sumarização com narração; se sustentar, decidir dois usos
> separados: leitura própria e material de aula (INBOX 2026-08-17, *"this IS for me"*)  
> [ ] [or-gate-shape] OR gate body ainda ausente no deck de portas lógicas; investigar o tipo `CUSTOM` no grupo do slide
> 23, depois decidir se vale seguir debugando  

> [ ] [acessibilidade-edson] preparar uma versão acessível das missões E do site da disciplina para o Edson — os dois
> artefatos, não só um (INBOX 2026-08-24)  
> [ ] [slides-pesquisa] material (talvez slides) que apresente aos alunos os conceitos dos projetos de pesquisa: dobra,
> cria, texpace/spacemantics — serve de ponte entre a disciplina e a pesquisa própria (INBOX 2026-08-24)  
> [ ] [ai4good-revisao-sobras] sobras da revisão dos decks História/ML/MLP + Prática MLP (2026-08-21): (1) checar
> visualmente a timeline da parte 3 — cobre Dartmouth 1956, inverno da IA, backprop 1986, AlexNet 2012? decidir se sobe
> pra parte 1 ou ganha recap; (2) slide-ponte no fim da aula amarrando os dois decks; (3) o único slide de resultados
> restante é da turma anterior — rotular "turma 2026.1" ou remover; (4) depois de aprovar, deletar os slides marcados
> "SKIPPED —" nos dois decks; (5) o slide "impacto das funções de ativação" (ex-163) foi deletado junto com sua cópia
> corrigida — se era pra manter, refazer a correção de pontuação  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-09-01  ·  trend: advancing  ·  touches: 39/59/59/59/59/59
<!-- stats:end -->
