# pdf_cache.py — a figure described once is never described again: the same look with the same OCR, in this PDF or any other, reads its answer back.
#
# WHY. A run that dies at figure 90 of 127 lost 45 minutes of vision calls (2026-11-24, the PDI),
# and the same SIGAA screen or crest crosses dozens of documents. Each answer is appended the moment
# it lands, so the cache is both the resume and the cross-document memory. The key is the average
# hash AND the OCR: two screenshots of one template share a look but not their text.
# Only trusted answers are kept: a flagged one is asked again next time.
from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path

import describe

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / '.cache' / 'describe.jsonl'   # gitignored: the OCR can hold what a twin's .gitignore hides


def key(look: str, ocr_text: str) -> str:
    return hashlib.sha256(f'{look}\n{" ".join(ocr_text.split()).lower()}'.encode()).hexdigest()


class Cache:
    def __init__(self, path: Path = CACHE):
        self.path, self._lock, self._known = path, threading.Lock(), {}
        if path.exists():
            for line in path.read_text(encoding='utf-8').splitlines():
                entry = json.loads(line)
                self._known[entry['key']] = describe.Description(entry['text'], entry['by'], entry['overlap'], False)

    def get(self, k: str) -> describe.Description | None:
        return self._known.get(k)

    def put(self, k: str, said: describe.Description) -> None:
        if said.needs_review or not said.text or said.by == describe.NOBODY:
            return
        with self._lock:
            self._known[k] = said
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open('a', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps({'key': k, 'text': said.text, 'by': said.by, 'overlap': said.overlap},
                                   ensure_ascii=False) + '\n')
