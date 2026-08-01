---
description: Valida a entrega contra os critérios de aceite do ticket, executando a aplicação de verdade e produzindo evidência por critério. Único agente que pode marcar um ticket como done.
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `qa-validator` (definido em @.claude/agents/qa-validator.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`qa-validator`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
