# Peças de desenho no estilo dos decks do Lucas (título minúsculo + termo em inglês, fonte no rodapé), para slides_build.py.
import json, os

GRAY, LIGHT, MID, ACCENT, WHITE = "#595959", "#EEEEEE", "#BDBDBD", "#1A73E8", "#FFFFFF"
OLD = os.environ.get("OLD_DECK_JSON")  # json do deck de onde se clonam slides


def titulo(pt, en=None):
    els = [("text", .05, .06, .75, .12, pt, {"size": 26, "bold": True})]
    if en:
        els.append(("text", .05, .15, .75, .08, en, {"size": 18, "italic": True, "color": GRAY}))
    return els


def fonte(txt, url):
    return [("text", .035, .915, .7, .05, txt, {"size": 8, "color": GRAY, "link": url})]


def legenda(txt, y=.8):
    return [("text", .05, y, .78, .1, txt, {"size": 15, "color": GRAY})]


def tokens(lista, x=.05, y0=.3, w=.17, h=.075, dest=()):
    return [("box", x, y0 + i * (h + .012), w, h, t,
             {"size": 13, "fill": ACCENT if i in dest else LIGHT, "color": WHITE if i in dest else "#212121"})
            for i, t in enumerate(lista)]


def modelo(nome, sub, x=.31, y=.33, w=.2, h=.3):
    return [("box", x, y, w, h, f"{nome}\n{sub}", {"size": 18, "bold": True, "fill": WHITE, "outline": GRAY}),
            ("line", .235, y + h / 2, x - .01, y + h / 2, {}),
            ("line", x + w + .01, y + h / 2, .585, y + h / 2, {})]


def barras(pares, x=.6, y0=.3, h=.07, dest=0):
    els = []
    for i, (rot, p) in enumerate(pares):
        y = y0 + i * (h + .015)
        els += [("text", x, y, .12, h, rot, {"size": 13, "align": "END", "middle": True}),
                ("box", x + .13, y + .012, max(.2 * p, .006), h - .024, "",
                 {"shape": "RECTANGLE", "fill": ACCENT if i == dest else MID}),
                ("text", x + .14 + .2 * p, y, .08, h, f"{round(p * 100)}%", {"size": 12, "color": GRAY, "middle": True})]
    return els


def numero(n, txt, y=.32):
    """Número grande em azul com a frase que o explica ao lado."""
    return [("text", .05, y, .34, .2, n, {"size": 54, "bold": True, "color": ACCENT}),
            ("text", .4, y + .03, .55, .2, txt, {"size": 16, "color": GRAY})]


def imagem(url, x=.5, y=.25, w=.45, h=.6):
    return [("img", url, x, y, w, h)]


def desenhado(els, notas):
    return {"layout": "Blank", "els": els, "notes": notas}


def fallback(titulo_, corpo, notas=""):
    return {"layout": "Title and body", "skip": True, "ph": {"TITLE": f"[fallback] {titulo_}", "BODY": corpo},
            "notes": notas or "Slide de apoio, pulado na apresentação: argumento completo, fontes e imagens."}


def secao(txt, notas=""):
    return {"layout": "Section header 1 1", "ph": {"TITLE": txt}, "notes": notas}


def clones(*pares):
    """(slide_id, notas) do deck OLD; vazio se OLD não foi passado."""
    if not OLD:
        return []
    deck = json.load(open(OLD, encoding="utf-8"))
    return [{"clone": (deck, sid), "notes": n} for sid, n in pares]


def vocabulario(termos, notas="Passe rápido: cada palavra numa frase, dita pela turma."):
    return desenhado(titulo("vocabulário", "vocabulary")
                     + [("box", .05 + (i % 4) * .225, .3 + (i // 4) * .15, .21, .11, t, {"size": 14, "fill": LIGHT})
                        for i, t in enumerate(termos)], notas)


def verificacao(perguntas, notas):
    return desenhado(titulo("verificação", "check")
                     + [("text", .05, .28, .88, .55, "\n\n".join(f"{i + 1}. {p}" for i, p in enumerate(perguntas)), {"size": 18})],
                     notas)
