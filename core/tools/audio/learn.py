# Passive STT self-learning from dictated text vs sent agent user prompts
from __future__ import annotations

import datetime as dt
import difflib
import json
import os
import pathlib
import re
import sys

_HERE = pathlib.Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import refine  # noqa: E402

_STOPWORDS = frozenset({
    "para", "com", "que", "uma", "uns", "umas", "por", "dos", "das", "nos", "nas",
    "como", "mais", "mas", "isso", "isto", "esse", "essa", "este", "esta", "aqui",
    "ali", "tem", "ter", "fazer", "pode", "vou", "vai", "então", "porque", "sobre",
})


def _parse_iso_ts(value: str | int | float | None) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [c.get("text", "") for c in content
                 if isinstance(c, dict) and c.get("type") in ("text", "input_text")]
        return " ".join(p.strip() for p in parts if p.strip())
    return ""


def _default_transcript_roots() -> list[pathlib.Path]:
    home = pathlib.Path.home()
    return [
        home / ".claude" / "projects",
        home / ".codex" / "sessions",
        home / ".gemini" / "antigravity-cli" / "brain",
    ]


def _messages_from_file(path: pathlib.Path) -> list[tuple[float, str]]:
    out: list[tuple[float, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return out
    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        ts = _parse_iso_ts(obj.get("timestamp") or obj.get("ts"))
        text = ""
        if obj.get("type") == "user" and isinstance(obj.get("message"), dict):
            text = _extract_text(obj["message"].get("content"))
        elif obj.get("role") == "user":
            text = _extract_text(obj.get("content") or obj.get("text"))
        elif isinstance(obj.get("payload"), dict):
            p = obj["payload"]
            if p.get("role") == "user" or p.get("type") == "user_message":
                text = _extract_text(p.get("content") or p.get("message") or p.get("text"))
        if ts is not None and text:
            out.append((ts, text))
    return out


def collect_user_messages(roots: list[pathlib.Path] | None = None,
                          max_age_days: float = 14.0) -> list[tuple[float, str]]:
    """Collect (timestamp, text) user messages from recent local agent transcripts."""
    cutoff = dt.datetime.now().timestamp() - max_age_days * 86400.0
    msgs: list[tuple[float, str]] = []
    for root in (roots if roots is not None else _default_transcript_roots()):
        if not root.exists():
            continue
        for jsonl in root.rglob("*.jsonl"):
            try:
                if jsonl.stat().st_mtime < cutoff:
                    continue
            except OSError:
                continue
            msgs.extend(_messages_from_file(jsonl))
    msgs.sort(key=lambda item: item[0])
    return msgs


def _tokens(text: str) -> list[str]:
    return re.findall(r"[^\W\d_][\w-]*", text, re.UNICODE)


def diff_token_pairs(dictated: str, sent: str) -> list[tuple[str, str]]:
    """Return conservative 1-to-1 word correction pairs when sent resembles dictated."""
    d_norm, s_norm = dictated.strip(), sent.strip()
    if not d_norm or not s_norm:
        return []
    sim = difflib.SequenceMatcher(None, d_norm.lower(), s_norm.lower()).ratio()
    if sim < 0.65 or sim >= 1.0:
        return []
    d_tok, s_tok = _tokens(d_norm), _tokens(s_norm)
    pairs: list[tuple[str, str]] = []
    sm = difflib.SequenceMatcher(None, [t.lower() for t in d_tok], [t.lower() for t in s_tok])
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "replace" or (i2 - i1) != 1 or (j2 - j1) != 1:
            continue
        wrong, right = d_tok[i1].lower(), s_tok[j1]
        r_low = right.lower()
        if wrong == r_low or len(wrong) < 3 or len(r_low) < 3:
            continue
        if wrong in _STOPWORDS or r_low in _STOPWORDS:
            continue
        if difflib.SequenceMatcher(None, wrong, r_low).ratio() < 0.45:
            continue
        pairs.append((wrong, right))
    return pairs


def run(state_dir: pathlib.Path | None = None, manual_vocab_path: pathlib.Path | None = None,
        transcript_roots: list[pathlib.Path] | None = None, window_seconds: float = 180.0,
        min_count: int = 2) -> dict:
    """Update learned.json idempotently from dictations.jsonl and recent agent prompts."""
    sdir = state_dir or refine.state_dir()
    log_path = sdir / "dictations.jsonl"
    learned_path = sdir / "learned.json"
    manual_only = (json.loads((manual_vocab_path or (_HERE / "vocab.json")).read_text(encoding="utf-8"))
                   if (manual_vocab_path or (_HERE / "vocab.json")).is_file() else {})
    manual_keys = {k.lower() for k in (manual_only.get("replacements") or {})}

    state = (json.loads(learned_path.read_text(encoding="utf-8"))
             if learned_path.is_file() else {"counts": {}, "replacements": {}, "terms": [], "last_ts": 0.0})
    counts: dict[str, dict[str, int]] = state.get("counts") or {}
    last_ts = float(state.get("last_ts") or 0.0)
    max_ts = last_ts

    if not log_path.is_file():
        return {"processed": 0, "promoted": 0, "replacements": state.get("replacements") or {}}

    msgs = collect_user_messages(transcript_roots)
    processed = 0
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        d_ts = float(row.get("ts") or 0.0)
        if d_ts <= last_ts:
            continue
        max_ts = max(max_ts, d_ts)
        dictated = str(row.get("corrected") or row.get("raw") or "")
        best_msg, best_ratio = "", 0.0
        for m_ts, m_text in msgs:
            delta = m_ts - d_ts
            if 0.0 <= delta <= window_seconds:
                r = difflib.SequenceMatcher(None, dictated.lower(), m_text.lower()).ratio()
                if r > best_ratio:
                    best_ratio, best_msg = r, m_text
        if best_msg:
            for wrong, right in diff_token_pairs(dictated, best_msg):
                bucket = counts.setdefault(wrong, {})
                bucket[right] = int(bucket.get(right, 0)) + 1
            processed += 1

    promoted: dict[str, str] = {}
    term_scores: dict[str, int] = {}
    for wrong, targets in counts.items():
        if wrong in manual_keys or not targets:
            continue
        ranked = sorted(targets.items(), key=lambda kv: kv[1], reverse=True)
        top_word, top_n = ranked[0]
        second_n = ranked[1][1] if len(ranked) > 1 else 0
        if top_n >= min_count and (second_n == 0 or top_n >= 2 * second_n):
            promoted[wrong] = top_word
            term_scores[top_word] = term_scores.get(top_word, 0) + top_n

    terms = [w for w, _ in sorted(term_scores.items(), key=lambda kv: kv[1], reverse=True)][:15]
    out = {"counts": counts, "replacements": promoted, "terms": terms, "last_ts": max_ts}
    sdir.mkdir(parents=True, exist_ok=True)
    tmp = learned_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, learned_path)
    return {"processed": processed, "promoted": len(promoted), "replacements": promoted, "terms": terms}
