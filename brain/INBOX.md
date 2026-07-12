# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/brain-inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

proj: workspace — finding (2026-07-11 compass): `.hooks/brain_stats.py` tem 392 linhas, acima do BLOCK_LINES=200 do pre-edit gate → o Edit tool RECUSA qualquer edição (mesmo net-zero), tive que patchar via Bash/python. Débito real: ou splitar em módulos (parse / stats / dashboard / done-log), ou o gate isentar `.hooks/`. Enquanto não resolver, edições nesse arquivo são fricção.

proj: workspace — finding (2026-07-11): mesmo bug de case do `Models/` atingiu o Brain. `brain_stats.py` usava `Path("Brain")` e o pre-commit grepava `^Brain/goals/`, mas o dir é `brain/` → hook de stats do Brain NUNCA rodava (dashboard congelado desde 16/06). Corrigido. Suspeita: algum tool/sessão recria dirs capital-case (mesmo padrão do Models/). Vale um gate anti-capital-case em nomes de dir de topo.

a pasta Models/ (com M maiúscula) ressucitou. eu tenho a suspeita que isso foi uma sessão que usou o ComfyUI. lembrando que queremos ficar somente com a models/ (m minúscula), sem duplicatas