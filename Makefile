# Workspace verification contract — see core/tools/verify/CONTEXT.md.
# The global pre-commit gate (.hooks/pre-commit § 1a) discovers `verify-fast:` by
# convention and blocks the commit if it is red. Keep it under ~5s: it runs on every
# commit that stages a .py/.ts/.js/.dart file anywhere in the workspace repo.

PYTEST := .venv/bin/pytest

.PHONY: verify-fast verify-full

# T0 static + T1 unit. No network, no model downloads, no browser.
verify-fast:
	@bash -n .hooks/*.sh
	@$(PYTEST) core/tools/test/ -m "not network" -q

# T2: adds the network-marked tests (live yt-dlp against real URLs — needs cookies
# for the Instagram cases, see core/tools/video.SETUP.md).
verify-full:
	@bash -n .hooks/*.sh
	@$(PYTEST) core/tools/test/ -q
