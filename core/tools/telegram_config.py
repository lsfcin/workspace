#!/mnt/workspace/.venv/bin/python3
# telegram_config.py — shared config (bot token, allowed chat id) for Core/tools/telegram
import json, pathlib

_CONFIG_DIR = pathlib.Path.home() / ".config" / "workspace-telegram"


def config_dir() -> pathlib.Path:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_DIR.chmod(0o700)
    return _CONFIG_DIR


def _config_file() -> pathlib.Path:
    return config_dir() / "config.json"


def load_config() -> dict:
    f = _config_file()
    return json.loads(f.read_text()) if f.exists() else {}


def save_config(**updates) -> dict:
    """Merge updates into config.json, write chmod 600 (bot token is a secret)."""
    cfg = load_config()
    cfg.update(updates)
    f = _config_file()
    f.write_text(json.dumps(cfg, indent=2))
    f.chmod(0o600)
    return cfg


def bot_token() -> str:
    token = load_config().get("bot_token")
    if not token:
        raise RuntimeError("No bot_token configured — run: core/tools/telegram init --token <TOKEN>")
    return token


def allowed_chat_id() -> int:
    chat_id = load_config().get("allowed_chat_id")
    if chat_id is None:
        raise RuntimeError("No allowed_chat_id configured — run: core/tools/telegram init")
    return chat_id
