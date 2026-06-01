Foundry VTT v14 — AppV2 sheet customization: tab injection, stale tabGroups bug, partial re-render nav-wipe bug.

---

## AppV2 Tab Injection

Nav selector differs by sheet type — SceneConfig uses `sheet-tabs`, others use `tabs`:
```typescript
const $nav = $html.find("nav.tabs:not(.secondary-tabs), nav.sheet-tabs:not(.secondary-tabs)").first();
```

Content element: `<div class="tab" data-tab="NAME">` (div, no data-group). Insert after last existing tab:
```typescript
$html.find(".tab[data-tab]").last().after($section);
// Falls inside .sheet-body — NOT after the footer.
```

AppV2 `changeTab()` validates against static `TABS` — unregistered tab names throw. Fix:
```typescript
$html.on("click", `a[data-tab="${TAB}"]`, (e) => {
  e.stopPropagation();                             // prevent AppV2 from calling changeTab
  $nav.find("a[data-tab]").removeClass("active");
  $html.find(".tab[data-tab]").removeClass("active");
  $(e.currentTarget).addClass("active");
  $html.find(`.tab[data-tab="${TAB}"]`).addClass("active");
});
// Also deactivate ours when other tabs clicked:
$nav.on("click", `a[data-tab]:not([data-tab="${TAB}"])`, () => {
  $html.find(`.tab[data-tab="${TAB}"], a[data-tab="${TAB}"]`).removeClass("active");
});
```

Other AppV2 gotchas:
- `html` in `renderSceneConfig` **IS the `<form>`** — `$html.find("form")` returns 0
- `[data-tab="basics"]` matches both nav `<a>` and content `<section>` — always add element type
- `name="flags.MODULE_ID.key"` on checkbox → Foundry auto-persists on form submit, no JS needed
- Do NOT clone submit button — Foundry's own button handles form save

## AppV2 Stale `tabGroups` Bug

When `stopPropagation` on custom tab click (prevents AppV2 calling `changeTab`), AppV2 never updates `tabGroups[group]`. Next native tab click: `changeTab()` compares `tabGroups[group] === clickedTab` — if group was already on that tab, returns early without activating content `<div>`.

Fix: in "other tab clicked" handler, **explicitly add `active` class** to clicked tab's content section:
```typescript
$nav.on("click", `a[data-tab]:not([data-tab="${TAB}"])`, (e) => {
  $html.find(`.tab[data-tab="${TAB}"], a[data-tab="${TAB}"]`).removeClass("active");
  // Re-activate clicked section in case changeTab() returned early due to stale tabGroups
  const clickedTab = (e.currentTarget as HTMLElement).dataset.tab;
  if (clickedTab) $html.find(`.tab[data-tab="${clickedTab}"]`).addClass("active");
});
```

## AppV2 Partial Re-render: Nav Items Wiped, Tab Content Persists

AppV2 re-renders the sheet on every document change (e.g. GridConfig live-preview calls `scene.update()` on each form edit). The re-render does a **partial DOM update**: nav `<a>` items are wiped and replaced, but injected tab content `<div class="tab">` elements are preserved.

**Consequence for injected tabs:**
- Guard idempotency on the **content div** (`.tab[data-tab="${TAB}"]`) — NOT the nav item
- Re-inject the nav item unconditionally when missing (each re-render wipes it)
- Bind event handlers only on first injection (when content div was absent)
- **Use delegated handlers on `$html` (form element)** for all clicks — survive nav DOM replacement

```typescript
function addIsorollTab($html, label, fieldsetContent, onFirstInject) {
  const $nav = $html.find("nav.tabs:not(.secondary-tabs), nav.sheet-tabs:not(.secondary-tabs)").first();
  const tabContentExists = $html.find(`.tab[data-tab="${TAB}"]`).length > 0;

  // Nav item wiped on re-render — always re-inject if missing
  if (!$nav.find(`a[data-tab="${TAB}"]`).length)
    $nav.append(`<a class="item" data-tab="${TAB}">...</a>`);

  if (tabContentExists) return;  // content + delegated events already present

  // First injection only: create content div + bind delegated handlers
  $html.find(".tab[data-tab]").last().after(`<div class="tab" data-tab="${TAB}">...</div>`);
  $html.on("click", `a[data-tab="${TAB}"]`, ...);                           // delegated → survives nav replacement
  $html.on("click", `nav a[data-tab]:not([data-tab="${TAB}"])`, ...);       // delegated from $html not $nav
  onFirstInject?.($html);
}
```

**Multiple same-name inputs bug**: if guard fires on nav item (always 0 after wipe), content divs accumulate — multiple copies of every `<input name="flags.X.Y">` in the form. `FormDataExtended` collects all values; Foundry stores them as arrays. Next render reads e.g. `"false,false,false"` — truthy string → checkbox appears checked. Fix: guard on content div + sanitize flag reads with `=== true` / `typeof === "number"` etc.

**Flag read sanitization after corruption:**
```typescript
// Prior bad saves may have stored comma-joined arrays (e.g. "false,false,false")
const enabled     = doc.getFlag(MODULE_ID, "enabled")            === true;
const transformBg = doc.getFlag(MODULE_ID, "transformBackground") === true;
const rawProj     = doc.getFlag(MODULE_ID, "projection");
const projection  = (typeof rawProj === "string" ? rawProj : undefined) ?? "dimetric_2_1";
const rawNum      = doc.getFlag(MODULE_ID, "customRotation");
const cRot        = (typeof rawNum === "number" ? rawNum : undefined) ?? -45;
```
