# Conteúdo novo do deck "Aula - Autoaprimoramento" (aula de 23/09/2026), aplicado por slides_build.py.
from slides_pecas import GRAY, titulo, fonte, numero, imagem, desenhado, fallback, secao, vocabulario, verificacao

PREFIX = "ap23"
# movidos para o deck Language Models, apagados daqui depois do build: slides 5–10 e o LoRA (33)
MOVIDOS = ["g39b93bc0e41_0_24", "g39bf4d154ea_0_416", "g39bf4d154ea_0_438", "g39bf4d154ea_0_444",
           "g39bf4d154ea_0_449", "g39bf4d154ea_0_424", "g39bf4d154ea_0_387"]

RSI = "https://www.anthropic.com/institute/recursive-self-improvement"
ALPHAEVOLVE = "https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/"
DREAM = "https://arxiv.org/abs/2609.14858"
S2 = "https://arxiv.org/abs/2609.19644"
METR = "https://metr.org/time-horizons/"
METR11 = "https://metr.org/blog/2026-1-29-time-horizon-1-1/"
IMG_RSI = "https://www-cdn.anthropic.com/images/4zrzovbb/website/6d4a0d28992ade92d6fa63646fd9c9d318245c6c-2400x1260.jpg"
IMG_DREAM = "https://the-decoder.com/wp-content/uploads/2026/09/dream-rsi-generated-image-nano-banana-pro.jpg"
IMG_S2 = "https://scientist-two.github.io/static/images/teaser.png"
IMG_METR = "https://metr.org/assets/images/time-horizon-domains/time-horizons-increasing.png"


def texto(t, y=.5, h=.35, size=14):
    return [("text", .05, y, .42, h, t, {"size": size, "color": GRAY})]


ABERTURA = [
    desenhado([("text", .08, .28, .84, .25, "uma IA já melhora a si mesma?", {"size": 34, "bold": True, "align": "CENTER"}),
               ("text", .08, .5, .84, .15, "o que precisa mudar: o código, os dados, a busca ou os pesos?", {"size": 20, "italic": True, "color": GRAY, "align": "CENTER"})],
              "Pergunta de abertura. Separe as quatro coisas que podem melhorar: o código em volta (DGM), os dados de treino (SEAL), a estratégia de busca "
              "(Dream-RSI) e os pesos. Cada caso do deck mexe numa delas; quase nenhum mexe nos pesos sozinho. Anote o palpite da turma."),
    fallback("pergunta de abertura",
             "Pergunta: uma IA já melhora a si mesma? O que muda: código, dados, busca ou pesos?\n"
             "Mapa dos casos: Darwin Gödel Machine reescreve o próprio código de agente; SEAL gera os próprios dados e ajusta pesos com LoRA; "
             "Dream-RSI melhora só a política de exploração; AlphaEvolve e o Claude escrevem o código de quem treina a próxima IA.\n"
             "Layout: pergunta grande, subpergunta em itálico."),
]

LOOP = [
    desenhado(titulo("a IA escreve a IA", "AI building AI") + imagem(IMG_RSI, y=.28, h=.4)
              + numero("80%+", "", y=.26)[:1]
              + texto("do código mesclado na Anthropic, em maio de 2026,\nfoi escrito pelo Claude. antes do Claude Code (fev/2025):\npoucos por cento.\n\n"
                      "engenheiros entregam 8× mais código que em 2021–2025.", y=.47, h=.4)
              + fonte("Anthropic Institute — When AI builds itself (2026)", RSI),
              "Esse é o elo real do loop recursivo hoje: a IA escreve boa parte do código de quem constrói a próxima IA. O AlphaEvolve faz o mesmo no Google "
              "(0,7% do compute mundial recuperado, kernel do Gemini mais rápido). A própria Anthropic diz: ainda não é autoaprimoramento recursivo completo, "
              "que seria desenhar o sucessor sozinho, mas pode chegar antes de as instituições estarem prontas."),
    fallback("a IA escreve a IA",
             "Anthropic Institute, 'When AI builds itself' (2026): em maio de 2026, mais de 80% do código mesclado na Anthropic era do Claude; antes do Claude Code "
             "(fev/2025), poucos por cento. Engenheiros entregam em média 8× mais código por trimestre que em 2021–2025. Define autoaprimoramento recursivo "
             "como um sistema que projeta e desenvolve o próprio sucessor de forma totalmente autônoma: 'ainda não estamos lá', não é inevitável, pode vir antes "
             "do que as instituições esperam. " + RSI + "\n"
             "AlphaEvolve (DeepMind, mai/2025): heurística de escalonamento que recupera 0,7% dos recursos de computação do Google; kernel que acelerou o treino do Gemini. "
             + ALPHAEVOLVE + "\nImagem: capa da página da Anthropic. Layout: número grande + imagem."),
    desenhado(titulo("sonhar antes de tentar", "Dream-RSI") + imagem(IMG_DREAM, y=.25, h=.45)
              + numero("162×", "", y=.26)[:1]
              + texto("menos chamadas ao agente para achar um solver Lasso.\n\no histórico de descobertas vira um simulador;\no agente 'sonha' estratégias nele e só leva as boas pro mundo real.\n\nos pesos não mudam: melhora a busca.", y=.47, h=.42)
              + fonte("Google / Google DeepMind — Dream-RSI: Recursive Self-Improvement through Evolving Worlds, arXiv 2609.14858 (14/09/2026)", DREAM),
              "Nove dias atrás. O detalhe que os posts escondem: nada nos pesos muda; o que melhora é a política de exploração. É autoaprimoramento de verdade, "
              "mas de um pedaço específico. Bom para separar o fato do mito: 'a IA se reescreve' quase nunca quer dizer 'reescreve o próprio cérebro'."),
    fallback("Dream-RSI",
             "Dream-RSI (Google e Google DeepMind, arXiv 2609.14858, 14/09/2026): a política atual explora e registra árvores de descoberta; as árvores viram um "
             "conjunto de simuladores; políticas candidatas são avaliadas 'sonhando' nesse conjunto (feedback barato, off-policy); a melhor volta pro online e "
             "o conjunto cresce. Resultados em engenharia de algoritmos, otimização matemática e kernels de GPU: 162× menos chamadas num solver Lasso; mais de "
             "50× de economia em três problemas matemáticos. O modelo de base fica fixo. " + DREAM + "\n"
             "Captura de origem: post Vyzual AI (academy/refs/REFS.md, [aula-dream-rsi]). Imagem: capa do The Decoder (gerada por IA — dizer isso)."),
]

CIENTISTA = [
    desenhado(titulo("a IA que faz ciência", "ScientistTwo") + imagem(IMG_S2, y=.25, h=.5)
              + numero("91,9%", "", y=.26)[:1]
              + texto("dos artigos 'aceitos'... por revisores que também são IA.\n\nlê um artigo de conferência, acha a falha, propõe,\nprograma, faz ablação, escreve e rebate revisores.\n80,4% de sucesso em 100+ desafios de ML.", y=.47, h=.42)
              + fonte("Google Cloud AI Research + U. Waterloo — ScientistTwo, arXiv 2609.19644 (18/09/2026)", S2),
              "Cinco dias atrás. O ciclo inteiro da pesquisa, sozinho. Metade da lição está no número: quem avaliou foram revisores automáticos. "
              "Pergunta: se a IA escreve e a IA revisa, quem garante que é ciência? Ponte com o deck de crises: a crise da ciência em AI4Good."),
    fallback("ScientistTwo",
             "ScientistTwo (Google Cloud AI Research e Univ. of Waterloo, arXiv 2609.19644, 18/09/2026): framework multiagente que, dado um artigo de ICLR/ICML/NeurIPS, "
             "diagnostica limitações, gera hipóteses ranqueadas por novidade, escreve e depura código, verifica ganhos, isola a causa por ablação, redige o artigo "
             "e responde a revisores simulados com novos experimentos. 80,4% de sucesso em 100+ desafios de ML; 91,9% de aceitação sob o revisor automático "
             "ScholarPeer; 72,1% atingem padrão alto no Stanford Agentic Reviewer. Todas as avaliações de aceitação são automáticas. " + S2 + "\n"
             "Página: https://scientist-two.github.io/ · Captura: academy/papers/ai4good/refs/REFS.md. Imagem: teaser do projeto."),
]

LORA = [secao("LoRA mudou de casa\n→ deck language models",
              "O parêntese sobre LoRA agora mora no deck language models (lucassf.pages.dev/ai4good/language-models). Aqui basta: o SEAL ajusta os próprios "
              "pesos com LoRA, que treina matrizes pequenas ao lado dos pesos congelados.")]

METR_ = [
    desenhado(titulo("o horizonte cresceu", "METR time horizons, 2026") + imagem(IMG_METR, y=.25, h=.55)
              + numero("~12 h", "", y=.26)[:1]
              + texto("de tarefa humana que o Claude Opus 4.6 completa\ncom 50% de sucesso.\n\ndobra a cada ~4 meses (131 dias, método TH1.1).\nacima de 16 h, o METR diz que a medida não é confiável.", y=.47, h=.42)
              + fonte("METR — Task-Completion Time Horizons of Frontier AI Models (2026)", METR),
              "Atualiza os slides de 2025: lá o horizonte dobrava a cada 7 meses. Com o método de janeiro de 2026 (TH1.1), a dobra depois de 2023 é de 131 dias. "
              "O próprio METR avisa: acima de 16 h a suíte de tarefas não mede bem, e são tarefas de software."),
    fallback("METR atualizado",
             "METR, página viva de horizontes: " + METR + " · Time Horizon 1.1 (29/01/2026): " + METR11 + "\n"
             "Opus 4.6: horizonte de 50% em torno de 12 h. TH1.1: dobra pós-2023 em 131 dias (165 no TH1). Maio/2026: medidas acima de 16 h não são confiáveis "
             "com a suíte atual. Limitações: https://metr.org/notes/2026-01-22-time-horizon-limitations/\n"
             "Imagem: gráfico do METR (conferir se é o mais recente na página antes de apresentar)."),
]

FECHO = [
    vocabulario(["autoaprimoramento", "recursivo", "sucessor", "código × pesos", "dados sintéticos", "LoRA",
                 "política de exploração", "simulador", "revisor automático", "horizonte de tarefa", "benchmark", "mito × fato"]),
    verificacao(["no Dream-RSI, o que melhora e o que fica igual?",
                 "por que o 91,9% do ScientistTwo não prova que os artigos são bons?",
                 "qual é hoje o elo mais concreto do loop 'IA constrói IA'?"],
                "Volte à abertura: código, dados, busca ou pesos? Ponte pro próximo deck: um sistema que melhora quer continuar existindo?"),
    fallback("vocabulário e verificação",
             "Respostas: (1) melhora a política de exploração; os pesos do modelo ficam fixos. (2) quem aceitou foram revisores automáticos, não pares humanos. "
             "(3) a IA escrevendo o código de quem treina a próxima IA: 80%+ do código mesclado na Anthropic; AlphaEvolve na infraestrutura do Google.\n"
             "Layout: grade 4×3; três perguntas grandes."),
]

INSERCOES = [
    ("g289ea4407ca_0_0", ABERTURA),
    ("g39bf4d154ea_0_212", LOOP),
    ("g39bf4d154ea_0_223", CIENTISTA),
    ("g39bf4d154ea_0_387", LORA),
    ("g39bf4d154ea_0_322", METR_ + FECHO),
]
