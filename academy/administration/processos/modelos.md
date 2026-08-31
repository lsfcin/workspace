# Modelos de Pareceres e Despachos Acadêmicos
> Biblioteca de minutas e textos padronizados para atos administrativos no SIPAC/UFRPE.

## 1. Parecer Favorável (Deferimento Total)

```markdown
Ao Departamento de Computação - DC/UFRPE e à Coordenação de Bacharelado em Ciência da Computação,

Após análise da documentação acostada ao Processo nº {{NUMERO_PROCESSO}}, referente ao pedido de aproveitamento de estudos e dispensa de disciplinas do(a) discente {{NOME_DISCENTE}}, manifesto-me FAVORÁVEL à dispensa da unidade curricular {{CODIGO_NOME_DISCIPLINA_UFRPE}} ({{CH_UFRPE}}h).

A disciplina correspondente cursada na instituição de origem {{NOME_IES}} — {{CODIGO_NOME_DISCIPLINA_ORIGEM}} ({{CH_ORIGEM}}h, aprovado com nota {{NOTA}}) — contempla carga horária equivalente e compatibilidade superior a 80% do conteúdo programático, atendendo plenamente aos requisitos da Resolução CEPE/UFRPE nº 744, de 22 de Agosto de 2024 e dos Art. 282 a 286 do Regulamento Geral da Graduação da UFRPE.

Recife-PE, {{DATA_ATUAL}}.

{{NOME_DOCENTE}}
Professor do Magistério Superior – DC/UFRPE
```

---

## 2. Parecer Favorável Conjugado (2+ Disciplinas de Origem $\rightarrow$ 1 UFRPE)

```markdown
Ao Departamento de Computação - DC/UFRPE e à Coordenação do Curso,

Após análise da documentação acostada ao Processo nº {{NUMERO_PROCESSO}}, referente ao pedido do(a) discente {{NOME_DISCENTE}}, sou de parecer FAVORÁVEL à dispensa da disciplina {{DISCIPLINA_UFRPE}} ({{CH_UFRPE}}h), mediante a integralização conjunta das disciplinas cursadas na {{NOME_IES}}:
1. {{DISCIPLINA_ORIGEM_1}} ({{CH_1}}h)
2. {{DISCIPLINA_ORIGEM_2}} ({{CH_2}}h)

O somatório de carga horária e a conjugação dos conteúdos programáticos cobrem integralmente o programa exigido pela UFRPE, em consonância com a Resolução CEPE/UFRPE nº 744/2024.

Recife-PE, {{DATA_ATUAL}}.
```

---

## 3. Parecer Desfavorável (Indeferimento)

```markdown
Ao Departamento de Computação - DC/UFRPE e à Coordenação do Curso,

Após análise da documentação do Processo nº {{NUMERO_PROCESSO}} do(a) discente {{NOME_DISCENTE}}, manifesto-me DESFAVORÁVEL ao pedido de dispensa da disciplina {{DISCIPLINA_UFRPE}} pelos seguintes motivos:

- [ ] Carga Horária Insuficiente: A disciplina cursada ({{CH_ORIGEM}}h) possui carga horária inferior à exigida pela UFRPE ({{CH_UFRPE}}h), em desacordo com o Art. 283 do RGG/UFRPE.
- [ ] Incompatibilidade de Conteúdo: A ementa apresentada não atinge o percentual mínimo de 80% de convergência programática com o plano pedagógico da disciplina na UFRPE (defasagem nos tópicos: {{TOPICOS_FALTANTES}}).

Recife-PE, {{DATA_ATUAL}}.
```

---

## 4. Despacho de Diligência / Solicitação de Ementa

```markdown
À Coordenação do Curso,

Para fins de análise técnica conclusiva do pedido de dispensa, faz-se necessária a juntada pelo(a) requerente da ementa e programa detalhado oficial da disciplina {{NOME_DISCIPLINA}}, devidamente autenticada pela IES de origem, visto que o documento anexado encontra-se ilegível ou incompleto.

Recife-PE, {{DATA_ATUAL}}.
```
