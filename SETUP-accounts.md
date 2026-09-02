# Setup — outside accounts
> Everything that reaches a service off this machine: web search, the shared Google OAuth behind six
> tools, the Forms API's separate project, and the Telegram capture bridge. Four of the five need a
> human for one browser action, and each says exactly which one.
> feature: web-search, google-auth, forms, telegram-capture
> enforced-by: core/tools/test/workspace/test_setup_executable.py

The five-part contract, and the rule for what the agent hands over: [`SETUP.md`](SETUP.md). Secrets
are asked for and written by the agent; only the click is the human's.

<!-- steps:start -->

## Web search
> feature: `web-search` · agent: yes

[`core/tools/web/search`](core/tools/web/search) is the single entrypoint for every agent — no MCP,
no per-agent wiring — and resolves its own backend. It works with no key through ddgr; Exa is the
optional upgrade below. DuckDuckGo answers HTTP 202 with an empty body under load, so the fallback
retries with backoff (`WEB_RETRIES`, default 5) and exits non-zero with `all backends failed`.

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
and `forms/gforms`. Tokens live at `~/.config/workspace-<service>/`, dir `700` / file `600`. An
expired token names its own fix — relay it verbatim:
[`core/tools/SPECS.md`](core/tools/SPECS.md) § An auth failure names its own fix.

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
tool actually authenticates against** — `forms` and `docs` run on a different project from
everything else, per [`core/tools/forms/SPECS.md`](core/tools/forms/SPECS.md).

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
