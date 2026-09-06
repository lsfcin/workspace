# Metodologia de disciplina — o que a investigação devolveu (2026-09-03)

> Contraparte de [`metodologia-disciplinas-gemini.md`](metodologia-disciplinas-gemini.md), escrita no
> mesmo dia. **Não é uma proposta concorrente** — é o estado real das duas disciplinas, a evidência
> revisada por pares, e as opções que sobram depois dela.
>
> Nome sem provedor de propósito: a norma do workspace proíbe nome de modelo em arquivo, e o INBOX
> de 2026-09-01 já registra que o par `-sonnet`/`-gemini`/`-opus` precisa de veredito. Este arquivo
> não espalha o padrão.
>
> Os artefatos completos ficam em `outputs/` (fora do git, como este arquivo):
> `metodologia-disciplinas-estado.md` · `-sota.md` · `-opcoes.md` · `-sota.provenance.md` ·
> `ai4good-folha-de-avaliacao.md`. As 15 referências estão em `academy/refs/REFS.md`.

## 1. O que foi lido antes de opinar

As duas páginas do Notion, as planilhas de nota e de pares no Drive, um deck de Missão e a folha de
banca. A avaliação real das duas disciplinas **não estava no disco** — foi por isso que a
investigação começou por aí.

**O achado que muda o desenho: a grade de XP já existe e ninguém a vê.** A planilha intergrupos do
TecEdu roda desde 2024.1 uma rubrica de especificação completa — **6 missões × 3 critérios**, escala
`A`/`AP`/`NA`, cada equipe avaliada por várias outras, mais uma linha própria de *avaliação das
avaliações*. Isso é o substrato da barra de progresso. O AI4Good não tem grade nenhuma: a nota é
soma de pontos por prática, sem critério escrito atrás.

**Segundo achado: a anatomia da entrega existe três vezes com três vocabulários** — `modelo ·
exemplo · passo a passo · verificação` no lab; `alvo · exemplo bom e ruim · modelo · roteiro ·
checklist` na aula prática; `objetivo · material · template · exemplo · critérios · roteiro ·
entrega` no deck de Missão. Mesmo contrato, três línguas.

Onze assimetrias listadas no arquivo de estado. A que bloqueia o modelo comum é a primeira: **`VA1`
mede coisas diferentes** — no TecEdu é a qualidade da avaliação que a equipe faz das outras, no
AI4Good é a soma das práticas entregues. Mesmo rótulo, mesmo peso, coisas sem relação.

## 2. O que a literatura devolveu

Quinze fontes, todas revisadas por pares, veículo nomeado linha a linha. Nenhum preprint sustenta
conclusão aqui.

1. **Gamificação tem efeito pequeno e positivo** (Sailer & Homner, g=.49 cognitivo), e o moderador
   que funciona é **competição combinada com colaboração** — não o ponto em si.
2. **O elo mais fraco medido é competência percebida** (Li, Hew & Du, g=.277) — justo o que uma
   barra de XP promete entregar.
3. **A fronteira que decide o XP** (Cameron, Banko & Pierce): o dano aparece com recompensa
   *tangível, prometida antes e frouxamente ligada ao desempenho*; quando é **ligada ao nível
   atingido**, a motivação intrínseca sobe ou fica igual. *"Uma vez verificado, uma vez provado"*
   cai no lado seguro.
4. **Expor trabalho excelente do colega faz desistir** (Rogers & Feller, N=5.740) — e o mecanismo do
   estudo era **avaliação por pares**, que é o coração da VA1 do TecEdu.
5. **O vale de novidade dura semanas, não o semestre** (Rodrigues et al., CS1 brasileiro, N=756):
   cai na 4ª semana, volta entre a 6ª e a 10ª. Medir no meio dá a resposta errada.
6. **Nota alternativa não tem respaldo de resultado** (Hackerson et al., revisão de escopo em STEM):
   literatura escassa, sem consenso teórico, instrumentos não validados. Adotar specs grading segue
   defensável — como decisão de desenho, não como conclusão de literatura.
7. **O que tem respaldo é o que já se faz**: rubrica g=.45 (Panadero & Jonsson — e nº de critérios e
   de níveis **não** moderou), avaliação por pares g=.31 contra nada e **g=.28 contra a avaliação do
   professor** (Double et al.), com a condição de Falchikov & Goldfinch: julgamento **global sobre
   critérios bem entendidos**, não muitas dimensões separadas.
8. **Problema antes da técnica bate técnica antes** (Sinha & Kapur, 53 estudos, g=.36 e .87
   corrigido), e **seis das oito sequências possíveis são compatíveis com carga cognitiva**
   (Gorbunova, van Merriënboer & Costley). A pergunta não é qual campo — é qual sequência para qual
   objetivo e qual aluno. **O AI4Good roda hoje o formato mais fraco** (QUA teoria → SEX prática).
9. **Banca estruturada por folha α=.75–.80; banca solta α=.50** (Abuzied & Nabag). O TecEdu tem
   folha; o AI4Good não.

## 3. A decisão tomada

**Painel: só o dono vê.** Cada aluno vê a própria barra, cada equipe a da equipe. Nada nominal, nada
projetado em sala. Consequência assumida: o painel precisa de identificação, o que encarece publicar
— e a ideia inicial de "site público de consulta rápida" está descartada.

## 4. O que ficou pendente

A mecânica do XP, a ordem da capacitação e a unificação do rótulo `VA1`. As três estão armadas com
número em `outputs/metodologia-disciplinas-sota.md`; nenhuma foi decidida.

## 5. Contra a proposta do Gemini

**Convergem sozinhos em cinco pontos**, e esse núcleo é o achado confiável: contrato de entrega em
três peças (modelo + par bom/ruim + checklist binário); correção binária sem nota fracionada em
marco intermediário; duas camadas de progresso, equipe e indivíduo; painel alimentado por formulário
sem digitação; uma régua só para as duas disciplinas.

**Divergem em seis, três dos quais importam:** o *dashboard aberto* é o recorte que a evidência
associa a desistência e que já foi descartado; a Tensão 1 é resolvida a favor do I-PS no AI4Good,
que é o lado que perde na meta-análise; e os quatro arcos **não batem com o semestre que já correu**
— o TecEdu fez Design Thinking no encontro 3, não no 7, e o AI4Good está nos encontros 07–12 com
teoria de redes neurais, não com problematização. Somam-se: Nilson e Amabile entram como evidência
sem serem estudo de resultado; a escala 0–7 / 7–10 aparece sem origem; e o passo final proposto cria
`SPECS-disciplinas.md`, que pela norma é último recurso e depende do teu OK.

## 6. O que foi produzido além do texto

Rascunho da **folha de banca do AI4Good** (`outputs/ai4good-folha-de-avaliacao.md`), não publicado:
4 blocos `2|3|3|3`, 13 subitens, escala `NA/AP/A/AE`, espelhando a folha do TecEdu com conteúdo de
pesquisa em vez de produto. É a mudança mais barata e mais bem respaldada de toda a lista.

Achado no caminho: a disciplina usa **três níveis no grid de pares e quatro na banca**. Duas escalas
na mesma disciplina.

## 7. Dívidas e bloqueios

- `academy/refs/REFS.md` foi de 154 para **197 linhas**, com teto em 200 — a próxima captura não
  cabe. Candidato a corte: a seção de reels do Instagram no topo, cuja prosa longa é segunda cópia
  do que já está em `brain/goals/teaching-materials.md`. Corte é decisão de Lucas.
- Token do `gforms` da conta `personal` expirou; a reconsentimento abre navegador na máquina dele.
- As duas cópias da planilha de pares com o mesmo nome seguem sem canônica declarada.
- O Miro ainda vive dentro dos decks de Missão, embora Excalidraw seja o padrão desde 2026-08-26.
