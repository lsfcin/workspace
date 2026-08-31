"""Extract SIGAA-shaped fields from an old-schema ('PROGRAMA DA DISCIPLINA') source doc.

Flattens all table rows top-to-bottom and pattern-matches known section headers,
so it tolerates the small per-file layout drift seen across the corpus (DED/DC
courses vs the looser 'Bancos de Dados Não-Convencionais' proposal doc).
Returns a dict with the same keys port.py's new-schema extractor uses, plus
`_derived_conteudo` (True if CONTEÚDO had to be split out of EMENTA text) and
`_carga_note` (explanation when Teórica/Prática hours were computed from créditos).
"""
import re
import docx
from docx.oxml.ns import qn
from docx.table import Table


def uniq_cells(row):
    seen, out = set(), []
    for c in row.cells:
        if id(c._tc) in seen:
            continue
        seen.add(id(c._tc))
        out.append(c)
    return out


def flatten_rows(path):
    d = docx.Document(path)
    tbls = d.element.body.findall(".//" + qn("w:tbl"))
    rows = []
    for tb in tbls:
        for row in Table(tb, d).rows:
            rows.append([c.text for c in uniq_cells(row)])
    return rows


def _find(rows, *patterns):
    """Return (row_idx, cell_idx, match) for first row whose any cell matches any pattern."""
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            for pat in patterns:
                m = re.search(pat, cell)
                if m:
                    return ri, ci, m
    return None, None, None


def _section_text(rows, start_ri, stop_patterns):
    """Concatenate cell text of rows after start_ri until a row matches a stop header."""
    out = []
    for row in rows[start_ri + 1:]:
        joined = " ".join(row).strip()
        if any(re.match(p, joined.strip(), re.I) for p in stop_patterns):
            break
        if joined:
            out.append(joined)
    return "\n".join(out).strip()


HEADERS = [
    r"^PR[ÁA]TICA COMO COMPONENTE CURRICULAR",
    r"^CONTE[ÚU]DOS?( PROGRAM[ÁA]TICO)?$",
    r"^BIBLIOGRAFIA",
    r"^EMENTA$",
]


def extract(path):
    rows = flatten_rows(path)
    fields = {}

    ri, ci, m = _find(rows, r"(?:NOME|DISCIPLINA):\s*([^\n]*?)\s*(?:C[ÓO]DIGO:|$)")
    fields["componente"] = (m.group(1).strip() if m else "")

    ri2, ci2, m2 = _find(rows, r"C[ÓO]DIGO:\s*(\S*)")
    fields["codigo"] = (m2.group(1).strip() if m2 else "")

    ri3, ci3, m3 = _find(rows, r"CARGA HOR[ÁA]RIA TOTAL\s*:?\s*(\d+)")
    total_h = int(m3.group(1)) if m3 else None
    fields["carga_total_h"] = total_h

    m4 = None
    for row in rows:
        joined = " | ".join(row)
        m4 = re.search(r"TE[ÓO]RICAS?:\s*(\d+).*?PR[ÁA]TICAS?:\s*(\d+)", joined)
        if m4:
            break
    creditos_teo = int(m4.group(1)) if m4 else None
    creditos_pra = int(m4.group(2)) if m4 else None
    if total_h and creditos_teo is not None and (creditos_teo + (creditos_pra or 0)) > 0:
        h_per_credito = total_h / (creditos_teo + (creditos_pra or 0))
        fields["carga_teorica_h"] = round(creditos_teo * h_per_credito)
        fields["carga_pratica_h"] = round((creditos_pra or 0) * h_per_credito)
        fields["_carga_note"] = f"derivado de créditos ({creditos_teo}T+{creditos_pra or 0}P) x {h_per_credito:.1f}h/crédito = {total_h}h total"
    else:
        fields["carga_teorica_h"] = total_h
        fields["carga_pratica_h"] = 0
        fields["_carga_note"] = "sem quebra créditos na fonte; carga total alocada em Teórica"

    ri5, ci5, m5 = _find(rows, r"PR[ÉE]-REQUISITOS?:\s*(.*)")
    pre = (m5.group(1).strip() if m5 else "")
    fields["pre_requisito"] = "NÃO TEM" if pre.upper() in ("", "NENHUM", "NENHUMA") else pre

    ri6, ci6, m6 = _find(rows, r"CO-?REQUISITOS?:\s*(.*)")
    co = (m6.group(1).strip() if m6 else "")
    fields["correquisito"] = "NÃO TEM" if co.upper() in ("", "NENHUM", "NENHUMA") else co

    fields["equivalencia"] = "NÃO TEM"

    ri_em, _, _ = _find(rows, r"^EMENTA$")
    ementa = _section_text(rows, ri_em, HEADERS) if ri_em is not None else ""
    fields["ementa"] = ementa

    ri_ct, _, _ = _find(rows, r"^CONTE[ÚU]DOS?( PROGRAM[ÁA]TICO)?$")
    if ri_ct is not None:
        conteudo = _section_text(rows, ri_ct, HEADERS)
        fields["_derived_conteudo"] = False
    else:
        # split EMENTA into a numbered list, verbatim sentences, zero new content
        sentences = [s.strip() for s in re.split(r"(?<=[.;])\s+", ementa) if s.strip()]
        conteudo = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))
        fields["_derived_conteudo"] = True
    fields["conteudo"] = conteudo

    # bibliography: restrict search to rows AFTER the "BIBLIOGRAFIA" header row --
    # searching the whole doc risks false-matching "básicas"/"básico" inside the
    # EMENTA/CONTEÚDO prose, which always comes first.
    ri_bib, _, _ = _find(rows, r"^BIBLIOGRAFIA$")
    bib_rows = rows[ri_bib + 1:] if ri_bib is not None else rows
    full = "\n".join(" ".join(r) for r in bib_rows)
    # \b on both sides: guards against matching "básicas"/"complementares" etc.
    # embedded mid-sentence inside an actual bibliography entry (seen for real
    # in Estágio III's BÁSICA list, which cites "...complementares aos PCN...").
    mb = re.search(r"\bB[ÁA]SICA\b\s*:?\s*\n*(.*?)(?=\n?\s*\bCOMPLEMENTAR\b|\Z)", full, re.S | re.I)
    mc = re.search(r"\bCOMPLEMENTAR\b\s*:?\s*\n*(.*)\Z", full, re.S | re.I)
    fields["bib_basica"] = mb.group(1).strip() if mb else ""
    fields["bib_comp"] = mc.group(1).strip() if mc else ""

    fields["objetivos"] = ""  # always generated for old-schema sources
    return fields


if __name__ == "__main__":
    import sys, json
    print(json.dumps(extract(sys.argv[1]), ensure_ascii=False, indent=2))
