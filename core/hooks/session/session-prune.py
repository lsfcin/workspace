#!/usr/bin/env python3
# SessionStart — delete session marker stores older than 2 days, and temp folders a dead run left behind. See code/ROADMAP-verify.md W1.
#
# THIS HOOK IS NOW LOAD-BEARING, not hygiene. The stores moved out of the temp directory into the
# repository on 2026-09-22, because a session outlives a reboot and a temp directory does not. The
# operating system used to empty them; nothing does now but this. If it stops running, the stores
# accumulate under core/state/ forever — which is the cost that buys a marker surviving the night.
#
# A SECOND SPELLING OF A PATH ANOTHER MODULE OWNS is the defect this was ported to remove, and it
# outranks any question about which directory is which: where state and scratch live is asked of
# platform_law, never restated here.
#
# THE STORE LIST IS HAND-MAINTAINED, and that is a known cost: a new kind leaks until someone adds
# it here (five had, 1,600 files, b20261127). The temp directory gets a RULE instead, because what
# leaks there is named by whoever ran mktemp (tools, the suite, agents' shells, browsers): this
# user's, a day untouched, and holding no socket — a live tmux, ssh-agent or editor keeps one.
#
# WHY THE TEMP DIRECTORY TOO. It is tmpfs on this machine, so what a killed run leaves there is RAM,
# and the operating system ages it at 10 days: 4 GB of leaks starved every worker (2026-11-27).
import os
import shutil
import stat
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from platform_law import scratch_root, session_state, system_temp  # noqa: E402

MAX_AGE_SECONDS = 2 * 24 * 60 * 60
SCRATCH_AGE_SECONDS = 24 * 60 * 60
STORES = ('claude_ctx_seen_*', 'claude_iface_seen_*', 'claude_facades_*', 'claude_cg_reminded_*',
          'claude_nostub_*', 'claude_branch_*', 'claude_ctx_meter_*', 'claude_agent_ctx_*',
          'claude_ctx_compacted_*', 'claude_web_retry_*', 'claude_rtk_compact_*', 'dirt_before_*',
          'turn_*')


def stale(now: float, path: Path, age: float = MAX_AGE_SECONDS) -> bool:
	"""Untouched for `age`, by the newest mtime of the path and what sits directly in it — a folder
	whose run is still writing a file inside is not stale. Never raises on a path that vanished
	mid-scan: a live session writes while this runs, and missing is not stale."""
	try:
		newest = path.stat().st_mtime
		if path.is_dir() and not path.is_symlink():
			newest = max([newest, *(child.lstat().st_mtime for child in path.iterdir())])
		return now - newest > age
	except OSError:
		return False


def _drop(path: Path) -> None:
	try:
		if path.is_dir() and not path.is_symlink():
			shutil.rmtree(path, ignore_errors=True)
		else:
			path.unlink()
	except OSError:
		pass


def _in_use(path: Path) -> bool:
	"""A socket at the path or directly in it: something alive is listening there. Unreadable counts."""
	try:
		if stat.S_ISSOCK(path.lstat().st_mode):
			return True
		return path.is_dir() and any(stat.S_ISSOCK(c.lstat().st_mode) for c in path.iterdir())
	except OSError:
		return True


def leftovers(temp: Path, uid: int) -> list:
	"""Temp entries of this user that nothing listens on: the top level, pytest's numbered folders
	(their parent is touched every run), and each Claude session's scratchpad (claude-<uid>/<p>/<s>)."""
	found = [*temp.iterdir(), *temp.glob('pytest-of-*/pytest-[0-9]*'), *temp.glob(f'claude-{uid}/*/*')]
	mine = []
	for path in found:
		try:
			if path.lstat().st_uid == uid and not path.is_symlink() and not _in_use(path):
				mine.append(path)
		except OSError:
			continue
	return mine


def sweep(now: float, temp: Path = None) -> None:
	"""Scratch folders older than a day, wherever platform_law put them, and our temp leftovers."""
	uid = os.getuid() if hasattr(os, 'getuid') else -1
	roots = {scratch_root(), scratch_root(tree=True)}
	candidates = [child for root in roots for child in root.iterdir()]
	candidates += leftovers(Path(temp or system_temp()), uid)
	for path in candidates:
		if stale(now, path, SCRATCH_AGE_SECONDS):
			_drop(path)


def main() -> int:
	"""Never blocks. A SessionStart hook that raises is a traceback where the session belonged."""
	# The parent of a store, never a spelled path: session_state answers where these live, and the
	# argument is discarded. Asking it is what makes this hook find the stores on both systems.
	state_dir = session_state('any').parent
	now = time.time()
	for pattern in STORES:
		for store in state_dir.glob(pattern):
			if stale(now, store):
				_drop(store)
	try:
		sweep(now)
	except OSError:
		pass
	return 0


if __name__ == '__main__':
	sys.exit(main())
