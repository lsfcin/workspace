#!/usr/bin/env python3
# Which repos the Git Flow convention covers. The answer is core/hooks/gitflow.txt; this only reads it.
#
# The branch gate, the branch marker and the session close all ask here, so the repo a commit is
# blocked in is the repo a close promotes. They used to hold two copies of the scope — the gate any
# depth under code/, the close only a direct child — and a repo outside both was skipped in silence.
from pathlib import Path, PurePosixPath

DECLARED = Path(__file__).resolve().parent / 'gitflow.txt'


def scope() -> list:
    """The declared patterns, comments and blank lines dropped."""
    lines = DECLARED.read_text(encoding='utf-8').splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith('#')]


def enforced(toplevel, root) -> bool:
    """Whether the repo at `toplevel` is covered, judged relative to the workspace at `root`."""
    try:
        rel = PurePosixPath(Path(toplevel).resolve().relative_to(Path(root).resolve()).as_posix())
    except ValueError:
        return False
    return any(rel.full_match(pattern) for pattern in scope())
