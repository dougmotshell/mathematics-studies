---
description: Modela progresso, domínio de habilidades, estatísticas de acerto/erro, diagnóstico de lacunas e recomendação do próximo passo do aluno. Usar para definir métricas, eventos de telemetria, relatórios d…
argument-hint: [tarefa ou pergunta para o agente]
---
<!-- managed-by:mathematics-studies/sync-slash-commands -->

Delegue ao subagent `learning-analytics` (definido em @.claude/agents/learning-analytics.md) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`learning-analytics`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
