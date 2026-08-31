# Workspace Setup
> How to make this environment work on a new machine: toolchain install and per-machine config.

What the workspace *is* and what each feature buys you: [`README.md`](README.md). What the gates
enforce: [`core/hooks/SPECS.md`](core/hooks/SPECS.md). This file is only the install.

**This file is a procedure an agent executes, not prose a human reads and improvises from.** You
cloned the repo and opened your own coding agent; *that agent* is the installer. There is no
`curl | sh` and there is not going to be one — an installer would have to be ported to every
harness, while a procedure works on whichever one you already opened. `/install` is a doorway into
this file for agents that support skills; it adds nothing, and this file never depends on it.

**Every step below has the same parts, and an agent runs them in this order:**

| Part | Contract |
|---|---|
| `> feature:` | which feature the step installs. Skip the step, lose exactly that feature |
| `> substrate: yes` | installs no feature — it installs what every feature *runs on*. Skip it and nothing works, so there is nothing to ablate and no registry row |
| **Precondition** | a command that says whether the step is *already done*. Run it first, always |
| **Install** | idempotent. Running it twice must be a no-op, never a second copy |
| **Verify** | a command proving the thing works. **A step is done when its probe passes, never when its config looks right** |

`agent: no` marks the short list an agent cannot finish **alone** — an API key, a consent screen, a
device pairing. It has never meant the agent steps back. **Every step here is agent-guided,
including the ones the agent cannot finish**: it runs everything it can, and then hands the human
the one remaining part, already set up and named as a single action.

That last part takes whichever of two shapes the thing itself has. When it is a **secret**, ask for
the secret and write the config yourself — never hand over a command to run for something you could
have run. When it is an **act only a person can perform** — authorising in a browser, accepting a
consent screen, choosing between options only they can weigh — give the exact command or click,
say what will happen next, and then verify the result yourself.

What never changes is that the human receives **one action, not an investigation**. A step that
leaves someone reading documentation to work out what to do has not been installed; it has been
delegated. Everything else, run without asking.

`substrate` marks a step that installs no feature, and the distinction is the ablation's rather
than bookkeeping (2026-08-17): switching off the interpreter the switch itself runs on produces no
signal. Third-party machine state this workspace does not author is a step here plus a
`core/tools/deps.txt` line, never a feature.

There used to be a second substrate step, § Workspace path, which rewrote an absolute venv shebang
into all 33 tools on every clone. It is gone (2026-08-29): a per-machine value in a versioned file
is the defect `core/run` exists to remove, and an install step that repairs it every time is the
symptom, not the cure.

**Sections are named, never numbered** — a number is a pointer that goes stale the first time a
step is added, and two of them already had. Everything here is per-machine state git cannot carry;
everything else is versioned, because the file system is the source of truth.

## Already wired — nothing to do

Versioned, and they activate on their own after a clone. Listed so a newcomer does not go looking
for an install step; they are not steps and have no probes.

| Feature | Why nothing is needed |
|---|---|
| Claude Code hooks | `.claude/settings.json` is in the repo; Claude Code reads it when the workspace is opened, and `core/hooks/` activates immediately |
| ZCode hooks | `.zcode/config.json` is in the repo and ZCode reads it at every session start — but project-scope hooks stay **inert until the workspace is trusted in the client** (one-time, per machine; `agent: no` — open the workspace in ZCode and accept the trust prompt). Until then zcode enforces nothing at edit time; the git gates still fire |
| opencode policy plugin | `.opencode/plugins/workspace-policy.js` is a project-level plugin, auto-loaded from the workspace root. Helpers live in `.opencode/wp-helpers.js`, outside `plugins/` so opencode does not load them as a second plugin |
| Antigravity hooks | `.agents/hooks.json` is in the repo; Antigravity / Gemini reads it on startup and delegates lifecycle events to `core/hooks/antigravity/antigravity_policy.py` |
| Copilot hook registration | `.github/hooks/workspace-policy.json` and `.github/hooks/rtk-rewrite.json` are inert config files until Copilot itself is installed |
| The feature registry | `core/features.txt` and `core/profile.txt` are versioned, and `core/hooks/feature_law.py` reads them where they sit |

The one exception is rtk for Claude Code: its code is versioned but its registration is not, which
is why § RTK — Claude Code registration is a step.

**Before running the steps, read your profile** — it decides which of them you need, and
`core/features.txt` says what each feature buys, so a step is judged before it is run.

```bash
core/run tools/wos/features                 # every feature, grouped, with your answer
core/run tools/wos/features --off <slug>    # one you do not want; its install step is then moot
```

<!-- steps:start -->

## Agent permissions
> feature: `permissions` · agent: yes

**This step runs first, and its position is the point.** Every step below is an agent editing files
and running commands; how often it has to stop and ask is decided here. Left unset, the newcomer
answers that question one prompt at a time, under time pressure, by approving whatever is in front
of them — which is how the allowlist on the machine that wrote this step came to hold nine entries
that were whole command lines, matching nothing and asking again every time.

The levels and what each one costs are declared in [`core/permissions.txt`](core/permissions.txt),
in one sentence each. **Read them out and let the person choose**; never summarise them here, or
this file becomes a second copy that disagrees with the first.

**Precondition**
```bash
core/run tools/wos/permissions --check     # exit 0 = a level is answered and rendered
```

**Install** — idempotent. It installs the safest level **without asking**, so a clone with nobody
watching still ends up configured, and only then offers the choice:
```bash
core/run tools/wos/permissions --set guarded    # safe default, no question asked
core/run tools/wos/permissions                  # print the levels; offer to raise it
```

**Verify**
```bash
core/run tools/wos/permissions --check
```

The policy is versioned; the rendered config is not. `core/permissions.txt` is in git so a reviewer
can read what this workspace permits, while `.claude/settings.local.json` is git-ignored because it
is an answer about one machine — a versioned `bypassPermissions` would arrive switched on for
whoever cloned next.

## The venv
> substrate: yes · agent: yes

One virtualenv at the workspace root, shared by every tool and the suite. `code/*` repos own theirs.

The venv keeps its executables in a directory whose name differs per machine, so nothing below
spells it: `sh core/run --python` prints this clone's interpreter and exits non-zero when there
isn't one, which makes it both the precondition and the path. Steps here used to name that
directory outright and therefore could not run on a clone that was not the authoring machine.

**Precondition** `sh core/run --python`

**Install** — `python3` is the creating interpreter and comes from the system, not the venv:
```bash
python3 -m venv .venv              # no-op if .venv already exists
"$(sh core/run --python)" -m pip install --upgrade pip
```

**Verify** `"$(sh core/run --python)" -c "import sys; print(sys.prefix)"` — this `.venv`, not the
system prefix.

## Declared dependencies
> feature: `declared-deps` · agent: yes

[`core/tools/deps.txt`](core/tools/deps.txt) declares every external dependency with its install
command, its probe, and **what its absence looks like** — a missing dep makes a tool return a worse
answer rather than an error. The rule: [`core/tools/SPECS.md`](core/tools/SPECS.md) § Declared
dependencies.

**Precondition** — also the install plan, in one command:
```bash
core/run tools/wos/deps            # every dep, ok/MISSING, with the install line for each miss
```

**Install** — run what it printed. Rows marked `apt` need `sudo`; if you cannot get it, hand that
row to Lucas, naming the package and the `breaks` line printed beside it.

**Verify** `core/run tools/wos/deps --check` — exit 0 means nothing is missing.

## GitHub account
> feature: `github-auth` · agent: no

Runs next to the git hook because that hook is what makes it urgent: `core/hooks/post-commit`
auto-pushes every `feature/*` branch, so an unauthenticated clone finds out at its first commit.
`/roundup` cannot promote either, and the agent loses PRs and issues — it ends up asking you to
paste output from a browser, which is the shape this whole file exists to avoid.

**Precondition**
```bash
gh auth status                     # a logged-in host means this step is done
```

**Install** — the agent installs the CLI, and **`gh auth login` is the one part it cannot do**: the
device flow needs a terminal it can type into. There is nothing to choose and nothing to paste back.
```bash
core/run tools/wos/deps --feature github-auth    # prints the install line for THIS machine's manager
```

**Needs you:** one command, in your own terminal, and nothing else — hand over exactly this:

> Run `gh auth login`. Pick **GitHub.com**, then **HTTPS**, then **Login with a web browser**. It
> shows an eight-character code, opens GitHub, and you paste the code and approve.

Wait for them, then finish it yourself — this part is not theirs:
```bash
gh auth setup-git                  # registers gh as git's credential helper, which fixes push
```

**Verify** — both halves, because authentication and pushing fail separately:
```bash
gh auth status
git push --dry-run origin HEAD
```

`gh` is a declared dependency, so its absence is reported by `core/run tools/wos/deps` like any other,
and its probe is `gh auth status` rather than `gh --version` on purpose: a CLI installed but not
logged in breaks every line of the `breaks` column just as completely as one that is missing.

## Git hook
> feature: `git-hooks` · agent: yes

Applies `core/hooks/pre-commit` to **every** repo on the machine — that global reach is the point,
since projects under `code/` are their own repos.

**Precondition** `git config --global core.hooksPath`

**Install**
```bash
git config --global core.hooksPath "$PWD/core/hooks"
```

**Verify** `test -f "$(git config --global core.hooksPath)/pre-commit" && echo "hook reachable"` —
the path must resolve to a dispatcher, not just be a string.

## Executable bits
> feature: `git-hooks` · agent: yes

Git carries the execute bit, so a normal clone arrives correct. This step is for an archive export,
a filesystem that drops modes, a `umask` that strips it.

**Only the shell entrypoints git or a harness starts by path need a bit.** Nothing under
`core/tools/` does: those are spawned as `core/run tools/<family>/<leaf>`, so the interpreter is
named by the launcher and the bit is not consulted. This step used to `chmod +x` them and verify
that every extensionless file under `core/tools` carried one — a check that could only ever pass
on the machine it was written on, since the execute bit is not a permission Windows has.

**Precondition** `test -x core/hooks/pre-commit && test -x core/hooks/post-edit.sh && echo "set"`

**Install** — idempotent by nature:
```bash
chmod +x core/hooks/post-edit.sh core/hooks/read/pre-read.sh core/hooks/pre-commit \
         core/hooks/post-commit core/hooks/copilot/copilot-agent.sh \
         core/hooks/session/start-session.sh
```

**Verify** `find core/hooks -type f -name "*.sh" ! -perm -u+x` — no output. Any line is a file
that will fail to run.

## Skill mirrors
> feature: `skill-mirrors` · agent: yes

Every harness looks for skills in its own directory, so `core/skills/<name>.md` is published as a
copy into `.claude/skills/`, `.opencode/skills/`, `.zcode/skills/` and `.claude/commands/`. **Those
copies are generated and git does not track them**, which is why this step is not optional: a fresh
clone has the sources and none of the copies, so every `/<skill>` is missing until it runs.

They were symlinks until 2026-08-29. `ln -s` under Git Bash silently copies unless
`MSYS=winsymlinks:nativestrict`, which needs Developer Mode — a machine-level privilege out of
proportion to what this workspace is. Copying removes the per-OS axis instead of adding an arm for
it, and what the symlink bought was freshness, which is now regeneration at the moments that change
a skill: this step, the post-edit hook, and the pre-commit generator.

**Precondition** `bash core/tools/wos/sync-skills --check`

`bash …`, not `core/run …` and not `sh …`: the launcher execs its target with **Python**, and these
two tools are the workspace's only bash ones — while on POSIX `sh` is dash, which has no arrays and
dies on their first line. Everything else under `core/tools/` is spelled `core/run tools/…`.

**Install** — idempotent; it also prunes mirrors whose source skill is gone or switched off:
```bash
bash core/tools/wos/sync-skills
```

**Verify** `bash core/tools/wos/sync-skills --check` — prints `OK: all mirrors and command files in
sync`. Any `MISSING` / `STALE` / `ORPHAN` line names the file and the source it disagrees with.

## Python interfaces — stubgen
> feature: `interface-stubs` · agent: yes

Generates the `.pyi` stubs the read gate hands an agent instead of a source file.

`stubgen` is a console script inside the venv and has no `-m` form, so it is located rather than
spelled: `sh core/run --script stubgen` prints its path on any machine.

**Precondition** `"$(sh core/run --script stubgen)" --version`

**Install**
```bash
"$(sh core/run --python)" -m pip install mypy
```

**Verify** `"$(sh core/run --script stubgen)" -o "$(mktemp -d)" core/hooks/file_law.py` — it must
produce a stub, not merely answer `--version`.

## TypeScript interfaces — tsc
> feature: `interface-stubs` · agent: yes

The hook checks `tsc` on `PATH` first, then `~/.local/bin/tsc`, so either location works.

**Precondition** `tsc --version || ~/.local/bin/tsc --version`

**Install** — needs Node (`node --version`); install it with `nvm` if absent:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc && nvm install --lts
npm install -g typescript                    # if this needs sudo: --prefix ~/.local
```

**Verify** `tsc --version`

## ESLint + Prettier for TypeScript projects
> feature: `lint-typescript` · agent: yes

Project-local, in every TS project carrying an `eslint.config.js`; each imports `code/eslint.shared.js`
and runs via `node_modules/.bin/eslint`. No global install.

**Precondition** `ls code/isoroll-module/node_modules/.bin/eslint code/voti/node_modules/.bin/eslint`

**Install**
```bash
(cd code/isoroll-module && npm install)
(cd code/voti && npm install)
```

**Verify** — the gate must *bite*, not merely run:
```bash
printf '// test\nconst x = foo(bar());\n' > /tmp/test-lint.ts
(cd code/isoroll-module && node_modules/.bin/eslint /tmp/test-lint.ts)   # expect: 2 calls in one statement
```

## LaTeX toolchain
> feature: `latex` · agent: yes

For `academy/papers/`. The procedure is [`academy/SETUP.md`](academy/SETUP.md), which answers a
question no workspace-level install covers.

**Precondition** `pdflatex --version | head -1`

**Install** — follow [`academy/SETUP.md`](academy/SETUP.md).

**Verify**
```bash
cd academy && make -n 2>/dev/null | head -3 || pdflatex --version | head -1
```

## RTK
> feature: `rtk-compaction` · agent: yes

[rtk-ai/rtk](https://github.com/rtk-ai/rtk) — a Rust proxy that compresses dev-command output (git,
test runners, docker) before it reaches the context: 60-90% savings. Complementary to caveman,
which compresses the agent's *own* output. Apache 2.0, one static binary, no deps.

⚠ **Name collision.** If `rtk gain` reports an unknown subcommand, the installed binary is
reachingforthejack/rtk, a different tool with the same name. Check `which rtk`.

**Precondition** `rtk --version && rtk gain --help >/dev/null && echo "rtk present"`

**Install**
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh   # → ~/.local/bin/rtk
```

**Verify** `rtk gain` — a savings table, not an error.

## RTK — Claude Code registration
> feature: `rtk-compaction` · agent: yes

**One registration, and it must be the shim** — registered **globally**, because Claude Code runs
*all* matching hooks and a global entry also covers sessions started inside nested `code/*` repos.
Why a shim rather than `rtk hook`, which rewrites line 1 only:
[`core/hooks/compact/SPECS.md`](core/hooks/compact/SPECS.md).

⚠ **Never run `rtk init --global --auto-patch` here.** It reverts the entry to `rtk hook claude`,
silently dropping multi-line compaction, and `rtk init --show` reports both wirings as configured.

**Precondition** `grep -c bash-compact-rewrite ~/.claude/settings.json` — one match when done.

**Install** — idempotent; replaces any existing `Bash` entry rather than appending:
```bash
"$(sh core/run --python)" - <<'PATCH'
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
d = json.loads(p.read_text())
shim = f'sh {pathlib.Path.cwd()}/core/run hooks/compact/bash-compact-rewrite.py'
pre = d.setdefault('hooks', {}).setdefault('PreToolUse', [])
entry = next((e for e in pre if e.get('matcher') == 'Bash'), None)
if entry is None:
    pre.append({'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': shim}]})
else:
    entry['hooks'] = [{'type': 'command', 'command': shim}]
p.write_text(json.dumps(d, indent=2) + '\n')
PATCH
```

**Verify** — end to end. **Config alone proves nothing**, and this is the step that taught this
file that rule.
```bash
printf '%s' '{"hook_event_name":"PreToolUse","tool_name":"Bash","session_id":"probe",
"tool_input":{"command":"cd core\ngit status\nls -la"}}' \
  | sh core/run hooks/compact/bash-compact-rewrite.py
# expect: cd core / rtk git status / rtk ls -la  — lines 2 and 3 are what raw rtk drops
```

## RTK — other agents
> feature: `rtk-compaction` · agent: yes

Skip whichever you do not use. Pi and Feynman need the local `package.json`: their loader resolves
the generated `rtk.ts`'s import as a real `require()`, relative to the extension's own directory.

**Precondition** `ls ~/.config/opencode/plugins/rtk.ts ~/.pi/agent/extensions/rtk.ts 2>/dev/null`

**Install**
```bash
rtk init --global --opencode        # writes ~/.config/opencode/plugins/rtk.ts
rtk init --agent pi --global
mkdir -p ~/.pi/agent/extensions && cd ~/.pi/agent/extensions
echo '{"name":"pi-extensions-peer-deps","private":true}' > package.json
npm install @earendil-works/pi-coding-agent
mkdir -p ~/.feynman/agent/extensions && cp ~/.pi/agent/extensions/rtk.ts ~/.feynman/agent/extensions/
cd ~/.feynman/agent/extensions && cp ~/.pi/agent/extensions/package.json .
npm install @earendil-works/pi-coding-agent
```

**Verify** `pi -e ~/.pi/agent/extensions/rtk.ts --no-session` — silence and exit 0 means loaded.
Feynman has no dry-run flag; its only signal is the **absence** of `[rtk] rtk binary not found` on
the first real session, so treat it as unverified. Uninstall any target:
`rtk init --uninstall [--global] [--copilot|--opencode|--agent pi]`.

## Caveman
> feature: `caveman` · agent: yes

Output compression, ~65% of the agent's own output. **Vendored** since 2026-07-23 — source of truth
[`core/skills/caveman/`](core/skills/caveman/CONTEXT.md), upstream credit
[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). **Do not run the upstream
installer**: it replaces the links with copies and re-forks both installs. Needs Node ≥ 18.

**Precondition** `bash core/tools/wos/sync-global-skills --check`

**Install** — the links, then the config every agent reads:
```bash
bash core/tools/wos/sync-global-skills           # links ~/.agents/skills/caveman + ~/.claude/hooks/caveman-*
mkdir -p ~/.config/caveman && echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
```
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\caveman" | Out-Null
'{"defaultMode": "full"}' | Set-Content "$env:USERPROFILE\.config\caveman\config.json"
```

If `~/.claude/settings.json` did not come across from the old machine, add its three entries:
`SessionStart` → `caveman-activate.js`, `UserPromptSubmit` → `caveman-mode-tracker.js`,
`statusLine` → `caveman-statusline.sh`. Modes: `lite`, `full`, `ultra`, `off`.

**Verify** — open a Claude Code session; the `[CAVEMAN] ⛏` badge appears in the statusline.

**Wiring a new agent** — either **installed**, session-start hooks calling `caveman-activate.js`
(Claude Code), or **induced**, a session-start shim injecting the rules as context (Copilot, via
`core/hooks/copilot/copilot-session-start.py`). Both read that one config file, so one toggle
controls every agent. Follow the induced pattern by hand.

## Caveman shell helper
> feature: `caveman` · agent: yes

**Precondition** `grep -q "caveman-compress()" ~/.bashrc && echo "already appended"`

**Install** — guarded by the precondition; appending twice defines the function twice.
```bash
cat >> ~/.bashrc << EOF

# caveman-compress shortcut. The root is baked in at install time because ~/.bashrc lives
# outside the repo; the interpreter is asked for, never spelled `python3`.
caveman-compress() {
  local CLAUDE_BIN
  CLAUDE_BIN="\$(dirname "\$CLAUDE_CODE_EXECPATH")"
  (cd $PWD/core/skills/caveman && PATH="\$CLAUDE_BIN:\$PATH" "\$(sh $PWD/core/run --python)" -m scripts "\$1")
}
EOF
source ~/.bashrc
```
```powershell
Add-Content $PROFILE @'
function caveman-compress {
    param([string]$File)
    $claudeBin = Split-Path $env:CLAUDE_CODE_EXECPATH
    Push-Location "$env:USERPROFILE\.claude\skills\caveman"
    $env:PATH = "$claudeBin;$env:PATH"
    python3 -m scripts $File
    Pop-Location
}
'@
```

**Verify** `type caveman-compress` — expected: "caveman-compress is a function".

## Web search
> feature: `web-search` · agent: yes

[`core/tools/web/search`](core/tools/web/search) is the single entrypoint for every agent — no MCP,
no per-agent wiring — and resolves its own backend, so picking a search CLI stays inside one script
instead of in every agent's prompt. It works with no key through ddgr; Exa is the optional upgrade
below. DuckDuckGo answers HTTP 202 with an empty body under load, so the fallback retries with
backoff (`WEB_RETRIES`, default 5) and exits non-zero with `all backends failed` when both die.

**Precondition** `ddgr --version` — expected 2.2 or later.

**Install**
```bash
sudo apt install -y ddgr                           # or: pipx install ddgr
```

**Verify** `core/run tools/web/search "test query" --backend ddgr --n 3`

## Exa API key
> feature: `web-search` · agent: no

Optional. Upgrades search quality; without it ddgr serves every call.

**Needs you:** an API key from the [Exa dashboard](https://exa.ai). Ask for the key itself and
write it yourself — never hand him a command.

**Install** — once he pastes the key:
```bash
mkdir -p ~/.feynman
printf '{"exaApiKey": "%s"}\n' "$KEY" > ~/.feynman/web-search.json    # key via env, never argv
```

**Verify** `core/run tools/web/search "test query" --n 3` — auto-picks Exa when the key is present.

## Google account access
> feature: `google-auth` · agent: no

Shared OAuth for `mail/gmail`, `calendar/gcalendar`, `files/gdrive`, `slides/gslides`, `docs/gdocs`
and `forms/gforms`. Tokens live at `~/.config/workspace-<service>/`, dir `700` / file `600`; Drive,
Slides, Docs and Forms keep a write token separate from their read one. An expired token names its
own fix — relay it verbatim: [`core/tools/SPECS.md`](core/tools/SPECS.md) § An auth failure names
its own fix.

**Needs you:** the consent screen is a browser interaction nobody can click for him. Run the
install, hand him the URL it prints, ask for the code it returns. Everything either side is yours.

**Precondition** `core/tools/calendar/gcalendar upcoming --days 1` — a listing means auth is live.

**Install**
```bash
core/run tools/mail/gmail sync --since 1               # prompts the consent flow on first run
```

**Verify** `core/tools/mail/gmail sync --since 1 && core/tools/calendar/gcalendar upcoming --days 7`

## Google Forms API
> feature: `forms` · agent: no

One switch per API, inside the GCP project owning the OAuth client: consent alone is not enough, a
disabled API answers `SERVICE_DISABLED` whatever the scopes say. **Enable an API in the project the
tool actually authenticates against** — `forms` and `docs` read their own credential from
`~/.config/workspace-<service>/` and run on a different project from everything else, per
[`core/tools/forms/SPECS.md`](core/tools/forms/SPECS.md) and
[`core/tools/docs/SPECS.md`](core/tools/docs/SPECS.md).

**Needs you:** in console.cloud.google.com as `lsf.cin@gmail.com` — create a project, enable
**Google Forms API** and **Google Drive API**, configure the auth platform (External, himself as
test user), create an **OAuth client → Desktop app**, download its JSON. A 403 names a project by
*number* while the console lists ids, so resolve it through `project_id` in the matching
`credentials.json` before sending him anywhere.

**Precondition** `core/tools/forms/gforms read --account personal <form_id>` — an outline means on.

**Install**
```bash
core/run tools/forms/gforms auth personal --write        # prompts the consent flow on first run
```

**Verify** `core/tools/forms/gforms new --account personal <spec.json>`

## Telegram bot — `code/aiwbot`
> feature: `telegram-capture` · agent: no

The Telegram bridge lives in [`code/aiwbot`](code/aiwbot/CONTEXT.md) as the systemd `--user` service
`aiwbot`: it captures text, photo, voice and document into `brain/INBOX.md` and drives coding agents
remotely.

**Needs you:** a bot token from BotFather, and the pairing — he must message the bot once so its
`allowed_chat_id` is captured. Tokens are guessable by username, so that allowlist is the only thing
between a stranger and writes into `brain/INBOX.md`. Ask for the token; write
`~/.config/workspace-aiwbot/config.json` yourself, dir `700` / file `600`.

**Precondition** `systemctl --user status aiwbot --no-pager | head -3`

**Install** — the unit lives outside the repo, at `~/.config/systemd/user/aiwbot.service`:
```bash
systemctl --user daemon-reload
systemctl --user enable --now aiwbot
```

**Verify** — send a message from the paired chat and confirm the entry lands in `brain/INBOX.md`;
`journalctl --user -u aiwbot -n 50` if it does not.

<!-- steps:end -->

## Verification

Does the install work? This is the whole-install probe; each step's own Verify is above.

```bash
core/run tools/wos/deps --check                           # every declared dependency present
git config --global core.hooksPath                    # the global gate is wired
"$(sh core/run --script stubgen)" --version && tsc --version   # interface generators are reachable
node --input-type=module -e "import('$PWD/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"
# Expected: function
./verify.py fast                                      # the workspace's own suite
```

Whether each *gate* then behaves as promised is a different question, answered by
[`core/hooks/SPECS.md`](core/hooks/SPECS.md) § What a working install looks like.

## Per-project setup

Each project under `code/` is its own git repo and owns its environment. A project whose setup
cannot be inferred from its code carries its own `SETUP.md`.

- [`code/SETUP.md`](code/SETUP.md) — per-language quick start, facade templates, codegraph
- [`academy/SETUP.md`](academy/SETUP.md) — LaTeX toolchain, paper compilation
- [`core/tools/video/SETUP.md`](core/tools/video/SETUP.md) — the video tool's model and cookie state
