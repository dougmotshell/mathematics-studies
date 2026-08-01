---
description: Audita segurança e privacidade — dados de menores (LGPD/COPPA), autenticação, regras de acesso, segredos, dependências e superfície de ataque. Usar em tickets sensíveis e em auditorias periódicas.
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Assuma o papel definido em [`.claude/agents/security-auditor.md`](../../.claude/agents/security-auditor.md) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais do projeto estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets está em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/security-auditor.md`, o contexto
  da área em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/security-auditor.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições de erro ou sucesso em
  `memory/lessons/` com os índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md` do ticket, no formato do protocolo.
