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
<folder>/index.d.ts       ← what does that folder export? (fold point)
<folder>/file.d.ts        ← what does a specific file export?
<folder>/file.ts          ← source (only when modifying)
```

Stop as soon as you have enough context. Most tasks stop at `index.d.ts`.

---

## New Project Checklist

Each project under `Code/` must have:
- `CONTEXT.md` — line 2 is `> Short description`
- `README.md` — user-facing overview
- Facade (`index.ts` / `__init__.py` / `index.dart`) at every folder with source files

Optional but recommended:
- `SPECS.md` — architecture decisions and design rationale
- `ROADMAP.md` — planned work

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
