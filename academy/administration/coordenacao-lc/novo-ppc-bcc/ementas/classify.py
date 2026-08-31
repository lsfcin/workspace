"""Classify each fonte/<periodo>__<nome>.docx as new-filled / new-blank / old-schema."""
import json, pathlib
import docx
from docx.oxml.ns import qn
from docx.table import Table

HERE = pathlib.Path(__file__).parent
inv = json.load(open(HERE / "inventory.json", encoding="utf-8"))
fonte = HERE / "fonte"

CONTENT_LABELS = ["EMENTA:", "CONTEÚDO PROGRAMÁTICO:", "BIBLIOGRAFIA BÁSICA:", "OBJETIVOS:"]


def uniq_cells(row):
    seen, out = set(), []
    for c in row.cells:
        if id(c._tc) in seen:
            continue
        seen.add(id(c._tc))
        out.append(c)
    return out


def classify(path):
    d = docx.Document(path)
    tbls = d.element.body.findall(".//" + qn("w:tbl"))
    all_cells = [cell.text for tb in tbls for row in Table(tb, d).rows for cell in uniq_cells(row)]
    all_text = "\n".join(all_cells)
    if "COMPONENTE CURRICULAR:" in all_text:
        filled = False
        for cell_text in all_cells:
            for label in CONTENT_LABELS:
                if cell_text.strip().startswith(label):
                    remainder = cell_text.strip()[len(label):].strip()
                    if len(remainder) > 15:
                        filled = True
        return "new-filled" if filled else "new-blank"
    if "PROGRAMA DA DISCIPLINA" in all_text or "IDENTIFICAÇÃO" in all_text:
        return "old-schema"
    return "unknown"


for item in inv:
    safe = f"{item['periodo']}__{item['nome']}".replace("/", "-")
    path = fonte / f"{safe}.docx"
    kind = classify(path) if path.exists() else "MISSING"
    print(f"{kind:12s} {item['periodo']:5s} {item['nome']}")
