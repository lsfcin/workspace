#!/usr/bin/env python3
# Draw a course page's progress panel from its data block, and refuse a panel whose boxes do not add up.
#
# The data block is authored — Lucas marks each verification item 'v' (done) or '-' (pending):
#
#   <!-- painel:dados-va1 caixas=50
#   albérico: git=vvv, tex=vvv-, mlp·c=vvvvv
#   -->
#
# The drawing is generated, between <!-- painel-va1:start --> and <!-- painel-va1:end -->, so the
# size cap does not weigh it (core/hooks/file_law.py authored_text) and nobody edits it by hand.
# `caixas=` is the total the course promises per student; a row that does not reach it exactly is an
# error, because "50 boxes = 100 points = 10,0" is the rule the students were handed.
#
#   python3 academy/teaching/structure/painel.py <disciplina.md>          rewrite every panel
#   python3 academy/teaching/structure/painel.py <disciplina.md> --check  exit 1 if a drawing is stale
import re
import sys
from pathlib import Path

DONE, PENDING = '◼', '◻'
DATA = re.compile(r'<!--\s*painel:dados-(?P<id>[\w-]+)(?:\s+caixas=(?P<caixas>\d+))?\s*\n'
                  r'(?P<body>.*?)-->', re.S)


def parse(body: str) -> list:
    """[(name, [(code, marks)])] in the order written."""
    rows = []
    for line in body.strip().splitlines():
        name, _, cells = line.partition(':')
        items = [cell.strip().split('=', 1) for cell in cells.split(',') if cell.strip()]
        rows.append((name.strip(), [(code.strip(), marks.strip()) for code, marks in items]))
    return rows


def check(panel: str, caixas, rows: list) -> list:
    """Every way a panel can lie: a stray mark, a row shaped unlike the first, a code wider than
    its boxes, or a total other than the one promised."""
    errors, shape = [], [(code, len(marks)) for code, marks in rows[0][1]]
    for name, items in rows:
        if [(code, len(marks)) for code, marks in items] != shape:
            errors.append(f'{panel}: {name} is not shaped like {rows[0][0]}')
        if any(set(marks) - {'v', '-'} for _, marks in items):
            errors.append(f'{panel}: {name} has a mark other than v or -')
    errors += [f'{panel}: code {code} is wider than its {width} boxes'
               for code, width in shape if len(code) > width]
    total = sum(width for _, width in shape)
    if caixas and total != int(caixas):
        errors.append(f'{panel}: {total} boxes per student, promised {caixas}')
    return errors


def draw(panel: str, rows: list) -> str:
    """The fenced text block: names right-aligned, one space between groups, points at the end."""
    width = max(len(name) for name, _ in rows)
    groups = [(code, len(marks)) for code, marks in rows[0][1]]
    label = 'nota ' + re.sub(r'\D', '', panel)
    header = ' ' * (width + 3) + ' '.join(code.ljust(n) for code, n in groups) + ' ' + label
    lines = [header.rstrip()]
    for name, items in rows:
        boxes = ' '.join(marks.replace('v', DONE).replace('-', PENDING) for _, marks in items)
        points = 2 * sum(marks.count('v') for _, marks in items)
        lines.append(f'{name.rjust(width)}   {boxes} {points:02d} pts')
    return '```text\n' + '\n'.join(lines) + '\n```'


def render(text: str) -> tuple:
    """(new text, errors). A panel with errors is left exactly as it was."""
    errors = []
    for match in DATA.finditer(text):
        panel, rows = match['id'], parse(match['body'])
        found = check(panel, match['caixas'], rows)
        errors += found
        if found:
            continue
        block = re.compile(rf'(<!--\s*painel-{panel}:start\s*-->\n).*?(\n<!--\s*painel-{panel}:end\s*-->)',
                           re.S)
        if not block.search(text):
            errors.append(f'{panel}: no <!-- painel-{panel}:start/end --> block to draw into')
            continue
        drawing = draw(panel, rows)
        text = block.sub(lambda m: m[1] + drawing + m[2], text)
    return text, errors


def main() -> int:
    path, stale_only = Path(sys.argv[1]), '--check' in sys.argv[2:]
    old = path.read_text(encoding='utf-8')
    new, errors = render(old)
    for error in errors:
        print(error, file=sys.stderr)
    if stale_only:
        if new != old:
            print(f'{path}: panel drawing is stale — run without --check', file=sys.stderr)
        return 1 if errors or new != old else 0
    if new != old:
        path.write_text(new, encoding='utf-8', newline='\n')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
