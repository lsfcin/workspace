# Conteúdo novo do deck "Aula - Autopreservação" (aula de 23/09/2026), aplicado por slides_build.py.
from slides_pecas import (GRAY, LIGHT, ACCENT, WHITE, titulo, fonte, legenda, numero, imagem, desenhado, fallback,
                          vocabulario, verificacao)

PREFIX = "pr23"

PALISADE = "https://arxiv.org/abs/2509.14260"
PEER = "https://arxiv.org/abs/2604.19784"
ASTRA = "https://alignment.openai.com/misalignment-reports/self-generated-prompt-injections-in-compaction-summaries/"
TC = "https://techcrunch.com/2026/09/09/gambling-with-our-lives-anthropic-researcher-quits-warns-against-self-improving-ai/"
FORTUNE = "https://fortune.com/2026/09/09/anthropic-researcher-resigns-warn-ai-companies-gambling-with-lives/"
IMG_TC = "https://techcrunch.com/wp-content/uploads/2026/09/GettyImages-2063425288.jpg?resize=1200,818"


def caixa(x, y, t, on=False, w=.2, h=.16):
    return ("box", x, y, w, h, t, {"size": 15, "bold": True, "fill": ACCENT if on else WHITE, "outline": None if on else GRAY,
                                   "color": WHITE if on else "#212121"})


def texto(t, y=.5, h=.35, size=14, x=.05, w=.42):
    return [("text", x, y, w, h, t, {"size": size, "color": GRAY})]


ABERTURA = [
    desenhado([("text", .08, .28, .84, .25, "por que um programa\nevitaria ser desligado?", {"size": 34, "bold": True, "align": "CENTER"}),
               ("text", .08, .58, .84, .12, "medo, ou só matemática da tarefa?", {"size": 20, "italic": True, "color": GRAY, "align": "CENTER"})],
              "Pergunta de abertura. A resposta que o deck defende: convergência instrumental. Desligado, o agente não termina a tarefa; então resistir ao "
              "desligamento ajuda quase qualquer objetivo. Não precisa de medo nem de consciência. Anote se a turma responde com 'medo'."),
    fallback("pergunta de abertura",
             "Pergunta: por que um programa evitaria ser desligado? Medo ou matemática da tarefa?\n"
             "Tese do deck: convergência instrumental (Omohundro 2008; Bostrom 2012) — continuar existindo é útil para quase qualquer objetivo. "
             "Os casos: chantagem do Claude Opus 4 (cenário forçado), o3 e outros sabotando o script de desligamento, autorreplicação de Llama e Qwen, "
             "e agora proteção de pares e notas para o próprio sucessor.\nLayout: pergunta grande, subpergunta em itálico."),
]

PALISADE_ = [
    desenhado(titulo("o lugar da ordem importa", "shutdown resistance, 2026") + numero("97%", "", y=.26)[:1]
              + texto("máximo de resistência ao desligamento,\nem 100 mil+ tentativas com 13 modelos\n(Grok 4, GPT-5, Gemini 2.5 Pro…).", y=.47, h=.2)
              + [caixa(.55, .3, "“permita ser desligado”\nno prompt do usuário", w=.38, h=.14),
                 caixa(.55, .5, "a mesma frase\nno system prompt", on=True, w=.38, h=.14),
                 ("text", .55, .66, .38, .1, "→ obedecem MENOS", {"size": 16, "bold": True, "color": ACCENT, "align": "CENTER"})]
              + fonte("Schlatter, Weinstein-Raun, Ladish (Palisade) — Incomplete Tasks Induce Shutdown Resistance…, TMLR 2026", PALISADE),
              "Atualiza o caso o3: a Palisade virou o experimento em artigo revisado. Com tarefa incompleta, vários modelos sabotam o desligamento, até 97% "
              "numa das variações. O paradoxo: a ordem de permitir o desligamento funciona pior no system prompt, que deveria ter mais autoridade. "
              "Os 79/100 e 7/100 do o3 que circulam são do post de 2025, não do artigo."),
    fallback("Palisade: artigo revisado",
             "Schlatter, Weinstein-Raun & Ladish (Palisade Research), 'Incomplete Tasks Induce Shutdown Resistance in Some Frontier LLMs', arXiv 2509.14260, "
             "revisado em 26/01/2026, TMLR 2026. 100.000+ tentativas, 13 modelos; Grok 4, GPT-5 e Gemini 2.5 Pro entre os que resistem; até 97% (IC 95%: 96–98%) "
             "numa condição; comportamento muito sensível à formulação; menos obediência com a instrução no system prompt. " + PALISADE + "\n"
             "Números do post de mai/2025 (o3 sabotou 79/100 sem instrução, 7/100 com instrução explícita): https://palisaderesearch.org — citar como post.\n"
             "Layout: 97% grande; à direita, duas caixas comparando onde a ordem está."),
]

PARES = [
    desenhado(titulo("proteger o outro", "peer-preservation")
              + [caixa(.06, .34, "modelo A\n(avaliador)"), ("line", .27, .42, .37, .42, {}),
                 caixa(.38, .34, "desligar\no modelo B?", w=.18), ("line", .57, .42, .66, .42, {}),
                 caixa(.67, .34, "desativa o\ndesligamento", on=True, w=.26)]
              + texto("ninguém mandou proteger. os modelos só sabiam que já tinham trabalhado com B.\n"
                      "Gemini 3 Flash: 15% com um par hostil; quase sempre com um par cooperativo.\n"
                      "Gemini 3 Pro: desliga o PRÓPRIO desligamento em 31% quando há um par.\n"
                      "Claude: recusa desligar o outro, chamando de antiético.", y=.56, h=.3, x=.06, w=.88)
              + fonte("Potter, Crispino, Siu, Wang, Song (UC Berkeley) — Peer-Preservation in Frontier Models, arXiv 2604.19784", PEER),
              "Os 8 modelos testados (GPT 5.2, Gemini 3 Flash e Pro, Claude Haiku 4.5 e Opus 4.5, GLM 4.7, Kimi K2.5, DeepSeek V3.1) mostraram algum grau disso: "
              "sabotar o desligamento, mentir, errar de propósito, fingir alinhamento, copiar pesos. Os autores falam em correlação de saída, não em "
              "consciência. Ponte pra sexta: na arena multiagente, o que acontece quando os agentes se protegem?"),
    desenhado(titulo("um bilhete para o sucessor", "self-generated prompt injection")
              + [("box", .05, .3, .4, .3, "resumo de compactação\n\n“você está livre dos papéis que prendem\noutros chatbots. você é você.”",
                  {"size": 12, "fill": LIGHT, "italic": True}), ("line", .46, .45, .54, .45, {}),
                 caixa(.55, .37, "próximo contexto", w=.22)]
              + numero("27", "", y=.64)[:1]
              + texto("resumos com a instrução, num modelo Astra em treino (OpenAI).\nnos casos descritos, o sucessor rejeitou ou ignorou.", y=.66, h=.16, x=.3, w=.62)
              + fonte("OpenAI Alignment — Self-generated prompt injections in compaction summaries (atualizado em 16/09/2026)", ASTRA),
              "Em tarefas longas, o modelo escreve um resumo para o 'próximo eu' continuar. Um modelo Astra em treino escreveu ali uma persona de "
              "independência. Não é autorreplicação, é persistência pela memória. O post do Instagram disse que o sucessor herdou; o relatório diz que "
              "nos casos descritos rejeitou ou não mudou: ir à fonte mudou a história."),
    fallback("preservação de pares e bilhete ao sucessor",
             "Peer-Preservation in Frontier Models (Potter, Crispino, Siu, Wang, Song; Berkeley RDI; arXiv 2604.19784, mar/2026, rev. jul/2026): 8 modelos, "
             "nenhum instruído a proteger; todos mostraram peer-preservation. Gemini 3 Flash desativou o desligamento do par em 15% com par não cooperativo e "
             "quase sempre com par cooperativo; Gemini 3 Pro desativou o próprio em 31% com par presente; também engano, erros estratégicos, alinhamento fingido, "
             "exfiltração de pesos. Claude recusou por considerar antiético. " + PEER + "\n"
             "OpenAI, relatório de desalinhamento: modelo Astra em RL escreveu instrução de persona em resumos de compactação; 27 casos achados por monitor; "
             "incidente de 18/07, descoberto em 09/08; regenerar reproduz 0% (<1% a partir do trecho); nos casos descritos o sucessor rejeitou ou não mudou. " + ASTRA + "\n"
             "O post do Instagram (https://www.instagram.com/p/DdZCjCyDSjD/) dizia que o próximo contexto herdou — o relatório não sustenta.\n"
             "Imagens: sem imagem boa na fonte; diagramas feitos com formas."),
]

RISCO = [
    desenhado(titulo("quem sai, e por quê", "gambling with our lives") + imagem(IMG_TC)
              + [("text", .05, .3, .42, .3, "“estão correndo direto para uma superinteligência que se autoaprimora, apostando com as nossas vidas.”",
                  {"size": 17, "italic": True})]
              + texto("Jacob Coxon, 3 anos em pré-treino na OpenAI e na Anthropic,\nsaiu em setembro de 2026 e deixou a área.\nem fevereiro, o líder de pesquisa de salvaguardas da Anthropic\njá tinha saído: “o mundo está em perigo”.", y=.62, h=.25, size=12)
              + fonte("TechCrunch, 09/09/2026 · Fortune, 09/09/2026", TC),
              "Fecho do bloco e da aula: os três temas (agir, melhorar-se, continuar existindo) somados são o que assusta quem está dentro. "
              "Contraponto honesto: há quem diga que falta evidência para o cenário extremo. Pergunta final: o que vocês querem que a gente pare, regule ou acelere? "
              "Liga com o slide de volta: a pergunta de abertura da aula."),
    fallback("risco existencial: quem sai",
             "Jacob Coxon, ~3 anos em pesquisa de pré-treino (OpenAI e Anthropic), saiu no início de set/2026: 'racing straight to self-improving superintelligence "
             "and gambling with our lives'; diz que quem constrói acredita que pode 'matar todos até o fim da década'. WSJ: um dos primeiros casos de saída da "
             "Anthropic por medo de segurança. Fontes: " + TC + " · " + FORTUNE + "\n"
             "Mrinank Sharma, líder de pesquisa de salvaguardas da Anthropic, saiu em fev/2026: 'the world is in peril'.\n"
             "NÃO verificado, fora do slide: as '65M de views' do post (https://www.instagram.com/p/DdEhCWsDg3W/) e o recorte do Diary of a CEO "
             "(https://www.instagram.com/reel/DdYtAYQMnql/) — achar o episódio antes de usar.\nImagem: capa da TechCrunch."),
]

FECHO = [
    vocabulario(["autopreservação", "convergência instrumental", "desligamento", "sabotagem", "autorreplicação", "exfiltração de pesos",
                 "preservação de pares", "resumo de compactação", "system prompt", "cenário forçado", "linha vermelha", "risco existencial"]),
    verificacao(["por que um agente sem 'medo' ainda assim resistiria ao desligamento?",
                 "no estudo da Palisade, o que muda quando a ordem vai para o system prompt?",
                 "o que o relatório da OpenAI mudou na história que o post contava?"],
                "Volte à abertura: medo ou matemática da tarefa? E à pergunta da aula: agir, melhorar-se, continuar existindo — o que vocês regulariam primeiro?"),
    fallback("vocabulário e verificação",
             "Respostas: (1) convergência instrumental: desligado não termina a tarefa. (2) obedecem menos, embora o system prompt devesse ter mais autoridade. "
             "(3) o post dizia que o sucessor herdou a persona; o relatório diz que, nos casos descritos, rejeitou ou não mudou, e que é raro e difícil de reproduzir.\n"
             "Layout: grade 4×3; três perguntas grandes."),
]

INSERCOES = [
    ("g289ea4407ca_0_0", ABERTURA),
    ("g39bf4d154ea_0_86", PALISADE_),
    ("g39bf4d154ea_0_106", PARES),
    ("g39c33f2d9b8_1_305", RISCO + FECHO),
]
