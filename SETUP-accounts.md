# Setup — outside accounts
> Everything that reaches a service off this machine: web search, the shared Google OAuth behind six
> tools, the Forms API's separate project, the Telegram capture bridge, and the CIn VPN. Five of the
> six need a human for one browser action or one password, and each says exactly which one.
> feature: web-search, google-auth, forms, telegram-capture, vpn-cin
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

## VPN do CIn
> feature: `vpn-cin` · agent: no

IKEv2 through strongSwan to `vpn.cin.ufpe.br`, full tunnel, parameters from
[the CIn helpdesk](https://helpdesk.cin.ufpe.br/servicos/conectividade/vpn) § IKEv2 → Linux Manual
— the PET *Manual de Sobrevivência* is stale and only points there, and
`/redes/vpn` (L2TP, PPTP) is retired. **`network-manager-l2tp` must stay uninstalled**, the
helpdesk's own first cause of "connects but does not browse". The tunnel carries IPv4 only, so the
dispatcher blackholes IPv6 while it is up; without it every AAAA site is reached from the local
address and institutional access is silently not recognised.

**Needs you:** the CIn domain password, typed into the NetworkManager prompt. Nothing stores it —
`password-flags=2` asks every time and this file carries only the label. The account is Active
Directory: **stop after two failed attempts** and reset at <https://account.cin.ufpe.br>, because a
locked account and a wrong password fail identically and guessing is what locks it.

**Precondition** `nmcli -g NAME connection show | grep -qx VPN-CIn`

**Install**
```bash
sudo apt install -y network-manager-strongswan libstrongswan-extra-plugins libcharon-extra-plugins
nmcli connection add type vpn con-name VPN-CIn ifname '*' vpn-type strongswan autoconnect no \
  ipv4.method auto ipv6.method disabled ipv4.ignore-auto-dns yes \
  ipv4.dns '172.21.2.151,172.21.2.152,172.21.2.153' \
  ipv4.dns-search 'cin.ufpe.br,windows.cin.ufpe.br'
for kv in address=vpn.cin.ufpe.br method=eap user=lsf virtual=yes encap=no ipcomp=no \
          proposal=yes ike=aes256-sha256-modp2048 esp=aes256-sha256-modp2048 password-flags=2; do
  nmcli connection modify VPN-CIn +vpn.data "$kv"
done
sudo tee /etc/NetworkManager/dispatcher.d/90-vpn-cin-ipv6 >/dev/null <<'EOF'
#!/bin/sh
# The CIn VPN tunnels IPv4 only; without this, IPv6 leaves on the local address.
[ "$CONNECTION_ID" = "VPN-CIn" ] || exit 0
case "$2" in
  vpn-up)   ip -6 route replace blackhole ::/0 metric 1 ;;
  vpn-down) ip -6 route del blackhole ::/0 metric 1 2>/dev/null || true ;;
esac
EOF
sudo chmod 0755 /etc/NetworkManager/dispatcher.d/90-vpn-cin-ipv6
```

**Verify** — `nmcli --ask connection up VPN-CIn`, then all three:
```bash
curl -4 -s https://ifconfig.me            # 150.161.2.x, reverse Net-ExtVPN-extIP.cin.ufpe.br
getent hosts virtualdisk.cin.ufpe.br      # 172.21.2.20 — internal name resolves
curl -6 -s --max-time 5 https://ifconfig.me || echo "IPv6 blocked — correct"
```
`journalctl -u NetworkManager -n 80 | grep -iE 'charon|eap|ike'` names a failure:
`AUTHENTICATION_FAILED` is the password, an `IKE_SA` retransmit is the provider blocking UDP
500/4500 — then `nmcli connection modify VPN-CIn +vpn.data encap=yes`.

<!-- steps:end -->
