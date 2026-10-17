# tweaks
> Como configurar as máquinas e os apps de Lucas. Inclui a proteção Ubuntu/Brave,
> seus arquivos, diagnóstico e remoção; cada ajuste registra a decisão.

Um ajuste entra aqui quando sobrevive a formatar a máquina — se é para fazer uma vez e esquecer, é tarefa, não tweak. Ajuste ainda não decidido fica em `## a decidir` até virar passo.

## a decidir

### Brave — atalhos de busca por site na barra de endereço

No Chrome o Lucas usava atalhos de uma letra: digitar `y` + Tab abre a busca do YouTube dentro da própria barra de endereço. O Brave tem o mesmo recurso; ativar é o passo fácil.

**O trabalho é a lista, não a ativação.** Atalho de uma letra é recurso escasso — cada letra gasta vale um serviço que ele usa toda semana. Certos: **Maps** e **Google Tradutor**. Em dúvida:
**Amazon**, **Mercado Livre**, **ChatGPT**. Decidir a lista com ele antes de configurar (INBOX 2026-08-24).

### Ubuntu / Windows — Atalho global de STT (Speech-to-Text) com invocação de agente

Configurar atalho de teclado global de sistema no Ubuntu (e posteriormente no Windows) com gravação de áudio e dupla ação: (1) transcrição direta via STT onde o cursor estiver; (2) ativação de agente autônomo do WOS caso o áudio inicie com "bot ...". Avaliar STT do Antigravity (com revisão contextual e correção de siglas) vs. Whisper/aiwbot (INBOX 2026-10-01/02).

## Ubuntu / Brave — voz e Foundry

### Estado e motivo

Conferido em **2026-10-17**, no `DELL-G15-LSF-UBUNTU`, usuário `lucas`: Ubuntu 26.04.1 LTS, kernel 7.0.0-38-generic, 16 GB de memória de acesso aleatório (RAM). Este bloco é o registro permanente da intervenção; atualizar aqui quando ela mudar.

Com Discord e Foundry no Brave, o computador apresentava crescimento de memória, congelamento do mouse e áudio, encerramento da sessão e eventuais reinícios. Não há confirmação de vazamento. Os registros anteriores incluem falta de memória e erros NVIDIA; a relação entre eles permanece sem diagnóstico conclusivo.

**É uma proteção personalizada, não uma configuração oferecida pelo Brave.** Usa recursos nativos do Linux e do gerenciador de serviços systemd, no âmbito deste usuário. O Brave instalado continua sendo o pacote oficial; foi atualizado para 1.97.56 durante a intervenção. A proteção não modifica os binários do pacote, os drivers, a swap nem a proteção interna do navegador (sandbox). Memória comprimida em RAM (zram) foi adiada.

O teto anterior de 2816 mebibytes (MiB), aproximadamente 3 GB, foi retirado: os registros de 17/out às 16:21 e 17:48 confirmam encerramentos por esse limite local (`CONSTRAINT_MEMCG`), sem demonstrar esgotamento global. O orçamento fixo do jogo também foi removido. **Não restaurar esses tetos como se fossem a política atual.**

### Regra atual e uso

- O monitor `brave-memory-watch.service` inicia no login e é acionado também pelo lançador. Reinicia em caso de falha; sua prontidão é verificada antes de abrir o navegador.
- A cada 250 milissegundos consulta `MemAvailable`, a estimativa do Linux de RAM disponível sem precisar recorrer à swap, incluindo cache recuperável. Abaixo de **1 gibibyte (GiB), aproximadamente 1,07 GB**, inicia a intervenção. Isso não corresponde exatamente a “15 GB usados” no gráfico.
- Encerra primeiro o grupo do Foundry. Dá um segundo para o encerramento normal e, se a memória continuar baixa, força a saída dos remanescentes. Espera o grupo esvaziar e uma nova leitura antes de considerar o Brave com Discord.
- A recuperação para pelo menos 1 GiB cancela a escalada pendente. Se o jogo não estiver aberto e a memória estiver abaixo do limiar, o Brave de voz/navegação é a opção restante. O monitor escolhe esses alvos mesmo que outro aplicativo tenha causado a falta de memória.
- Os grupos não têm teto fixo de RAM. O limiar é um ponto de reação: um aumento rápido, atraso do monitor ou processo preso no driver pode impedir a liberação a tempo. Os mecanismos próprios do Ubuntu ainda podem agir antes dele.

**Discord:** usar o Brave normal. **Jogo:** abrir pelo atalho **Foundry - Brave**, que usa um diretório de dados independente. Links clicados dentro do Discord web abrem no navegador da voz; se abrir o jogo dessa forma, ele não fica separado. Fechar o grupo da voz encerra todas as suas janelas e abas, não apenas o Discord.

Nas partidas, manter VS Code/Claude e fechar ChatGPT/Antigravity conforme a escolha de Lucas. Não mudar de navegador, instalar outro cliente Discord nem alterar swap ou drivers sem uma nova avaliação.

### Arquivos envolvidos

Todos os caminhos abaixo pertencem ao usuário `lucas`; `~` significa `/home/lucas`.

| Caminho | Função |
|---|---|
| `~/.local/share/brave-protecao/launch.py` | Abre as duas instâncias, exige o monitor ativo, mantém os processos no grupo correto e limpa a configuração temporária ao sair. |
| `~/.local/share/brave-protecao/watch.py` | Contém o limiar (`THRESHOLD`), intervalo (`INTERVAL`), espera (`GRACE`) e ordem dos alvos (`ROLES`). |
| `~/.local/share/brave-protecao/installation.json` | Relação dos oito arquivos instalados com resumos de integridade; a remoção recusa arquivos alterados. Não editar só para contornar essa verificação. |
| `~/.local/share/brave-protecao/undo.py` | Remove a instalação conferida, após fechar todos os processos Brave, preservando os dados dos perfis. |
| `~/.local/share/brave-protecao/foundry-profile/` | Dados persistentes do navegador do jogo; não apagar para remover a proteção. |
| `~/.config/systemd/user/brave-memory-watch.service` | Serviço do monitor, habilitado em `default.target.wants/` para os próximos logins. |
| `~/.config/systemd/user/app-brave.slice` e `app-foundry.slice` | Grupos irmãos da voz/navegação e do jogo; ambos com `MemoryMax=infinity`. |
| `~/.local/share/applications/brave-browser.desktop` | Substituição local do atalho oficial, encaminhando abertura normal, nova janela e janela privada ao lançador. |
| `~/.local/share/applications/foundry-brave.desktop` | Atalho do jogo com seu endereço; consultar aqui o endereço atual, sem duplicá-lo neste documento. |

O lançador adapta em memória a última chamada do script oficial `/usr/bin/brave-browser`, preservando o restante do preparo do pacote. Isso mantém o identificador de processo (PID) durante a abertura. Chromium cria um grupo para seu processo principal; uma configuração temporária **apenas para aquele PID** coloca esse grupo junto dos filhos, fora do grupo da interface do Ubuntu. Não há alteração genérica aplicada a todos os aplicativos Chromium.

As identidades e travas temporárias ficam em `$XDG_RUNTIME_DIR/brave-protecao/` e `foundry-protecao/`; a configuração por processo fica em `$XDG_RUNTIME_DIR/systemd/user/app-org.chromium.Chromium-<PID>.scope.d/50-brave-protecao.conf`. O lançador cria serviços `brave-protegido-<identificador>.service` e remove somente o que pertence àquela abertura. O monitor confere o grupo dos processos e usa identificadores estáveis antes de sinalizá-los.

### Como conferir ou investigar uma falha

Executar no terminal da sessão de `lucas`, sem `sudo`. Para um agente em ambiente isolado, a inspeção precisa acessar a sessão real do computador.

```bash
systemctl --user status brave-memory-watch.service --no-pager
systemctl --user is-enabled brave-memory-watch.service
systemctl --user show app-brave.slice app-foundry.slice -p MemoryMax -p DropInPaths -p ControlGroup
journalctl --user -u brave-memory-watch.service --since today --no-pager
free -h
```

Esperado: monitor `active (running)` e `enabled`, os dois `MemoryMax=infinity`, sem configurações adicionais em `DropInPaths`. Um grupo sem navegador aberto pode não ter `ControlGroup`. `EffectiveMemoryMax` pode mostrar a RAM física mesmo sem teto configurado; não exigir que seja `infinity`. No grupo ativo, o arquivo `/sys/fs/cgroup<ControlGroup>/memory.max` deve conter `max`; conferir também os ancestrais se houver suspeita de limite herdado.

O registro do monitor informa alvo, RAM disponível em MiB, quantidade de processos sinalizados e eventual encerramento forçado. Se o Brave fechar **sem** um registro correspondente, investigar também o serviço de abertura, a própria aplicação e os mecanismos do Ubuntu; não atribuir automaticamente ao limiar:

```bash
journalctl --user --since today --no-pager -g 'brave-protegido|oom|memory'
journalctl -k -b --no-pager -g 'oom-kill|Out of memory|NVRM: Xid'
```

Se houve reinício, repetir a segunda consulta com `-b -1` para o boot anterior, quando os registros estiverem disponíveis. Uma atualização que mude o formato do lançador oficial pode fazer `launch.py` recusar a abertura; revisar a adaptação, sem desativar o sandbox. Se o monitor falhou, consultar seus registros antes de reiniciá-lo com `systemctl --user restart brave-memory-watch.service`.

### Alterar ou remover

Para ajustar o limiar, revisar `watch.py`, testar a ordem com valores de memória simulados e processos descartáveis, atualizar a integridade dos arquivos intencionalmente alterados em `installation.json` e reiniciar o serviço. Não ocupar 15 GB de RAM só para testar. Atualizar este bloco junto da mudança.

Para remover toda a intervenção, **fechar primeiro todas as instâncias do Brave**, incluindo o jogo, e executar:

```bash
python3 ~/.local/share/brave-protecao/undo.py
```

O procedimento confere os arquivos, desabilita o monitor, encerra os grupos vazios e remove os arquivos rastreados e o manifesto. A remoção do atalho local devolve a abertura ao atalho oficial do pacote. Não desinstala nem rebaixa o Brave; preserva o perfil normal e `foundry-profile/`. Se recusar por arquivo alterado, comparar a alteração antes de decidir como remover; não apagar diretórios de perfil como atalho.

Parar somente o serviço não desfaz a intervenção: uma nova abertura pelo lançador pode iniciá-lo novamente. Os scripts instalados ficam fora deste repositório; antes de formatar ou migrar a máquina, preservar os arquivos listados em `installation.json`, o próprio manifesto e os dados de perfil necessários. Este documento não é um instalador, e arquivos em `/tmp` não são uma fonte durável para reinstalação.

### Evidência e pendências

Monitor ativo e habilitado, integridade dos oito arquivos conferida e tetos removidos também no kernel em 17/out. Testes com leituras simuladas e grupos descartáveis verificaram o limiar, a ordem, a recuperação sem encerrar voz, o encerramento forçado e a preservação de um processo externo. Os dois modos do lançador passaram pela consulta de versão. O áudio do Discord foi validado com outra pessoa em 14/out; o Foundry real não foi aberto nestes testes.

A próxima partida deve validar a separação com VS Code/Claude aberto e acompanhar a memória disponível. Vazamento e falha NVIDIA seguem sem solução confirmada. Acompanhamento em [rpg-isoroll](../../brain/goals/rpg-isoroll.md); modelos ociosos em `code/aiwbot/ROADMAP.md`.
