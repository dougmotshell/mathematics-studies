---
description: Classifica a tarefa recebida e define a cadeia mínima de agents do /dev-loop (quais etapas rodam, quais agents, o que roda em paralelo, o que é pulado). Usar como primeira etapa de qualquer loop de d…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `task-router` (definido em @.claude/agents/task-router.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`task-router`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
