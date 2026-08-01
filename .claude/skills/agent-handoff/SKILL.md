---
name: agent-handoff
description: Transfere uma tarefa em andamento entre CLIs (Claude Code, Codex, Copilot, Gemini) usando .agent-handoff.md como contrato compartilhado. Usar ao trocar de ferramenta no meio de um trabalho.
---

# Handoff entre CLIs

Cada CLI tem sessão e memória próprias. O contrato de transferência é um arquivo no
repositório — nunca a expectativa de que o outro agente "lembre".

## Ao entregar (agente que está saindo)

1. `bash tools/agent-handoff.sh init` (não sobrescreve handoff existente).
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
