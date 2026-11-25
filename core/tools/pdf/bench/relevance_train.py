# Usage: core/run tools/pdf/bench/relevance_train.py <out-dir> [--recall 0.98] [--write <profile-dir>] — fit pdf_relevance's weights on <out-dir>/signals.tsv and labels.tsv, leaving one document out at a time, and print what the bar would skip and miss
#
# The model half of the relevance bench (the panel, 2026-11-25): an L1 logistic regression, because
# 50 documents are too few for a tree and a person must be able to read why a figure was skipped.
# Figures of one document are not independent, so each document is held out whole and scored by a
# model that never saw it. The bar is the lowest-cost one whose rules-plus-score recall still meets
# --recall. --write replaces the profile's relevance.tsv and decorations.txt (pdf_relevance.py says
# what a profile is); without it nothing changes.
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(_HERE.parent), str(_HERE.parents[1]), str(_HERE.parents[2] / 'hooks')]
import pdf_relevance  # noqa: E402

NEVER = {'threshold': (0, 1, 2.0), 'bias': (0, 1, 0.0)}   # a table under which only the rules describe
C_GRID = (0.03, 0.1, 0.3, 1.0, 3.0)


def labelled(out: Path) -> tuple[list[dict], list[int]]:
    labels = {(r[0], r[1]): int(r[2]) for r in csv.reader((out / 'labels.tsv').open(encoding='utf-8'), delimiter='\t')
              if len(r) >= 3 and r[2] in ('0', '1')}
    rows = [r for r in csv.DictReader((out / 'signals.tsv').open(encoding='utf-8'), delimiter='\t')
            if (r['doc'], r['figure']) in labels]
    for r in rows:
        r.update({k: float(r[k]) for k in pdf_relevance.SIGNALS if k in r})
    for doc in {r['doc'] for r in rows}:   # the whole-PDF signals, from every figure the bench found in it
        mine = [r for r in rows if r['doc'] == doc]
        for r in mine:
            r.update(pdf_relevance.document([r_['area'] for r_ in mine]))
    return rows, [labels[(r['doc'], r['figure'])] for r in rows]


def out_of_fold(rows: list[dict], y: list[int], c: float) -> list[float]:
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import LeaveOneGroupOut
    from sklearn.preprocessing import StandardScaler
    x = np.array([[r[k] for k in pdf_relevance.SIGNALS] for r in rows])
    groups, p = [r['doc'] for r in rows], np.zeros(len(rows))
    for train, test in LeaveOneGroupOut().split(x, y, groups):
        if len(set(np.array(y)[train])) < 2:
            p[test] = np.mean(np.array(y)[train])
            continue
        scale = StandardScaler().fit(x[train])
        model = LogisticRegression(l1_ratio=1.0, C=c, solver='liblinear', class_weight='balanced')
        model.fit(scale.transform(x[train]), np.array(y)[train])
        p[test] = model.predict_proba(scale.transform(x[test]))[:, 1]
    return list(p)


def bar(p: list[float], ruled: list[bool], y: list[int], recall: float) -> tuple[float, float, float]:
    """(threshold, recall, skipped share): the highest threshold whose rules-or-score recall holds."""
    relevant = sum(y) or 1
    best = (0.0, 1.0, 0.0)
    for t in sorted(set(round(v, 3) for v in p)):
        kept = [r or v >= t for r, v in zip(ruled, p)]
        hit = sum(k and t_ for k, t_ in zip(kept, y)) / relevant
        if hit >= recall:
            best = (t, hit, 1 - sum(kept) / len(kept))
    return best


def fit_all(rows: list[dict], y: list[int], c: float) -> dict:
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    x = np.array([[r[k] for k in pdf_relevance.SIGNALS] for r in rows])
    scale = StandardScaler().fit(x)
    model = LogisticRegression(l1_ratio=1.0, C=c, solver='liblinear', class_weight='balanced').fit(scale.transform(x), y)
    return {k: (float(m), float(s), float(w)) for k, m, s, w in
            zip(pdf_relevance.SIGNALS, scale.mean_, scale.scale_, model.coef_[0]) if abs(w) > 1e-6} | \
        {'bias': (0.0, 1.0, float(model.intercept_[0]))}


def write(profile: Path, table: dict, threshold: float, note: str) -> None:
    lines = [f'# The weights pdf_relevance.py scores a figure with: z = bias + sum(weight * (value - mean) / std), '
             f'p = 1 / (1 + e^-z); a figure at or above `threshold` is described.',
             '# Written by bench/relevance_train.py from labelled figures; edit by retraining, not by hand.',
             f'# {note}', 'signal\tmean\tstd\tweight', f'threshold\t0\t1\t{threshold:.3f}']
    lines += [f'{k}\t{m:.4f}\t{s:.4f}\t{w:.4f}' for k, (m, s, w) in table.items()]
    (profile / pdf_relevance.WEIGHTS).write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('out', type=Path)
    ap.add_argument('--recall', type=float, default=0.98)
    ap.add_argument('--write', metavar='PROFILE', type=Path, help="the collection's profile folder to write")
    args = ap.parse_args()
    rows, y = labelled(args.out)
    ruled = [pdf_relevance.judge(r, NEVER)[0] == 'describe' for r in rows]
    print(f'{len(rows)} labelled figures, {sum(y)} relevant, {len({r["doc"] for r in rows})} documents; '
          f'the rules alone describe {sum(ruled)}')
    results = []
    for c in C_GRID:
        t, hit, skipped = bar(out_of_fold(rows, y, c), ruled, y, args.recall)
        results.append((skipped, c, t, hit))
        print(f'C={c:<5} threshold={t:.3f} recall={hit:.3f} skipped={skipped:.1%}')
    skipped, c, t, hit = max(results)
    table = fit_all(rows, y, c)
    print('weights:', ', '.join(f'{k} {w:+.2f}' for k, (_, _, w) in sorted(table.items(), key=lambda kv: -abs(kv[1][2]))))
    if args.write:
        import pdf_figures
        looks = sorted({f'{int(pdf_figures.look(args.out / "img" / f"{r["doc"]}--{r["figure"]}.png"), 2):064x}'
                        for r, label in zip(rows, y) if not label})
        args.write.mkdir(parents=True, exist_ok=True)
        (args.write / pdf_relevance.DECORATIONS).write_text(
            '# Looks (256-bit average hash, hex) of figures labelled decorative by bench/relevance_train.py.\n'
            + '\n'.join(looks) + '\n', encoding='utf-8', newline='\n')
        write(args.write, table, t, f'Trained {len(rows)} figures / {len({r["doc"] for r in rows})} documents, '
                                    f'C={c}: held-out recall {hit:.3f}, skipped {skipped:.1%}.')
        print(f'wrote {args.write}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
