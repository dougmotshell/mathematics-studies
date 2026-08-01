---
description: Produz e mantém a documentação interna do projeto (docs/) nos padrões do repositório — ADRs, specs, C4, padrões de conteúdo, READMEs e índices. Usar para escrever, reorganizar ou corrigir documentaçã…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `docs-writer` (definido em @.claude/agents/docs-writer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`docs-writer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
