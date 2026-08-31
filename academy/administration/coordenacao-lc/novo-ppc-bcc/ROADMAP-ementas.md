## STATUS — BATCH executado (Sonnet, 2026-07-21), aguardando eyeball do Lucas

41/44 disciplinas geradas localmente em `ementas/saida-docx/` (`[MODELO-SIGAA] <nome>.docx`), verbatim-diff + varredura
de alucinação limpas (`ementas/verify.py`, `ementas/hallucination_scan.py`). Auditoria completa em `ementas/gaps.md` +
`ementas/audit.json`. **Nada subiu ao Drive ainda** — gate de revisão do Lucas é pré-requisito do upload.

3 gaps reais sem fonte em lugar nenhum (nem doc próprio, nem consolidado BCC): FUNDAMENTOS DA EDUCAÇÃO, PROJETO
INTEGRADOR EM DESENVOLVIMENTO DE ARTEFATOS EDUCACIONAIS, PROJETO INTEGRADOR EM EDUCAÇÃO EM COMPUTAÇÃO — precisam
conteúdo do professor/Paulo antes de qualquer geração.

Achado importante desta run: a maioria das disciplinas em `OBRIGATORIAS/N Periodo` **não** estava no schema SIGAA
nested-sdt como a seção "BATCH" abaixo assumia — estava num schema antigo "PROGRAMA DA DISCIPLINA" (sem campo OBJETIVOS,
sem CONTEÚDO separado da EMENTA), exigindo remapeamento de campos em vez de simples fallback pro consolidado.
`ementas/extract_old.py` (novo) faz esse remapeamento. 3 bugs reais encontrados e corrigidos no `port.py` "validado"
durante esta sessão (overrun multi-curso por tabela, append-em-vez-de-replace em campo com default do template, regex de
bibliografia sem word-boundary) — ver `brain/INBOX.md`.

Próximo passo: Lucas revisa `saida-docx/` + `gaps.md`; após OK, `drive put --account ufrpe --parent <subpasta> --gdoc
--name "[MODELO-SIGAA] <nome>" <arquivo>` por disciplina.

---

# EMENTAS-ROADMAP — Reformatação das ementas do novo PPC

> Resultado da run de investigação (Sonnet, 2026-07-21). Este arquivo **é** o plano — o ponteiro que
> ficava aqui apontava para `~/.claude/plans/`, estado do harness que nenhum clone deste workspace
> receberia, e que `AGENTS.md` proíbe: plano mora no ROADMAP daquilo que ele muda.

## TL;DR — a reformatação em massa JÁ ESTÁ (quase toda) FEITA

O pedido do Paulo era "colocar as ementas no template novo (SIGAA)". A investigação mostra que **isso já foi feito** em
dois documentos consolidados no Drive `ufrpe` (Maio/2026), ambos em formato de tabela SIGAA:

| Documento | Conteúdo | Formato | id |
|-----------|----------|---------|-----|
| PROGRAMA ... OBRIGATÓRIOS.pdf | **28 componentes** obrigatórios | ✅ tabela SIGAA | `1752k3RJoS7B7Lxb5dgwtQ0cjSpo1qTI_` |
| PROGRAMA ... OPTATIVOS.docx | **102 componentes** optativos (93 tabelas) | ✅ tabela SIGAA | `1CKNht6fYU0Vm1TKlIQihoRSGh1_JcCO9` |

As 2 optativas novas do Lucas (**Inteligência Híbrida**, **Análise Visual do Comportamento Humano**) **já estão
incluídas** no OPTATIVOS.docx.

**Conclusão:** não é uma tarefa de reformatação em lote — é uma tarefa de **completar campos faltantes + confirmar
escopo**. Antes de qualquer produção, resolver os 3 bloqueios abaixo com o Paulo. Fazer reformatação em massa agora =
trabalho jogado fora.

---

## 🚧 Bloqueios a resolver com Paulo ANTES de produzir

### B1. Escopo: LC (Licenciatura) vs BCC (Bacharelado)
Todos os arquivos e a pasta dizem **BCC** (`...OBRIGATÓRIOS`, `Lista ... - BCC.xlsx`, `novo-ppc-bcc/`), mas a demanda é
o **PPC da Licenciatura em Computação (LC)**. As disciplinas listadas são de perfil BCC (Cálculo NI/NII, Teoria da
Computação, Compiladores...). **Pergunta ao Paulo:** o LC reaproveita esse mesmo conjunto de ementas do BCC, ou existe
um conjunto/programa próprio do LC (com práticas de ensino, disciplinas pedagógicas)? A conversa do WhatsApp cita
"práticas de ensino de computação I e II" (EAD, 60h) que **não** aparecem no OBRIGATÓRIOS — indício de que o programa do
LC é diferente/adicional.

### B2. Template canônico (Paulo nunca nomeou o arquivo)
Paulo só falou "template novo"/"formato SIGAA", genérico. Dois candidatos:
- `MODELO EMENTA SIGAA.docx` (`1mvfME9JdnBl46Jm3KkTVy20oUWyfdhde`) — modelo em branco, mas com **tabelas aninhadas** que
  o python-docx NÃO acessa (só 0 top-level). Ruim como base programática.
- Os PROGRAMA docs consolidados (OBRIGATÓRIOS/OPTATIVOS) — tabelas limpas, um-componente-por-tabela, python-docx lê e
  escreve bem. **São a melhor base de fato.**
- **Pergunta ao Paulo:** confirmar que o padrão SIGAA desses PROGRAMA docs é o alvo final. Se ele tiver um MODELO mais
  novo, pegar o link.

### B3. Gap de completude: campo OBJETIVOS vazio de forma sistemática
Medido no OBRIGATÓRIOS: **OBJETIVOS vazio em 24/28** componentes. EMENTA vazia em 2/28. BIBLIOGRAFIA BÁSICA presente em
28/28. Amostra de OPTATIVOS também tem OBJETIVOS vazio. **Este é o trabalho real restante:** preencher OBJETIVOS (e
completar EMENTA/pré-requisitos onde faltam). Isso exige **conteúdo de professor**, não só formatação — o Claude pode
rascunhar OBJETIVOS a partir da EMENTA+CONTEÚDO, mas cada um precisa de revisão do responsável.

---

## Schema SIGAA (referência única — extraído do OBRIGATÓRIOS preenchido)

```
COMPONENTE CURRICULAR: <nome>
CÓDIGO: <cod SIGAA | NOVA se disciplina nova>
PERÍODO A SER OFERTADO: <Nº>
FORMATO DE OFERTA:   ( X ) Presencial   ( ) EaD
CARGA HORÁRIA TOTAL: <Xh>
   Teórica: <Xh> | Prática: <Xh> | Extensão: <Xh> | EaD: <Xh>
PRÉ-REQUISITO:  <(cod) NOME | NÃO TEM>
CORREQUISITO:   <(cod) NOME | NÃO TEM>
EQUIVALÊNCIA:   <(cod) NOME | NÃO TEM>
EMENTA:         <parágrafo corrido>
OBJETIVOS:      <← sistematicamente VAZIO; gap principal>
CONTEÚDO PROGRAMÁTICO:  <lista numerada 1- 2- ...>
BIBLIOGRAFIA BÁSICA:    <lista numerada>
BIBLIOGRAFIA COMPLEMENTAR: <lista numerada>
```
Convenções: checkbox `( X )` marcado; defaults `NÃO TEM`; código `NOVA` para disciplina nova.

---

## Caminho de escrita em Google Docs (decisão do Lucas = "Docs direto", automatizado)

**`core/tools/docs/gdocs` existe (2026-08-25) e NÃO substitui este pipeline.** Ele escreve markdown,
que não carrega a tabela em `sdt` do MODELO SIGAA nem a cópia verbatim das células. O que ele agrega
aqui é a *conferência*: `gdocs read <id>` lê a ementa já convertida sem exportar `.docx`.

**Escrita EXISTE no workspace** — não é só read-only. O `core/tools/files/gdrive` é read-only (scope `drive.readonly`),
MAS `core/tools/files/drive_migrate_core.py` usa **`SCOPES_WRITE = ["https://www.googleapis.com/auth/drive"]`** (escrita
total) com token separado `drive-write`, e já criou pastas/copiou arquivos antes (`find_or_create_folder`, `copy_file`).

Estado dos tokens de escrita (`~/.config/workspace-drive-write/`):
- ✅ `personal.token.json` e `cin.token.json` existem (Lucas já autorizou escrita antes).
- ❌ **`personal` está EXPIRADO/REVOGADO** (`invalid_grant`) e **não há token da `ufrpe`** (conta das ementas).

**Método (validado): geração local OK; upload precisa de 1 re-auth.**
1. `python-docx` copia o MODELO (tabela em `sdt`) e preenche as células → `.docx` individual `[MODELO-SIGAA]
   <disciplina>.docx`. **Validado** com Álgebra Vetorial (dedupe de células mescladas necessário — ver
   `scratchpad/filler.py`).
2. Para upload+conversão automáticos que o Lucas pediu, falta:
   - (i) **re-autorizar escrita na conta ufrpe** (uma vez, browser): `core/tools/files/gdrive auth ufrpe --write
     --reauth` — **o agente roda o comando**, o browser abre na máquina do Lucas e a única parte dele é escolher a conta
     na tela de consentimento.
   - (ii) adicionar método **upload-local-`.docx` + converter p/ Google Doc** (`files().create` com
     `mimeType=application/vnd.google-apps.document` + media) — hoje só existe `copy_file` (copia arquivo já no Drive),
     não upload de arquivo local.
3. Com (i)+(ii): Claude cria pastas, sobe cada ementa, converte p/ Google Doc e organiza — 100% automatizado, sem
   trabalho manual do Lucas.

### Refactor spec — módulo de escrita em Drive (aprovado; executar no Opus, PRÉ-REQUISITO do upload)

Objetivo: tirar a escrita de `drive_migrate` (script específico cin→personal) e criar um seam de Drive read+write,
account-agnostic. Seguir `core/SCHEMA.md` + gerar `.pyi` (interface enforçada).

**Estado atual (verificado nesta sessão):**
- `core/tools/files/gdrive` (CLI) + `drive_fetch.py`: só leitura, scope `drive.readonly`. `DOWNLOAD_DIR =
  ~/Downloads/workspace-drive` (**bug**: deve cair sob `Downloads` — item do Lucas no INBOX).
- `drive_migrate_core.py`: `SCOPES_WRITE=["…/auth/drive"]`, `get_cin_service`/`get_personal_service` (contas hardcoded),
  `find_or_create_folder`, `copy_file`. Auth via `gauth.auth(alias,'drive-write',SCOPES_WRITE)` → token em
  `~/.config/workspace-drive-write/<alias>.token.json`.
- Token `drive-write` da **ufrpe** recém-criado pelo Lucas (validar liveness antes de usar).

**Alvo:**
- `drive_core.py` (novo): `get_service(alias, write=False)`; reexporta `list/search/recent/download`; **novos**:
  `mkdir(alias, name, parent_id, dry_run=False)`, `upload_local(alias, path, parent_id, as_gdoc=False)` → converte
  `.docx`→Google Doc via `files().create(mimeType='application/vnd.google-apps.document', media=MediaFileUpload(path))`,
  retorna `{id, webViewLink}`; `find_or_create_folder` (movido).
- `drive` (CLI): subcomandos novos `mkdir`, `put`, `put --gdoc`. `download` continua.
- `drive_migrate*` → wrapper fino sobre `drive_core`.
- `DOWNLOAD_DIR` configurável, default sob workspace.
- Scope de escrita isolado por conta (já é o padrão do token `drive-write`).

**Validação do refactor:** `mkdir` uma pasta de teste na ufrpe → `put --gdoc` o `[MODELO-SIGAA] Álgebra...docx` →
conferir link/fonte no Docs → limpar teste. Só então rodar o bulk das ementas.

---

## Estrutura de pastas proposta (sob `novo-ppc-bcc/`)
```
novo-ppc-bcc/
  ementas/
    fonte/        # PROGRAMA docs baixados do Drive (referência, não versionar binários grandes)
    template/     # 1-tabela.docx limpo extraído do OPTATIVOS
    saida-docx/   # ementas preenchidas geradas p/ Lucas subir ao Drive
    gaps.md       # tabela componente|campo-faltante (OBJETIVOS etc.)
```
Workspace só versiona estruturais (`.md`); `.docx` grandes ficam em `scratchpad`/Drive, não no git.

---

## Pipeline validado (teste 1 disciplina — Álgebra Vetorial ✅)

`scratchpad/port.py`: para cada disciplina cria um novo `[MODELO-SIGAA] <nome>.docx` a partir do MODELO EMENTA
SIGAA.docx e **preenche VERBATIM** a partir do `.docx`-fonte editável:
- **Cópia byte-a-byte** dos campos existentes (COMPONENTE...BIBLIOGRAFIA) da célula-fonte — Claude NUNCA redigita.
  Elimina invenção de ano/página/título/edição.
- **OBJETIVOS é o ÚNICO campo gerado** (fonte vem vazia), mantido em arquivo à parte; derivado só de EMENTA+CONTEÚDO
  existentes.
- Dedupe de células mescladas (senão duplica valores); **fonte Times New Roman forçada em todos os runs** (senão Docs
  renderiza Cambria).
- Fontes editáveis: `OBRIGATÓRIOS.docx` (`1hvMHdkL35pa6nFxdBcZ7Pz5kHisXSxFj`), `OPTATIVOS.docx`
  (`1CKNht6fYU0Vm1TKlIQihoRSGh1_JcCO9`). Não usar os PDFs (artefatos de extração).

## Execução (só APÓS B1–B3 resolvidos)

1. **Confirmar escopo LC** (B1) → lista de componentes do LC (obrigatórios + optativos + práticas de ensino).
2. **Cruzar a lista com OBRIGATÓRIOS/OPTATIVOS.docx** → `gaps.md`: quais existem, quais faltam campos, quais não
   existem.
3. Para cada disciplina: `port.py` gera `[MODELO-SIGAA] <nome>.docx` (verbatim + OBJETIVOS gerado quando vazio).
4. **Gate de revisão (eyeball)**: Lucas revisa cada doc — especialmente OBJETIVOS gerado. Ordem: obrigatórios →
   optativos → novas/práticas.
5. Upload+conversão p/ Google Doc + organização em pastas (automatizado, após re-auth `drive-write` da ufrpe — ver seção
   de escrita).

## Etapa final — auditoria do que foi criado/modificado + varredura de alucinações

Antes de fechar, rodar uma checagem completa e entregar ao Lucas:

1. **Inventário do que mudou**: listar todos os docs criados (`[MODELO-SIGAA] *`), pastas criadas no Drive, e
   arquivos/tools modificados no workspace. Tabela `disciplina | doc criado | Drive id/link | status`.
2. **Diff verbatim automatizado (anti-alucinação estrutural)**: para cada disciplina, comparar por script cada campo
   copiado do doc gerado **contra a célula-fonte** — devem ser idênticos byte-a-byte (exceto OBJETIVOS). Qualquer
   divergência = bug de porte ou edição indevida → sinalizar. Não confiar em leitura visual pra isso.
3. **Varredura de alucinação nos OBJETIVOS** (único campo gerado): para cada OBJETIVOS, verificar que todo verbo/tópico
   mapeia a um item existente de EMENTA/CONTEÚDO daquela disciplina; nenhum conceito, ferramenta, autor ou número novo.
   Marcar dúvidas.
4. **Tabela final de campos preenchidos por conta própria** (entregável ao Lucas): `disciplina | campo | conteúdo gerado
   | item-fonte que embasa`. Um item por linha.
5. **Checagem de fidelidade visual**: abrir ao menos 1 doc convertido no Google Docs e confirmar fonte (Times New
   Roman), estrutura da tabela e ausência de Cambria/duplicação.

## Verificação (gates de saída)
- `gaps.md` cobre 100% dos componentes da lista LC confirmada.
- Diff verbatim: 100% dos campos não-OBJETIVOS idênticos à fonte.
- Todo OBJETIVOS gerado consta na tabela final com item-fonte que o embasa.
- Nenhum `.docx` subiu ao Drive sem OK do Lucas.
- 1 doc conferido visualmente no Docs (fonte + tabela ok).

---

## Efeito colateral desta run (registrar)
- **pandoc instalado** (`pip install pypandoc-binary` no `.venv`; symlinks no bin do venv e em `~/.local/bin/pandoc`).
  `core/tools/paper/parse` agora lê `.docx`. Melhoria durável — anotar no `brain/INBOX.md`.

---

# BATCH — execução (Sonnet, sessão NOVA) — decisões travadas 2026-07-21

**Decisões do Lucas:** novos docs = **MODELO preenchido com o conteúdo da disciplina** (verbatim + OBJETIVOS só quando
faltar). Executor = **Sonnet, sessão nova** (mecânico; precisão é estrutural via script+auditoria; esta sessão Opus
estava em 80%). Prefixo = **`[MODELO-SIGAA]`** (hífen). Escrita 100% automatizada (write path pronto).

## Pasta-alvo real (Drive ufrpe)
`EMENTAS` = `1fWoNtOt1bnw3Jh-Idl1d-3jUjjAtr4fp` (`00_comissão PPC_2026/EMENTAS`). Cada ementa vira `[MODELO-SIGAA]
<mesmo nome>` **na mesma subpasta**.

| Subpasta | id | escopo |
|----------|-----|--------|
| OBRIGATORIAS | `1OFz7PRrLAphkRZ8RK1QTOIC5vslBmb1q` | **alvo** — 9 subpastas "N Periodo" (~43 docs) + MODELO + REMOVIDAS |
| NOVAS DISCIPLINAS PROPOSTAS | `1yPgYMan_Z2jgD1FR5Ve8hw0sjdiZ0rNG` | **alvo** — 6 docs diretos |
| OPTATIVAS | `1VRXpkY3zA3Lcdpm6Wm1R_koD6CnzUlTa` | vazia hoje |
| Outros | `19BItGCNdIOh7wSuPBtOrQIV6qlRYUQss` | 37 docs **legado** (códigos antigos, .doc) — provável FORA; confirmar c/ Lucas |
| OBRIGATORIAS/REMOVIDAS | — | FORA |

Períodos (OBRIGATORIAS): `1 Periodo=1TvICk8Hxq4x4YwINRwb45NYdXvIHHOH6`; demais: re-listar via `drive` (ids mudam pouco).
Re-inventariar no início (fonte da verdade = Drive).

## Formatos-fonte (variam — tratar cada)
- **Fonte JÁ é o MODELO SIGAA** (tabelas aninhadas em `sdt`, não top-level). `python-docx .tables` retorna 0 — extrair
  via `element.body.findall(qn('w:tbl'))`. **`port.py` atual lê tabelas TOP-LEVEL (formato consolidado) — PRECISA
  adaptar p/ nested-sdt.**
- **Estados**: preenchida (ex. INTELIGÊNCIA HÍBRIDA.docx — copiar verbatim) vs **template vazio** (ex. 0001 FUNDAMENTOS
  — sem conteúdo). Regra: fonte preenchida → verbatim; **fonte vazia → NÃO inventar**; puxar do consolidado
  (`OBRIGATÓRIOS.docx` `1hvMHdkL…` / `OPTATIVOS.docx` `1CKNht6f…` na pasta "Comissão PPC - 2026") OU flag pro Lucas.
- **Google Docs** (maioria): `download_file` hoje exporta gdoc→**PDF** (ruim p/ tabela). Adicionar export **gdoc→.docx**
  (`EXPORT_MIME[GDOC]='…wordprocessingml.document'`) p/ ler verbatim. `.doc` antigo (só em Outros/legado).

## Pipeline por disciplina
1. Baixar fonte (gdoc→.docx export; .docx direto).
2. Extrair campos **VERBATIM** das tabelas nested-sdt (`ementas/port.py`, adaptado).
3. OBJETIVOS: gerar só se vazio, mapeado 1:1 ao CONTEÚDO, **sem AISlop/alucinação** (datas/anos/páginas/títulos = nunca
   inventar; verbatim only).
4. Preencher MODELO fresco (`ementas/filler.py`: dedupe células mescladas + **Times New Roman em todos os runs** — senão
   Cambria no Docs).
5. Upload: `core/tools/files/gdrive put --account ufrpe --parent <id_subpasta> --gdoc --name "[MODELO-SIGAA] <nome>"
   <arquivo.docx>` → converte p/ Google Doc na mesma subpasta.

## Ferramentas prontas (desta run)
- **Write path**: `core/tools/files/gdrive` (branch `feature/drive-core-write`, commit `5726518`, pushed) — `mkdir`,
  `put`, `put --gdoc`, `auth --write/--reauth`. `drive_core.py` = seam read+write. **Token `drive-write` da ufrpe já
  vivo.**
- **Scripts**: `ementas/port.py` + `ementas/filler.py` (persistidos; port.py precisa da adaptação nested-sdt + gdoc
  export).
- Se auth falhar (`invalid_grant`): `drive auth ufrpe --write --reauth` (sessão interativa).

## Etapa final (obrigatória) — auditoria + anti-alucinação
Ver seção "Etapa final" acima: inventário do que foi criado, **diff verbatim automatizado** (campo gerado vs
célula-fonte, byte-a-byte exceto OBJETIVOS), varredura de alucinação nos OBJETIVOS, tabela final dos campos preenchidos
por conta, eyeball de ≥1 Doc convertido. Gate: nada fica sem OK do Lucas.
