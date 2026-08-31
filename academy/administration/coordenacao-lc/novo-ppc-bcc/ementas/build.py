"""Build every [MODELO-SIGAA] <nome>.docx into saida-docx/, from whichever
source shape each discipline actually has (new-filled / new-blank+BCC-fallback
/ old-schema-remapped). Writes a per-discipline audit record for gaps.md and
the final review table -- no Drive upload here.
"""
import json, pathlib
import classify, extract_old, extract_single, port

HERE = pathlib.Path(__file__).parent
FONTE = HERE / "fonte"
OUT = HERE / "saida-docx"
OUT.mkdir(exist_ok=True)
CONSOLIDADO_OBRIGATORIOS = FONTE / "PROGRAMA DOS COMPONENTES CURRICULARES OBRIGATÓRIOS.docx"

inv = json.load(open(HERE / "inventory.json", encoding="utf-8"))
objetivos_gerados = json.load(open(HERE / "objetivos_gerados.json", encoding="utf-8"))

audit = []


def carga_breakdown_raw(teorica_h, pratica_h, extensao="", ead=""):
    pratica_txt = f" {pratica_h}h" if pratica_h else ""
    return f" {teorica_h}h\nPrática:{pratica_txt}\nExtensão: {extensao}\nEaD: {ead}"


for item in inv:
    nome, periodo = item["nome"], item["periodo"]
    safe = f"{periodo}__{nome}".replace("/", "-")
    src = FONTE / f"{safe}.docx"
    kind = classify.classify(src)
    record = {"nome": nome, "periodo": periodo, "kind": kind}

    if kind == "new-filled":
        fields = extract_single.extract(src)
        fields["periodo"] = fields.get("periodo") or ("OPTATIVA" if periodo == "NOVA" else f"{periodo}º")
        record["source"] = "próprio doc (já preenchido) -- verbatim"
        record["objetivos_status"] = "verbatim (já presente na fonte)" if fields.get("objetivos") else "FALTA (fonte sem objetivos, não gerado)"

    elif kind == "new-blank":
        try:
            fields = port.extract(str(CONSOLIDADO_OBRIGATORIOS), nome)
            record["source"] = "fallback: PROGRAMA DOS COMPONENTES CURRICULARES OBRIGATÓRIOS.docx (BCC consolidado)"
        except SystemExit:
            record["source"] = "SEM FONTE -- doc próprio em branco, sem equivalente no consolidado BCC"
            record["status"] = "GAP -- precisa conteúdo do professor/Paulo, nada gerado"
            audit.append(record)
            continue
        gen = objetivos_gerados.get(nome, "")
        if not fields.get("objetivos") and gen:
            fields["objetivos"] = gen
            record["objetivos_status"] = f"GERADO (grounded em EMENTA/CONTEÚDO do consolidado BCC) -- {gen[:80]}..."
        elif fields.get("objetivos"):
            record["objetivos_status"] = "verbatim (já presente no consolidado)"
        else:
            record["objetivos_status"] = "FALTA (sem objetivos gerados)"

    elif kind == "old-schema":
        f = extract_old.extract(src)
        gen = objetivos_gerados.get(nome, "")
        periodo_val = "OPTATIVA" if periodo == "NOVA" else f"{periodo}º"
        fields = {
            "componente": f["componente"],
            "codigo": f["codigo"],
            "periodo": periodo_val,
            "carga": f"{f['carga_total_h']}h" if f["carga_total_h"] else "",
            "carga_breakdown_raw": carga_breakdown_raw(f["carga_teorica_h"], f["carga_pratica_h"]),
            "pre_requisito": f["pre_requisito"],
            "correquisito": f["correquisito"],
            "equivalencia": f["equivalencia"],
            "ementa": f["ementa"],
            "objetivos": gen,
            "conteudo": f["conteudo"],
            "bib_basica": f["bib_basica"],
            "bib_comp": f["bib_comp"],
        }
        record["source"] = "doc próprio (schema antigo 'PROGRAMA DA DISCIPLINA') -- remapeado"
        record["_carga_note"] = f["_carga_note"]
        record["_derived_conteudo"] = f["_derived_conteudo"]
        record["objetivos_status"] = f"GERADO (grounded na EMENTA própria) -- {gen[:80]}..." if gen else "FALTA (sem objetivos gerados)"

    else:
        record["source"] = f"UNKNOWN schema -- pulado"
        record["status"] = "GAP -- schema não reconhecido, revisar manualmente"
        audit.append(record)
        continue

    out_path = OUT / f"[MODELO-SIGAA] {nome}.docx"
    port.fill(fields, str(out_path))
    record["status"] = "OK"
    record["out"] = str(out_path.name)
    record["fields"] = fields
    audit.append(record)
    print("built:", out_path.name)

json.dump(audit, open(HERE / "audit.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n{sum(1 for r in audit if r['status']=='OK')} built, {sum(1 for r in audit if r['status'].startswith('GAP'))} gaps")
