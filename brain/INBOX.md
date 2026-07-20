# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

gostaria muito de engatilhar tarefas aqui no claudecode de forma que assim que o limite de tempo fosse liberado o agente continuasse. será que é possível?

proj: workspace — finding (2026-07-11): `git add -A` na raiz engoliu 10 projetos com `.git` próprio (academy/papers/*, branches/*, code/*) como gitlinks embedded quebrados; precisei `git rm --cached` + amend antes do push. O .gitignore un-ignora o dir do projeto (pra pegar CONTEXT.md) mas isso deixa o `add -A` embutir o repo aninhado. Fix durável: pre-commit gate que BLOQUEIA gitlinks (mode 160000) não declarados em .gitmodules. → rota: workspace-os backlog.
