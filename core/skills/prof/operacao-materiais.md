---
name: operacao-materiais
description: >
  Operação docente e distribuição de materiais — Cloudflare Pages, dual-view humanos/agentes, gforms, QR codes e áudio.
---

# /prof operacao-materiais

> Operação docente e distribuição de materiais — Cloudflare Pages, dual-view humanos/agentes, gforms, QR codes e áudio.

---

## Fundamentos & Evidências Científicas

- **Princípios de Engenharia Aplicados à Docência**:
  - **Git como Fonte Única da Verdade**: Todos os materiais de disciplina nascem e vivem como arquivos Markdown (`.md`) no workspace do professor (`academy/teaching/classes/<disciplina>/`). Zero dependência de LMSs proprietários lentos, opacos ou que exigem autenticações burocráticas que travam a dinâmica de sala de aula.
  - **Distribuição Descentralizada e de Baixa Latência**: Espelhamento estático no Cloudflare Pages via repositório público `lsf-links` (`outputs/links/`). Deploys em segundos, zero custo de infraestrutura e imunidade a oscilações de rede da universidade.
  - **Arquitetura Dual-View Nativa**: A mesma fonte `.md` atende simultaneamente às necessidades cognitivas humanas (estética rica, responsividade mobile, temas) e aos harnesses de agentes autônomos (endpoints limpos e ingestão direta via `curl`).

---

## Casos Reais de Sucesso (Benchmarks de Vanguarda)

- **Open Courseware Moderno Baseado em Git** (UC Berkeley CS61A & MIT The Missing Semester):
  - Disciplinas de referência mundial que abandonaram plataformas fechadas de gestão de aprendizagem e migraram 100% de seus roteiros, slides e especificações de projeto para repositórios públicos e páginas estáticas ultra-rápidas. Estudantes consomem o conteúdo sem atrito e colaboram continuamente abrindo pull requests e apontando melhorias em tempo real.
- **Arquitetura Dual-View do Workspace**:
  - Solução que permite aos estudantes visualizarem materiais ricos com temas claro/escuro e tabelas responsivas em seus celulares (`lucassf.pages.dev`), enquanto seus agentes de IA (Claude Code, Antigravity, OpenCode) ingerem a especificação pura via botão *"Copiar p/ Agente (RAW)"* ou comando simples `curl -s ... .md`, sem perda de contexto por parsing de tags HTML.

---

## Protocolo Operacional para o Professor e Agentes

### 1. Disponibilização de Materiais (Acesso Humano vs. Agente)
- **Visualização Rica para Humanos e Mobile**:
  - URL amigável: `https://lucassf.pages.dev/<disciplina>/<name>`.
  - Renderizado pelo visualizador leve nativo (`viewer.js` + `viewer.css` + `marked.min.js`).
  - Suporte total a alertas GitHub (`[!NOTE]`, `[!TIP]`, `[!WARNING]`, `[!IMPORTANT]`, `[!CAUTION]`), tabelas responsivas e temas claro/escuro.
- **Visualização RAW Direta para Agentes e Automações**:
  - Endpoint direto: `https://lucassf.pages.dev/<disciplina>/<name>.md`.
  - Botão *"Copiar p/ Agente (RAW)"* no topo da página.
  - Permite ingestão via terminal: `curl -s https://lucassf.pages.dev/<disciplina>/<name>.md`.
- **Edição Online em Tempo Real (Zero Atrito)**:
  - Botão *"Editar (github.dev)"* na barra de navegação da página.
  - Abre instantaneamente o VS Code Web no navegador diretamente no arquivo do GitHub, permitindo que o professor ou monitores façam correções em sala de aula com commits imediatos.

### 2. Arquitetura Canônica em Dois Níveis
O ecossistema da disciplina opera a partir dos modelos canônicos em `academy/teaching/structure/templates/`:
1. **Página-Mestre da Disciplina (`template-disciplina.md`)**:
   - Centraliza banner visual, canais de comunicação rápida, propósito (Chão $\to$ Horizonte) e grafo do conhecimento.
   - Calendário cronológico de encontros e catálogo de entregas com links para os artefatos.
   - Sistema de pontos acumulados, avaliação intergrupos (+1 ponto) e hall da fama.
2. **Artefatos Modulares Autocontidos (`template-artefato.md`)**:
   - Reúne em um só arquivo a tríade de materiais (modelo, excelente, quase bom/sem alma) e a metodologia construtiva passo a passo com ciclo de 8 etapas.
   - Define de 1 a 3 pontos de verificação objetivos (feito / não feito) para compor a nota na planilha mestre e no SIGAA.

### 3. Automação de Recursos de Sala de Aula
- **Formulários Automatizados via `gforms`**:
  - Criar e gerenciar programaticamente o formulário de abertura e retenção através da skill `gforms`.
  - Automatizar abertura no início do encontro e fechamento no final.
- **QR Codes Dinâmicos nos Slides**:
  - Incluir imagem do QR code visível no slide do Kickoff apontando direto para o formulário.
- **Geração de Podcasts e Áudios Acessíveis**:
  - Para cada deck ou roteiro de aula teórica, converter a narrativa conceitual em um episódio de áudio via Google NotebookLM, disponibilizando o arquivo na pasta da disciplina.

---

## Checklist de Auditoria

- `[ ]` O arquivo `.md` está na pasta canônica da disciplina e versionado no Git?
- `[ ]` A página está publicada no Cloudflare Pages com visualização rica e botão RAW para agentes?
- `[ ]` O link para edição online no navegador (`github.dev`) está ativo e funcional?
- `[ ]` A página da disciplina (`disciplina.md`) e os artefatos modulares (`artefatos/art-*.md`) estão consistentes e devidamente vinculados?
- `[ ]` O formulário da aula (`gforms`) e o QR code correspondente estão prontos e testados?
- `[ ]` Há resumo em áudio acessível gerado para estudo assíncrono?
