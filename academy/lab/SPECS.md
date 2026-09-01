# Research checkpoints — the law
> What must stay true of the student-facing checkpoint document, whoever edits it next.

The document itself is Portuguese and student-facing. This file is the contract behind it.

## Why it exists

A good process makes good research. The seven failures it is built against, in Lucas's words:
student gets stuck and does not say · lots of work, nothing converges · writing left to the end ·
shallow literature · **contribution defined far too late** · **no grip on what is doable with the
resources we actually have** · **technical results rare, and flawed method sinks the ones that
arrive**. The last three are decision failures, not effort failures — weekly delivery does not fix
them, gates that refuse to advance without a written decision do.

Audience is every kind at once: IC/PIBIC, TCC, master's/PhD, and course teams. **So checkpoints are
ordered by maturity, never dated.** Calendar lives in checkpoint 3, per student.

## Anatomy — identical in all 21

```
# <n>. <name>                    HEADING_1, collapses the whole checkpoint
<italic line>                    what the NEXT step does with this answer
## modelo                        fields, each with an italic *ex.:* ghost line
## exemplo                       filled in for real
## passo a passo                 numbered recipe, 5-9 steps, WOS lane inline
## verificação                   checkboxes
```

**Two collapse levels, never three.** H1 checkpoint, H2 block. Two checkpoints carry a fifth H2
block — `orçamento de viabilidade` (9) and `pré-registro de métricas` (13). They earned peer status
because they are the fix for the two hardest failures; burying them under `modelo` hid them.

**All 21 carry `modelo` and `verificação`. Only 8, 9, 10, 11, 13, 18 and 19 carry all four** — they
are the ones the two loops run through.

## Verification is the only sensor

Lucas chose no meeting artifact at all. That decision puts the entire weight of process visibility on
the checkboxes, so they obey rules the rest of the document does not:

- **A state that became true, written in the past — never a task.** "the table has five rows",
  not "fill the table".
- **Falsifiable by a third party in under a minute.** No item may need the student's word for it.
- **Every box carries `data: ___`.** Dates are what make the sensor readable: no box ticked in seven
  days means stuck, and the document says so out loud so that stuck is information, not shame.
- **3 to 7 boxes, 9 is the hard ceiling** — a DO-CONFIRM list past working memory stops being read.

## The two loops

Named so a meeting can say "third turn of loop A" instead of "we might be dragging".

- **LOOP A — what is worth doing.** 8 ↔ 9 ↔ 10 ↔ 11. Exits when the proposed contribution is
  covered by no competitor **and** fits the real budget. **Healthy deadline: one month**, Lucas's
  number. Kills failures 5 and 6.
- **LOOP B — whether the data holds the claim.** 18 ↔ 19 ↔ 9. Exits when the written claim is
  exactly what the data supports. Kills failure 7.

Contribution stays at position 9 — Lucas's call, made knowing LOOP A is what pulls it earlier.

## The 21, in order

1 cenário e planejamento pessoal · 2 burocracias de iniciação · 3 prazos chave · 4 textos de
fundamentação e palavras chave · 5 diagrama da área e escopo · 6 veículo alvo · 7 modelo no overleaf
e harness · **8 artigos competidores** · **9 proposta de contribuição** · **10 configuração** ·
**11 dados: origem, licença, tamanho** · 12 repositório de código · **13 metodologia** · 14 ética e
CEP · 15 esqueleto comentado · 16 desenvolvimento · 17 demonstração · **18 resultados** ·
**19 análise** · 20 submissão · 21 burocracias de encerramento

**14 exists early on purpose.** Ethics approval takes months and cannot run alongside collection, so
checkpoint 2 carries a trigger question — *does this touch human beings?* — that sends the student
to 14 in week one. Finding out late costs a semester.

## Design laws, and where they came from

- **`passo a passo` is READ-DO, `verificação` is DO-CONFIRM** (Gawande). Recipe you read while
  doing versus confirmation you run after. A DO-CONFIRM list needs a declared **pause point** — here
  the weekly 30-minute meeting.
- **Two disclosure levels maximum** (Nielsen Norman). Hence H1 → H2 and nothing deeper.
- **A blank box is a cliff** — novices guess rather than follow a scent. Every field gets an italic
  `*ex.: …*` ghost line. That `ex.:` convention is Lucas's own, from the original document.
- **Each question declares what the next step does with the answer** (GOV.UK question protocol).
  This is the mechanism behind "each checkpoint connects to the next" — it is the italic subtitle.
- **Stepped forms complete better than one long page**, which is why everything ships collapsed.

## The `passo a passo` runs in two lanes

Generic first — what to do, any student, any assistant. Then the **com o WOS** lane inline, with the
real command. The public scaffold repo students clone does not exist yet ([`ROADMAP.md`](../../ROADMAP.md)),
so the WOS lane is written and inert until it does.

## What the markdown round trip does

Measured 2026-08-26 against this document, not predicted. The general facts live in
[`core/tools/docs/SPECS.md`](../../core/tools/docs/CONTEXT.md); these are the ones this document
depends on:

- **`- [ ]` becomes a real Google Docs checkbox** and survives the round trip in both directions.
  All 104 boxes confirmed. The sensor works.
- **A fenced code block loses its fence** and lands as a normal paragraph. The WOS lane therefore
  uses inline code, which does survive.
- **Consecutive lines collapse into one paragraph.** Anything meant to be four lines must be a list.

## Checks before any push

Mechanical, over the source markdown: 21 numbered checkpoints, contiguous · every one has an italic
subtitle · every one has a `verificação` block · no verification over 9 boxes · every box carries
`data: ___` · no heading deeper than H2 · no field whose only content is `…`.
