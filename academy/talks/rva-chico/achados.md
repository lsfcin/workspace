# Achados da varredura — o que entra no deck

> Ciclo 2 do plano da palestra de 03/09/2026. Cada item: **o que é · por que é diferentona · a
> linhagem**. Lucas rege o que sobe. Fontes conferidas em página de prêmios da conferência, não em
> título de busca.

## A linhagem — o slide central

**A pergunta do redirected walking não morreu: ela generalizou.**

Em 2018–19 a pergunta era *"quanto dá pra torcer o caminho da pessoa sem ela perceber?"*. Em 2026 o
**Best Paper do IEEE VR** é `How Much Is Too Much? Comfort Envelopes for Distortions in Virtual
Reality Interaction` (Hayeon Kim, In-Kwon Lee) — a mesma pergunta, agora sobre **qualquer** distorção
da interação, não só a do caminho. O campo trocou o truque pela lei.

E a escola do próprio redirected walking mudou de alvo: **Frank Steinicke**, um dos nomes fundadores
da técnica, assina o **Best Paper do ISMAR 2025** — `Negotiated User-to-Group Teleportations in
Social VR`. O problema deixou de ser *uma* pessoa numa sala e virou *várias* pessoas se
coordenando. Locomoção virou problema social.

Reforço: `Collaborative Navigation Improves Spatial Learning Across Symmetric and Asymmetric
Locomotion in VR` (IEEE VR 2026, menção honrosa) e `Walking in the Wild: Safe and Natural Redirected
Walking in Open Physical Spaces` (2025) — a técnica saiu do laboratório para o espaço aberto.

---

## Frente C — sem óculos nenhum (a mais forte, e a mais barata de fazer)

**O dado que abre o bloco: dois dos cinco Best Papers do IEEE VR 2026 são projeção — nenhum
headset envolvido.**

1. **`Shadowless Projection Mapping for Tabletop Workspaces with Synthetic Aperture Projector`**
   (IEEE VR 2026, **Best Paper**) — projeção sobre a mesa que **não faz sombra da sua própria mão**.
   *Linhagem:* é o neto direto do IllumiRoom (slide 126, de 2013), e resolve o problema que matava
   projeção interativa.
2. **`Setup-Independent Full Projector Compensation`** e **`High-Contrast Projection Mapping under
   Light Field Illumination`** (IEEE VR 2026) — projetar em qualquer superfície, sem calibrar.
3. **`Viewpoint-Tolerant Depth Perception for Shared Extended Space Experience on Wall-Sized
   Display`** (ISMAR 2025, **Best Paper**) — *linhagem:* é o **fishtank VR dos slides 64–66**,
   trinta anos depois, resolvido para **várias pessoas ao mesmo tempo** (o fishtank clássico só
   funcionava para uma cabeça).
4. **`Cam-2-Cam: Dual-Camera Interactions for Smartphone-based AR`** (CHI 2025) — usar as **duas**
   câmeras do celular ao mesmo tempo: o mundo na traseira, o seu rosto na frontal.
5. **`TangiAR: Markerless Tangible Input with Everyday Objects`** e **`MobileBiHap: Bi-Manual
   Interaction and Haptic Feedback Using Smartphones`** — objeto qualquer vira controle; celular
   vira háptico.

**Por que esta frente é a que muda o comportamento da turma:** todo aluno na sala já tem o hardware.

---

## Frente B — a máquina que finalmente entende (resposta ao slide 56)

1. **`When LLMs Recognize Your Space: Experiences with Spatially Aware LLM Agents`** (ISMAR 2025,
   **Best Paper**) — o agente sabe que aquilo é uma mesa, não uma malha de triângulos.
   *É literalmente a tese do `spacemantics`, premiada.* O slide 55–56 pergunta "quem deve entender
   quem?"; a resposta de 2026 é que a máquina agora pode ser o lado que entende.
2. **O padrão de fato virou `olhar + pinçar`** — o survey *Towards spatial computing: recent
   advances in multimodal natural interaction for XR headsets* (2025) mostra gesto (24 artigos) e
   olhar (13) como os dois eixos dominantes, com o Vision Pro tendo fixado o par como método
   primário. E o velho problema do olhar continua com o nome de sempre: **Midas touch**.
3. **Fala explodiu em 2024 por causa dos LLMs** — o mesmo survey registra o salto, e aponta
   *silent speech* (reconhecer fala sem vocalizar) como direção nova.
4. **`Facilitating Exploration of Linearly Aligned Objects in Controller-Free 3D Environment with
   Gaze and Microgestures`** (ISMAR 2025) — microgesto no lugar do controle.

---

## Frente E — o papel da IA na interação (o tema que o deck não tem)

Quatro camadas, e o valor está em separá-las:

| Camada | O que a IA faz | Evidência premiada |
|---|---|---|
| **Percepção** | rastrear mão, corpo, olhar | é rede neural hoje, não visão clássica — é o que fez o Mágico de Oz (slide 81) virar desnecessário |
| **Compreensão de cena** | saber *o que* é aquilo | `When LLMs Recognize Your Space` (ISMAR'25 Best Paper) |
| **Geração** | criar mundo, movimento, som sob demanda | `Dynamic Worlds, Dynamic Humans: Generating Virtual Human-Scene Interaction Motion in Dynamic Scenes` (IEEE VR'26 **Best Paper**) · `Tuning Immersion with Adaptive Generative Music in VR` |
| **Intenção** | inferir o que a pessoa quer | fala + LLM no laço; `ExciteVR`, que usa LLM para **explicar e mitigar cybersickness** |

Bônus para o bloco social: **`The Impact of AI-Based Real-Time Gesture Generation on the Perception
of Others and Interaction Quality in Social XR`** (ISMAR 2025) — o seu avatar gesticula sozinho, e
isso muda o que as pessoas acham de você.

Captura por **gaussian splatting** já é infraestrutura, não pesquisa exótica: `GSReuse` (IEEE VR'26)
e `Fast Digitization in XR of Reality-Linked Gaussian-Splatted Proxies` (Steven Feiner, Best Demo
menção honrosa).

---

## Frente F — Niantic, com o grau de certeza de cada afirmação

O slide 39 já mostra a Niantic escaneando 10 milhões de lugares com jogadores como "câmeras
humanas". O desfecho, em três níveis de certeza — **e a força do slide está justamente em separá-los:**

- **Fato, confirmado pela empresa:** os escaneamentos de jogadores de Pokémon Go e Ingress
  **treinaram** o *Large Geospatial Model* da Niantic Spatial — cinco anos de construção, mais de 30
  bilhões de imagens, feito para posicionar **onde não há GPS**.
- **Fato, público:** em **dezembro de 2025** a Niantic Spatial fechou parceria com a **Vantor**
  (ex-Maxar Intelligence), empresa de defesa, mirando **operações de drones sem GPS**. A Vantor tem
  contrato de até **US$ 217 milhões com o Exército dos EUA** (fev/2025) para terreno 3D imersivo.
- **Negado pelas duas empresas:** que os escaneamentos do Pokémon Go tenham sido **transferidos**
  para a Vantor.

**A pergunta que fica de pé mesmo com a negativa, e que é o slide:** *você jogou Pokémon Go. O mapa
que você ajudou a fazer treinou um modelo que hoje é vendido para posicionar sem GPS. Você foi
perguntado?*

---

## Ato 1 — o bloco de crises ganhou uma literatura inteira

Isto não existia quando o deck foi escrito: **privacidade e segurança em RV/RA viraram área.**

1. **`Detecting Visual Information Manipulation Attacks in Augmented Reality`** (ISMAR 2025,
   **Best Paper**) — dá para **mentir para os olhos de alguém** em RA, e já existe pesquisa em como
   detectar. É o slide que fecha o bloco de crises com uma ameaça nova, não com uma manchete velha.
2. **`p-Blend: Privacy-Preserving Blendshape Perturbation Against Re-identification Attacks in VR`**
   — o **jeito como seu rosto se mexe** te identifica.
3. **`Casual-VRAuth`** — o **jeito como você se mexe** é sua senha (e, portanto, sua digital).
4. **`Visceral Notices and Privacy Mechanisms for Eye Tracking in AR`** — o rastreio de olhar sabe
   demais, e ninguém avisa.
5. **`How Harassment Shapes Embodiment and Self-Identification in Social VR`** (IEEE VR 2026,
   menção honrosa) — assédio em RV social muda a percepção que a pessoa tem de si.

---

## Frente D — impacto social, e o argumento da restrição

**O caso-âncora, que não é RA de propósito: o M-Pesa (Quênia, 2007).**
Funciona em **qualquer** celular por menu de texto **USSD**, com recibo por SMS, **sem internet**.
Usou os revendedores de crédito que já existiam como rede de agentes. Não venceu por ser avançado —
venceu por resolver o problema real (trabalhador urbano mandando dinheiro para a família no campo)
com a infraestrutura que já estava lá.

**A lição para a turma do Chico:** projetar **para** a restrição, e não **apesar** dela. É a resposta
antecipada ao aluno que diz "mas eu não tenho um Quest".

O mesmo princípio, já dentro de XR:

1. **`LiteAT: A Data-Lightweight and User-Adaptive VR Telepresence System for Remote Education`**
   (ISMAR 2025) — telepresença em RV **projetada para internet ruim**. É o M-Pesa da RV.
2. **`Adaptive Augmented Reality Pathfinding for Parkinson's Disease`** (ISMAR 2025, **Best
   Poster**) — RA que ajuda pessoa com Parkinson a **voltar a andar**. E é um pôster: escala de
   projeto de aluno.
3. **`Portable Silent Room: VR for Anxiety and Emotion Regulation for Neurodivergent Women and
   Non-Binary Individuals`** e **`'I was truly able to express the image of myself that I have
   within': VR Group Therapy with the LGBTQIA+ community`** (ambos ISMAR 2025) — RV para quem o
   mundo físico não acomoda.
4. Pesquisa de RV/RA/TUI **na África** existe e tem venue próprio (*African HCI Conference*):
   treinamento médico em RV na Nigéria, ferramentas de RA na África do Sul, patrimônio interativo
   com interface tangível no Quênia.

---

## Diferentonas — as que existem só para dar "como assim?"

1. **`Multisensory In-Car VR: Repurposing the Vehicle's HVAC System and Power Seat for Immersive
   Haptic Feedback`** (ISMAR 2025, **Best Demo**) — o **ar-condicionado do carro** vira háptica.
   Semente pronta de operador E SE: *e se o hardware que você já tem fosse o dispositivo?*
2. **`52-Hz Whale Song: An Embodied VR Experience for Exploring Misunderstanding and Empathy`**
   (CHI 2026) — a baleia que canta numa frequência que nenhuma outra escuta.
3. **`Objestures: Everyday Objects Meet Mid-Air Gestures`** (CHI 2026) — qualquer objeto na mesa
   entra no gesto.
4. **`MetaRoundWorm`** (ISMAR 2025) — escape room em RV sobre o ciclo de vida de um parasita.
5. **`From Slides to Space: Interactive Scale Navigation for XR Presentations`** (IEEE VR 2026,
   Best 3DUI Contest, grupo do **Doug Bowman**) — apresentação que é espaço, não sequência. Piada
   pronta: é o que este deck deveria ser.

---

## Sobras

- `papers --ss` devolveu **HTTP 429** (limite do Semantic Scholar) — a varredura foi feita pelas
  páginas de prêmios das conferências, que é fonte melhor de qualquer forma. Vale registrar o 429
  como issue da ferramenta.
