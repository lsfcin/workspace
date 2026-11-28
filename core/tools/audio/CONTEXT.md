# audio
> Speech to text. Backend leaf: `faster-whisper large-v3-turbo`, local, no network.

The wrapper is domain-free on purpose: `run` takes the conditioning prompt as an argument, so the vocabulary lives with whoever owns it — aiwbot primes for workspace jargon, `code/obra` primes for construction and cartório terms. A bare word list ANYWHERE in that prompt suppresses punctuation; write it as writing someone could have said.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`config.json`](config.json) | — | — | Default shortcuts, idle timeout, and safety recording limits for desktop STT dictation. |
| [`config.py`](config.py) | [`config.pyi`](config.pyi) | `default_config_path`, `local_config_path`, `load_config`, `normalize_shortcut`, `find_gnome_conflicts` | Default and local configuration for desktop STT dictation |
| [`dictate`](dictate) | — | — | desktop dictation CLI |
| [`ibus_engine.py`](ibus_engine.py) | [`ibus_engine.pyi`](ibus_engine.pyi) | `default_socket_path`, `WosDictateEngine`, `IBusInjector`, `main`, `do_enable` | Persistent IBus engine helper for injecting dictated UTF-8 text on Wayland |
| [`ibus_inject.py`](ibus_inject.py) | [`ibus_inject.pyi`](ibus_inject.pyi) | `default_socket_path`, `notify`, `ibus_alive`, `set_state`, `inject` | Inject dictated UTF-8 text via IBus daemon with wl-copy clipboard fallback |
| [`learn.py`](learn.py) | [`learn.pyi`](learn.pyi) | `collect_user_messages`, `diff_token_pairs`, `run` | Passive STT self-learning from dictated text vs sent agent user prompts |
| [`refine.py`](refine.py) | [`refine.pyi`](refine.pyi) | `state_dir`, `load_aiwbot_carrier`, `load_vocab`, `build_prompt`, `apply_replacements` | Deterministic STT vocabulary correction, prompt builder, Ollama polish, and log |
| [`stt.py`](stt.py) | [`stt.pyi`](stt.pyi) | `default_socket_path`, `daemon_alive`, `DaemonWhisper`, `model`, `confident` | stt.py — speech-to-text boundary: faster-whisper large-v3-turbo, lazy-loaded; fails safe to "" . Priming is the CALLER's data — a domain passes its own carrier prose to `run`, because the prompt is what buys both vocabulary and punctuation, and no two domains share one. |
| [`sttd`](sttd) | — | — | local STT daemon |
| [`tray.py`](tray.py) | [`tray.pyi`](tray.pyi) | `write_svg_icons`, `DictateTray`, `start_tray`, `set_state`, `close` | Vector-SVG StatusNotifierItem top-bar indicator for WOS desktop dictation |
| [`vocab.json`](vocab.json) | — | — | Editable manual STT vocabulary replacements and punctuated desktop carrier sentences. |
<!-- routing:end -->
