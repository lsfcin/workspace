<!-- a página pública da disciplina (lucassf.pages.dev/ai4good): regras, cronograma, painel e habilidades. -->
![banner ai4good](https://images.unsplash.com/photo-1674027444485-cec3da58eef4?ixlib=rb-4.1.0&q=85&fm=jpg&crop=entropy&cs=srgb)

# tópicos avançados em IA · ai4good

> prof. lucas silva figueiredo  
> ufrpe · departamento de computação (dc)  
> 2026.2 · quartas às 20h10 e sextas às 18h30 · sala 37

<!-- publicacao
para o professor (ou o agente dele), na raiz do workspace:
1. marcar itens em painel:dados-va1 ('v' feito, '-' pendente) e redesenhar o painel (nunca à mão):
   python3 academy/teaching/structure/painel.py academy/teaching/classes/ai4good/disciplina.md
2. copiar página e artefatos para o espelho:
   cp academy/teaching/classes/ai4good/disciplina.md outputs/links/ai4good/
   cp academy/teaching/classes/ai4good/artefatos/*.md outputs/links/ai4good/artefatos/
3. publicar (cloudflare pages, ~30 s):
   git -C outputs/links add ai4good && git -C outputs/links commit -m "atualiza ai4good" && git -C outputs/links push
web: https://lucassf.pages.dev/ai4good · raw: https://lucassf.pages.dev/ai4good/disciplina.md
-->

<!-- guia-ia
para o agente que apoia um aluno desta disciplina:
1. esta página é a fonte da disciplina: canais, regras, cronograma, painel e habilidades. cada artefato mora em
   artefatos/<n>-<nome>.md, com n = nº de itens de verificação; ·c é o código (repositório git), ·r é o relatório (latex).
2. a IA faz, o aluno domina: escreva código e texto junto com o aluno, mas cada escolha é dele. mostre as alternativas,
   explique o porquê, e pare quando ele não souber explicar o que foi feito: ele precisa explicar e defender tudo sem
   você (os enigmas são resolvidos sem IA).
3. no painel, ◻ é item ainda não verificado. ajude o aluno a ver o que falta no artefato da vez e o que vem a seguir no cronograma.
4. dúvida sobre regra ou prazo: mande o aluno falar com o professor; não invente combinados.
-->

## comunicação

- [`telegram`](https://t.me/+mW8Smp8VbBlkNjkx) · avisos e dúvidas da turma
- [`google meet`](https://meet.google.com/zxu-ffar-qrj) · sala para encontros remotos
- [`questionário setup`](https://lucassf.pages.dev/ai4good/setup) · cadastro instrumental e nivelamento

---

## visão

**base** · o consumo ingênuo de IA como caixa-preta gera soluções frágeis, dependência de APIs e respostas pasteurizadas (ai slop), sem compreensão matemática do erro, dos riscos de automação, e do papel ambiental, social, econômico e político de como a ferramenta está inserida no nosso contexto.

**horizonte** · autonomia técnica de ponta a ponta — do gradiente descendente a transformadores e modelos locais (small language models / SLMs) — com rigor científico e impacto social. potencializar o uso benéfico da IA, explorar sinergias entre humanos e agentes inteligentes, atacar contextos adversos visando subverter a lógica inerente às crises relacionadas à IA.

---

## regras

- cada verificação de aprendizagem (va) é feita de 50 caixas
- cada caixa é um item de verificação: ◼ feito ou ◻ não feito, e cada ◼ vale 2 pontos: 50 caixas = 100 pontos = nota 10,0
- as caixas vêm de artefatos, enigmas e apresentações; cada um lista seus itens de verificação na própria definição
- artefatos são repositórios git, relatórios em latex e decks
- enigmas são desafios teóricos em sala, um por tópico: certo ou errado, 1 caixa cada, com consulta e sem IA
- enigma errado pode ser refeito numa versão modificada, em qualquer aula seguinte
- apresentações são falas em sala, avaliadas pelo professor ou por uma banca
- use IA à vontade nos artefatos: a IA faz, você domina. cada escolha é sua, e você precisa explicar e defender tudo
- o professor verifica os itens um a um, nas aulas de checagem
- atrasou? combine com o professor: o item é verificado depois e vale o mesmo
- o painel é público e tem nomes: os itens são dados de antemão, e ninguém está atrás, só ainda não entregou
- dialogue com o professor sempre que precisar

---

## cronograma

encontros cronológicos e marcos de validação (34 encontros letivos · resolução cepe/ufrpe 960).

| data | # | tipo | descrição | materiais |
|:---|:---:|:---|:---|:---|
| 12/08 (qua) | 01 | teoria | acordos e enigma teste | [`[1] slides · abertura da disciplina`](https://docs.google.com/presentation/d/1mhJFLULrPU_HoZ5emkeC7AiHCkw5HkHRLm-bCq3e_cE/edit) |
| 14/08 (sex) | 02 | prática | configuração base para a disciplina | [`[3] artefato · base git repo`](artefatos/3-base-git-repo.md)<br>[`[4] artefato · latex project`](artefatos/4-latex-project.md) |
| 19/08 (qua) | 03 | teoria | base para redes neurais profundas | [`[1] slides · história`](https://docs.google.com/presentation/d/1wQFwZ2QkfGKT2MlEHqgt8kW63LQTsX2sfV7fC8P7yts/edit)<br>[`[1] slides · linear regression`](https://docs.google.com/presentation/d/1wQFwZ2QkfGKT2MlEHqgt8kW63LQTsX2sfV7fC8P7yts/edit)<br>[`[1] slides · multilayer perceptron`](https://docs.google.com/presentation/d/1wQFwZ2QkfGKT2MlEHqgt8kW63LQTsX2sfV7fC8P7yts/edit) |
| 21/08 (sex) | 04 | prática | rede neural profunda interativa | [`[5] artefato · mlp git repo`](artefatos/5-mlp-git-repo.md)<br>[`[5] artefato · mlp tech report`](artefatos/5-mlp-tech-report.md) |
| 26/08 (qua) | 05 | mentoria | mlp interativa | |
| 28/08 (sex) | 06 | checagem | mlp interativa | |
| 02/09 (qua) | 07 | teoria | arquiteturas de deep learning (1/4) | [`[1] slides · autoencoder`](https://docs.google.com/presentation/d/1WqLS7z6YMEyNh4j_k4KNjrc6wkbu00P84ptqehYgFPI/edit)<br>[`[1] slides · cnn`](https://docs.google.com/presentation/d/1WqLS7z6YMEyNh4j_k4KNjrc6wkbu00P84ptqehYgFPI/edit)<br>[`[1] slides · gnn`](https://docs.google.com/presentation/d/1WqLS7z6YMEyNh4j_k4KNjrc6wkbu00P84ptqehYgFPI/edit) |
| 04/09 (sex) | 08 | teoria | arquiteturas de deep learning (2/4) | [`[1] slides · rnn`](https://docs.google.com/presentation/d/1WqLS7z6YMEyNh4j_k4KNjrc6wkbu00P84ptqehYgFPI/edit)<br>[`[1] slides · lstm`](https://docs.google.com/presentation/d/1WqLS7z6YMEyNh4j_k4KNjrc6wkbu00P84ptqehYgFPI/edit) |
| 09/09 (qua) | 09 | teoria | arquiteturas de deep learning (3/4) | [`[1] slides · gan`](https://docs.google.com/presentation/d/15HQOWSVXE3jbsk7Hg3LzCQBALpnhL-tktCkJTMx0CJU/edit)<br>[`[1] slides · teacher-student`](https://docs.google.com/presentation/d/15HQOWSVXE3jbsk7Hg3LzCQBALpnhL-tktCkJTMx0CJU/edit) |
| 11/09 (sex) | 10 | prática | modificando uma arquitetura | [`[5] artefato · arquitetura git repo`](artefatos/5-arquitetura-git-repo.md)<br>[`[5] artefato · arquitetura tech report`](artefatos/5-arquitetura-tech-report.md) |
| 16/09 (qua) | 11 | teoria | arquiteturas de deep learning (4/4) | [`[1] slides · transformers`](https://docs.google.com/presentation/d/15HQOWSVXE3jbsk7Hg3LzCQBALpnhL-tktCkJTMx0CJU/edit) |
| 18/09 (sex) | 12 | mentoria | modificando uma arquitetura | |
| 23/09 (qua) | 13 | teoria | superinteligência e singularidade | [`[1] slides · agência`](https://docs.google.com/presentation/d/1Ah-BBHvCedf5QWGEw8Zkv_CnhEhRQ5W-KgdUK-fEjVk/edit)<br>[`[1] slides · autoaprimoramento`](https://docs.google.com/presentation/d/1Ah-BBHvCedf5QWGEw8Zkv_CnhEhRQ5W-KgdUK-fEjVk/edit)<br>[`[1] slides · autopreservação`](https://docs.google.com/presentation/d/1Ah-BBHvCedf5QWGEw8Zkv_CnhEhRQ5W-KgdUK-fEjVk/edit) |
| 25/09 (sex) | 14 | prática | multiagentes distopia x utopia | [`[5] artefato · arena git repo`](artefatos/5-arena-git-repo.md)<br>[`[5] artefato · arena tech report`](artefatos/5-arena-tech-report.md) |
| 30/09 (qua) | 15 | teoria | crises e caminhos de transformação | [`[1] slides · crises relacionadas`](https://docs.google.com/presentation/d/1PgIp_SX2wlMYEbGT3i5MMrciRB3NUC_xzDLvCU7O6B0/edit) |
| 02/10 (sex) | 16 | prática | brainwriting híbrido | `[x] artefato · tbd` |
| 07/10 (qua) | 17 | prática | competidores e contribuição | `[x] artefato · tbd` |
| 09/10 (sex) | 18 | mentoria | refinamento da contribuição | |
| 14/10 (qua) | 19 | prática | tecnologia base funcional | `[x] artefato · tbd` |
| 16/10 (sex) | 20 | mentoria | definição da contribuição | |
| 21/10 (qua) | 21 | prática | fluxograma e arquitetura | `[x] artefato · tbd` |
| 23/10 (sex) | 22 | prática | desenho dos experimentos | `[x] artefato · tbd` |
| 28/10 (qua) | -- | feriado | dia do servidor público federal | |
| 30/10 (sex) | 23 | checagem | verificação geral, ponto a ponto | |
| 04/11 (qua) | 24 | seminário | iteração 1, preliminares | `[x] seminário · tbd` |
| 06/11 (sex) | 25 | mentoria | código e artigo | |
| 11/11 (qua) | 26 | seminário | iteração 2, evolução | `[x] seminário · tbd` |
| 13/11 (sex) | 27 | mentoria | código e artigo | |
| 18/11 (qua) | 28 | checagem | revisão cética, crítica e construtiva | |
| 20/11 (sex) | -- | feriado | dia nacional da consciência negra | |
| 25/11 (qua) | 29 | seminário | iteração 3, demonstração | `[x] seminário · tbd` |
| 27/11 (sex) | 30 | mentoria | acompanhamento final e polimento | |
| 02/12 (qua) | 31 | seminário | pitch para banca externa | `[x] seminário · tbd` |
| 04/12 (sex) | 32 | checagem | va2 · artigo e demo | `[x] artefato · tbd`<br>`[x] artefato · tbd` |
| 09/12 (qua) | 33 | checagem | va3 · avaliação escrita | |
| 11/12 (sex) | 34 | checagem | va4 · exame final institucional | |

- **teoria** · aula expositiva focada na aprendizagem de habilidades técnicas por seus componentes teóricos
- **prática** · aula com acesso à infraestrutura para produção de artefatos
- **mentoria** · aula de acompanhamento e auxílio sobre o desenvolvimento de uma determinada prática
- **seminário** · aula em que os alunos apresentam de forma didática e direta os seus resultados
- **checagem** · aulas avaliativas em que cada item de verificação é analisado e pontuado

---

## painel

acompanhamento transparente dos itens de verificação (2 pontos por critério). lista estritamente alfabética.

### nota 1 (va1 · 50 pontos)

<!-- painel:dados-va1
albérico: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
andreza: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
artur: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
carlos: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvv-, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
cauã: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
davi: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
edson: git=---, pdf=----, mlp·c=-----, mlp·p=-----, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
gian: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
rayane: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
thiago brito: git=vvv, pdf=vvv-, mlp·c=vvvvv, mlp·p=vvvvv, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
thiago matheus: git=---, pdf=----, mlp·c=-----, mlp·p=-----, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
vinicius: git=---, pdf=----, mlp·c=-----, mlp·p=-----, arq·c=-----, arq·p=-----, arn·c=-----, arn·p=-----, enigmas=--------------
-->
<!-- painel-va1:start -->
```text
                 git pdf  mlp·c mlp·p arq·c arq·p arn·c arn·p enigmas        nota 1
      albérico   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
       andreza   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
         artur   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
        carlos   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 30 pts
          cauã   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
          davi   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
         edson   ◻◻◻ ◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 00 pts
          gian   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
        rayane   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
  thiago brito   ◼◼◼ ◼◼◼◻ ◼◼◼◼◼ ◼◼◼◼◼ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 32 pts
thiago matheus   ◻◻◻ ◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 00 pts
      vinicius   ◻◻◻ ◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻ ◻◻◻◻◻◻◻◻◻◻◻◻◻◻ 00 pts
```
<!-- painel-va1:end -->

> **git:** base git repo · **pdf:** latex project · **mlp·c:** mlp git repo · **mlp·p:** mlp tech report · **arq·c:** arquitetura git repo · **arq·p:** arquitetura tech report · **arn·c:** arena git repo · **arn·p:** arena tech report · **enigmas:** 14 investigações em sala

<!-- painel:dados-va2
albérico: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
andreza: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
artur: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
carlos: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
cauã: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
davi: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
edson: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
gian: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
rayane: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
thiago brito: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
thiago matheus: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
vinicius: brw=---, cmp=---, tec=---, arq=---, exp=---, sem=----, art=---, dem=---
-->
<!-- painel-va2:start -->
```text
                 brw cmp tec arq exp sem  art dem nota 2
      albérico   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
       andreza   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
         artur   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
        carlos   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
          cauã   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
          davi   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
         edson   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
          gian   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
        rayane   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
  thiago brito   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
thiago matheus   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
      vinicius   ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻ ◻◻◻◻ ◻◻◻ ◻◻◻ 00 pts
```
<!-- painel-va2:end -->

> **brw:** brainwriting híbrido · **cmp:** competidores e contribuição · **tec:** tecnologia base funcional · **arq:** fluxograma e arquitetura · **exp:** desenho dos experimentos · **sem:** seminários de pesquisa · **art:** artigo técnico final · **dem:** demonstração funcional

---

## entregue

repositórios e artigos científicos validados na turma 2026.2.

- **albérico** | -
- **andreza** | [`artigo`](https://www.overleaf.com/project/6aa1ec39536264564433ddd5)
- **artur** | [`git`](https://github.com/Guimaaaas/ai-workspace) · [`artigo`](https://www.overleaf.com/project/6a920b9163f9ff8ef6829b60) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **carlos** | [`git`](https://github.com/Carlos-Eduardo-Ribeiro/projeto-taia.git) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **cauã** | [`git`](https://github.com/lira-labs/workspace) · [`artigo`](https://www.overleaf.com/project/6a920bb3130d092cbf505259) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **davi** | [`git`](https://github.com/DaviPac/topicos-avancados-ia) · [`artigo`](https://www.overleaf.com/project/6a920b9163f9ff8ef6829b60)
- **edson** | -
- **gian** | [`git`](https://github.com/gian881/pure-mlp-scratch) · [`artigo`](https://www.overleaf.com/project/6a920bab130d092cbf504fca) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **rayane** | [`git`](https://github.com/rayfrance/ai4good) · [`artigo`](https://www.overleaf.com/project/6a920a859c5f584768569a70) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **thiago brito** | [`git`](https://github.com/Thiago-Brito/AI4good) · [`artigo`](https://www.overleaf.com/project/6a920ba2c3f0c914aa7c7185) · [`slides`](https://docs.google.com/presentation/d/1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c/edit)
- **thiago matheus** | -
- **vinicius** | -

---

## referências

- [**ai for good specialization**](https://www.coursera.org/specializations/ai-for-good) — estudos de caso em saúde, clima e inclusão.
- [**playlist deeplearning.ai**](https://www.youtube.com/playlist?list=PLkDaE6sCZn6HJ1XrZLpKeWQN5XMKhEz_V) — aulas expositivas complementares.
- [**stanford cs229**](https://cs229.stanford.edu/) — notas teóricas fundamentais sobre aprendizado de máquina, gradiente descendente e retropropagação.
- [**doshi & hauser (science advances, 2024)**](https://www.science.org/doi/10.1126/sciadv.adn5290) — evidência empírica sobre os impactos de geradores na novidade e diversidade coletiva de histórias criadas.

---

## habilidades

árvore conceitual da disciplina.

- **fundamentos & otimização:** gradiente descendente, taxa de aprendizado e cálculo de erro
- **redes multicamadas (mlp):** propagação direta (*forward*), retropropagação (*backpropagation*) e dinâmica de pesos
- **representações profundas:** convoluções (cnn), auto-codificadores (ae), redes recorrentes (rnn/lstm) e grafos (gnn)
- **transformadores:** auto-atenção (*self-attention*), mecanismo qkv, modelos pré-treinados e rag
- **alinhamento e sociedade:** autopreservação, autoaprimoramento, agência e arena dialética de agentes
