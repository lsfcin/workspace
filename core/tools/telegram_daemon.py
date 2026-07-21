#!/mnt/workspace/.venv/bin/python3
# telegram_daemon.py — long-running Telegram bot: captures messages into brain/INBOX.md
# and dispatches /-commands to control Claude Code sessions headlessly.
import asyncio, html, json, os, pathlib, random, re, shutil, signal, sys
from datetime import datetime
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, ContextTypes

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import telegram_config, attachments_util

BRAIN_ATTACHMENTS = pathlib.Path("/mnt/workspace/brain/attachments")
INBOX_FILE = pathlib.Path("/mnt/workspace/brain/INBOX.md")
INBOX_MARKER = "<!-- add entries below, newest first -->"
WORKSPACE_DIR = "/mnt/workspace"
TRANSCRIPTS_DIR = pathlib.Path.home() / ".claude/projects/-mnt-workspace"
TELEGRAM_MSG_LIMIT = 4096
NOTIFY_POLL_SECONDS = 20
REPLY_MAP_MAX = 50
NEW_SESSION_CHECKPOINTS = (2, 5, 10, 30, 60)
DEFAULT_SELECT_COUNT = 5
SESSION_ID_LABEL_LEN = 3
NOTIFY_PUSH_TRUNCATE = 1000

# Phrase banks — natural-language variants, picked at random per message.
_CAPTURE_ACKS = [
    "Guardado em brain/INBOX.md.",
    "Adicionado ao INBOX.md.",
    "Salvo em brain/INBOX.md.",
    "Enviado para o INBOX.md",
    "Registrado em brain/INBOX.md.",
]
_NEW_STARTED_PHRASES = [
    "Sessão iniciada — agora é a ativa.",
    "Sessão criada e selecionada.",
    "Nova sessão no ar, já selecionada.",
    "Iniciada. Selecionada.",
    "Comecei a sessão — ela é a ativa agora.",
]
_NEW_UNCONFIRMED_PHRASES = [
    "Disparei, mas não consegui confirmar o id da sessão nova — tenta /select.",
    "Não achei a sessão nova depois de 60s — dá uma olhada no /select.",
    "Rodou, mas não confirmei qual sessão é — confere no /select.",
    "Sem confirmação do id novo depois de 1 minuto — check /select.",
    "Disparado, só não consegui achar o id — veja no /select.",
]
_NEW_EMPTY_PROMPT_PHRASES = [
    "Manda o prompt junto: /new <o que você quer que essa sessão faça>",
    "Faltou o prompt — /new precisa de um texto depois, tipo /new revisa esse arquivo",
    "/new sem prompt não dispara nada. Escreve o que quer depois do comando.",
]
_NEW_DISPATCH_FAILED_PHRASES = [
    "Não consegui nem disparar a sessão:",
    "Falhou já no disparo:",
    "Deu erro antes de criar a sessão:",
]
_SELECT_EMPTY_PHRASES = [
    "Nenhuma sessão ativa agora.",
    "Não tem sessão rodando no momento.",
    "Sem sessões ativas pra mostrar.",
    "Nenhuma sessão encontrada.",
    "Zero sessões ativas agora.",
]
_SELECT_UNRESOLVED_PHRASES = [
    'Não achei sessão única com "{p}" — confere no /select.',
    'Não bateu nenhuma sessão com "{p}".',
    '"{p}" não identifica uma sessão só — tenta de novo.',
    'Nenhuma ou mais de uma sessão bate com "{p}".',
    'Não consegui resolver "{p}" pra uma sessão única.',
]
_SELECT_LIST_PHRASES = [
    "Sessões recentes:",
    "Escolhe uma sessão:",
    "Aqui estão as últimas sessões:",
    "Qual sessão?",
    "Sessões disponíveis:",
]
_SELECT_TAP_PHRASES = [
    "Sessão selecionada.",
    "Essa é a ativa agora.",
    "Selecionei essa sessão.",
    "Pronto, essa é a ativa.",
    "Ok, focando nessa sessão.",
]
_NOTIFY_ON_PHRASES = [
    "Notificações ativadas — aviso quando qualquer sessão terminar uma resposta.",
    "Ativado — vou avisar a cada resposta terminada, de qualquer sessão.",
    "Notify ligado — sessões que terminarem vão te avisar aqui.",
    "Ativei os avisos automáticos de sessões.",
    "Ligado — qualquer sessão que terminar eu aviso.",
]
_NOTIFY_OFF_PHRASES = [
    "Notificações desativadas.",
    "Desligado — sem avisos automáticos agora.",
    "Notify off — paro de avisar.",
    "Desativei os avisos.",
    "Ok, sem mais avisos automáticos.",
]
_NOTIFY_USAGE_PHRASES = [
    "Uso: /notify on ou /notify off",
    "Manda /notify on ou /notify off.",
    'Só aceito "on" ou "off" depois de /notify.',
    "/notify precisa de on ou off.",
    "Especifica: /notify on ou /notify off.",
]
_NOTIFY_PUSH_PHRASES = [
    "Terminou uma resposta.",
    "Essa sessão respondeu.",
    "Nova resposta pronta.",
    "Acabou de responder.",
    "Resposta nova chegou.",
]
_STOP_STOPPED_PHRASES = [
    "Sessão interrompida.",
    "Parei a sessão.",
    "Encerrada.",
    "Matei a sessão.",
    "Sessão finalizada.",
]
_STOP_PID_GONE_PHRASES = [
    "Pid {pid} já não existia mais.",
    "Esse processo já tinha caído sozinho.",
    "Já não tem processo rodando com pid {pid}.",
    "Pid {pid} já sumiu.",
    "Nada pra parar — pid {pid} já não existe.",
]
_STOP_NO_TARGET_PHRASES = [
    "Nenhuma sessão pra parar — passa um id ou selecione uma antes.",
    "Não tem sessão ativa pra parar. Usa /select antes.",
    "Sem id nenhum e nenhuma sessão selecionada.",
    "Passa o id da sessão, ou selecione uma com /select primeiro.",
    "Preciso de um id, ou de uma sessão já selecionada.",
]
_STOP_NO_MATCH_PHRASES = [
    'Nenhuma sessão rodando bate com "{p}".',
    'Não achei sessão ativa com "{p}".',
    '"{p}" não corresponde a nenhuma sessão rodando.',
    'Sem sessão rodando pra "{p}".',
    'Nada rodando que bata com "{p}".',
]
_STOPALL_PROMPT_HEADER = "Vai parar {n} sessão(ões):"
_STOPALL_CANCELLED = "Cancelado — nenhuma sessão parada."
_STOPALL_DONE = "Pronto — {n} sessão(ões) parada(s)."
_UNKNOWN_CMD_PHRASES = [
    "Não conheço {cmd}. Manda /help pra ver os comandos.",
    "{cmd} não existe. Confere o /help.",
    "Comando {cmd} desconhecido — veja /help.",
    "Não entendi {cmd}. Tenta /help.",
    "{cmd}? Não conheço. /help lista o que dá pra fazer.",
]
_ERROR_PHRASES = [
    "Deu erro: {e}",
    "Algo quebrou: {e}",
    "Erro ao rodar: {e}",
    "Falhou: {e}",
    "Rolou um erro: {e}",
]
_SESSION_LIVE_ELSEWHERE_PHRASES = [
    "Essa sessão tá aberta ao vivo em outro lugar (VSCode?) agora — não dá pra mandar prompt por aqui enquanto ela estiver aberta lá. Fecha lá ou espera terminar e tenta de novo.",
    "Não consigo mandar prompt: essa sessão já tá em uso em outro lugar (provavelmente o VSCode). Fecha lá primeiro.",
    "Essa sessão parece estar aberta em outra janela agora — só dá pra continuar por aqui quando ela não estiver aberta em nenhum outro lugar.",
]
_WORKING_PHRASES = [
    "⏳ trabalhando…",
    "⏳ rodando…",
    "⏳ processando…",
    "⏳ um instante…",
    "⏳ pensando…",
]
_CONTINUE_REPLY_PHRASES = [
    "Terminei.",
    "Pronto.",
    "Rodei o prompt.",
    "Feito.",
    "Aqui está.",
]

_HELP_TEXT = (
    "<b>Comandos</b>\n"
    "<code>/new</code> &lt;prompt&gt; — inicia sessão nova com esse prompt, já fica selecionada\n"
    "<code>/select</code> [N] — lista sessões recentes (ou <code>/select id</code>) pra escolher qual continuar\n"
    "<code>/notify</code> [on|off] — ativa/desativa aviso automático quando qualquer sessão terminar uma resposta\n"
    "<code>/stop</code> [id|all] — encerra uma sessão (ou todas, com confirmação)\n"
    "<code>/help</code> — essa mensagem\n\n"
    "Texto, foto, áudio ou documento mandado sem <code>/</code> vai direto pro brain/INBOX.md.\n\n"
    "Responder a qualquer mensagem de sessão continua aquela sessão — não precisa digitar id.\n\n"
    "🖥️ na lista do /select = sessão aberta ao vivo em outro lugar (ex.: VSCode) — só dá pra ler, não dá pra mandar prompt por aqui enquanto ela estiver aberta lá.\n\n"
    "Quer abrir uma sessão criada aqui num terminal? <code>claude attach &lt;id&gt;</code> se ela ainda tá rodando em background, ou <code>claude --resume &lt;id&gt;</code> se já virou só histórico (depois de continuada por reply)."
)


def _pick(bank: list[str], **kw) -> str:
    text = random.choice(bank)
    return text.format(**kw) if kw else text


def _plain(text: str) -> str:
    return html.escape(text)


def _title_words(name: str | None, n: int = 3) -> str:
    if not name or not name.strip():
        return "(SEM TÍTULO)"
    return " ".join(name.split()[:n]).upper()


def _head_tail_words(text: str, head: int = 10, tail: int = 10) -> str:
    words = text.split()
    if len(words) <= head + tail:
        return text
    return " ".join(words[:head]) + " … " + " ".join(words[-tail:])


def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def _is_table_sep(line: str) -> bool:
    s = line.strip()
    core = s.strip("|").strip()
    if not core:
        return False
    cells = [c.strip() for c in core.split("|")]
    return all(c and set(c) <= set("-:") and "-" in c for c in cells)


def _convert_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`\n]+?)`", r"<code>\1</code>", text)
    return text


def _format_text_chunk(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if _is_table_row(lines[i]) and i + 1 < len(lines) and _is_table_sep(lines[i + 1]):
            block = [lines[i], lines[i + 1]]
            j = i + 2
            while j < len(lines) and _is_table_row(lines[j]):
                block.append(lines[j])
                j += 1
            out.append(f"<pre>{html.escape(chr(10).join(block))}</pre>")
            i = j
        else:
            out.append(_convert_inline(lines[i]))
            i += 1
    return "\n".join(out)


def _format_body(text: str) -> str:
    # Telegram has no table syntax at all — pipe-tables get boxed as monospace <pre>.
    out, last = [], 0
    for m in re.finditer(r"```(?:\w+\n)?(.*?)```", text, flags=re.S):
        out.append(_format_text_chunk(text[last:m.start()]))
        out.append(f"<pre>{html.escape(m.group(1))}</pre>")
        last = m.end()
    out.append(_format_text_chunk(text[last:]))
    return "".join(out)


def _session_block(phrase: str, sid: str | None, title: str | None, body: str | None = None, extra: str | None = None) -> str:
    lines = [html.escape(phrase)]
    if sid:
        header = f"[{sid[:SESSION_ID_LABEL_LEN].upper()}] {_title_words(title)}"
        if extra:
            header += f" · {extra}"
        lines.append(html.escape(header))
    if body:
        lines.append(_format_body(body))
    return "\n".join(lines)


def _append_inbox_entry(entry: str) -> None:
    text = INBOX_FILE.read_text()
    marker_pos = text.index(INBOX_MARKER) + len(INBOX_MARKER)
    updated = text[:marker_pos] + f"\n\n{entry}" + text[marker_pos:]
    INBOX_FILE.write_text(updated)


async def _save_media(file_id: str, context: ContextTypes.DEFAULT_TYPE, suffix: str) -> pathlib.Path:
    tg_file = await context.bot.get_file(file_id)
    month_dir = attachments_util.month_dir(BRAIN_ATTACHMENTS)
    filename = attachments_util.safe_name(f"telegram-{file_id}{suffix}")
    filepath = attachments_util.unique_path(month_dir / filename)
    await tg_file.download_to_drive(str(filepath))
    return filepath


def _build_entry(body: str, attachment_path: pathlib.Path | None) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    lines = [body]
    if attachment_path is not None:
        lines.append(f"[attachment: {attachment_path.relative_to('/mnt/workspace')}]")
    lines.append(f"— via telegram · {date}")
    return "\n".join(lines)


def _claude_bin() -> str:
    override = shutil.which("claude")
    if override:
        return override
    candidates = sorted(pathlib.Path.home().glob(
        ".vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude"))
    if not candidates:
        raise RuntimeError("claude binary not found (checked PATH and VSCode extension dir)")
    return str(candidates[-1])


async def _claude_agents(all_sessions: bool = False) -> list[dict]:
    args = [_claude_bin(), "agents", "--json", "--cwd", WORKSPACE_DIR]
    if all_sessions:
        args.append("--all")
    proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return json.loads(stdout.decode())


def _parse_result_json(stdout: str) -> dict | None:
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


async def _run_claude_print(*extra_args: str, prompt: str) -> dict:
    args = [_claude_bin(), "-p", "--permission-mode", "bypassPermissions", "--output-format", "json", *extra_args, prompt]
    proc = await asyncio.create_subprocess_exec(*args, cwd=WORKSPACE_DIR, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    result = _parse_result_json(stdout.decode())
    if result is None:
        return {"error": f"(no parseable result)\n{stderr.decode()[-500:]}"}
    if result.get("is_error"):
        return {"error": result.get("result", stderr.decode()[-500:])}
    return {
        "text": result.get("result", "(empty result)"),
        "cost": result.get("total_cost_usd"),
        "session_id": result.get("session_id"),
    }


async def _all_known_session_ids() -> set[str]:
    # A --fork-session continuation is a one-shot -p process: it exits after answering and
    # never registers with `claude agents` — only its transcript file proves it existed.
    # So "every session that exists" = live/finished agents UNION every *.jsonl on disk.
    ids = {s["sessionId"] for s in await _claude_agents(all_sessions=True) if s.get("sessionId")}
    if TRANSCRIPTS_DIR.exists():
        ids |= {f.stem for f in TRANSCRIPTS_DIR.glob("*.jsonl")}
    return ids


async def _resolve_session(prefix: str) -> str | None:
    matches = [sid for sid in await _all_known_session_ids() if sid.startswith(prefix)]
    return matches[0] if len(matches) == 1 else None


async def _cmd_new(prompt: str) -> tuple[str, str | None]:
    if not prompt.strip():
        return _plain(_pick(_NEW_EMPTY_PROMPT_PHRASES)), None
    before = {s["sessionId"] for s in await _claude_agents(all_sessions=True)}
    proc = await asyncio.create_subprocess_exec(
        _claude_bin(), "--bg", "--permission-mode", "bypassPermissions", prompt,
        cwd=WORKSPACE_DIR, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # communicate() (not wait()) — draining stdout/stderr here avoids a pipe-buffer deadlock,
    # and gives us the dispatch's own error output instead of silently polling for 60s.
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        detail = (stderr.decode().strip() or stdout.decode().strip())[-500:]
        text = _pick(_NEW_DISPATCH_FAILED_PHRASES)
        if detail:
            text += f"\n{detail}"
        return _plain(text), None
    elapsed = 0.0
    new = []
    for checkpoint in NEW_SESSION_CHECKPOINTS:
        await asyncio.sleep(checkpoint - elapsed)
        elapsed = checkpoint
        after = await _claude_agents(all_sessions=True)
        new = [s for s in after if s["sessionId"] not in before]
        if new:
            break
    if not new:
        detail = (stdout.decode().strip() + "\n" + stderr.decode().strip()).strip()[-500:]
        text = _pick(_NEW_UNCONFIRMED_PHRASES)
        if detail:
            text += f"\n{detail}"
        return _plain(text), None
    s = new[0]
    sid = s["sessionId"]
    telegram_config.save_config(claude_focused_session=sid)
    _seed_notify_seen(sid)
    return _session_block(_pick(_NEW_STARTED_PHRASES), sid, _last_ai_title(_transcript_path(sid))), sid


async def _continue_session(sid: str, prompt: str) -> dict:
    # --fork-session is mandatory: any session known to `claude agents` (bg or interactive)
    # refuses a plain --resume ("currently running as a background agent") — even once finished.
    # Forking mints a NEW session_id each call, so callers must track result["session_id"] going
    # forward, not the id they resumed from, or every later reply forks from the same stale point.
    return await _run_claude_print("--resume", sid, "--fork-session", prompt=prompt)


async def _cmd_status(arg: str) -> tuple[str, str | None]:
    prefix = arg or (telegram_config.load_config().get("claude_focused_session") or "")[:8]
    if not prefix:
        return _plain("no session id given and none focused"), None
    sessions = await _claude_agents(all_sessions=True)
    matches = [s for s in sessions if s.get("sessionId", "").startswith(prefix)]
    if not matches:
        return _plain(f"no session matching '{prefix}'"), None
    s = matches[0]
    return _plain(f"{s['sessionId'][:8]}  kind={s.get('kind')}  pid={s.get('pid')}  cwd={s.get('cwd')}"), s["sessionId"]


async def _cmd_stop(arg: str) -> tuple[str, str | None]:
    prefix = arg.strip() or (telegram_config.load_config().get("claude_focused_session") or "")[:8]
    if not prefix:
        return _plain(_pick(_STOP_NO_TARGET_PHRASES)), None
    sessions = await _claude_agents(all_sessions=True)
    matches = [s for s in sessions if s.get("sessionId", "").startswith(prefix) and s.get("pid")]
    if not matches:
        return _plain(_pick(_STOP_NO_MATCH_PHRASES, p=prefix)), None
    s = matches[0]
    sid, pid = s["sessionId"], s["pid"]
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return _session_block(_pick(_STOP_PID_GONE_PHRASES, pid=pid), sid, _last_ai_title(_transcript_path(sid))), None
    return _session_block(_pick(_STOP_STOPPED_PHRASES), sid, _last_ai_title(_transcript_path(sid)), extra=f"pid {pid}"), None


async def _cmd_notify(arg: str) -> tuple[str, str | None]:
    arg = arg.strip().lower()
    if arg not in ("on", "off"):
        return _plain(_pick(_NOTIFY_USAGE_PHRASES)), None
    enabled = arg == "on"
    if enabled:
        _seed_notify_seen_all()
    telegram_config.save_config(notify_enabled=enabled)
    return _plain(_pick(_NOTIFY_ON_PHRASES if enabled else _NOTIFY_OFF_PHRASES)), None


def _notify_keyboard(enabled: bool) -> InlineKeyboardMarkup:
    label = "🔕 Desativar" if enabled else "🔔 Ativar"
    data = "notify:off" if enabled else "notify:on"
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=data)]])


def _transcript_path(session_id: str) -> pathlib.Path:
    return TRANSCRIPTS_DIR / f"{session_id}.jsonl"


def _last_assistant_text(path: pathlib.Path) -> str | None:
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "assistant":
            content = d.get("message", {}).get("content", [])
            texts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
            if texts:
                return "\n".join(texts).strip()
    return None


def _last_ai_title(path: pathlib.Path) -> str | None:
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "ai-title":
            return d.get("aiTitle")
    return None


def _select_button_label(sid: str, title: str | None, preview: str, kind: str | None = None) -> str:
    # kind=interactive sessions are live in another client (e.g. VSCode) — replying can't
    # attach a second process to them, so flag it before the tap, not after the failure.
    tag = "🖥️ " if kind == "interactive" else ""
    header = f"{tag}[{sid[:SESSION_ID_LABEL_LEN].upper()}] {_title_words(title)}"
    label = f"{header} — {preview}" if preview else header
    return label if len(label) <= 60 else label[:57] + "…"


async def _select_deliver(sid: str, source_msg) -> None:
    title = _last_ai_title(_transcript_path(sid))
    text = _last_assistant_text(_transcript_path(sid))
    block = _session_block(_pick(_SELECT_TAP_PHRASES), sid, title, body=text)
    sent = await _send_chunked(source_msg, block)
    if sent is not None:
        _remember_reply_target(sent.message_id, sid)
    telegram_config.save_config(claude_focused_session=sid)


async def _handle_select(msg, arg: str) -> None:
    arg = arg.strip()
    if arg and not arg.isdigit():
        sid = await _resolve_session(arg)
        if sid is None:
            await _safe_reply(msg, _plain(_pick(_SELECT_UNRESOLVED_PHRASES, p=arg)))
            return
        await _select_deliver(sid, msg)
        return

    n = int(arg) if arg.isdigit() else DEFAULT_SELECT_COUNT
    agents_by_id = {s["sessionId"]: s for s in await _claude_agents(all_sessions=True) if s.get("sessionId")}
    all_ids = set(agents_by_id) | (
        {f.stem for f in TRANSCRIPTS_DIR.glob("*.jsonl")} if TRANSCRIPTS_DIR.exists() else set()
    )
    ranked = sorted(
        all_ids,
        key=lambda sid: (_transcript_path(sid).stat().st_mtime if _transcript_path(sid).exists() else 0),
        reverse=True,
    )[:n]
    if not ranked:
        await _safe_reply(msg, _plain(_pick(_SELECT_EMPTY_PHRASES)))
        return

    keyboard = []
    for sid in ranked:
        text = _last_assistant_text(_transcript_path(sid))
        preview = _head_tail_words(text) if text else "(sem resposta ainda)"
        kind = agents_by_id.get(sid, {}).get("kind")
        keyboard.append([InlineKeyboardButton(
            _select_button_label(sid, _last_ai_title(_transcript_path(sid)), preview, kind),
            callback_data=f"select:{sid}")])
    await _safe_reply(msg, _plain(_pick(_SELECT_LIST_PHRASES)), reply_markup=InlineKeyboardMarkup(keyboard))


async def _handle_stop_all_prompt(msg) -> None:
    sessions = await _claude_agents(all_sessions=True)
    running = [s for s in sessions if s.get("pid")]
    if not running:
        await _safe_reply(msg, _plain(_pick(_STOP_NO_TARGET_PHRASES)))
        return
    lines = [_STOPALL_PROMPT_HEADER.format(n=len(running))]
    lines += [f"[{s['sessionId'][:SESSION_ID_LABEL_LEN].upper()}] {_title_words(_last_ai_title(_transcript_path(s['sessionId'])))}" for s in running]
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Confirmar", callback_data="stopall:confirm"),
        InlineKeyboardButton("Cancelar", callback_data="stopall:cancel"),
    ]])
    await _safe_reply(msg, _plain("\n".join(lines)), reply_markup=keyboard)


def _seed_notify_seen(session_id: str) -> None:
    cfg = telegram_config.load_config()
    seen = cfg.get("notify_seen", {})
    path = _transcript_path(session_id)
    seen[session_id] = path.stat().st_size if path.exists() else 0
    telegram_config.save_config(notify_seen=seen)


def _seed_notify_seen_all() -> None:
    if not TRANSCRIPTS_DIR.exists():
        return
    seen = {f.stem: f.stat().st_size for f in TRANSCRIPTS_DIR.glob("*.jsonl")}
    telegram_config.save_config(notify_seen=seen)


def _remember_reply_target(message_id: int, session_id: str) -> None:
    cfg = telegram_config.load_config()
    reply_map = cfg.get("reply_map", {})
    reply_map[str(message_id)] = session_id
    if len(reply_map) > REPLY_MAP_MAX:
        for k in sorted(reply_map, key=int)[: len(reply_map) - REPLY_MAP_MAX]:
            del reply_map[k]
    telegram_config.save_config(reply_map=reply_map)


async def _safe_reply(msg, html_text: str, reply_markup=None) -> "telegram.Message | None":
    # Every caller passes pre-escaped/composed HTML (_plain() or _session_block()) — never raw text.
    for attempt in range(2):
        try:
            return await msg.reply_text(html_text, parse_mode="HTML", do_quote=True, reply_markup=reply_markup)
        except TelegramError as e:
            if attempt == 0:
                await asyncio.sleep(2)
                continue
            print(f"reply_text failed after retry: {e}")
            return None


async def _send_chunked(msg, html_text: str, reply_markup=None) -> "telegram.Message | None":
    sent = None
    for i in range(0, len(html_text), TELEGRAM_MSG_LIMIT):
        sent = await _safe_reply(msg, html_text[i:i + TELEGRAM_MSG_LIMIT], reply_markup=reply_markup if i == 0 else None)
    return sent


async def _dispatch_command(text: str, msg) -> None:
    parts = text.split(maxsplit=1)
    cmd, arg = parts[0], (parts[1] if len(parts) > 1 else "")
    arg = arg.strip()

    if cmd == "/help":
        await _safe_reply(msg, _HELP_TEXT)
        return
    if cmd == "/select":
        await _handle_select(msg, arg)
        return
    if cmd == "/stop" and arg.lower() == "all":
        await _handle_stop_all_prompt(msg)
        return
    if cmd == "/notify" and not arg:
        enabled = bool(telegram_config.load_config().get("notify_enabled"))
        await _safe_reply(msg, _plain(_pick(_NOTIFY_ON_PHRASES if enabled else _NOTIFY_OFF_PHRASES)),
                           reply_markup=_notify_keyboard(enabled))
        return
    if cmd == "/new" and not arg:
        # Tapping the /new suggestion from Telegram's own command menu sends it with no args —
        # dispatching an empty prompt creates a session stuck waiting for input forever.
        await _safe_reply(msg, _plain(_pick(_NEW_EMPTY_PROMPT_PHRASES)))
        return

    handlers = {
        "/new": lambda: _cmd_new(arg),
        "/stop": lambda: _cmd_stop(arg),
        "/notify": lambda: _cmd_notify(arg),
        "/status": lambda: _cmd_status(arg),
    }
    handler = handlers.get(cmd)
    if handler is None:
        await _safe_reply(msg, _plain(_pick(_UNKNOWN_CMD_PHRASES, cmd=cmd)))
        return
    if cmd == "/new":
        await _safe_reply(msg, _plain(_pick(_WORKING_PHRASES)))
    try:
        reply, session_id = await handler()
    except Exception as e:
        reply, session_id = _plain(_pick(_ERROR_PHRASES, e=e)), None
    sent = await _send_chunked(msg, reply)
    if session_id and sent is not None:
        _remember_reply_target(sent.message_id, session_id)
        telegram_config.save_config(claude_focused_session=session_id)


async def _handle_reply_continue(update: Update, sid: str) -> None:
    msg = update.message
    await _safe_reply(msg, _plain(_pick(_WORKING_PHRASES)))
    result = await _continue_session(sid, msg.text)
    if "error" in result:
        if "No conversation found" in result["error"]:
            await _safe_reply(msg, _plain(_pick(_SESSION_LIVE_ELSEWHERE_PHRASES)))
        else:
            await _safe_reply(msg, _plain(_pick(_ERROR_PHRASES, e=result["error"])))
        return
    new_sid = result.get("session_id") or sid
    title = _last_ai_title(_transcript_path(new_sid))
    extra = f"${result['cost']:.3f}" if result.get("cost") else None
    block = _session_block(_pick(_CONTINUE_REPLY_PHRASES), new_sid, title, body=result["text"], extra=extra)
    sent = await _send_chunked(msg, block)
    if sent is not None:
        _remember_reply_target(sent.message_id, new_sid)
    telegram_config.save_config(claude_focused_session=new_sid)


async def _handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.message is None or query.message.chat_id != telegram_config.allowed_chat_id():
        return
    data = query.data or ""
    await query.answer()

    if data.startswith("select:"):
        sid = data.split(":", 1)[1]
        context.application.create_task(_select_deliver(sid, query.message))
    elif data.startswith("notify:"):
        enabled = data.split(":", 1)[1] == "on"
        if enabled:
            _seed_notify_seen_all()
        telegram_config.save_config(notify_enabled=enabled)
        await query.edit_message_text(_plain(_pick(_NOTIFY_ON_PHRASES if enabled else _NOTIFY_OFF_PHRASES)),
                                       parse_mode="HTML", reply_markup=_notify_keyboard(enabled))
    elif data.startswith("stopall:"):
        action = data.split(":", 1)[1]
        if action == "confirm":
            sessions = await _claude_agents(all_sessions=True)
            killed = 0
            for s in sessions:
                if not s.get("pid"):
                    continue
                try:
                    os.kill(s["pid"], signal.SIGTERM)
                    killed += 1
                except ProcessLookupError:
                    pass
            await query.edit_message_text(_plain(_STOPALL_DONE.format(n=killed)), parse_mode="HTML")
        else:
            await query.edit_message_text(_plain(_STOPALL_CANCELLED), parse_mode="HTML")


async def _notify_tick(app: Application) -> None:
    while True:
        await asyncio.sleep(NOTIFY_POLL_SECONDS)
        try:
            cfg = telegram_config.load_config()
            if not cfg.get("notify_enabled"):
                continue
            if not TRANSCRIPTS_DIR.exists():
                continue
            seen = cfg.get("notify_seen", {})
            chat_id = telegram_config.allowed_chat_id()
            changed = False
            for f in TRANSCRIPTS_DIR.glob("*.jsonl"):
                sid = f.stem
                size = f.stat().st_size
                if size <= seen.get(sid, 0):
                    continue
                lines = f.read_text().splitlines()
                last_type = None
                for line in reversed(lines):
                    if line.strip():
                        try:
                            last_type = json.loads(line).get("type")
                        except json.JSONDecodeError:
                            pass
                        break
                seen[sid] = size
                changed = True
                if last_type != "assistant":
                    continue
                text = _last_assistant_text(f)
                if not text:
                    continue
                snippet = text[:NOTIFY_PUSH_TRUNCATE] + ("…" if len(text) > NOTIFY_PUSH_TRUNCATE else "")
                title = _last_ai_title(f)
                block = _session_block(_pick(_NOTIFY_PUSH_PHRASES), sid, title, body=snippet)
                sent = await app.bot.send_message(chat_id=chat_id, text=block, parse_mode="HTML")
                _remember_reply_target(sent.message_id, sid)
            if changed:
                telegram_config.save_config(notify_seen=seen)
        except Exception as e:
            print(f"notify_tick error: {e}")


async def _handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.chat_id != telegram_config.allowed_chat_id():
        print(f"Rejected message from chat_id={update.effective_chat.id if update.effective_chat else '?'}")
        return

    msg = update.message
    if msg.text and msg.text.startswith("/"):
        context.application.create_task(_dispatch_command(msg.text, msg))
        return
    if msg.text and msg.reply_to_message is not None:
        reply_map = telegram_config.load_config().get("reply_map", {})
        sid = reply_map.get(str(msg.reply_to_message.message_id))
        if sid:
            context.application.create_task(_handle_reply_continue(update, sid))
            return
    if msg.voice is not None:
        path = await _save_media(msg.voice.file_id, context, ".ogg")
        _append_inbox_entry(_build_entry("voice note (untranscribed)", path))
    elif msg.photo:
        path = await _save_media(msg.photo[-1].file_id, context, ".jpg")
        _append_inbox_entry(_build_entry(msg.caption or "(photo)", path))
    elif msg.document is not None:
        suffix = pathlib.Path(msg.document.file_name or "file").suffix
        path = await _save_media(msg.document.file_id, context, suffix)
        _append_inbox_entry(_build_entry(msg.caption or "(document)", path))
    elif msg.text:
        _append_inbox_entry(_build_entry(msg.text, None))
    else:
        return

    await _safe_reply(msg, _plain(_pick(_CAPTURE_ACKS)))


async def _post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("new", "Inicia sessão nova com um prompt"),
        BotCommand("select", "Escolhe/mostra uma sessão recente"),
        BotCommand("notify", "Liga/desliga aviso automático"),
        BotCommand("stop", "Encerra uma sessão (ou todas)"),
        BotCommand("status", "Detalhes técnicos de uma sessão (pid, cwd)"),
        BotCommand("help", "Lista os comandos"),
    ])
    asyncio.create_task(_notify_tick(app))


def main() -> None:
    app = Application.builder().token(telegram_config.bot_token()).post_init(_post_init).build()
    app.add_handler(CallbackQueryHandler(_handle_callback))
    app.add_handler(MessageHandler(filters.ALL, _handle_message))
    print("telegram_daemon: polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
