# motion
> How elements change between steps — Morph, pan, zoom, entrance, exit: one kind of change at a time.

Change over time; what a shape looks like is `drawing`, the deck's order is `narrative`.

- **Static waits for motion.** An element that does not move never enters, leaves or fades while something moves, pans or zooms: it changes before or after, as its own step, or it belongs to the moving content and takes the same transform. An element present before and after a Morph always rides it; it never vanishes and reappears still.
- **What appears after a Morph is its own frame.** A shape never enters with an effect on the slide a Morph lands on (it blinks); it arrives as the next frame, camera still, auto-advanced (`advTm`) when it needs no click.
- **A click is where something is said.** Steps that only follow from the last one chain on their own; count the clicks a sequence asks for, and cut every one with nothing to say.
- **One text at a time.** A text leaves before the next arrives, no cross-fade. A title is never Morphed into another title (it stretches).
- **Forward is a pan, back is a zoom out.** In a deck built as a map (an overview slide whose regions are later slides, entered by zooming in), the next-slide key goes to the next region in reading order — the order the PDF prints — never back to the overview. The camera slides sideways from the current region to the next, keeping its zoom, at most zooming out slightly on the way. The camera zooms out to the overview only when the viewer goes back. The overview is never duplicated to return to it; a region may hold a smaller map of its own.
- **A 3D turn shows the next face.** When a drawn solid turns to show another side (front view to top view, street to drone), neither view is flat-on with the other face hidden. Each tilts a little: the front view already shows a thin strip (5–10%) of the top it turns to, and the top view keeps a strip of the front. Morph then only moves and reshapes shapes present in both frames; nothing fades in or out.
- **An arrow that grows or turns** is a fixed unit line, scaled and turned by its transform and present in every frame; Morph never resizes an arrowhead (it distorts it).
- **Easing** is *cadência* in pt-br (long form *cadência do movimento*), written with *easing* in italics in parentheses.

Refs: `pptx-morph` · `pptx-morph-3d` · `keynote-magic-move` · `wcag-motion`
