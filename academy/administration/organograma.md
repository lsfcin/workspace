# Organograma e Estrutura Institucional (DC / UFRPE)
> Mapa visual e estrutural das unidades, secretarias, comissões deliberativas e atores acadêmicos do Departamento de Computação.

## 1. Mapa de Governança e Relações Institucionais

```mermaid
graph TD
    PREG["Pró-Reitoria de Ensino de Graduação (PREG)"]
    
    subgraph UFRPE_DC ["Departamento de Computação (DC - 11.01.60)"]
        Chefia["Chefia do DC"]
        SEC_DC["Secretaria do DC (SEC-DC)<br/>• Stéphane Farias Alves<br/>• Lenina Figueiredo de Oliveira"]
        CTA["Conselho Técnico-Administrativo (CTA.DC)<br/><i>Deliberação Colegiada / Homologação</i>"]
        CAPR["Comissão de Avaliação Docente (CAPR/DC)<br/><i>PDA / RAD</i>"]
        
        subgraph Subunidades ["Áreas Docentes / Grupos de Trabalho"]
            DOCENTES["Grupo DOCENTES.DC<br/><i>Pareceristas</i>"]
            SI["Sistemas de Informação (SI-DC)<br/>• Lucas Silva Figueiredo<br/>• Lucas Albertins de Lima"]
            SFC["Sistemas e Fundamentos (SFC-DC)<br/>• Rafael Ferreira Leite de Mello"]
            OutrosDoc["Docentes DC<br/>• Sidney Nogueira<br/>• Fernando Aires<br/>• Ricardo Souza<br/>• Marcos Cardoso"]
        end
    end

    subgraph Coordenacoes ["Coordenações de Curso (PREG)"]
        CCBCC["Coord. Bacharelado em Ciência da Computação (CCBCC)<br/>• Sandra Cândida Xavier"]
        CCLC["Coord. Licenciatura em Computação (CCLC)<br/>• Lucas Silva Figueiredo (Coord.)"]
    end

    subgraph Externos ["Departamentos Parceiros"]
        DL["Departamento de Letras (DL)<br/>• SEC-DL: Ray Matheus R. Silva<br/>• Docente: Leane P. Cordeiro (LIBRAS)"]
    end

    PREG --> CCBCC
    PREG --> CCLC
    PREG --> Chefia
    Chefia --- CTA
    Chefia --> SEC_DC
    SEC_DC --> DOCENTES
    DOCENTES --> SI
    DOCENTES --> SFC
    DOCENTES --> OutrosDoc
    CTA --- CAPR
    CCBCC <-->|Processos SIPAC| SEC_DC
    CCLC <-->|Processos SIPAC| SEC_DC
    CCBCC <-->|Demandas de Letras| DL
```

---

## 2. Instâncias e Comissões Recorrentes

| Instância / Colegiado | Natureza | Composição Principal | Atribuição Típica |
| :--- | :--- | :--- | :--- |
| **CTA (Conselho Técnico-Administrativo)** | Deliberativa Departamental | Chefia do DC, representantes docentes de cada subunidade e coordenações. | Homologação final de pareceres de equivalência, aprovação de PDA/RAD, afastamentos e matérias administrativas. |
| **NDE (Núcleo Docente Estruturante)** | Consultiva / Propositiva | Docentes do curso (BCC / LC). | Atualização pedagógica do PPC, reformulação de matriz curricular e ementas. |
| **Colegiado de Curso** | Deliberativa de Curso | Coordenador do curso, docentes e representação discente. | Deliberações sobre matrículas, trancamentos, recursos e diretrizes específicas do curso. |
| **CAPR / DC** | Comissão Setorial | Comissão de docentes designada por portaria. | Pareceres sobre Planos Docentes de Atividades (PDA) e Relatórios de Atividades Docentes (RAD). |
| **Secretaria do DC (`SEC-DC`)** | Executiva / Operacional | Stéphane Alves, Lenina Oliveira. | Triagem no SIPAC, protocolo, tramitação de processos, preparação de pautas de reuniões do CTA. |
| **Secretaria do BCC (`CCBCC`)** | Executiva de Curso | Sandra Xavier. | Atendimento discente, autuação de processos de aproveitamento e registro de despachos no SIGAA. |
