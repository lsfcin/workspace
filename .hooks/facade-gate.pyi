from _typeshed import Incomplete
from pathlib import Path

WORKSPACE: Incomplete
FACADE_NAMES: Incomplete
CODE_EXTS: Incomplete
TEST_RE: Incomplete

def get_session_id() -> str: ...
def facades_read() -> set[str]: ...
def find_nearest_facade(path: Path) -> Path | None: ...

data: Incomplete
tool: Incomplete
file_path: Incomplete
facade: Incomplete
rel_f: Incomplete
rel_p: Incomplete
