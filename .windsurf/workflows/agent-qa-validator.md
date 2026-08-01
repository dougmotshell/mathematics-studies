---
description: Valida a entrega contra os critérios de aceite do ticket, executando a aplicação de verdade e produzindo evidência por…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /agent-qa-validator

Valida a entrega contra os critérios de aceite do ticket, executando a aplicação de verdade e produzindo evidência por critério. Único agente que pode marcar um ticket como done.

## Passos

1. Abra e leia integralmente `.claude/agents/qa-validator.md` — ele define o papel, o escopo exclusivo, os
   limites e o que este agente **não** faz.
2. Leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/qa-validator.md`, o contexto da área
   em `memory/context/` e `docs/errors/README.md`.
3. Se o trabalho pertence a um ticket, leia `docs/ai/ticket-protocol.md` e o
   `tickets/TCK-NNNN-<slug>/log.md` correspondente.
4. Execute a tarefa **assumindo o papel**, respeitando o escopo exclusivo: trabalho da área
   de outro agente exige handoff, não execução direta.
5. Não valide artefato que você mesmo produziu. Apresente evidência real do resultado.
6. Ao concluir, atualize `memory/agents/qa-validator.md` e registre lições em
   `memory/lessons/` com os índices; em ticket, registre a entrada no `log.md`.
