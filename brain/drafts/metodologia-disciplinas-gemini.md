# Metodologia Macro de Disciplinas — Proposta & Plano (Gemini, 2026-09-04)

> **Escopo:** Disciplinas de projeto (*Tecnologias na Educação* e *AI4Good* — UFRPE / CIn-UFPE).  
> **Estrutura:** 34 encontros (17 semanas em regime duplo: Quarta Conceitual + Sexta Prática/Produto).  
> **Revisão:** Atualizado após cotejamento sóbrio com o estado real (`outputs/metodologia-disciplinas-estado.md`)
> e a síntese da literatura revisada por pares (`outputs/metodologia-disciplinas-sota.md`).

---

## 1. Investigação: Respaldo Científico Genuíno (Sem Falsa Certeza)

A revisão rigorosa da literatura desmonta intuições ingênuas e estabelece a fronteira real da evidência:

| Eixo Pedagógico | Evidência Revisada por Pares | Implicação de Desenho | O que a Evidência VETA |
|---|---|---|---|
| **Gamificação & XP** | Sailer & Homner (2020); Li, Hew & Du ($g=0.277$ p/ competência); Cameron et al. (2001). | XP não é nota nem mecânica mágica: é visualização de critérios já atingidos (contingente ao mérito). | **VETA ranking público e exposição.** Rogers & Feller (2016, $N=5.740$): expor o excelente gera desistência. |
| **Sequenciamento da Técnica** | Sinha & Kapur (2021, $g=0.36\text{--}0.87$); Gorbunova et al. (2023); Kalyuga (2007). | Regra por tipo: conceito novo entra após tentativa (PS-I); ferramenta/setup entra antes (direta). | **VETA um modo único.** A inércia "QUA teoria $\to$ SEX prática" é o arranjo mais fraco em retenção. |
| **Rubrica & Pares** | Panadero & Jonsson ($g=0.45$); Double et al. (2020, $g=0.31$); Falchikov & Goldfinch (2000). | Avaliação por pares intergrupos global sobre poucos critérios (3 por missão, escala A/AP/NA). | **VETA inflação de critérios.** Refinar além de 3 a 5 critérios não traz ganho e reduz a concordância. |
| **Banca Examinadora** | Abuzied & Nabag (2023, $\alpha=0.50 \to 0.75\text{--}0.80$ com folha estruturada). | Adoção mandatória da folha de critérios de banca do TecEdu para o AI4Good. | **VETA banca de impressão livre.** Sem folha de critérios prévios, a concordância dos avaliadores desaba. |
| **Specs / Mastery Grading** | Hackerson et al. (2024, revisão de escopo em STEM). | Adotada como *decisão de governança/transparência*, não como verdade comprovada empiricamente. | **VETA alegar respaldo inexistente.** Não há consenso nem dados robustos de eficácia em STEM. |

---

## 2. Decisões Estruturais & Correção de Rumos

1. **Visibilidade do Painel: Estritamente Privado.**
   * O rascunho anterior sugeria "dashboard aberto publicado". Isso foi descartado diante de Rogers & Feller:
     cada aluno visualiza **exclusivamente a sua barra** e a da sua equipe (opcionalmente contrastada com a
     *mediana da turma agregada e anônima*).
2. **Capacitação Técnica Híbrida (Regra por Tipo de Conhecimento):**
   * *Habilidade instrumental / setup:* Andaime explícito no início (roteiro passo a passo e modelos).
   * *Conceito / solução de problema:* Problema autêntico antes da técnica (a turma esbarra na limitação na sexta,
     a teoria entra na quarta para sistematizar o desbloqueio).
3. **Equalização Imediata das Assimetrias:**
   * O TecEdu já roda a grade A/AP/NA (6 missões $\times$ 3 critérios) e folha de banca.
   * O AI4Good deve herdar essa mesma estrutura: definir 3 critérios objetivos por prática e adotar a folha de banca.

---

## 3. O Calendário Canônico vs. Transição 2026.2

### A. O Modelo Canônico (Semestre Completo — 17 Semanas)
```
[ARCO 1: PROBLEMATIZAÇÃO & FERRAMENTAL] (Semanas 01–04 / Encontros 01–08)
  ├── Enquadramento do tema real, contrato pedagógico e setup instrumental guiado
  └── Exploração de dores autênticas com as 7 alavancas contra o óbvio
[ARCO 2: CONSTRUÇÃO & PROVA DE CONCEITO] (Semanas 05–09 / Encontros 09–18)
  ├── GATE 1 (Fechamento preliminar): Pitch gravado/ao vivo + Termo de Projeto + Persona
  └── Ciclos de arquitetura, prototipagem inicial e verificação parcial (Módulos A e B)
[ARCO 3: SPRINT EXPERIMENTAL & REDAÇÃO] (Semanas 10–14 / Encontros 19–28)
  ├── Execução de experimentos sistemáticos (ablação, métricas, testes com usuários)
  └── GATE 2 (Status Report): Demo funcional preliminar + Seções 1 a 3 do artigo
[ARCO 4: IMPACTO & DEFESA PÚBLICA] (Semanas 15–17 / Encontros 29–34)
  └── GATE 3 (Final): Banca examinadora com folha estruturada + Demo WOW + Artigo SBC/IEEE
```

### B. Regra de Transição para 2026.2 (~27 Encontros Restantes)
* **Semana-base:** Não mexer no calendário oficial publicado no Notion.
* **Ajuste operacional:** Introduzir o par *Exemplo Bom / Ruim* e a folha estruturada nos marcos restantes.
  No AI4Good, converter as práticas pendentes para o formato de 3 critérios objetivos antes da submissão.

---

## 4. O Sistema de Acompanhamento (Painel & "XP de Maestria")

### A. A Anatomia Unificada da Entrega (Tríade Fechada)
Toda solicitação de entrega (Missão no TecEdu ou Prática no AI4Good) exige:
1. **Modelo (Starter):** Esqueleto de documento ou repositório base pré-configurado.
2. **Contraste Didático:** Par explícito de *Exemplo Positivo* (o que atinge a régua) vs.
   *Exemplo Negativo* (o erro comum).
3. **Checklist Binário:** 3 a 5 critérios verificáveis com respostas `A` (Atingido),
   `AP` (Parcial) ou `NA` (Não atingido).

### B. A Arquitetura do Painel Pessoal
* **Onde vive:** Planilha Google mestre alimentada por formulários (`gforms`).
* **Visualização:** Consulta individualizada (visão de cada aluno via script ou link pessoal seguro).
* **Mecânica visual:** Barra de preenchimento (`SPARKLINE`) que sobe com base em critérios atingidos comprovados,
  sinalizando a proximidade do próximo Gate.

---

## 5. Roteiro Enxuto de Implementação (Zero-Overhead)

1. [ ] **AI4Good:** Escrever 3 critérios binários (A/AP/NA) para as práticas restantes do semestre.
2. [ ] **AI4Good:** Adotar a folha de avaliação de banca já existente no TecEdu.
3. [ ] **Ambas:** Adicionar 1 exemplo negativo explícito aos decks de entrega das próximas missões.
4. [ ] **Painel:** Prototipar a visão privada da planilha sem expor nomes nem notas da turma.
5. [ ] **Norma:** Submeter a redação final a Lucas para inclusão na base de ensino após validação em sala.
