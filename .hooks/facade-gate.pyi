from _typeshed import Incomplete
from pathlib import Path

WORKSPACE: Incomplete
FACADE_NAMES: Incomplete
CODE_EXTS: Incomplete
TEST_RE: Incomplete

def facades_read(session_id: str) -> set[str]: ...
def find_nearest_facade(path: Path) -> Path | None: ...
def main() -> int: ...
