---
name: feedback-provider-agnostic-naming
description: "Provider/model names are banned as a DIRECTIVE (assigning work, naming a tier, coupling code to a vendor) and fine as DATA (a measurement, a quoted id, which harness produced a draft) — position, not presence"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bb9b9715-4ea6-4628-9115-ce47ee08dba4
---

User feedback (2026-07-07, isoroll multiview session): "we are doing a lot of work to make our workspace agnostic to
specific providers/models... putting nb in the name of the files seems a bit too much".

**Why:** the workspace invests heavily in provider-agnostic structure (core/ skills, flows, tier→model mapping
volatile). A leading model is fine; baking it into file names couples code to a vendor.

**How to apply:** name modules/verbs/dirs by FUNCTION (imagegen_client, multiview_commands, mv-tile, gen-inbox), keep
provider choice as data (alias registry, docs). Applies to any provider: NB/Gemini, OpenAI, Comfy checkpoints, etc.
Related: [[fable-quota-strategy]].

**Widened 2026-08-17, and it is not only filenames.** Lucas reacted to me saying *"sonnet wires it"* about a roadmap
step: *"nothing in WOS should be tied to a specific vendor/company/model."* The rule covers **work assignments and how I
speak to him**, not just paths. Both ledgers carried 26 routing directives reading `model: sonnet` / `model: opus`; they
now read `tier: high|medium|low`, and which model fills a tier is data in `core/flows/craft/routing.md`.

The line that decides a given mention: **directive vs data.** Assigning work by model name is the violation; a
*measured* split ("opus-5 56.5%, sonnet 7.7%") or a quoted stale model id inside a bug report is legitimate, because
there the model is the fact being reported. This is why it cannot become a flat retired token — a presence check would
fire on the honest uses, so any guard has to read position. Related: [[project-wos-zero-roadmap]].

**A FILENAME IS NOT AN EXCEPTION TO THIS — it was never covered (ruled 2026-09-05, Lucas, closing
b20260905-brain-drafts).** I had summarised this rule as an absolute ban and asked whether comparing harnesses needed a
written exception. It does not. Lucas: *"essa é uma estratégia que queremos dar suporte... não se encaixa na
preocupação de provider agnostic, pelo contrário, entra no adversarial / experimental"*, and the distinction he drew is
the one already implemented — *"é muito diferente ter algo que só funciona pra 1 harness vs ter algo que é uma
contribuição que nós tivemos o cuidado de dizer qual foi o harness/modelo que gerou aquilo."* `brain/drafts/
metodologia-aulas-{sonnet,opus,gemini}.md` are legal and the names are the point: the provider is the variable under
study. `core/hooks/entropy/entropy_vendor.py`'s head is the authority — *"THE CHECK READS POSITION, NOT PRESENCE"* —
so read that file before ruling on any mention, and never widen it into a token ban.

**Ask the code, not this memory.** The nuance was in this body since 2026-08-17 and I still recalled the absolute
version off the description line, because that is what the index loads.
