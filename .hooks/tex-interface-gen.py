#!/usr/bin/env python3
# tex-interface-gen.py: Generate .texif interfaces, LABELS.md, and bib/review checks.
#
# Usage:
#   tex-interface-gen.py <file.tex>             — generate <stem>.texif + regenerate LABELS.md
#   tex-interface-gen.py --bib-check <file.bib> — warn about missing reviews/*.yaml files

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── Environment sets ─────────────────────────────────────────────────────────

EQ_ENVS = {
    'equation', 'equation*', 'align', 'align*', 'alignat', 'alignat*',
    'cases', 'multline', 'multline*', 'gather', 'gather*', 'eqnarray', 'eqnarray*',
    'subequations', 'flalign', 'flalign*',
}
FLOAT_ENVS = {'figure', 'figure*', 'table', 'table*', 'wrapfigure', 'wraptable'}
LISTING_ENVS = {'lstlisting', 'minted', 'verbatim', 'code', 'Verbatim'}

# ─── Helpers ──────────────────────────────────────────────────────────────────


def line_of(text: str, pos: int) -> int:
    return text[:pos].count('\n') + 1


def extract_braced(text: str, open_pos: int) -> str:
    depth, buf = 0, []
    for c in text[open_pos:]:
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                break
        if depth > 0:
            buf.append(c)
    return ''.join(buf)


def extract_caption(body: str) -> str | None:
    m = re.search(r'\\caption\{', body)
    if not m:
        return None
    open_brace = body.find('{', m.start() + len('\\caption') - 1)
    if open_brace == -1:
        return None
    return extract_braced(body, open_brace).strip()


def first_prose_snippet(text: str, after_pos: int, until_pos: int, n: int = 10) -> str | None:
    for line in text[after_pos:until_pos].splitlines():
        s = line.strip()
        if s and not s.startswith('%') and not s.startswith('\\') and len(s) > 10:
            words = s.split()[:n]
            return ' '.join(words) + ('...' if len(s.split()) > n else '')
    return None


def find_paper_root(path: Path) -> Path | None:
    p = path if path.is_dir() else path.parent
    while True:
        if (p / 'main.tex').exists() or (p / '.latexmkrc').exists():
            return p
        parent = p.parent
        if parent == p:
            return None
        p = parent


def word_count(text: str) -> int:
    count = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith('%') or s.startswith('\\begin') or s.startswith('\\end'):
            continue
        count += len(s.split())
    return count


# ─── Parser ───────────────────────────────────────────────────────────────────


def parse_tex(path: Path) -> dict:
    text = path.read_text(encoding='utf-8', errors='ignore')

    result: dict = {
        'loc': len(text.splitlines()),
        'words': word_count(text),
        'struct_points': [],   # {line, level, title}  — all sections/subsections
        'openings': {},        # (level, title) -> snippet
        'content_items': [],   # {line, kind, data}  — floats/equations/listings
        'citations': set(),
        'todos': [],
        'inputs': [],
        'defined_labels': [],
        'used_refs': [],
    }

    # ── Section structure ────────────────────────────────────────────────────
    sec_re = re.compile(r'\\((?:sub){0,2}section)\*?\{([^}]+)\}')
    sec_positions: list[tuple[int, int, str]] = []  # (pos, level, title)
    for m in sec_re.finditer(text):
        cmd = m.group(1)
        level = {'section': 1, 'subsection': 2, 'subsubsection': 3}[cmd]
        title = m.group(2).strip()
        lnum = line_of(text, m.start())
        result['struct_points'].append({'line': lnum, 'level': level, 'title': title})
        sec_positions.append((m.start(), level, title))

    # ── Opening snippets for each section/subsection ──────────────────────────
    for i, (pos, level, title) in enumerate(sec_positions):
        next_pos = sec_positions[i + 1][0] if i + 1 < len(sec_positions) else len(text)
        brace_end = text.find('}', pos)
        after = brace_end + 1 if brace_end != -1 else pos + 30
        snippet = first_prose_snippet(text, after, next_pos)
        if snippet:
            result['openings'][(level, title)] = snippet

    # ── TODOs ────────────────────────────────────────────────────────────────
    todo_re = re.compile(r'%\s*TODO[:\s]+(.+)', re.IGNORECASE)
    for i, line in enumerate(text.splitlines(), 1):
        m = todo_re.search(line)
        if m:
            result['todos'].append({'line': i, 'text': m.group(1).strip()})

    # ── Citations ────────────────────────────────────────────────────────────
    cite_re = re.compile(r'\\cite\w*\{([^}]+)\}')
    for m in cite_re.finditer(text):
        for key in m.group(1).split(','):
            k = key.strip()
            if k:
                result['citations'].add(k)

    # ── Cross-references (for LABELS.md) ─────────────────────────────────────
    for m in re.finditer(r'\\(?:ref|eqref|pageref|autoref|cref)\{([^}]+)\}', text):
        result['used_refs'].append({'ref': m.group(1).strip(), 'line': line_of(text, m.start())})

    # ── \input commands ───────────────────────────────────────────────────────
    for m in re.finditer(r'\\input\{([^}]+)\}', text):
        result['inputs'].append({'path': m.group(1).strip(), 'line': line_of(text, m.start())})

    # ── Environments ─────────────────────────────────────────────────────────
    env_re = re.compile(r'\\begin\{(\w+\*?)\}(.*?)\\end\{\1\}', re.DOTALL)
    for m in env_re.finditer(text):
        env = m.group(1)
        body = m.group(2)
        env_line = line_of(text, m.start())

        label_m = re.search(r'\\label\{([^}]+)\}', body)
        label = label_m.group(1).strip() if label_m else None
        caption = extract_caption(body)

        if env in EQ_ENVS:
            content = re.sub(r'\\label\{[^}]+\}', '', body).strip()
            result['content_items'].append({
                'line': env_line, 'kind': 'equation',
                'data': {'env': env, 'label': label, 'content': content},
            })
            if label:
                result['defined_labels'].append({'label': label, 'type': 'equation', 'line': env_line})

        elif env in FLOAT_ENVS:
            float_type = 'figure' if 'figure' in env else 'table'
            result['content_items'].append({
                'line': env_line, 'kind': float_type,
                'data': {'label': label, 'caption': caption},
            })
            if label:
                result['defined_labels'].append({'label': label, 'type': float_type, 'line': env_line})

        elif env in LISTING_ENVS:
            opts_m = re.search(r'\\begin\{' + re.escape(env) + r'\}\[([^\]]*)\]', m.group(0))
            lang = cap = lbl = None
            if opts_m:
                opts = opts_m.group(1)
                lm = re.search(r'language\s*=\s*(\w+)', opts)
                if lm:
                    lang = lm.group(1)
                cm = re.search(r'caption\s*=\s*\{([^}]*)\}', opts)
                if cm:
                    cap = cm.group(1)
                lbm = re.search(r'label\s*=\s*\{([^}]*)\}', opts)
                if lbm:
                    lbl = lbm.group(1)
            body_lines = body.strip().splitlines()
            final_label = lbl or label
            result['content_items'].append({
                'line': env_line, 'kind': 'listing',
                'data': {
                    'label': final_label, 'caption': cap or caption,
                    'lang': lang, 'loc': len(body_lines), 'preview': body_lines[:5],
                },
            })
            if final_label:
                result['defined_labels'].append({'label': final_label, 'type': 'listing', 'line': env_line})

    # ── Standalone \label{} not inside an environment ─────────────────────────
    already = {e['label'] for e in result['defined_labels']}
    for m in re.finditer(r'\\label\{([^}]+)\}', text):
        lbl = m.group(1).strip()
        if lbl not in already:
            lbl_line = line_of(text, m.start())
            nearby = text[max(0, m.start() - 80):m.start()]
            ltype = 'section' if ('\\section' in nearby or '\\subsection' in nearby) else 'other'
            result['defined_labels'].append({'label': lbl, 'type': ltype, 'line': lbl_line})
            already.add(lbl)

    return result


# ─── .texif writer ────────────────────────────────────────────────────────────


def write_interface(tex_path: Path, data: dict, paper_root: Path | None) -> Path:
    out_path = tex_path.with_suffix('.texif')
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    rel = str(tex_path.relative_to(paper_root)) if paper_root else tex_path.name

    lines: list[str] = []

    lines.append(
        f'<!-- INTERFACE: {rel} | LOC: {data["loc"]} | ~{data["words"]} words | {ts} -->\n'
        f'<!-- Auto-generated — do not edit. Regenerated on every save of the source. -->'
    )

    # Merge struct_points and content_items into one event stream sorted by line
    events: list[tuple[int, str, dict]] = []
    for s in data['struct_points']:
        events.append((s['line'], 'struct', s))
    for c in data['content_items']:
        events.append((c['line'], c['kind'], c['data']))
    events.sort(key=lambda x: x[0])

    openings = data['openings']

    def render_content(lnum: int, kind: str, d: dict) -> list[str]:
        out: list[str] = []
        if kind == 'equation':
            lbl = f'`{d["label"]}`' if d['label'] else '*(unlabelled)*'
            out.append(f'`equation` [line {lnum}] {lbl}')
            out.append('```latex')
            out.append(d['content'].strip())
            out.append('```')
        elif kind in ('figure', 'table'):
            lbl = f'`{d["label"]}`' if d['label'] else '*(unlabelled)*'
            cap = f'"{d["caption"]}"' if d['caption'] else '*(no caption)*'
            out.append(f'`{kind}` [line {lnum}] {lbl} — {cap}')
        elif kind == 'listing':
            lbl = f'`{d["label"]}`' if d['label'] else '*(unlabelled)*'
            cap = f'"{d["caption"]}"' if d['caption'] else '*(no caption)*'
            lang = d['lang'] or 'text'
            out.append(f'`listing` [line {lnum}] {lbl} · {lang} · {d["loc"]} lines — {cap}')
            if d['preview']:
                out.append(f'```{lang}')
                out.extend(d['preview'])
                out.append('```')
        return out

    for lnum, kind, d in events:
        if kind == 'struct':
            level, title = d['level'], d['title']
            lines.append('')
            lines.append('#' * level + ' ' + title)
            snippet = openings.get((level, title))
            if snippet:
                lines.append(f'*"{snippet}"*')
        else:
            lines.extend(render_content(lnum, kind, d))

    # Inputs (\input commands — mainly useful for main.tex)
    if data['inputs']:
        lines.append('\n---')
        lines.append('\n## Inputs')
        for i in data['inputs']:
            lines.append(f'- `{i["path"]}` [line {i["line"]}]')

    # Citations
    if data['citations']:
        lines.append('\n---')
        cites = ' · '.join(f'`{k}`' for k in sorted(data['citations']))
        lines.append(f'\n## Citations\n\n{cites}')

    # TODOs
    if data['todos']:
        lines.append('\n---')
        lines.append('\n## TODOs')
        for t in data['todos']:
            lines.append(f'- [line {t["line"]}] {t["text"]}')

    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out_path


# ─── Relationship check ───────────────────────────────────────────────────────


def check_relationships(data: dict, paper_root: Path) -> None:
    """Warn about cited papers whose reviews/<key>.yaml lacks a this_paper relationship."""
    if not data['citations']:
        return
    reviews_dir = paper_root / 'reviews'
    if not reviews_dir.exists():
        return

    missing: list[str] = []
    for key in sorted(data['citations']):
        yaml_path = reviews_dir / f'{key}.yaml'
        if not yaml_path.exists():
            continue  # bib-check handles missing files
        try:
            content = yaml_path.read_text(encoding='utf-8', errors='ignore')
            has_rel = bool(re.search(r'this_paper:\s*".{5,}"', content))
            if not has_rel:
                missing.append(key)
        except Exception:
            pass

    if missing:
        print(f'💬 RELATIONSHIPS: add/update this_paper in {len(missing)} review(s):')
        for k in missing:
            print(f'   reviews/{k}.yaml → relationships.this_paper')


# ─── LABELS.md regenerator ────────────────────────────────────────────────────


def regenerate_labels(paper_root: Path) -> None:
    tex_files = sorted(f for f in paper_root.rglob('*.tex') if '.texif' not in str(f) and 'build' not in str(f))

    all_defined: list[dict] = []
    all_used: list[dict] = []

    for tf in tex_files:
        try:
            d = parse_tex(tf)
        except Exception:
            continue
        rel = str(tf.relative_to(paper_root))
        for lbl in d['defined_labels']:
            all_defined.append({**lbl, 'file': rel})
        for ref in d['used_refs']:
            all_used.append({**ref, 'file': rel})

    defined_set = {e['label'] for e in all_defined}
    dangling = [u for u in all_used if u['ref'] not in defined_set]

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    out: list[str] = [
        '# LABELS — cross-file label registry',
        f'> Auto-generated {ts} — do not edit.',
        '',
        '## Defined Labels',
        '',
        f'{"Label":<40} {"Type":<12} {"File":<50} Line',
        '─' * 110,
    ]
    for e in sorted(all_defined, key=lambda x: x['label']):
        out.append(f'{e["label"]:<40} {e["type"]:<12} {e["file"]:<50} {e["line"]}')

    out.append('')
    if dangling:
        out.append(f'## Dangling References ({len(dangling)} issues) ⚠')
        out.append('')
        out.append(f'{"\\ref{...}":<40} {"Used in":<50} Line')
        out.append('─' * 100)
        for dr in sorted(dangling, key=lambda x: x['ref']):
            out.append(f'{dr["ref"]:<40} {dr["file"]:<50} {dr["line"]}')
    else:
        out.append('## Dangling References (0 issues)')
        out.append('')
        out.append('All \\ref{} usages resolved.')

    labels_path = paper_root / 'LABELS.md'
    labels_path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'✓ LABELS.md: {labels_path}')


# ─── Bib check ────────────────────────────────────────────────────────────────


def bib_check(bib_path: Path) -> None:
    text = bib_path.read_text(encoding='utf-8', errors='ignore')
    keys = re.findall(r'^@\w+\{(\w+),', text, re.MULTILINE)

    root = find_paper_root(bib_path)
    if not root:
        return

    reviews_dir = root / 'reviews'
    if not reviews_dir.exists():
        print(f'💬 REVIEWS: reviews/ directory missing at {reviews_dir}')
        return

    missing = [k for k in keys if not (reviews_dir / f'{k}.yaml').exists()]
    if missing:
        print(f'💬 REVIEWS MISSING ({len(missing)}) — create review files:')
        for k in missing:
            print(f'   {k}  →  reviews/{k}.yaml')
    else:
        print(f'✓ reviews: all {len(keys)} bib entries have review files')


# ─── Entry point ──────────────────────────────────────────────────────────────


def main() -> int:
    args = sys.argv[1:]

    if not args:
        print('Usage: tex-interface-gen.py <file.tex> | --bib-check <file.bib>', file=sys.stderr)
        return 1

    if args[0] == '--bib-check':
        if len(args) < 2:
            print('--bib-check requires a .bib path', file=sys.stderr)
            return 1
        bib_check(Path(args[1]))
        return 0

    tex_path = Path(args[0])
    if not tex_path.exists() or tex_path.suffix != '.tex':
        return 0

    root = find_paper_root(tex_path)

    try:
        data = parse_tex(tex_path)
        out = write_interface(tex_path, data, root)
        print(f'✓ .texif: {out}')
    except Exception as e:
        print(f'⚠ tex-interface-gen: {tex_path}: {e}', file=sys.stderr)
        return 1

    if root:
        try:
            regenerate_labels(root)
        except Exception as e:
            print(f'⚠ LABELS.md: {e}', file=sys.stderr)
        try:
            check_relationships(data, root)
        except Exception as e:
            print(f'⚠ relationships check: {e}', file=sys.stderr)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
