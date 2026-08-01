---
description: Cria exercícios, quizzes e avaliações com feedback diagnóstico, dicas progressivas, solução passo a passo e metadados (tipo, dificuldade, habilidade, tempo estimado), conforme docs/content/exercise-s…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-ai-adapters -->

Delegue ao subagent `exercise-designer` (definido em @.claude/agents/exercise-designer.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`exercise-designer`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
