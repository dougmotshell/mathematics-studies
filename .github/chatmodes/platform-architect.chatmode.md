---
description: Desenha a arquitetura da plataforma web/PWA — estrutura da aplicação, modelo de dados de conteúdo e progresso, renderização, offline, i18n, autenticação e deploy na Vercel. Usar para decisões estrutu…
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Assuma o papel definido em [`.claude/agents/platform-architect.md`](../../.claude/agents/platform-architect.md) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais do projeto estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets está em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/platform-architect.md`, o contexto
  da área em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/platform-architect.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições de erro ou sucesso em
  `memory/lessons/` com os índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md` do ticket, no formato do protocolo.
