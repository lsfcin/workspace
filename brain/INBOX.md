# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

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

task: today — VPN do CIn está de pé e funcionando (IPv4 sai por Net-ExtVPN-extIP.cin.ufpe.br), mas o dispatcher que
bloqueia IPv6 durante a VPN NÃO foi instalado: falta um `sudo install` que eu não consegui rodar. Enquanto isso todo
site com AAAA é acessado com o IP de casa, e periódico/editora não reconhece o acesso institucional —
silenciosamente. Comando e script prontos em `SETUP-accounts.md` § VPN do CIn (bloco Install, heredoc do
`90-vpn-cin-ipv6`); a Precondição/Verify da própria seção diz se já foi. Decidir também: `SETUP-accounts.md`
foi de 113→163 linhas com essa seção e passou do aviso de 150 — ou corta ~13 linhas (candidato: a seção Exa
API key, 15 linhas para uma feature opcional), ou o heredoc do dispatcher vira arquivo versionado (−14 aqui,
+1 arquivo).

task: backlog — `branches/casinhas` mantém a pasta espelho no Drive à mão, e já existe um motor declarativo
pra isso: um `drive_sync.json` na raiz do projeto (como o de `academy/teaching/ai4good`) faria o
`core/run tools/files/gdrive sync` alcançar a pasta, e o mapa em `PROJECTS.md` passaria a mostrar `sync` em vez
de um link cru. Decidir: vale sincronizar de verdade, ou o espelho manual é intencional porque a pasta tem
material que não deve subir?

task: backlog — dois módulos do enforcement passaram do aviso de 200 linhas fechando as issues de
2026-09-11: `core/hooks/commit/generators.py` (193→214) e `core/hooks/entropy/entropy_corpus.py`
(199→214). Nenhum chega perto do teto de 250, e o segundo já estava a uma linha do aviso, então
qualquer adição o derrubava. O ROADMAP tem um item para as ferramentas acima do limiar mas ele cobre
`core/tools/`, não `core/hooks/`. Decidir: estender aquele item para o enforcement, ou cortar —
`generators.py` tem cinco estágios que poderiam virar dois arquivos pela linha gera-artefato /
gera-interface.

task: backlog — o gate de tipo do pre-commit recusou um repositório de teste descartável durante a
sessão porque `core.hooksPath` é global e alcança qualquer repo criado sob o workspace, inclusive um
`tmp_path` do pytest. O teste contorna apontando `core.hooksPath` para um diretório vazio. Decidir: o
pre-commit deveria se recusar a rodar num repo fora da árvore do workspace, em vez de cada teste ter
de lembrar de desligá-lo?

task: backlog — nada impede uma prosa `.md` de repetir um número que `core/hooks/limits.env` já
define, e em 2026-09-11 duas cópias estavam paradas em 150/200 cinco dias depois da lei virar
200/250: `code/CONTEXT.md`, lido 56 vezes, e `core/hooks/SPECS.md` quatro linhas abaixo da regra que
proíbe exatamente essa repetição. Os dois foram corrigidos tirando o número. Falta o invariante:
`core/tools/test/law/test_citation_gate.py` já guarda a família irmã (número de item citado fora do
roadmap), então ou ele cresce um caso, ou nasce um checker que recusa qualquer `.md` que enuncie um
limiar de `limits.env` diferente do vigente. Construir custa linhas, e crescer precisa do aval do
Lucas — daí estar aqui e não feito.
