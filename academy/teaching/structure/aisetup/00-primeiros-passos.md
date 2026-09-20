# Passo 0 — Primeiros passos: instalar o OpenCode

> O OpenCode é um assistente de programação que roda no terminal. Ele conversa com você, lê seus arquivos, edita código
> e roda comandos — usando um "cérebro" (modelo de IA) que você escolhe. Este guia ensina a instalar e a escolher o
> cérebro grátis.

## O que você precisa

- Um computador com acesso à internet
- Um terminal: **Linux/macOS** ou **PowerShell** (Windows)
- Uma conta de email (e, dependendo da rota, conta Google, GitHub ou conta NVIDIA)

## 1. Instalar o OpenCode

### Linux (e macOS)

Abra o terminal e rode:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Se preferir com npm (Node.js instalado):

```bash
npm install -g opencode-ai
```

### Windows

Abra o **PowerShell** (menu Iniciar → digite "PowerShell") e rode:

```powershell
irm https://opencode.ai/install.ps1 | iex
```

Se preferir com npm (Node.js instalado):

```powershell
npm install -g opencode-ai
```

> **Alternativa avançada (opcional):** no Windows, muitos programadores usam o **WSL** (subsistema Linux). Se você
> quiser, instale o WSL e siga as instruções de Linux dentro dele. Não é necessário para este guia.

### Verificar a instalação

```bash
opencode --version
```

Deve aparecer um número de versão (ex.: `1.2.30`).

## 2. Conceitos básicos (aprender antes de continuar)

| Comando | O que faz |
|---------|-----------|
| `opencode` | Abre o assistente dentro da pasta do seu projeto |
| `/connect` | Conecta um provedor de IA (você cola uma API key) |
| `/models` | Mostra a lista de modelos disponíveis e permite trocar |
| `/new` | Começa uma nova conversa |

**O fluxo é sempre o mesmo:**

1. Você pega uma API key grátis no site do provedor (os roteiros 1–4 explicam)
2. `opencode` → `/connect` → escolhe o provedor → cola a key
3. `/models` → escolhe o modelo
4. Pronto: converse em português e peça tarefas de programação

**Onde as keys ficam guardadas:** em `~/.local/share/opencode/auth.json` (Linux) ou
`%USERPROFILE%\.local\share\opencode\auth.json` (Windows). Ninguém além de você deve ter acesso a esse arquivo.

## 3. Teste rápido do setup

Depois de conectar um provedor (roteiros 1–4), teste com:

```
olá! Me diga em uma linha qual modelo você é.
```

Se responder, seu setup está funcionando.

## Checklist

- [ ] `opencode --version` mostra uma versão
- [ ] `opencode` abre o terminal interativo
- [ ] `/connect` adicionou pelo menos um provedor
- [ ] `/models` mostra modelos do provedor
- [ ] O modelo respondeu a uma mensagem