# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

aparentemente nossas ferramentas estão verbose... ver se vale uma revisão disso. abaixo um exemplo:
```text
E AssertionError: index claims 40 findings, sum of ledgers is 560 E assert 40 == 560
pytest failure: core/tools/test/law/entropy/dashboard/test_entropy_scatter.py:32: AssertionError =========================== short test summary info ============================ FAILED core/tools/test/law/entropy/dashboard/test_entropy_scatter.py::test_the_root_total_equals_the_sum_of_the_local_ledgers FAILED core/tools/test/law/entropy/dashboard/test_entropy_scatter.py::test_the_index_lists_every_repo_that_has_a_ledger 2 failed, 624 passed in 40.59s
```

pra cada .yaml que preenchemos ao pesquisar referências da literatura fazer duas coisas antes, baixar o .pdf e converter ele pra um arquivo de texto (talvez .md) com todo o conteúdo (inclusive tabelas e figuras) num formato acessível para as IAs, em texto (zero imagens, só as descrições delas)

aprender essa
https://www.instagram.com/reel/DcouwIwTBX1/?igsi=NTc4MTIwNjQ2YQ==
— via aiwbot · 2026-08-31

transicionar prum modelo de investimentos que eu acredito
https://www.instagram.com/p/DcMf6TuFIYS/?utm_source=ig_web_copy_link
— via aiwbot · 2026-08-31

verify.py n deveria ficar em algum lugar melhor do WOS?

LINHA DE BASE do port, medida hoje em Windows sem bash nenhum: 433 passam, 138 falham, 1 skip de 572.
E a categoria das falhas mudou meu entendimento do trabalho: só 96 são exec/shebang (OSError +
FileNotFoundError, esperadas). As outras 150 são AssertionError de UM padrão só — o código emite
`C:\Users\lucas\workspace\academy\papers` onde o teste espera `academy/papers`. O pathlib resolveu o
SISTEMA DE ARQUIVOS e não resolveu o VOCABULÁRIO DE PATH: toda vez que um path vira texto (linha de
routing table, chave de registry, linha do ISSUES.md, comparação com features.txt) ele sai no
separador do SO. Proposta: barra normal, sempre, para todo path que é DADO — `.as_posix()` no
boundary, Path só para tocar disco. É o que o git faz internamente há 20 anos. E não é concessão a
Windows: torna routing table e entropy dashboard byte-idênticos entre máquinas, que é justamente o
que `test_the_output_is_deterministic` já pede. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

6 falhas de UnicodeDecodeError: parte do código abre arquivo sem `encoding='utf-8'` e pega o default
do SO (cp1252 no Windows brasileiro). Todo `.md` do workspace é UTF-8, então o default do SO nunca é
a resposta certa em lugar nenhum — inclusive em Linux, onde só funciona por acidente de locale.
proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

os hooks NÃO ativam sozinhos depois de um clone, e o SETUP.md afirma que sim. `.claude/settings.json`
e `.zcode/config.json` são versionados com `/mnt/workspace/...` hardcoded em ~20 comandos, e o passo
"Workspace path" só reescreve shebang de core/tools. Em qualquer clone fora daquele path a camada de
enforcement inteira fica morta em silêncio — o modo de falha exato que o deps.txt existe pra eliminar.
Vale pro Windows e vale pro aluno que clonar em ~/wos. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

as três bifurcações por-SO do WOS estão todas quebradas, e isso é argumento e não coincidência:
start-session.ps1 imprime WORKSPACE.md (arquivo que não existe; o real é AGENTS.md) enquanto o .sh
imprime AGENTS.md e ainda se descreve como "Neutral session-start entrypoint"; .agentrc.json aponta
start_session_windows pro .ps1 quebrado; caveman/hooks/activate.js escolhe caveman-statusline.ps1 no
Windows e esse arquivo não existe no repo. A correção não é consertar os .ps1, é deletá-los. Um
entrypoint que roda nos dois. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

a convenção de segredo "dir 700 / file 600" (SETUP-accounts.md, e a entrada de 26/08 sobre os tokens
664/775) não tem equivalente escrito pra nenhum sistema sem modo POSIX. No Windows a permissão é ACL,
não modo. Isso não é um passo de install, é uma pergunta do seam de plataforma: secure_dir() /
secure_file() ao lado de interpretador e package manager. E o Lucas tem razão que deveria vir cedo —
um segredo escrito frouxo não fica seguro depois. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

deps.txt não tem como dizer "esta dep só existe neste sistema", e o caso do secretstorage é pior do
que parece. Medido no Windows hoje: `pip install secretstorage` sai 0 e `import secretstorage` sai 0
— ou seja, a probe declarada em deps.txt fica VERDE. Mas o Secret Service é D-Bus, que só existe em
Linux, então a dep está presente e inútil ao mesmo tempo. É um falso verde, que é pior que um falso
vermelho: a coluna `breaks` promete avisar quando a feature some, e aqui ela não avisa. O redesenho
do `kind` precisa de um teto de aplicabilidade por sistema, e a probe precisa medir função e não
importação. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

o permissions.allow do .claude/settings.json versionado é todo `Bash(git -C * log *)`. Numa máquina
onde o agente chama a tool PowerShell, nenhum desses padrões casa e o usuário leva prompt de permissão
em tudo. Mesma classe do /mnt/workspace: config versionada assumindo um ambiente. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27

README.md descreve um WOS que não existe mais: diz que "the registry that would let you switch one off
is unbuilt … Today it is all or nothing", mas features.txt (76 features), profile.txt e
`wos/features --on|--off` estão lá e funcionam. proj: os-agnostic-port
— sessão port agnóstico de SO · 2026-08-27


o port do WOS pra Windows achou que o bloqueio real não era o bash. das 139 falhas da baseline, ~45
eram uma coisa só: os testes spawnam `python3`, que no Windows não existe — o alias da Microsoft
Store responde, imprime um anúncio e sai 9009. o gate nunca roda e quem chamou lê o anúncio como se
fosse a saída do gate. uma função de 3 linhas (`platform_law.interpreter()`) devolveu 41 testes.
eu tinha cortado ela do plano como "API sem caller" — os ~20 callers eram spawn sites, não imports,
então procurar por uso não achava nada.
— sessão port os-agnostic S2 · 2026-08-28

o entropy dashboard vê um workspace menor nesta máquina: 713 arquivos escaneados contra 2368, e a
metade dos repos aninhados some. um teste rodou o dashboard e reescreveu o bloco gerado do
ISSUES.md com esse retrato parcial — revertido. duas assimetrias num achado só: um teste que suja
arquivo rastreado, e uma medição que fica menor sem dizer que ficou.
— sessão port os-agnostic S2 · 2026-08-28

`.gitignore` não tinha `.venv/`. o venv entrou num `git add -A` meu e foram 6207 arquivos pro
commit antes de eu pegar. adicionei a linha. o allowlist não nomear o venv pega o próximo também.
— sessão port os-agnostic S2 · 2026-08-28

o Bash do Git no Windows converte argumento que parece path POSIX absoluto: `git grep '/mnt/workspace'`
devolve zero porque o MSYS reescreve o padrão pra `C:/Program Files/Git/mnt/...`. sem a barra
inicial funciona. qualquer medição nossa que passe path absoluto por bash aqui mente calada.
— sessão port os-agnostic S2 · 2026-08-28

`core/tools/wos/roundup` é bash, então o ritual de fechamento não roda no Windows — este fechamento
foi à mão. e `caveman` não está em `core/hooks/vendored.txt`, apesar de o plano do port afirmar que
estava quarentenado ali. ou entra na lista, ou para de ser chamado de vendored.
— sessão port os-agnostic S2 · 2026-08-28

os gates do workspace nunca rodaram nesta máquina, e agora rodam — mas ainda não bloqueiam. o shim
estava quebrado em duas camadas: `/mnt/workspace` não existe aqui, e `python3` cai no alias da Store.
consertei as duas com `core/hooks/run`. o que sobra é a lógica dos gates, e tem dois bugs:
`context-gate.py:45` compara path como texto (`str(target).startswith(str(WORKSPACE) + '/')`), e no
Windows o alvo tem `\` contra um prefixo com `/`, então nunca casa e todo acesso retorna 0 cedo —
passa em silêncio, o mesmo modo de falha do anúncio da Store. são 3 sítios (`chain.py:53`,
`context-gate.py:45`, `spec-read-gate.py:79`).
— sessão permissões + push · 2026-08-28

e o segundo, que é o que impede consertar o primeiro sozinho: os marcadores de sessão vivem em `/tmp`
literal, em 15 arquivos. do Python nativo `/tmp` é `C:\tmp`, que não existe; do Git Bash é o `/tmp`
do MINGW. shell e Python discordam sobre onde estão os marcadores, e `pre-read.sh` (shell) lê
marcadores que `context-tracker.py` (Python) escreve. consertar só a comparação faria o gate bloquear
sem nunca poder ser satisfeito — o workspace ficaria inutilizável aqui. os dois precisam ir juntos, e
isso é a migração de-bash.
— sessão permissões + push · 2026-08-28

`test_shim_paths.py` guardava opencode, copilot e zcode — nunca `.claude/settings.json`. o shim que o
teste existia para guardar era o único que ele não lia, e foi ali que 20 comandos mortos sobreviveram.
adicionei. a lição não é o arquivo faltando, é que a tabela de shims era escrita à mão e ninguém
comparou com `ls` das configs que existem.
— sessão permissões + push · 2026-08-28

as duas máquinas commitam com e-mails diferentes: `lsf@cin.ufpe.br` aqui, `lucas.sfigueiredo@ufrpe.br`
na outra. mesmo Lucas, dois autores no GitHub. não mexi — é decisão sua qual é o canônico.
— sessão permissões + push · 2026-08-28

a saída das nossas ferramentas quebra acento no console do Windows: `permissions --check` imprimiu
`permissions: open � rendered config matches`. o port declarou encoding na leitura e escrita de
arquivo, mas `sys.stdout` ainda herda o cp1252 do console.
— sessão permissões + push · 2026-08-28

as quatro linhas `apt` do `core/tools/deps.txt` (poppler-utils, ffmpeg, tesseract-ocr, ddgr) seguem
POSIX-only: o `wos/deps` imprime `sudo apt-get` pra elas, que não roda aqui. o `kind: system` novo
resolve pelo platform_law, mas não migrei essas quatro — cada uma precisa que alguém verifique que o
mesmo nome resolve nos três gerenciadores, que foi o que fiz pro `gh` e custa uma sonda por linha.
migrar sem verificar seria afirmar uma portabilidade que ninguém mediu.
— sessão permissões + push · 2026-08-28

o `bash -n` do verify-fast só cobre `core/hooks/*.sh` e `*/*.sh`. os três arquivos de shell com o
maior raio de dano do workspace — `pre-commit`, `post-commit` e o `run` novo — não têm extensão
porque o git dita os dois primeiros nomes, então eram exatamente os três que nada checava. cobri num
teste; o alvo do Makefile continua estreito.
— sessão permissões + push · 2026-08-28
https://www.instagram.com/reel/DcOxARouQxF/?igsi=NTc4MTIwNjQ2YQ==
essa é a mentalidade de AI4good, talvez encaixe em algum lugar
— via aiwbot · 2026-08-28

três ferramentas mentem caladas nesta máquina, e as três me custaram tempo real numa sessão só.
(1) o Git Bash converte argumento que parece path POSIX absoluto: `git grep '/mnt/workspace'` devolve
zero num tree que tem 126 ocorrências — use `MSYS_NO_PATHCONV=1` ou a tool Grep. (2) o
`Measure-Object -Line` do PowerShell não conta linhas em branco, subestima ~20%, e fez a S2 prometer
um corte que não existia — use `wc -l`. (3) **a tool Grep normaliza separador de path DENTRO do
conteúdo casado**, não só no prefixo: ela me mostrou `'core\hooks\pre-commit'` num arquivo que
contém `'core/hooks/pre-commit'`, e eu quase "consertei" um bug inexistente. **confirme com Read
antes de agir sobre um path visto via Grep.** as três merecem um lar versionado — o handoff é
`outputs/`, que é gitignored, então tudo que mora só lá morre com a máquina.
— sessão port do caminho de commit · 2026-08-28

https://www.instagram.com/reel/DcRMN_hM537/?igsi=NTc4MTIwNjQ2YQ==
adicionar nas minhas aulas
— via aiwbot · 2026-08-28

corrigir o nosso gitflow forçando que commits para a main só podem vir da develop. 

estudar se vale a pena diminuir o verbose das nossas tools

https://www.instagram.com/reel/DclKZARteCP/?utm_source=ig_web_copy_link
será que vale a pena implantar no wos?
— via aiwbot · 2026-08-28

no apptime, no cronômetro geral e nas estatísticas todas, excluir apps não monitorados. um caso que tem acontecido comigo e que é "misleading" é o gmaps, que aumenta muito meu uso diário mas não devia pq está como 'não-monitorado'
— via aiwbot · 2026-08-27
