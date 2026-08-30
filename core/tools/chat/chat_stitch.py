# chat_stitch.py — a chat export becomes one readable conversation: every "audio attached" line
# gains what was actually said underneath, bot menus that repeat verbatim go, and secrets are redacted.
from __future__ import annotations
import sys, pathlib, re

ATTACHED = re.compile(r"‎?([\w.\- ]+\.opus) \(arquivo anexado\)")
# A chat robot re-sends the same greeting and menu on every inbound message. Four copies of a menu
# is not conversation, and it buries the two lines a human actually typed.
BOT_NOISE = ("Agora escolha uma das opções abaixo", "*[ 1 ]* - *Orçamento*",
             "Seja bem-vindo(a) ao Cartório", "Opção inválida.",
             "Ajude-nos a melhorar a prestação de nossos serviços")


def transcript_for(audio_name: str, media: pathlib.Path) -> str | None:
    side = media / f"{audio_name}.txt"
    return side.read_text(encoding="utf-8").strip() if side.exists() else None


def fold(line: str, media: pathlib.Path) -> list[str]:
    """One export line -> the lines it becomes. An audio keeps its original line (the timestamp and
    speaker live there) and gains an indented transcript below it."""
    hit = ATTACHED.search(line)
    if not hit:
        return [line]
    said = transcript_for(hit.group(1), media)
    return [line] if said is None else [line, f"    ↳ {said}"]


def is_noise(line: str) -> bool:
    return any(marker in line for marker in BOT_NOISE)


# core/norms/secrets.md: the versioned text carries the label, never the value.
#
# A bare 11-digit run is NOT enough to call something a CPF — a Brazilian mobile with area code is
# eleven digits too. So bare digits are redacted only near a line that says CPF; a punctuated one
# is unambiguous and goes anywhere.
FORMATTED_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
BARE_CPF = re.compile(r"\b\d{11}\b")
PASSWORD = re.compile(r"(?i)(senha\W{0,3})\d{6,}")
CPF_LABEL = "‹CPF em segredos.env›"


# How many lines a mention of "CPF" keeps colouring. In chat the number arrives a turn or two after
# the request — "Me informa o seu CPF" / "o meu é ..." — so a line-local test misses the real case.
CPF_WINDOW = 3


def redact_line(line: str, in_cpf_context: bool) -> str:
    out = PASSWORD.sub(r"\1‹em segredos.env›", FORMATTED_CPF.sub(CPF_LABEL, line))
    return BARE_CPF.sub(CPF_LABEL, out) if in_cpf_context else out


def redact(text: str) -> str:
    out, countdown = [], 0
    for line in text.split("\n"):
        if "cpf" in line.lower():
            countdown = CPF_WINDOW
        out.append(redact_line(line, countdown > 0))
        countdown -= 1
    return "\n".join(out)


def stitch(export: pathlib.Path, media: pathlib.Path) -> str:
    out: list[str] = []
    for line in export.read_text(encoding="utf-8").split("\n"):
        if not is_noise(line):
            out.extend(fold(line, media))
    return redact("\n".join(out))


DATE = re.compile(r"^(\d{2}/\d{2}/\d{4})")


def span(text: str) -> tuple[str, str]:
    """First and last dates in the export — the header says what period the file covers."""
    dates = [m.group(1) for m in (DATE.match(l) for l in text.split("\n")) if m]
    return (dates[0], dates[-1]) if dates else ("?", "?")


def header(who: str, text: str, audios: int) -> str:
    """The first-line description every text file in this workspace owes its routing table."""
    first, last = span(text)
    return f"# Conversa com {who} — {first} a {last}, {audios} áudios transcritos inline."


def run(export: pathlib.Path, out: pathlib.Path, who: str | None = None) -> int:
    text = stitch(export, export.parent)
    count = text.count("    ↳ ")
    name = who or out.stem
    out.write_text(f"{header(name, text, count)}\n\n{text}", encoding="utf-8")
    return count


if __name__ == "__main__":
    print(run(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])), "áudios costurados")
