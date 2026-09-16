# SPECS | disciplinas
> metodologia macro semestral de condução, ciclos de projeto, avaliação e acompanhamento.
> governs: todas as disciplinas de graduação e pós ministradas por Lucas (techedu, ai4good, etc)

## objetivos

1. **visão de mundo e de contribuição**
   - *cenário micro:* escutar os alunos, suas histórias, experiências, dificuldades, desejos, visões, como funcionam, como aprendem, quais os perfis.
   - *calibrar visão macro:* conectar com a realidade ampla com foco na verdade, no estudo, na ciência e não em opinião rasa.
   - *reperar agência:* fortalecer a capacidade, a capacidade de atuação, impulsionar a autoestima, coletividade e criatividade.
2. **desenvolvimento de habilidades**
   - *problemáticas:* conectar o ferramental teórico-prático a ser desenvolvido com problemáticas relevantes à atualidade e ao contexto dos alunos.
   - *habilidades técnicas e comportamentais:* definir de antemão o conjunto de habilidades alvo da disciplina.
   - *grafo de conhecimento:* conectar o conjunto de habilidades de forma estruturada, dependências e sinergias.
   - *etapas:* conduzir aprendizagem com instrução direta prévia, entregar starter kits, receitas, passos construtivos explícitos, cada peça conecta com a seguinte. aprendizagem sem mistério, simplicidade como valor central.
   - *verificação:* critérios de avaliação fornecidos de antemão, verificação continuada. permitir ritmos diferentes de aprendizagem. recapitular e reavaliar.
3. **produção de artefatos**
   - *demonstração wow:* conduzir alunos a produzirem soluções com tom de novidade e utilidade que impressionem terceiros que os deixem orgulhosos.
   - *relatório técnico:* desenvolver com rigor metodológico que gere relatórios que vamos submeter para veículos científicos.
   - *apresentação:* para bancas avaliadoras para ter discussão e conexão externa servindo de preparatório para pitchs em editais e eventos.

---

## calendário (4 arcos: ~30 encontros | 15 semanas)

```
[ARCO 1: INICIALIZAÇÃO] (semanas 01–02)
  ├── escuta e partilha de experiências relevantes
  ├── contrato pedagógico e problemáticas alvo
  └── setup instrumental guiado
[ARCO 2: FERRAMENTAL E PROBLEMATIZAÇÃO] (semanas 03–06)
  ├── estudo das técnicas, apropriação, estrapolação
  └── estudo das problemáticas relevantes, macro
[ARCO 3: CICLOS DE CONSTRUÇÃO DA SOLUÇÃO] (semanas 07–12)
  ├── definição de macro-áreas de interesse, para problema e técnica
  ├── prototipação da técnica base, garantir código funcional
  ├── levantamento de competidores, na indústria e academia
  ├── ideação da contribuição para a literatura e sociedade
  ├── diagrama da solução técnica, módulos, entradas e saídas
  ├── definição de métricas e desenho dos experimentos
  ├── desenvolvimento, iterativo incremental, foco no diferencial
  └── aplicação de testes, coleta dos resultados e avaliação
[ARCO 4: PREPARAÇÃO E DEFESA PÚBLICA] (semanas 13–15)
  ├── refinamento geral, solução e experimentos
  ├── revisão e ajustes da demonstração, vídeo que causa efeito wow
  ├── revisão e ajustes do relatório técnico, pronto para submissão
  ├── refinamento da apresentação
  └── banca examinadora e encerramento
```

---

## entregas (metodologia e materiais)

toda entrega (checkpoint) de disciplina é direcionada por dois documentos canônicos (metodologia e materiais), gerados a partir de modelos-base em markdown (.md) estruturados por artefatos:

### anatomia

- **metodologia (`templates/template-metodologia.md`):**
   - grafo de dependência entre os artefatos da entrega (entradas e saídas encadeadas).
   - para cada artefato a ser produzido:
      - racional pedagógico ancorado (Chão $\to$ Horizonte, Doshi & Hauser).
      - entrada, o que precisa estar pronto antes de começar.
      - etapas, construção passo a passo por artefato a ser produzido naquela entrega.
      - saída, o que é esperado do produto, qual sua utilidade.
- **materiais (`templates/template-materiais.md`):**
   - para cada artefato a ser produzido:
      - **modelo:** material de modelo com espaços / lacunas estruturadas com conteúdo guia indicando como deve ser preenchido.
      - **exemplo excelente:** versão do modelo preenchido de forma excelente, gerado através dos passos indicados na metodologia.
      - **exemplo que parece bom mas não é:** versão do modelo preenchido, cumprindo superficialmente o que foi solicitado, alcançando um potencial estado de "entregue" porém sem substância ("sem alma"), entrando na lógica da "educação faz de conta" em que o aluno finge que faz e o professor finge que acredita.

*nota: em cada ponto relevante é recomendado que adicionemos trechos focados no uso de agentes (IAs, harness). tanto no macro quanto no micro, prompts, subprompts, instruções de leitura focadas na IA, instruções de acesso, de forma geral estes documentos são guias explícitos para humanos e para IAs. como os humanos não precisam visualizar a parte específica para as IAs estes trechos devem ser escritos como comentários*

### acesso e edição

em ambos os casos usamos arquivos markdown com **visualização rica** e **edição online**. a **fonte canônica** dos arquivos `.md` fica em `academy/teaching/<disciplina>/` no workspace do professor. a **distribuição** é feita pelo Cloudflare Pages, sendo um espelhamento estático no repositório público `lsf-links` (`outputs/links/`). 

a **visualização rica** focada em humanos e também útil para mobile é acessível online no formato `https://lucassf.pages.dev/<disciplina>/<name>`, sendo renderizado pelo visualizador nativo (`viewer.js` + `viewer.css` + `marked.min.js`), com suporte a alertas GitHub, tabelas responsivas e tema dark/light, sem dependências de CDN externa. também é fornecida uma **visualização direta** pensada para IAs /harnesses, acessível no formato `https://lucassf.pages.dev/<disciplina>/<name>.md` (ou botão "Copiar p/ Agente (RAW)" no topo da página), permitindo ingestão via `curl -s` ou cópia com 1 clique.

a **edição online** (zero custo / zero Limites) é fornecida pelo botão "Editar (github.dev)" na barra superior, abrindo o VS Code no navegador diretamente no arquivo no GitHub. commits vão direto para a branch `main` e o Cloudflare Pages atualiza em segundos.

---

## acompanhamento ("pontos, experiência")

- **painel:**
   - as entregas estarão organizadas e disponibilizadas em um painel para todos.
   - o painel irá conter para cada entrega itens de verificação, escrita clara, feito ou não feito, e uma vez feito acréscimo direto nos pontos do aluno ou da equipe.
   - o painel centraliza toda a parte prática da disciplina, datas, instruções, verificações e pontos. por isso deve se ter um cuidado para garantir acesso e usabilidade para o painel.

---

## análise usando agentes

ao auditar ou planejar a condução de uma disciplina, o agente (harness) deve validar:
1. `[ ]` cada entrega do calendário possui o par de `.md` guiado pelos modelos canônicos
   (`templates/template-metodologia.md` e `templates/template-materiais.md`)?
2. `[ ]` a metodologia decompõe a entrega em artefatos com entradas e saídas explícitas e inclui guias para IAs onde é pertinente?
3. `[ ]` o documento de materiais cobre a tríade modelo, exemplo excelente e exemplo quase bom, acompanhada de anotações críticas do professor para cada artefato?
4. `[ ]` o fluxo prático macro está consistente? entradas e saídas entre entregas se encaixam bem?
5. `[ ]` o fluxo didático macr está consistente? conteúdos teóricos estão vinculados corretamente à prática? 
6. `[ ]` todos os conteúdos estão publicados no com páginas de visualização rica e endpoints RAW para harnesses de agentes?
