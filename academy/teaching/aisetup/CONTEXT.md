# aisetup
> Modelos de IA grátis no OpenCode: material de setup para alunos, Windows e Linux, uma rota por arquivo.

Ler na ordem: `00-primeiros-passos.md` instala o OpenCode; cada arquivo numerado depois é **uma**
rota de modelo, e o aluno precisa de apenas uma delas.

## Comparação das rotas

| Rota | Custo | Volume | Dados usados para treino? | Dificuldade |
|------|-------|--------|---------------------------|-------------|
| **Gemini** | R$ 0 | 1.500 req/dia por aluno | **Sim** (free level) | Fácil |
| **Zen** | R$ 0 | ~200 req/dia, dinâmico e instável | **Sim** (modelos free) | Trivial |
| **OpenRouter** | R$ 0 | 50 req/dia | Varia por modelo | Fácil |
| **NVIDIA NIM** | R$ 0 | ~1.000 créditos iniciais, 40 req/min | **Logs de uso** (NVIDIA) | Fácil |

## Qual escolher?

- **Para a maioria dos trabalhos da disciplina:** Gemini (rote 01) — maior volume, mais estável, setup simples.
- **Para testar sem criar conta nenhuma:** OpenCode Zen caminho A (rote 02) — funciona direto, mas a cota é pequena e
  imprevisível.
- **Para experimentar modelos diferentes (DeepSeek, Llama, Qwen):** OpenRouter (rote 03).
- **Para modelos grandes de código aberto (Nemotron):** NVIDIA NIM (rote 04).

## ⚠️ Regra de privacidade (leia antes de tudo)

> **NUNCA** cole código sensível, senhas, dados pessoais ou trabalho proprietário em **nenhum** modelo gratuito. Todos
> podem usar seus dados para melhorar os modelos:
>
> - Gemini free level e OpenCode Zen free: **explicitamente** usam seus dados para treino.
> - NVIDIA NIM: registra o uso para segurança e melhoria de produtos.
>
> Exercícios e projetos da disciplina: ok. Segredos de empresa ou do seu trabalho: nunca.

## Troubleshooting rápido

| Erro | O que significa | O que fazer |
|------|-----------------|-------------|
| `401 Unauthorized` | Key errada ou expirada | Recolar a key; no NVIDIA, gerar key nova (expira em ~6 meses) |
| `429` / "rate limit" | Cota estourada ou excesso por minuto | Esperar alguns minutos (RPM) ou até o dia seguinte (RPD); trocar de modelo/rota |
| `Free usage exceeded, add credits` (Zen) | Cota do dia estourada — **não** é problema de saldo | Esperar ~10–24 h ou usar outra rota |
| Modelo não aparece no `/models` | Catálogo desatualizado ou provider não conectado | Rodar `/connect` de novo; atualizar com `opencode upgrade` |
| Sessão lenta / travada | Pico de uso nos servidores grátis | Ter paciência, trocar de modelo (ex.: Flash-Lite) ou de rota |

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`00-primeiros-passos.md`](00-primeiros-passos.md) | Passo 0 — Primeiros passos: instalar o OpenCode |
| [`01-gemini.md`](01-gemini.md) | Roteiro 1 — Google Gemini (recomendado) |
| [`02-opencode-zen.md`](02-opencode-zen.md) | Roteiro 2 — OpenCode Zen (sem cadastro) |
| [`03-openrouter.md`](03-openrouter.md) | Roteiro 3 — OpenRouter (modelos `:free`) |
| [`04-nvidia-nim.md`](04-nvidia-nim.md) | Roteiro 4 — NVIDIA NIM (build.nvidia.com) |
<!-- routing:end -->
