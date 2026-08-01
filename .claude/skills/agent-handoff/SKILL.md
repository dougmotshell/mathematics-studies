---
name: agent-handoff
description: Transfere uma tarefa em andamento entre CLIs (Claude Code, Codex, Copilot, Gemini) usando .agent-handoff.md como contrato compartilhado. Usar ao trocar de ferramenta no meio de um trabalho.
---

# Handoff entre CLIs

Cada CLI tem sessão e memória próprias. O contrato de transferência é um arquivo no
repositório — nunca a expectativa de que o outro agente "lembre".

## Quando trocar: medir o contexto antes de perder o detalhe

A compactação automática do Claude Code é **lossy**: quando ela dispara, o detalhe já se
perdeu. Meça antes com `python3 tools/context-watch.py` (só Claude Code — ver adiante).

| Zona | Uso | Exit code | O que fazer |
|---|---|---|---|
| verde | < 60% | `0` | seguir normalmente |
| atenção | < 75% | `10` | evitar releitura de arquivos grandes; preferir trechos |
| preparar | < 85% | `20` | `bash tools/agent-handoff.sh snapshot --force` |
| crítico | ≥ 85% | `30` | handoff agora: snapshot + `validate`, depois trocar de CLI |
| sem telemetria | — | `40` | a ferramenta não expõe uso de contexto; **não** estimar |

Quando checar: antes de tarefas longas, depois de ler arquivos grandes, e ao retomar
trabalho. O hook `PostToolBatch` avisa sozinho **quando a zona sobe** (nunca a cada
chamada). O hook `PreCompact` (matcher `auto`) grava o snapshot antes da compactação.
Os hooks avisam e escrevem — **trocar de ferramenta continua sendo decisão do usuário**.

**Declare a janela antes de confiar no percentual:** sem configuração, a janela é presumida
a partir do id do modelo, que não distingue a variante de 200k da de 1M. Nesse caso o script
presume a **menor** janela (mais alarme, nunca silêncio); se a própria medição refutar essa
presunção (`usado > janela`), ele sobe um degrau e **anuncia a refutação** em vez de imprimir
um número que o dado desmente. Em ambos os casos `janela_confiavel` é `false` e o hook
declara isso uma vez por sessão. Para acabar com o palpite, crie
`.claude/settings.local.json` (gitignored, por máquina) com `{"autoCompactWindow": 1000000}`
— vale para terminal, hook e `snapshot`. `export CONTEXT_WINDOW=…` **não** alcança o hook.

`bash tools/agent-handoff.sh snapshot` preenche o handoff com estado real (branch, HEAD,
`git status`, `git diff --stat`, tickets fora de `done` com a última entrada do `log.md`,
dev-loop ativo, comandos de verificação e a medição de contexto). Ele **não** inventa
intenção: as seções `<preencher>` continuam sendo trabalho do agente.

**Ferramentas sem telemetria (Codex, Copilot, Gemini e web):** nenhuma expõe o uso de
contexto e o script sai com `40` — número inventado sobre contexto restante é pior que
número nenhum. O procedimento honesto é por *proxy*: fazer o snapshot em marcos (fim de
cada etapa, antes de ler qualquer arquivo grande, a cada ~10 trocas de mensagem) e ao
primeiro sintoma de degradação (a ferramenta esquece decisão já tomada, repete pergunta
respondida, ignora restrição do início). Detalhes: `docs/ai/cross-agent-handoff.md`.

## Ao entregar (agente que está saindo)

1. `bash tools/agent-handoff.sh snapshot` (estado real, sem digitação) ou
   `bash tools/agent-handoff.sh init` (template em branco). Nenhum dos dois sobrescreve um
   handoff existente — `snapshot --force` sobrescreve e guarda o anterior em
   `.agent-handoff.prev.md`.
2. Preencha `.agent-handoff.md` com **todas** as seções obrigatórias:
   - **Objetivo** — o que a tarefa deve alcançar
   - **Estado atual** — o que está pronto e o que falta, sem otimismo
   - **Arquivos alterados** — caminhos + o que mudou em cada um
   - **Decisões técnicas** — o que foi decidido e por quê (e o que foi descartado)
   - **Testes** — o que rodou, com a saída real (inclusive falhas)
   - **Problemas ou riscos** — o que pode morder o próximo agente
   - **Próxima ação exata** — o comando/arquivo/passo imediato, sem ambiguidade
   - **Restrições** — o que **não** pode ser feito (ex.: não commitar, não renomear slug)
   - **Última atualização** — data absoluta + qual CLI produziu
3. `bash tools/agent-handoff.sh validate`.
4. Não faça commit, push ou stash sem pedido explícito. Deixe o working tree como está.

## Ao receber (agente que está entrando)

1. Leia, nesta ordem: `.agent-handoff.md` → `AGENTS.md` → `memory/MEMORY.md` →
   `docs/errors/README.md`.
2. Inspecione `git status --short` e `git diff` — **não reverta** trabalho alheio.
3. Confirme que entendeu a "Próxima ação exata"; se estiver ambígua, pergunte ao usuário
   antes de agir.
4. Ao concluir ou ao passar adiante, **atualize o mesmo arquivo** (não crie outro).

## Regras

- Apenas **um agente** edita o working tree por vez.
- Se a tarefa faz parte de um `/dev-loop`, cite `.dev-loop/<task-slug>/loop.md` na
  "Próxima ação exata" — os briefings continuam sendo o contrato entre etapas.
- `.agent-handoff.md` é efêmero e está no `.gitignore`; nada de conhecimento durável deve
  viver só nele — o que for permanente vai para `memory/` ou `docs/`.
- O `context-watch.py` lê o transcript da sessão, que contém a conversa inteira: ele extrai
  **apenas contagens e metadados** e nunca imprime conteúdo. Nada é enviado para fora da
  máquina. Não relaxe isso.
