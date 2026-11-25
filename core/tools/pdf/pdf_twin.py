# pdf_twin.py — one PDF becomes its twin: a sibling folder whose .md holds all the text, every figure described, and the metadata that says whether the twin is still true.
#
#   res-12-2024.pdf
#   res-12-2024/res-12-2024.md     frontmatter + <!-- page N --> anchors + one block per figure
#   res-12-2024/img/p03-fig1.png   original, gitignored
#   res-12-2024/img/p03-fig1.jpg   small preview, versioned unless the PDF lives at a live URL
#
# Runs under .venv; the engines run under .venv-pdf through pdf_engine.py (see that file for why).
from __future__ import annotations

import concurrent.futures
import datetime
import json
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

import describe
import pdf_cache
import pdf_figures
import pdf_meta
import pdf_relevance
import platform_law
import secret_law

_HERE = Path(__file__).resolve().parent
ENGINE_VENV = '.venv-pdf'
ENGINE_TIMEOUT = 3600
REVIEW_COVERAGE = 0.9   # below this share of the PDF's own words, a person looks
WORKERS = 3             # vision calls at once: ~40% of each is the CLI starting (2026-11-25), so they overlap
NOBODY = describe.Description('', describe.NOBODY, None, False)


class EngineMissing(RuntimeError):
    pass


def run_engine(engine: str, pdf: Path, out: Path) -> dict:
    python = platform_law.venv_script('python', ENGINE_VENV)
    if not python.exists():
        raise EngineMissing(
            f'{ENGINE_VENV} is missing, so no engine can run. Install it (core/tools/pdf/CONTEXT.md § Install):\n'
            f'  uv venv -p 3.12 {ENGINE_VENV} && uv pip install --python {python} '
            f'-r core/tools/pdf/requirements-pdf.txt')
    r = subprocess.run([str(python), str(_HERE / 'pdf_engine.py'), engine, str(pdf), str(out)],
                       capture_output=True, text=True, encoding='utf-8', timeout=ENGINE_TIMEOUT)
    if r.returncode:
        raise RuntimeError(f'{engine} failed: {r.stderr.strip().splitlines()[-1:] or r.returncode}')
    return json.loads((out / 'engine.json').read_text(encoding='utf-8'))


def origin_live(url: str | None) -> bool:
    if not url:
        return False
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=10) as r:
            return r.status < 400
    except Exception:  # noqa: BLE001 — anything but a clean answer means "not live"
        return False


def _page_body(page_md: str, blocks: list[str]) -> str:
    parts = page_md.split('<!-- figure -->')
    queue = iter(blocks)
    return parts[0] + ''.join(next(queue, '') + part for part in parts[1:])


def _gitignore(folder: Path, live: bool, secret: bool) -> None:
    lines = ['*'] if secret else ['img/'] if live else ['img/*.png']
    (folder / '.gitignore').write_text('\n'.join(lines + ['review/']) + '\n', encoding='utf-8', newline='\n')


def _describe_all(figures: list, texts_of: dict, describer: str, _describe, cache) -> dict:
    """{name: Description} for the figures worth a vision call, WORKERS at a time; a cached answer is
    read back, and each new one is cached the moment it lands, so a dead run resumes where it stopped."""
    said, todo = {}, []
    for fig in figures:
        k = pdf_cache.key(fig.look, texts_of[fig.name])
        hit = cache.get(k) if cache else None
        if hit:
            said[fig.name] = hit
        else:
            todo.append((fig, k))
    if todo and _describe is describe.describe and describer in ('agy', 'local'):
        describe.agy_logged_in()   # asked once here, not by three workers at once
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        running = {pool.submit(_describe, fig.source, describer, texts_of[fig.name]): (fig, k) for fig, k in todo}
        for done in concurrent.futures.as_completed(running):
            fig, k = running[done]
            said[fig.name] = done.result()
            if cache:
                cache.put(k, said[fig.name])
    return said


def build(pdf: Path, engine: str, describer: str = 'agy', origin: str | None = None, force: bool = False,
          _engine=run_engine, _describe=describe.describe, _ocr=describe.ocr, cache=None) -> dict:
    """Write the twin of one PDF. Returns what happened, for the batch summary."""
    state, twin = pdf_meta.twin_state(pdf)
    before = pdf_meta.read_frontmatter(twin)
    if state == 'fresh' and not force:
        return {'status': 'fresh', 'twin': twin, 'needs_review': before.get('needs_review')}
    digest = pdf_meta.sha256(pdf)
    info, texts = pdf_meta.pdfinfo(pdf), pdf_meta.page_texts(pdf)
    origin = origin or before.get('origin')
    live = origin_live(origin)
    folder = twin.parent
    with tempfile.TemporaryDirectory(prefix='pdf-twin-') as tmp:
        result = _engine(engine, pdf, Path(tmp))
        shutil.rmtree(folder / 'img', ignore_errors=True)   # only once the new figures exist
        figures = pdf_figures.name_all(result['figures'], info['pages'])
        firsts = [f for f in figures if not f.same_as]
        texts_of = {f.name: _ocr(f.source) for f in firsts}
        table, seen = pdf_relevance.load(), pdf_relevance.decorations()
        doc = pdf_relevance.document([pdf_relevance.area(f) for f in firsts])
        verdicts = {f.name: pdf_relevance.verdict(f, result['pages'][f.page - 1], texts_of[f.name], describer,
                                                  table, doc, seen) for f in firsts}
        said = _describe_all([f for f in firsts if verdicts[f.name][0] == 'describe'], texts_of, describer,
                             _describe, cache)
        links, blocks, flagged, figure_text = {}, {}, False, []
        for fig in figures:
            first = fig.same_as or fig.name
            action, why = verdicts[first]
            if action == 'hide':   # a crest or a letterhead: not saved or described, only counted below
                continue
            if fig.same_as:
                blocks.setdefault(fig.page, []).append(pdf_figures.block(fig, links[fig.same_as]))
                continue
            links[fig.name] = pdf_figures.save(fig, folder / 'img', preview=not live)
            figure_text.append(texts_of[fig.name])
            told = said.get(fig.name, NOBODY)
            flagged |= told.needs_review
            blocks.setdefault(fig.page, []).append(
                pdf_figures.block(fig, links[fig.name], told, texts_of[fig.name], why))
    pages = result['pages']
    body = ''.join(f'<!-- page {n} -->\n\n{_page_body(md, blocks.get(n, []))}\n\n'
                   for n, md in enumerate(pages, 1))
    # The reference OCRs a page with no text layer whole, figures included, so the figures' own OCR —
    # which the twin keeps verbatim — counts too; without it a slide deck scored 0.57 for text it has.
    coverage = pdf_meta.coverage(pdf_meta.reference(pdf, texts), '\n'.join(pages + figure_text))
    distinct = sum(not f.same_as for f in figures)
    audit = {'word_coverage': coverage, 'images': f'{distinct}/{pdf_figures.embedded_count(pdf)}',
             'pages': f'{len(pages)}/{info["pages"]}', **pdf_meta.counts('\n'.join(pages))}
    needs_review = flagged or coverage < REVIEW_COVERAGE or len(pages) != info['pages']
    fields = {'description': before.get('description'),
              'source': f'../{pdf.name}', 'sha256': digest, 'origin': origin,
              'origin_checked': datetime.date.today().isoformat() if origin else None, 'pdf': info,
              'text_layer': pdf_meta.text_layer(texts), 'engine': result['engine'], 'audit': audit,
              'needs_review': needs_review, 'reviewed_by': None}
    folder.mkdir(parents=True, exist_ok=True)
    twin.write_text(pdf_meta.render_frontmatter(fields) + '\n' + body.rstrip() + '\n', encoding='utf-8', newline='\n')
    secrets = secret_law.scan(twin)
    _gitignore(folder, live, bool(secrets))
    return {'status': 'written', 'twin': twin, 'needs_review': needs_review, 'audit': audit,
            'secrets': sorted({f.kind for f in secrets})}
