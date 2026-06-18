from pathlib import Path
from workspace_scanner import has_code_content as has_code_content

RS: str
RE: str

def migrate_legacy(text: str) -> tuple[str, bool]: ...
def sync(target: Path): ...
