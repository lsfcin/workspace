# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

me pergunto se o fable, dado que tenho 100 dólares de crédito pra gastar até setembro, ainda assim consome do meu limite por turno / semanal

tenho usado bastante o opus, com dificuldade de confiar no sonnet para as coisas que tenho feito...

git graph no vscode não mostra grafo dos subrepositórios, me pergunto se tem um jeito fácil de resolver isso

tabelas e bold continuam sem funcionar no bot.
— via aiwbot · 2026-07-23

sobre emojis nas mensagens, tipo ampulhetas, luzes verde/amarela/vermelha... acho com frequência os emojis escolhidos meio bregas. prefiro emojis simples, se tiverem, por exemplo, a luz vermelha pode ser sem efeitos, sem gradiente, só uma bolha vermelha. a ampulheta poderia ser preta e branca. enfim, é só um gosto visual, longe de ser algo crítico, mas seria legal ter um design mais estiloso e minimalista

usar nas minhas aulas, provavelmente em ai4good
https://www.instagram.com/p/DbGep4CDGtk/?utm_source=ig_web_copy_link
— via aiwbot · 2026-07-23

test/compare our skills and our flows with "state of the art" industry repos. one thing I would point though is that often the industry is not that concerned with tokens as I am give I only spend 20 dolars on AI (for devs on USA/europe/etc it seems considerably easier to spend 100 dolars)

montar base inicial e extensível para lidar com toda a burocracia da vida academica. pdfs (lembrar da ideia de ter arquivos associados aos pdfs de forma que evite o agente ler sem precisar e criar quando for ler, ter um hook pra isso, ter uma inteligência pra entender que talvez seja preciso uma segunda passada no pdf), resoluções, instruções normativas, páginas, links, estrutura organizacional mapeada, fluxos de processos, cada passo a passo relevante, transparente e facilmente editável, estruturar se possível não só pra mim mas criar um guia extensível para todo o departamento.

[16:57, 23/07/2026] Lenina Oliveira: Boa tarde Lucas
[16:57, 23/07/2026] Lenina Oliveira: podes relatar um processo de progressão pro CTA de terça?
[17:02, 23/07/2026] Lucas S. Figueiredo: oi Lenina, oficialmente estou de férias até o dia 24, então só poderia assinar a partir do dia 25. mas acho que funciona né? pode ser assim?
[17:03, 23/07/2026] Lenina Oliveira: então te encaminho e você faz na segunda ou na própria terça, pode ser?
[17:06, 23/07/2026] Lenina Oliveira: processo 23082.018263/2026-55 inserido no GT CTA
[17:11, 23/07/2026] Lucas S. Figueiredo: então te encaminho e você faz na segunda ou na própria terça, pode ser?
combinado
— via aiwbot · 2026-07-23

review SETUP.md, see if it remains accurate, if additions are correctly represented, if something was ditched but is still there, review coverage (w-os features are all there, skills, hooks, flows, brain, etc) and precision (it gives the needed info for newcomers to plugnplay all w-os functionalities)

considerar deixar o claude code rodando nos 10 dias de vipassana. será que é possível? será que existe alguma tarefa que ele conseguiria executar com autonomia de forma SEGURA e entregando resultados RELEVANTES? talvez um watcher pra construir e refinar continuamente as sessões de revisão do estado da arte dos papers planejados por hora. talvez criar uma pasta de sandbox pra codar vários protótipos. definitivamente pra isso vou precisar de uma mecânica de autostart de sessões. acho que no link abaixo isso foi criado

isso TEM que ser considerado com cuidado pro nosso workspace 
https://www.instagram.com/p/DbIo0eaErW9/?utm_source=ig_web_copy_link
— via aiwbot · 2026-07-23

gostaria de monitorar uma métrica que estou inventando agora de task expansion vs resolution. quantas tarefas estamos de fato resolvendo e quantas estamos criando?

fazer um tratamento do meu workspace pra garantir que ele seja de fato adaptável pra qualquer um que clonar o repo (pensando nos meus alunos)

definir um projeto pra ser executado pelo opencode

a skill de roundup tá consumindo bastante (7%), talvez mereça um redesign
abaixo o padrão de uso
Last 7d · these are independent characteristics of your usage, not a breakdown
67% of your usage was at >150k context
Longer sessions are more expensive even when cached. /compact mid-task, /clear when switching to new tasks.
27% of your usage came from subagent-heavy sessions
Each subagent runs its own requests. Be deliberate about spawning them — and consider configuring a cheaper model for simpler subagents.
21% of your usage was while 4+ sessions ran in parallel
All sessions share one limit. If you don't need them all at once, queueing uses it more evenly.
13% of your usage came from sessions active for 8+ hours
These are often background/loop sessions. Continuous usage can add up quickly so make sure it is intentional.
Skills
% of usage
/roundup
7%
/handoff
1%
/artifact-design
1%
Subagents
% of usage
general-purpose
6%
loop-medium
1%
Explore
1%
esses dados me fazem pensar se não podemos voltar com a ideia de induzir trocas de sessão automaticamente dado o tamanho do contexto, induzir agentes a buscar checkpoints, effective transition points, com mais frequência. será que um agente consegue por conta própria abriar uma nova sessão. sinto que este trabalho de gestão de contexto é penoso e não deveria ser do usuário.

confirmar que tudo que tá funcionando pro claude code também tá pro opencode E pro copilot

GOALS.md não parece estar monitorando corretamente. aparecem vários "touches" em frentes que não fiz nada.

o TODO.md me parece pouco funcional. não sei bem como melhorar. acho que ele poderia talvez ser mais mutável. e outra coisa também é remover as atividades já feitas, jogar em outro canto ou simplesmente deletar.

para o novo PPC de LC criar ementas das três disciplinas que faltaram já no formato novo
- FUNDAMENTOS DA EDUCAÇÃO, 
- PROJETO INTEGRADOR EM DESENVOLVIMENTO DE ARTEFATOS EDUCACIONAIS, 
- PROJETO INTEGRADOR EM EDUCAÇÃO EM COMPUTAÇÃO.

adiantar pra jarbinhas, publicar a tese dele

organizar a migração das pastas do drive e o espelhamento com a pasta academy aqui. organizar pastas ou algum tipo de referencia para os alunos/pessoas

automaticamente ou pelo menos oferecer a opção de ao solicitar o plan mode e mandar um prompt perguntar se quero mudar de modelo para um mais poderoso na hora de planejar e igualmente perguntar ou sugerir um modelo mais simples para a execução, inclusive considerar um modelo mais simples para partes/etapas da execução. de toda forma temos que fazer um benchmark/avaliação do /loops em termos de resultado e de custo.