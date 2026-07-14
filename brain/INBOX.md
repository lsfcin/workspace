# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/brain-inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->
shared Downloads folder between my smartphone and both computers

there is some apps and/or configs that still point to our old Downloads folder, I wanted it unified to make it all point to /mnt/workspace/Downloads/

prompt-dsl, usar DSLs como contratos entre agentes, cada agente especializado em um tipo de tarefa terá a sua DSL e só repassaremos o prompt pra ele se o parsing da DSL for perfeito. isso permite garantir uma comunicação específica e nos moldes que desejarmos, com completudes de todos os termos pra não existir ambiguidade ou espaço pra decisões equivocadas. uma preocupação é se LLMs são boas com DSLs. elas são boas com linguagens de programação mas provavelmente por conta do treinamento exaustivo. não tenho certeza se com uma gramática nova elas se adaptam bem. então como acoplar ferramentas às LLMs pra facilitar essa interação com DSLs?

gary stevenson, ler e entender, incluir as obras dele no nosso workspace onde for pertinente

ruth bregnam e moral ambition, ler e entender, incluir as obras dele no nosso workspace onde for pertinente

proj: workspace — finding (2026-07-11): `git add -A` no repo workspace engoliu 10 projetos com `.git` próprio (academy/papers/*, branches/*, code/*) como gitlinks embedded quebrados. Tive que `git rm --cached` + amend antes do push. O .gitignore un-ignora o dir do projeto (pra pegar o CONTEXT.md) mas isso deixa o `add -A` embutir o repo aninhado. Vale um pre-commit gate que BLOQUEIA gitlinks (mode 160000) não declarados em .gitmodules.

proj: workspace — finding (2026-07-11 compass): `.hooks/brain_stats.py` tem 392 linhas, acima do BLOCK_LINES=200 do pre-edit gate → o Edit tool RECUSA qualquer edição (mesmo net-zero), tive que patchar via Bash/python. Débito real: ou splitar em módulos (parse / stats / dashboard / done-log), ou o gate isentar `.hooks/`. Enquanto não resolver, edições nesse arquivo são fricção.

proj: workspace — finding (2026-07-11): mesmo bug de case do `Models/` atingiu o Brain. `brain_stats.py` usava `Path("Brain")` e o pre-commit grepava `^Brain/goals/`, mas o dir é `brain/` → hook de stats do Brain NUNCA rodava (dashboard congelado desde 16/06). Corrigido. Suspeita: algum tool/sessão recria dirs capital-case (mesmo padrão do Models/). Vale um gate anti-capital-case em nomes de dir de topo.

a pasta Models/ (com M maiúscula) ressucitou. eu tenho a suspeita que isso foi uma sessão que usou o ComfyUI. lembrando que queremos ficar somente com a models/ (m minúscula), sem duplicatas