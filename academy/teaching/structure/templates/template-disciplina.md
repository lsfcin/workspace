![banner da disciplina](https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1600&auto=format&fit=crop&q=80)

# [nome da disciplina]

> prof. lucas silva figueiredo  
> ufrpe · departamento de computação (dc)  
> [semestre, ex.: 2026.2] · [dias e horários, ex.: quartas às 20h10 e sextas às 18h30] · [sala física / laboratório, ex.: sala 37]

<!-- publicacao
como publicar / atualizar este documento no cloudflare pages (autonomia do professor):
1. sincronizar com a pasta publica:
   cp academy/teaching/structure/templates/template-disciplina.md outputs/links/teaching/template_disciplinas.md
2. commitar e enviar para o cloudflare pages:
   git -C outputs/links commit -am "atualiza template de disciplina" && git -C outputs/links push
3. links resultantes no ar (instantaneo):
   - visualizacao web (humano): https://lucassf.pages.dev/teaching/template_disciplinas
   - visualizacao raw (agente/ia): https://lucassf.pages.dev/teaching/template_disciplinas.md
   - edicao direta no navegador (sem terminal): botao 'editar (github.dev)' no rodape da pagina
-->

<!-- guia-ia
instruções para o agente / IA de apoio e manutenção da disciplina:
1. este arquivo é o documento soberano da disciplina (o próprio site da matéria). ele centraliza comunicação, visão, regras de avaliação, cronograma com artefatos, painel de progresso, entregas dos estudantes, referências e a árvore de habilidades.
2. publicação na web: este arquivo é espelhado em 'outputs/links/<disciplina>/disciplina.md' e servido via 'outputs/links/<disciplina>/disciplina.html' no Cloudflare Pages (https://lucassf.pages.dev/<disciplina>/disciplina). ao editar o canônico no workspace, sincronize a pasta de links e dê commit/push para atualizar o site ao vivo.
3. todas as entregas apontam para artefatos modulares na pasta 'artefatos/<n>-<nome>.md' (ex.: 'artefatos/3-base-git-repo.md'). os pontos de verificação e critérios atômicos pertencem exclusivamente ao arquivo do próprio artefato; o cronograma cita o link estilizado no formato `[`[n] tipo · nome`](artefatos/n-nome.md)`.
4. painel de progresso: dados de verificação ficam armazenados no bloco de dados oculto (painel:dados ...) no formato atômico 'v' (feito) ou '-' (pendente) por critério de artefato (ex.: 'git=vvv, pdf=vvv-'). o bloco renderizado em ASCII monospace entre 'painel:render' e 'painel:fim' é derivado diretamente desses dados, mantendo ordem estritamente alfabética e nomes alinhados à direita. cada critério atendido confere 2 pontos, totalizando 100 pontos acumulados ao longo do curso (50 caixas no total).
5. interação socrática: ao interagir com o estudante, ajude-o a localizar seu momento no cronograma, pré-requisitos na árvore de habilidades e pontos pendentes nas missões. nunca tome decisões pelos alunos, dialogue com eles ponto a ponto.
-->

## comunicação

- [`telegram`](url-do-grupo) · canal oficial da disciplina
- [`google meet`](url-da-sala) · videochamadas e encontros remotos
- [`questionário`](url-do-form) · levantamento de perfil e interesses

---

## visão

**base** · [descrever o dilema, a dor real ou o gargalo inicial que motiva a existência desta disciplina]

**horizonte** · [qual impacto concreto, autonomia e competências duradouras os estudantes constroem ao longo do semestre]

---

## regras

- a disciplina opera por pontos acumulados
- cada item de verificação confere 2 pontos
- a nota 10,0 é obtida acumulando 100 pontos (50 caixas de verificação no total)
- as formas de conquistar seus pontos são produzindo artefatos, resolvendo enigmas e apresentando resultados
- cada artefato, enigma e apresentação possui itens de verificação especificados na sua própria definição
- artefatos são documentos, links de repositórios git, decks de slides
- enigmas são exercícios teóricos, desafios aplicados em sala, com direito a consulta sem uso de IA
- em qualquer aula subsequente os enigmas em que você falhou poderão ser refeitos em uma versão modificada
- apresentações são falas em sala, avaliadas pelo professor ou por uma banca
- os itens são verificados diretamente pelo professor, um a um, em momentos definidos no cronograma
- em casos de atrasos, a verificação dos itens pode ser realizada depois desde que combinada com o professor
- as caixas no painel abaixo mostram todos os itens de verificação da disciplina
- dialogue com o professor sempre que preciso

---

## cronograma

encontros cronológicos e marcos de validação.

| data | # | tipo | descrição | materiais |
|:---|:---:|:---|:---|:---|
| 12/08 (qua) | 01 | teoria | acordos e enigma inaugural | [`[1] slides · introdução`](url) |
| 14/08 (sex) | 02 | prática | configuração base para a disciplina | [`[3] artefato · base git repo`](artefatos/3-base-git-repo.md)<br>[`[4] artefato · latex project`](artefatos/4-latex-project.md) |
| 19/08 (qua) | 03 | teoria | conceitos fundamentais e arquitetura | [`[1] slides · fundamentos`](url) |
| 21/08 (sex) | 04 | prática | implementação inicial e relatório | [`[5] artefato · projeto git repo`](artefatos/5-projeto-git-repo.md)<br>[`[5] artefato · projeto tech report`](artefatos/5-projeto-tech-report.md) |
| 26/08 (qua) | 05 | mentoria | acompanhamento e dúvidas | |
| 28/08 (sex) | 06 | checagem | verificação de marcos e pontuação | |

- **teoria** · aula expositiva focada na aprendizagem de habilidades técnicas por seus componentes teóricos
- **prática** · aula com acesso à infraestrutura para produção de artefatos
- **mentoria** · aula de acompanhamento e auxílio sobre o desenvolvimento de uma determinada prática
- **seminário** · aula em que os alunos apresentam de forma didática e direta os seus resultados
- **checagem** · aulas avaliativas em que cada item de verificação é analisado e pontuado

---

## painel

acompanhamento transparente dos itens de verificação (2 pontos por critério · 50 caixas = 100 pontos no total). lista estritamente alfabética.

<!-- painel:dados
formato: cada critério atômico do artefato é marcado como 'v' (feito) ou '-' (pendente).
aluno-a: git=vvv, pdf=vvv-, rep=vvvvv, art=vvvvv
aluno-b: git=vvv, pdf=vvv-, rep=vvvvv, art=vvvv-
-->
<!-- painel:render -->
```text
                 git pdf  rep   art   ...               total
       aluno a   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻   32 pts
       aluno b   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻   30 pts
```
<!-- painel:fim -->

> **git:** base git repo · **pdf:** latex project · **rep:** projeto git repo · **art:** projeto tech report

---

## entregue

repositórios e artigos científicos validados na turma atual.

- **aluno a** | [`git`](url) · [`artigo`](url) · [`slides`](url)
- **aluno b** | [`git`](url) · [`artigo`](url)
- **aluno c** | -

---

## legado

projetos de turmas anteriores.

- **projeto a** | [`git`](url) · [`artigo`](url)
- **projeto b** | [`git`](url) · [`artigo`](url)

---

## referências

leituras de base e recursos de suporte.

- [**referência 1**](url) — descrição da referência.
- [**referência 2**](url) — descrição da referência.

---

## habilidades

árvore de habilidades e conhecimento desenvolvida ao longo da disciplina. cada conceito aponta para o slide exato onde o fundamento é ensinado.

- **[perceptrons & mlp](slides-mlp.html#1)** (redes neurais multicamadas de alimentação direta)
  - **[forward pass](slides-mlp.html#forward)** — passo de inferência e propagação direta
  - **[backpropagation](slides-mlp.html#backprop)** — retropropagação do erro via regra da cadeia
  - **[loss function](slides-mlp.html#loss)** — função de perda / custo de calibração
- **[cnn (redes neurais convolucionais)](slides-cnn.html#1)**
  - **[convolução](slides-cnn.html#convolucao)** — operação de filtragem espacial deslizante
    - **[kernel](slides-cnn.html#kernel)** — núcleo / matriz de pesos do filtro
    - **[laplace](slides-cnn.html#laplace)** — operador de bordas omnidirecional
    - **[sobel](slides-cnn.html#sobel)** — gradientes direcionais horizontal e vertical
  - **[stride](slides-cnn.html#stride)** — passo de deslocamento do kernel
  - **[padding](slides-cnn.html#padding)** — preenchimento de bordas para preservação dimensional
  - **[pooling](slides-cnn.html#pooling)** — subamostragem e redução espacial
- **[autoencoders](slides-autoencoder.html#1)** (auto-codificadores)
  - **[encoder](slides-autoencoder.html#encoder)** — codificador de compressão
  - **[bottleneck](slides-autoencoder.html#bottleneck)** — gargalo / espaço latente comprimido
  - **[decoder](slides-autoencoder.html#decoder)** — decodificador de reconstrução
