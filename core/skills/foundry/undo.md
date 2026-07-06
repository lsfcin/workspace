---
name: undo
description: >
  Foundry VTT v14 — undo/history system: suppression, manual push, dual-stack ordering.
---

Foundry VTT v14 — undo/history system: suppression, manual push, dual-stack ordering.

---

## History Array Structure

Each layer (`canvas.tiles`, `canvas.walls`, `canvas.tokens`) owns a plain JS array `.history`.

```typescript
type HistoryEntry = { type: "update" | "create" | "delete"; data: object[]; options: object };
// e.g.
canvas.tiles.history.push({ type: "update", data: [{ _id: id, width: 200 }], options: {} });
```

`undoHistory()` pops the last entry and routes to `_onUndoCreate/Update/Delete`.
Called via `_onUndoKey` → **active layer only**. If user is in Walls layer, tile history is ignored.
"CONTROLS.EmptyUndoHistory" shown when `!this.history.length`.

`canvas.getCollectionLayer(collection)` determines which layer owns a document type.

---

## Suppressing Foundry's Auto-Record

Pass `{ isUndo: true }` in update/create/delete options to skip Foundry's undo recording.

**Gate in Foundry source** (`Scene._preUpdateDescendantDocuments`):
```javascript
if ((userId === game.userId) && this.isView && !options.isUndo) {
  layer?.storeHistory("update", priorState);
}
```

Use `{ isUndo: true }` on every embedded-document call that you want to manage yourself:
```typescript
await scene.updateEmbeddedDocuments("Wall", updates, { isUndo: true });
await scene.createEmbeddedDocuments("Wall", data,    { isUndo: true });
await scene.deleteEmbeddedDocuments("Wall", ids,     { isUndo: true });
await doc.update({ field: value },                   { isUndo: true });
```

**Caution:** `_storeHistory` drops entries where `data` contains only `_id` (no changed fields).

---

## setFlag Has No Options Param

`doc.setFlag(scope, key, value)` → no third argument for options. Cannot pass `{ isUndo: true }`.

**Workaround** — use `doc.update()` directly:
```typescript
// Set flag without recording
await doc.update({ [`flags.${MODULE_ID}.myKey`]: value }, { isUndo: true });

// Delete flag without recording (note -= prefix)
await doc.update({ [`flags.${MODULE_ID}.-=myKey`]: null }, { isUndo: true });
```

The `-=` prefix is Foundry's convention for flag deletion (equivalent to `unsetFlag`, but accepts options).

---

## Preserving IDs on Recreate

`createEmbeddedDocuments` with `{ keepId: true }` preserves original `_id` values:
```typescript
await scene.createEmbeddedDocuments("Wall", dataWithIds, { keepId: true, isUndo: true });
```

Critical when a custom undo stack records original IDs (e.g. for "create" undo that must find walls by ID). Without `keepId: true`, walls get new IDs and the undo entry's ID list becomes stale → crash.

---

## Manual History Push Pattern (Drag Gizmos)

Problem: calling `doc.update()` on every `pointermove` stacks one history entry per frame.
Solution: suppress ALL intermediate updates, push pre-drag state once on `pointerup`.

```typescript
// On pointerup, BEFORE committing final value:
const entry = { type: "update", data: [{ _id: id, width: drag.startW }], options: {} };
(canvas.tiles as any).history.push(entry);

// Commit with isUndo:true so Foundry doesn't record the final write either
await doc.update({ width: finalW }, { isUndo: true });
```

Key: capture start values at drag-begin (store in `DragState` fields), not at drag-end.
If you capture at drag-end, the document is already modified — undo restores last frame, not pre-drag.

---

## Dual-Stack Ordering (WallHistory + Tile History)

When a module maintains a custom stack alongside Foundry's native layer history, Ctrl+Z must
respect chronological order across both stacks.

**Pattern:**
1. Each custom entry records `tileHistLen = canvas.tiles.history.length` at push time.
2. Ctrl+Z interceptor: if `canvas.tiles.history.length > WallHistory.topTileHistLen`, defer to Foundry (tile op is more recent). Otherwise, handle in custom stack.

```typescript
window.addEventListener("keydown", (e) => {
  if (!e.ctrlKey || e.key !== "z" || e.shiftKey) return;
  if (!WallHistory.size) return;
  const tilelen = (canvas as any).tiles?.history?.length ?? 0;
  if (tilelen > WallHistory.topTileHistLen) return; // tile op is newer — let Foundry handle
  e.preventDefault();
  e.stopImmediatePropagation();
  WallHistory.undo().catch(console.warn);
});
```

Limitation: multiple separate history arrays have no shared chronological ordering.
The `tileHistLen` trick works for one pair of stacks (tiles + custom), but breaks if the user
performs custom ops → tile drags → custom ops (Ctrl+Z would undo drags before second custom op).
Accepted design tradeoff for isoroll.

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Capturing "original" state at drag-end | Undo restores to last drag frame, not pre-drag | Capture start values at drag-begin |
| `setFlag` without `isUndo:true` | Foundry records flag change; rogue Ctrl+Z restores flags without walls | Use `doc.update({ "flags.x.y": v }, { isUndo: true })` |
| `createEmbeddedDocuments` without `keepId:true` on recreate | New IDs; custom undo entry's ID list stale → crash | Add `keepId: true` |
| Both custom stack and Foundry both recording same ops | Double-undo required per logical action | Suppress Foundry everywhere with `isUndo:true`; let custom stack be sole manager |
| Pushing entry with `data` containing only `_id` | Foundry's `_storeHistory` silently drops it; undo skips | Include at least one non-`_id` field |
