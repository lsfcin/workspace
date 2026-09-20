# Roteiro 3 — OpenRouter (modelos `:free`)

> **Por que usar:** o OpenRouter é um "mercado" que reúne modelos de dezenas de laboratórios (DeepSeek, Meta, Alibaba,
> OpenAI e outros) numa única API. Muitos têm versão **grátis** — basta adicionar o sufixo `:free` ao nome do modelo.

## Visão geral

| Item | Valor |
|------|-------|
| Custo | R$ 0 (sem créditos) |
| Requisições/dia | **50** (sem créditos) |
| Requisições/minuto | 20 |
| Modelos | 20+ gratuitos: `meta-llama/llama-3.3-70b-instruct:free`, `qwen/qwen3-coder-480b-a35b-instruct:free`, `openai/gpt-oss-20b:free`, `deepseek/deepseek-r1:free` e mais |
| Atalho | `openrouter/free` — o OpenRouter sorteia um modelo grátis que suporte o que você precisa |
| Privacidade | Varia por modelo — presuma que não é privado |

## Passo 1 — Pegar a API key

1. Acesse **openrouter.ai** e entre com sua conta **GitHub** ou **Google**
2. Vá em **Settings → Keys** (openrouter.ai/settings/keys)
3. Clique em **Create Key**, dê um nome (ex.: "minha-chave") e copie a key (começa com `sk-or-...`)

## Passo 2 — Conectar no OpenCode

1. Rode `opencode` na pasta do projeto
2. `/connect` → digite `openrouter` → selecione **OpenRouter** → cole a key

## Passo 3 — Escolher o modelo

1. `/models`
2. Escolha um modelo cujo nome termine com `free` (ex.: `qwen/qwen3-coder-480b-a35b-instruct:free` — bom para código)
3. Ou escolha **`openrouter/free`** — o sistema escolhe um modelo grátis aleatório para você (cuidado: você não sabe
   qual modelo responde)

## Passo 4 — Testar

```
olá! Me diga em uma linha qual modelo você é.
```

## Configuração opcional — adicionar modelo no `opencode.json`

Se um modelo free não aparecer no `/models`, adicione na raiz do projeto (`opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "models": {
        "qwen/qwen3-coder-480b-a35b-instruct:free": {}
      }
    }
  }
}
```

## Problemas comuns desta rota

| Problema | Solução |
|----------|---------|
| `429` | Cota diária (50) ou por minuto (20) estourada. Requests **falhos também contam** — não fique reenviando em loop |
| "No endpoints found that support tool use" | Bug conhecido em alguns modelos `:free` — troque de modelo |
| Resposta truncada | Contexto dos modelos free costuma ser **menor** que o pago — reduza o tamanho da conversa (`/compact`) |
| Modelo lento em horário de pico | Normal — use outra rota ou espere |

> **Nota para o professor:** adicionar US$ 10 de crédito uma única vez aumenta o limite para 1.000 req/dia, mas é
> opcional e não é necessário para a disciplina.