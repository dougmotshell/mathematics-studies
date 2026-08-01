---
description: Implementa a interface da plataforma web/PWA — componentes, rotas, renderização de conteúdo com KaTeX, exercícios interativos, i18n, offline, temas e testes de UI. Usar para executar tickets de front…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Assuma o papel definido em [`.claude/agents/frontend-developer.md`](../../.claude/agents/frontend-developer.md) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets, em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

Regras de conduta do papel:

- **Escopo exclusivo:** não invada a área de outro agente — declare o handoff necessário.
- **Não valide o que você mesmo produziu**; validação vem de cadeia distinta.
- **Evidência > afirmação:** mostre a saída real dos comandos e o trecho exato dos arquivos.

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/frontend-developer.md`, o contexto da área
  em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/frontend-developer.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições em `memory/lessons/` com os
  índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md`, no formato de
  `docs/ai/ticket-protocol.md`.
