# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

https://www.instagram.com/reel/De8hjW0MFrN/?cplk=OG15MTBndjRjMzEz
— via aiwbot · 2026-10-26

https://www.instagram.com/p/DeTHW7JAVjj/?vrfl=Y2dvM2w2ajhkOTA2
alguma chance da gente conseguir esse nível de animação pro isoroll?
— via aiwbot · 2026-10-25

https://www.instagram.com/p/DezzceOAbYc/?psln=MWVtc3M0OWt0dHZyeQ==
pra juntar no
— via aiwbot · 2026-10-22

criar um material com foco nos ex-bolsonaristas e ex-aliados como novos críticos do bolsonarismo
https://www.instagram.com/reel/DeyuDXHzUSE/?dlrf=NTc4MTIwNjQ2YQ==

tem aquele (acho que deputado) recém eleito, meio gordinho, não lembro do nome
tem a joyce hasselman, tem aquele outro homem político que deu entrevistas em algums podcasts e que era um dos fortes aliados de bolsonaro no governo dele, tem a janaína pascoal, o weintraub, as pessoas do mbl (katagiri, renan)
tem o general que fala no vídeo de wagner moura
— via aiwbot · 2026-10-22

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

wos: o ISSUES.md da raiz já estava acima dos limites antes desta triagem. Enxugar os relatos sem apagar problemas abertos nem criar outro arquivo.
— via Codex · 2026-10-24

wos (sessão RDA 2025): virar ferramenta o que rodou como script solto — (1) `gmail search --query --after --before` com download de anexos, o `fetch` só pega não-lidos; (2) varredor dos Boletins de Serviço da PROGEPE por nome/SIAPE (o site exige a intermediária RNP ICPEdu, baixada do AIA); (3) watchdog de job em background que vigia o PID — o que procurava texto com pgrep deu falso "parado" e falso "morreu". `gcalendar range` voltou vazio para cin e ufrpe: checar auth. `academy/cv` é repo local sem remoto: criar privado no GitHub? O `pdf-gate` barra PDF compilado de `.tex` gerado por script (sem `.texif`) e exige twin — a regra "nunca twin de PDF compilado" não chega ao hook. O token de escrita do Drive pessoal caiu duas vezes na mesma sessão.
— via Claude · 2026-10-24

wos (progressão docente): complementar o varredor já proposto com o Boletim de Gestão de Pessoas federal: progressão 279/2024 e reenquadramento 1.022/2025 apareceram lá, fora dos 1.293 PDFs da PROGEPE. A busca do gdrive limita silenciosamente a 20 resultados; expor limite/paginação. Scripts e evidências copiados do scratchpad para `Downloads/progressao-scripts/` (fora do git, matéria-prima para as ferramentas).
— via Codex · 2026-10-26

wos (matriz de subagentes): todo agente chama os outros direto, sem eu pedir — Claude Code, Codex/ChatGPT, agy/Antigravity, opencode, zcode, o que estiver instalado. Uma matriz chamador × chamado com o comando verificado de cada célula, e por modelo: capacidade, custo, limite de uso do plano, data da última checagem; setup automático que detecta o instalado e escolhe sozinho. Claude Code é o limite mais precioso, GPT o segundo melhor com limite generoso — conferir se o ranking da tabela bate com isso. Automático e barato em tokens (hooks + tools, não troca de mensagem). Jobs em background com watchdog em bash puro (zero token até disparar; vigiar crescimento do log, não pgrep) e aviso curto na última mensagem do turno (não telegram), porque mensagem do chat do VS Code entre chamadas de ferramenta às vezes some. Base já feita: `core/agents/SPECS.md` tem a linha do Codex com auth do Google (`-s workspace-write`, rede, `--add-dir ~/.config/workspace-*`), e `secure_dir` não grava mais quando o modo já está certo.
— via Claude · 2026-10-26

wos (commit parcial vaza AGENTS.md): `git commit -- <caminhos>` com uma norma entre eles fez o gerador de normas regenerar e incluir o `AGENTS.md` inteiro, levando junto a linha `EDIT > CREATE` staged por outra sessão (a fonte `core/norms/edit.md` ficou de fora). É o vazamento que `test_partial_commit_staging` proíbe para ISSUES/GOALS/.gitignore, mas o AGENTS.md não está coberto. Assimetria parecida, já corrigida: `validate_agents` não excluía `SPECS.md`, o validador de flows excluía.
— via Claude · 2026-10-26
