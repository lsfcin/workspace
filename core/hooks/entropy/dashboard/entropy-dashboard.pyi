from _typeshed import Incomplete
from pathlib import Path

REPORT: Incomplete
LEDGERS: Incomplete

def collect(files: list, repo: Path = ..., promoting: str = '') -> dict: ...
def main(argv: list | None = None) -> int: ...
