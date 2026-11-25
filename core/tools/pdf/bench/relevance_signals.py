# Usage: core/run tools/pdf/bench/relevance_signals.py <listing> <out-dir> — every figure of every PDF in the listing, through the production engine, as one TSV row of pdf_relevance signals, with its crop and the description its twin already holds
#
# The data half of the relevance bench: relevance_train.py fits the weights on these rows once each
# has a label. The labels are a person's (or an agent's, audited by one): `labels.tsv` beside the
# rows, `doc<TAB>figure<TAB>1|0`. The crops land in <out-dir>/img/ so a contact sheet can show them.
# Like the other benches, no corpus is versioned: the out-dir is passed in.
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(_HERE.parent), str(_HERE.parents[1]), str(_HERE.parents[2] / 'hooks')]
import describe  # noqa: E402
import pdf_figures  # noqa: E402
import pdf_meta  # noqa: E402
import pdf_relevance  # noqa: E402
import pdf_twin  # noqa: E402

DESCRIBED = re.compile(r'<!-- figure (p\d+-fig\d+) \| described_by: (\S+)[^>]*-->\n([^\n]*)')
COLUMNS = ('doc', 'figure', 'page', 'described_by', 'said') + pdf_relevance.SIGNALS


def described(twin: Path) -> dict[str, tuple[str, str]]:
    """{figure: (who described it, the first line it said)} from a twin already built."""
    if not twin.exists():
        return {}
    return {m[0]: (m[1], m[2][:160]) for m in DESCRIBED.findall(twin.read_text(encoding='utf-8'))}


def rows(pdf: Path, img_dir: Path) -> list[dict]:
    twin = pdf_meta.twin_of(pdf)
    engine = 'docling' if 'docling' in str(pdf_meta.read_frontmatter(twin).get('engine', '')) else 'pymupdf'
    said = described(twin)
    out = []
    with tempfile.TemporaryDirectory(prefix='relevance-') as tmp:
        result = pdf_twin.run_engine(engine, pdf, Path(tmp))
        for fig in pdf_figures.name_all(result['figures'], pdf_meta.pdfinfo(pdf)['pages']):
            if fig.same_as:
                continue
            ocr = describe.ocr(fig.source)
            sig = pdf_relevance.signals(fig, result['pages'][fig.page - 1], ocr)
            shutil.copyfile(fig.source, img_dir / f'{pdf.stem}--{fig.name}.png')
            by, head = said.get(fig.name, ('-', ''))
            out.append({'doc': pdf.stem, 'figure': fig.name, 'page': fig.page, 'described_by': by,
                        'said': ' '.join(head.split()).replace('\t', ' '), **sig})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('listing', type=Path, help='one PDF path per line')
    ap.add_argument('out', type=Path)
    args = ap.parse_args()
    (args.out / 'img').mkdir(parents=True, exist_ok=True)
    table = args.out / 'signals.tsv'
    done = {ln.split('\t')[0] for ln in table.read_text(encoding='utf-8').splitlines()[1:]} if table.exists() else set()
    if not done:
        table.write_text('\t'.join(COLUMNS) + '\n', encoding='utf-8', newline='\n')
    for line in args.listing.read_text(encoding='utf-8').splitlines():
        pdf = Path(line.strip())
        if not line.strip() or pdf.stem in done:
            continue
        try:
            found = rows(pdf, args.out / 'img')
        except Exception as e:  # noqa: BLE001 — one PDF's failure never ends the bench
            print(f'FAILED {pdf}: {e}', flush=True)
            continue
        with table.open('a', encoding='utf-8', newline='\n') as f:
            f.writelines('\t'.join(str(r[c]) for c in COLUMNS) + '\n' for r in found)
        print(f'{len(found):3d} figures  {pdf.stem}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
