# test_video_core.py — T0/T1 unit tests for video_core (no network; fixtures + injected runners)
import pathlib, subprocess, sys
import video_core as vc

FIX = pathlib.Path(__file__).parent / "fixtures"


class FakeProc:
    def __init__(self, stdout="", stderr=""):
        self.stdout, self.stderr = stdout, stderr


def test_probe_parses_dump():
    dump = (FIX / "ytdlp_dump.json").read_text()
    meta = vc.probe("http://x", runner=lambda a: FakeProc(stdout=dump))
    assert meta["ok"]
    assert meta["title"] == "Test Clip"
    assert meta["uploader"] == "Chan"
    assert "en" in meta["auto_captions"]


def test_probe_failure_no_crash():
    meta = vc.probe("http://x", runner=lambda a: FakeProc(stderr="ERROR: login required"))
    assert meta["ok"] is False
    assert "login" in meta["error"]


def test_clean_vtt():
    assert vc.clean_vtt((FIX / "sample.vtt").read_text()) == "Hello world\nthis is a test"


def test_assemble_stops_at_metadata():
    meta = {"ok": True, "title": "T", "uploader": "U",
            "description": "a flower shop in 3D", "subtitles": [], "auto_captions": []}

    def boom(url):
        raise AssertionError("captions must not be fetched when none advertised")

    b = vc.assemble("http://x", _probe=lambda u: meta, _captions=boom)
    assert b["method"] == "metadata"
    assert "flower shop" in b["text"]


def test_assemble_uses_captions():
    meta = {"ok": True, "title": "T", "uploader": "U",
            "description": "desc", "subtitles": [], "auto_captions": ["en"]}
    b = vc.assemble("http://x", _probe=lambda u: meta, _captions=lambda u: "spoken words")
    assert b["method"] == "captions"
    assert "spoken words" in b["text"] and "desc" in b["text"]


def test_source_of():
    assert vc.source_of("https://instagram.com/reel/x") == "instagram"
    assert vc.source_of("https://youtu.be/x") == "youtube"
    assert vc.source_of("https://example.com/v") == "web"


def test_save_no_overwrite(tmp_path):
    meta = {"ok": True, "title": "My Clip", "uploader": "U",
            "description": "body", "subtitles": [], "auto_captions": []}
    b1 = vc.assemble("http://x", save=True, base=tmp_path, _probe=lambda u: meta)
    b2 = vc.assemble("http://x", save=True, base=tmp_path, _probe=lambda u: meta)
    p1, p2 = pathlib.Path(b1["saved_path"]), pathlib.Path(b2["saved_path"])
    assert p1.exists() and p2.exists() and p1 != p2
    assert "body" in p1.read_text()


def test_cli_usage_exits_1():
    cli = pathlib.Path(vc.__file__).with_name("video")
    r = subprocess.run([sys.executable, str(cli)], capture_output=True, text=True)
    assert r.returncode == 1
    assert "Usage" in r.stderr
