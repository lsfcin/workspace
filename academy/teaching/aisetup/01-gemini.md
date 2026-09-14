# Roteiro 1 — Google Gemini (recomendado)

> **Por que esta é a rota recomendada:** é a mais generosa das gratuitas — **1.500 requisições por dia**, não pede
> cartão de crédito e não expira. Cada aluno usa a própria conta Google.

## Visão geral

| Item | Valor |
|------|-------|
| Custo | R$ 0 (sem cartão, permanente) |
| Requisições/dia | **1.500** (por modelo, reseta à meia-noite no horário do Pacífico) |
| Requisições/minuto | ~15 (Flash) / ~30 (Flash-Lite) |
| Modelos | `gemini-3.5-flash` e `gemini-3.1-flash-lite` (gratuitos) |
| Privacidade | ⚠️ Dados do free level **são usados para treinar** produtos Google |

## Passo 1 — Pegar a API key (Windows e Linux, igual)

1. Abra o navegador e entre em **aistudio.google.com**
2. Faça login com sua **conta Google** (crie uma se não tiver)
3. Clique em **Get API key** (no canto esquerdo da tela)
4. Clique em **Create API key** → escolha um projeto (ou crie um) → **Create**
5. **Copie a key** (começa com `AIza...`) e guarde num lugar seguro

> Cada key é **sua** — não compartilhe com colegas. O limite é por conta/projeto, e criar várias keys não aumenta a
> cota.

## Passo 2 — Conectar no OpenCode (Windows e Linux, igual)

1. No terminal, dentro da pasta do seu projeto, rode `opencode`
2. Digite `/connect`
3. Digite `google` na busca e selecione **Google**
4. Cole sua key e confirme

## Passo 3 — Escolher o modelo

1. Digite `/models`
2. Escolha `google/gemini-3.1-flash-lite` (mais rápido, 30 req/min — melhor para volume)
   ou `google/gemini-3.5-flash` (mais capaz)
3. Se os nomes não aparecerem, escolha qualquer modelo **Gemini Flash** da lista

## Passo 4 — Testar

```
olá! Me diga em uma linha qual modelo você é.
```

## Configuração opcional — modelo padrão

Para o OpenCode sempre abrir com o Gemini, crie um arquivo `opencode.json` na raiz do seu projeto:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "google/gemini-3.1-flash-lite"
}
```

## Problemas comuns desta rota

| Problema | Solução |
|----------|---------|
| `429` em rajada | Você excedeu req/minuto: espere 1–2 minutos |
| `429` o dia todo | Cota diária estourada: aguarde até a meia-noite (horário do Pacífico) ou use outra rota |
| "Free level is not available in your country" | O free level não está liberado na sua região: avise o professor |
| Modelo Pro não aparece | Normal: modelos Pro saíram do free level — use apenas os **Flash** |