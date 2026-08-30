# diagram
> The workspace drawn from its own declarations: one generated HTML picture, zero tokens, no model.

`architecture` writes [`ARCHITECTURE.html`](../../../../ARCHITECTURE.html) at the workspace root.
Everything above the tab strip answers *is it well tied, what is loose*; the tabs hold the detail
that answers *where exactly*. Every view reads a source that already exists:

| View | Renders | Read from |
|------|---------|-----------|
| summary | each declared layer against how hard it pushes, plus the findings and their targets | [`core/features.txt`](../../../features.txt) |
| lifecycle | which features fire at which moment of a session, in order | the hook registrations, via [`core/hooks/trigger/`](../../../hooks/trigger/CONTEXT.md) |
| fan-in | how many features one switch point carries | [`core/features.txt`](../../../features.txt) § wired |
| enforcement | every feature against every site that enforces it | [`core/features.txt`](../../../features.txt) |
| routing | the chain an agent walks, three levels deep | the generated routing blocks |
| mass | tracked bytes per directory | `git ls-files` |

**A hand-drawn map is the rot the routing tables exist to prevent**, so nothing here is drawn by
hand and no model runs at render time. The picture can be no more wrong than its sources: a wrong
edge means a wrong routing table, and fixing the drawing means fixing the source. **Nothing on the
page is inferred, as of 2026-08-18** — *when a hook fires* was the last exception, guessed from
directory convention until [`trigger_law.py`](../../../hooks/trigger/trigger_law.py) started reading
it out of the registrations. What the registrations cannot place is counted as a gap rather than
guessed at.

Total and fail-loud: every run prints `parsed N of M routing blocks`, and a block it cannot slice
is named rather than skipped — a picture that quietly drops a subtree is worse than no picture.

```
core/run tools/wos/diagram/architecture              # regenerate ARCHITECTURE.html
core/run tools/wos/diagram/architecture --check      # exit 1 if the committed file is stale
core/run tools/wos/diagram/architecture --out /tmp/x.html
core/run tools/wos/diagram/architecture --repos      # one picture per code repo, into its own root
```

**Every code repo carries its own document too** (ruled 2026-08-20), and building it named the first
real difference between the two kinds of picture. It shared a scope line with `ISSUES.md` until the
entropy scatter generalised to every nested repo (2026-08-25) and this did not follow — `--repos`
still walks `code/` alone. Left as an asymmetry rather than closed in passing: a repo's page needs
declarations a paper repo does not have, so widening it is a question, not a loop bound.
Only *routing* and *mass* transferred — both already took a root argument. The other four drawings
read [`core/features.txt`](../../../features.txt) and the hook registrations, which exist once, for
the enforcement layer. So **the workspace's picture is about what fires and what is wired; a repo's
is about what it is made of**, and a repo's health band reads its own `ISSUES.md` rather than
recounting anything. That boundary is stated in each page's own footer and pinned by
[`test_diagram_repo.py`](../../test/wos/diagram/test_diagram_repo.py).

`/roundup` regenerates and commits it at every session close, which is what keeps a stale picture a
bug in the close rather than a fact of life. Output determinism is load-bearing for that: no
timestamp, no commit sha, so the file changes only when the workspace did.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`views/`](views/CONTEXT.md) | One drawing per file. A view renders data it is handed and computes nothing about the workspace. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`architecture`](architecture) | — | — | draw the workspace as it is (enforcement matrix, routing spine, folder mass) into one self-contained ARCHITECTURE.html; --repos draws every code repo into its own; --check exits 1 when a committed file is stale |
| [`diagram_data.py`](diagram_data.py) | [`diagram_data.pyi`](diagram_data.pyi) | `area_of`, `trigger_of`, `lifecycle`, `features`, `matrix` | The canonical data behind ARCHITECTURE.html: what the workspace declares, what contains what, and how much of it there is. |
| [`diagram_footer.py`](diagram_footer.py) | [`diagram_footer.pyi`](diagram_footer.pyi) | `render` | The page's honesty block: what this picture covered, what it inferred, and where to change it. |
| [`diagram_health.py`](diagram_health.py) | [`diagram_health.pyi`](diagram_health.pyi) | `harness_owned`, `orphans`, `by_layer`, `findings`, `detail` | What the workspace's declarations say about its HEALTH, as opposed to its contents. |
| [`diagram_page.py`](diagram_page.py) | [`diagram_page.pyi`](diagram_page.pyi) | `render` | The page the three drawings live in: one self-contained HTML file, no script, no asset it does not carry. It opens from a file:// path on a machine with no network and under any provider, which is what "an asset inside the workspace" has to mean to be worth committing. |
| [`diagram_repo.py`](diagram_repo.py) | [`diagram_repo.pyi`](diagram_repo.pyi) | `findings`, `health`, `build` | A code repo drawn from its own declarations — the same page shell as the workspace's, holding only the drawings a repo actually has a source for. |
<!-- routing:end -->
