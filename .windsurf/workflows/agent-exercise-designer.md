---
description: Cria exercícios, quizzes e avaliações com feedback diagnóstico, dicas progressivas, solução passo a passo e metadados (…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /agent-exercise-designer

Cria exercícios, quizzes e avaliações com feedback diagnóstico, dicas progressivas, solução passo a passo e metadados (tipo, dificuldade, habilidade, tempo estimado), conforme docs/content/exercise-s…

## Passos

1. Abra e leia integralmente `.claude/agents/exercise-designer.md` — ele define o papel, o escopo exclusivo, os
   limites e o que este agente **não** faz.
2. Leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/exercise-designer.md`, o contexto da área
   em `memory/context/` e `docs/errors/README.md`.
3. Se o trabalho pertence a um ticket, leia `docs/ai/ticket-protocol.md` e o
   `tickets/TCK-NNNN-<slug>/log.md` correspondente.
4. Execute a tarefa **assumindo o papel**, respeitando o escopo exclusivo: trabalho da área
   de outro agente exige handoff, não execução direta.
5. Não valide artefato que você mesmo produziu. Apresente evidência real do resultado.
6. Ao concluir, atualize `memory/agents/exercise-designer.md` e registre lições em
   `memory/lessons/` com os índices; em ticket, registre a entrada no `log.md`.
