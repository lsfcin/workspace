# tweaks
> Como configurar as máquinas e os apps de Lucas; cada ajuste registra a decisão.

Um ajuste entra aqui quando sobrevive a formatar a máquina — se é para fazer uma vez e esquecer, é tarefa, não tweak. Ajuste ainda não decidido fica em `## a decidir` até virar passo.

## a decidir

### Brave — atalhos de busca por site na barra de endereço

No Chrome o Lucas usava atalhos de uma letra: digitar `y` + Tab abre a busca do YouTube dentro da própria barra de endereço. O Brave tem o mesmo recurso; ativar é o passo fácil.

**O trabalho é a lista, não a ativação.** Atalho de uma letra é recurso escasso — cada letra gasta vale um serviço que ele usa toda semana. Certos: **Maps** e **Google Tradutor**. Em dúvida:
**Amazon**, **Mercado Livre**, **ChatGPT**. Decidir a lista com ele antes de configurar (INBOX 2026-08-24).

### Ubuntu / Windows — Atalho global de STT (Speech-to-Text) com invocação de agente

Configurar atalho de teclado global de sistema no Ubuntu (e posteriormente no Windows) com gravação de áudio e dupla ação: (1) transcrição direta via STT onde o cursor estiver; (2) ativação de agente autônomo do WOS caso o áudio inicie com "bot ...". Avaliar [Hex](https://github.com/anomalyco/hex) (overlay global de teclado para STT) como referência de arquitetura, comparando STT do Antigravity vs. Whisper/aiwbot (INBOX 2026-10-01/02, 2026-11-02).

## Memória — earlyoom e zram (proteção global contra travamento)

### Motivo e decisão (2026-11-05)
Com 14 GB de RAM física e base de ~6.6 GB em uso no login, cargas de desenvolvimento com múltiplos agentes e inferência local (Whisper, modelos de visão ou compilações) esgotavam a memória e levavam o Ubuntu a congelamento completo por *I/O thrashing* (leitura/escrita desesperada no `/swap.img` em disco) antes que o OOM killer nativo do kernel pudesse agir. Brave com Discord e Foundry era o caso mais frequente.

Três camadas, todas padrão do Ubuntu, sem ajuste próprio (decisão 2026-11-10: manter os padrões):
1. **`zram-config`**: swap compactada na RAM (`/dev/zram0`, prioridade 5, acima do `/swap.img` com -1); a paginação acontece na velocidade da memória, sem saturar o disco.
2. **`systemd-oomd`** (já vem no Ubuntu): encerra o grupo de aplicativo com mais pressão quando a sessão do usuário passa 20 s acima de 50% de pressão de memória.
3. **`earlyoom`** (`EARLYOOM_ARGS="-r 3600"` em `/etc/default/earlyoom`): encerra o processo de maior consumo quando RAM **e** swap livres caem abaixo de 10%.

Rejeitado: a proteção caseira do Brave (grupos systemd próprios, monitor em Python e lançador que reescrevia `/usr/bin/brave-browser`), removida em 2026-11-10. Só cobria o navegador e quebrava os apps do Brave abertos fora dela. Não reinstalar.

### Instalação e verificação
```bash
sudo apt update && sudo apt install -y earlyoom zram-config
sudo systemctl enable --now earlyoom
```

Conferência:
```bash
systemctl status earlyoom systemd-oomd
swapon --show
```
Deve exibir `/dev/zram0` com prioridade maior que `/swap.img`. Depois de um app fechar sozinho, ver quem agiu: `journalctl -u earlyoom -u systemd-oomd --since today` e `journalctl -k -g oom-kill`.

