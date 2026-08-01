---
description: Revisa rigor matemático — definições, enunciados, demonstrações, contra-exemplos, hipóteses omitidas e gabaritos de exercícios. Usar antes de publicar qualquer conteúdo e sempre que houver dúvida sob…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `math-reviewer` (definido em @.claude/agents/math-reviewer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`math-reviewer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
