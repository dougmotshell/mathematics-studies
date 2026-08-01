---
description: Implementa a camada de dados e serviços — persistência de progresso, sincronização, autenticação, APIs, pipeline de build do conteúdo e integrações. Usar para executar tickets de backend/dados.
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `backend-developer` (definido em @.claude/agents/backend-developer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`backend-developer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
