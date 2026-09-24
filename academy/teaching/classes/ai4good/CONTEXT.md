# ai4good
> Disciplina AI4Good — material e questionários da turma. Espelha `teaching/classes/ai4good/` no Drive pessoal.

Aulas 2026.2: quarta 20h10 e sexta 18h30.

## Calendário 2026.2

Mesmos números fixos de [`techedu`](../techedu/CONTEXT.md), que os
registra por inteiro: início 10/08 · término 12/12 · finais 14–18/12, e **34 encontros** depois de
tirar 28/10 e 20/11, que são feriado. Publicado na página do Notion
`25d1656e-2069-803e-a564-d510d9db8307`, um parágrafo por mês, `DD|DIA⇥Rótulo | Tema`, com o link
nomeado inline em **Apresentação** e **Especificação**.

Conferido contra o calendário oficial em 2026-08-26, quando o calendário desta disciplina somava
35 encontros: **20/11 estava marcado como aula** e é feriado nacional. A Feira de Profissões cai
em 07 e 08/10 e **não derruba aula** — decisão de Lucas, igual no TE.

## Um passo a mais

Mesmo requisito de [`techedu`](../techedu/CONTEXT.md), que o
descreve por inteiro, aqui redigido para projeto de pesquisa: ao fechar o problema e ao fechar a
abordagem, deslocar um dos dois com uma das sete alavancas, e **declarar qual alavanca e qual era o
óbvio abandonado**. Num artigo isso tem nome — é a diferença entre mais um resultado e uma
contribuição. Mora dentro da seção `Metodologia` da página do Notion.

## Material da aula

Os decks moram no Drive pessoal, em `material/aulas`
(`11XkvpRtaougD_Bs726E97lS-PE1auLa6`) — o mesmo arranjo de `techedu`, que antes
não valia aqui: os arquivos estavam soltos em `material/`.

**A cópia de junho tinha congelado.** Todo o trabalho de agosto seguiu no Drive do cin, então em
2026-08-26 seis decks foram recopiados e nove arquivos que nunca tinham sido migrados vieram junto
— entre eles as três planilhas, o documento e o form, que o migrador ignorava por não serem
apresentação. As cópias velhas estão na lixeira do Drive, não deletadas.

**Um deck por tema desde 2026-09-24**: `ai4good · <tema>`, 17 decks, cada um com link curto
`ai4good/<tema sem acento>` (regras em [`SPECS-aulas.md`](../../SPECS-aulas.md) § slides). Os
combinados, as práticas e as planilhas substituídas levam `[deprecated]` no nome — renomeados, não
apagados, então links antigos seguem vivos. O Drive do cin não tem mais nenhum deck desta disciplina.

Questionários são specs versionados, aplicados por [`gforms`](../../../../core/tools/forms/CONTEXT.md):

```bash
core/run tools/forms/gforms new --account personal \
  --folder 1uM6P5Zkj9iBh4StAzI2IcI8P9nldUdXf academy/teaching/classes/ai4good/<spec>.json
core/run tools/forms/gforms responses --account personal <form_id>
```

`1uM6P5Zkj9iBh4StAzI2IcI8P9nldUdXf` é a pasta desta disciplina no Drive pessoal — cada turma tem a
sua, e o mesmo questionário vira um form separado em cada uma, porque a leitura das respostas é
por turma.

| Spec | `formId` | Link de resposta |
|------|----------|------------------|
| [`2026-2-rotina-e-setup.json`](2026-2-rotina-e-setup.json) | `1Nfdbl6jj5aG5AXMbK0wOip79v-3Q6gTrycVaxL8fqAY` | `lucassf.pages.dev/ai4good/setup` |

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`artefatos/`](artefatos/CONTEXT.md) | Um arquivo por artefato da disciplina, `<n>-<nome>.md` com n = nº de itens de verificação; espelhado em lucassf.pages.dev/ai4good/artefatos. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`2026-2-rotina-e-setup.json`](2026-2-rotina-e-setup.json) | — | — | O questionário de rotina e setup da turma 2026.2, escrito como spec e aplicado por gforms new. |
| [`AI4Good - Prática extra para abono de faltas .md`](AI4Good - Prática extra para abono de faltas .md) | — | — | Prática extra para abono de faltas da disciplina  Tópicos Avançados em IA \- Turma 2 (AI4Good) |
| [`agencia_conteudo.py`](agencia_conteudo.py) | [`agencia_conteudo.pyi`](agencia_conteudo.pyi) | `texto` | Conteúdo novo do deck "Aula - Agência" (aula de 23/09/2026), aplicado por slides_build.py. |
| [`autoaprimoramento_conteudo.py`](autoaprimoramento_conteudo.py) | [`autoaprimoramento_conteudo.pyi`](autoaprimoramento_conteudo.pyi) | `texto` | Conteúdo novo do deck "Aula - Autoaprimoramento" (aula de 23/09/2026), aplicado por slides_build.py. |
| [`autopreservacao_conteudo.py`](autopreservacao_conteudo.py) | [`autopreservacao_conteudo.pyi`](autopreservacao_conteudo.pyi) | `caixa`, `texto` | Conteúdo novo do deck "Aula - Autopreservação" (aula de 23/09/2026), aplicado por slides_build.py. |
| [`disciplina.md`](disciplina.md) | — | — | a página pública da disciplina (lucassf.pages.dev/ai4good): regras, cronograma, painel e habilidades. |
| [`drive_sync.json`](drive_sync.json) | — | — | Estado do sync desta pasta com o Drive, escrito por core/tools/files/drive_sync.py — não é um formulário. |
| [`lm_conteudo.py`](lm_conteudo.py) | [`lm_conteudo.pyi`](lm_conteudo.pyi) | `fita` | Conteúdo novo do deck "Aula - Language Models" (aula de 23/09/2026), aplicado por slides_build.py. |
| [`notion-port.md`](notion-port.md) | — | — | Tópicos em IA - AI4Good |
| [`plano-refino.md`](plano-refino.md) | — | — | Decisões do diálogo de 2026-09-23 e as fases que faltam. Arquivo temporário: é apagado quando a última fase fechar. |
| [`slides_build.py`](slides_build.py) | [`slides_build.pyi`](slides_build.pyi) | `rgb`, `frame`, `style_reqs`, `element`, `clone_elements` | Intercala slides novos num deck existente, ancorados no id do slide que os precede. |
| [`slides_pecas.py`](slides_pecas.py) | [`slides_pecas.pyi`](slides_pecas.pyi) | `titulo`, `fonte`, `legenda`, `tokens`, `modelo` | Peças de desenho no estilo dos decks do Lucas (título minúsculo + termo em inglês, fonte no rodapé), para slides_build.py. |
| [`transformers-guia-acessivel-slides.md`](transformers-guia-acessivel-slides.md) | — | — | Material didático acessível e roteiro pareado aos 106 slides da aula, com audiodescrição estrutural e preparação para NotebookLM. |
<!-- routing:end -->
