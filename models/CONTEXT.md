# Models
> Local model checkpoints and weights used across research and code projects

**Every weight on this machine lives here, whatever tool downloaded it.** A tool that insists on its own path gets a symlink into this folder: `~/.cache/huggingface` → `hf/`, each `~/ComfyUI/models/<kind>` → `diffusion/<kind>`, and Ollama reads `OLLAMA_MODELS=llm/ollama`. The root partition is small and the workspace partition is not; on 2026-10-24 the root filled to 100% with 13 GB of Hugging Face weights in `~/.cache`. Where the disk goes: `core/run tools/disk/ubuntu diagnose`.

<!-- routing:start -->
## Routing

<!-- routing:end -->
