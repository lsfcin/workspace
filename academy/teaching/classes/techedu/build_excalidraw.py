#!/usr/bin/env python3
"""Gera o quadro da aula 02: um frame por equipe + um frame de exemplo preenchido.

Cada frame carrega o MODELO vazio ([QUEM] precisa [VERBO] porque [VIRADA]) e o
espaco do mapa de atores. O frame de exemplo fica na primeira posicao, ja
preenchido, para nao sobrar duvida do que e' "pronto".
"""
import json, random, sys

N_EQUIPES = 8
FW, FH = 1500, 1150          # tamanho do frame
GAP_X, GAP_Y = 260, 220      # respiro entre frames
COLS = 3

INK = "#1e1e1e"
LABEL = "#1971c2"
HINT = "#868e96"
FILLED = "#2f9e44"

_seed = random.Random(20260819)


def _base(x, y, w, h, frame_id=None):
    return {
        "id": None, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": INK, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": frame_id,
        "roundness": None, "seed": _seed.randint(1, 2**31), "version": 1,
        "versionNonce": _seed.randint(1, 2**31), "isDeleted": False,
        "boundElements": [], "updated": 1, "link": None, "locked": False,
    }


def frame(eid, x, y, name):
    e = _base(x, y, FW, FH)
    e.update({"id": eid, "type": "frame", "name": name, "strokeColor": "#bbb"})
    return e


def rect(eid, x, y, w, h, fid, stroke=INK, dashed=False):
    e = _base(x, y, w, h, fid)
    e.update({"id": eid, "type": "rectangle", "strokeColor": stroke,
              "roundness": {"type": 3},
              "strokeStyle": "dashed" if dashed else "solid"})
    return e


def ellipse(eid, x, y, w, h, fid, stroke=INK):
    e = _base(x, y, w, h, fid)
    e.update({"id": eid, "type": "ellipse", "strokeColor": stroke})
    return e


def text(eid, x, y, s, fid, size=20, color=INK, family=1, w=None):
    lines = s.split("\n")
    w = w or int(max(len(l) for l in lines) * size * 0.56)
    h = int(len(lines) * size * 1.25)
    e = _base(x, y, w, h, fid)
    e.update({"id": eid, "type": "text", "text": s, "originalText": s,
              "fontSize": size, "fontFamily": family, "textAlign": "left",
              "verticalAlign": "top", "containerId": None,
              "lineHeight": 1.25, "strokeColor": color, "autoResize": True})
    return e


def bloco(els, fid, tag, x, y, label, hint, box_h, filled=None):
    """Um slot do modelo: rotulo + dica + caixa (ou texto preenchido)."""
    els.append(text(f"{tag}-lab", x, y, label, fid, size=26, color=LABEL))
    els.append(text(f"{tag}-hint", x, y + 34, hint, fid, size=17, color=HINT))
    els.append(rect(f"{tag}-box", x, y + 64, FW - 80, box_h, fid,
                    stroke=FILLED if filled else INK, dashed=not filled))
    if filled:
        els.append(text(f"{tag}-fill", x + 24, y + 64 + 22, filled, fid,
                        size=24, color=FILLED))


def montar_frame(els, idx, x, y, name, dados=None):
    fid = f"f{idx}"
    els.append(frame(fid, x, y, name))
    px, py = x + 40, y + 40

    titulo = name if dados else "EQUIPE:                                    "
    els.append(text(f"{fid}-t", px, py, titulo, fid, size=34,
                    color=FILLED if dados else INK))

    if not dados:
        els.append(text(f"{fid}-n", px, py + 48,
                        "nomes:", fid, size=18, color=HINT))

    bloco(els, fid, f"{fid}-a", px, py + 100,
          "QUEM", "não 'estudante'. um traço que muda tudo.", 110,
          filled=dados[0] if dados else None)

    bloco(els, fid, f"{fid}-b", px, py + 300,
          "PRECISA", "verbo. o que a pessoa precisa FAZER ou SENTIR. nunca 'precisa de um app'.",
          110, filled=dados[1] if dados else None)

    bloco(els, fid, f"{fid}-c", px, py + 500,
          "PORQUE", "a virada. se o porque fosse óbvio, não era descoberta.", 150,
          filled=dados[2] if dados else None)

    # mapa de atores
    ay = py + 740
    els.append(text(f"{fid}-m", px, ay, "quem mais é afetado, e como?", fid,
                    size=26, color=LABEL))
    cx = x + FW // 2 - 110
    els.append(ellipse(f"{fid}-e", cx, ay + 60, 220, 120, fid,
                       stroke=FILLED if dados else INK))
    els.append(text(f"{fid}-ec", cx + 48, ay + 105,
                    dados[3] if dados else "a pessoa", fid, size=20,
                    color=FILLED if dados else INK))
    if dados:
        for i, (dx, dy, txt) in enumerate(dados[4]):
            els.append(text(f"{fid}-at{i}", x + dx, ay + dy, txt, fid,
                            size=18, color=FILLED))


EXEMPLO = (
    "aluno de computação que trabalha 40h\ne chega na aula às 19h20",
    "sentir na mão que a solução saiu dele",
    "porque cada entrega boa feita pela máquina vira mais uma prova,\n"
    "para ele mesmo, de que sozinho não teria conseguido",
    "o aluno",
    [(90, 60, "o professor\nnão sabe mais o que\nestá avaliando"),
     (1130, 60, "o colega de equipe\ncarrega sozinho\ne se cala"),
     (110, 250, "o chefe no estágio\ncontrata alguém que\ntrava sem a ferramenta"),
     (1120, 250, "a próxima turma\nherda o mesmo hábito\ncomo se fosse normal")],
)


def build():
    els = []
    montar_frame(els, 0, 0, 0, "EXEMPLO — preenchido", dados=EXEMPLO)
    for i in range(N_EQUIPES):
        col = (i + 1) % COLS
        row = (i + 1) // COLS
        montar_frame(els, i + 1, col * (FW + GAP_X), row * (FH + GAP_Y),
                     f"equipe {i + 1}")
    return {
        "type": "excalidraw", "version": 2,
        "source": "https://excalidraw.com",
        "elements": els,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "aula02.excalidraw"
    doc = build()
    with open(out, "w", encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False)
    print(f"{len(doc['elements'])} elementos · 1 exemplo + {N_EQUIPES} equipes -> {out}")
