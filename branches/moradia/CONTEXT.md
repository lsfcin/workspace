# Moradia
> Cockpit de onde o Lucas mora: o aluguel atual (apto 305, Rua Cassilândia 67, CTI Imobiliária), a saída dele e a casa
> seguinte (Rua Eduardo Dubeux 24A). Goal: [moradia](../../brain/goals/moradia.md).

## Aluguel atual — apto 305, Edf. Praça dos Jacarandás, Rua Cassilândia 67, Várzea

Fonte: contrato 5506 (DocuSign/Owli, assinado 19/11/2024) e vistoria de entrada de 14/11/2024, em [`docs/`](docs/).
CPFs, RGs, conta Neoenergia e sequencial do IPTU: `segredos.env`.

| Item | Valor | Cláusula |
|------|-------|----------|
| Locador | J de Vasconcelos Aragão Filho & Cia, representada pela CTI Imobiliária | p. 1 |
| Fiadores | Marcos (pai) e Verônica, Rua Eduardo Dubeux 22 — respondem até a entrega das chaves | 15, 15.3 |
| Prazo | 36 meses, 05/12/2024 → 04/12/2027; chaves recebidas 22/11/2024 | p. 1 |
| Aluguel | R$ 1.700,00 + R$ 3,00 tarifa de boleto, pago **vencido**; vencimento mudou do dia 5 para o **dia 15** no boleto de 15/09/2026 (pagou R$ 566,66 pelos 10 dias da troca). Desde então 15/MM paga 15→14 do mês anterior. Atrasar devolve o vencimento ao dia 5 | p. 1, 6.1 |
| Reajuste | IGP-M a cada 12 meses; próximo em jan/2027 (boleto) | 4.1 |
| Fundo de reserva | é do proprietário: a CTI desconta do boleto o que você pagou no condomínio (−R$ 14,93 em set/2026) | — |
| Multa rescisória | 3 aluguéis proporcionais ao prazo restante — **isenta após 18 meses** (05/06/2026) com aviso formal de 30 dias | p. 1, Ressalva |
| Encargos do inquilino | condomínio, água, luz, gás, IPTU, taxa de bombeiro, seguro incêndio anual (parcela única) | 5, 13 |
| Devolução | limpo, vago, no estado recebido, salvo desgaste normal; reparos com mesma marca e padrão | 3, 7.1, 7.2 |
| Luz/água | dar baixa do nome na Neoenergia/Compesa ao sair é dever do inquilino | 12.1 |
| Proibido | furar cerâmica/porcelanato de cozinha, varanda, área de serviço e banheiros | Ressalva |
| Caução | não houve (confirmado pela CTI em 17/10/2026) | — |

Condomínio: DAC Administradora, unidade 0305, vence dia 10; o valor varia. Os boletos pararam de chegar no Gmail pessoal em nov/2025.

Contatos CTI: rescisão → raquel.gusmao@ctiimobiliaria.com.br e administrativo1@ctiimobiliaria.com.br;
financeiro (boletos) → boleto@ctiimobiliaria.com, WhatsApp 81 99111-5133; administrativo → WhatsApp 81 99292-5743.
Condomínio: ADM DAC 81 8649-2717; portaria 81 8944-6205.

## Saída
Plano, conta e checklist: [`saida-cassilandia.md`](saida-cassilandia.md). Conversa com a CTI: [`conversas/cti.txt`](conversas/cti.txt).

## Próxima casa — Rua Eduardo Dubeux 24A, Várzea
Casa alugada; a 24 foi dividida em três. Fica em frente à casa do pai e perto da obra das [casinhas](../casinhas/CONTEXT.md), mas é outro lugar. O contrato novo entra em `docs/` quando for assinado.

## Google Drive — espelho
[`branches/moradia/`](https://drive.google.com/drive/folders/1sR13uw1vIay4Xbek1BCGqlJHkP4DHbdK) na conta `personal`, com as mesmas subpastas (`docs/`, `conversas/`) e os mesmos nomes de arquivo. O git guarda o texto; o Drive guarda os PDFs, as 145 fotos da vistoria de entrada (`docs/2024-11-14_vistoria-entrada-fotos.zip`) e uma cópia em Google Doc de `saida-cassilandia.md`, para ler no celular. Documento novo, como o termo de entrega ou o contrato da casa nova, vai nos dois lugares, com nome `AAAA-MM-DD_<item>`. `segredos.env` nunca sobe.

PDFs e twins com CPF ficam fora do git (`.gitignore`).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`docs/`](docs/CONTEXT.md) | — |

| File | Description |
|------|-------------|
| [`conversas/cti.txt`](conversas/cti.txt) | WhatsApp com a CTI Imobiliária (Débora) sobre a saída do apto 305 |
| [`saida-cassilandia.md`](saida-cassilandia.md) | Saída do apto 305 — entrega das chaves seg 16/11/2026 |
<!-- routing:end -->
