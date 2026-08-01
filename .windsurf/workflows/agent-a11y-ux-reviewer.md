---
description: Revisa acessibilidade (WCAG 2.2 AA, matemática acessível a leitor de tela, teclado, contraste) e UX de aprendizagem (ca…
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

# /agent-a11y-ux-reviewer

Revisa acessibilidade (WCAG 2.2 AA, matemática acessível a leitor de tela, teclado, contraste) e UX de aprendizagem (carga cognitiva, feedback, navegação, progresso). Usar antes de publicar interface…

## Passos

1. Abra e leia integralmente `.claude/agents/a11y-ux-reviewer.md` — ele define o papel, o escopo exclusivo, os
   limites e o que este agente **não** faz.
2. Leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/a11y-ux-reviewer.md`, o contexto da área
   em `memory/context/` e `docs/errors/README.md`.
3. Se o trabalho pertence a um ticket, leia `docs/ai/ticket-protocol.md` e o
   `tickets/TCK-NNNN-<slug>/log.md` correspondente.
4. Execute a tarefa **assumindo o papel**, respeitando o escopo exclusivo: trabalho da área
   de outro agente exige handoff, não execução direta.
5. Não valide artefato que você mesmo produziu. Apresente evidência real do resultado.
6. Ao concluir, atualize `memory/agents/a11y-ux-reviewer.md` e registre lições em
   `memory/lessons/` com os índices; em ticket, registre a entrada no `log.md`.
