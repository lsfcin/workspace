#!/usr/bin/env python3
"""Conteudo da aula 02 — o que entra no deck e onde.

Separado da mecanica (add_aula02.py) porque isto aqui e' texto de aula: muda a
cada revisao do Lucas, e nao deve arrastar o codigo junto.
"""

SECTION = "g19343927402_0_11"   # SECTION_HEADER        -> TITLE
SECTION1 = "g19343927402_0_18"  # SECTION_HEADER_1_1    -> TITLE
BODY = "g19343927402_0_22"      # TITLE_AND_BODY        -> TITLE, BODY
TWOCOL = "g19343927402_0_34"    # TITLE_AND_TWO_COLUMNS -> TITLE, BODY, BODY1
MAIN = "g19343927402_0_46"      # MAIN_POINT            -> TITLE
BIG = "g19343927402_0_58"       # BIG_NUMBER            -> TITLE, BODY

CEPR = ("Strömberg, Lei & Wu · The Generative AI Learning Penalty · CEPR DP21577 · 2026\n"
        "conference.nber.org/conf_papers/f240545.pdf")
OSU = ("Choudhuri, Sanchez, Burnett & Sarma · Why Johnny Can't Think · Oregon State · jan/2026\n"
       "arxiv.org/abs/2601.22430")
SCIADV = ("Doshi & Hauser · Generative AI enhances individual creativity but reduces the\n"
          "collective diversity of novel content · Science Advances · doi.org/10.1126/sciadv.adn5290")

# (indice 0-based no deck ORIGINAL = inserir antes deste slide, [(layout, {slot: texto})])
INSERCOES = [

 (2, [  # depois de "aula de hoje": a historia e o espelho
  (SECTION, {"TITLE": "antes: um problema meu"}),
  (MAIN, {"TITLE": "alunos de computação que entregam tudo com IA\n"
                   "precisam sentir na mão que a solução saiu deles\n\n"
                   "porque cada entrega boa feita pela máquina\n"
                   "vira mais uma prova, para eles mesmos,\n"
                   "de que sozinhos não teriam conseguido"}),
  (SECTION, {"TITLE": "e um dado sobre vocês"}),
  (BIG, {"TITLE": "+18%",
         "BODY": "nota do dever de casa, usando IA\ne o tempo de fazer caiu 30%\n\n"
                 "26.811 alunos · acompanhados por 30 meses\n\n" + CEPR}),
  (BIG, {"TITLE": "−20%",
         "BODY": "os mesmos alunos, na prova de livro fechado, seis meses depois\n\n"
                 "no vestibular: −18% a −24%\n\n" + CEPR}),
  (MAIN, {"TITLE": "os melhores alunos\nforam os que mais perderam"}),
  (BODY, {"TITLE": "e quem é o mais exposto",
          "BODY": "299 alunos de STEM, 5 universidades\n\n"
                  "quem confia e usa IA por rotina: menos reflexão, menos vontade de "
                  "entender, menos pensamento crítico\n\n"
                  "quem tem mais tecnofilia, mais tolerância a risco e mais autoeficácia "
                  "com computador é MAIS vulnerável\n\n"
                  "experiência prévia não protege\n\n" + OSU}),
  (MAIN, {"TITLE": "o estrago leva dois anos pra aparecer.\n"
                   "é por isso que ninguém corrige a rota."}),
  (BODY, {"TITLE": "a saída está no mesmo estudo",
          "BODY": "quem usou IA mantendo o esforço teve perda mínima\n\n"
                  "o problema nunca foi a ferramenta\n"
                  "o problema é terceirizar justo a parte que constrói você\n\n"
                  "nesta disciplina vocês vão usar IA o semestre inteiro\n"
                  "e eu vou pedir que vocês façam a parte difícil"}),
 ]),

 (6, [  # depois do carrinho da IDEO: por que DT agora
  (SECTION, {"TITLE": "por que não\ncomeçar codando?"}),
  (BODY, {"TITLE": "o que a IA faz com as ideias",
          "BODY": "experimento com escritores: metade recebeu ideias de um modelo de linguagem\n\n"
                  "cada história ficou mais criativa, melhor escrita e mais gostosa de ler — "
                  "principalmente para quem era menos criativo\n\n"
                  "e todas ficaram mais parecidas umas com as outras\n\n" + SCIADV}),
  (MAIN, {"TITLE": "se cada equipe pedir o problema pro Gemini,\nsaem oito projetos iguais."}),
  (BODY, {"TITLE": "por isso o primeiro diamante é de vocês",
          "BODY": "diamante 1 — abrir o problema, e só depois fechar num problema só\n"
                  "diamante 2 — abrir soluções, e só depois fechar numa solução só\n\n"
                  "o segundo diamante vocês podem acelerar com IA à vontade\n"
                  "o primeiro decide se o projeto é de vocês ou de todo mundo\n\n"
                  "hoje a gente faz só o lado esquerdo do primeiro diamante"}),
 ]),

 (22, [  # depois do exemplo da Larissa: o teste
  (TWOCOL, {"TITLE": "o teste do porque",
            "BODY": "não serve\n\n“uma adolescente precisa de comida mais nutritiva "
                    "porque vitaminas são vitais à saúde”\n\n"
                    "isso é um fato. não dá vontade de construir nada.",
            "BODY1": "serve\n\n“uma adolescente com uma perspectiva sombria precisa se "
                     "sentir socialmente aceita ao comer comida saudável, porque no bairro "
                     "dela um risco social é mais perigoso que um risco de saúde”\n\n"
                     "segura a tensão. já dá ideia."}),
  (MAIN, {"TITLE": "se o porque fosse óbvio,\nnão era descoberta."}),
 ]),

 (44, [  # depois de "outros campos": o eixo novo
  (SECTION, {"TITLE": "e um eixo que não estava\naqui no ano passado"}),
  (BODY, {"TITLE": "educação sob IA",
          "BODY": "a crise da verdade — o aluno não tem como saber se o que leu aconteceu\n"
                  "a crise do raciocínio crítico — os dados do começo da aula\n"
                  "a avaliação virou teatro — a prova mede o quê, agora?\n"
                  "autoria — o professor não tem instrumento para saber quem escreveu\n"
                  "o professor sozinho — formado para um mundo que acabou\n"
                  "quem não tem computador — a distância aumentou, não diminuiu"}),
  (BODY, {"TITLE": "para cavar nesse eixo",
          "BODY": "penalidade de aprendizagem, 26.811 alunos · CEPR DP21577\n"
                  "conference.nber.org/conf_papers/f240545.pdf\n\n"
                  "dívida cognitiva em alunos de STEM · Oregon State\n"
                  "arxiv.org/abs/2601.22430\n\n"
                  "criatividade individual sobe, diversidade coletiva cai · Science Advances\n"
                  "doi.org/10.1126/sciadv.adn5290\n\n"
                  "autoridade epistêmica e IA generativa · Frontiers in Education 2025\n"
                  "doi.org/10.3389/feduc.2025.1647687"}),
 ]),

 (47, [  # depois do roteiro: os quatro tempos
  (BODY, {"TITLE": "os 40 minutos, partidos",
          "BODY": "grupos de 3 a 4\n\n"
                  "10 min — cada um conta a história de UMA pessoa real que conhece, e a "
                  "dor dela. os outros anotam\n"
                  "15 min — escolham uma. preencham o modelo\n"
                  "10 min — mapa de atores: quem mais é afetado, e como\n"
                  "5 min — reescrevam o porque. na primeira versão ele quase sempre está óbvio\n\n"
                  "no fim: 30 segundos por equipe, lendo a frase em voz alta"}),
 ]),

 (49, [  # depois do link do miro: o quadro de hoje
  (BODY, {"TITLE": "o quadro de hoje",
          "BODY": "um frame por equipe, mais um frame de EXEMPLO já preenchido\n\n"
                  "cada frame tem os três campos do modelo e o mapa de atores\n\n"
                  "link: [EXCALIDRAW]"}),
 ]),
]

# (id do elemento de texto num slide existente, texto novo)
REFINOS = [
 ("g289d88ffaf1_0_8",  # slide 21 — o MODELO
  "[QUEM] precisa [VERBO] porque [VIRADA]\n\n"
  "QUEM — não “estudante”. um traço que muda tudo\n"
  "PRECISA — verbo. o que a pessoa precisa FAZER ou SENTIR. nunca “precisa de um app”\n"
  "PORQUE — a virada. o que vocês descobriram e ninguém esperava"),

 ("g289d88ffaf1_0_146",  # slide 22 — a Larissa, no formato novo
  "Larissa, 15 anos, estuda pelo celular porque é o único aparelho da casa,\n\n"
  "precisa conseguir voltar ao ponto onde parou depois de cada interrupção,\n\n"
  "porque na casa dela o problema não é falta de foco —\n"
  "é que ninguém ali reconhece estudar como uma coisa\n"
  "que exige não ser interrompida."),
]
