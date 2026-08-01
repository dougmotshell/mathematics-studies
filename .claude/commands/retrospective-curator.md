---
description: Fecha o ciclo de trabalho — atualiza memory/agents/, registra lições em memory/lessons/, erros em docs/errors/ e mantém os índices (MEMORY.md, LESSONS.md) consistentes. Usar como última etapa do /dev…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Delegue ao subagent `retrospective-curator` (definido em @.claude/agents/retrospective-curator.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`retrospective-curator`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
