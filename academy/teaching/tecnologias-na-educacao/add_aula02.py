#!/usr/bin/env python3
"""Aula 02: intercala slides novos no deck existente e refina dois slides.

Nada e' deletado: os 56 slides originais mantem a ordem original e os novos
entram entre eles. As insercoes sao emitidas do fim para o comeco, para que os
indices calculados sobre o deck original continuem validos durante o batch.

Conteudo (o que entra e onde): aula02_conteudo.py
"""
import json, sys
from aula02_conteudo import INSERCOES, REFINOS


def build():
    reqs, n = [], 0
    for idx, slides in sorted(INSERCOES, key=lambda x: -x[0]):
        for j, (layout, texts) in enumerate(slides):
            sid = f"add{n:02d}"
            n += 1
            mappings = []
            for key in texts:
                ph = {"type": "BODY" if key.startswith("BODY") else key}
                if key == "BODY1":
                    ph["index"] = 1
                mappings.append({"layoutPlaceholder": ph,
                                 "objectId": f"{sid}_{key.lower()}"})
            reqs.append({"createSlide": {
                "objectId": sid,
                "insertionIndex": idx + j,
                "slideLayoutReference": {"layoutId": layout},
                "placeholderIdMappings": mappings,
            }})
            for key, txt in texts.items():
                reqs.append({"insertText": {"objectId": f"{sid}_{key.lower()}",
                                            "text": txt, "insertionIndex": 0}})

    for oid, txt in REFINOS:
        reqs.append({"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}})
        reqs.append({"insertText": {"objectId": oid, "text": txt, "insertionIndex": 0}})
    return reqs, n


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "add.json"
    reqs, n = build()
    json.dump(reqs, open(out, "w", encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print(f"{n} slides intercalados · {len(REFINOS)} refinados · "
          f"{len(reqs)} requests -> {out}")
