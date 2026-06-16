# Code Setup
> Per-language setup, facade templates, and project scaffolding reference

## Facade Templates

Each folder with multiple source files needs a facade. Templates below — copy, adapt, prune to actual public API.

### TypeScript / JavaScript — `index.ts`

```typescript
// Public API for the <module> module — implementation in sibling files
export type { TypeA, TypeB } from './file-a';
export { functionA, ClassB } from './file-b';
// No `export *` — breaks tree-shaking in Vite/webpack
```

**Rules:**
- Explicit named exports only, no `export *`
- Only export what external callers actually need
- Types and values exported separately (`export type` vs `export`)
- File must have first-line description comment (enforced by hook)

### Python — `__init__.py`

```python
# Public API for the <module> package — implementation in sibling files
from .file_a import ClassA, TypeA
from .file_b import function_b

__all__ = ['ClassA', 'TypeA', 'function_b']
```

**Rules:**
- Explicit `__all__` required — defines the public contract
- Relative imports only inside a package
- `mock.patch` in tests must target the definition site, not the facade:
  `mock.patch('pkg.module.Symbol')` not `mock.patch('pkg.Symbol')`

### Dart — `index.dart`

```dart
// Public API for the <module> library — implementation in sibling files
export 'file_a.dart' show ClassA, TypeA;
export 'file_b.dart' show functionB;
// Use `show` to whitelist — never bare `export`
```

### SCSS — `_index.scss`

```scss
// Public API for the <module> styles — implementation in sibling files
@forward 'file-a' show mixin-a, $var-b;
@forward 'file-b';
```

---

## Fold Protocol

Reading order for any unfamiliar module (most compact → least compact):

```
CONTEXT.md routing        ← which folder do I need?
<folder>/index.ts         ← what does that folder export? (fold point — read directly)
<folder>/file.d.ts        ← what does a specific file export? (full signatures)
<folder>/file.ts          ← source (only when modifying)
```

Stop as soon as you have enough context. Most tasks stop at `index.ts` or `file.d.ts`.

---

## New Project Checklist

Each project under `Code/` must have:
- `CONTEXT.md` — line 2 is `> Short description`
- `README.md` — user-facing overview
- Facade (`index.ts` / `__init__.py` / `index.dart`) at every folder with source files
- `.mcp.json` — loads codegraph MCP when working in this project (see below)
- `.gitignore` entry for `.codegraph/`

Optional but recommended:
- `SPECS.md` — architecture decisions and design rationale
- `ROADMAP.md` — planned work

---

## codegraph

Pre-indexed knowledge graph (tree-sitter + SQLite). Lets you query architecture, find callers, and explore flows without reading raw source. Per-project — each project has its own index.

### Init a new project

```bash
cd /mnt/workspace/Code/<project>
codegraph init          # indexes all source files → .codegraph/
codegraph status        # verify: nodes, edges, files, DB size
```

Add to project `.gitignore`:
```
# codegraph knowledge graph index
.codegraph/
```

Create `.mcp.json` at project root (MCP server loads only when Claude Code opens this directory):
```json
{
  "mcpServers": {
    "codegraph": {
      "type": "stdio",
      "command": "codegraph",
      "args": ["serve", "--mcp"]
    }
  }
}
```

### Keep index fresh

Index auto-syncs via inotify while `codegraph serve --mcp` runs. No manual update needed during a session. To force a full reindex:

```bash
cd /mnt/workspace/Code/<project> && codegraph init
```

### MCP tools (available in sessions opened from project directory)

| Tool | Use |
|------|-----|
| `codegraph_explore` | Architecture questions, "how does X connect to Y" |
| `codegraph_search` | Find a symbol by name across the project |
| `codegraph_callers` | Every call site of a function |
| `codegraph_node` | One symbol's full source + callers |

### Projects with codegraph

All current projects are indexed: `isoroll-module`, `flows`, `apptime`, `voti`, `shortvid`, `corpora`, `futebots`, `ppc`.

---

## Per-Project Setup

Each project has its own git repo. Project-specific environment setup lives in the project's own `SETUP.md`.

| Project | Stack | Setup |
|---------|-------|-------|
| `isoroll-module` | TypeScript + Vite | `npm install` |
| `isoroll-content` | Python | `pip install -r requirements.txt` |
| `flows` | Python | `pip install -r requirements.txt` |
| `apptime` | Flutter + Kotlin | [`apptime/SETUP.md`](apptime/SETUP.md) |
| `voti` | Next.js / TypeScript | `npm install` |
| `corpora` | Python / PyTorch | `pip install -r requirements.txt` |
| `futebots` | Python | `pip install -r requirements.txt` |
| `shortvid` | Python / PySide6 | `pip install -r requirements.txt` |
| `ppc` | Vanilla HTML / Alpine.js | open `index.html` via local server |
