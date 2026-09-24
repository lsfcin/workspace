# plano de refino da página ai4good
> Decisões do diálogo de 2026-09-23 e as fases que faltam. Arquivo temporário: é apagado quando a última fase fechar.

## como trabalhar
- Toda mudança de TEXTO passa por Lucas como antes → depois, em lotes de perguntas (popup), uma seção por vez. Nada é gravado sem o OK dele.
- Mão dupla: cada decisão na página (micro) é espelhada no macro (`../../SPECS-disciplinas.md`, `../../structure/templates/`), e vice-versa. Ao ver uma incoerência entre os dois, pergunte.
- Ordem: do topo para baixo (site → materiais) e no tempo (passado → hoje → futuro).
- O painel é desenhado por `python3 academy/teaching/structure/painel.py academy/teaching/classes/ai4good/disciplina.md`, e `--check` confere. Nunca edite o desenho à mão. O `caixas=50` no marcador de dados trava a conta.
- Sessão paralela: outra sessão escreveu `slides_build.py`, `lm_conteudo.py` e `slides_pecas.py` aqui (não commitados em 2026-09-23). Use `git commit -- <paths>` e confira o branch.

## estado (branch feature/ai4good-disciplina)
- `08d7b1be` linha de base do Antigravity + planilha de notas fora do git (gitignore) + painel.md apagado.
- `8b6511b0` script do painel + o teto de tamanho desconta blocos gerados (`core/hooks/file_law.py` authored_text). Commitado com `--no-verify` (motivo na mensagem): rodar verify:fast quando os scripts da sessão paralela entrarem.
- A página ainda tem o conteúdo do Antigravity; só os marcadores do painel mudaram. O espelho `outputs/links/ai4good/` ainda não recebeu nada desta sessão.

## decisões
- **contas:** cada VA = 50 caixas = 100 pts = nota 10,0 no SIGAA. VA1 = git 3 + tex 4 + mlp·c 5 + mlp·r 5 + arq·c 5 + arq·r 5 + arn·c 5 + arn·r 5 (37) + 13 enigmas = 50. VA2 = outro bloco de 50 (sessão própria).
- **enigmas:** binários, 1 caixa = 2 pts (a meia caixa foi descartada: não há glifo do mesmo tamanho de ◼/◻). 1 enigma por deck de tópico, menos redes recorrentes, autopreservação e modelos de linguagem, que ficam `[0] slides` (a página ainda mostra redes recorrentes `[1]`, e o deck dela já tem os placeholders de gatilho e enigma: se virar `[0]`, tirar os dois). Conta aberta: com esses três em `[0]` ainda sobram 14 decks `[1]` para 13 enigmas; fechar no lote do cronograma (o enigma teste da abertura conta?). Um deck = um tópico, nunca fundir dois. Nenhum enigma foi aplicado até 23/09. A aplicação (minissistema de formulário, versões por enigma, rastreio de acesso/envio) é projeto do Lucas a partir de 30/09.
- **nomes:** "item de verificação" é o único termo (saem critério, ponto de verificação, critério de verificação). Em pt-br: `<tema> · código` → `<tema>·c`, `<tema> · relatório` → `<tema>·r`, com tema = mlp, arquitetura→arq, arena→arn. A abreviação sai inteira do nome completo e cabe na largura das caixas. Setup (confirmar com Lucas): "repositório git" → `git` (3), "projeto latex" → `tex` (4). Saem `pdf`, `cod` e `·p`. O arquivo continua `artefatos/<n>-<nome>.md` com n = nº de itens (o id é o nome). `[1] slides` = 1 enigma no deck. As trocas vão para um § vocabulário no SPECS-disciplinas (não no core/SCHEMA.md).
- **privacidade:** o painel público segue com NOMES REAIS, e "entregue" lista todos. O SPECS-disciplinas perde a proibição de painel nominal e ganha a justificativa do Lucas: as entregas já são públicas; os itens são binários e dados de antemão, sem julgamento; atraso é aceito sem ônus e o ponto é recuperável; há um clima de crítica construtiva entre colegas; ninguém é "pior", só "ainda não entregou". Falar de privacidade e explicar por que aqui ela foi tratada assim.
- **IA:** a IA faz, o aluno domina. A IA escreve código e texto; o aluno decide cada escolha e precisa explicar e defender tudo (enigmas sem IA conferem). O guia-ia da página ("nunca redija código ou texto") está errado → reescrever na página, nos templates e no SPECS.
- **itens dos artefatos:** a base é a lista original do Lucas (abaixo). Saem os acréscimos do Antigravity (mlp·c padronização obrigatória, git "assinado… mensagem estruturada", arn·c "temperatura/contexto", arn·r "7 alavancas", "SLM local", "5 papéis"). Exceção: mlp·r mantém os 5 itens do arquivo atual, que foram os conferidos em sala. Cada ajuste que eu propuser é mostrado como antes → depois.
- **passado:** o cronograma da página é o que aconteceu. As regras novas substituem as do Notion em silêncio (sem nota de transição).
- **VA3/VA4:** ficam no cronograma como formalidade, sem texto extra.
- **individual:** ai4good é individual (dupla sem distinção): painel VA2 com 1 linha por aluno. Equipes são assunto do techedu (outra sessão).
- **passo a mais / 7 alavancas:** entra na metodologia do artefato de ideação híbrida da VA2 (1–2 itens), não na página.
- **habilidades:** árvore derivada dos decks, com os mesmos nomes do cronograma e link por deck, agrupada por tema. Template e SPECS explicam que é a mesma fonte vista no eixo do tempo e no eixo da dependência.
- **VA2:** o esqueleto e os itens ficam para uma sessão própria, ANTES de 02/10 (brainwriting). Na página, até lá, o painel VA2 sai ou vira uma linha "em definição" (perguntar). Rascunho de partida: ide·r, cmp·r, bas·c, flx·r, exp·r (5 cada), it1·a/it2·a/it3·a (4 cada), pit·a (4 = as 4 dimensões da banca), prj·c 4, prj·r 5 = 50; `·a` = apresentação. Atenção: `arq` já é da VA1 (colidia).
- **entregue:** "slides" é o deck compartilhado 1p3rhulc…, então cada aluno aponta para o seu slide (#slide=id…; buscar os ids com a skill `slides`). davi overleaf = `https://www.overleaf.com/project/6a920bbbb8e36eb1e2f18159`, artur = `https://www.overleaf.com/project/6a920b9163f9ff8ef6829b60`. Os links de andreza (git), carlos (artigo) e albérico (nada): buscar nas respostas do gforms (`core/run tools/forms/gforms responses --account personal 1Nfdbl6jj5aG5AXMbK0wOip79v-3Q6gTrycVaxL8fqAY`) e nos repos; o que não achar, perguntar.
- **legado:** fora por hoje.
- **artefatos:** seguem o template-artefato E reaproveitam o material antigo: decks "Especificação" — setup `1tPA8BDEXU5S_qBrKspkW81Pj_gzZ0L0UC-flEtiNLEY`, mlp `1p3rhulc-_ZZxOOpETi8CJyiAJqA0VeiBLAg924iLD5c`, arquitetura `1nxPb6Df7eSBWiZBY0yOaMae0y1FUJ04v4bjINOk2MtQ`, adversarial (antigo, sem artefato hoje) `1FbH8pLTZzecBH6bkBiG2t2SxnXXZ86yJ7h-R-mPd2r0` e a planilha mapa de entregas `1IgBJWxItjmolBgwsnjlER894V6BP9nns8dFcc-NhStY`.
- **limpeza:** notion-port.md é apagado quando a migração fechar (depois de lidos os ids dos decks).

## lista original do Lucas (base dos itens)
- **git (repositório git):** 1 primeiro commit feito pelo harness (agente); 2 sistema de pastas integrando código e artigo no mesmo repo; 3 um .md por pasta, começando por AGENTS.md e seguindo com CONTEXT.md.
- **tex (projeto latex):** 1 ferramentas de geração de .pdf via projeto latex funcionando, primeiro pdf gerado pelo harness; 2 conexão com overleaf, primeira contribuição direta harness → overleaf; 3 ferramentas de busca de artigos no workspace (plataformas utilizáveis por agentes), download de pdf, ocr automático (zero-token) incluindo imagens, pasta refs/ do artigo com mecânica de geração dos .yaml; 4 árvore de pesquisa no workspace: skills para coleta, leitura e revisão de artigos, diálogo sobre metodologia, montagem de experimentos e escrita técnica.
- **mlp·c:** 1 subrepositório na pasta de código, seguindo o WOS, com CONTEXT.md; 2 rede configurável em tempo real, aplicação rodando, arquitetura (camadas, neurônios por camada) e hiperparâmetros (taxa de aprendizagem, épocas, ativações etc.) configuráveis pelo usuário; 3 base baixada e separada em treino (80%) e teste (20%), OPCIONALMENTE tratada (duplicatas, padronização); 4 treinamento com feed forward e backpropagation; 5 visualização da atualização dos pesos a cada época, em números e espessura das arestas.
- **mlp·r (Lucas tinha 3; ficam os 5 do arquivo atual, conferidos em sala):** a lista dele: report-mlp.tex; background técnico escrito com o harness e as skills de escrita (ML, por que regressão linear é ML, erro, mínimos quadrados × gradiente descendente, neurônio artificial, feed forward e backprop de 1 neurônio com números reais, por que mais neurônios; imagens e equações); método e resultados enviados ao overleaf pelo harness, com gráfico de acurácia de treino e teste por época e tabela.
- **arq·c:** 1 subrepositório (WOS, CONTEXT.md); 2 dataset do artigo ou compatível baixado; 3 código do modelo do artigo baixado, inferência feita; 4 treino no dataset sem mudanças no modelo; 5 alteração substancial da arquitetura ou do treino, motivada por melhorar algo (desempenho/velocidade, acurácia…): camadas novas, conexões residuais, outro backbone, fine-tuning; resultados coletados depois.
- **arq·r:** 1 report-arch.tex; 2 artigo de 2023+ com CNN, GNN ou RNN/LSTM e código no github; seção de motivação (por que o artigo, qual rede, qual oportunidade de contribuição); 3 ≥ 3 parágrafos (via harness) sobre o trabalho base em trabalhos relacionados; 4 planilha comparativa com as métricas dos autores: original reportado, reproduzido sem alterações, depois das alterações; 5 resultados qualitativos explicando os quantitativos com exemplos dos dados (o que passou a funcionar, o que deixou de funcionar).
- **arn·c:** 1 subrepositório (WOS, CONTEXT.md); 2 README com a arquitetura/diagrama de papéis e comunicação dos agentes; 3 prompts de cada papel; 4 agentes com busca na web; 5 agentes com thinking/reasoning.
- **arn·r:** 1 report-arena.tex; 2 arquitetura do experimento (papéis, fluxo); 3 condições técnicas (modelos, máquina, desempenho, tempo de execução); 4 resultados em tabelas e imagens claras; 5 discussão com destaques e subseção de limitações.

## achados abertos (resolver nas fases)
- Artefatos: `3-base-git-repo.md` diz código `cod`; nenhum dos 8 segue o template-artefato.
- `entregue`: andreza tem git=vvv mas nenhum link de git; carlos tem mlp·r 4/5 e nenhum link de artigo.
- Assimetria aceita (2026-09-23): o `publicacao` do template publica o próprio template, não uma disciplina; quem cria uma disciplina copia o bloco da ai4good.
- Rótulo final do painel: hoje é "nota 1" sobre "32 pts". Propor "pts" ou "nota" com vírgula (3,2)?
- `template-disciplina.md` publica como `template_disciplinas.md` (underscore e plural): nome assimétrico.
- SPECS-disciplinas: arcos dizem "~30 encontros", o semestre tem 34; a folha de banca (4 dimensões) não aparece em lugar nenhum da página nem dos artefatos.
- Visão com jargão ("subverter a lógica inerente às crises").

## fases
1. ✔ higiene + teto (commits acima).
2. **página, seção a seção** (lotes antes → depois; cabeçalho, comunicação, guia-ia, publicacao, visão e regras fechados com espelho no template e no SPECS): cronograma (`[1]`/`[0] slides`; decks e links conferidos em 2026-09-24) → painel VA1 (dados com códigos novos: `tex` com 4 caixas, `mlp·r`, `arq·r`, `arn·r`, 13 enigmas, `caixas=50`; rodar o painel.py) → painel VA2 (placeholder) → entregue → referências → habilidades (árvore).
3. **macro espelhado:** SPECS-disciplinas (privacidade com justificativa, ontologia e nomes, enigma, VA = 50, papel da IA fora da nota do guia-ia, § vocabulário, checklist dos agentes, 34 encontros) + template-disciplina + template-artefato (ajustar onde a instância mostrar o erro) + CONTEXT.md.
4. **artefatos da VA1**, um lote por artefato: ler os decks de Especificação (skill `slides`) e a planilha mapa (skill `drive`), reescrever no template a partir da lista acima com as minhas propostas, renomear (`3-repositorio-git.md`, `4-projeto-latex.md`, `5-mlp-codigo.md`, `5-mlp-relatorio.md`…).
5. **publicar:** copiar para `outputs/links/ai4good/` (+ .html pareado de cada artefato renomeado; remover os velhos), commit e push no lsf-links. Lucas olha no PC e no celular antes do push final.
6. **fechar:** apagar notion-port.md e este plano; INBOX com o que sobrar; commit.

## verificação
- `painel.py --check` sai 0; VA1 = 50 caixas por aluno; pts = 2 × ◼.
- Cada `[n]` no cronograma == nº de itens do arquivo; todo link `artefatos/…` existe no canônico e no espelho.
- `diff -r` dos .md entre canônico e `outputs/links/ai4good` vazio; página e .md raw respondendo no ar.
- grep sem sobras: "critério de verificação", "ponto de verificação", `pdf=`, `cod`, `·p` em ai4good, templates e SPECS.
