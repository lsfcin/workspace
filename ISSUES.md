# Workspace issues
> Open workspace defects; project defects belong in their owning ISSUES.md.

Delete resolved issues only with matching passing regression proof. Tools own generated measurements (core/SCHEMA.md).

## Open

- Calendar ranges reportedly returned empty for cin/ufrpe; verify dates, account/auth and empty-versus-failure output (Claude RDA session, 24 Oct). `b20261030-calendar-range-auth`

- Personal Drive write token reportedly failed twice in one RDA session; reproduce token persistence/refresh separately from read access (Claude, 24 Oct). `b20261030-drive-write-token`

- Drive search reportedly silently caps results at 20; expose limit/pagination and distinguish exhausted results from a partial page (Codex progression report, 26 Oct). `b20261030-drive-search-pagination`

- PDF gate reportedly requires a twin for script-compiled TeX without .texif despite the compiled-PDF exclusion. Verify source recognition, keeping arbitrary Python PDF reads separate (Claude RDA, 24 Oct). `b20261030-compiled-pdf-detection`

- Partial path commit reportedly regenerated full AGENTS.md with another session's staged EDIT > CREATE line but excluded its norm source. Extend test_partial_commit_staging scope to generated norms, preserving unrelated staging (Claude, 26 Oct). `b20261030-partial-norm-staging`

- Mail fetch defaults to 50 unread messages, one page, no arbitrary query. Reproduce missed DocuSign PDFs (Claude, 17 Oct; multipart recursion exists), query/after/before pagination, long attachment filenames and cached-email PDF evidence (RDA/progression reports, 24–28 Oct). `b20261024-mail-search-attachments`

- **Slides text writes despite its ambiguous name.** It creates a text box; Claude reports nearly invoking it as a read and an expired grant blocking authenticated reads (19 Oct). Clarify intent/grant. `b20261024-slides-command-auth`

- **Public rebuild reportedly fails its target suite.** Claude reports omitted generator dependencies, a missing vendored fixture, routing/header failures and timeouts (21 Oct); test markers were staged into the target. Reproduce current failures; isolation: b20260923-publish-test-real-target; markers: b20260922-state-stores. `b20261024-publish-target-suite`

- **Named-link checks accept a site target its renderer cannot resolve.** Claude reports ai4good/brw used an extensionless route instead of the Markdown query form (21 Oct). Validate local targets or diagnose unsupported routes before sharing. `b20261024-links-target-resolution`

- **Scheduled disk cleanup reportedly depends on a tool absent from the active tree.** Claude reports a 1 Nov job targeting tools/disk/ubuntu, missing SETUP coverage for scheduling and Hugging Face/ComfyUI symlinks into models/, and three Whisper variants: turbo for audio, base for video, small for rastro-da-banca (24 Oct). Verify installation and visible failures before November; assess model differences before standardizing. `b20261024-disk-cleanup-install`

- **Retired memory integration targets a missing directory.** The Claude memory symlink still targets absent brain/memory (verified 24 Oct). Remove obsolete integration; use durable workspace files. `b20261024-retired-memory-pointer`

- **UNGATED WRITE can attribute an output to the directory preceding cd.** Claude session, 16 Oct, reports a warning naming brw/excelente.md while the command wrote into cmp/; verify relative-path attribution across directory changes. `b20261017-ungated-write-cwd`

- Video extraction hides progress/partial results and calls empty or error-only galleries successful. Reproduced 30 Oct: mixed-carousel omissions, dimensionless thumbnail selection at 150 px, IndexError on downloaded clips without audio, serial image-call stalls without persisted per-link results. Preserve every slide/full-resolution image and numeric comparisons with estimation uncertainty. Earlier reports: cancellation with no output (24 Oct), YouTube 403 despite JS runtime (19 Oct). `b20261017-video-batch-results`

- **Roundup attributes native ChatGPT closes to a Claude transcript.** `core/tools/wos/roundup.session_id()` picks the newest `.claude/projects` transcript; unlike `tools/wos/handoff`, it ignores native session identity. Cost, size deltas and compaction need provider-aware attribution before being treated as this session's measurements. `b20261016-roundup-session-attribution`

- **Brain stats reports success but leaves its refreshed files unstaged.** Inbox triage observed `brain/GOALS.md` unstaged and refreshed goal files partly staged after a successful `core/run hooks/brain/brain_stats.py`; complete staging explicitly and establish why its internal stage call fails. 24 Oct: every commit staging a goal leaves it dirty again, worktree one touch ahead of HEAD (rpg-isoroll 7/121 committed, 8/122 on disk), so roundup never sees a clean tree. `b20261014-brain-stats-staging`

- **Reported PDF conversions exceed their expected duration; low-confidence page recognition inflates audit references. Isolate the blocking stage and filter confidence (25 Sep, 8/9 Oct).** `b20261014-pdf-conversion-audit`

- **Python scripts opening PDFs escape command-text detection; scope this independently of metadata inspection and verified self-generated PDF access (26 Sep).** `b20261014-pdf-script-read`

- **Slide sampling starts a renderer per page instead of a multi-page request; verify equivalent output from batched rendering (deck_sample.render_sample_images, 26 Sep).** `b20261014-slide-sample-batch`

- Read-gate tests alternate success/failure; completed CONTEXT reads are repeatedly demanded, including immediately preceding reads in native Codex (30 Oct). Investigate registration/session identity; reported reproducer test_b20260831_silent_stub_gate.py (26 Sep/7 Oct). `b20261014-read-registration`

- **Retired-token substring matching rejects valid words and titles; match the intended lexical unit (26 Sep).** `b20261014-retired-substrings` Claude session, 16 Oct, reports a finding inside the cited Patel et al. article title in teaching/cmp; assess proper-name and citation handling alongside lexical matching.

- **The reported private-repository fiscal-identifier exception conflicts with the current secrets rule and PDF-twin ignore behavior. Resolve policy before changing either; bypass debt casinhas fa7244e (29 Sep).** `b20261014-private-pdf-policy`

- **Default gslides previews land in the workspace root, unlike Drive downloads; private-deck export lacks an authenticated path. The cross-filesystem move is already corrected (26 Sep).** `b20261014-slides-preview-export`

- **Presentation generation reads JSON instead of design-system tables; themes can diverge (26 Sep).** `b20261014-theme-input`

- **Reported slide references use inconsistent classification and generic descriptions; assess ownership and relevance descriptions without automatic YAML promotion (26 Sep).** `b20261014-slide-ref-metadata`

- **Verify transcript redaction of the authorization-code pattern reported in the Canva session; retain labels rather than credentials (26 Sep).** `b20261014-transcript-redaction`

- **File-description lookup and tracked-file validation use incompatible repository roots; neither accepts Virada pagina/frases.json.** Claude reports described.txt suffix matching against nested-repository-relative paths despite workspace-relative keys (administration,18 Oct; 1322,23 Oct). On 30 Oct, the PPC session reports partials/jsconfig.json fails by repository-relative path but works by absolute path; stubgen creates folder configs that trigger it. Its config-consolidation workaround is a report, not the root fix. Resolve roots; bypass debt e106d95 awaits regression coverage. `b20261014-nested-file-description`

- **Expanded hook-link verification becomes slow in duplication checking; isolate the cause before changing it (5 Oct).** `b20261014-verification-latency`

- **rtk rejects supported search flags; support them or show a working alternative (12 Oct).** `b20261014-search-flags`

- Cloned/shell-created directories do not refresh routing; compare disk independently of edit events. Claude 28 Oct: ai4good/artefatos routing gained tec/* only when flx committed; flx still absent, one turn late. Earlier manual resync: ce4d4ab7 (14 Oct). `b20261014-routing-cloned-dirs`

- bash-context-gate.py unnecessarily demands subtree context for binary metadata tools such as pdfinfo. Establish metadata/self-generated compiled-PDF exemptions separately from Python-script PDF detection (25 Sep/9 Oct). `b20260925-gate-binary-readonly`

- Marker/MinerU/Surya children retain VRAM after PDF-tool failure; verify deterministic child cleanup. Distinguish this from reported Docling exhaustion, screen-unlock failure and driver behavior; check simultaneous model residency (25 Sep). `b20260925-gpu-orphan-vram`

- Root pre-commit omits nested repos: cached removals/branch switches can silently delete tracked teaching files. Include quiet repositories; Claude restored administration mass deletions on 18 Oct, cause unknown. `b20260925-subrepo-tracked-deleted-sentinel`

- entropy_context.check_truncation flags any literal ellipsis in routing prose/titles. Restrict to actual truncation/description overflow; preserve intentional characters (3 Oct). `b20261003-check-truncation-ellipsis`

- Ignored outputs/.drafts and tmp research/benchmarks/Canva utilities do not sync between machines. Preserve reusable findings, inputs and provenance durably; keep credentials excluded. Reassess prototype tracking, lost conference twins and reported artifact limits (511/version,255/publication). 1322 source tracking resolved its own case; broader sync remains open. `b20260924-drafts-sync`

- line_counts.py, entropy_crowding.py and entropy_context.py use double-negative NOT REFUSED warnings. Audit against SCHEMA vocabulary and prefer affirmative ALLOWED wording (Lucas, 2 Oct). `b20261002-hook-warning-vocabulary`

- Goal backlogs and technical roadmaps duplicate/stale work; define capture versus execution ownership. rpg-isoroll still names painting in Foundry while content ROADMAP D8 chooses text-authored layouts and parks painting; align tracking without reopening design (29 Sep). `b20260929-task-roadmap-boundary`

- Antigravity lifecycle hooks start at HOME, so relative core/run blocks tool calls. Current fallback uses ~/workspace from sync-global-skills; prove dispatch from HOME via regression without authoring-mount paths (test_port_ceiling.py). `b20260925-antigravity-hook-cwd`

- Agents rewriting an old INBOX snapshot can overwrite concurrent captures. Bot locks, writes and reads back (f11a2334), but other writers need the same lock or fresh-read contract; lost 20 Sep captures were never committed. `b20260921-inbox-writers`

- Nonmedia fallback reads GitHub sign-in chrome instead of raw README and counts no text as ok. Reports add core/ mistaken as workspace root, Exec format error, JavaScript/PDF/HTTP handling, empty searches and concurrency failures; r.jina.ai blocked 12 Oct. Batch persistence/progress: b20261017-video-batch-results. `b20260921-fetch-fallback`

- SCHEMA underscore-template rule has no checker; teaching/structure/templates remains unmarked (AD-16). Decide whether enforcement earns its cost before rename; existing mechanisms otherwise correctly treat unmarked directories as instances. `b20260918-template-naming`

- Parallel sessions share index, branch and suite; unfinished work blocks unrelated commits and failures are misattributed. A previous bypass masked CRLF-on-staged-deletion and untracked-target checker faults and let core refs exceed cap. On 30 Oct, full-suite teardown guards blamed tests for concurrent changes in code/ppc and code/rastro-da-banca; assertion failures were cleared, but this prevented a green close. Verify branch/index scope and guard attribution; audit bypass scope. Worktree preparation remains in ROADMAP. `b20260918-shared-index`

- test_a_rebuilt_target_settles_in_one_pass rebuilds the real code/wos target (core/public.txt), alternately dirtying/failing subsequent serial runs. conftest tree guard misses gitignored nested repos; isolate the target and cover the guard (23 Sep; related b20260902). `b20260923-publish-test-real-target`

- Remaining ruled renames: shim→adapter, drift→divergence, corpus→tracked files, crowding→files per folder, drain→empty, sweep→scan, whitelist→allowed list. list/check/law/harness/boundary/surface need costed scope; some were chosen replacements despite Lucas finding them unclear. Keep legitimate multi-hop; remeasure with git grep (23 Sep). `b20260923-vocabulary-queue`

- Per-machine ignored scoreboard keys were migrated only here; other machine retains inbox-nudge/compass-nudge/publish-nudge after feature renames. Preserve history there and define migration for future versioned-key/per-machine-data asymmetry before interpreting the reading. `b20260920-scoreboard-keys`

- Nested entropy refreshes only on that repo commit; quiet reports age undetected despite printed dates. ai4good example on 20 Sep regenerated a 4 Sep snapshot. Add freshness interpretation without pretending root close scans nested repos. `b20260920-quiet-repo-entropy`

- Generated safe-to-delete branch lists age during the session and may name newly unmerged work. Recheck ancestry against origin/main at deletion and assess excluding branches whose tips moved; never execute snapshot advice blindly (14 Sep). `b20260914-branch-list-snapshot`

- Registry keys google-auth/notes-notion/link-shortener/wazip/video-text/asset-inspect/vpn-cin diverge from function-family names. Follow tools+skills merge precedent, update setup/profile/deps joins and retired-token rows. links collides with the norm in a flat namespace despite group distinctions; preserve that design question. `b20260915-feature-names-carry-vendors`

- Feature bot and crossing tree code/aiwbot use different names. Rename tree and all pointers together rather than claim the registry rename completed the family-name rule (17 Sep). `b20260917-bot-directory-keeps-vendor`

- foundry/iso-visual/prof cannot cross publicly, but registry crosses verbatim; removing their rows makes is_enabled fail open and leaves them unswitchable (AD-14). Filter registry by crossing policy and compare filtered text in _same; cut implementation before growth, assess rebuild.py as owner. `b20260917-private-skills-unswitchable`

- _present subtracts target gitignore, hiding newly refused files from sync cleanup. Old prof files remain locally ignored, not remotely leaked, and can resurface later. Delete generated absent/orphan entries while preserving IGNORE_HEAD exclusions; cut before implementation growth. `b20260917-refused-file-never-removed`

- publish --check/_same ignores generated blocks and reports clean for corrupted target blocks. Sync regenerates them, but check and roundup public status remain blind. Regenerate-and-compare writes, so decide honest sync/check reporting boundaries. `b20260917-check-blind-to-stale-block`

- Public authored prose promises absent private paths: README→brain/academy/branches/models, SETUP→academy, craft/tree→code/ROADMAP-spec-drive, hooks→ROADMAP-verify, goal headers→brain/goals. Generated ignore makes pointer checks green but readers still hit missing files; rewrite promises or deliberately ship dependencies. `b20260917-crossed-prose-broken-pointers`

- Read gate keys on path, demanding identical CONTEXT files again inside code/wos. Assess source-target equivalence through core/public.txt while retaining boundaries for genuinely different content (16 Sep). `b20260916-read-gate-charges-twice`

- Feature names opencode-plugin/antigravity-hooks diverge from harnesses.txt names opencode/claude/zcode/agents and the actual antigravity adapter path. Reconcile mechanism/vendor vocabulary rather than add another spelling. `b20260916-harness-names-four-ways`

- Paper tool services remain unavailable: Semantic Scholar 429/arXiv timeout (13 Sep). Dependency checks now call services and flows name venue-host web fallback; capability still missing, forcing per-page venue/review/citation checks. Recheck service and consider another provider. `b20260913-paper-search-has-no-arm`

- scoreboard.tsv grows append-only; read-matrix.tsv is bounded by day modulo 365; state markers prune after two days. Evaluate shared bounded aging after the scoreboard reading due 28 Sep. Claude 16 Oct reports test markers accumulating; reproduce with claude_nostub_missing-stub and verify teardown/pruning. `b20260922-state-stores`

- rtk git commit reports success after pre-commit refusal (24 Sep), with index unchanged and old HEAD. Send output to a file and verify actual git log until wrapper status propagation is corrected. `b20260924-rtk-commit-false-ok`

- Empty .git/.codex/.agents (also .aws) directories appear in tmp, root provider folders and isolated outputs after Codex. Sandbox mount-point origin is a hypothesis. is_repo now requires HEAD/file; directory writer/cleanup remains unresolved (7/23 Oct). `b20261007-empty-git-dirs`

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans this repo and no other. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-10-30 · 1186 tracked files scanned · **5 findings here** (2026-10-19: 5 · +0 over 11 days)

| Check | Findings |
|-------|----------|
| Off-allowlist `.md` types | 0 |
| CONTEXT.md hand-written inventories | 0 |
| Naming and placement | 0 |
| Routing tables pointing at files git does not carry | 0 |
| Projects not declaring their goal | 0 |
| Wiki-links naming nothing | 0 |
| Retired tokens still alive | 0 |
| Roadmap item numbers cited outside a roadmap | 0 |
| Items claimed by two lists | 0 |
| Size signals | 0 |
| Source files with no interface stub | 0 |
| Directories holding too many files | 3 |
| Prose describing finished work | 0 |
| Unanswered placeholders | 0 |
| Doubt stores missing their own discipline | 0 |
| Lists naming a model where they mean a level | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 0 |
| Constraints trapped in a CONTEXT.md head | 0 |
| Local branches holding unpromoted work | 0 |
| Work that exists on this disk and nowhere else | 0 |
| Local branches already merged into their base | 1 |
| Remote branches already merged into their base | 1 |

*A check with no findings is the `0` in that table and nothing more. Only a check with something to show gets a section below.*

### Directories holding too many files

*splitting costs one hop — pay it only when it removes more table than it adds*

- core/tools/slides — 13 code files in one directory. NOT REFUSED — this is the warning at 10. Nothing stops until 15; split by responsibility if the split removes more table than the hop adds
- core/tools/test — 15 code files in one directory. NOT REFUSED — this is the warning at 10. Nothing stops until 15; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace — 11 code files in one directory. NOT REFUSED — this is the warning at 10. Nothing stops until 15; split by responsibility if the split removes more table than the hop adds

### Local branches already merged into their base

*safe to delete, and purely local — `git -C <repo> branch -d <branch>`*

- . — 3 merged into main: git -C . branch -d feature/ementas-lc feature/goals-roadmap feature/pdf-twin

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 5 merged into main: git -C . push origin --delete feature/disk-hygiene feature/ementas-lc feature/goals-roadmap feature/pdf-twin feature/virada-semana-final

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-10-30 · `verify.py full` · **green (25 passed, 1122 deselected in 5.53s · 1121 passed, 1 skipped in 188.72s (0:03:08))**
<!-- verify:end -->
