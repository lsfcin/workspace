#!/usr/bin/env python3
"""Intercala slides novos num deck existente, ancorados no id do slide que os precede.

Um conteúdo é uma lista INSERCOES de (id_ancora, [slide, ...]). Cada slide é um dict:
  layout  nome de exibição do layout do deck ("Blank", "Section header", "Title and body", ...)
  ph      {"TITLE": texto, "BODY": texto} para os placeholders do layout
  els     formas desenhadas: ("text"|"box"|"img"|"line", ...) em frações do slide (0..1)
  notes   notas do apresentador
  skip    True no fallback: some no modo apresentação, fica visível na edição
  clone   (deck_json, slide_id) para reconstruir um slide de outro deck (a API não copia entre decks)

Duas passadas, porque o id da caixa de notas de um slide só existe depois que ele é criado:
  build   -> requests de criação (do fim para o começo, para os índices continuarem válidos)
  notes   -> requests de notas, lidos do deck já criado
"""
import json, sys

W, H = 9144000, 5143500
FONT = "Open Sans"
GRAY = "#595959"
LIGHT = "#EEEEEE"
MID = "#BDBDBD"
ACCENT = "#1A73E8"


def rgb(hexa):
    h = hexa.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


def frame(page, x, y, w, h):
    return {"pageObjectId": page,
            "size": {"width": {"magnitude": max(w * W, 1), "unit": "EMU"},
                     "height": {"magnitude": max(h * H, 1), "unit": "EMU"}},
            "transform": {"scaleX": 1, "scaleY": 1, "translateX": x * W, "translateY": y * H, "unit": "EMU"}}


def style_reqs(oid, st):
    """Estilo de texto: size, bold, italic, color, link, align, font, middle."""
    s, f = {"fontFamily": st.get("font", FONT)}, ["fontFamily"]
    if "size" in st:
        s["fontSize"] = {"magnitude": st["size"], "unit": "PT"}; f.append("fontSize")
    for k in ("bold", "italic"):
        if k in st:
            s[k] = st[k]; f.append(k)
    s["foregroundColor"] = {"opaqueColor": {"rgbColor": rgb(st.get("color", "#212121"))}}; f.append("foregroundColor")
    if "link" in st:
        s["link"] = {"url": st["link"]}; f.append("link")
    out = [{"updateTextStyle": {"objectId": oid, "textRange": {"type": "ALL"}, "style": s, "fields": ",".join(f)}},
           {"updateParagraphStyle": {"objectId": oid, "textRange": {"type": "ALL"},
                                     "style": {"alignment": st.get("align", "START")}, "fields": "alignment"}}]
    if st.get("middle"):
        out.append({"updateShapeProperties": {"objectId": oid, "shapeProperties": {"contentAlignment": "MIDDLE"},
                                              "fields": "contentAlignment"}})
    return out


def element(page, oid, el):
    kind = el[0]
    if kind in ("text", "box"):
        _, x, y, w, h, txt, st = el
        shape = st.get("shape", "TEXT_BOX" if kind == "text" else "ROUND_RECTANGLE")
        r = [{"createShape": {"objectId": oid, "shapeType": shape, "elementProperties": frame(page, x, y, w, h)}}]
        if kind == "box":
            props = {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": rgb(st.get("fill", LIGHT))}}}}
            fields = ["shapeBackgroundFill.solidFill.color"]
            if st.get("outline"):
                props["outline"] = {"outlineFill": {"solidFill": {"color": {"rgbColor": rgb(st["outline"])}}},
                                    "weight": {"magnitude": st.get("weight", 1.5), "unit": "PT"}}
                fields += ["outline.outlineFill.solidFill.color", "outline.weight"]
            else:
                props["outline"] = {"propertyState": "NOT_RENDERED"}; fields.append("outline.propertyState")
            r.append({"updateShapeProperties": {"objectId": oid, "shapeProperties": props, "fields": ",".join(fields)}})
            st = {"align": "CENTER", "middle": True, **st}
        if txt:
            r.append({"insertText": {"objectId": oid, "text": txt, "insertionIndex": 0}})
            r += style_reqs(oid, st)
        return r
    if kind == "img":
        _, url, x, y, w, h = el
        return [{"createImage": {"objectId": oid, "url": url, "elementProperties": frame(page, x, y, w, h)}}]
    if kind == "line":  # só horizontal ou vertical, da esquerda pra direita / de cima pra baixo
        _, x1, y1, x2, y2, st = el
        r = [{"createLine": {"objectId": oid, "lineCategory": "STRAIGHT",
                             "elementProperties": frame(page, x1, y1, x2 - x1, y2 - y1)}}]
        lp = {"lineFill": {"solidFill": {"color": {"rgbColor": rgb(st.get("color", GRAY))}}},
              "weight": {"magnitude": st.get("weight", 2), "unit": "PT"}}
        fields = "lineFill.solidFill.color,weight"
        if st.get("arrow", True):
            lp["endArrow"] = "FILL_ARROW"; fields += ",endArrow"
        if st.get("dash"):
            lp["dashStyle"] = "DASH"; fields += ",dashStyle"
        r.append({"updateLineProperties": {"objectId": oid, "lineProperties": lp, "fields": fields}})
        return r
    raise ValueError(kind)


def clone_elements(page, sid, src):
    """Reconstrói imagens, caixas de texto e setas de um slide de outro deck."""
    out = []
    for k, e in enumerate(src.get("pageElements", [])):
        oid = f"{sid}_c{k:02d}"
        props = {"pageObjectId": page, "size": e.get("size"),
                 "transform": {"scaleX": 1, "scaleY": 1, "translateX": 0, "translateY": 0,
                               **e.get("transform", {}), "unit": "EMU"}}
        if "image" in e:
            out.append({"createImage": {"objectId": oid, "url": e["image"]["contentUrl"], "elementProperties": props}})
            continue
        if "shape" not in e:
            continue
        sh = e["shape"]
        out.append({"createShape": {"objectId": oid, "shapeType": sh.get("shapeType", "TEXT_BOX"),
                                    "elementProperties": props}})
        fill = sh.get("shapeProperties", {}).get("shapeBackgroundFill", {}).get("solidFill")
        if fill and sh.get("shapeType") != "TEXT_BOX":
            out.append({"updateShapeProperties": {"objectId": oid, "shapeProperties": {
                "shapeBackgroundFill": {"solidFill": fill}}, "fields": "shapeBackgroundFill.solidFill"}})
        runs = [x for x in sh.get("text", {}).get("textElements", []) if "textRun" in x]
        text = "".join(x["textRun"]["content"] for x in runs).rstrip("\n")
        if not text:
            continue
        out.append({"insertText": {"objectId": oid, "text": text, "insertionIndex": 0}})
        pos = 0
        for x in runs:
            n = len(x["textRun"]["content"])
            end = min(pos + n, len(text))
            st = {k2: v for k2, v in x["textRun"].get("style", {}).items()
                  if k2 not in ("weightedFontFamily", "backgroundColor") and v != {}}
            if st and end > pos:
                out.append({"updateTextStyle": {"objectId": oid, "style": st, "fields": ",".join(st),
                                                "textRange": {"type": "FIXED_RANGE", "startIndex": pos,
                                                              "endIndex": end}}})
            pos += n
    return out


def placeholder_text(src, ptype):
    for e in src.get("pageElements", []):
        if e.get("shape", {}).get("placeholder", {}).get("type") == ptype:
            return "".join(x.get("textRun", {}).get("content", "")
                           for x in e["shape"].get("text", {}).get("textElements", [])).rstrip("\n")
    return None


def build(deck, insercoes, prefix):
    layouts = {l["layoutProperties"].get("displayName"): l["objectId"] for l in deck["layouts"]}
    order = [s["objectId"] for s in deck["slides"]]
    plan = sorted(((order.index(a), i, sl) for i, (a, sl) in enumerate(insercoes)), key=lambda t: (-t[0], -t[1]))
    reqs, made, n = [], [], 0
    for idx, _, slides in plan:
        for j, sp in enumerate(slides):
            sid = f"{prefix}{n:03d}"; n += 1
            ph, src = dict(sp.get("ph", {})), None
            if "clone" in sp:
                cdeck, cid = sp["clone"]
                src = next(s for s in cdeck["slides"] if s["objectId"] == cid)
                clay = {l["objectId"]: l["layoutProperties"].get("displayName") for l in cdeck["layouts"]}
                sp = {**sp, "layout": clay[src["slideProperties"]["layoutObjectId"]]}
                for t in ("TITLE", "BODY"):
                    txt = placeholder_text(src, t)
                    if txt:
                        ph[t] = txt
            maps = [{"layoutPlaceholder": {"type": t}, "objectId": f"{sid}_{t.lower()}"} for t in ph]
            reqs.append({"createSlide": {"objectId": sid, "insertionIndex": idx + 1 + j,
                                         "slideLayoutReference": {"layoutId": layouts[sp.get("layout", "Blank")]},
                                         "placeholderIdMappings": maps}})
            for t, txt in ph.items():
                reqs.append({"insertText": {"objectId": f"{sid}_{t.lower()}", "text": txt, "insertionIndex": 0}})
            if src is not None:
                reqs += clone_elements(sid, sid, {"pageElements": [
                    e for e in src.get("pageElements", []) if not e.get("shape", {}).get("placeholder")]})
            for k, el in enumerate(sp.get("els", [])):
                reqs += element(sid, f"{sid}_e{k:02d}", el)
            if sp.get("skip"):  # fallback: pulado, e letra menor para caber o argumento inteiro
                reqs.append({"updateSlideProperties": {"objectId": sid, "slideProperties": {"isSkipped": True},
                                                       "fields": "isSkipped"}})
                reqs += [{"updateTextStyle": {"objectId": f"{sid}_{t.lower()}", "textRange": {"type": "ALL"},
                                              "style": {"fontSize": {"magnitude": pt, "unit": "PT"}}, "fields": "fontSize"}}
                         for t, pt in (("TITLE", 20), ("BODY", 12)) if t in ph]
            made.append((sid, sp.get("notes", "")))
    return reqs, made


def notes(deck, made):
    by = {s["objectId"]: s for s in deck["slides"]}
    reqs = []
    for sid, txt in made:
        if txt and sid in by:
            nid = by[sid]["slideProperties"]["notesPage"]["notesProperties"]["speakerNotesObjectId"]
            reqs.append({"insertText": {"objectId": nid, "text": txt, "insertionIndex": 0}})
    return reqs


if __name__ == "__main__":
    import importlib
    mode, conteudo, deck_json, out = sys.argv[1:5]
    deck = json.load(open(deck_json, encoding="utf-8"))
    mod = importlib.import_module(conteudo)
    reqs, made = build(json.load(open(sys.argv[5], encoding="utf-8")) if mode == "notes" else deck, mod.INSERCOES, mod.PREFIX)
    if mode == "notes":
        reqs = notes(deck, made)
    json.dump(reqs, open(out, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(f"{mode}: {len(made)} slides · {len(reqs)} requests -> {out}")
