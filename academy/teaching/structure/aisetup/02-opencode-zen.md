# Roteiro 2 — OpenCode Zen (sem cadastro)

> **Por que usar:** é a rota mais rápida de todas — em muitos casos **não precisa nem criar conta**. O OpenCode traz
> modelos grátis embutidos, fornecidos pelo time do próprio OpenCode. Use para testes rápidos; não use para trabalho
> sério (cota pequena e instável).

## Visão geral

| Item | Valor |
|------|-------|
| Custo | R$ 0 |
| Requisições/dia | ~200 (cota dinâmica, **não publicada** — muda conforme a demanda) |
| Modelos | `big-pickle`, `deepseek-v4-flash-free`, `nemotron-3-ultra-free`, `nemotron-3.5-lightning-free`, `mimo-v2.5-free`, `hy3-free`, `laguna-s-2.1-free` |
| Privacidade | ⚠️ Dados dos modelos free **são usados para treino** |
| Estabilidade | Baixa — lineup muda com frequência (modelo grátis vira pago e outro entra no lugar) |

## Caminho A — Sem conta (o mais rápido)

1. Rode `opencode` na pasta do projeto
2. Digite `/models`
3. Escolha um modelo com **Free** no nome ou preço `$0` (ex.: `opencode/big-pickle` ou
   `opencode/deepseek-v4-flash-free`)
4. Pronto — sem key, sem cadastro

## Caminho B — Com conta (cota por usuário em vez de por IP)

1. Acesse **opencode.ai/auth** e crie uma conta (Google ou email)
2. Clique em **Create API key** e copie
3. No OpenCode: `/connect` → digite `zen` → selecione **OpenCode Zen** → cole a key
4. `/models` → escolha o modelo free

> Fazer login dá uma cota por conta (mais estável que a por IP) e libera modelos pagos, se um dia você quiser. **Não
> adianta pagar créditos para aumentar a cota dos modelos free** — o teto continua o mesmo.

## Testar

```
olá! Me diga em uma linha qual modelo você é.
```

## Problemas comuns desta rota

| Problema | Solução |
|----------|---------|
| `Free usage exceeded, add credits` | **Não é problema de saldo.** É a cota do dia estourando. Espere ~10–24 h ou use outra rota |
| Modelo que estava free sumiu | Normal: o lineup roda (rotação). Escolha outro modelo free da lista |
| Erro `429` | Cota estourada ou servidor sobrecarregado — troque de modelo ou aguarde |