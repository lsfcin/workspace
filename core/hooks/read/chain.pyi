from _typeshed import Incomplete
from pathlib import Path

EXEMPT_NAMES: Incomplete
SKIP_PARTS: Incomplete
TOKEN_RE: Incomplete

def context_chain(target: Path) -> list[Path]: ...
def paths_in(text: str, cwd: str, files_only: bool = False) -> set[Path]: ...
def summary_of(ctx: Path) -> str: ...
