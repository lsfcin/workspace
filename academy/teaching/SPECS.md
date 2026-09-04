# Metodologia de Ensino — Especificação Raiz
> O que deve ser verdade em toda aula teórica ou prática e em toda condução de disciplina.
> Contrato de planejamento e auditoria para o professor e agentes (Antigravity, Claude Code, etc.).

## 1. Princípio & Horizonte

Toda atividade de ensino parte do chão e aponta para o horizonte:
- **Ancoragem real (o chão):** conecta direto com as dores, contradições e problemas concretos que
  os alunos vivem hoje. Nada de teoria abstrata sem dono.
- **Horizonte crível (a direção):** desenha futuros possíveis e melhores nos quais dá para
  acreditar e trabalhar para construir. A tecnologia e a teoria entram como ferramentas de agência e
  emancipação, nunca como fim em si mesmas.

---

## 2. Acessibilidade Universal & Desenho Inclusivo

Acessibilidade não é pós-processamento, é requisito de projeto:
- **Auditoria de Turma:** No início de cada semestre, registrar demandas específicas de
  acessibilidade dos alunos matriculados.
- **Adaptação para Deficiência Visual (ex.: alunos cegos):**
  - **Áudio / Podcasts:** Gerar obrigatoriamente um resumo em áudio / podcast explicativo para cada
    aula (via NotebookLM, Gemini Notebook ou equivalente), narrando a lógica conceitual dos slides.
  - **Audiodescrição Ativa:** Ao apresentar diagramas, imagens e quadros, verbalizar explicitamente
    a estrutura e as relações em vez de usar expressões vazias como "vejam aqui" ou "essa seta liga nisso".
  - **Artefatos Legíveis por Leitores de Tela:** Código, roteiros e textos de apoio devem estar em
    markdown limpo, estruturados com níveis hierárquicos de cabeçalho bem definidos.

---

## 3. Contrato para Agentes (Protocolo de Ensino)

Agentes que manipulam materiais de ensino neste repositório devem seguir este protocolo:
- **Planejamento ou Auditoria de Aula (nível micro):** Seguir as regras de [`SPECS-aulas.md`](SPECS-aulas.md)
  (Kickoff de 10 min, QR Code de retenção, dupla codificação, modelagem com contraste e checklist).
- **Planejamento ou Auditoria de Disciplina (nível macro):** Seguir as regras de
  [`SPECS-disciplinas.md`](SPECS-disciplinas.md) (os 4 Arcos, Tríade de entrega, painel privado de maestria,
  regra de sequenciamento e folha de banca).

<!-- routing:start -->
## Routing

| Shard | Description | Governs |
|-------|-------------|---------|
| [`SPECS-aulas.md`](SPECS-aulas.md) | Contrato de planejamento e auditoria para aulas teóricas e práticas (nível micro). | toda aula teórica ou prática ministrada por Lucas |
| [`SPECS-disciplinas.md`](SPECS-disciplinas.md) | Metodologia macro semestral de condução, ciclos de projeto, avaliação e acompanhamento. | todas as disciplinas de graduação e pós ministradas por Lucas (TecEdu, AI4Good) |
<!-- routing:end -->
