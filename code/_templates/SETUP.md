# [Project Name] — Dev Setup
> Everything needed to run this project locally from scratch.

<!-- What: dev environment only — getting a new machine from zero to running.
     Not here: what the project does (→README.md), architecture decisions (→SPECS.md).
     Be specific about versions. Assume nothing is pre-installed. -->

## Prerequisites
<!-- Runtime versions, system tools, and external accounts required.
     Example: "Python 3.11+", "Node 20+", "ffmpeg in PATH", "GEMINI_API_KEY". -->

## Install
<!-- Step-by-step from a clean checkout. Include the package install command. -->

```bash
# example
pip install -r requirements.txt
```

## Environment Variables
<!-- All env vars the project reads. Mark which are required vs optional. -->

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `VAR_NAME` | yes / no | — | ... |

## Build
<!-- How to compile, bundle, or generate assets before running.
     Skip this section entirely if the project needs no build step. -->

```bash
# example
npm run build
```

## Run
<!-- Exact command to start the dev server, CLI, or app. -->

```bash
# example
python start.py
```

## Test
<!-- Command to run the test suite. Include useful flags (verbose, filter, coverage). -->

```bash
# example
python -m pytest
```

## Verification Contract
<!-- Required for all code projects — see workspace VERIFY.md + core/tools/verify/CONTEXT.md.
     verify:fast (static + unit, seconds) is enforced by the global pre-commit gate: red blocks commits.
     verify:full (headless functional + goldens) runs pre-merge and at /handoff.
     Regression specs: test/**/b<N>-*.* — KNOWN-BUGS.md FIXED flips are hook-gated on these. -->

```bash
npm run verify:fast   # or make verify-fast
npm run verify:full   # or make verify-full
```

## Release
<!-- Optional. How to cut a release, create a tag, or deploy.
     Link to CI config if the process is automated. -->
