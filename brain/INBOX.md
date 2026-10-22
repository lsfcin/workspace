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

ementas: `build.py` regrava os 46 .docx a cada run (bytes iguais, carimbo novo), o que suja o diff — gravar só quando o conteúdo mudar. `verify.py` acusa 1 mismatch antigo (PROGRAMAÇÃO AUTOMÁTICA COM LLM, correquisito '' × 'NÃO TEM'): é a convenção do SPECS, então o verify precisa aplicá-la. `drive_core` não tem função para trocar o conteúdo de um Doc: em 2026-10-19 fiz `files().update(media_body=<docx>)` no Doc existente, que mantém id, link e histórico — promover a `drive_core` + flag `--update` no `upload_all.py`. acervo da Rural é Pergamum (SPA React, sem consulta por script): uma folha que confira a bibliografia básica no acervo poupa o Lucas. `Nova Grade — LC.html/.md` e `PPC — Grade LC_UFRPE*.md` têm nomes de PI de software, desatualizados frente a `code/ppc/grade-curricular.json`
— via claude · 2026-10-19

wos: `gslides text` ESCREVE no deck, mas o nome soa como leitura ao lado de `read` (assimetria de nome; quase rodei por engano). token `slides-write` personal expirou — `read` falha e só `export` funciona sem OAuth
— via claude · 2026-10-19

wos: subagente fora do Claude (2026-10-19). o GPT (`gpt-6.1-sol` via `codex exec`) recusa gerar ou ranquear persuasão política para um grupo de eleitores (6 de 9 geradores e o juiz da virada), mas checa fatos muito bem com `-c tools.web_search=true`; o agy está sem cota até ~25/out. então a regra de rota é por tipo de tarefa, não por custo só: GPT para checagem, levantamento e código; Claude para o que a política da OpenAI recusa. hoje está só na tabela de `core/agents/CONTEXT.md`; falta virar regra que uma sessão aplica sozinha (item de delegação em `core/ROADMAP.md`)
— via claude · 2026-10-19

wos: a disputa de ideias da virada (brief → geradores por operador → juiz cego com duelos suíços → interrogatório → portão → Lunga) rodou duas vezes à mão, e o brainwriting de ai4good é o mesmo motor para aluno. candidata a flow em `core/flows/`, com o design space como entrada; assimetria: um é artefato de disciplina, o outro é cockpit, e nenhum cita o outro
— via claude · 2026-10-19

virada: o repo aninhado tem `CONTEXT.md` e `ISSUES.md` no stage, de outra sessão, sem commit (achado ao abrir `feature/virada-semana-final` em 19/out); bancos 1–3, `sintese.md` e o item "Jornada e sábado" ainda tratam a folga como "parada no Senado", falso desde 14/out (Flávio votou sim, EC 141 de 16/out)
— via claude · 2026-10-19

wos: `yt-dlp` não baixa mídia do YouTube (19/out): sem runtime JS dá aviso, e com `--js-runtimes node:…` dá HTTP 403; `--download-sections` também falha (ffmpeg código 8). só legenda automática sai. a camada L2 (transcrição) de `core/tools/video` está cega para YouTube até resolver token/cookies ou atualizar o yt-dlp (instalado por pip, avisa que está velho)
— via claude · 2026-10-19

wos/publish: `publish --push` recusado pela suíte do repo público em 21/out (14 vermelhos, nada enviado; `feature/sync-20261021-*` ficou em `code/wos`). causas vistas: `academy/teaching/structure/arvore.py` não cruza mas `test_links::test_a_page_with_habilidades_block_runs_arvore_generator` o chama; `code/aiwbot/CONTEXT.md` linha 3 aponta para meta que não cruza; testes gravam `core/state/claude_*_test-*` dentro do alvo e o `--push` os versiona; o fixture `brain/drafts/taste-galeria-1.md` do `vendored.txt` sumiu; 1 linha de routing para arquivo não rastreado; 1 CONTEXT.md com contrato no cabeçalho; timeouts em `test_shim_paths` e `test_features_wiring`. corrigir AQUI e rodar `/publish` de novo.
— via claude · 2026-10-21

wos/links: o site só renderiza um .md pelo formato `<curso>/?doc=<caminho>.md`; um link curto para `<curso>/artefatos/x` (sem `.md`, sem `?doc=`) abre "Nothing to see here". `ai4good/brw` ficou assim de 17 a 21/out, e é o link dos pareceres. `cfpages add` deveria recusar alvo do próprio site que não resolve, ou o `check` deveria pegar.
— via claude · 2026-10-21

máquina: disco com 97% de uso (3,5 GB livres em 21/out); o exemplo do artefato tec usou whisper `small` porque o `large-v3` (3 GB) não cabia.
— via claude · 2026-10-21
