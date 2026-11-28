# Workspace roadmap

> Everything still open in the workspace repo, in one file. A finished item is deleted; a killed one gets **one line** under § Rejected so it cannot come back looking new.
>
> **Three fields per item, no fourth.** *What* will exist · *Why* it is worth building · *Done when*, the observable that ends it. **HOW is the job of the session that takes the item** — a roadmap carrying its own implementation goes stale the day the code disagrees with it. Rules live in the `SPECS.md` that owns them; numbers live in `core/experiments/` and `ISSUES.md`. Re-run an instrument.
>
> 🔴 Lucas decides · 🟡 an agent can rule alone · 🟢 mechanical. Items are named, never numbered.
>
> **`## Agora` is what comes now: ≤3 `- [tag] — why now` pointers to items in any ROADMAP of this repo. The item stays in its section.** Lucas ranks it. `handoff --take`, `wos/take`, `/roundup` and SessionStart show it, and `handoff --write` refuses an Agora or a Next action that points at nothing (Lucas, 2026-11-26).

## Agora

- [wos-diet] — the workspace feels heavy, and every cut shrinks every future session
- [delegate-v1] — half-proven; cutting the WOS is its workbench
- [scoreboard-reading] — the baseline that tells which cut is a guess

## Measurement — does any of this earn its keep

**🟡 [scoreboard-reading] the scoreboard is running and owes its first reading**
*What* — the two-week reading, and the cuts it justifies: `core/run tools/wos/features --scoreboard`, into `core/experiments/hook-scoreboard.md`. **Due 2026-09-28**; the tool prints its own start date, so check it rather than this line.
*Why* — 82 features are on, so every cut is a guess and kept rules are paid on faith.
*Done when* — the table is read after two weeks of ordinary use and each silent feature is a decision.

**🟡 the ablation — the repo has never been measured against its own absence**
*What* — variants of the public repo, one feature off in each, against one synthetic task suite.
*Why* — this workspace compensates for model failures; a rule that outlives its failure is pure cost.
It also **runs before the cutting campaign** (Lucas, 2026-09-15), because it is what says which mechanism earns its keep. Unblocked 2026-09-16: the repo it varies is `lsfcin/wos`, public, synced one way by `core/run tools/wos/publish/repo` and green on its own suite.
*Done when* — a **per-feature** verdict is readable. Runs outside this workspace (`academy/papers/wos-ablation/`).

**🟡 what a session carries between turns and sessions — three mechanisms, none looked at**
*What* — readings against what this workspace already does (the CONTEXT.md chain, the interface-first read, the handoff): `briefd` (a git-backed corpus compiled into one token-budgeted bundle per task over MCP), the cheap decide-only model (what to expand or contract per turn; does it also automate functional tests here?), and the *state file* (GlitchCatClub): a compact file kept during work that the harness re-presents when it discards history, against native auto-compaction and the handoff. All in `core/refs/REFS.md`.
*Why* — they attack the bill `core/experiments/context-window.md` and `read-amplification.md` measure; native compaction fires late and its opaque summaries rot the context. INBOX 2026-09-18, 09-21, 09-27, 09-29.
*Done when* — each has a verdict against a measured number of ours (the state file on one long task: facts lost, integrity), and each loser is deleted from `REFS.md` with its reason.

**🟡 avaliar jevgrep para seleção cirúrgica de arquivos para coding agents**
*What* — testar o `jevgrep` (ou seu método de busca/indexação focada em agentes) contra os comandos de busca e leitura do WOS (`grep_search`, `find_by_name`, `session/reads`).
*Why* — Lucas (INBOX 2026-09-30): ferramenta open-source promete reduzir em até ~30% o consumo de tokens/custos por tarefa ao entregar apenas os arquivos exatos ao contexto do modelo.
*Done when* — teste comparativo medido em 3 tarefas de refatoração no WOS, registrando se houve ganho real sobre a navegação atual por `CONTEXT.md` + ferramentas de busca.

**🟡 [stt-desktop-ux] ditado por voz local (Ubuntu/Windows): cursor via IBus, feedback e memória**
*What* — evoluir `core/tools/audio/` (v1 entregue em 2026-11-28): corrigir deadlock IBus (`b20261128-ibus-deadlock`) para injetar direto no cursor sem apagar o clipboard (+ avaliar histórico `Super+V`); remover notificação inicial redundante; avaliar indicador piscando na barra superior e feedback no cursor via IBus preedit (`"[ouvindo...]"`/`"[reconhecendo...]"` ou texto parcial em tempo real); isolar inferência do `wos-stt` em worker descartável (`b20261128-sttd-memory-retention`); agendar `dictate learn` automaticamente e cobrir `Auto T`→`Alt+T`, `AGI`/`Multigravity IY`→`agy`/`Antigravity IDE`. Mantém no horizonte gatilho `"bot ..."` e Windows.
*Why* — teste ao vivo de Lucas (2026-11-28): transcrição PT-BR ficou muito boa, mas a usabilidade sofre com atraso de 2 s + queda no clipboard, falta de sinal visual de gravação ativa/progresso no cursor e 1,3 GiB RAM / 2 GiB swap retidos no `wos-stt`.
*Done when* — ditado via `Alt+T` injeta direto no cursor sem tocar o clipboard, mostra feedback claro sem notificação intrusiva, devolve RAM/swap/VRAM a ~0 após idle testado ao vivo e roda `learn` automaticamente.

## Legibility — can Lucas still read what he owns

**🔴 personal design data**
*What* — Decide whether Lucas's palette and fonts cross into the public clone. *Why* — The boundary is unresolved. *Done when* — Publication matches his choice.

**🔴 source-heavy documents**
*What* — Decide how source URLs participate in document limits. *Why* — Source requirements forced an approved dossier partition. *Done when* — Traceable evidence survives without routine sibling files.

**🟡 visualizador de fluxo de commits e trocas de contexto (swaps) entre projetos**
*What* — visualização gráfica do fluxo de trabalho onde cada repositório é uma linha vertical e cada commit é um nó, mapeando visualmente os *swaps* (trocas de projeto) ao longo do tempo para o `/compass`.
*Why* — diagnosticar se a troca de projeto acontece num ponto de parada com marco de valor entregue ou no meio de uma tarefa inacabada, revelando dispersão de atenção e o que está prestes a ser fechado (Lucas, INBOX 2026-09-29).
*Done when* — gerador executável via `core/tools/wos/session` que desenha o grafo temporal de commits e swaps entre repositórios a partir do histórico git.

**🔴 the health picture is built and does not land — redesign it**
*What* — `ARCHITECTURE.html` redrawn as a list ordered by colour and symbol, where the page now puts a big mostly-empty table. Next deliverable is the Claude Design prompt for that session, and it has to resolve one conflict: Lucas wants per-file reads per session on this page, and that is the one number that breaks its determinism — it is regenerated at every close and must change only when the workspace does.
*Why* — three drawings answered *what is there*; Lucas read this one 2026-09-15 and ruled it an inventory with better manners.
*Done when* — he reads it at a glance and the shapes that fail are deleted.

## Portability — would this work on a machine that is not Lucas's

**🟡 the port grew the workspace and the payment is still short** — *after the ablation, not before*
*What* — the cut that funds the port, from the top of `core/run tools/wos/size --weighted` down. The instrument names the candidate and it is **this file**, so draining the roadmap and paying the debt are one job.
Next related-fix candidates: `core/hooks/SPECS.md`, added `feature_law.py` commentary and tools concentrated in `core/tools/wos/` (INBOX 26 Sep / 5 Oct).
*Why* — `core/norms/reduce.md`: a session leaves fewer lines than it found. The port was worth every line; that is a reason to pay, not a reason not to.
The instrument that names candidates is `publish/repo --orphans`: every tracked file no feature claims, a stronger question than "who reads this" — `size --weighted` ranks what a session opens, this ranks what nothing can say a purpose for. It read 659 on 2026-09-15 and **10** on 2026-09-16, because most of those were claims the registry had not written; what is left is the real list.
*Done when* — the **weighted** total falls: lines SERVED per session, not lines on disk. The disk number can be paid by deleting a file nobody opens, which nearly took `core/experiments/` — 11% of the lines, zero reads in 88 sessions, and **the WOS paper's data. The cut never comes from there**
(Lucas, 2026-09-15). Several sessions; re-run the instrument rather than quoting a figure here. [machine-consistency] Inventory loose files, Downloads and repository inconsistencies before proposing verified cleanup (Lucas, INBOX 30 Oct).

**🔴 the install is a document a person executes, and it should be an interview**
*What* — `SETUP.md` driven as a deterministic decision tree: a fixed set of questions that maps what this person actually wants installed, then emits a plan their own harness executes across however many sessions it takes. Lucas, INBOX 2026-09-18.
*Why* — the contract today is prose the reader has to route themselves, and every branch in it is a question only they can answer (which harness, which of the 82 features, what is already on the machine). `/install` already checks and executes; what is missing is the part that asks. Deterministic and not a chat: the same answers must produce the same plan, or it is one more thing to verify.
*Done when* — a person who has never seen this workspace answers the questions and gets a plan naming every step, and `/install` runs it.

**🟡 the platform boundary's last answer needs one session run from inside Windows**
*What* — manager names for the 3 `apt` rows (`poppler-utils`, `tesseract-ocr`, `ddgr`). The file's own head only lets a row claim `system` once the name is VERIFIED on the other managers.
*Why* — a row claiming a portability nobody checked is the false green these checks exist to end.
Unblocked 2026-09-15: the machine is dual boot and `/mnt/windows` is that install mounted, so the block was never "no Windows" but "not booted into it". From **WSL2** on that side the hooks run unchanged — they are `sh core/run` — and `winget.exe` is reachable by interop. A native port with no WSL is a different item, blocked on the `sh` in each shim.
*Done when* — each of the three is `system` with a verified name, or stays `apt` with the reason.
One session from Windows does it: WSL2 + Ubuntu, clone, `/install`, read the names out of `winget.exe search` / `choco search`. `SETUP.md` names no operating system today, so what that session discovers goes back into it as a step.
The other two answers are in: `is_owner_only()` reads the ACL back rather than trusting `st_mode`, and `core/tools/deps.txt` carries a `floor` column — a floor, not a ceiling, because the failure is a distro shipping something too old, never a release from the future.

## Workers — who else can do the work

One delegation policy for outside workers and harness subagents: [core/ROADMAP-workers.md](core/ROADMAP-workers.md).

## Deferred — real work, deliberately not now

- **`academy/` as a satellite repo** (Lucas, 2026-09-18) — **reopen when the ablation has a per-feature verdict**, not before. What it would buy is an independent commit lane, which is a real cost paid today: two sessions share one index, and one session's half-written tree refuses the other's commits. What it would cost, measured: 20 hook and tool files name `academy/` directly, 10 of 38 goal files point into it, and `brain/goals/teaching-materials.md` — third-most served file in the workspace — is built out of pointers into it. The only argument available now is lines on disk (18% of the corpus), which is the number this workspace rejects.
- **`core/flows/` and `core/agents/`** (Lucas, 2026-08-25) — wait until v1 repo is tight.
- **Anything a nested repo owns** — each keeps its own `ISSUES.md` and fixes its own findings.
- **`[gdrive-integration]`, `[offline-resilience]`, serious OCR** — content/infrastructure, not repo.
- **One `WOS_SESSION_ID` for every harness** (panel recommended, Lucas deferred, 2026-11-10) — **reopen when a drift warning goes missing** on Copilot, opencode or Antigravity; without it, a commit there loses only that warning.

## Rejected

Twenty-six killed items are in git, not here: `git log -S'## Rejected' -- ROADMAP.md`. A tombstone stops earning its line once nobody who might revive the item remembers it, and this is the heaviest file in the workspace — one nobody needs is read by everyone. The six of 2026-09-14 and the four of 2026-09-15 joined them on 2026-09-17 (Lucas): the git log IS the other place, and this section keeps the pointer rather than the list.

- **A repo of its own for `code/aiwbot`** — 2026-09-17 (Lucas): it would not have closed the item.
  The wos clone would still carry a registry row naming a file it does not have.
- **A `needs` column in the feature registry** — 2026-09-17: one `bot` row means no dependency left to declare, and a column with zero filled values is worse than one with a single case.
- **Rewriting the hooks in a faster language** — 2026-09-21 (Lucas, after the number): the complaint was real (*"toda vez o meu computador fica fritando"*), the cause is not language. `core/experiments/hook-latency.md` measures ~60% of any hook's cost as CPython *starting*, before a gate reads a byte, and says so in one line: the fix that pays is removing processes. The saving already banked came from collapsing PostToolUse into the dispatcher, 1.9x. What is left is `post-edit.sh` doing real work per write (0.155-0.172 s) and a 961-test suite the roundup runs — neither gets faster by being written in something else, and the suite is pytest.
- **Adopting LoopForge, and a worker heartbeat** — 2026-11-21 (Lucas, panel unanimous): LoopForge is Docker + MySQL beside a craft that already relays files, so its ideas are borrowed, not the platform. A heartbeat says the process lives, not that it progresses; the timeout that kills the process group is the guard. The canary is `echo 'Reply OK.' | core/run tools/delegate/ask --only <worker> -`, never a flag of its own.
