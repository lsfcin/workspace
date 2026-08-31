"""Flag any token in a generated OBJETIVOS that doesn't appear in that same
discipline's own EMENTA+CONTEÚDO -- a crude but automatable proxy for 'nothing
new was invented'. Numbers/acronyms are the highest-risk case (dates, editions,
page counts); this scan targets those plus capitalized multi-word terms.
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).parent
audit = json.load(open(HERE / "audit.json", encoding="utf-8"))

NUM_RE = re.compile(r"\b\d+\b")
ACRONYM_RE = re.compile(r"\b[A-ZÀ-Ú]{2,}\b")

flags = []
for rec in audit:
    if rec["status"] != "OK":
        continue
    gen = rec.get("objetivos_status", "")
    if "GERADO" not in gen:
        continue
    f = rec["fields"]
    ground = f["ementa"] + " " + f["conteudo"]
    obj = f["objetivos"]
    ground_nums = set(NUM_RE.findall(ground))
    obj_nums = set(NUM_RE.findall(obj))
    new_nums = obj_nums - ground_nums
    ground_acr = set(ACRONYM_RE.findall(ground))
    obj_acr = set(ACRONYM_RE.findall(obj))
    new_acr = obj_acr - ground_acr
    if new_nums or new_acr:
        flags.append((rec["nome"], new_nums, new_acr))

if flags:
    print(f"{len(flags)} discipline(s) with terms in OBJETIVOS not found in EMENTA/CONTEÚDO:")
    for nome, nums, acr in flags:
        print(f"  {nome}: numbers={nums} acronyms={acr}")
else:
    print("Clean: every number/acronym in every generated OBJETIVOS also appears in that discipline's own EMENTA/CONTEÚDO.")
