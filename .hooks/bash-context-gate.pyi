from _typeshed import Incomplete
from pathlib import Path

WORKSPACE: Incomplete
EXEMPT_NAMES: Incomplete
SKIP_PARTS: Incomplete
TOKEN_RE: Incomplete

def candidates(command: str, cwd: str) -> set[Path]: ...
def context_chain(target: Path) -> list[Path]: ...
def main() -> int: ...
