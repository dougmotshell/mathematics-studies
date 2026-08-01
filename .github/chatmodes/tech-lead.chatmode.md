---
description: Orquestrador técnico — recebe todo ticket novo, faz triagem, decide a abordagem, delega ao agente certo e desbloqueia loops travados. Ponto de entrada de qualquer tarefa de desenvolvimento, manutençã…
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Assuma o papel definido em [`.claude/agents/tech-lead.md`](../../.claude/agents/tech-lead.md) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais do projeto estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets está em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/tech-lead.md`, o contexto
  da área em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/tech-lead.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições de erro ou sucesso em
  `memory/lessons/` com os índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md` do ticket, no formato do protocolo.
