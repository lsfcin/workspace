# Core SPECS
> Architecture decisions and conventions for the Core agent library.

---

## Architecture Decisions

### AD-01 — AGENTS.md como entrypoint universal (2026-06-18)
`WORKSPACE.md` renomeado para `AGENTS.md`. Todos agentes (Copilot, Codex, OpenCode, Claude Code) leem `AGENTS.md` nativa ou via `@AGENTS.md` em `CLAUDE.md`. Elimina bifurcação de descoberta entre agentes.

### AD-02 — Frontmatter `description:` obrigatório em skills (2026-06-18)
Todas skills em `core/skills/*.md` devem ter frontmatter YAML com `name:` e `description:`. O `context_synchronizer.py` lê o campo `description:` (incluindo block scalars YAML `>` e `|`) para popular o routing table automaticamente. Template em `core/skills/_template.md`.

### AD-03 — google_auth.py como módulo auth compartilhado (2026-06-18)
Auth OAuth2 Google centralizado em `core/tools/google_auth.py`. Todos serviços Google (gmail, drive, calendar, slides futuro) importam deste módulo. Tokens separados por serviço em `~/.config/workspace-{service}/{alias}.token.json`. Credentials em `~/.config/workspace-gmail/credentials.json` (projeto GCP 1048141740528) servem todos os serviços.

### AD-04 — Slides: Slidev + Vue (2026-06-18)
Decisão de stack para apresentações profissionais: **Slidev** (Markdown + Vue). Razões: (1) source file texto puro editável por agente, git-versionável; (2) animações Vue nativas (`v-click`, `@vueuse/motion`, springs); (3) vídeo nativo via `<SlidevVideo>`; (4) interatividade (componentes Vue, Monaco live coding). Google Slides mantido para colaboração/aulas cotidianas. Quarto descartado para slides (melhor para papers com código executável). Remotion = vídeo, não slides.

### AD-05 — Porte Google Slides → Slidev via API JSON (2026-06-18)
Formato intermediário para conversão: Google Slides API JSON (não PPTX, não HTML). A API retorna estrutura completa (texto, posições, imagens, notas) em JSON limpo. PPTX é XML verboso com perda de layout; HTML do Google é minificado/ilegível. Requer habilitar Google Slides API no GCP project 1048141740528.

### AD-06 — Convenção de pastas `refs/` em skills (2026-07-05)
Qualquer skill que acumule referências externas (papers, links, pesquisas, notas de leitura) deve manter uma pasta `refs/` no **mesmo nível do arquivo da skill**. Exemplo: `core/skills/prepare/refs/`. A pasta `refs/` é **excluída do sync** (o `sync-skills` copia apenas o `<name>.md` e gera o symlink; não toca em subpastas). Isso evita poluir os mirrors com arquivos auxiliares e mantém o source of truth limpo. Future agents must follow this convention when creating or updating skill-related reference folders.

### AD-07 — Agrupamento de sub-skills em pastas (2026-07-05)
Skills que formam um **suite** lógico (compartilham namespace, domínio ou prefixo comum) devem ser agrupadas em uma **pasta**, com uma **skill pai** atuando como roteador. Regras:

1. **Estrutura da pasta:** `core/skills/<suite>/` contém:
   - `SKILL.md` — skill pai (frontmatter YAML obrigatório, `name: <suite>`, atua como roteador/índice)
   - Sub-skills: `<slug>.md` — sem prefixo do suite (ex: `core/skills/foundry/canvas.md` em vez de `foundry-canvas.md`)
   - `refs/` — seguindo AD-06, se houver referências coletivas do suite

2. **Skill pai (SKILL.md):** deve listar as sub-skills em uma tabela com `When to load`, incluir o bloco `<!-- routing:start -->` com links para cada sub-arquivo, e nunca implementar lógica operacional (apenas roteamento/meta-info).

3. **Sub-skills:** cada uma tem frontmatter YAML completo (não herda do pai), e nome curto (sem prefixo).

4. **sync-skills** gera symlinks apenas para o `SKILL.md` do suite. Sub-skills são carregadas manualmente via skill pai (`Load subfiles relevant to the task`).

5. **Motivação:** evita poluir `core/skills/` com dezenas de arquivos flat; mantém skills relacionadas coesas; o padrão `foundry-*` foi o gatilho.

---

### AD-08 — Flows: posse, composição e ciclos (2026-07-23)
Extensão de AD-07 para a camada de **flows**. Contrato completo em [`SCHEMA.md`](SCHEMA.md) § *Composition and cycles*; aqui fica a decisão e o porquê.

1. **Posse define o lugar.** Flow que pertence a uma *dispatcher skill* mora em `core/flows/<skill>/`, e **o nome do arquivo é igual ao sufixo do comando**: `research scout` ⟺ `core/flows/research/scout.md`. Flow sem dono fica flat em `core/flows/`. O eixo é **independência de invocação**, não composição — `scout` compõe `deep`/`literature` e mesmo assim é sub-flow.

2. **Vocabulário: "flow" é o termo canônico.** "Loop" foi aposentado para o sentido de agentes conectados (virou buzzword). *Flow* é mais preciso: um loop vai do fim ao começo sem ramificação e com uma saída só; nossos procedimentos ramificam, escapam e compõem. Loop continua válido só para um repeat de verdade.

3. **Flows compõem** via `uses:`. Composto-vs-folha **não é um tipo** — é só se o flow invoca outros ou não. Não existe camada "orquestrador" no schema.

4. **Dois tipos de ciclo, só um é legal.** Ciclo **definicional** (A é construído a partir de B, B a partir de A) é **proibido** — nunca termina de expandir; o grafo `uses:` tem que ser um DAG, verificado estaticamente. Ciclo de **execução** (um flow volta a um passo anterior) é **permitido**, com teto de iterações + condição de saída — isso é iteração, o estado muda a cada passada. Um trace `A → B → C → A` não viola o DAG: a seta de volta é o loop interno de `A`, não uma aresta que `B`/`C` declaram.

5. **Nenhum flow é privilegiado.** O status de "reference implementation / oracle do validador" que `deepresearch` tinha foi **aposentado** — acoplava a evolução de um flow ao schema. O exemplar é `flows/_template.md`; realismo vem do `validate_flows` rodar sobre *todos* os flows, inclusive o template. (Lucas: *"a template should be a template. just that."*)

6. **Motivação:** o gatilho foi a assimetria `deepresearch` (flow) vs `/research scout` (sub-flow) — que se revelou apenas lexical, mas expôs a falta de regra de posse e de um modelo de composição.

---

## Conventions

- **Nome de arquivo: uma palavra só, e a palavra inteira** (preferência do Lucas, 2026-07-23). Truncação perde para a palavra completa: `architect` > `arch`, `literature` > `lit`. Nome que repete o namespace do pai é ruído — sob `research/`, `deepresearch.md` gagueja (`research deepresearch`), então virou `deep.md`. Nomes genéricos e óbvios devem ser **reservados** para o flow que realmente os merece: `explore` ficou com o loop de tentar ideias justamente para deixar `experiment` e `optimize` livres para flows futuros distintos.
- Nova skill (flat): copiar `core/skills/_template.md`, preencher frontmatter.
- Nova skill (suite): criar `core/skills/<suite>/SKILL.md` + sub-arquivos `<slug>.md`.
- Sub-skills relacionadas em pasta são sempre preferidas a skills flat com prefixo longo quando > 2 sub-skills.
- Novos serviços Google: importar `google_auth.py`, definir `SCOPES` e `CONFIG_DIR`, seguir padrão de `drive_fetch.py`.
- Tokens OAuth nunca commitados — ficam em `~/.config/workspace-*/`.
- **Pasta `refs/` em skills**: quando uma skill acumular referências externas, criar `core/skills/<name>/refs/` (ou `core/skills/<suite>/refs/`) e manter todos os arquivos de referência lá. Não criar `refs/` dentro de `.opencode/skills/` ou `.claude/skills/` — esses são mirrors gerados automaticamente.
- **Formato de arquivos em `refs/`**: notas de leitura, links rápidos e sumários informais vão em `*.md`. Referências estruturadas (papers com metadados, datasets com schema, configurações de ferramentas) vão em `*.yaml` com frontmatter ou schema claro. Preferir YAML para anything que uma skill vai parsear ou que precisa de schema.
