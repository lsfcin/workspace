"""Extract SIGAA fields from a standalone single-table new-schema doc (no
name-matching needed -- the file holds exactly one discipline)."""
import docx
from docx.oxml.ns import qn
from docx.table import Table
import port


def extract(path):
    d = docx.Document(path)
    tbls = d.element.body.findall(".//" + qn("w:tbl"))
    t = Table(tbls[0], d)
    fields, current = {}, None
    for row in t.rows:
        for cell in port.uniq_cells(row):
            text = cell.text
            key, rest = port.match_label(text)
            if key:
                if key == "componente" and "componente" in fields:
                    return fields
                current = key
                fields[key] = rest.lstrip("\n ")
            elif current in port.BLOCK:
                fields[current] = (fields.get(current, "") + "\n" + text).strip("\n")
    return fields


if __name__ == "__main__":
    import sys, json
    print(json.dumps(extract(sys.argv[1]), ensure_ascii=False, indent=2))
