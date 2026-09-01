---
name: feedback-multiharness-essential
description: Multi-harness is ESSENTIAL to Lucas — optimize the copying, never delete a harness; and no hook dies without a scoreboard
metadata:
  node_type: memory
  type: feedback
---

**Lucas, 2026-08-25**, when I offered to cut `.opencode/`, `.zcode/` and the shims (78 files, ~1,500
LOC) on the grounds that he only uses Claude Code: *"ser multiharness é ESSENCIAL, podemos otimizar
isso, estudar como é feito para garantir o mínimo de retrabalho, de cópia e cola, mas nunca
excluir."*

In the same round, on cutting hooks: *"por serem automáticos, hooks são a garantia de uma estratégia
de comportamento que é 'zero-token' e não quero cortar nenhum a menos que cheguemos a esta conclusão
a partir de dados e de uma análise mais coerente."*

**Why:** both answers have the same shape — he refuses to cut a **capability** to buy tidiness.
Multi-harness is the workspace's thesis (nothing that matters lives in a vendor's directory), and an
automatic hook is the central bet (zero-token beats prompt). The waste he will attack is the
**copying** and the **prose**, never the function.

**How to apply:**

- Multi-harness: the optimization is one source plus generation, not deletion. Skills are already
  symlinks to `core/skills/*.md`; `.claude/commands/*.md` is a rendered copy because relative links
  change depth. If it grates, the way out is to stop versioning what is generated — never to delete
  a harness.
- Hooks: a proposal to cut arrives with a scoreboard or not at all. The item that produces the
  scoreboard is in `ROADMAP.md` § Measurement, and he has already ruled: **nothing is deleted before
  it exists.**
- The reduction target he wants is `.md`, not enforcement code.

Related: [[feedback-provider-agnostic-naming]], [[feedback-delete-weak-features]] (weak signal kills
a *feature*, never *a capability he has named essential*), [[project-wos-zero-roadmap]].
