# links
> A link gets a name a room can be told out loud. Provider leaf: `cfpages` (Cloudflare Pages).

```bash
core/run tools/links/cfpages add ai4good/setup <url>   # mint a slug
core/run tools/links/cfpages find ai4                  # query the map — never read it whole
core/run tools/links/cfpages rm ai4good/setup
core/run tools/links/cfpages build --push              # regenerate _redirects and deploy
core/run tools/links/cfpages check                     # what is untrue about the map
```

Named slugs, not codes — `ai4good`, not `x7f2q`. A slug is said out loud and typed from memory.

```
lsf.pages.dev/ai4good        a course home
lsf.pages.dev/ai4good/setup  something inside it — one level
lsf.pages.dev/rva-chico      a one-off, flat and hyphenated
```

[`links.txt`](links.txt) records every slug's target, one tab-separated row, queried with `find`.
`gforms new`, `gslides new`, `gdocs new` and `gdrive share` each take `--slug`, through
[`../slug.py`](../slug.py), so a link is named where it is created.

The slug grammar, the private-subtree refusal, why Cloudflare rather than GitHub Pages, and what
`check` watches: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Why the redirect is Cloudflare's and not GitHub's, why a private subtree gets no slug, and what makes a map that grows forever stay cheap. |
| [`cfpages`](cfpages) | — | — | named short links: add, find, rm, build, check |
| [`links.txt`](links.txt) | — | — | Every short link this workspace hands out: the slug someone is told out loud, and where it really goes. Read by core/tools/links/links_core.py; published as _redirects by `cfpages build`. |
| [`links_core.py`](links_core.py) | [`links_core.pyi`](links_core.pyi) | `Refused`, `load`, `preamble`, `save`, `validate_slug` | links_core.py — the slug map read+write seam, and the redirect file it emits, for links/cfpages |
<!-- routing:end -->
