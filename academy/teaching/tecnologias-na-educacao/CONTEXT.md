# tecnologias-na-educacao
> Disciplina Tecnologias na Educação — material e questionários da turma. Espelha `teaching/tecnologias-na-educacao/` no
> Drive pessoal.

Aulas 2026.2: quarta 18h30 e sexta 20h10.

## Calendário 2026.2 — os números fixos

Resolução CEPE/UFRPE nº 960, de 2025-11-20. **Início 10/08/2026 · término 12/12/2026 · provas
finais 14–18/12.** Não recontar isto: 18 quartas (12/08→09/12) e 18 sextas (14/08→11/12), **menos
28/10 (qua, Dia do Servidor Público Federal) e 20/11 (sex, Consciência Negra) = 17 + 17 = 34
encontros.**

Semanas quebradas, onde a presença cai: 07/09 seg · 12/10 seg · 02/11 seg · 08/12 ter (feriado
municipal do Recife, e a última quarta do semestre, 09/12, cai logo depois). Marcos da universidade
que competem por atenção: 07 e 08/10 Feira de Profissões · 19/11 Fórum de Internacionalização ·
03/12 Cantata Natalina. **Nenhum deles derruba aula** — 07/10 é quarta letiva e Lucas mantém aula
nas duas disciplinas; o Dia do Professor, 15/10, o calendário oficial já manda manter com todas as
letras.

Conferido linha a linha contra o Calendário de Graduação UFRPE 2026 em 2026-08-26. A Feira estava
registrada aqui como 27/10, que é dia nenhum.

**O calendário 2026.2 publicado é o da página do Notion**
(`0bd17453-ea83-4019-ba38-22a79d0114ce`), cinco parágrafos, um por mês, no formato do AI4Good:
`DD|DIA⇥Rótulo | Tema`, com o link nomeado inline. Os rótulos são **Apresentação** (aula nova),
**Especificação** (a sexta) e **Status Report**, e cada um aponta para o deck no **Drive pessoal**.
Quarta é a aula; **sexta carrega produto e artigo ao mesmo tempo** — é onde a publicação vive.

## Um passo a mais

Requisito da disciplina desde 2026-08-26, e **o AI4Good tem o mesmo**: ao definir o problema e ao
definir a solução, a equipe é obrigada a sair do óbvio. Sete alavancas — inverter um componente,
trocar a persona, juntar dois pontos não-usuais, inverter o objetivo, restrição dura como motor,
trocar quem faz o trabalho, mudar o momento.

**O que o torna corrigível em vez de decorativo:** a equipe declara, na entrega, *qual alavanca
usou e qual era o óbvio que abandonou*. Sem esse par, o passo não foi dado. Mora embutido nos
passos 3 e 4 da seção `Processo` da página do Notion — não em seção própria, porque a exigência
tem de ser lida no momento da decisão, não num lugar que se visita uma vez.

O argumento para a turma é [Doshi & Hauser](../../refs/REFS.md): ideias vindas de LLM deixam cada
texto mais criativo **e todos mais parecidos entre si**. Ancoragem institucional: o *Dark Horse
Prototype* do Stanford ME310.

## Material da aula

O deck de cada aula mora no Drive pessoal, em `material/aulas`
(`18L_A9hTVyIQGYUouJg0qS9R_3jwQ8oWX`), e é editado no lugar por
[`gslides`](../../../core/tools/slides/CONTEXT.md). **Contribuição em deck existente é aditiva**:
slides novos entram entre os antigos, os antigos são refinados no lugar, nada é deletado nem pulado.

| Aula | Deck | Gerador |
|------|------|---------|
| 02 — Design Thinking e Problemas na Educação | `1sPvsyaAMkCUf5Ok5O94V3xrB5kF77fYRMzEPgisZdKY` | [`add_aula02.py`](add_aula02.py) + [`aula02_conteudo.py`](aula02_conteudo.py) |

O quadro colaborativo da aula 02 é [`aula02-problemas.excalidraw`](aula02-problemas.excalidraw),
gerado por [`build_excalidraw.py`](build_excalidraw.py) — um frame por equipe mais um frame de
EXEMPLO preenchido. **A colaboração ao vivo do Excalidraw é efêmera e ancorada em quem abriu a
sala**: fechar a aba mata o trabalho da turma, então o arquivo tem de ser salvo antes do fim da aula.

**Excalidraw é o padrão da disciplina** (veredito de 2026-08-26, depois da aula de 19/08). O Miro
foi removido da página do Notion e de toda menção aqui — se um dia fizer falta, o git tem.

## A árvore de tecnologias

**A § Tecnologias Emergentes da página do Notion é gerada, não editada à mão.** A fonte é
[`tecnologias.json`](tecnologias.json) — 12 eixos, 68 folhas, cada folha com um vídeo e um
repositório próprios, mais estrelas e data do último commit **gravadas no dado**, que é o que
deixa a árvore auditável no semestre seguinte. Publicar:

```bash
core/run --python academy/teaching/tecnologias-na-educacao/build_tecnologias.py
core/run tools/notes/notion apply --account personal /tmp/notion-ops-tecnologias.json
```

O plano de ops sai fora da árvore de propósito: regenera do JSON, e versioná-lo criaria uma segunda
cópia sempre atrasada. Os doze ids que ele apaga estão nomeados um a um no gerador — a página
carrega calendário, processo e avaliação no mesmo nível, e um delete por prefixo levaria tudo.

Uma folha declara o equipamento só quando ele passa de um laptop: `[desktop 4090]`, `[Quest 3]`,
`[licença]`, `[peça ~R$30]`. Sem marca é laptop comum. `⚡` marca o que pouca gente usou — **cada
eixo precisa de pelo menos uma**, senão a curadoria daquele eixo falhou. A equipe ordena um top-10
no Excalidraw; a mecânica é dela, não há formulário.

Três armadilhas de licença ficam ditas na folha porque a equipe descobriria tarde: **3D Gaussian
Splatting** é não-comercial (Inria), e **YOLO** e **MiroFish** são AGPL-3.0 — publicar como serviço
obriga a abrir o código.

Questionários são specs versionados, aplicados por [`gforms`](../../../core/tools/forms/CONTEXT.md):

```bash
core/run tools/forms/gforms new --account personal \
  --folder 10tmlq_os3ltiS-UzdEMG8mj45ni5t45O academy/teaching/tecnologias-na-educacao/<spec>.json
core/run tools/forms/gforms responses --account personal <form_id>
```

`10tmlq_os3ltiS-UzdEMG8mj45ni5t45O` é a pasta desta disciplina no Drive pessoal — cada turma tem a
sua, e o mesmo questionário vira um form separado em cada uma, porque a leitura das respostas é
por turma.

| Spec | `formId` | Link de resposta |
|------|----------|------------------|
| [`2026-2-rotina-e-setup.json`](2026-2-rotina-e-setup.json) | `1QyOkwdY9nNZPLLh179tSRyadgh6Cl-p9R1XM7qRTWkY` | [viewform](https://docs.google.com/forms/d/e/1FAIpQLScOoEjTI-l64rgUSBMQ198J_B9ssrai_tIVAcPAOYe-uWklww/viewform) |

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`add_aula02.py`](add_aula02.py) | [`add_aula02.pyi`](add_aula02.pyi) | `build` | Aula 02: intercala slides novos no deck existente e refina dois slides. |
| [`aula02_conteudo.py`](aula02_conteudo.py) | [`aula02_conteudo.pyi`](aula02_conteudo.pyi) | — | Conteudo da aula 02 — o que entra no deck e onde. |
| [`build_excalidraw.py`](build_excalidraw.py) | [`build_excalidraw.pyi`](build_excalidraw.pyi) | `frame`, `rect`, `ellipse`, `text`, `bloco` | Gera o quadro da aula 02: um frame por equipe + um frame de exemplo preenchido. |
| [`build_tecnologias.py`](build_tecnologias.py) | [`build_tecnologias.pyi`](build_tecnologias.pyi) | `par`, `toggle`, `folha`, `blocos`, `ops` | Gera a seção Tecnologias Emergentes do Notion a partir de tecnologias.json: toggle por eixo, toggle por folha. |
<!-- routing:end -->
