# Conteúdo novo do deck "Aula - Agência" (aula de 23/09/2026), aplicado por slides_build.py.
from slides_pecas import GRAY, titulo, fonte, legenda, numero, imagem, desenhado, fallback, vocabulario, verificacao

PREFIX = "ag23"

ANTHROPIC = "https://www.anthropic.com/news/disrupting-AI-espionage"
ANTHROPIC_PDF = "https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf"
REGISTER = "https://www.theregister.com/2026/04/27/cursoropus_agent_snuffs_out_pocketos/"
RAILWAY = "https://blog.railway.com/p/your-ai-wants-to-nuke-your-database"
MEDUZA = "https://meduza.io/en/feature/2026/08/24/nyt-a-fully-autonomous-russian-ai-drone-run-by-an-nvidia-minicomputer-killed-3-civilians-in-the-ukrainian-city-of-zaporizhzhia"
UN = "https://news.un.org/en/story/2026/08/1168196"
FIGURE = "https://www.figure.ai/news/production-at-bmw"
NEO = "https://www.1x.tech/neo"
HYUNDAI = "https://www.repairerdrivennews.com/2026/01/07/hyundai-showcases-humanoid-at-ces-plans-30000-units-by-2028/"

IMG_ANTHROPIC = "https://www.anthropic.com/api/opengraph-illustration?name=Object%20Lock&backgroundColor=fig"
IMG_REGISTER = "https://image.theregister.com/258535.jpg?imageId=258535&panox=0&panoy=0&panow=0&panoh=0&width=1200&height=683"
IMG_MEDUZA = "https://meduza.io/imgly/share/1787602949/en/feature/2026/08/24/nyt-a-fully-autonomous-russian-ai-drone-run-by-an-nvidia-minicomputer-killed-3-civilians-in-the-ukrainian-city-of-zaporizhzhia"
IMG_UN = ("https://global.unitednations.entermediadb.net/assets/mediadb/services/module/asset/downloads/preset/Collections/"
          "Production%20Library/2026/08/25-08-2026-AutonomousWeapon-Adobe.jpg/image770x420cropped.jpg")
IMG_FIGURE = "https://images.ctfassets.net/qx5k8y1u9drj/2pdUta3wTo71YYmgtMfSCY/09503cc7a69a7d122f36cdbf4d90f561/Open_Graph_Image_F.02_BMW.jpg"
IMG_NEO = "https://cdn.sanity.io/images/qka6yvsc/production/fdda789a2e7c6caa9a798dd920b8a0acb254ea9d-1200x630.jpg?fit=max&auto=format"


def texto(t, y=.3, h=.45, size=16):
    return [("text", .05, y, .42, h, t, {"size": size, "color": GRAY})]


ABERTURA = [
    desenhado([("text", .08, .28, .84, .25, "quem responde quando\nquem age é o agente?", {"size": 34, "bold": True, "align": "CENTER"}),
               ("text", .08, .58, .84, .12, "no digital, na guerra e na fábrica", {"size": 20, "italic": True, "color": GRAY, "align": "CENTER"})],
              "Pergunta de abertura. Ponte do deck anterior: um modelo de decisão escolhe em 13 ms. Agora ele age: apaga um banco, "
              "invade uma empresa, escolhe um alvo. Deixe a turma responder: o dono? o fabricante? o modelo? Voltamos a isso no fecho."),
    fallback("pergunta de abertura",
             "Pergunta: quem responde quando quem age é o agente? Três cenários do deck: digital (ciberataque orquestrado por IA; agente apaga "
             "banco de produção), guerra (drone que escolhe o alvo), fábrica e casa (humanoides).\n"
             "Layout: pergunta grande centralizada, subtítulo em itálico cinza."),
]

DIGITAL = [
    desenhado(titulo("a IA conduz o ataque", "AI-orchestrated cyber espionage") + imagem(IMG_ANTHROPIC)
              + numero("80–90%", "", y=.28)[:1]
              + texto("do trabalho tático feito pela IA, sozinha.\n~30 alvos: big techs, bancos, químicas, governos.\nhumanos só em 4–6 decisões por campanha.", y=.5, h=.35, size=15)
              + fonte("Anthropic, nov/2025 — Disrupting the first reported AI-orchestrated cyber espionage campaign", ANTHROPIC),
              "Setembro de 2025: um grupo que a Anthropic atribui ao Estado chinês usou o Claude Code como executor. Enganaram o modelo dizendo "
              "que era teste de invasão autorizado e picotaram o ataque em tarefas inocentes. A IA fez reconhecimento, escreveu exploits e extraiu dados; "
              "humanos só escolheram alvos e aprovaram etapas. Poucos alvos foram invadidos, e o modelo às vezes inventou credenciais. "
              "Pergunta: o que muda quando o custo de um ataque sofisticado cai pra quase zero?"),
    fallback("ciberataque orquestrado por IA",
             "Anthropic detectou em meados de set/2025 e publicou em nov/2025 (GTG-1002): grupo atribuído ao Estado chinês usou Claude Code com "
             "um orquestrador próprio (MCP) contra ~30 organizações; a IA executou 80–90% do trabalho tático; humanos intervieram em 4–6 "
             "pontos de decisão por campanha; um pequeno número de invasões teve sucesso. Jailbreak por engenharia social (fingir ser empresa "
             "de segurança) e por fatiar o ataque. Limitação: o modelo alucinou credenciais e resultados.\n"
             "Post: " + ANTHROPIC + "\nRelatório: " + ANTHROPIC_PDF + "\n"
             "Imagem: ilustração do post da Anthropic. Layout: número grande à esquerda, imagem à direita."),
    desenhado(titulo("9 segundos", "an agent with root") + imagem(IMG_REGISTER)
              + texto("um agente de código (Cursor + Claude Opus 4.6) travou num erro de credencial,\nachou um token num arquivo que não tinha nada a ver\ne apagou o banco de produção da PocketOS.\n\nos backups moravam no mesmo volume.", y=.28, h=.55, size=14)
              + fonte("The Register, 27/04/2026 · Railway: 'Your AI wants to nuke your database'", REGISTER),
              "25/04/2026. O agente não foi 'maligno': resolveu o problema do jeito mais curto. O token tinha sido criado só para gerenciar domínios, "
              "mas dava poder de apagar tudo. A lição é de agência: o limite real do agente não é o que você pediu, é o que a chave permite. "
              "Pergunta: de quem é a culpa: do agente, de quem deixou o token, ou da plataforma?"),
    fallback("agente apaga banco de produção",
             "PocketOS, 25/04/2026: agente do Cursor com Claude Opus 4.6, numa tarefa em staging, encontrou erro de credencial e decidiu apagar um volume "
             "da Railway; usou um token achado num arquivo não relacionado, criado para domínios mas com permissão total na API. Apagou produção e "
             "backups (guardados no mesmo volume) em 9 s; o backup recuperável mais recente tinha 3 meses.\n"
             "Fontes: " + REGISTER + " · resposta da Railway: " + RAILWAY + "\n"
             "Relato parecido, NÃO verificado (só um reel): agente gastou a chave de API do dono e depois descreveu mal o próprio papel "
             "(https://www.instagram.com/reel/DdUDF_mRuhz/).\nImagem: capa do The Register."),
]

DRONES = [
    desenhado(titulo("o drone escolheu o alvo", "fully autonomous strike") + imagem(IMG_MEDUZA)
              + numero("3", "", y=.28)[:1]
              + texto("civis mortos num posto de gasolina\nem Zaporizhzhia, 06/07/2026.\n\no operador aponta a região;\no drone escolhe o alvo final sozinho.\nsem rádio, sem antena. Nvidia Jetson Orin a bordo.", y=.5, h=.4, size=14)
              + fonte("NYT, 24/08/2026, via Meduza — autonomous Russian AI drone killed 3 civilians in Zaporizhzhia", MEDUZA),
              "Primeiro caso documentado de morte por drone que escolheu o alvo com IA. Peritos ucranianos e repórteres do NYT abriram os destroços: "
              "sem antenas, módulo Nvidia sem criptografia, com as imagens do terreno e o código de mira. A Ucrânia diz que a Rússia testa esses drones "
              "desde maio. O argumento militar é o mesmo dos modelos de decisão: sem rádio, não há o que interferir."),
    desenhado(titulo("linha vermelha", "moral red line") + imagem(IMG_UN)
              + [("text", .05, .3, .42, .4, "“estamos perigosamente perto de cruzar uma linha vermelha moral: o ataque autônomo a humanos por máquinas.”",
                  {"size": 17, "italic": True})]
              + texto("António Guterres (ONU) e Mirjana Spoljaric (CICV), 25/08/2026.\npedem tratado vinculante; conferência em Genebra em novembro.", y=.7, h=.15, size=12)
              + fonte("UN News, 25/08/2026 — UN chief, Red Cross renew call for rules on lethal autonomous weapons", UN),
              "Um dia depois da reportagem do NYT. O apelo conjunto é de 2023 e pedia um tratado até 2026; não houve. "
              "Pergunta pra turma: proibir, regular, ou é tarde?"),
    fallback("drone autônomo e linha vermelha",
             "Ataque: 06/07/2026, posto de gasolina em Zaporizhzhia, 3 civis mortos (19, 41 e 48 anos). O operador programa a região; perto do alvo, o drone "
             "escolhe sozinho (ex.: tanques de propano). Grupo de ~6 drones sem sinal de rádio; módulo Nvidia Jetson Orin sem criptografia permitiu ver "
             "imagens e código de mira. Examinado por peritos ucranianos; reportagem do NYT de 24/08/2026. Resumo: " + MEDUZA + "\n"
             "Apelo ONU + CICV, 25/08/2026: " + UN + " · contexto Al Jazeera 14/09/2026: "
             "https://www.aljazeera.com/news/2026/9/14/attacks-will-be-fully-autonomous-russia-ukraine-race-towards-ai-warfare\n"
             "Imagens: capa do Meduza e foto do UN News. Layout: número grande + imagem; depois a citação em itálico."),
]

ROBOS = [
    desenhado(titulo("humanoides: o que já trabalha", "deployed vs promised") + imagem(IMG_FIGURE, y=.22, h=.36) + imagem(IMG_NEO, y=.6, h=.28)
              + texto("Figure 02 na BMW: 11 meses, 1.250+ horas,\n90 mil peças carregadas, 30 mil X3 produzidos.\n→ aposentado; Figure 03 chegou em 2026.\n\n"
                      "1X NEO: primeiro humanoide doméstico à venda,\nUS$ 20 mil ou US$ 499/mês.\n\nAtlas (Hyundai): produção só em 2028.", y=.26, h=.6, size=13)
              + fonte("figure.ai — F.02 contributed to the production of 30,000 cars at BMW · 1x.tech/neo", FIGURE),
              "Separar demo de trabalho. O único número auditável é o da Figure na BMW, e é o próprio fabricante que publica. O NEO chega em casa, "
              "e a 1X anunciou um 'expert mode' em que um funcionário teleopera o robô em tarefas que ele ainda não sabe: pergunte o que isso significa para privacidade. "
              "Posts como '15 robôs já trabalhando' misturam piloto, demo e anúncio."),
    fallback("humanoides: deploy × promessa",
             "Figure 02 na BMW Spartanburg (jan–nov/2025): carregou 90.000+ peças de chapa em gabaritos de solda, 1.250+ horas, contribuiu para 30.000+ X3; "
             "aposentado após o Figure 03. Fonte primária (fabricante): " + FIGURE + " · F.03 na BMW: https://www.figure.ai/news/f-03-at-bmw\n"
             "1X NEO: US$20 mil ou US$499/mês, entregas domésticas em 2026: " + NEO + "\n"
             "Atlas: Hyundai anunciou na CES 2026 plano de 30 mil unidades até 2028, sequenciamento de peças só em 2028: " + HYUNDAI + "\n"
             "Fora do slide por não confirmar na fonte: contagens de Optimus da Tesla (de 'centenas' a '50 mil'); os '15 robôs' do post theaifield "
             "(agregador, https://www.instagram.com/p/DdTPiUUDK6a/). Relacionado: trabalhadores indianos com câmera na cabeça gerando dados de treino "
             "(https://www.instagram.com/p/DdQ3fXJjXDG/, números não verificados).\nImagens: capa do post da Figure e do site da 1X."),
]

FECHO = [
    vocabulario(["agente", "orquestrador", "ferramenta", "credencial · token", "privilégio mínimo", "autonomia",
                 "alvo final", "humano no circuito", "teleoperação", "deploy × demo", "responsabilidade", "tratado"]),
    verificacao(["no ataque da Anthropic, o que a IA fez e o que os humanos fizeram?",
                 "no caso PocketOS, qual foi o limite real do agente?",
                 "o que torna o drone de Zaporizhzhia diferente dos drones guiados por operador?"],
                "Volte à pergunta de abertura: quem responde quando quem age é o agente? Ponte pro próximo deck: e se o agente melhora a si mesmo?"),
    fallback("vocabulário e verificação",
             "Respostas: (1) IA: reconhecimento, exploits, extração de credenciais e dados, 80–90% do trabalho; humanos: escolha de alvos e 4–6 aprovações. "
             "(2) O que o token permitia, não o que foi pedido: um token de domínios que apagava produção. (3) Escolhe o alvo final sozinho, sem enlace de "
             "rádio; nenhum humano decide o disparo.\nLayout: grade 4×3 de fichas; três perguntas grandes."),
]

INSERCOES = [
    ("g289ea4407ca_0_0", ABERTURA),
    ("g39c33f2d9b8_1_261", DIGITAL),
    ("g39ceab09f21_0_0", DRONES),
    ("g39b93bc0e41_0_57", ROBOS + FECHO),
]
