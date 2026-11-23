from _typeshed import Incomplete
from pathlib import Path

WORKSPACE_ROOT: Incomplete
OPENER: Incomplete
REDIRECT: Incomplete
TEE: Incomplete
STDIN_DASH: Incomplete
WRITE_VERB: Incomplete
QUOTED: Incomplete
SED_INPLACE: Incomplete
INLINE: Incomplete
QUOTES: Incomplete

def targets(line: str) -> list: ...
def body_writes(body: str, cwd: str) -> list: ...
def in_workspace(target: str, cwd: str) -> Path | None: ...
def candidates(command: str, cwd: str, every_line: bool = False) -> list: ...
def written_paths(command: str, cwd: str) -> list: ...
def main() -> int: ...
