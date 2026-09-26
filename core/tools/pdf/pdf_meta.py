# pdf_meta.py — what a twin says about its PDF before and after conversion: hash, pdfinfo, text layer, the free audit, the frontmatter.
#
# Everything here is poppler + tesseract + stdlib: zero tokens, no GPU. The frontmatter values are
# written as JSON, which is valid YAML, so one writer needs no YAML library and the reader
# (`read_frontmatter`) gets back exactly what was written.
from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

PDFINFO = {'Title': 'title', 'Author': 'author', 'Subject': 'subject', 'Keywords': 'keywords',
           'Creator': 'creator', 'Producer': 'producer', 'CreationDate': 'created',
           'ModDate': 'modified', 'Pages': 'pages', 'Encrypted': 'encrypted'}
TEXT_PAGE = 10     # a page with fewer pdftotext words than this has no usable text layer
WORD = re.compile(r'[a-zà-ÿ0-9]{3,}')
FIELDS = ('source', 'sha256', 'origin', 'origin_checked', 'pdf', 'text_layer', 'engine', 'audit',
          'needs_review', 'reviewed_by')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def pdfinfo(path: Path) -> dict:
    out = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True, encoding='utf-8').stdout
    info = {}
    for line in out.splitlines():
        key, _, value = line.partition(':')
        if key in PDFINFO and value.strip():
            info[PDFINFO[key]] = value.strip()
    info['pages'] = int(info.get('pages', 0))
    info['encrypted'] = info.get('encrypted', 'no').startswith('yes')
    return info


def page_texts(path: Path) -> list[str]:
    """pdftotext, one string per page (form feed is poppler's page separator)."""
    out = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True, text=True,
                         encoding='utf-8').stdout
    return out.split('\f')[:-1] if out.endswith('\f') else out.split('\f')


def text_layer(pages: list[str]) -> str:
    with_text = sum(len(p.split()) >= TEXT_PAGE for p in pages)
    if with_text == len(pages):
        return 'born-digital'
    return 'scanned' if with_text == 0 else 'mixed'


def ocr_page(path: Path, page: int) -> str:
    with tempfile.TemporaryDirectory(prefix='pdf-ocr-') as tmp:
        subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(page), '-l', str(page), str(path),
                        f'{tmp}/p'], capture_output=True)
        return '\n'.join(subprocess.run(['tesseract', str(img), '-', '-l', 'por+eng'],
                                        capture_output=True, text=True, encoding='utf-8').stdout
                         for img in sorted(Path(tmp).glob('p*.png')))


def reference(path: Path, pages: list[str]) -> str:
    """What the PDF says, from the free tools: the text layer, and OCR where a page has none."""
    return '\n'.join(text if len(text.split()) >= TEXT_PAGE else ocr_page(path, n)
                     for n, text in enumerate(pages, 1))


def coverage(reference_text: str, markdown: str) -> float:
    """Share of the reference's words (with multiplicity) that the twin kept."""
    ref = collections.Counter(WORD.findall(reference_text.lower()))
    got = collections.Counter(WORD.findall(markdown.lower()))
    return round(sum(min(c, got[w]) for w, c in ref.items()) / max(1, sum(ref.values())), 2)


def counts(markdown: str) -> dict:
    return {'tables': len(re.findall(r'^\|.*\|\s*\n\|[\s:|-]+\|', markdown, re.M)),
            'formulas': len(re.findall(r'\$\$.+?\$\$|<!-- formula', markdown, re.S))}


def render_frontmatter(fields: dict) -> str:
    return '---\n' + ''.join(f'{k}: {json.dumps(fields.get(k), ensure_ascii=False)}\n'
                             for k in FIELDS) + '---\n'


def read_frontmatter(twin: Path) -> dict:
    """The frontmatter of an existing twin, or {} when there is none to read."""
    if not twin.exists():
        return {}
    text = twin.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}
    return yaml.safe_load(text[4:text.index('\n---\n', 4)]) or {}


def replace_frontmatter(twin: Path, **changes) -> None:
    text = twin.read_text(encoding='utf-8')
    body = text[text.index('\n---\n', 4) + 5:]
    twin.write_text(render_frontmatter({**read_frontmatter(twin), **changes}) + body, encoding='utf-8', newline='\n')
