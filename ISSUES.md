# Workspace issues
> Open workspace defects; project defects belong in their owning ISSUES.md.

Delete resolved issues only with matching passing regression proof. Tools own generated measurements (core/SCHEMA.md).

## Open

- **`context-chain off` não cala `pre-read.py`**: lista a cadeia; nomear só o stub. [src: agent 2026-11-27]

- **`is_twin` só aceita `source: ../<stem>.pdf`**: twin de .doc/.docx não é isento dos tetos. Aceitar, com caso em `test_pdf_twin.py`. [src: agent 2026-11-26]

- **Processo de agente sem prazo**: o `memory-reminder` nomeia CLIs vivos há um dia, mas um `&` de agente (Foundry, 6 dias) segue sem prazo: `systemd-run --user --collect -p RuntimeMaxSec=`. [src: agent 2026-11-26]

- **aiwbot vaza memória** (3,7 GiB em 2 h): `MemoryMax=1G` agora o reinicia; o vazamento segue sem causa. [src: agent 2026-11-26]

- **A cópia do modo artifact não leva `brain/` nem o espelho de skills**: `verify.py fast` falha lá e passa na árvore real. [src: agent 2026-11-26]

- **`handoff --take` aceita o nome do repo, `wos/take` exige o caminho** (assimetria). Um resolvedor só. [src: agent 2026-11-26]

- **Fios herdados sem detalhe** (handoffs até 26 Nov): token órfão; rótulo de segredo × INBOX; `outputs/codex-git-write/e2e.sh` só read-only de `/tmp`; seção 7 atrás do roadmap. [src: agent 2026-11-26]

- **O outbox é oferecido em vez de usado**: no /inbox, disse "podemos encaminhar" sem chamar `wos/note` (25 Nov). Refinar `core/norms/improve.md`. [src: agent 2026-11-25]

- **Codex aberto de dentro do Claude herda `CLAUDE_CODE_SESSION_ID`**; `lock.SESSION_ENV` lê esse antes do `CODEX_THREAD_ID` e confunde as sessões (25 Nov). [src: agent 2026-11-25]

- **Espelhos de skills não seguem `claim`/`switch`** (untracked): com `inbox.md` diferente entre branches, o close falha `test_a_mirror_dirtied_by_a_merge` até o `sync-skills` (25 Nov). [src: agent 2026-11-25]

- **verify fast checa a forma da árvore inteira**: um commit paralelo em `code/docs-ufrpe` deu 13 erros falsos (25 Nov). [src: agent 2026-11-25]

- **`routing()` só re-sincroniza o pai imediato** (`commit/generators.py` 43-44): em `<pasta>/<nome>/<nome>.md` (docs-ufrpe modelos/), 30 formulários no disco e 5 na tabela. Subir até o ancestral com CONTEXT.md (24 Nov). [src: agent 2026-11-24]

- `session/context` despeja as pastas `-tmp-describe-*`; `gforms.md` foge do padrão de nome das skills (25 Nov). [src: agent 2026-11-25]

- **Roundup stats and cost messages missing after an apparent fix (Lucas, twice).** Only Claude Code has user-only Stop delivery (`close-report`); reproduce per harness and verify delivery. [src: agent 2026-11-23]

- **`context_synchronizer.py code` gravou `code/wos/CONTEXT.md`** no clone público. Pular os `WORKSPACE_MARKERS`, como `_under_code`. [src: agent 2026-11-23]

- **Os workers do painel não leem a web**: Codex (`Internal Error`) e argon (sem rede) falharam numa página pública (23/11). Declarar em `core/workers.txt` ou dar rede. [src: agent 2026-11-23]

- **O wrapper do git deixa passar o Copilot** (`outputs/lock-facade/e2e.sh`, 24/11): `-p` pula hooks sem raiz em `trustedFolders` (falta OK de Lucas). `ancestors()` dá [] fora do Linux. `b20261124-git-wrapper-harnesses`

- **Três harnesses sem headless.** ZCode 0.16.3 `--prompt`: `Model config is missing`; `pi -p`: 402 ollama cloud (usar OpenRouter); DeepSeek: só `.exe` Windows (20, 24 Nov). `b20261120-zcode-headless-no-model`

- **`delegate/ask --list` dá `live ok` a um worker que não responde**: o deepseek (opencode) aceitou a chamada e não disse nem "ok" em 100 s (24 Nov). [src: agent 2026-11-24] `b20261124-deepseek-hangs`

- **O pymupdf põe um dígito solto como título** (`# 0`, `# 8`) logo após `<!-- page N -->`, resto do brasão; 45 no docs-ufrpe, corrigidos à mão (24 Nov). [src: agent 2026-11-24] `b20261124-pdf-crest-title`

- **`video` não avisa quando a fala sai curta.** `video_media.transcribe()` devolve `""` em qualquer exceção, e ninguém compara o último segmento com a duração (21 Nov). [src: agent 2026-11-21] `b20261121-video-speech-cut`

- **`core/harnesses.txt` não tem copilot**, mas existem `core/hooks/copilot/` e um teste de shim dele: linha ou ausência escrita (20 Nov). [src: agent 2026-11-20] `b20261120-harnesses-no-copilot`

- **Censo do docs-ufrpe.** `web/fetch`: UFRPE omite intermediário (RNP ICPEdu) e trava UA de curl (502 em 90 s); levar bundle de `verificar.py` (19–21 Nov). `b20261119-census-tool-gaps`

- **`checks/web-retry.py` só escuta o Claude Code.** Só `.claude/settings.json` registra `PostToolUseFailure`; conferir os outros shims (21 Nov). [src: agent 2026-11-21] `b20261121-web-retry-shims`

- **O pre-commit diz que `core/hooks/brain` é ignorado** ao re-stagear, mas `git check-ignore` diz que não; suspeita: o `.gitignore` de `brain/` (20 Nov). [src: agent 2026-11-20] `b20261120-brain-hooks-staged-as-ignored`

- **173 arquivos órfãos no publish** (2.681 linhas): nenhuma feature os reivindica; `/publish` pede zero (`publish/repo --orphans`, 20 Nov). [src: agent 2026-11-20] `b20261120-publish-173-orphans`

- **Pergunta para Lucas fecha a sessão sem resposta.** Uma escolha "Lucas decide" foi construída sem resposta nem linha em "Decidido sem perguntar" (apptime 6 Nov, `82cdec2`); o roundup podia cobrar. `b20261106-handoff-unanswered`

- **"O que tem pela frente" respondido com o ROADMAP lido pela metade.** A sessão do apptime listou só os itens 🟡/🔴 (6 Nov); a pergunta pede o ROADMAP inteiro. `b20261106-partial-roadmap-read`

- **Commit que cita `Bnn` não confere o ISSUES.** `3747fb3` (apptime) anunciou o B10 sem escrevê-lo; entrou só em `e5f13a1` (6 Nov). `b20261106-commit-cites-missing-bnn`

- **Read-antes-de-Edit empurra para o caminho sem gate.** Editar o l10n do apptime exige ler os `.api` inteiros, então a sessão caiu num heredoc python, UNGATED WRITE (6 Nov). `b20261106-read-gate-pushes-heredoc`

- **Gate de primeira linha barra arquivo de trabalho**: o prompt do painel no scratchpad (9 Nov) e em `outputs/` (17 Nov), de novo no scratchpad (20 Nov). `b20261109-first-line-gate-workfiles`

- **Gates de contexto cobram uma volta por árvore**: uma recusa por árvore tocada (9 Nov; 6 recusas numa triagem em 17 Nov; de novo em 19 e 20 Nov). `b20261109-context-gate-round-trips`

- **`phone/adb prefs` ignora o `.bak`**: lê o XML truncado depois de um install; `--open app` não abre nada (6 Nov). `b20261106-adb-prefs-bak`

- **`cfpages check` não testa o 302 de verdade** (6 Nov). `b20261106-cfpages-check-302`

- **`cfpages publish` não apaga um artefato que saiu da origem**: `5-demonstracao-poster.md` seguiu no ar até remoção à mão (19 Nov). `b20261119-publish-orphans`

- **Tokens Google vencem um serviço por vez**, cada um pedindo navegador; `gslides preview` depende do token de drive (9 Nov). App em Teste: tokens vencem perto de 01/12. `b20261109-google-token-per-service`

- **`delegate/ask` só aceita caminho de arquivo**: texto dá traceback, não erro claro (9 Nov). `b20261109-panel-ask-text`

- **`core/refs/REFS.md` está no teto de caracteres**: a fila de intake não tem espaço; promover os itens avaliados para `.yaml` (20 Nov). [src: agent 2026-11-20] `b20261120-refs-at-cap`

- tools/delegate/ask cannot attach images; PNG paths went in prose (17 Nov). Verify delivery, not acceptance of the path. `b20261117-panel-images`

- tools/web/shoot serves only the page directory and reads a query string as a path; the docs-ufrpe viewer needs a parent root and ?doc= (17 Nov). `b20261117-shoot-root-query`

- **Não se sabe se o `session_id` do Codex é o `CODEX_THREAD_ID`.** O pre-commit reconhece um commit de agente pela variável de ambiente; o gate do dispatcher não depende dela (10 Nov). `b20261110-codex-session-id`

- Two verify-fast failures on 17 Nov in tests since deleted (test_branch_gate.py, test_b20260902_…); recheck that nothing intermittent remains. `b20261117-verify-intermittent`

- **Processo morto com 137, sem rastro**: a suíte no pre-commit (10 Nov) e o roundup (16 Nov). Causa desconhecida. `b20261110-exit-137`

- **Gate pós-chamada do plugin opencode sem teste**: o after-hook não repassa shell, e hoje nenhum gate pós-shell existe para provar o caminho (10 Nov). `b20261110-opencode-post-gate`

- **O `handoff-gate` recusa comando que só CITA um handoff** em prosa; o pdf-gate já tira o heredoc de prosa e os dois podiam dividir a função (10 Nov). `b20261110-handoff-gate-prose`

- **O `handoff-gate` trata todo `outputs/handoff-*.md` como handoff**, e bloqueou a saída de um painel (10 Nov). `b20261110-handoff-gate-prefix`

- **`core/run -m pytest` quebra** com "can't open core/-m" (10 Nov; de novo 19 Nov). `b20261110-core-run-module`

- **Em plan mode, o pdf-gate bloqueia a leitura de um PDF sem gêmeo**, porque gerar o gêmeo é escrita (10 Nov). Proposta: gêmeo no scratchpad. `b20261110-pdf-gate-plan-mode`

- **`gmail attachments` quebra sem chave da API Anthropic** (13 Nov). `b20261113-gmail-attachments-key`

- **Resposta do painel chega a Lucas sem conferência de domínio**: citou um PDF da UFAPE como da UFRPE (13 Nov; de novo em 21 Nov, a Res. 009/2019). `b20261113-panel-domain-check`

- **Entropia conta `[[14]]` de nota de rodapé como wiki-link quebrado** (docs-ufrpe, 13 Nov). `b20261113-entropy-footnote-wikilink`

- **Proposta "aguardando OK" atravessa a sessão só como resumo**; o handoff devia apontar para o arquivo com o texto exato (17 Nov). `b20261117-handoff-proposal-text`

- **Lote docs-ufrpe (11 Nov).** Gêmeo PDF com frontmatter e .docx pedem first-line comment; norma revogada dispara finished work; CNPJ público da UFRPE cai na lei de segredos; `docling` >10 min onde `pymupdf` resolve. `b20261111-docs-ufrpe-lote`

- **Edição de cronograma colide com nota dada no site**: editar `disciplina.md` atrás do painel faz o `publish` recusar (13 Nov). Trazer o painel antes, ou mesclar por linha de aluno. `b20261113-cfpages-pull-colisao`

- **Painel externo barrado com dados pessoais**: o modo auto barrou o Gemini com CPF (16 Nov). Redigir antes (`secret_law.redact`). `b20261116-panel-pii`

- **`progressao.md` § Lado da comissão contradiz a própria regra** de duplicidade (parecer de George, 16 Nov). `b20261116-capd-duplicidade`

- **Rotas do academy desatualizadas**: `capd/CONTEXT.md` diverge da pasta de George; `lab/` e `students/` sem CONTEXT.md; `students/` e `cv/` fora da tabela (16 Nov). `b20261116-academy-routing`

- **Ferramentas que a sessão não achou**: downloads não aponta `chat/wazip` para zip do WhatsApp; faster-whisper sem `libcublas.so.12` cai para CPU (16 Nov). `b20261116-tool-discovery`

- **gslides lint marca "off the slide" em placeholders herdados do layout** que renderizam no lugar (techedu 111, ai4good 62 achados, 16 Nov). `b20261116-gslides-lint-placeholder`

- Recheck the 2-Nov Codex parity audit (outputs/codex-audit-20261102/). `b20261102-codex-parity`

- **cfpages secrets --push configures production only**: preview lacks GITHUB_TOKEN/ENIGMA_SECRET, and segredos.env understates the token's scope (4 Nov). `b20261104-cfpages-preview-secrets`

- **O type gate recusa pastas de cache .json**; o rastro-da-banca adotou um TSV com primeira linha. Formalizar a convenção (30 Out). `b20261030-type-gate-api-cache`

- Calendar ranges return empty for cin/ufrpe; tell empty from failure (24 Oct). `b20261030-calendar-range-auth`

- Personal Drive write token failed twice in one session; test refresh apart from reads (24 Oct). `b20261030-drive-write-token`

- Drive search caps at 20 results, and gsheets/Drive `list` has no pagination (26 Oct, 25 Nov). `b20261030-drive-search-pagination`

- PDF gate demands a twin for script-compiled TeX without .texif (24 Oct). `b20261030-compiled-pdf-detection`

- A partial path commit regenerated all of AGENTS.md with another session's staged norm line (26 Oct). Extend test_partial_commit_staging to generated norms. `b20261030-partial-norm-staging`

- Mail fetch: 50 unread, one page, no query; missed DocuSign PDFs, long attachment names (17–28 Oct). `b20261024-mail-search-attachments`

- **`slides text` writes despite its name**, and an expired grant blocked reads (19 Oct). `b20261024-slides-command-auth`

- **Named-link checks accept a site target its renderer cannot resolve** (ai4good/brw, 21 Oct). `b20261024-links-target-resolution`

- **Scheduled disk cleanup depends on a tool absent from the active tree**; SETUP lacks the scheduling and the models/ symlinks (24 Oct). `b20261024-disk-cleanup-install`

- **The Claude memory symlink targets the absent brain/memory** (24 Oct). Remove the integration. `b20261024-retired-memory-pointer`

- UNGATED WRITE misattributes paths after `cd`, and reads a literal `$S/file` as a path (16 Oct, 3 Nov). `b20261017-ungated-write-cwd`

- Video batches dizem ok na falha: galerias vazias ("38 ok", 17 Nov), parciais perdidas, `--level full` sem camada visual (25 Nov, `agy not logged in`), cookie jar read-only (Errno 30). [src: Lucas 2026-11-19] `b20261017-video-batch-results`

- **Brain stats staging**: refreshed goal files left unstaged (14–24 Oct); a path-only commit leaves the index old, HEAD and disk new (5961a25, eeba4ab, 51ba029, 25–26 Nov). `b20261014-brain-stats-staging`

- **PDF conversions overrun; low-confidence pages inflate audit references (25 Sep–9 Oct).** `b20261014-pdf-conversion-audit`

- **Python scripts opening PDFs escape command-text detection (26 Sep).** `b20261014-pdf-script-read`

- **Slide sampling starts a renderer per page (deck_sample.render_sample_images, 26 Sep).** `b20261014-slide-sample-batch`

- Read gate re-demands CONTEXT reads already made, including native Codex reads (30 Oct); reproducer test_b20260831_silent_stub_gate.py. `b20261014-read-registration`

- **Retired-token substring matching rejects valid words**, a cited article title among them (26 Sep, 16 Oct). `b20261014-retired-substrings`

- **The private-repo fiscal-identifier exception conflicts with the secrets rule**; bypass debt casinhas fa7244e (29 Sep). `b20261014-private-pdf-policy`

- **gslides previews land in the workspace root; private decks have no authenticated export (26 Sep).** `b20261014-slides-preview-export`

- **Presentation generation reads JSON instead of design-system tables (26 Sep).** `b20261014-theme-input`

- **Slide references use inconsistent classification and generic descriptions (26 Sep).** `b20261014-slide-ref-metadata`

- **Verify transcript redaction of the authorization-code pattern from the Canva session (26 Sep).** `b20261014-transcript-redaction`

- File-description lookups disagree on repo roots (frases.json, jsconfig.json; 18 Oct–1 Nov). Bypass e106d95 needs a regression. `b20261014-nested-file-description`

- **Expanded hook-link verification slows duplication checking (5 Oct).** `b20261014-verification-latency`

- **rtk rejects supported search flags (12 Oct).** `b20261014-search-flags`

- Shell-created directories do not refresh routing until a later commit (ai4good/artefatos, 28 Oct; ce4d4ab7). `b20261014-routing-cloned-dirs`

- context_synchronizer listed a nested repo's ignored segredos.env and demanded a first-line comment (18 Nov). Respect the owning repo's ignores. `b20261118-routing-nested-ignore`

- bash-context-gate.py demands subtree context for binary metadata tools such as pdfinfo (25 Sep). `b20260925-gate-binary-readonly`

- PDF-tool children (Marker/MinerU/Surya) keep VRAM after a failure (25 Sep). `b20260925-gpu-orphan-vram`

- Root pre-commit omits nested repos: cached removals or switches can silently delete tracked teaching files (administration mass deletion, 18 Oct). `b20260925-subrepo-tracked-deleted-sentinel`

- entropy_context.check_truncation flags any literal ellipsis (3 Oct). `b20261003-check-truncation-ellipsis`

- Ignored outputs/.drafts/tmp work does not sync across machines; brain/drafts/ai4good-git-retro-opus.md (627 lines, 2 Nov) went missing by 7 Nov. `b20260924-drafts-sync`

- line_counts.py, entropy_crowding.py and entropy_context.py print double-negative NOT REFUSED warnings (Lucas, 2 Oct). `b20261002-hook-warning-vocabulary`

- Goal backlogs and roadmaps duplicate work: rpg-isoroll still names painting in Foundry against content ROADMAP D8 (29 Sep). `b20260929-task-roadmap-boundary`

- Antigravity lifecycle hooks start at HOME, so a relative core/run fails; prove dispatch from HOME (25 Sep). `b20260925-antigravity-hook-cwd`

- Agents rewriting an old INBOX snapshot can overwrite concurrent captures; only the bot locks (f11a2334). `b20260921-inbox-writers`

- Nonmedia fallback reads GitHub sign-in chrome instead of the raw README and counts no text as ok (12 Oct). `b20260921-fetch-fallback`

- SCHEMA's underscore-template rule has no checker; teaching/structure/templates is unmarked (AD-16). `b20260918-template-naming`

- test_a_rebuilt_target_settles_in_one_pass rebuilds the real code/wos target and dirties later runs; the tree guard misses ignored nested repos (23 Sep; seen again 19 Nov). `b20260923-publish-test-real-target`

- Remaining ruled renames: shim→adapter, drift→divergence, corpus→tracked files, crowding→files per folder, drain→empty, sweep→scan, whitelist→allowed list (23 Sep). `b20260923-vocabulary-queue`

- The other machine's scoreboard keeps the pre-rename keys inbox-nudge/compass-nudge/publish-nudge (20 Sep). `b20260920-scoreboard-keys`

- Nested repos' `ISSUES.md` mantêm bloco de entropia antigo; limpar e tirar `*/ISSUES.md` de `core/hooks/generated.txt` (20 Sep, 19 Nov). Roundup só escreve `outputs/state/entropy-<repo>.md` (24 Nov). `b20260920-quiet-repo-entropy`

- Safe-to-delete branch lists in the entropy report age during a session; recheck ancestry at deletion (14 Sep). `b20260914-branch-list-snapshot`

- Registry keys google-auth/notes-notion/link-shortener/wazip/video-text/asset-inspect/vpn-cin carry vendor names, not family names. `b20260915-feature-names-carry-vendors`

- Feature `bot` and the crossing tree code/aiwbot use different names (17 Sep). `b20260917-bot-directory-keeps-vendor`

- foundry/iso-visual/prof cannot cross publicly, but the registry crosses verbatim, leaving them unswitchable (AD-14). `b20260917-private-skills-unswitchable`

- `_present` subtracts the target's gitignore, so a newly refused file is never removed from the target (17 Sep). `b20260917-refused-file-never-removed`

- publish --check/_same ignores generated blocks and reports clean for a corrupted target block. `b20260917-check-blind-to-stale-block`

- Public prose promises private paths the clone lacks (README→brain/academy, craft/tree→code/ROADMAP-spec-drive, goal headers→brain/goals). `b20260917-crossed-prose-broken-pointers`

- The read gate demands the same CONTEXT files again inside code/wos (16 Sep). `b20260916-read-gate-charges-twice`

- Feature names opencode-plugin/antigravity-hooks diverge from harnesses.txt and the adapter path. `b20260916-harness-names-four-ways`

- Paper search has no working service: Semantic Scholar 429, arXiv timeout (13 Sep). `b20260913-paper-search-has-no-arm`

- scoreboard.tsv grows append-only; test markers accumulate in core/state (16 Oct). `b20260922-state-stores`

- **`git commit` (via rtk, or with `-q`) reports success after a pre-commit refusal** (24 Sep, 11 and 16 Nov). Verify the git log after every commit. `b20260924-rtk-commit-false-ok`

- Empty .git/.codex/.agents/.aws directories appear after Codex runs (7/23 Oct). `b20261007-empty-git-dirs`
