# Conteúdo novo do deck "Aula - Language Models" (aula de 23/09/2026), aplicado por slides_build.py.
import os
from slides_pecas import (GRAY, LIGHT, MID, ACCENT, WHITE, titulo, fonte, legenda, tokens, modelo, barras, desenhado,
                          fallback, secao, clones, vocabulario, verificacao)

PREFIX = "lm23"
SVG_URL = os.environ.get("SVG_URL")  # url pública do png da versão (b)

GPT2 = "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"
BERT = "https://arxiv.org/abs/1810.04805"
BART = "https://arxiv.org/abs/1910.13461"
JEV = "https://typesafe.ai/blog/introducing-system-one-models-and-jev"
LAYA = "https://github.com/mizorewww/laya-mlx"
QWEN = "https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507"
CACHE = "https://docs.claude.com/en/docs/build-with-claude/prompt-caching"
VEC2TEXT = "https://arxiv.org/abs/2310.06816"
F_GPT = fonte("Radford et al. 2019 — Language Models are Unsupervised Multitask Learners", GPT2)
F_BERT = fonte("Devlin et al. 2018 — BERT: Pre-training of Deep Bidirectional Transformers", BERT)

ABERTURA = [
    desenhado([("text", .08, .28, .84, .25, "o que entra e o que sai\nde um language model?", {"size": 34, "bold": True, "align": "CENTER"}),
               ("text", .08, .58, .84, .12, "e o que muda quando a saída deixa de ser texto?", {"size": 20, "italic": True, "color": GRAY, "align": "CENTER"})],
              "Pergunta de abertura. Deixe a turma responder: a maioria diz 'entra texto, sai texto'. O bloco desmonta isso: sai uma "
              "distribuição de probabilidade, e o que muda de modelo pra modelo é sobre o quê. Guarde as respostas: voltamos a elas no fecho."),
    fallback("pergunta de abertura",
             "Pergunta: o que entra e o que sai de um language model? E quando a saída deixa de ser texto?\n"
             "Resposta que o bloco constrói: entram tokens, sai uma distribuição de probabilidade; muda sobre o quê.\n"
             "Layout: pergunta grande centralizada, subpergunta em itálico cinza, sem imagem."),
]

FRASE = ["o", "gato", "subiu", "no"]
ES = [
    {"layout": "Section header", "ph": {"TITLE": "todo transformer termina numa\ndistribuição de probabilidade.\no que muda é: sobre o quê?"},
     "notes": "Ideia central do bloco. Os próximos slides repetem o mesmo desenho (tokens → caixa → barras) e só a saída muda."},
    desenhado(titulo("gpt: o que entra", "decoder-only") + tokens(FRASE) + modelo("GPT", "decoder")
              + [("text", .66, .38, .2, .14, "?", {"size": 44, "color": MID})]
              + legenda("entra: os tokens até aqui, lidos só da esquerda pra direita.") + F_GPT,
              "Entra a frase cortada. O decoder só olha pra trás (máscara causal). Pergunte: qual a próxima palavra?"),
    desenhado(titulo("gpt: o que sai", "next-token prediction") + tokens(FRASE) + modelo("GPT", "decoder")
              + barras([("telhado", .62), ("muro", .21), ("sofá", .09), ("carro", .04)])
              + legenda("sai: uma probabilidade para cada palavra do vocabulário (dezenas de milhares).") + F_GPT,
              "A saída não é uma palavra: é uma barra para cada token do vocabulário (o do GPT-2 tem ~50 mil). Números ilustrativos. "
              "Temperatura e amostragem decidem qual barra vira texto: por isso a mesma pergunta dá respostas diferentes."),
    desenhado(titulo("gpt: e volta", "autoregressive") + tokens(FRASE + ["telhado"], dest=(4,)) + modelo("GPT", "decoder")
              + barras([(".", .48), ("e", .27), ("da", .14), ("quando", .06)])
              + legenda("↺ a palavra escolhida vira entrada. texto longo = essa volta, milhares de vezes.") + F_GPT,
              "O loop é o que faz o GPT 'escrever': uma passada inteira por token de saída. Os modelos de decisão, no fim do bloco, quebram esse loop."),
    desenhado(titulo("bert: o buraco", "encoder-only · masked language model") + tokens(["o", "gato", "[MASK]", "no", "telhado"], dest=(2,))
              + modelo("BERT", "encoder") + barras([("subiu", .71), ("dormiu", .12), ("pulou", .08), ("está", .05)])
              + legenda("entra a frase inteira com um buraco; o encoder olha pros dois lados.\nsai: probabilidade das palavras para o buraco.") + F_BERT,
              "Mesmo desenho, entrada diferente. O encoder é bidirecional: 'telhado', que vem depois, ajuda a adivinhar 'subiu'. É assim que o BERT é treinado."),
    desenhado(titulo("bert: a classe", "classification") + tokens(["[CLS]", "adorei", "o", "filme"], dest=(0,))
              + modelo("BERT", "encoder") + barras([("positivo", .94), ("negativo", .06)])
              + legenda("depois do treino, uma cabeça pequena lê o [CLS] e distribui sobre classes:\nsentimento, spam, tópico.") + F_BERT,
              "O uso prático do BERT: a saída troca o vocabulário por poucas classes. Não escreve: decide. Ancestral direto dos modelos de decisão."),
    desenhado(titulo("bart: lê e reescreve", "encoder-decoder · seq2seq") + tokens(["o", "gato", "subiu", "no", "telhado"])
              + [("box", .28, .36, .14, .24, "encoder", {"size": 15, "bold": True, "fill": WHITE, "outline": GRAY}),
                 ("box", .47, .36, .14, .24, "decoder", {"size": 15, "bold": True, "fill": WHITE, "outline": GRAY}),
                 ("line", .235, .48, .27, .48, {}), ("line", .425, .48, .465, .48, {}), ("line", .615, .48, .66, .48, {})]
              + tokens(["the", "cat", "climbed", "onto", "the roof"], x=.67, w=.15)
              + legenda("o encoder lê tudo; o decoder escreve uma sequência nova, token a token.\ntradução, resumo, reescrita.")
              + fonte("Lewis et al. 2019 — BART: Denoising Sequence-to-Sequence Pre-training", BART),
              "Os dois pedaços do transformer original: o encoder entende a frase inteira (como o BERT), o decoder escreve (como o GPT) olhando pro encoder."),
]
if SVG_URL:
    ES.append(desenhado([("img", SVG_URL, .03, .03, .94, .88)], "Versão (b), imagem única, para comparar com a versão (a) animada. Escolha uma depois da aula."))
ES.append(fallback("o que entra, o que sai",
    "Ideia central: todo transformer termina numa distribuição de probabilidade; o que muda é sobre o quê.\n"
    "GPT (decoder-only): entram os tokens até aqui; sai uma probabilidade por token do vocabulário; o escolhido volta pra entrada. " + GPT2 + "\n"
    "BERT (encoder-only): entra a frase com [MASK]; sai a distribuição para o buraco; uma cabeça no [CLS] distribui sobre classes. " + BERT + "\n"
    "BART (encoder-decoder): encoder lê tudo, decoder escreve uma sequência nova (tradução, resumo). " + BART + "\n"
    "Ilustrações para baixar: https://jalammar.github.io/illustrated-gpt2/ · https://jalammar.github.io/illustrated-bert/\n"
    "Layout: mesmo desenho em todos (tokens → caixa → barras), barra vencedora em azul; só a saída muda. Probabilidades ilustrativas."))

JEVLAYA = [
    desenhado(titulo("modelos de decisão", "system one models") + tokens(["estado do jogo", "cacto a 40 px", "velocidade 9", "pular · abaixar · nada"], w=.2)
              + modelo("Laya", "encoder\nbidirecional", x=.3, w=.22) + barras([("pular", .93), ("abaixar", .05), ("nada", .02)])
              + legenda("não escreve: devolve uma probabilidade por opção, numa passada só.\nparente direto do BERT com [CLS].")
              + fonte("mizorewww/laya-mlx — state + typed question → bidirectional encoder → decision heads → probabilities", LAYA),
              "Setembro de 2026: Jev (TypeSafe, 15/09) e Laya (Convai, porte local em MLX). É o BERT classificador levado ao limite: entra estado + opções, "
              "sai uma distribuição sobre as opções, sem gerar token. 'Sistema 1' rápido ao lado do GPT 'sistema 2'. Já é um agente decidindo: ponte pra agência."),
    desenhado(titulo("jev × laya", "nuvem × local")
              + [("text", .05, .3, .42, .1, "jev · TypeSafe · nuvem", {"size": 18, "bold": True}),
                 ("text", .05, .4, .42, .33, "70–500 ms por decisão\nUS$ 0,042 por milhão de tokens de entrada\nsaída: grátis", {"size": 16, "color": GRAY}),
                 ("text", .53, .3, .42, .1, "laya-mlx · local · Mac", {"size": 18, "bold": True}),
                 ("text", .53, .4, .42, .33, "13,4 ms (mediana, decisão curta)\n421M parâmetros · contexto de 512\nsem nuvem, sem gerar texto", {"size": 16, "color": GRAY})]
              + legenda("números dos próprios autores. o '50× mais rápido que o jev' é alegação de um dev, num demo de tetris.", y=.76)
              + fonte("TypeSafe (15/09/2026) · github.com/mizorewww/laya-mlx", JEV),
              "Números das fontes primárias (blog da TypeSafe, README do laya-mlx). O vídeo do Tetris e o '50×' são de um desenvolvedor, em tarefa escolhida: diga isso. "
              "Pergunta: se decidir custa 13 ms e quase nada, o que acontece quando pomos isso num robô ou num drone?"),
    fallback("modelos de decisão: jev e laya",
        "Jev (TypeSafe AI, fundada por Diogo Almeida, ex-OpenAI; lançado em 15/09/2026): primeiro 'System One model' público. Devolve valores tipados com "
        "probabilidade (sim/não, nota, escolha), não texto. Alegações: 70–500 ms; 40–200× mais rápido que modelos de fronteira nessas tarefas; "
        "US$0,042/milhão de tokens de entrada, saída grátis; treino RLCD. " + JEV + "\n"
        "Laya (Convai Innovations), porte laya-mlx: estado + pergunta tipada → encoder bidirecional → cabeças de decisão → probabilidades. "
        "421M parâmetros, contexto 512, 13,42 ms de mediana num M3 Max. " + LAYA + "\n"
        "Tetris/Snake (Laya ~43–50 ms × Jev ~316 ms; '50×'): alegação de desenvolvedor, via https://www.instagram.com/p/Ddl6O0jjTI3/ — não usar como fato.\n"
        "Imagens: capturas do README do laya-mlx e do blog da TypeSafe. Layout: mesmo desenho E/S; depois duas colunas nuvem × local."),
]

CLONES_510 = clones(("g39b93bc0e41_0_24", "E quando dois modelos conversam? Nature Biotechnology: pensar em dupla vai mais longe que em grupo. Ponte pra agência."),
                    ("g39bf4d154ea_0_416", ""), ("g39bf4d154ea_0_438", ""), ("g39bf4d154ea_0_444", ""), ("g39bf4d154ea_0_449", ""),
                    ("g39bf4d154ea_0_424", "BERT e GPT em loop: um entende, o outro escreve. A pergunta da sexta: e se forem muitos agentes?"))

CHIPS = [("Qwen3", "família"), ("30B", "30 bi de\nparâmetros"), ("A3B", "3 bi ativos\npor token (MoE)"),
         ("Instruct", "ajustado pra\nconversar"), ("2507", "versão\njul/2025"), ("GGUF", "formato pra\nrodar local"), ("Q4_K_M", "~4 bits\npor peso")]
ADAPTAR = [secao("adaptar\nadapt", "Como um modelo grande vira um modelo que roda e serve pra você: LoRA e o nome do modelo.")]
ADAPTAR += clones(("g39bf4d154ea_0_387", "LoRA: em vez de reescrever bilhões de pesos, treina duas matrizes pequenas ao lado. É o que torna o ajuste fino barato."))
ADAPTAR += [
    desenhado(titulo("ler o nome de um modelo", "model naming")
              + [e for i, (c, d) in enumerate(CHIPS) for e in (
                  ("box", .04 + i * .132, .38, .122, .12, c, {"size": 14, "bold": True, "fill": ACCENT if c == "A3B" else LIGHT,
                                                              "color": WHITE if c == "A3B" else "#212121"}),
                  ("text", .04 + i * .132, .52, .122, .16, d, {"size": 11, "color": GRAY, "align": "CENTER"}))]
              + legenda("A3B: dos 30 bi, só ~3 bi trabalham em cada token. roda com custo de modelo pequeno.", y=.74)
              + fonte("huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507", QWEN),
              "Um nome de modelo é uma ficha técnica. O destaque é o A3B: mixture of experts, 30,5 bi no total, 3,3 bi ativos por token. "
              "GGUF e Q4 dizem como ele cabe num computador comum. Pergunta: por que um 30B-A3B responde mais rápido que um 30B denso?"),
    fallback("adaptar: LoRA e nome de modelo",
        "LoRA (Hu et al. 2021, https://arxiv.org/abs/2106.09685): congela os pesos e treina matrizes de posto baixo ao lado.\n"
        "Nome peça por peça (Qwen3-30B-A3B-Instruct-2507, GGUF Q4_K_M): família Qwen3; 30B = ~30,5 bi de parâmetros; A3B = ~3,3 bi ativos por token "
        "(mixture of experts); Instruct = pós-treinado pra seguir instruções; 2507 = julho/2025; GGUF = formato do llama.cpp; Q4_K_M = ~4 bits por peso. " + QWEN + "\n"
        "Captura: carrossel Analytics Vidhya ([aula-nome-de-modelo]). Layout: o nome como fita de fichas com legenda embaixo; A3B em destaque."),
]


def fita(y, partes, resp):
    els, x = [], .05
    for p in partes:
        w = .085 if len(p) < 8 else .12
        els.append(("box", x, y, w, .08, p, {"size": 10, "fill": LIGHT}))
        x += w + .006
    return els + [("line", x + .005, y + .04, x + .04, y + .04, {}),
                  ("box", x + .045, y, .1, .08, resp, {"size": 10, "fill": ACCENT, "color": WHITE})]


P = ["sistema", "pergunta 1", "resposta 1", "pergunta 2", "resposta 2", "pergunta 3"]
MEMORIA = [
    desenhado(titulo("memória é contexto", "context window")
              + [e for k, (n, y) in enumerate(((2, .32), (4, .48), (6, .64)))
                 for e in [("text", .05, y - .05, .2, .05, f"chamada {k + 1}", {"size": 11, "color": GRAY})] + fita(y, P[:n], f"resposta {k + 1}")]
              + legenda("o modelo não lembra: o programa reenvia a conversa inteira a cada chamada.\ncache = releitura barata (~10% do preço), não memória.", y=.76)
              + fonte("Anthropic — prompt caching (leitura de cache a 0,1× do preço base)", CACHE),
              "A cada mensagem o programa (harness) manda de novo tudo que veio antes. A fita cresce, o custo cresce, a atenção se dilui (context rot). "
              "Cache só barateia reler o mesmo começo. Quem 'lembra' é o programa em volta, não o modelo."),
    fallback("memória é contexto",
        "O modelo não tem memória entre chamadas: o harness reenvia a conversa inteira. A janela de contexto é o limite dessa fita.\n"
        "Cache de prompt: leitura a 0,1× o preço base na Anthropic: " + CACHE + "\n"
        "Context rot (Chroma Research): desempenho cai com contexto longo, mesmo em tarefas simples: https://research.trychroma.com/context-rot\n"
        "Captura: reel kem_glitch ([memoria-e-contexto]) + os quatro caches do serving (core/refs/REFS.md). Layout: três fitas crescentes, resposta em azul."),
]

EMBEDDINGS = [
    desenhado(titulo("embeddings não anonimizam", "embedding inversion")
              + [("box", .04, .34, .22, .14, "“Maria Silva, 54,\ndiabetes tipo 2”", {"size": 12, "fill": LIGHT}),
                 ("line", .265, .41, .3, .41, {}),
                 ("box", .305, .34, .2, .14, "[0.12, −0.83,\n0.41, … ]", {"size": 12, "fill": WHITE, "outline": GRAY}),
                 ("line", .51, .41, .545, .41, {}),
                 ("box", .55, .34, .14, .14, "inversor", {"size": 13, "bold": True, "fill": WHITE, "outline": GRAY}),
                 ("line", .695, .41, .73, .41, {}),
                 ("box", .735, .34, .22, .14, "“Maria Silva, 54,\ndiabetes tipo 2”", {"size": 12, "fill": ACCENT, "color": WHITE}),
                 ("text", .05, .53, .25, .18, "92%", {"size": 54, "bold": True, "color": ACCENT}),
                 ("text", .3, .55, .62, .16, "dos textos de 32 tokens recuperados exatamente a partir do vetor.\ntambém extraiu nomes completos de notas clínicas.", {"size": 14, "color": GRAY})]
              + legenda("um banco vetorial (RAG) não é uma cópia anonimizada.", y=.76)
              + fonte("Morris, Kuleshov, Shmatikov, Rush (Cornell) — Text Embeddings Reveal (Almost) As Much As Text, EMNLP 2023", VEC2TEXT),
              "RAG guarda textos como vetores, e muita gente acha que isso protege os dados. O vec2text chuta um texto, embeda, compara com o alvo e corrige até bater: "
              "92% de acerto exato em 32 tokens. Limite honesto: cai em textos longos e exige consultar o mesmo modelo de embedding. 'Maria Silva' é ilustrativo."),
    fallback("embeddings não anonimizam",
        "Morris, Kuleshov, Shmatikov & Rush (Cornell), EMNLP 2023: " + VEC2TEXT + "\n"
        "vec2text: gera candidato, embeda, compara com o alvo, corrige, repete. 92% dos textos de 32 tokens recuperados exatamente; nomes completos extraídos de notas clínicas.\n"
        "Limites: textos longos derrubam a taxa; exige consultar o mesmo modelo de embedding.\n"
        "Captura: post 'The Artificial Intelligence' ([aula-embedding-nao-anonimiza]). Layout: pipeline texto → vetor → inversor → mesmo texto; 92% grande."),
]

FECHO = [
    vocabulario(["token", "encoder", "decoder", "[MASK] · [CLS]", "distribuição", "autorregressivo",
                 "system one", "LoRA", "MoE", "quantização", "contexto · cache", "embedding"]),
    verificacao(["GPT e BERT recebem tokens. o que muda na saída de cada um?",
                 "por que um Qwen3-30B-A3B responde mais rápido que um modelo denso de 30B?",
                 "guardar documentos como embeddings num RAG protege os dados? por quê?"],
                "Volte à pergunta de abertura: agora a resposta é 'uma distribuição; muda sobre o quê'."),
    fallback("vocabulário e verificação",
        "Respostas: (1) GPT distribui sobre o vocabulário na próxima posição e realimenta a escolha; BERT distribui sobre o vocabulário no [MASK] ou sobre "
        "classes a partir do [CLS]. (2) Mixture of experts: só ~3 bi dos 30 bi trabalham em cada token. (3) Não: vec2text recupera 92% de textos curtos a partir do vetor.\n"
        "Layout: vocabulário em grade 4×3 de fichas cinza; verificação com três perguntas grandes."),
]

INSERCOES = [
    ("g289ea4407ca_0_0", ABERTURA),
    ("g38d58f2db91_0_142", ES + JEVLAYA + CLONES_510),
    ("g38d58f2db91_1_22", ADAPTAR),
    ("g38d58f2db91_1_114", MEMORIA),
    ("g38d58f2db91_0_20", EMBEDDINGS),
    ("g39c33b80c0d_0_0", FECHO),
]
