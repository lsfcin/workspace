# Roteiro 4 — NVIDIA NIM (build.nvidia.com)

> **Por que usar:** a NVIDIA hospeda 100+ modelos de código aberto (Nemotron, DeepSeek, Llama, GLM, Qwen) de graça no
> build.nvidia.com, rodando nas GPUs deles. Ótimo para experimentar modelos grandes sem precisar de hardware próprio.

## Visão geral

| Item | Valor |
|------|-------|
| Custo | R$ 0 (sem cartão) |
| Créditos iniciais | ~1.000 (alguns modelos são 100% grátis; outros consomem créditos) |
| Requisições/minuto | ~40 (best-effort — pode cair em horários de pico) |
| Key | `nvapi-...` — **válida ~6 meses**, depois precisa gerar outra |
| Privacidade | ⚠️ Uso de trial: NVIDIA registra o uso para segurança e melhoria de produtos |
| Uso permitido | Desenvolvimento, testes e pesquisa — **não** produção |

## Passo 1 — Criar conta e pegar a key

1. Acesse **build.nvidia.com** e clique em **Create account** (email, sem cartão)
2. Vá em **Settings → API Keys** (ou abra qualquer modelo e clique em **Get API Key**)
3. Clique em **Generate API Key**
4. **Copie a key agora** — ela começa com `nvapi-` e **só é mostrada uma vez**!

> A key expira em ~6 meses. Quando expirar, volte ao build.nvidia.com → Settings → API Keys → gere outra e atualize no
> OpenCode.

## Passo 2 — Conectar no OpenCode (Windows e Linux, igual)

1. Rode `opencode` na pasta do projeto
2. `/connect` → digite `nvidia` → selecione **NVIDIA** → cole a key

## Passo 3 — Escolher o modelo

1. `/models`
2. Modelos recomendados:
   - `nvidia/nemotron-3-super-120b-a12b` — 120B com 1M de contexto (bom para conversas longas)
   - `nvidia/nemotron-3-ultra-550b-a55b` — o mais forte da família
3. Outros modelos do catálogo (DeepSeek, Llama, GLM) também aparecem

## Passo 4 — Testar

```
olá! Me diga em uma linha qual modelo você é.
```

## Se um modelo não aparecer — baseURL manual

Crie um arquivo `opencode.json` na raiz do projeto:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "nvidia": {
      "options": {
        "baseURL": "https://integrate.api.nvidia.com/v1"
      }
    }
  }
}
```

Depois rode `/models` de novo.

## Problemas comuns desta rota

| Problema | Solução |
|----------|---------|
| `401 Unauthorized` | Key errada, ou **expirada** (6 meses) — gere uma nova no dashboard |
| `429 Too Many Requests` | Limite por minuto — espere, reduza a frequência, ou troque de modelo (o limite é por modelo) |
| `404 model not found` | O nome do modelo mudou — copie o ID exato da página do modelo no build.nvidia.com |
| Créditos acabando | Alguns modelos consomem créditos. Prefira os marcados como **Free Endpoint** no catálogo |