# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

task: month — `academy/papers/megatruth/` é o único paper sem repo próprio: os outros nove têm o
seu, e por isso o `CONTEXT.md` deles é carregado por alguém. O do megatruth não era carregado por
ninguém, e a linha em `academy/papers/CONTEXT.md` apontava pra um arquivo que nenhum clone recebe.
Tirei a linha em 2026-09-01 (decisão reversível). Duas saídas, e a escolha é tua: dar um repo ao
megatruth como todo paper tem — aí o `CONTEXT.md` volta a ser roteado e o conteúdo ganha história,
que hoje não existe em lugar nenhum — ou deixar o paper local mesmo, sem linha.

sessão wos-zero (GLM flash, 2026-08-31): 13 commits na feature/inbox-drain — B3 B5 B6 B7 B9 B11 B12 B13 resolvidos com specs, B4 restaurado como o único bug aberto, cap de linha vence coluna (norm), refs fold, SPECS-module, harnesses.txt, issues-gate lê deleção. Fila: cortar os 4 files over-200 (SETUP 605, hooks/SPECS 361, core/SPECS 266, SCHEMA 226 — corte de conteúdo, um por sessão), PT→EN do corpus, resto do ROADMAP (28 findings aqui). PAYBACK de --no-verify: a sessão paralela editando core/norms/improve.md precisa commitar; até lá o round-trip do norms fica vermelho pra todo mundo.

será que tem como bloquear a adição de novas linhas no WOS? nenhum commit adiciona sem que diminua de outro canto?  