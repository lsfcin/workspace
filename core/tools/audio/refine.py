# Deterministic STT vocabulary correction, prompt builder, Ollama polish, and log
from __future__ import annotations

import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.request

_HERE = pathlib.Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_DEFAULT_MANUAL = _HERE / "vocab.json"
_AIWBOT_HOTWORDS = _ROOT / "code" / "aiwbot" / "frontend" / "voice" / "hotwords.py"


def state_dir() -> pathlib.Path:
    override = os.environ.get("WOS_STT_STATE_DIR")
    return pathlib.Path(override) if override else _ROOT / "outputs" / "state" / "stt"


def load_aiwbot_carrier(path: pathlib.Path | None = None) -> list[str]:
    """Read CARRIER sentences from aiwbot hotwords.py without duplicating them in two files."""
    src = path or _AIWBOT_HOTWORDS
    if not src.is_file():
        return []
    ns: dict = {}
    try:
        exec(compile(src.read_text(encoding="utf-8"), str(src), "exec"), ns)
    except Exception:
        return []
    carrier = ns.get("CARRIER")
    return [str(s) for s in carrier if isinstance(s, str)] if isinstance(carrier, list) else []


def load_vocab(manual_path: pathlib.Path | None = None,
               learned_path: pathlib.Path | None = None) -> dict:
    """Merge manual vocab.json with auto-learned rules; manual replacements always win."""
    m_path = manual_path or _DEFAULT_MANUAL
    l_path = learned_path or (state_dir() / "learned.json")
    manual = json.loads(m_path.read_text(encoding="utf-8")) if m_path.is_file() else {}
    learned = json.loads(l_path.read_text(encoding="utf-8")) if l_path.is_file() else {}
    repl: dict[str, str] = {}
    for k, v in (learned.get("replacements") or {}).items():
        if isinstance(k, str) and isinstance(v, str) and k and v:
            repl[k.lower()] = v
    for k, v in (manual.get("replacements") or {}).items():
        if isinstance(k, str) and isinstance(v, str) and k and v:
            repl[k.lower()] = v
    carrier = [str(s) for s in (manual.get("carrier") or []) if isinstance(s, str)]
    terms = [str(t) for t in (learned.get("terms") or []) if isinstance(t, str)]
    return {"replacements": repl, "carrier": carrier, "learned_terms": terms}


def build_prompt(extra_carrier: list[str], base_carrier: list[str],
                 learned_terms: list[str] | None = None, max_chars: int = 750) -> str:
    """Build punctuated end-to-end prose (AD-21: never append a bare word list)."""
    sentences = [s.strip() for s in [*extra_carrier, *base_carrier] if s and s.strip()]
    joined_lower = " ".join(sentences).lower()
    novel = [t.strip() for t in (learned_terms or []) if t.strip() and t.lower() not in joined_lower]
    if novel:
        sentences.append(f"Também costumo citar {', '.join(novel[:12])}.")
    kept: list[str] = []
    total = 0
    for sentence in sentences:
        add = len(sentence) + (1 if kept else 0)
        if kept and total + add > max_chars:
            break
        kept.append(sentence)
        total += add
    return " ".join(kept)


def apply_replacements(text: str, replacements: dict[str, str]) -> str:
    """Replace misrecognized terms on word boundaries, preserving initial capitalization."""
    if not text or not replacements:
        return text
    ordered = sorted(replacements.keys(), key=len, reverse=True)
    pattern = re.compile(r"(?<!\w)(" + "|".join(re.escape(k) for k in ordered) + r")(?!\w)",
                         re.IGNORECASE)

    def _sub(match: re.Match[str]) -> str:
        src = match.group(0)
        target = replacements[src.lower()]
        if src[:1].isupper() and target[:1].islower():
            return target[:1].upper() + target[1:]
        return target

    return pattern.sub(_sub, text)


def polish_ollama(text: str, model: str = "gemma3:4b",
                  url: str = "http://127.0.0.1:11434/api/generate",
                  timeout: float = 4.0, keep_alive: str = "60s") -> str:
    """Optional lightweight LLM cleanup for hesitations/punctuation; fails safe to original text."""
    stripped = text.strip()
    if not stripped:
        return text
    prompt = (
        "Limpe apenas hesitações, repetições e pontuação desta transcrição em português do Brasil. "
        "NÃO traduza nem altere termos técnicos em inglês, nomes próprios ou sentido. "
        "Devolva somente o texto limpo, sem comentários.\n\n"
        f"Texto: {stripped}"
    )
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "keep_alive": keep_alive}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, ValueError):
        return stripped
    out = str(data.get("response") or "").strip()
    if not out or len(out) < len(stripped) * 0.4 or len(out) > len(stripped) * 1.6:
        return stripped
    return out


def refine_text(raw: str, vocab: dict, use_polish: bool = False) -> str:
    """Apply deterministic replacements and optional Ollama polish."""
    cleaned = apply_replacements(raw.strip(), vocab.get("replacements") or {})
    if use_polish and cleaned:
        cleaned = polish_ollama(cleaned)
        cleaned = apply_replacements(cleaned, vocab.get("replacements") or {})
    return cleaned


def log_dictation(raw: str, corrected: str, source: str = "desktop",
                  log_path: pathlib.Path | None = None) -> pathlib.Path:
    """Append one dictation record (no audio stored) for passive self-learning."""
    target = log_path or (state_dir() / "dictations.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": round(time.time(), 3), "raw": raw, "corrected": corrected, "source": source}
    with target.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return target
