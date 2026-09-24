# inbox
> zero friction. thoughts. no taxonomy. no formating. handle duplications.
> triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted.
>
> signal the route preemptively (optional — agent infers if omitted):
> `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete`

---

<!-- add entries below, newest first -->

aprimorar os templates (e talvez specs se fizer sentido) de teaching diznedo pra incluir nos artefatos instruções para os humanos sobre como usar e como não usar os agentes/ia

temos uma seção "how to use" no readme do wos? dizendo do roundup, handoff, etc, as dicas gerais de uso

na coluna de nota dos paineis das disciplinas (disciplina.md) dar um espaço extra pra caber o 100 pts alinhado
ex.:
◻◻  00 pts
◻◻ 100 pts

na disciplina de ai4good, ao invés de 1 artefato sem pra seminário, teremos três, sem1, sem2, e sem3. o artefato da demonstração, do artigo e um extra do pitch devem somar o que falta pra fechar os 50 itens, pelas minhas contas essa soma dá 23, e aí pensei em fazer como demonstração 5, artigo 6, pitch 12 (aí pode rever as abreviações)

nas especificações das disciplinas, talvez nos artefatos em si, incluir parágrafos de "comando/prompt: ..." em que faço sugestões de prompt ou pro artefato como um todo ou pra cada parte da metodologia (acho melhor essa segunda opção). outra coisa, sempre que listarmos algum termo em português que é mais conhecido por sua versão em inglês a gente inclui a tradução pra inglês em parênteses e em itálico (ex.: retropropagação - backpropagation). isso pra todos os materiais, slides, site, etc.

pq o nome do repo publico do wos ficou wos-ablation? deveria ser só wos...

o antigravity compacta sozinho, confesso que acho isso perigosíssimo... será que tem como impedir?

NÃO MEXER ATÉ 2026-09-29 — nenhum /inbox deve rotear, resolver ou apagar esta entrada antes dessa
data. dia 28/09 vence a primeira leitura do scoreboard (ROADMAP.md § Measurement), e é só depois
dela que a gente pode mexer em como o core/scoreboard.tsv guarda as linhas. o scoreboard tá com
5.8 MB porque só cresce e nunca colapsa; a matriz de leitura que nasceu em 2026-09-22
(core/read-matrix.tsv) resolve isso com janela circular de 365 dias, e a ideia é o scoreboard
tomar essa mesma forma. mudar antes seria gastar a medição pra arrumar o arquivo de onde ela sai.
o item tá escrito em ISSUES.md como b20260922-state-stores; esta linha existe só pra você lembrar
de soltar a trava no dia 29. — via sessão 2026-09-22

será que podemos oficializar os nossos arquivos que são tsv mas que estão no formato .txt como .tsv? tem algum ponto negativo em fazer isso?

será que é útil pra gente
https://www.instagram.com/reel/DdmQR7MgQtG/?stkn=NTc4MTIwNjQ2YQ==
será que roda em 6gb de vram?

https://www.instagram.com/p/DdmKNCMhy0y/?utm_source=ig_web_copy_link
a gente deveria fazer isso no Brasil
— via aiwbot · 2026-09-22

tenho que aprender como atualiza os links dos .md (ex.: das minhas aulas). quero ganhar autonomia sobre isso. não depender da IA quando quiser fazer sozinho. isso é URGENTE, não quero deixar esse item do inbox ser jogado em algum roadmap perdido.

https://www.instagram.com/p/Ddl6O0jjTI3/?stkn=NTc4MTIwNjQ2YQ==
surfando na onda do JEV, agora Laya, e é local
— via aiwbot · 2026-09-22

https://www.instagram.com/reel/DdlvmwjTUb8/?utm_source=ig_web_copy_link
considerar pras obras um mix de energia solar + baterias
— via aiwbot · 2026-09-22

https://www.instagram.com/reel/Ddlr9B7DRmF/?utm_source=ig_web_copy_link
incluir na rotina de exercícios
— via aiwbot · 2026-09-22

ai4good: sistema de enigmas (formulário, versões por enigma, rastreio de acesso e envio) a partir de 30/09; sessão da VA2 (50 caixas, esqueleto em academy/teaching/classes/ai4good/plano-refino.md) antes de 02/10; seção legado da página depois. — via claude · 2026-09-23

techedu: como o painel e as caixas funcionam com equipes (ai4good é individual; ficou para outra sessão). — via claude · 2026-09-23

ai4good, reels nos slides: pra cada reel usado nos 4 decks novos (Jev/Laya, DOAC, demissão Anthropic…), achar o vídeo original no YouTube e inserir no slide (createVideo). legenda/dublagem pt-br não dá pra fixar no slide: é escolha do player na hora (⚙ → legendas → traduzir; faixa de áudio só se o canal ativou dublagem). — via claude · 2026-09-23

ai4good, refino que ficou pra depois da aula de 23/09: notas de apresentador nos slides ANTIGOS dos 4 decks, notas propostas pros slides só-imagem (autopreservação 44–60, 86–88; agência 92–99, 108–124) e correções visuais in loco. conteúdo em academy/teaching/classes/ai4good/*_conteudo.py. — via claude · 2026-09-23

wos, slides (IMPROVE WOS): (1) não há guia de estilo visual dos decks do Lucas — inferido hoje: Open Sans, título minúsculo bold + termo inglês itálico, fonte 8pt no rodapé, azul #1A73E8 como único destaque; vive só em ai4good/slides_pecas.py. (2) par desenhado + fallback pulado virou convenção → candidato a regra em [slides-dois-caminhos]. (3) links de deck seguem `<disciplina>/<tema>` apontando pra /present. (4) gslides não tem subcomando pra separar deck, copiar slide entre decks (a API não copia: slides_build.py reconstrói), inserir nota ou imagem — ai4good/slides_build.py é candidato a subir pra core/tools/slides. (5) gdrive não tem `rename`. (6) a regra de truncamento do routing acusa qualquer "…" numa descrição, mesmo sem truncar. — via claude · 2026-09-23

migrar o /prof para en-us, traduzindo E cortando ao mesmo tempo (como o /slides, que nasceu em inglês com os termos em pt entre crases) — decidido na sessão de slides de 2026-09-24

wos (IMPROVE WOS, sessão de slides 2026-09-24): (1) os espelhos das skills copiam só o SKILL.md, então os links relativos do /prof e do /slides para as subskills (`prof/x.md`, `slides/x.md`) não resolvem dentro de `.claude/skills/` — o agente acha pelo caminho do core, mas o link está quebrado; (2) as pesquisas de uma sessão ficam em `outputs/.drafts/`, que é gitignored: a outra máquina não vê as 5 pesquisas de slides; (3) `cfpages publish` imprime todo artefato, uma linha cada — talvez só a página e a contagem
