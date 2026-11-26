# description-writer
> Which model writes a document's one-line `description` (`Name: what it is for, who uses it`) well enough, at the lowest cost — so that bulk work need not run on the host's top level?

## Method

One prompt, the same for every arm: the instruction below plus the body of four docs-ufrpe documents, each with its figure blocks and HTML comments stripped and cut at 2,500 characters — `modelos/declaracao-acumulos`, `modelos/formulario-cadastro-bolsa-capes`, `modelos/termo-outorga-proap-auxilio-pesquisador`, `normas/calendario-academico` (11.5 kB in all).

> Escreva a linha `description` de cada documento. Formato: `Nome: resto.` — Nome até 40 caracteres; depois, para que serve e quem usa, numa frase. Sem inventar. Expanda sigla só se o texto a expandir. Responda só com 4 linhas `N. <description>`. *(plus three good descriptions already in the corpus as examples)*

- outside workers: `core/run tools/delegate/ask --only deepseek|flash|codex <prompt.md>`
- other codex models: `/usr/lib/chatgpt/resources/codex exec -s read-only -m <model> --ephemeral --skip-git-repo-check -o <out> "$(cat prompt.md)"`
- Claude: the Agent tool with `model: sonnet|haiku` (`general-purpose`), told to read the prompt file and answer only.

**Measurement.** Wall seconds per call. Quality is a hand verdict against the source text: does each line name the document, say what it is for and who uses it, and invent nothing? A format break counts too (a Name over 40 characters, wrong numbering, an acronym expanded that the text does not expand).

## Results

| Date | Arm | s | Cost | Verdict | Faults |
|---|---|---|---|---|---|
| 2026-11-23 | deepseek-v4.1-flash-free (opencode) | 10 | free | good, precise | numbered every line with a literal `N.` |
| 2026-11-23 | gpt-6-luna (codex) | 18 | subscription | good, the tersest | none |
| 2026-11-23 | gpt-5.6-luna (codex) | 18 | subscription | adequate, more generic | dropped "CAPES" from #2 |
| 2026-11-23 | gpt-6.2-sol (codex) | 18 | subscription | best: who signs, for whom | none |
| 2026-11-23 | gpt-6.1-sol (panel `codex`) | 16 | subscription | as good as 6.2-sol | none |
| 2026-11-23 | claude sonnet (subagent) | 5 | API | very good | one Name at 42 characters |
| 2026-11-23 | claude haiku (subagent) | 13 | API | good | "fevereiro a agosto" for the calendar — read off the 2,500-character cut, not the document |
| 2026-11-23 | gemini-3.8-flash-high (panel `flash`) | 400 timeout, then 165 | subscription | wordy | expanded CAPES and UFRPE against the rule |

## What changed

Lucas chose to stop doing bulk work on the host's top level: description writing goes to a free worker (deepseek, gpt-6-luna as the fallback), with `verificar.py` checking the format and a sample read by a stronger model; code goes to a Sonnet subagent, reviewed by the host. First user: the docs-ufrpe PRPG batch (`code/docs-ufrpe` ISSUES `[piloto-prpg]`).

## Limitations

- Four documents, one run per arm. The task is easy, so every arm passed: this ranks cost and format discipline, not ability.
- The prompt file is not versioned (it was built in a scratchpad); the recipe above rebuilds it, not byte for byte.
- The verdict is the host's (Claude Opus), the same vendor as two arms.
- Claude arms ran as subagents that also loaded the workspace's session context, so their seconds are not comparable with a bare call, and their cost was not measured (`—`).
- Haiku's calendar error comes from the cut input, and any arm that summarizes a whole document would hit it; at full length it may vanish.
