---
name: avaliacao-maestria
description: >
  Arquitetura de avaliação e feedback contínuo — critérios atômicos, feedback em tempo real em sala, painel e bancas.
---

# /prof avaliacao-maestria

> Arquitetura de avaliação e feedback contínuo — critérios atômicos, feedback em tempo real em sala, painel e bancas.

---

## Fundamentos & Evidências Científicas

- **Dylan Wiliam & Grant Wiggins** (*Educative Assessment* & *Embedded Formative Assessment*):
  - A avaliação só gera aprendizagem real quando fornece feedback oportuno que permite ao estudante corrigir sua rota enquanto ainda há tempo. Notas frias devolvidas semanas depois de uma entrega têm impacto formativo praticamente nulo (são autópsias, não diagnósticos).
- **Ernesto Panadero & Anders Jonsson** (*Educ Psych Rev* 2023):
  - Meta-análise comprova ganho significativo de desempenho com o uso de rubricas transparentes ($g=0.45$). O fator crítico é a clareza e o conhecimento prévio dos critérios pelos alunos antes da execução; refinar excessivamente escalas de pontos numéricos não compra melhoria adicional.
- **Keith S. Double et al. (2020) e Falchikov & Goldfinch (2000)**:
  - A avaliação por pares entre equipes possui validade e calibração equiparáveis às do professor ($g=0.28$) quando ancorada em julgamentos globais sobre poucos critérios atômicos bem compreendidos.
- **Abuzied & Nabag (BMC Med Educ 2023)**:
  - Bancas examinadoras orientadas por folha de critérios padronizada alcançam alta confiabilidade ($\alpha=0.75\text{--}0.80$); bancas livres sem folha caem para $\alpha=0.50$.
- **Todd Rogers & Avi Feller** (*Psychol Sci* 2016):
  - A exposição a rankings nominais públicos gera desmotivação e abandono entre estudantes em desvantagem. O progresso deve ser visualizado de forma estritamente privada.

---

## Casos Reais de Sucesso (Benchmarks de Vanguarda)

- **Mastery-Based Grading em Ciência da Computação** (Stanford University & UIUC):
  - Cursos de sistemas e algoritmos que aboliram a curva normal punitiva e adotaram listas de critérios atômicos binários (*pass/re-try*). Alunos que não atingem um critério recebem feedback imediato e podem ressubmeter o código corrigido. O modelo gerou retenção conceitual 30% superior em disciplinas subsequentes e praticamente erradicou o estresse de véspera de prova.
- **Intervenções Formativas em Larga Escala** (Dylan Wiliam, Reino Unido):
  - Programas educacionais onde o feedback descritivo imediato substituiu notas numéricas parciais ao longo do processo construtivo. Turmas submetidas a essa dinâmica dobraram a taxa de progresso anual em comparação com pares sob avaliação somativa tradicional.

---

## Protocolo Operacional para o Professor e Agentes

### 1. Critérios de Aceite Atômicos e Binários
- **Adeus às Notas Subjetivas Soltas**: Em vez de atribuir "nota 7 ou 8 por impressão estética", cada entrega é decomposta em critérios binários explícitos:
  - `[ ]` O repositório possui README com instruções de instalação que executam sem erro?
  - `[ ]` A API responde no endpoint `/predict` com payload JSON válido e latência $< 200\text{ms}$?
  - `[ ]` Os testes unitários cobrem ao menos 80% das funções de transformação de dados?
- Cada critério atingido adiciona o XP correspondente na barra de maestria do estudante/equipe.

### 2. O Rito da Aula Avaliativa (70–90 min)
- **[10 min] Relembrar o Acordo & Formato**:
  - Projetar a matriz de verificação e os critérios combinados.
  - Explicitar o timebox e a ordem das apresentações.
- **[50 min] Rodadas de Apresentações e Avaliações**:
  - Timebox rígido por equipe (ex.: 5 min de pitch + 3 min de perguntas/comentários).
  - Outras equipes e avaliadores preenchem a folha estruturada em tempo real.
- **[10 min] Encerramento & Lançamento de Pontos em Tempo Real**:
  - **O Impacto Imediato**: Durante os 10 minutos finais, o professor e monitores consolidam as marcações na planilha mestre.
  - Os estudantes saem da sala vendo os pontos creditados no seu painel privado, sentindo a recompensa direta do trabalho entregue.

### 3. Painel de Maestria da Turma
- **Centralização da Vida Prática**: O painel reúne o calendário, links dos enunciados, checkpoints de entrega, matrizes de verificação e o histórico de pontos.
- **Privacidade e Proteção Psicológica**:
  - Cada equipe/aluno acessa o seu estado de maestria e critérios pendentes.
  - Proibição absoluta de ranqueamentos públicos nominais que geram ansiedade e desistência.

### 4. Condução da Banca Final com Especialistas (Arco 4)
- Enviar previamente aos jurados convidados a **Folha de Banca** estruturada contendo as 4 dimensões essenciais:
  1. *Relevância e Autenticidade do Problema*: O problema é real e afeta uma comunidade identificável?
  2. *Rigor e Funcionalidade da Solução*: O software/modelo funciona ao vivo ou é mero protótipo estático?
  3. *Comunicação e Capacidade de Síntese*: O pitch foi persuasivo, técnico e dentro do tempo?
  4. *Defesa e Domínio Técnico na Arguição*: A equipe domina as decisões de engenharia tomadas?

---

## Checklist de Auditoria

- `[ ]` Os critérios de avaliação foram disponibilizados antes do início dos trabalhos?
- `[ ]` A avaliação é baseada em critérios atômicos e binários (feito / não feito)?
- `[ ]` A aula avaliativa reserva os 10 minutos finais para lançamento e feedback imediato?
- `[ ]` O painel protege a privacidade individual e evita ranqueamentos tóxicos?
- `[ ]` Há ciclos formativos de ressubmissão orientados por feedback antes da nota final?
- `[ ]` A banca examinadora externa utiliza folha de avaliação padronizada e confiável ($\alpha \ge 0.75$)?
