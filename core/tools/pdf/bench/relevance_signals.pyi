import pdf_relevance
from _typeshed import Incomplete
from pathlib import Path

DESCRIBED: Incomplete
COLUMNS: Incomplete

def described(twin: Path) -> dict[str, tuple[str, str]]: ...
def rows(pdf: Path, img_dir: Path, prof: pdf_relevance.Profile | None = None) -> list[dict]: ...
def main() -> int: ...
