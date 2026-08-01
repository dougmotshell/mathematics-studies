---
description: Refina pedidos em requisitos claros e critérios de aceite verificáveis, confrontando-os com a visão do produto, o roadm…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /agent-product-analyst

Refina pedidos em requisitos claros e critérios de aceite verificáveis, confrontando-os com a visão do produto, o roadmap e as specs. Usar quando um ticket chega ambíguo ou quando é preciso decidir o…

## Passos

1. Abra e leia integralmente `.claude/agents/product-analyst.md` — ele define o papel, o escopo exclusivo, os
   limites e o que este agente **não** faz.
2. Leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/product-analyst.md`, o contexto da área
   em `memory/context/` e `docs/errors/README.md`.
3. Se o trabalho pertence a um ticket, leia `docs/ai/ticket-protocol.md` e o
   `tickets/TCK-NNNN-<slug>/log.md` correspondente.
4. Execute a tarefa **assumindo o papel**, respeitando o escopo exclusivo: trabalho da área
   de outro agente exige handoff, não execução direta.
5. Não valide artefato que você mesmo produziu. Apresente evidência real do resultado.
6. Ao concluir, atualize `memory/agents/product-analyst.md` e registre lições em
   `memory/lessons/` com os índices; em ticket, registre a entrada no `log.md`.
