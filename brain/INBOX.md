# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/reel/DdME5hsNRju/?utm_source=ig_web_copy_link
colocar na minha aula
— via aiwbot · 2026-09-12

https://www.instagram.com/p/Dc-eScZjdmL/?utm_source=ig_web_copy_link
quero escutar todos esses álbuns
— via aiwbot · 2026-09-11

explorar
https://www.instagram.com/reel/DdG848DNm3p/?stkn=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-09-10

https://github.com/mattpocock/skills
talvez seja útil pra gente, avaliar

https://www.instagram.com/p/Dc9g2R7E-T5/?utm_source=ig_web_copy_link
acho que isso também cabe nas aulas
— via aiwbot · 2026-09-10

https://www.instagram.com/p/DdGCA8yAVsV/?utm_source=ig_web_copy_link
colocar nas minhas aulas
— via aiwbot · 2026-09-10

https://arxiv.org/abs/2608.30114v1
a gente TEM que olhar isso! não deixar pra mt longe.

https://www.instagram.com/p/DdEhCWsDg3W/?stkn=NTc4MTIwNjQ2YQ==
isso tem que entrar nas minhas aulas de ai4good

será que tem como a visualização default do VSCode para arquivos .md ser a visualização formatada? e se
tiver será que tem como também editar arquivos nesse tipo de visualização?

https://www.instagram.com/reel/DbBVIMJRj5X/?stkn=NTc4MTIwNjQ2YQ==
acho que esse bloco pode entrar na minha lista de exercícios
— via aiwbot · 2026-09-06

https://www.instagram.com/reel/DcpDEyzp7m4/?stkn=NTc4MTIwNjQ2YQ==
talvez seja isso, um conjunto fixo de 8 exercícios poderia facilitar a minha vida
— via aiwbot · 2026-09-06

https://www.instagram.com/reel/Dc61lZ_sBfz/?utm_source=ig_web_copy_link
será que vale a gente usar rust ao invés de python?
— via aiwbot · 2026-09-06

https://www.instagram.com/p/Dcygo4skfjX/?utm_source=ig_web_copy_link
fazer um comparativo com o ubuntu, talvez valha à pena trocar
— via aiwbot · 2026-09-05
(extração falhou 2026-09-05: post atrás de login, nem com cookies — retriage quando o conteúdo existir)

https://www.instagram.com/p/Dc54js5CEsw/?utm_source=ig_web_copy_link
temos que testar isso
— via aiwbot · 2026-09-05
(extração falhou 2026-09-05: post atrás de login, nem com cookies — retriage quando o conteúdo existir)

https://www.instagram.com/p/Dc37X91M4QQ/?igsi=NTc4MTIwNjQ2YQ==
será que consigo usar de alguma forma?
(extração falhou 2026-09-05: post atrás de login, nem com cookies — retriage quando o conteúdo existir)

task: backlog — `branches/casinhas` mantém a pasta espelho no Drive à mão, e já existe um motor declarativo
pra isso: um `drive_sync.json` na raiz do projeto (como o de `academy/teaching/ai4good`) faria o
`core/run tools/files/gdrive sync` alcançar a pasta, e o mapa em `PROJECTS.md` passaria a mostrar `sync` em vez
de um link cru. Decidir: vale sincronizar de verdade, ou o espelho manual é intencional porque a pasta tem
material que não deve subir?

task: backlog — o gate de tipo do pre-commit recusou um repositório de teste descartável durante a
sessão porque `core.hooksPath` é global e alcança qualquer repo criado sob o workspace, inclusive um
`tmp_path` do pytest. O teste contorna apontando `core.hooksPath` para um diretório vazio. Decidir: o
pre-commit deveria se recusar a rodar num repo fora da árvore do workspace, em vez de cada teste ter
de lembrar de desligá-lo?

task: backlog — regerar toda tabela de roteamento do workspace de uma vez revelou duas derivas
paradas em `academy/`, e as duas pioram o que está publicado. Um `.json` sem sintaxe de comentário
ganha linha com `← add first-line comment`, que é uma dívida que ninguém pode pagar naquele arquivo
— `core/hooks/described.txt` existe exatamente para isso e o gerador não o consulta para esse caso.
E em `academy/teaching/tecnologias-na-educacao/`, o blurb do próprio arquivo vence a descrição
escrita à mão, então `cp01-materiais.md` passa a anunciar na tabela o id da Planilha Mestre em vez
da frase que dizia o que o arquivo é. Revertido em 2026-09-11 sem commitar; volta na próxima vez que
alguém salvar naqueles diretórios.
