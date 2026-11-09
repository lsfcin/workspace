# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/p/DfXk6uLDXB7/?rpxt=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-11-05

https://www.instagram.com/p/De6plJiDbwa/?img_index=5&vrfl=MWtyYWJoOG1icjM3bg==
— via aiwbot · 2026-11-02

https://www.instagram.com/p/DfKkR_fDTFY/?img_index=2&obrf=azBmOXUycWR3amgw
a gente poderia pegar a transcrição disso pra ver como pode ser útil pra gente
— via aiwbot · 2026-10-31

https://www.instagram.com/p/DesLVzbDIb7/?img_index=7&mdxt=MWZ2eDd4ZHJraXVjdg==
incorporar o que for pertinente no wos e nas minhas aulas
— via aiwbot · 2026-10-31

https://www.instagram.com/reel/DfEwIxZhYkK/?vrfl=dnRweDQ3MmhuaXo3
pode se útil pra gente de diferentes formas, inclusive pode ajudar a melhorar nosso bot de telegram que hoje tá um pouco quebrado
— via aiwbot · 2026-10-31

https://www.instagram.com/reel/De9_Ma8gXZa/?rpxt=N3QxZTN6d3Bud2Ey
isso aqui é útil pra gente e alguma forma?
— via aiwbot · 2026-10-31

ver se isso é útil no WOS 
https://www.instagram.com/p/De-eRt1knz7/?img_index=3&exln=MXZmaWZncm9pYWkwNw==
— via aiwbot · 2026-10-31




- (2026-11-04, sessão apptime) `core/tools/panel/ask` só tem codex e agy; opencode (`~/.opencode/bin/opencode`) e zcode (`/usr/bin/zcode`) estão instalados mas ninguém testou a chamada headless — testar e entrar na cadeia. assimetria: a folha `ask` é uma cadeia de providers, e a regra da família diz "o arquivo é o provider".
- (2026-11-04, sessão apptime) `./gradlew testDebugUnitTest` falha em `:url_launcher_android` (teste do plugin, não nosso); `:app:testDebugUnitTest` passa. ver se o verify do apptime roda só `:app`. o MIUI recusa `adb install` às vezes (`INSTALL_FAILED_VERIFICATION_FAILURE`), passa na 2ª tentativa — o `phone/adb` podia repetir sozinho.
- (2026-11-04, sessão apptime) `code/apptime/ROADMAP.md` em 237 linhas / 19.381 chars, bloqueia em 250 / 20.000: cortar (as seções de painel e Workspace drift são candidatas), não dividir.
- (2026-11-04, sessão ai4good) o entropy dashboard rodou num worktree temporário (`/tmp/inbox-promote-develop-20261030`) e gravou no ISSUES.md do develop 72 achados falsos (routing para arquivos "que o repo não carrega"). rodar só na árvore principal, ou recusar fora dela.
- (2026-11-04, sessão ai4good) `cfpages secrets --push` só configura produção; preview fica sem GITHUB_TOKEN/ENIGMA_SECRET, então nenhum e2e roda em preview. o comentário do GITHUB_TOKEN em `core/tools/links/segredos.env` diz "só lsf-links", mas ele já cobre academy-teaching.
- (2026-11-04, sessão ai4good) `ciclo.py redes-convolucionais` parou de novo (agy vazio em revisa-d3-r1 e revisa-f3-r1; f6 com problema na r2). falhar de uma vez com o agy vazio fez parar 2 de 2 rodadas desse banco.
- (2026-10-31, sessão apptime) `core/run tools/web/shoot` nasceu sem o `--unbundle` prometido: desempacotar um artifact exportado (`__bundler/manifest`, base64+gzip) ainda é script de scratchpad — o round 1 do apptime precisou dele de novo. Proposta: flag no shoot ou ferramenta irmã; mesma sessão, mesmo OK.
- (2026-11-06, 3ª sessão apptime) WOS: decisão construída sem a resposta registrada do Lucas não caiu em "decidido sem perguntar" do handoff (ícone de notificação, `82cdec2`: telefone inteiro + zigue-zague; o estudo perguntou, ninguém registrou a resposta). o handoff/roundup podia cobrar: toda pergunta "para Lucas decidir" aberta na sessão tem resposta registrada ou vai para "decidido sem perguntar". e o agente leu o ROADMAP do apptime em pedaços e listou só os itens 🟡/🔴, deixando Aba, drag e outros de fora — "o que tem pela frente" pede o ROADMAP inteiro.
- (2026-11-06, 4ª sessão apptime) WOS: um commit anunciou "B10" (`3747fb3`) sem escrever o B10 no ISSUES — o gate de ISSUES cobra prova para *sair* da lista, mas nada confere que uma mensagem de commit que cita `Bnn` deixou o `Bnn` no arquivo. e editar l10n do apptime pelo Edit exige ler os `.api` inteiros (centenas de chaves), então a sessão caiu em heredoc python, que o hook marca como UNGATED WRITE: o pré-requisito do Read empurra para o caminho sem gate.
- (2026-11-06, 4ª sessão apptime) assimetria: o mesmo âmbar claro tinha três valores (`#8A5A00` no código, `#A86B0C` na página de estrutura, `#9E6500` derivado); ficou o do código, no SPECS § Visual. páginas de decisão deviam ler cores do SPECS, não reinventar. dois tokens aposentados sobrevivem em `code/apptime/refs/CONTEXT.md` (descrição) e no ROADMAP § Rejected do apptime (o hook nomeia).
- (2026-11-06, 5ª sessão apptime) `phone/adb prefs` faz force-stop e lê o XML sem olhar o `.bak`: pós-install truncou o prefs (o Android restaurou do `.bak`). Ler o `.bak` se existir; `--open app` não abre nada.
- (2026-11-06, 5ª sessão apptime) `cfpages build --push` empurra o branch atual de `outputs/links`; o Cloudflare só publica o `main` (links `apptime/*` ficaram fora do ar). Publicar o `_redirects` no `main` ou recusar fora dele; `check` testar o 302.
