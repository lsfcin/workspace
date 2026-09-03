# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

resolver isso do gcalendar, calendário pessoal deveria ser o novo centralizador, calendário do cin é útil pro pessoal do voxar saber como tá meu horário então.

acabei de rodar uma sessão inteira no opus só pra atualizar uns slides, e apesar da discussão na sessão ser boa o resultado nos slides foi péssimo, acabei pulando tudo que foi feito pela IA. os fluxos, as frases, tudo muito artificial, linguagem muito explicadinha... existe uma diferença grande no meu estilo de slides vs o que a IA gerou, talvez direcionar ela pra produzir em dois caminhos, um é o que será as notas de apresentador e outro são os slides em si, que ao meu ver servem de guia visual, de provocação e não de leitura. as imagens ficaram bem ruins também, pequenas, mal espaçadas, o texto por vezes ficava um por cima do outro, e pequenos também... enfim, design não é o forte e descobrimos mais uma vez essa limitação...

https://www.instagram.com/reel/Dc0okrDRp2z/?utm_source=ig_web_copy_link
— via aiwbot · 2026-09-03

considerar usar isso nas nossas janelas das casinhas
— via aiwbot · 2026-09-03

pesquisar skill UNSLOP e ver se vale a pena pra gente

pesquisar aihero.dev e ver se serve pra gente
pontos que podemos ver /grill-me, /implement pq usa TDD

ai-2027.com pode servir pra gente?

https://www.instagram.com/reel/DcyFpRtxEZn/?igsi=NTc4MTIwNjQ2YQ==
falar desse estudo nas minhas aulas, mobilidade social e diploma ainda demonstram causalidade
— via aiwbot · 2026-09-02

https://www.instagram.com/reel/DcyFJB0smCG/?igsi=NTc4MTIwNjQ2YQ==
quero discutir isso nas minhas aulas
— via aiwbot · 2026-09-02

https://www.instagram.com/reel/DcyNNHKtEsL/?igsi=NTc4MTIwNjQ2YQ==
será que faz sentido?
— via aiwbot · 2026-09-02

to com uma forte suspeita que os nossos hooks e talvez tools também estão consumindo muito mais tempo do que precisariam, honestamente, acho difícil acreditar que seja algo normal. o problema parece ser mais grave no windows inclusive

pesquisar sobre finasterida e outras estratégias pro cabelo, quero ver se tem uma forma saudável de conter ou até recuperar as minhas entradas. fazer isso direito, pesquisa científica, etc
— via aiwbot · 2026-09-01

https://www.instagram.com/reel/DZnwqiWuvZu/?utm_source=ig_web_copy_link
backchain dominance é uma coisa real? investigar, pesquisar, e aí talvez incluir na minha bateria de exercícios
— via aiwbot · 2026-09-01

https://www.instagram.com/p/DcuI3KiDuyu/?utm_source=ig_web_copy_link
interessado em particular nas animações svg
— via aiwbot · 2026-09-01

task: month — `academy/papers/megatruth/` é o único paper sem repo próprio: os outros nove têm o
seu, e por isso o `CONTEXT.md` deles é carregado por alguém. O do megatruth não era carregado por
ninguém, e a linha em `academy/papers/CONTEXT.md` apontava pra um arquivo que nenhum clone recebe.
Tirei a linha em 2026-09-01 (decisão reversível). Duas saídas, e a escolha é tua: dar um repo ao
megatruth como todo paper tem — aí o `CONTEXT.md` volta a ser roteado e o conteúdo ganha história,
que hoje não existe em lugar nenhum — ou deixar o paper local mesmo, sem linha.

sessão wos-zero (GLM flash, 2026-08-31): 13 commits na feature/inbox-drain — B3 B5 B6 B7 B9 B11 B12 B13 resolvidos com specs, B4 restaurado como o único bug aberto, cap de linha vence coluna (norm), refs fold, SPECS-module, harnesses.txt, issues-gate lê deleção. Fila: cortar os 4 files over-200 (SETUP 605, hooks/SPECS 361, core/SPECS 266, SCHEMA 226 — corte de conteúdo, um por sessão), PT→EN do corpus, resto do ROADMAP (28 findings aqui). PAYBACK de --no-verify: a sessão paralela editando core/norms/improve.md precisa commitar; até lá o round-trip do norms fica vermelho pra todo mundo.

será que tem como bloquear a adição de novas linhas no WOS? nenhum commit adiciona sem que diminua de outro canto?  

task: today — VPN do CIn está de pé e funcionando (IPv4 sai por Net-ExtVPN-extIP.cin.ufpe.br), mas o dispatcher que bloqueia IPv6 durante a VPN NÃO foi instalado: falta um `sudo install` que eu não consegui rodar. Enquanto isso todo site com AAAA é acessado com o IP de casa, e periódico/editora não reconhece o acesso institucional — silenciosamente. Comando e script prontos em `SETUP-accounts.md` § VPN do CIn (bloco Install, heredoc do `90-vpn-cin-ipv6`); a Precondição/Verify da própria seção diz se já foi. Decidir também: `SETUP-accounts.md` foi de 113→163 linhas com essa seção e passou do aviso de 150 — ou corta ~13 linhas (candidato: a seção Exa API key, 15 linhas para uma feature opcional), ou o heredoc do dispatcher vira arquivo versionado (−14 aqui, +1 arquivo).

sessão metodologia-aulas (2026-09-01): duas assimetrias achadas e não consertadas. (1) `brain/drafts/` não tem CONTEXT.md, não está na routing de `brain/CONTEXT.md` e por isso não entra no allowlist do `.gitignore` (`brain/*`) — as quatro metodologias de aula estão fora do git, e a única cópia é o disco. Ou drafts vira subtree de verdade (CONTEXT.md + linha de exceção), ou é declarado efêmero por escrito. (2) os rascunhos carregam nome de provedor no arquivo (`-sonnet`, `-gemini`, `-opus`), contra a norma de naming provider-agnostic; aqui o provedor É o dado (experimento cego de três saídas), então ou a norma ganha exceção escrita para experimento comparativo, ou os três viram `-a/-b/-c` com o provedor dentro do arquivo. Decidir antes de o padrão se espalhar.
