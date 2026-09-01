# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

to com uma forte suspeita que os nossos hooks e talvez tools também estão consumindo muito mais tempo do que precisariam, honestamente, acho difícil acreditar que seja algo normal. o problema parece ser mais grave no windows inclusive

pesquisar sobre finasterida e outras estratégias pro cabelo, quero ver se tem uma forma saudável de conter ou até recuperar as minhas entradas. fazer isso direito, pesquisa científica, etc
— via aiwbot · 2026-09-01

https://www.instagram.com/reel/DZnwqiWuvZu/?utm_source=ig_web_copy_link
backchain dominance é uma coisa real? investigar, pesquisar, e aí talvez incluir na minha bateria de exercícios
— via aiwbot · 2026-09-01

https://www.instagram.com/p/DcuI3KiDuyu/?utm_source=ig_web_copy_link
interessado em particular nas animações svg
— via aiwbot · 2026-09-01

task: month — `academy/papers/megatruth/` é o único paper sem repo próprio: os outros nove têm o
seu, e por isso o `CONTEXT.md` deles é carregado por alguém. O do megatruth não era carregado por
ninguém, e a linha em `academy/papers/CONTEXT.md` apontava pra um arquivo que nenhum clone recebe.
Tirei a linha em 2026-09-01 (decisão reversível). Duas saídas, e a escolha é tua: dar um repo ao
megatruth como todo paper tem — aí o `CONTEXT.md` volta a ser roteado e o conteúdo ganha história,
que hoje não existe em lugar nenhum — ou deixar o paper local mesmo, sem linha.

sessão wos-zero (GLM flash, 2026-08-31): 13 commits na feature/inbox-drain — B3 B5 B6 B7 B9 B11 B12 B13 resolvidos com specs, B4 restaurado como o único bug aberto, cap de linha vence coluna (norm), refs fold, SPECS-module, harnesses.txt, issues-gate lê deleção. Fila: cortar os 4 files over-200 (SETUP 605, hooks/SPECS 361, core/SPECS 266, SCHEMA 226 — corte de conteúdo, um por sessão), PT→EN do corpus, resto do ROADMAP (28 findings aqui). PAYBACK de --no-verify: a sessão paralela editando core/norms/improve.md precisa commitar; até lá o round-trip do norms fica vermelho pra todo mundo.

será que tem como bloquear a adição de novas linhas no WOS? nenhum commit adiciona sem que diminua de outro canto?  

sessão metodologia-aulas (2026-09-01): duas assimetrias achadas e não consertadas. (1) `brain/drafts/` não tem CONTEXT.md, não está na routing de `brain/CONTEXT.md` e por isso não entra no allowlist do `.gitignore` (`brain/*`) — as quatro metodologias de aula estão fora do git, e a única cópia é o disco. Ou drafts vira subtree de verdade (CONTEXT.md + linha de exceção), ou é declarado efêmero por escrito. (2) os rascunhos carregam nome de provedor no arquivo (`-sonnet`, `-gemini`, `-opus`), contra a norma de naming provider-agnostic; aqui o provedor É o dado (experimento cego de três saídas), então ou a norma ganha exceção escrita para experimento comparativo, ou os três viram `-a/-b/-c` com o provedor dentro do arquivo. Decidir antes de o padrão se espalhar.
