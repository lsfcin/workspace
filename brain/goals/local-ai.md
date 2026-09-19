# [ craft | research | year ] always-on autonomous local AI

Build a local AI setup compatible with Claude Code. Optimize agents to run fast and reliably using strategies of dynamically expanding and collapsing context: foldable contexts, smaller models operating under compressed representations. The research direction is clear and the literature is live.

*refs:*  
- https://openreview.net/pdf?id=JaLXQnA2wi  
- https://openreview.net/pdf?id=91jL62CQF1  
- https://arxiv.org/pdf/2603.16021  
- https://github.com/WeaveMindAI/weft  
- https://arxiv.org/pdf/2604.14228  
- https://arxiv.org/pdf/2601.10112  
- https://arxiv.org/pdf/2602.11988  
- https://www.instagram.com/p/DbKa8dzkRv4/ — [src: web:instagram.com] "no-limits local AI video gen" carousel (DM-gated, title cards only extracted so far)

>**signals**  
transformative · expected · motivated

>**owns**  
`code/dobra` · `code/aiwbot` · `academy/papers/2027-ICLR-dobra`

## selected next achievement
    [read-weft] read the weft implementation paper and repo — most concrete starting point

**ease-start**  
Open the weft repo (github.com/WeaveMindAI/weft). Read the README. Understand what the system does, what it builds on.
30 minutes max.

## backlog

> [ ] [read-weft] read the weft implementation paper and repo — most concrete starting point  
> [ ] [read-foldable] read the foldable contexts paper (arxiv 2603.16021)  
> [ ] [map-landscape] map the 7 cited papers — what problem does each solve, how they connect  
> [ ] [local-setup] set up a local model environment (Ollama or equivalent) compatible with Claude Code  
> [ ] [tiny-quant] avaliar quantização extrema como caminho pro setup local — Qwen3.6-27B rebuildado em 1-bit (3.9GB) / ternário (5.9GB), arquitetura intacta, cabe até em celular (ref em `core/refs/REFS.md`). Amarra direto em [local-setup]: decide se a RTX 3050 6GB roda um 27B em vez de um 7B (INBOX 2026-07-23)  
> [ ] [tts-local] KittenTTS <25MB em CPU — checar suporte a pt-BR ANTES de qualquer integração; sem pt-BR não serve pra nada aqui (ref em `core/refs/REFS.md`, INBOX 2026-07-23)  
> [ ] [cpu-inference-engine] investigar o claim de rodar modelos grandes sem GPU — "Kimi K3nc", motor em C99 de 176KB que alegadamente roda modelos de 2T de parâmetros em laptop com 8GB RAM e sem GPU ([reel](https://www.instagram.com/reel/Db92TZauDGF/), INBOX 2026-08-16, Lucas: *"várias relevantes, especialmente essa de rodar localmente"*). **Conteúdo de agregador de hype, verificar antes de investir**: o mesmo reel mistura releases reais com nomes provavelmente errados. Se o claim se sustentar, muda [local-setup] e [tiny-quant] por completo — daí a prioridade de checar a fonte primária, não o reel  
> [ ] [local-opus-claim] checar a leva de releases open-source da semana de 2026-08-17 — claim de um modelo chinês "nível Opus" rodando local e grátis, mais releases Meta/xAI/Zhipu/Alibaba ([reel](https://www.instagram.com/reel/DcJ3PUDyIvS/), INBOX, Lucas: *"interessado especialmente nos casos em que podemos rodar algo localmente"*). **Mesmo gênero de fonte que [cpu-inference-engine] e o mesmo cuidado se aplica**:
> nenhum modelo é nomeado e nenhum benchmark é citado, então o valor é o ponteiro para aquela semana, não a afirmação.
> Ir na fonte primária ou descartar  
> [ ] [prototype-context] build a first prototype: dynamic context collapse for a specific task type  
> [ ] [benchmark] measure: speed, reliability, quality vs cloud baseline  
> [ ] [claude-code-alt] set up CLI coding agent alternative to Claude Code — candidates: qwencode + qwen model locally, GLM 5.1 (free cloud), opencode, codex  
> [ ] [local-video-gen] evaluate the local AI video-gen setup as alternative to opencode+nvidia+image-model (INBOX 2026-07-26, IG carousel `DbKa8dzkRv4` — DM-gated, only title cards extracted; may need the "GUIDE" DM or independent search to get the real tool list)  
> [ ] [vipassana-autonomous] explorar deixar um agente rodando com autonomia SEGURA durante os 10 dias de vipassana (1–12 ago, offline), entregando resultados RELEVANTES — candidatos: watcher que constrói/refina continuamente as revisões de estado-da-arte dos papers planejados; pasta sandbox pra prototipar. Pré-requisito duro: **mecânica de autostart de sessões** (o caso "sessão morreu, ninguém acorda o agente" do [workspace-os] triggers pós-janela).
> Definir escopo seguro ANTES; sem isso, não roda (INBOX 2026-07-23)  
> [ ] [finetune-libs] avaliar as 10 libs de fine-tuning local (Unsloth, LLaMA-Factory, PEFT, Axolotl, TRL, torchtune, LitGPT, SWIFT, DeepSpeed, AutoTrain) — quais servem ao runner de SLM do dobra na RTX 3050 6GB? ref em `core/refs/REFS.md` (INBOX 2026-07-27)  
> [ ] [manaca-1b] olhar o Manacá-1B — 1.72B decoder-only aberto e reproduzível pra pt-BR, pesos e logs soltos. Lucas:
> *"a gente TEM que olhar isso! não deixar pra mt longe"* (INBOX 2026-09-11), então **é o próximo daqui**. Duas coisas separadas: (1) cabe na RTX 3050 6GB e serve de base local em português — amarra em [local-setup] e [tiny-quant];
> (2) a armadilha de tokenizer que o paper documenta (SentencePiece com case-folding → HF fast derruba o normalizer, LAMBADA-PT 45.3 → 25.0, invisível na métrica agregada) é um erro que a gente pode cometer em qualquer avaliação nossa, independente de adotar o modelo. Ref em `academy/refs/REFS.md`  
> [ ] [layerwise-70b] avaliar a lib Python que roda modelos de 70B carregando camada por camada do disco, com flash attention e memória quase plana — Lucas: *"talvez sirva pros nossos testes"*. Mesmo gênero de fonte de [cpu-inference-engine], então ir na fonte primária antes do número. Ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [openworker] olhar o OpenWorker do Andrew Ng — co-worker que executa tarefas em vez de conversar, roda local, conecta 40+ apps e aceita qualquer modelo. Lucas: *"vale muito a pena a gente consultar"*. Ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [higgsfield-o-que-roda-aqui] a pergunta estreita sobre o Higgsfield: o que da stack dele roda **aqui**, se é que algo roda. O post é patrocinado e fala em acesso por API na nuvem, então a resposta honesta pode ser "nada" — e um "não" curto, escrito, vale mais que a pergunta voltando a cada captura. Irmão de [higgsfield-asset-gen] em `rpg-isoroll.md`. Ref em `core/refs/REFS.md` (— via aiwbot)  
> [ ] [nvidia-pair] olhar o PAIR da Nvidia — aberto, junta a capacidade ociosa de várias máquinas da mesma casa (Windows, Linux, macOS) para uma carga local de IA. Lucas: *"será que consigo usar de alguma forma?"*. A pergunta concreta daqui: somar a RTX 3050 a outra máquina muda o teto de [local-setup] e [tiny-quant], ou o gargalo continua sendo VRAM numa placa só? Ref em `core/refs/REFS.md` (— via aiwbot)  

## done

<!-- done:start -->
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-09-17  ·  trend: advancing  ·  touches: 72/100/101/101/101/101
<!-- stats:end -->
