# test_video_core.py — T0/T1 unit tests for video_core (no network; fixtures + injected runners)
import pathlib, shutil, subprocess, sys
import pytest
import video_core as vc

FIX = pathlib.Path(__file__).parent / "fixtures"


class FakeProc:
    def __init__(self, stdout="", stderr=""):
        self.stdout, self.stderr = stdout, stderr


class FakeMedia:
    """Stand-in for video_media — records calls, returns canned text."""
    def __init__(self, spoken="", screen=""):
        self.spoken, self.screen, self.calls = spoken, screen, []

    def download_audio(self, url):
        self.calls.append("dl_audio")
        return "a.m4a" if self.spoken else None

    def transcribe(self, path):
        return self.spoken

    def download_video(self, url):
        self.calls.append("dl_video")
        return "v.mp4" if self.screen else None

    def ocr_frames(self, path):
        return self.screen


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
    assert "captions" in b["method"]
    assert "spoken words" in b["text"] and "desc" in b["text"]


def test_assemble_speech_forced():
    meta = {"ok": True, "title": "T", "uploader": "U",
            "description": "", "subtitles": [], "auto_captions": []}
    fm = FakeMedia(spoken="the spoken line")
    b = vc.assemble("http://x", level="speech", _probe=lambda u: meta, _media=fm)
    assert "speech" in b["method"]
    assert "the spoken line" in b["text"]


def test_assemble_auto_escalates_to_speech_then_ocr():
    meta = {"ok": True, "title": "T", "uploader": "U",
            "description": "", "subtitles": [], "auto_captions": []}
    fm = FakeMedia(spoken="", screen="text on the screen")
    b = vc.assemble("http://x", _probe=lambda u: meta, _media=fm)
    assert fm.calls == ["dl_audio", "dl_video"]  # tried speech, empty, escalated to ocr
    assert "ocr" in b["method"] and "text on the screen" in b["text"]


def test_assemble_auto_skips_heavy_when_metadata_suffices():
    meta = {"ok": True, "title": "T", "uploader": "U",
            "description": "already enough", "subtitles": [], "auto_captions": []}
    fm = FakeMedia(spoken="nope")
    b = vc.assemble("http://x", _probe=lambda u: meta, _media=fm)
    assert fm.calls == []  # no download when L0 already has text
    assert b["method"] == "metadata"


def test_transcribe_joins_segments():
    import video_media as vm

    class Seg:
        def __init__(self, t):
            self.text = t

    class FakeModel:
        def transcribe(self, path, language=None):
            return ([Seg(" hi "), Seg("there")], None)

    assert vm.transcribe("x", _model=FakeModel()) == "hi there"


@pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract not installed")
def test_ocr_image_reads_fixture():
    import video_media as vm
    assert "HELLO OCR" in vm.ocr_image(FIX / "text_on_image.png", lang="eng")


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
