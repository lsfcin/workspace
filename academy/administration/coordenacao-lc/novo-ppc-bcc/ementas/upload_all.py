"""Upload every built [MODELO-SIGAA] doc to the Drive subfolder matching its
source discipline's period (or Novas Disciplinas), converting to Google Doc."""
import json, pathlib, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[5] / "core/tools"))
import drive_core

HERE = pathlib.Path(__file__).parent
OUT = HERE / "saida-docx"

PERIOD_FOLDER = {
    "1": "1TvICk8Hxq4x4YwINRwb45NYdXvIHHOH6",
    "2": "1-2EryGwBtqoGWrQwQHhIlPeCFnv1z3I5",
    "3": "1wwGg6kJcsO9j4T73-rEfolM8iNBpmU8k",
    "4": "1JjGaIyGfIxbvkZQaClk8tSLgtDBxhZPA",
    "5": "1Ojt6BrfUT8sn5NAn--twSSx1oKinWMOv",
    "6": "19s6U_3kX8sUgpyYl4RsU4g3E7ZWEvXaA",
    "7": "1rYk5b3pH5mE0AuIBlQlolaJ5Jdwfk7sX",
    "8": "1R0BR7b61mkn8YGpQ03YFOUulbz3k_CVA",
    "9": "1yR6v-0N_xxaTOcnaoFntuoSl8vmT8GOW",
    "NOVA": "1yPgYMan_Z2jgD1FR5Ve8hw0sjdiZ0rNG",
}

audit = json.load(open(HERE / "audit.json", encoding="utf-8"))
svc = drive_core.get_service("ufrpe", write=True)

results = []
for rec in audit:
    if rec["status"] != "OK":
        continue
    parent = PERIOD_FOLDER[rec["periodo"]]
    path = OUT / rec["out"]
    name = f"[MODELO-SIGAA] {rec['nome']}"
    res = drive_core.upload_local(svc, path, parent, as_gdoc=True, name=name)
    print(f"uploaded: {name}  ->  {res.get('webViewLink','')}")
    results.append({"nome": rec["nome"], "periodo": rec["periodo"], "id": res["id"], "link": res.get("webViewLink", "")})

json.dump(results, open(HERE / "upload_results.json", "w", encoding="utf-8", newline='\n'), ensure_ascii=False, indent=2)
print(f"\n{len(results)} uploaded")
