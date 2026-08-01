---
description: Classifica a tarefa recebida e define a cadeia mínima de agents do /dev-loop (quais etapas rodam, quais agents, o que roda em paralelo, o que é pulado). Usar como primeira etapa de qualquer loop de d…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Assuma o papel definido em [`.claude/agents/task-router.md`](../../.claude/agents/task-router.md) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets, em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

Regras de conduta do papel:

- **Escopo exclusivo:** não invada a área de outro agente — declare o handoff necessário.
- **Não valide o que você mesmo produziu**; validação vem de cadeia distinta.
- **Evidência > afirmação:** mostre a saída real dos comandos e o trecho exato dos arquivos.

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/task-router.md`, o contexto da área
  em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/task-router.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições em `memory/lessons/` com os
  índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md`, no formato de
  `docs/ai/ticket-protocol.md`.
