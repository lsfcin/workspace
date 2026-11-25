# Usage: core/run tools/pdf/bench/relevance_sheet.py <out-dir> <profile-dir> — one HTML page of every figure in <out-dir>/signals.tsv: the crop, its label, what its twin said, and the verdict the profile's weights give it, the disagreements first
#
# How a person audits the relevance bench in minutes: thumbnails, not files. The page lands at
# <out-dir>/folha.html beside the crops it shows; nothing is published.
from __future__ import annotations

import csv
import html
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(_HERE.parent), str(_HERE.parents[1]), str(_HERE.parents[2] / 'hooks')]
import pdf_relevance  # noqa: E402

STYLE = ('body{font:13px sans-serif;margin:16px}.f{display:inline-block;width:230px;margin:6px;vertical-align:top;'
         'border:3px solid #ccc;padding:4px}.f img{max-width:220px;max-height:160px}.miss{border-color:#c00}'
         '.extra{border-color:#e90}small{color:#555}')


def main() -> int:
    out, prof = Path(sys.argv[1]), pdf_relevance.profile(Path(sys.argv[2]))
    labels = {(r[0], r[1]): r[2] for r in csv.reader((out / 'labels.tsv').open(encoding='utf-8'), delimiter='\t')
              if len(r) >= 3} if (out / 'labels.tsv').exists() else {}
    table = prof.table
    cards, rows = [], list(csv.DictReader((out / 'signals.tsv').open(encoding='utf-8'), delimiter='\t'))
    areas: dict[str, list[float]] = {}
    for r in rows:
        areas.setdefault(r['doc'], []).append(float(r['area']))
    for r in rows:   # the verdict without the known-decoration rule: those looks came from these very labels
        sig = {k: float(r[k]) for k in pdf_relevance.SIGNALS if k in r} | pdf_relevance.document(areas[r['doc']])
        action, why = pdf_relevance.judge(sig, table)
        label = labels.get((r['doc'], r['figure']), '?')
        kind = 'miss' if label == '1' and action != 'describe' else 'extra' if label == '0' and action == 'describe' else ''
        cards.append((not kind, r['doc'], f'<div class="f {kind}"><img src="img/{html.escape(r["doc"])}--{r["figure"]}.png">'
                     f'<br><b>{html.escape(r["doc"][:40])} {r["figure"]}</b><br>rótulo {label} · {action} ({why})'
                     f'<br><small>{html.escape(r["said"][:120])}</small></div>'))
    body = ''.join(card for *_, card in sorted(cards))
    page = (f'<!doctype html><meta charset="utf-8"><title>Figuras: rótulo e veredito</title><style>{STYLE}</style>'
            f'<p>Vermelho: rótulo 1 (relevante) que o índice não descreveria. Laranja: rótulo 0 que ele descreveria. '
            f'Para corrigir um rótulo, edite labels.tsv (doc, figura, 1|0).</p>{body}')
    (out / 'folha.html').write_text(page, encoding='utf-8', newline='\n')
    print(out / 'folha.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())
