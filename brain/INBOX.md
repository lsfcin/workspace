# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

A gente fez uma pausa no investimento de avanço do workspace OS, mas eu sinto que é uma coisa latente que precisa melhorar no futuro próximo. E aí, uma das coisas é que, por exemplo, nas seções agora, só em montar o plano da seção, a seção já chega em torno de 140 mil tokens. Então eu tô na dúvida se a gente realmente não tá sobrecarregando muito a gente. logo na entrada. Enfim, tá aqui uma coisa pra gente pensar.
— via aiwbot · 2026-10-17

Isso é urgente. Isso é urgente. E não pode ser triado no INBOX, sendo escondido em algum lugar. Ou isso é feito, realizado por uma sessão, ou fica no INBOX. É o seguinte, se eu perder meu celular hoje, eu me lasquei. Eu perco várias das minhas contas. Perco o acesso ao GitHub, porque o aplicativo de autenticação tá no celular. E essa autenticação dos fatores, ela já foi um problema pra mim, porque eu perdi uma conta do Discord por conta disso. A conta do Discord foi hackeada, deslogada. Quando eu fui logado no open de autenticação dos fatores, eu não consegui achar a autenticação. Eu tenho muito medo disso acontecer com a minha conta do Google, com a minha conta do GitHub, com as várias outras contas que eu tenho. O autenticador hoje tem autenticação pra GitHub, Microsoft, Google e tem mais outros lá. Então, eu quero ter algum mecanismo que me deixe tranquilo pra que uma vez meu celular quebrando, perdendo ele, qualquer cenário desses, sendo roubado, eu não perca todas as minhas contas. Obrigado. Obrigado. Obrigado. Obrigado. Obrigado.
— via aiwbot · 2026-10-17

https://www.instagram.com/reel/DdVargvpEQ8/?dlrf=amlsZ3o3aTBiOTIw
ver se a gente tá cobrindo isso no wos e/ou se podemos aprender algo e melhorar
— via aiwbot · 2026-10-17

https://www.instagram.com/p/DefaJVojOSp/?img_index=9&cplk=MWZncXVoYWE4MG04YQ==
pode ser útil pro wos
— via aiwbot · 2026-10-17

https://www.instagram.com/p/DeMgL8IDfD5/?img_index=3&stkn=MWkzNmhmOWlhb2NyZw==
talvez ajude a gente no wos
— via aiwbot · 2026-10-07

wos: `gmail fetch` trava em 50 e-mails e só filtra por dias — pra achar o contrato do apto tive que chamar a API na mão com busca (q=). falta `gmail search "<query>"` + baixar anexo aninhado (o `attachments` atual não viu os PDFs do DocuSign, que vêm em parts aninhadas). e os boletos da DAC sumiram do gmail pessoal desde nov/2025 — conferir se foram pra outro e-mail
— via claude · 2026-10-17

wos (sessão ementas LC): o sub-repo `academy/administration` estava com 150 arquivos deletados no working tree (tudo intacto no HEAD, restaurado com checkout). causa desconhecida — só existia 1 commit e nada de reflog; suspeita: sync entre as duas máquinas ou limpeza de pasta gitignored pelo pai. vale um check que avise quando um sub-repo tem deleção em massa não commitada
— via claude · 2026-10-18

wos: o symlink `~/.claude/projects/-mnt-workspace/memory → brain/memory` está quebrado (a pasta não existe; há um `memory.pre-merge-backup`). a regra que o Lucas deu hoje — "nunca editar o arquivo original, sempre criar um arquivo extra; se mudou, recupera e cria outro" — não teve onde ser salva. rotear pra uma norma em `core/norms/` (ela vale pra Drive, Docs e arquivos locais)
— via claude · 2026-10-18

wos: `core/hooks/described.txt` casa por `str(path).endswith(chave)`, mas num repo aninhado o gate recebe o path relativo ao sub-repo, então a chave com `academy/administration/...` nunca casa — tive que usar só o sufixo. assimetria: o resto do workspace é relativo à raiz
— via claude · 2026-10-18

ppc: Decreto 12.456/2025 art. 10 §1 limita EaD de curso presencial a 30%, mas `code/ppc` (restrição c9) e `restricoes-curriculares-atualizado.md` ainda usam 40% da CEPE 744/2024. corrigir c9 depois que o Lucas confirmar. também: a pasta `novo-ppc-bcc/` guarda o PPC da LC (nome errado) e `organograma.md` chama o Lucas de coordenador, `brain/CONTEXT.md` de vice
— via claude · 2026-10-18

wos: o venv não tem `openpyxl` — li a planilha do BCC desmontando o .xlsx (xml). se planilha virar rotina, declarar a dep em `core/tools/deps.txt` e dar uma folha `xlsx` à família certa
— via claude · 2026-10-18
