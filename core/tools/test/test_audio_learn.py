# T1 audio self-learning: temporal correlation, conservative promotion, manual priority
from __future__ import annotations

import json


def _write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8", newline="\n")


def test_learn_promotes_repeated_corrections_and_is_idempotent(tmp_path):
    import learn
    state_dir = tmp_path / "state"
    manual = tmp_path / "vocab.json"
    manual.write_text(json.dumps({"replacements": {"cloud": "claude"}}), encoding="utf-8", newline="\n")
    t0 = 1_700_000_000.0

    _write_jsonl(state_dir / "dictations.jsonl", [
        {"ts": t0, "raw": "faz o rondape agora", "corrected": "faz o rondape agora", "source": "desktop"},
        {"ts": t0 + 100, "raw": "manda o rondape hoje", "corrected": "manda o rondape hoje", "source": "desktop"},
        {"ts": t0 + 200, "raw": "abre o pitxis aqui", "corrected": "abre o pitxis aqui", "source": "desktop"},
        {"ts": t0 + 300, "raw": "cloud faz o teste", "corrected": "cloud faz o teste", "source": "desktop"},
        {"ts": t0 + 400, "raw": "frase totalmente diferente sem relacao", "corrected": "frase totalmente diferente sem relacao", "source": "desktop"},
    ])

    claude_dir = tmp_path / "claude_proj"
    _write_jsonl(claude_dir / "sess.jsonl", [
        {"type": "user", "timestamp": t0 + 10, "message": {"content": "faz o roundup agora"}},
        {"type": "user", "timestamp": t0 + 115, "message": {"content": "manda o roundup hoje"}},
        {"type": "user", "timestamp": t0 + 215, "message": {"content": "abre o ptyxis aqui"}},
        {"type": "user", "timestamp": t0 + 310, "message": {"content": "claude faz o teste"}},
        {"type": "user", "timestamp": t0 + 410, "message": {"content": "outra conversa nada a ver"}},
    ])

    first = learn.run(state_dir=state_dir, manual_vocab_path=manual, transcript_roots=[claude_dir])
    assert first["replacements"] == {"rondape": "roundup"}
    assert "pitxis" not in first["replacements"]
    assert "cloud" not in first["replacements"]
    assert "roundup" in first["terms"]

    second = learn.run(state_dir=state_dir, manual_vocab_path=manual, transcript_roots=[claude_dir])
    assert second["processed"] == 0
    assert second["replacements"] == {"rondape": "roundup"}


def test_learn_ignores_ambiguous_or_distant_matches(tmp_path):
    import learn
    state_dir = tmp_path / "state"
    manual = tmp_path / "vocab.json"
    manual.write_text(json.dumps({"replacements": {}}), encoding="utf-8", newline="\n")
    t0 = 1_700_000_000.0

    _write_jsonl(state_dir / "dictations.jsonl", [
        {"ts": t0, "raw": "roda o fooo agora", "corrected": "roda o fooo agora", "source": "desktop"},
        {"ts": t0 + 10, "raw": "roda o fooo agora", "corrected": "roda o fooo agora", "source": "desktop"},
        {"ts": t0 + 20, "raw": "abre o bazz depois", "corrected": "abre o bazz depois", "source": "desktop"},
        {"ts": t0 + 30, "raw": "abre o bazz depois", "corrected": "abre o bazz depois", "source": "desktop"},
    ])

    codex_dir = tmp_path / "codex_sess"
    _write_jsonl(codex_dir / "rollout.jsonl", [
        {"timestamp": t0 + 2, "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "roda o fooo1 agora"}]}},
        {"timestamp": t0 + 12, "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "roda o fooo2 agora"}]}},
        {"timestamp": t0 + 250, "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "abre o bazzz depois"}]}},
    ])

    res = learn.run(state_dir=state_dir, manual_vocab_path=manual, transcript_roots=[codex_dir], window_seconds=180.0)
    assert res["replacements"] == {}


def test_learn_antigravity_phrases_skips_chunks_and_early_exits(tmp_path, monkeypatch):
    import learn
    state_dir = tmp_path / "state"
    manual = tmp_path / "vocab.json"
    manual.write_text(json.dumps({"replacements": {}}), encoding="utf-8", newline="\n")
    t0 = 1_700_000_000.0

    _write_jsonl(state_dir / "dictations.jsonl", [
        {"ts": t0, "raw": "aperta o auto t no multigravity iy agora", "corrected": "aperta o auto t no multigravity iy agora"},
        {"ts": t0 + 100, "raw": "manda o auto t no multigravity iy hoje", "corrected": "manda o auto t no multigravity iy hoje"},
    ])

    agy_root = tmp_path / ".gemini" / "antigravity-cli" / "brain"
    conv_logs = agy_root / "conv1" / ".system_generated" / "logs"
    rows = [
        {"type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": t0 + 5,
         "content": "<USER_REQUEST>\naperta o Alt+T no Antigravity IDE agora\n</USER_REQUEST>"},
        {"type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": t0 + 105,
         "content": "<USER_REQUEST>\nmanda o Alt+T no Antigravity IDE hoje\n</USER_REQUEST>"},
    ]
    _write_jsonl(conv_logs / "transcript.jsonl", rows)
    _write_jsonl(conv_logs / "transcript_full.jsonl", rows)
    _write_jsonl(conv_logs / "chunks" / "transcript" / "00000000.jsonl", rows)

    res = learn.run(state_dir=state_dir, manual_vocab_path=manual, transcript_roots=[agy_root])
    assert res["processed"] == 2
    assert res["replacements"]["auto t"] == "Alt+T"
    assert res["replacements"]["multigravity iy"] == "Antigravity IDE"

    # Early exit: when no new dictations exist after last_ts, transcript scan is skipped completely.
    monkeypatch.setattr(learn, "collect_user_messages", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("should not scan")))
    again = learn.run(state_dir=state_dir, manual_vocab_path=manual, transcript_roots=[agy_root])
    assert again["processed"] == 0
    assert again["replacements"] == res["replacements"]
