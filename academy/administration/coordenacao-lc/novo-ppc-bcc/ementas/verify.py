"""Round-trip verification: re-read every built [MODELO-SIGAA] doc and diff its
fields against what build.py wrote, for every field EXCEPT objetivos/conteudo
(conteudo may be derived) and carga_breakdown_raw (reshaped by design).
"""
import json, pathlib
import extract_single

HERE = pathlib.Path(__file__).parent
OUT = HERE / "saida-docx"
audit = json.load(open(HERE / "audit.json", encoding="utf-8"))

CHECK_FIELDS = ["componente", "codigo", "periodo", "carga", "pre_requisito",
                "correquisito", "equivalencia", "ementa", "bib_basica", "bib_comp"]

mismatches = 0
for rec in audit:
    if rec["status"] != "OK":
        continue
    written = extract_single.extract(OUT / rec["out"])
    expected = rec["fields"]
    for f in CHECK_FIELDS:
        exp = (expected.get(f) or "").strip()
        got = (written.get(f) or "").strip()
        if exp != got:
            mismatches += 1
            print(f"MISMATCH [{rec['nome']}] field={f}")
            print("  expected:", repr(exp[:120]))
            print("  got     :", repr(got[:120]))

print(f"\n{len(audit)} records, {mismatches} field mismatches")
