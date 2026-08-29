from _typeshed import Incomplete
from pathlib import Path

FACADE_NAMES: Incomplete
FACADE_EXTS: Incomplete
TEST_RE: Incomplete

def facades_read(session_id: str) -> set[str]: ...
def find_nearest_facade(path: Path) -> Path | None: ...
def main() -> int: ...
