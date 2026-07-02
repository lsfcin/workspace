from _typeshed import Incomplete
from pathlib import Path

WORKSPACE: Incomplete
GATED_TOOLS: Incomplete
EXEMPT_NAMES: Incomplete
SKIP_PARTS: Incomplete

def target_path(tool: str, tool_input: dict) -> str: ...
def context_chain(target: Path) -> list[Path]: ...
def main() -> int: ...
